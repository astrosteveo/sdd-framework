#!/usr/bin/env python3
"""
Spec Validator - Validates SDL specifications for completeness and quality.
Outputs a validation report with coverage score (0-100).
"""

import sys
import re
from pathlib import Path
import yaml


class SpecValidator:
    """Validates SDL specification files."""

    def __init__(self, spec_path: Path):
        self.spec_path = spec_path
        self.content = spec_path.read_text()
        self.frontmatter = {}
        self.body = ""
        self.issues = []
        self.warnings = []
        self.suggestions = []
        self.scores = {}

    def extract_frontmatter(self):
        """Extract YAML frontmatter from spec."""
        parts = self.content.split("---", 2)
        if len(parts) < 3:
            self.issues.append("Missing YAML frontmatter (must start with ---)")
            return False

        try:
            self.frontmatter = yaml.safe_load(parts[1])
            self.body = parts[2].strip()
            return True
        except yaml.YAMLError as e:
            self.issues.append(f"Invalid YAML syntax: {e}")
            return False

    def validate_format(self) -> int:
        """Validate format and return score (0-20)."""
        score = 20

        # Required fields
        required = ["spec_id", "name", "version", "status"]
        for field in required:
            if field not in self.frontmatter:
                self.issues.append(f"Missing required field: {field}")
                score -= 5

        # spec_id format
        if "spec_id" in self.frontmatter:
            if not re.match(r'^SPEC-[A-Z]+-\d{3}$', self.frontmatter["spec_id"]):
                self.issues.append(f"Invalid spec_id format: {self.frontmatter['spec_id']}")
                score -= 5

        # version semver
        if "version" in self.frontmatter:
            if not re.match(r'^\d+\.\d+\.\d+$', self.frontmatter["version"]):
                self.issues.append(f"Invalid semver: {self.frontmatter['version']}")
                score -= 5

        # status value
        if "status" in self.frontmatter:
            if self.frontmatter["status"] not in ["draft", "approved", "implemented"]:
                self.warnings.append(f"Unexpected status: {self.frontmatter['status']}")
                score -= 2

        return max(0, score)

    def validate_completeness(self) -> int:
        """Validate completeness and return score (0-30)."""
        score = 30

        # User stories
        if "## User Stories" not in self.body:
            self.issues.append("Missing User Stories section")
            score -= 6
        else:
            user_stories = len(re.findall(r'\*\*US-\d+\*\*:', self.body))
            if user_stories == 0:
                self.warnings.append("No user stories defined")
                score -= 4
            elif user_stories == 1:
                self.suggestions.append("Consider adding more user stories")
                score -= 2

        # Acceptance criteria
        if "## Acceptance Criteria" not in self.body:
            self.issues.append("Missing Acceptance Criteria section")
            score -= 6
        else:
            criteria = len(re.findall(r'\*\*AC-\d+\*\*:', self.body))
            if criteria == 0:
                self.warnings.append("No acceptance criteria defined")
                score -= 4
            elif criteria == 1:
                self.suggestions.append("Consider adding more acceptance criteria")
                score -= 2

        # Data models
        if "## Data Models" not in self.body:
            self.warnings.append("Missing Data Models section")
            score -= 4
        else:
            models = len(re.findall(r'interface \w+|class \w+|type \w+ struct', self.body))
            if models == 0:
                self.warnings.append("No data models defined")
                score -= 3

        # Edge cases
        if "## Edge Cases" not in self.body:
            self.issues.append("Missing Edge Cases section")
            score -= 6
        else:
            edge_cases = len(re.findall(r'\*\*EC-\d+\*\*:', self.body))
            if edge_cases < 3:
                self.warnings.append(f"Only {edge_cases} edge cases defined (recommend ≥5)")
                score -= 3

        # Non-functional requirements
        if "## Non-Functional Requirements" not in self.body:
            self.warnings.append("Missing Non-Functional Requirements section")
            score -= 4

        # Success metrics
        if "## Success Metrics" not in self.body:
            self.suggestions.append("Consider adding Success Metrics section")
            score -= 2

        return max(0, score)

    def validate_testability(self) -> int:
        """Validate testability and return score (0-25)."""
        score = 25

        # Find all acceptance criteria
        ac_pattern = r'\*\*AC-\d+\*\*:.*?(?=\*\*AC-\d+\*\*:|##|\Z)'
        criteria = re.findall(ac_pattern, self.body, re.DOTALL)

        if not criteria:
            self.warnings.append("No acceptance criteria found to test")
            return 0

        # Check for Given/When/Then structure
        testable_count = 0
        for criterion in criteria:
            has_given = "Given" in criterion or "**Given**" in criterion
            has_when = "When" in criterion or "**When**" in criterion
            has_then = "Then" in criterion or "**Then**" in criterion

            if has_given and has_when and has_then:
                testable_count += 1

        testability_ratio = testable_count / len(criteria)

        if testability_ratio < 0.5:
            self.issues.append(f"Only {testable_count}/{len(criteria)} criteria use Given/When/Then")
            score -= 15
        elif testability_ratio < 0.8:
            self.warnings.append(f"{testable_count}/{len(criteria)} criteria use Given/When/Then")
            score -= 8
        elif testability_ratio < 1.0:
            self.suggestions.append(f"{testable_count}/{len(criteria)} criteria use Given/When/Then")
            score -= 3

        return max(0, score)

    def validate_edge_cases(self) -> int:
        """Validate edge case coverage and return score (0-15)."""
        score = 15

        # Check for taxonomy categories
        categories = {
            "Boundary": ["boundary", "empty", "null", "min", "max"],
            "Security": ["security", "injection", "xss", "auth"],
            "Concurrency": ["concurrency", "race", "simultaneous"],
            "State": ["state", "transition", "expired"],
            "Performance": ["performance", "timeout", "large"]
        }

        coverage = {}
        body_lower = self.body.lower()

        for category, keywords in categories.items():
            coverage[category] = any(keyword in body_lower for keyword in keywords)

        covered = sum(coverage.values())

        if covered == 0:
            self.issues.append("No edge case categories covered")
            score = 0
        elif covered < 3:
            self.warnings.append(f"Only {covered}/5 edge case categories covered")
            score -= 9
        elif covered < 5:
            self.suggestions.append(f"{covered}/5 edge case categories covered")
            score -= 3

        return max(0, score)

    def validate_dependencies(self) -> int:
        """Validate dependencies and return score (0-10)."""
        score = 10

        if "dependencies" not in self.frontmatter:
            return score

        deps = self.frontmatter["dependencies"]
        if not isinstance(deps, list):
            self.issues.append("Dependencies must be an array")
            return 0

        # Check for circular dependencies (basic check)
        spec_id = self.frontmatter.get("spec_id", "")
        if spec_id in deps:
            self.issues.append(f"Circular dependency: {spec_id} depends on itself")
            score -= 10

        # Check format
        for dep in deps:
            if not re.match(r'^SPEC-[A-Z]+-\d{3}$', dep):
                self.warnings.append(f"Invalid dependency format: {dep}")
                score -= 2

        return max(0, score)

    def calculate_score(self) -> int:
        """Calculate total validation score."""
        self.scores["Format"] = self.validate_format()
        self.scores["Completeness"] = self.validate_completeness()
        self.scores["Testability"] = self.validate_testability()
        self.scores["Edge Cases"] = self.validate_edge_cases()
        self.scores["Dependencies"] = self.validate_dependencies()

        return sum(self.scores.values())

    def generate_report(self) -> str:
        """Generate validation report."""
        spec_id = self.frontmatter.get("spec_id", "UNKNOWN")
        total_score = sum(self.scores.values())

        if total_score >= 80:
            status = "✅ PASS"
            recommendation = "APPROVE - Ready for implementation"
        elif total_score >= 60:
            status = "⚠️  WARNING"
            recommendation = "REVISE - Address issues before implementation"
        else:
            status = "❌ FAIL"
            recommendation = "REJECT - Significant revisions required"

        report = f"""# Validation Report: {spec_id}

**Score**: {total_score}/100
**Status**: {status}
**File**: {self.spec_path.name}

"""

        if self.issues:
            report += "## 🔴 Critical Issues\n\n"
            for issue in self.issues:
                report += f"- {issue}\n"
            report += "\n"

        if self.warnings:
            report += "## ⚠️  Warnings\n\n"
            for warning in self.warnings:
                report += f"- {warning}\n"
            report += "\n"

        if self.suggestions:
            report += "## 💡 Suggestions\n\n"
            for suggestion in self.suggestions:
                report += f"- {suggestion}\n"
            report += "\n"

        report += "## 📊 Coverage Breakdown\n\n"
        for category, score in self.scores.items():
            max_score = {
                "Format": 20,
                "Completeness": 30,
                "Testability": 25,
                "Edge Cases": 15,
                "Dependencies": 10
            }[category]

            if score == max_score:
                icon = "✅"
            elif score >= max_score * 0.7:
                icon = "⚠️ "
            else:
                icon = "❌"

            report += f"- {icon} **{category}**: {score}/{max_score}\n"

        report += f"\n## 🎯 Recommendation\n\n**{recommendation}**\n"

        if total_score < 80:
            report += "\n### Next Steps\n\n"
            if self.issues:
                report += "1. Fix all critical issues\n"
            if self.warnings:
                report += "2. Address warnings\n"
            if self.suggestions:
                report += "3. Consider suggestions for improvement\n"
            report += "4. Re-run validation\n"

        return report

    def validate(self) -> bool:
        """Run full validation and return success status."""
        if not self.extract_frontmatter():
            return False

        total_score = self.calculate_score()
        print(self.generate_report())

        return total_score >= 80


def main():
    """Main entry point."""
    if len(sys.argv) != 2:
        print("Usage: spec_validator.py <spec-file.md>", file=sys.stderr)
        sys.exit(1)

    spec_path = Path(sys.argv[1])

    if not spec_path.exists():
        print(f"Error: File not found: {spec_path}", file=sys.stderr)
        sys.exit(1)

    validator = SpecValidator(spec_path)
    success = validator.validate()

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
