---
spec_id: SPEC-API-XXX
name: API Name
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
  category: api
  priority: null
---

## Overview

[Brief description of the API and its purpose]

### Base URL

```
Production: https://api.example.com/v1
Staging: https://api-staging.example.com/v1
Development: http://localhost:3000/v1
```

---

## Authentication

### Method

[Bearer Token | API Key | OAuth 2.0 | Basic Auth]

### Headers

```http
Authorization: Bearer <token>
Content-Type: application/json
```

### Token Format

```typescript
interface AuthToken {
  access_token: string;
  token_type: "Bearer";
  expires_in: number;
  refresh_token?: string;
}
```

---

## Endpoints

### [Endpoint Name]

**Method**: `GET | POST | PUT | PATCH | DELETE`
**Path**: `/resource/{id}`
**Description**: [What this endpoint does]

#### Request

**Path Parameters**:
- `id` (string, required): [Description]

**Query Parameters**:
- `filter` (string, optional): [Description]
- `limit` (number, optional): [Description, default: 10]
- `offset` (number, optional): [Description, default: 0]

**Headers**:
```http
Authorization: Bearer <token>
Content-Type: application/json
```

**Body**:
```typescript
interface RequestBody {
  field1: string;      // Description
  field2: number;      // Description
  field3?: boolean;    // Optional field
}
```

**Example**:
```bash
curl -X POST https://api.example.com/v1/resource/123 \
  -H "Authorization: Bearer token_here" \
  -H "Content-Type: application/json" \
  -d '{
    "field1": "value",
    "field2": 42
  }'
```

#### Response

**Success (200 OK)**:
```typescript
interface SuccessResponse {
  data: ResourceModel;
  meta: {
    timestamp: string;
    requestId: string;
  };
}
```

**Example**:
```json
{
  "data": {
    "id": "123",
    "field1": "value",
    "field2": 42
  },
  "meta": {
    "timestamp": "2025-10-22T10:30:00Z",
    "requestId": "req_abc123"
  }
}
```

#### Error Responses

**400 Bad Request** - Invalid input
```json
{
  "error": {
    "code": "INVALID_INPUT",
    "message": "Field 'field2' must be a positive number",
    "details": {
      "field": "field2",
      "value": -5,
      "constraint": "positive"
    }
  }
}
```

**401 Unauthorized** - Missing or invalid authentication
```json
{
  "error": {
    "code": "UNAUTHORIZED",
    "message": "Invalid or expired token"
  }
}
```

**403 Forbidden** - Insufficient permissions
```json
{
  "error": {
    "code": "FORBIDDEN",
    "message": "Insufficient permissions to access this resource"
  }
}
```

**404 Not Found** - Resource doesn't exist
```json
{
  "error": {
    "code": "NOT_FOUND",
    "message": "Resource with id '123' not found"
  }
}
```

**429 Too Many Requests** - Rate limit exceeded
```json
{
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "Rate limit exceeded. Try again in 60 seconds",
    "retryAfter": 60
  }
}
```

**500 Internal Server Error** - Server error
```json
{
  "error": {
    "code": "INTERNAL_ERROR",
    "message": "An unexpected error occurred",
    "requestId": "req_abc123"
  }
}
```

---

## Data Models

### [Primary Model]

```typescript
interface ResourceModel {
  id: string;
  createdAt: string;        // ISO 8601 timestamp
  updatedAt: string;        // ISO 8601 timestamp
  field1: string;
  field2: number;
  nested?: {
    subfield: string;
  };
}
```

### Error Response Model

```typescript
interface ErrorResponse {
  error: {
    code: string;           // Machine-readable error code
    message: string;        // Human-readable error message
    details?: object;       // Additional error context
    requestId?: string;     // Request ID for debugging
    retryAfter?: number;    // Seconds until retry allowed
  };
}
```

---

## Edge Cases

### Boundary Conditions

**EC-001**: Empty Request Body
- **Scenario**: POST request with empty JSON object `{}`
- **Expected**: 400 Bad Request with validation errors for required fields
- **Test Required**: Yes

**EC-002**: Maximum Page Size
- **Scenario**: Request with `limit=10000` (exceeds max of 100)
- **Expected**: Clamp to maximum, return 100 results with warning header
- **Test Required**: Yes

### Security

**EC-003**: SQL Injection in Query Parameters
- **Scenario**: `GET /resource?filter=' OR '1'='1`
- **Expected**: Input sanitized, parameterized queries used
- **Test Required**: Yes

