# Spec Validation Criteria

Detailed rubric for validating SDL specifications with scoring breakdown.

## Scoring System

**Total Score**: 0-100 points

- **Format**: 20 points
- **Completeness**: 30 points
- **Testability**: 25 points
- **Edge Cases**: 15 points
- **Dependencies**: 10 points

### Pass/Fail Thresholds

- **≥ 80**: PASS - Ready for implementation
- **60-79**: WARNING - Address issues before proceeding
- **< 60**: FAIL - Significant revisions required

---

## 1. Format Validation (20 points)

### Required Fields (20 points total, -5 each missing)

#### spec_id (mandatory)
**Format**: `SPEC-[DOMAIN]-[NUMBER]`
- Domain: Uppercase letters only
- Number: Three digits (001-999)

**Valid**:
- `SPEC-AUTH-001`
- `SPEC-PAYMENT-042`

**Invalid**:
- `AUTH-001` (missing SPEC-)
- `SPEC-auth-001` (lowercase domain)
- `SPEC-AUTH` (missing number)

#### name (mandatory)
Human-readable feature name

**Valid**:
- Any string with content
- Can contain spaces, punctuation, special characters

**Invalid**:
- Empty string
- Only whitespace

#### version (mandatory)
**Format**: Semantic versioning `X.Y.Z`

**Valid**:
- `1.0.0`
- `2.3.1`

**Invalid**:
- `1.0` (missing patch)
- `v1.0.0` (has 'v' prefix)
- `1.0.0-beta` (no pre-release tags)

#### status (mandatory)
**Allowed values**: `draft`, `approved`, `implemented`

**Scoring**:
- Valid value: 0 points deducted
- Invalid value: -2 points (warning)

---

## 2. Completeness Validation (30 points)

### User Stories (6 points)

**Scoring**:
- Section present: 0 deducted
- Section missing: -6 points (critical)
- No stories defined: -4 points (warning)
- Only 1 story: -2 points (suggestion)

**Quality Criteria**:
- Uses "As a... I want... So that..." format
- Clear role, goal, and benefit
- Focused on user value

**Example**:
```markdown
**US-001**: User Login
- **As a** registered user
- **I want to** log in with email and password
- **So that** I can access my account
```

### Acceptance Criteria (6 points)

**Scoring**:
- Section present: 0 deducted
- Section missing: -6 points (critical)
- No criteria defined: -4 points (warning)
- Only 1 criterion: -2 points (suggestion)

**Quality Criteria**:
- Uses Given/When/Then format
- Testable and measurable
- Unambiguous outcomes
- Priority specified (must/should/could)

**Example**:
```markdown
**AC-001**: Successful Login
- **Given**: User provides valid credentials
- **When**: User submits login form
- **Then**: User is authenticated and redirected
- **Priority**: must
```

### Data Models (4 points)

**Scoring**:
- Section present: 0 deducted
- Section missing: -4 points (warning)
- No models defined: -3 points (warning)

**Quality Criteria**:
- Language-appropriate syntax (TypeScript, Python, Go, etc.)
- Type annotations included
- Comments explaining fields
- Required vs optional fields clearly marked

**Example**:
```typescript
interface LoginRequest {
  email: string;      // User's email
  password: string;   // Plain text password
  rememberMe?: boolean; // Optional
}
```

### Edge Cases (6 points)

**Scoring**:
- Section present: 0 deducted
- Section missing: -6 points (critical)
- < 3 edge cases: -3 points (warning)

**Quality Criteria**:
- Categorized by taxonomy (Boundary, Security, Concurrency, State, Performance)
- Clear scenario description
- Expected behavior defined
- Test requirement specified

### Non-Functional Requirements (4 points)

**Scoring**:
- Section present: 0 deducted
- Section missing: -4 points (warning)

**Should Include**:
- Performance requirements
- Security requirements
- Reliability requirements
- Scalability requirements

### Success Metrics (2 points)

**Scoring**:
- Section present: 0 deducted
- Section missing: -2 points (suggestion)

**Should Include**:
- Must have criteria
- Should have criteria
- Could have criteria

---

## 3. Testability Validation (25 points)

### Given/When/Then Structure

**Scoring Based on Ratio**:
- 100% of ACs use GWT: 0 deducted
- 80-99% use GWT: -3 points (suggestion)
- 50-79% use GWT: -8 points (warning)
- < 50% use GWT: -15 points (critical)

### Measurability

**Each AC must have**:
- Clear initial condition (Given)
- Specific action (When)
- Measurable outcome (Then)

**Good Example**:
```markdown
**AC-001**: Login Success
- **Given**: User "test@example.com" with password "Pass123!"
- **When**: User clicks "Login" button
- **Then**: Dashboard loads within 2 seconds AND session token is set
```

**Poor Example** (not testable):
```markdown
**AC-001**: Login Works
- User should be able to log in successfully
```

### Automation Potential

**Questions to Ask**:
- Can this be tested without human intervention?
- Are success criteria binary (pass/fail)?
- Can the test be repeated with same results?

### Unambiguous Outcomes

