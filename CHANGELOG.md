# Changelog

## 3.5.0

- Added research design profiles: experimental, quantitative_observational, qualitative, systematic_review, theoretical, methods, and case_analysis.
- Added argument outline between evidence and drafting.
- Added claim IDs, section/paragraph/figure mapping, and `{{C001}}` manuscript markers.
- Added evidence-to-text impact analysis and recorded backtracking.
- Added executable `check_quality.py` checks for claim IDs, evidence IDs, placeholders, and CSV completeness.
- Fixed phase naming to include `reading` and `argument_outline`.
- Added claim traceability, research-design, and checker tests.

## 3.4.0

- Added quality tiers: course_pass, course_high, research_standard, publication_standard, and custom.
- Separated artifact profile from quality level.
- Added auto-inference and conflict rules, including course_report + research_standard and publication-standard boundaries.
- Added quality-tier-aware pre-write gate, capability depth, and Gate A-F applicability.
- Added quality-tier handoff fields and contract tests.

## 3.3.0

- Added artifact profiles: manuscript, course_report, proposal, thesis, and presentation.
- Added a FULL-mode pre-write gate covering capability map, evidence, rubric, claim boundary, and writing owner.
- Added style_audit and similarity_precheck capability slots.
- Added A-F artifact quality gates and profile applicability rules.
- Clarified that local AI-style and similarity checks are not Turnitin results.
- Added course-report routing, exclusions, and contract tests.

## 3.2.0

- Added a Triage Gate before skill discovery.
- Added BYPASS, LIGHT, and FULL operating modes.
- Added high-risk override so short citation, statistics, ethics, and submission tasks cannot bypass necessary checks.
- Updated capability maps, handoff schemas, user guide, and architecture documentation for triage.

## 3.1.0

- Added multi-signal capability discovery using metadata, script names, reference headings, and README excerpts.
- Added `manifest.yaml` and `agents/openai.yaml` fallback for nonstandard skill layouts.
- Added dependency preflight and `availability` states.
- Added user and project overrides.
- Added a portable baseline protocol for environments without research skills.
- Added duplicate resolution, capability map schemas, and validation tests.
- Added MIT license, user guide, architecture documentation, contribution guide, and GitHub Actions workflow example.

## 3.0.0

- Switched from fixed skill names to capability-slot routing.
- Added filesystem discovery and local skill catalog generation.

## 2.1.0

- Added route locking, phase contracts, quality gates, and conflict arbitration.

## 2.0.0

- Introduced the ResearchFlow orchestrator and handoff schemas.