**EC-004**: Expired Authentication Token
- **Scenario**: Request with token expired 1 hour ago
- **Expected**: 401 Unauthorized, prompt to refresh token
- **Test Required**: Yes

### Concurrency

**EC-005**: Concurrent Updates
- **Scenario**: Two clients update same resource simultaneously
- **Expected**: Use optimistic locking or last-write-wins with version tracking
- **Test Required**: Yes

### State Transitions

**EC-006**: Invalid State Change
- **Scenario**: Attempt to delete resource already in 'deleted' state
- **Expected**: 409 Conflict with clear error message
- **Test Required**: Yes

### Performance

**EC-007**: Large Response Payload
- **Scenario**: Query returns 100MB of data
- **Expected**: Pagination enforced, maximum 1000 records per response
- **Test Required**: Yes

**EC-008**: Request Timeout
- **Scenario**: Database query takes 35 seconds (exceeds 30s timeout)
- **Expected**: 504 Gateway Timeout with retry guidance
- **Test Required**: Yes

---

## Rate Limiting

### Limits

**Tier**: Free
**Limit**: 100 requests per hour
**Burst**: 10 requests per second

**Tier**: Pro
**Limit**: 10,000 requests per hour
**Burst**: 100 requests per second

### Headers

```http
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 87
X-RateLimit-Reset: 1635360000
```

### Behavior

When limit exceeded:
- Status: `429 Too Many Requests`
- Header: `Retry-After: 3600` (seconds)
- Body: Error response with `retryAfter` field

---

## Pagination

### Offset-Based Pagination

**Request**:
```http
GET /resources?limit=20&offset=40
```

**Response**:
```json
{
  "data": [...],
  "pagination": {
    "limit": 20,
    "offset": 40,
    "total": 150,
    "hasMore": true
  }
}
```

### Cursor-Based Pagination (Recommended)

**Request**:
```http
GET /resources?limit=20&cursor=eyJpZCI6MTIzfQ==
```

**Response**:
```json
{
  "data": [...],
  "pagination": {
    "nextCursor": "eyJpZCI6MTQzfQ==",
    "prevCursor": "eyJpZCI6MTAzfQ==",
    "hasMore": true
  }
}
```

---

## Webhooks

### Event Types

- `resource.created` - New resource created
- `resource.updated` - Resource modified
- `resource.deleted` - Resource deleted

### Payload Format

```typescript
interface WebhookPayload {
  event: string;           // Event type
  timestamp: string;       // ISO 8601
  data: ResourceModel;     // Event data
  signature: string;       // HMAC signature for verification
}
```

### Signature Verification

```typescript
const signature = crypto
  .createHmac('sha256', webhookSecret)
  .update(JSON.stringify(payload))
  .digest('hex');

if (signature !== receivedSignature) {
  throw new Error('Invalid signature');
}
```

---

## Versioning

### Strategy

URL-based versioning: `/v1/`, `/v2/`

### Breaking Changes

Require new version:
- Removing fields
- Changing field types
- Changing error codes
- Removing endpoints

### Non-Breaking Changes

Same version:
- Adding optional fields
- Adding endpoints
- Adding optional parameters

---

## Non-Functional Requirements

### Performance
- Response time: P95 < 200ms, P99 < 500ms
- Throughput: 1000 requests per second
- Availability: 99.9% uptime

### Security
- HTTPS required for all requests
- Authentication required for all endpoints except `/health`
- Input validation on all parameters
- Rate limiting per API key

### Reliability
- Idempotency for POST/PUT/PATCH using `Idempotency-Key` header
- Automatic retries with exponential backoff
- Circuit breaker for dependent services

---

## Test Plan

### Unit Tests
- Request validation logic
- Response serialization
- Error handling
- Authentication/authorization

### Integration Tests
- Full endpoint workflows
- Database interactions
- Third-party integrations
- Error scenarios

### E2E Tests
- Complete user journeys
- Multi-endpoint flows
- Authentication flows
- Webhook delivery

### Performance Tests
- Load testing (1000 req/s)
- Spike testing (10x normal load)
- Endurance testing (24 hours)
- Rate limit enforcement

---

## Documentation Requirements

- [ ] OpenAPI/Swagger specification
- [ ] API reference documentation
- [ ] Authentication guide
- [ ] Rate limiting guide
- [ ] Webhook integration guide
- [ ] Error code reference
- [ ] Example code (curl, JavaScript, Python)
- [ ] Postman collection

---

**END OF SPECIFICATION**
