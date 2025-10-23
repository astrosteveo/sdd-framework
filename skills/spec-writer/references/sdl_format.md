# SDL (Spec Definition Language) Format Reference

## Overview

SDL is a structured format for writing software specifications that combines YAML frontmatter with Markdown content. It enables machine-parseable metadata while maintaining human-readable documentation.

## YAML Frontmatter Structure

Every SDL spec begins with YAML frontmatter enclosed by `---` markers:

```yaml
---
spec_id: SPEC-DOMAIN-XXX
name: Human Readable Feature Name
version: 1.0.0
status: draft
dependencies: []
validators: []
test_fixtures: []
integration_hooks:
  pre_generation: null
  post_generation: null
composed_of: []
metadata:
  author: author_name
  created: YYYY-MM-DD
  category: optional_category
  priority: optional_priority
---
```

## Required Fields

### spec_id (string)

**Format**: `SPEC-[DOMAIN]-[NUMBER]`

- `DOMAIN`: Uppercase letters describing the domain (AUTH, USER, PAYMENT, API, etc.)
- `NUMBER`: Three-digit zero-padded number (001, 002, ..., 999)

**Examples**:
- `SPEC-AUTH-001` - First authentication spec
- `SPEC-PAYMENT-042` - Payment spec #42
- `SPEC-API-123` - API spec #123

**Invalid**:
- `AUTH-001` (missing SPEC- prefix)
- `SPEC-auth-001` (lowercase domain)
- `SPEC-AUTH` (missing number)
- `SPEC-001` (missing domain)

### name (string)

Human-readable feature name. Can contain spaces, punctuation, and special characters.

**Examples**:
- `User Authentication`
- `Payment Processing Gateway`
- `Real-time Messaging System`
- `User's "Advanced" Settings` (quotes properly escaped in YAML)

### version (string)

**Format**: Semantic versioning `MAJOR.MINOR.PATCH`

- `MAJOR`: Incompatible API changes
- `MINOR`: Backwards-compatible functionality
- `PATCH`: Backwards-compatible bug fixes

**Examples**:
- `1.0.0` - Initial version
- `1.1.0` - Added features
- `1.1.1` - Bug fixes
- `2.0.0` - Breaking changes

**Invalid**:
- `1.0` (missing patch)
- `v1.0.0` (no 'v' prefix)
- `1.0.0-beta` (no pre-release tags)

### status (enum)

Current state of the specification.

**Allowed values**:
- `draft` - Specification in progress
- `approved` - Specification reviewed and approved
- `implemented` - Feature has been implemented

## Optional Fields

### dependencies (array of strings)

List of other spec IDs that this spec depends on.

```yaml
dependencies:
  - SPEC-USER-001
  - SPEC-AUTH-001
```

**Use when**:
- Feature requires other features to exist first
- Implementation order matters
- Shared data models or interfaces

**Empty if**: No dependencies exist

```yaml
dependencies: []
```

### validators (array of strings)

Paths to validation scripts that check the spec.

```yaml
validators:
  - scripts/validators/yaml_validator.py
  - scripts/validators/sdl_schema_validator.py
  - scripts/validators/custom_business_rules.py
```

### test_fixtures (array of strings)

Paths to test data files for this spec.

```yaml
test_fixtures:
  - fixtures/valid_users.json
  - fixtures/invalid_credentials.json
  - fixtures/edge_case_inputs.json
```

### integration_hooks (object)

Scripts to run before/after spec operations.

```yaml
integration_hooks:
  pre_generation: scripts/hooks/validate_syntax.py
  post_generation: scripts/hooks/run_tests.py
```

**Use `null` if no hooks**:

```yaml
integration_hooks:
  pre_generation: null
  post_generation: null
```

### composed_of (array of strings)

For composite specs that combine multiple specs.

```yaml
composed_of:
  - SPEC-AUTH-001
  - SPEC-AUTH-002
  - SPEC-AUTH-003
```

**Empty for non-composite specs**:

```yaml
composed_of: []
```

### metadata (object)

Additional metadata about the spec.

