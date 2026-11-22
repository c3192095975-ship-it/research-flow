from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "check_quality.py"


class CheckQualityTests(unittest.TestCase):
    def run_check(self, manuscript: str, claims: str, evidence: str, require_markers: bool = False) -> subprocess.CompletedProcess:
        with tempfile.TemporaryDirectory() as td:
            base = Path(td)
            (base / "manuscript.md").write_text(manuscript, encoding="utf-8")
            (base / "claims.csv").write_text(claims, encoding="utf-8")
            (base / "evidence.csv").write_text(evidence, encoding="utf-8")
            cmd = [
                sys.executable, str(SCRIPT),
                "--manuscript", str(base / "manuscript.md"),
                "--claims", str(base / "claims.csv"),
                "--evidence", str(base / "evidence.csv"),
            ]
            if require_markers:
                cmd.append("--require-markers")
            return subprocess.run(cmd, capture_output=True, text=True)

    def test_valid_claim_chain(self) -> None:
        result = self.run_check(
            "A supported claim {{C001}}.\n",
            "claim_id,section_id,paragraph_id,figure_id,claim_text,evidence_ids,support_strength,allowed_wording,status,notes\nC001,1,1,,Claim text,E1,strong,descriptive,supported,\n",
            "evidence_id,source_id,claim_id,locator,verification_status\nE1,S1,C001,p.1,verified\n",
            require_markers=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_placeholder_and_unknown_marker_fail(self) -> None:
        result = self.run_check(
            "TODO {{C999}}.\n",
            "claim_id,section_id,paragraph_id,figure_id,claim_text,evidence_ids,support_strength,allowed_wording,status,notes\nC001,1,1,,Claim text,E1,strong,descriptive,supported,\n",
            "evidence_id,source_id,claim_id,locator,verification_status\nE1,S1,C001,p.1,verified\n",
        )
        self.assertEqual(result.returncode, 1)
        self.assertIn("placeholder", result.stdout)
        self.assertIn("C999", result.stdout)


if __name__ == "__main__":
    unittest.main()
