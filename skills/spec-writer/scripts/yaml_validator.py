#!/usr/bin/env python3
"""
YAML validator for SDL spec frontmatter.
Validates that YAML parses correctly and contains required fields.
"""

import sys
import yaml
from pathlib import Path


REQUIRED_FIELDS = ["spec_id", "name", "version", "status"]
OPTIONAL_FIELDS = [
    "dependencies",
    "validators",
    "test_fixtures",
    "integration_hooks",
    "composed_of",
    "metadata"
]


def extract_frontmatter(spec_file: Path) -> str:
    """Extract YAML frontmatter from spec file."""
    content = spec_file.read_text()

    if not content.startswith("---"):
        raise ValueError("Spec file must start with YAML frontmatter (---)")

    # Find the closing ---
    parts = content.split("---", 2)
    if len(parts) < 3:
        raise ValueError("Invalid YAML frontmatter format")

    return parts[1].strip()


def validate_yaml(frontmatter: str) -> dict:
    """Parse and validate YAML structure."""
    try:
        data = yaml.safe_load(frontmatter)
    except yaml.YAMLError as e:
        raise ValueError(f"Invalid YAML syntax: {e}")

    if not isinstance(data, dict):
        raise ValueError("YAML frontmatter must be a dictionary")

    return data


def validate_required_fields(data: dict) -> None:
    """Check that all required fields are present."""
    missing = [field for field in REQUIRED_FIELDS if field not in data]

    if missing:
        raise ValueError(f"Missing required fields: {', '.join(missing)}")


def validate_spec_id_format(spec_id: str) -> None:
    """Validate spec_id follows SPEC-[DOMAIN]-[NUMBER] format."""
    import re

    pattern = r'^SPEC-[A-Z]+-\d{3}$'
    if not re.match(pattern, spec_id):
        raise ValueError(
            f"Invalid spec_id format: '{spec_id}'. "
            f"Must match pattern: SPEC-[DOMAIN]-[NUMBER] (e.g., SPEC-AUTH-001)"
        )


def validate_semver(version: str) -> None:
    """Validate semantic version format."""
    import re

    pattern = r'^\d+\.\d+\.\d+$'
    if not re.match(pattern, version):
        raise ValueError(
            f"Invalid version format: '{version}'. "
            f"Must be semantic version (e.g., 1.0.0)"
        )


def validate_status(status: str) -> None:
    """Validate status is one of allowed values."""
    allowed = ["draft", "approved", "implemented"]

    if status not in allowed:
        raise ValueError(
            f"Invalid status: '{status}'. "
            f"Must be one of: {', '.join(allowed)}"
        )


def main():
    """Main validation logic."""
    if len(sys.argv) != 2:
        print("Usage: yaml_validator.py <spec-file.md>", file=sys.stderr)
        sys.exit(1)

    spec_file = Path(sys.argv[1])

    if not spec_file.exists():
        print(f"Error: File not found: {spec_file}", file=sys.stderr)
        sys.exit(1)

    try:
        # Extract and parse YAML
        frontmatter = extract_frontmatter(spec_file)
        data = validate_yaml(frontmatter)

        # Validate required fields
        validate_required_fields(data)

        # Validate field formats
        validate_spec_id_format(data["spec_id"])
        validate_semver(data["version"])
        validate_status(data["status"])

        print(f"✅ YAML validation passed: {spec_file.name}")
        sys.exit(0)

    except ValueError as e:
        print(f"❌ Validation failed: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