```yaml
metadata:
  author: username
  created: 2025-10-22
  category: authentication
  priority: high
  tags:
    - security
    - user-management
```

**Required metadata fields**:
- `author`: Who created the spec
- `created`: Date in YYYY-MM-DD format

**Optional metadata fields**:
- `category`: Domain category
- `priority`: Importance level
- `tags`: Array of tags
- Any custom fields needed

## Markdown Body Structure

After the YAML frontmatter, include these sections:

### Overview

Brief description of the feature and its purpose.

```markdown
## Overview

This specification defines the user authentication system...
```

### User Stories

User stories in "As a... I want... So that..." format.

```markdown
## User Stories

**US-001**: User Login
- **As a** registered user
- **I want to** log in with email and password
- **So that** I can access my account

**US-002**: Password Reset
- **As a** user who forgot password
- **I want to** reset my password via email
- **So that** I can regain access to my account
```

### Acceptance Criteria

Testable criteria in Given/When/Then format.

```markdown
## Acceptance Criteria

**AC-001**: Successful Login
- **Given**: User provides valid email and password
- **When**: User submits login form
- **Then**: User is authenticated and redirected to dashboard

**AC-002**: Invalid Credentials
- **Given**: User provides incorrect password
- **When**: User submits login form
- **Then**: Error message displayed: "Invalid credentials"
```

### Data Models

Data structures with language-specific examples.

```markdown
## Data Models

### LoginRequest

```typescript
interface LoginRequest {
  email: string;      // User's email address
  password: string;   // Plain text password
  rememberMe?: boolean; // Optional: keep session alive
}
\```

### LoginResponse

```typescript
interface LoginResponse {
  success: boolean;
  token?: string;     // JWT token if successful
  error?: string;     // Error message if failed
}
\```
```

### Edge Cases

Edge cases organized by taxonomy category.

```markdown
## Edge Cases

### Boundary Conditions

**EC-001**: Empty Email
- **Scenario**: User submits empty email field
- **Expected**: Validation error: "Email is required"
- **Test Required**: Yes

### Security

**EC-002**: SQL Injection
- **Scenario**: User enters `' OR '1'='1` in email field
- **Expected**: Input sanitized, no SQL execution
- **Test Required**: Yes
```

### Non-Functional Requirements

Performance, security, scalability requirements.

```markdown
## Non-Functional Requirements

### Performance
- Login request: < 500ms response time
- Password hashing: bcrypt with cost factor 12

### Security
- HTTPS required for all requests
- Passwords hashed with bcrypt
- Rate limiting: 5 attempts per minute

### Scalability
- Support 10,000 concurrent users
- Session storage: Redis cluster
```

## YAML Special Characters

When spec names or descriptions contain YAML special characters, use quotes:

```yaml
name: "User's \"Advanced\" Settings: Part 2"
description: "Handle edge cases (null, empty, invalid)"
```

**Special characters requiring quotes**:
- Colons `:` outside of structural YAML
- Quotes `"` and `'`
- Brackets `[` `]`
- Braces `{` `}`
- Hash `#` (comment character)
- Ampersand `&` (anchor)
- Asterisk `*` (alias)
- Exclamation `!` (tag)
- Pipe `|` and `>` (block scalars)

## Complete Example

```yaml
---
spec_id: SPEC-AUTH-001
name: User Authentication System
version: 1.0.0
status: draft
dependencies: []
validators:
  - scripts/validators/yaml_validator.py
test_fixtures:
  - fixtures/valid_credentials.json
integration_hooks:
  pre_generation: null
  post_generation: null
composed_of: []
metadata:
  author: astrosteveo
  created: 2025-10-22
  category: authentication
  priority: critical
---

## Overview

Complete user authentication system with email/password login...

## User Stories

**US-001**: User Login
- **As a** registered user
- **I want to** log in with credentials
- **So that** I can access my account

## Acceptance Criteria

**AC-001**: Successful Authentication
- **Given**: Valid email and password
- **When**: User submits login form
- **Then**: JWT token issued and user redirected

## Data Models

[... etc ...]
```
