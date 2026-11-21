# Changelog

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
