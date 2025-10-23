---
name: spec-validator
description: This skill should be used when validating specifications before implementation. Triggers on "validate spec", "check specification", "review spec". Performs comprehensive validation including format, completeness, testability, edge case coverage, and dependencies. Generates scored validation report (0-100).
allowed-tools: Read, Grep, Bash
---

## Purpose

Validate SDL specifications for completeness, testability, and quality before implementation begins. Provide scored validation report with actionable feedback for improvement.

## When to Use This Skill

Activate when:
- User requests validation: "Validate this spec"
- Before implementation starts: "Is this spec ready to implement?"
- During spec review: "Check if SPEC-AUTH-001 is complete"
- Quality gate in workflow: Auto-validate before tests are generated

## Validation Process

### Step 1: Automated Validation

Run validation script for objective scoring:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/spec-validator/scripts/spec_validator.py <spec-file>
```

This script:
- Parses YAML frontmatter
- Validates format and required fields
- Counts sections and elements
- Calculates coverage score (0-100)
- Generates detailed report

### Step 2: Manual Review

Review aspects the script cannot check:

**Clarity**: Are requirements unambiguous?
**Consistency**: Do sections align with each other?
**Completeness**: Are there obvious gaps?
**Feasibility**: Are requirements realistic?

### Step 3: Testability Analysis

For each acceptance criterion, verify:

**Measurable**: Can success/failure be objectively determined?
```markdown
✅ Good: "Response time < 500ms"
❌ Bad: "System is fast"
```

**Automatable**: Can this be tested without human judgment?
```markdown
✅ Good: "Returns HTTP 200 status"
❌ Bad: "UI looks good"
```

**Unambiguous**: Is the expected outcome clear?
```markdown
✅ Good: "Error message: 'Invalid email format'"
❌ Bad: "Shows an error"
```

**Complete**: Are all conditions specified?
```markdown
✅ Good: "Given email='test@example.com' AND password='Pass123!'"
❌ Bad: "Given valid credentials"
```

### Step 4: Edge Case Coverage

Reference `${CLAUDE_PLUGIN_ROOT}/skills/spec-validator/references/validation_criteria.md` for detailed criteria.

Check each taxonomy category:

**Boundary Conditions**: Empty, null, min/max values?
- Keywords: empty, null, zero, max, overflow

**Security**: Injection, XSS, auth bypass?
- Keywords: injection, xss, sql, auth, csrf

**Concurrency**: Race conditions, simultaneous operations?
- Keywords: race, simultaneous, parallel, concurrent

**State Transitions**: Invalid states, expired resources?
- Keywords: state, transition, expired, invalid

**Performance**: Timeouts, large datasets, resource limits?
- Keywords: timeout, large, scale, performance

### Step 5: Generate Report

Combine automated and manual findings into comprehensive report.

## Scoring System

**Total**: 0-100 points

- **Format** (20 points):
  - Valid YAML frontmatter
  - Required fields present and correctly formatted
  - spec_id, version, status valid

- **Completeness** (30 points):
  - User stories defined (≥2)
  - Acceptance criteria defined (≥2)
  - Data models specified
  - Edge cases enumerated (≥3)
  - Non-functional requirements included
  - Success metrics defined

- **Testability** (25 points):
  - Acceptance criteria use Given/When/Then
  - Outcomes are measurable
  - Tests can be automated
  - Expectations are unambiguous

- **Edge Cases** (15 points):
  - Boundary conditions covered
  - Security scenarios included
  - Concurrency cases considered
  - State transitions covered
  - Performance scenarios defined

- **Dependencies** (10 points):
  - Valid dependency format
  - No circular dependencies
  - Dependencies exist (if verifiable)

## Pass/Fail Thresholds

- **≥ 80**: ✅ PASS - Approve for implementation
- **60-79**: ⚠️  WARNING - Address issues first
- **< 60**: ❌ FAIL - Significant revisions required

## Report Format

```markdown
# Validation Report: SPEC-AUTH-001

**Score**: 82/100
**Status**: ✅ PASS
**File**: docs/specs/SPEC-AUTH-001.md

## 🔴 Critical Issues
(None - ready to proceed!)

## ⚠️  Warnings
- Only 3 edge cases defined (recommend ≥5)
- Missing non-functional requirements section

## 💡 Suggestions
- Consider adding Component Specification template
- Add rollout plan section

## 📊 Coverage Breakdown
- ✅ **Format**: 20/20
- ⚠️  **Completeness**: 26/30
- ✅ **Testability**: 25/25
- ✅ **Edge Cases**: 12/15
- ✅ **Dependencies**: 10/10

## 🎯 Recommendation
**APPROVE - Ready for implementation**

Next steps:
1. Address warnings for improved quality
2. Generate tests: /sdd-framework:tests-from-spec SPEC-AUTH-001.md
3. Create implementation plan
```

## Common Issues and Fixes

### Format Issues

**Missing required field**:
```yaml
# Missing version field
---
spec_id: SPEC-AUTH-001
name: Authentication
status: draft
---
```

**Fix**: Add missing field:
```yaml
---
spec_id: SPEC-AUTH-001
name: Authentication
version: 1.0.0  # Added
status: draft
---
```

**Invalid semver**:
```yaml
version: 1.0  # Invalid
```

**Fix**:
```yaml
version: 1.0.0  # Valid semver
```

### Completeness Issues

**No acceptance criteria**:
```markdown
## Overview
[Feature description]

## Data Models
[Models...]
```

**Fix**: Add acceptance criteria section:
```markdown
## Acceptance Criteria

**AC-001**: [Criterion]
- **Given**: [Context]
- **When**: [Action]
- **Then**: [Outcome]
```

### Testability Issues

**Non-testable criterion**:
```markdown
**AC-001**: System Should Work
- The login should work properly
```

**Fix**: Make testable with Given/When/Then:
```markdown
**AC-001**: Successful Login
- **Given**: User with email "test@example.com" and password "Pass123!"
- **When**: User submits login form
- **Then**: HTTP 200 returned AND session token set AND redirect to /dashboard
```

### Edge Case Issues

**Missing categories**:
```markdown
## Edge Cases

**EC-001**: Empty Email
- User submits empty email field
```

**Fix**: Cover multiple categories:
```markdown
## Edge Cases

### Boundary Conditions
**EC-001**: Empty Email
- **Scenario**: User submits empty email field
- **Expected**: Validation error "Email required"

### Security
**EC-002**: SQL Injection
- **Scenario**: Email field contains `' OR '1'='1`
- **Expected**: Input sanitized, no SQL execution

### Concurrency
**EC-003**: Simultaneous Login
- **Scenario**: User clicks login twice rapidly
- **Expected**: Idempotency - only one session created
```

## Integration with Workflow

**Pre-Implementation Gate**:
```bash
# Before generating tests
/sdd-framework:validate-spec SPEC-AUTH-001.md

# If score ≥ 80, proceed
/sdd-framework:tests-from-spec SPEC-AUTH-001.md
```

**CI/CD Integration**:
```bash
# In pre-commit hook
python3 spec_validator.py docs/specs/*.md
if [ $? -ne 0 ]; then
  echo "Spec validation failed"
  exit 1
fi
```

## Output

Provide clear recommendation with score, status, and next steps. If score < 80, include specific, actionable feedback for improvement organized by priority (critical issues first, then warnings, then suggestions).
