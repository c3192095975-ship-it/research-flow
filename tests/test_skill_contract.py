from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class SkillContractTests(unittest.TestCase):
    def test_version_and_profiles(self) -> None:
        text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn('version: "3.3.0"', text)
        for profile in ("manuscript", "course_report", "proposal", "thesis", "presentation"):
            self.assertIn(profile, text)
        self.assertIn("pre-write gate", text)

    def test_quality_gate_reference(self) -> None:
        text = (ROOT / "references" / "quality-gates.md").read_text(encoding="utf-8")
        for gate in ("Gate A", "Gate B", "Gate C", "Gate D", "Gate E", "Gate F"):
            self.assertIn(gate, text)
        self.assertIn("不等于 Turnitin", text)

    def test_profile_reference(self) -> None:
        text = (ROOT / "references" / "artifact-profiles.md").read_text(encoding="utf-8")
        self.assertIn("Profile: course_report", text)
        self.assertIn("FULL 模式在任何正式写作前必须确认", text)


if __name__ == "__main__":
    unittest.main()
