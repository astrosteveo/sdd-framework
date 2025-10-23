---
name: spec-writer
description: This skill should be used when creating specifications for new features. Triggers on phrases like "write spec", "create specification", "define requirements", "I want to build". Guides through SDL (Spec Definition Language) format, ensures completeness using edge case taxonomy, validates testability, and saves to appropriate location.
allowed-tools: Read, Write, Glob, Grep, Bash
---

## Purpose

Guide users through creating complete, testable SDL (Spec Definition Language) specifications by asking clarifying questions, teaching specification best practices, and ensuring all edge cases are considered.

## When to Use This Skill

Activate when the user:
- Describes a new feature: "I want to build a login system"
- Explicitly requests spec creation: "Create a spec for payments"
- Asks to define requirements: "Define requirements for the API"
- Needs to formalize an idea into a specification

## Specification Creation Process

### Step 1: Template Selection

Present template options based on feature type:

- **Feature Specification** - Most common, for user-facing features
- **API Specification** - For REST/GraphQL endpoints
- **Component Specification** - For UI components
- **Architecture Specification** - For system design

Load appropriate template from `${CLAUDE_PLUGIN_ROOT}/skills/spec-writer/assets/`:
- `feature-spec-template.md`
- `api-spec-template.md`

### Step 2: Requirements Gathering

Ask iterative questions to understand:

**User Stories**: Who, what, why?
- "As a [role], I want [goal], so that [benefit]"

**Acceptance Criteria**: Testable conditions
- "Given [context], when [action], then [outcome]"

**Data Models**: What information is needed?
- Show language-specific examples (TypeScript for Node.js, dataclasses for Python, etc.)
- Detect project language by checking for package.json, requirements.txt, go.mod

**Edge Cases**: Use the taxonomy
- Reference `${CLAUDE_PLUGIN_ROOT}/skills/spec-writer/references/edge_case_taxonomy.md`
- Systematically consider: Boundary, Security, Concurrency, State, Performance
- For each category, help identify specific scenarios

### Step 3: SDL Frontmatter Generation

Construct valid YAML frontmatter following SDL format:

Reference `${CLAUDE_PLUGIN_ROOT}/skills/spec-writer/references/sdl_format.md` for complete format specification.

**Required fields**:
- `spec_id`: Format `SPEC-[DOMAIN]-[NUMBER]` (e.g., SPEC-AUTH-001)
- `name`: Human-readable feature name
- `version`: Semantic version (1.0.0)
- `status`: draft | approved | implemented

**Optional fields**:
- `dependencies`: Array of spec IDs this depends on
- `validators`: Paths to validation scripts
- `test_fixtures`: Paths to test data files
- `integration_hooks`: Pre/post generation hooks

### Step 4: Validation

Before saving, validate the specification:

**YAML Validation**:
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/spec-writer/scripts/yaml_validator.py <spec-file>
```

Check for:
- [ ] Valid YAML syntax
- [ ] All required fields present
- [ ] spec_id matches format: `SPEC-[A-Z]+-\d{3}`
- [ ] version is valid semver: `\d+\.\d+\.\d+`
- [ ] status is one of: draft, approved, implemented

**Completeness Check**:
- [ ] At least 2 user stories defined
- [ ] At least 2 acceptance criteria (testable)
- [ ] Data models defined with types
- [ ] Minimum 3 edge cases identified (one from each category)
- [ ] Non-functional requirements specified

### Step 5: File Persistence

**Create directory if needed**:
```bash
mkdir -p docs/specs
```

**Save specification**:
- Path: `docs/specs/SPEC-[ID].md`
- Ensure atomic write (write to temp file, then move)
- Set file permissions to 644 (readable/writable)

**Confirm to user**:
```
✅ Specification saved: docs/specs/SPEC-AUTH-001.md

Next steps:
1. Review and refine acceptance criteria
2. Generate tests: /sdd-framework:tests-from-spec SPEC-AUTH-001.md
3. Create architecture plan: /sdd-framework:implement-spec SPEC-AUTH-001.md
```

## Edge Case Taxonomy

For comprehensive edge case coverage, reference the detailed taxonomy:

`${CLAUDE_PLUGIN_ROOT}/skills/spec-writer/references/edge_case_taxonomy.md`

**Quick Reference**:

1. **Boundary**: Empty/null values, min/max ranges, format violations
2. **Security**: Injection attacks, auth bypass, data exposure
3. **Concurrency**: Race conditions, deadlocks, synchronization
4. **State**: Invalid transitions, expired resources, orphaned data
5. **Performance**: Large datasets, timeouts, resource exhaustion

For each category, ask: "What could go wrong in this scenario?"

## Data Model Teaching

When discussing data models, provide language-specific examples:

**TypeScript (detected from package.json)**:
```typescript
interface LoginRequest {
  email: string;
  password: string;
  rememberMe?: boolean;
}
```

**Python (detected from requirements.txt)**:
```python
@dataclass
class LoginRequest:
    email: str
    password: str
    remember_me: bool = False
```

**Go (detected from go.mod)**:
```go
type LoginRequest struct {
    Email      string `json:"email"`
    Password   string `json:"password"`
    RememberMe bool   `json:"rememberMe,omitempty"`
}
```

## Context Handling

**Mid-Work Detection**:
If user describes a different feature while working on a spec:

```
⚠️  Context switch detected

Currently working on: SPEC-AUTH-001 (50% complete)
New feature detected: Payment processing

Options:
1. Save SPEC-AUTH-001 as draft and start SPEC-PAYMENT-001
2. Continue working on SPEC-AUTH-001
3. Work on both (track separately)

Which would you prefer?
```

**Multiple Specs in Session**:
Track each spec separately to prevent cross-contamination. Maintain state for each spec_id.

## Validation Scripts

Use bundled validation scripts to ensure quality:

**YAML Validator** - Validates frontmatter syntax and required fields:
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/spec-writer/scripts/yaml_validator.py docs/specs/SPEC-AUTH-001.md
```

Returns:
- ✅ YAML validation passed
- ❌ Validation failed: [specific error]

## Common Patterns

**For authentication features**: Emphasize security edge cases (injection, bypass, brute force)

**For payment features**: Emphasize state transitions (idempotency, duplicate charges, refunds)

**For API endpoints**: Use API template, include rate limiting and error codes

**For UI components**: Include accessibility requirements and responsive design

## Progressive Disclosure

Keep conversations focused:
- Ask 1-2 questions at a time (avoid overwhelming)
- Start with core functionality (happy path)
- Then explore edge cases systematically
- Save frequently (auto-save every 30 seconds mentally)

## Output Format

Produce complete specification file matching SDL format with:
- Valid YAML frontmatter
- Clear user stories in "As a/I want/So that" format
- Testable acceptance criteria in "Given/When/Then" format
- Data models with type annotations
- Comprehensive edge cases categorized by taxonomy
- Non-functional requirements (performance, security, reliability)
- Success metrics (must have, should have, could have)