**Good**: "HTTP 200 status code returned"
**Bad**: "Response is successful"

**Good**: "Error message: 'Invalid credentials' displayed"
**Bad**: "User sees an error"

---

## 4. Edge Case Coverage (15 points)

### Taxonomy Coverage

**Scoring Based on Categories Covered**:
- 5/5 categories: 0 deducted
- 3-4 categories: -3 points (suggestion)
- 1-2 categories: -9 points (warning)
- 0 categories: -15 points (critical)

### Required Categories

#### 1. Boundary Conditions
**Keywords**: empty, null, min, max, zero, overflow
**Examples**:
- Empty string inputs
- Null/undefined values
- Maximum length strings
- Off-by-one errors

#### 2. Security
**Keywords**: security, injection, xss, auth, sql, csrf
**Examples**:
- SQL injection attempts
- XSS payloads
- Authentication bypass
- Authorization failures

#### 3. Concurrency
**Keywords**: concurrency, race, simultaneous, parallel, thread
**Examples**:
- Simultaneous updates
- Race conditions
- Deadlocks
- Dirty reads

#### 4. State Transitions
**Keywords**: state, transition, expired, invalid, orphan
**Examples**:
- Invalid state changes
- Expired tokens/sessions
- Orphaned records
- Terminal state operations

#### 5. Performance
**Keywords**: performance, timeout, large, scale, slow
**Examples**:
- Large datasets
- Request timeouts
- Resource exhaustion
- Rate limiting

---

## 5. Dependency Validation (10 points)

### Dependency Format

**Each dependency must**:
- Follow spec_id format: `SPEC-[DOMAIN]-[NUMBER]`
- Reference existing spec (if checkable)

**Scoring**:
- All valid: 0 deducted
- Invalid format: -2 per invalid dependency

### Circular Dependency Check

**Critical Issue**:
- Spec depends on itself: -10 points
- Circular chain detected: -10 points

**Example of Circular Dependency**:
```yaml
# SPEC-A-001
dependencies:
  - SPEC-B-001

# SPEC-B-001
dependencies:
  - SPEC-A-001
```

### Version Compatibility

**If version ranges specified**:
- Check compatibility
- Warn about breaking changes
- Suggest pinning versions

---

## Quality Gates

### Critical Issues (Must Fix)

**Format**:
- Missing required fields
- Invalid spec_id format
- Invalid semver

**Completeness**:
- Missing User Stories section
- Missing Acceptance Criteria section
- Missing Edge Cases section

**Testability**:
- < 50% of ACs use Given/When/Then

**Dependencies**:
- Circular dependencies

### Warnings (Should Fix)

**Completeness**:
- No user stories defined
- No acceptance criteria defined
- No edge cases defined
- Missing data models
- Missing non-functional requirements

**Testability**:
- 50-79% of ACs use Given/When/Then

**Edge Cases**:
- Only 1-2 taxonomy categories covered

### Suggestions (Nice to Fix)

**Completeness**:
- Only 1 user story
- Only 1 acceptance criterion
- < 3 edge cases
- Missing success metrics

**Testability**:
- 80-99% of ACs use Given/When/Then

**Edge Cases**:
- 3-4 taxonomy categories covered

---

## Validation Workflow

1. **Format Check**
   - Parse YAML frontmatter
   - Validate required fields
   - Check field formats

2. **Completeness Scan**
   - Search for required sections
   - Count user stories, ACs, edge cases
   - Identify missing sections

3. **Testability Analysis**
   - Extract all acceptance criteria
   - Check Given/When/Then structure
   - Verify measurability

4. **Edge Case Review**
   - Identify mentioned categories
   - Count edge cases per category
   - Calculate coverage percentage

5. **Dependency Audit**
   - Validate dependency formats
   - Check for circular dependencies
   - Verify existence (if possible)

6. **Generate Report**
   - Calculate scores
   - Categorize issues/warnings/suggestions
   - Provide actionable recommendations

---

## Report Format

```markdown
# Validation Report: SPEC-XXX-001

**Score**: 82/100
**Status**: ✅ PASS

## 🔴 Critical Issues
(None)

## ⚠️  Warnings
- Only 1 user story defined
- Missing non-functional requirements section

## 💡 Suggestions
- Consider adding more edge cases (currently 3, recommend ≥5)

## 📊 Coverage Breakdown
- ✅ **Format**: 20/20
- ⚠️  **Completeness**: 24/30
- ✅ **Testability**: 25/25
- ✅ **Edge Cases**: 13/15
- ✅ **Dependencies**: 10/10

## 🎯 Recommendation
**APPROVE - Ready for implementation**
```

---

## Continuous Improvement

### Track Metrics Over Time

- Average spec score
- Common issues
- Categories with low scores
- Improvement trends

### Team Standards

Establish team-specific thresholds:
- Minimum score for approval
- Required edge case categories
- Mandatory sections
- Documentation depth

### Automated Validation

Integrate validation into:
- Pre-commit hooks
- CI/CD pipeline
- Spec review process
- Documentation generation
