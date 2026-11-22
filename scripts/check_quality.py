#!/usr/bin/env python3
"""Deterministic quality checks for ResearchFlow artifacts.

Checks claim IDs, evidence IDs, placeholders, and basic CSV completeness.
It does not judge scientific correctness or replace Turnitin.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path


CLAIM_MARKER_RE = re.compile(r"\{\{\s*(C[^}\s]+)\s*\}\}")
PLACEHOLDER_RE = re.compile(r"\b(TODO|TBD|FIXME|AUTHOR_INPUT_NEEDED|UNVERIFIED)\b|\[placeholder\]", re.I)
VALID_CLAIM_STATUS = {"supported", "partially_supported", "unsupported", "needs_author_input"}
VALID_EVIDENCE_STATUS = {"verified", "unverified", "needs_source", "author_input_needed", "not_applicable"}


@dataclass
class Report:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    files: dict[str, str] = field(default_factory=dict)
    claim_ids: list[str] = field(default_factory=list)
    markers: list[str] = field(default_factory=list)
    evidence_ids: list[str] = field(default_factory=list)
    checked_files: list[str] = field(default_factory=list)

    def error(self, message: str) -> None:
        self.errors.append(message)

    def warn(self, message: str) -> None:
        self.warnings.append(message)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(newline="", encoding="utf-8-sig", errors="replace") as handle:
        reader = csv.DictReader(handle)
        rows = [dict(row) for row in reader]
        return list(reader.fieldnames or []), rows


def split_ids(value: str) -> list[str]:
    if not value:
        return []
    return [item.strip() for item in re.split(r"[;,|\s]+", value) if item.strip()]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run deterministic ResearchFlow quality checks.")
    parser.add_argument("--manuscript", help="Markdown or text manuscript path")
    parser.add_argument("--claims", help="claim-evidence CSV path")
    parser.add_argument("--evidence", help="evidence-ledger CSV path")
    parser.add_argument("--outline", help="argument-outline Markdown path")
    parser.add_argument("--require-markers", action="store_true", help="Require every claim_id to appear in the manuscript")
    parser.add_argument("--format", choices=["text", "json"], default="text")
    parser.add_argument("--output", help="Optional report output path")
    args = parser.parse_args(argv)

    if not any([args.manuscript, args.claims, args.evidence, args.outline]):
        parser.error("provide at least one input file")

    report = Report()

    manuscript_text = ""
    if args.manuscript:
        path = Path(args.manuscript).expanduser()
        report.checked_files.append(str(path))
        if not path.is_file():
            report.error(f"manuscript not found: {path}")
        else:
            manuscript_text = read_text(path)
            report.files["manuscript"] = str(path)
            for match in PLACEHOLDER_RE.finditer(manuscript_text):
                line = manuscript_text.count("\n", 0, match.start()) + 1
                report.error(f"placeholder found in manuscript line {line}: {match.group(0)}")
            report.markers = sorted(set(CLAIM_MARKER_RE.findall(manuscript_text)))

    evidence_ids: set[str] = set()
    evidence_rows: list[dict[str, str]] = []
    if args.evidence:
        path = Path(args.evidence).expanduser()
        report.checked_files.append(str(path))
        if not path.is_file():
            report.error(f"evidence ledger not found: {path}")
        else:
            report.files["evidence"] = str(path)
            fields, evidence_rows = read_csv(path)
            if not evidence_rows:
                report.error("evidence ledger is empty")
            id_field = "evidence_id" if "evidence_id" in fields else "source_id"
            if id_field not in fields:
                report.error("evidence ledger needs evidence_id or source_id")
            if "verification_status" not in fields:
                report.warn("evidence ledger has no verification_status column")
            for index, row in enumerate(evidence_rows, start=2):
                evidence_id = (row.get(id_field) or "").strip()
                if not evidence_id:
                    report.error(f"evidence ledger row {index} has empty {id_field}")
                    continue
                if evidence_id in evidence_ids:
                    report.error(f"duplicate evidence_id: {evidence_id}")
                evidence_ids.add(evidence_id)
                status = (row.get("verification_status") or "").strip().lower()
                if status and status not in VALID_EVIDENCE_STATUS:
                    report.warn(f"unknown evidence status at row {index}: {status}")
                if status in {"unverified", "needs_source", "author_input_needed"}:
                    report.error(f"evidence {evidence_id} is not verified: {status}")
            report.evidence_ids = sorted(evidence_ids)

    claims: list[dict[str, str]] = []
    claim_ids: set[str] = set()
    if args.claims:
        path = Path(args.claims).expanduser()
        report.checked_files.append(str(path))
        if not path.is_file():
            report.error(f"claim register not found: {path}")
        else:
            report.files["claims"] = str(path)
            fields, claims = read_csv(path)
            required = {"claim_id", "claim_text", "evidence_ids", "status"}
            missing = required - set(fields)
            for item in sorted(missing):
                report.error(f"claim register missing column: {item}")
            for index, row in enumerate(claims, start=2):
                claim_id = (row.get("claim_id") or "").strip()
                if not claim_id:
                    report.error(f"claim register row {index} has empty claim_id")
                    continue
                if claim_id in claim_ids:
                    report.error(f"duplicate claim_id: {claim_id}")
                claim_ids.add(claim_id)
                if not (row.get("claim_text") or "").strip():
                    report.error(f"claim {claim_id} has empty claim_text")
                status = (row.get("status") or "").strip().lower()
                if status and status not in VALID_CLAIM_STATUS:
                    report.warn(f"claim {claim_id} has unknown status: {status}")
                if status == "unsupported":
                    report.error(f"claim {claim_id} is unsupported")
                ids = split_ids(row.get("evidence_ids") or "")
                if not ids:
                    report.error(f"claim {claim_id} has no evidence_ids")
                for evidence_id in ids:
                    if evidence_ids and evidence_id not in evidence_ids:
                        report.error(f"claim {claim_id} references unknown evidence_id: {evidence_id}")
                locations = [row.get("section_id"), row.get("paragraph_id"), row.get("figure_id")]
                if not any((value or "").strip() for value in locations):
                    report.warn(f"claim {claim_id} has no section/paragraph/figure location")
            report.claim_ids = sorted(claim_ids)

    if args.require_markers and claim_ids:
        missing_markers = sorted(claim_ids - set(report.markers))
        for claim_id in missing_markers:
            report.error(f"claim marker missing from manuscript: {claim_id}")
    elif claim_ids and manuscript_text:
        for marker in report.markers:
            if marker not in claim_ids:
                report.error(f"manuscript marker has no claim register entry: {marker}")
        missing_markers = sorted(claim_ids - set(report.markers))
        for claim_id in missing_markers:
            report.warn(f"claim has no manuscript marker: {claim_id}")

    if args.outline:
        path = Path(args.outline).expanduser()
        report.checked_files.append(str(path))
        if not path.is_file():
            report.error(f"argument outline not found: {path}")
        else:
            text = read_text(path)
            report.files["outline"] = str(path)
            for required in ("Question", "Core claim", "Supporting evidence", "Limitation"):
                if required.lower() not in text.lower():
                    report.warn(f"argument outline missing recommended field: {required}")

    status = "pass" if not report.errors else "fail"
    payload = {"status": status, **asdict(report)}
    if args.format == "json":
        output = json.dumps(payload, ensure_ascii=False, indent=2)
    else:
        lines = [f"status: {status}"]
        lines.append(f"checked_files: {len(report.checked_files)}")
        lines.append(f"errors: {len(report.errors)}")
        lines.extend(f"- {item}" for item in report.errors)
        lines.append(f"warnings: {len(report.warnings)}")
        lines.extend(f"- {item}" for item in report.warnings)
        output = "\n".join(lines)
    print(output)
    if args.output:
        out = Path(args.output).expanduser()
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(output + "\n", encoding="utf-8")
    return 0 if status == "pass" else 1


if __name__ == "__main__":
    sys.exit(main())
