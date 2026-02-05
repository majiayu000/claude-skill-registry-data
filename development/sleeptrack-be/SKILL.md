---
name: sleeptrack-be
description: This skill provides comprehensive backend REST API integration for Asleep sleep tracking platform. Use this skill when building server-side applications, API proxies for mobile apps, webhook event handlers, cross-platform backends (React Native, Flutter), analytics dashboards, or multi-tenant sleep tracking systems. Covers authentication, user management, session retrieval, statistics, webhook integration, and production-ready patterns with code examples in Python, Node.js, and curl.
---

# Sleeptrack Backend API Integration

## Overview

This skill provides comprehensive guidance for integrating the Asleep REST API into backend applications. It covers server-side user management, session data retrieval, statistics aggregation, webhook event handling, and production-ready patterns for building robust sleep tracking backends.

**Use this skill when:**
- Building backend/server-side sleep tracking integrations
- Creating API proxies for mobile applications
- Implementing webhook handlers for real-time sleep data
- Developing cross-platform backends (React Native, Flutter)
- Building analytics dashboards and reporting systems
- Creating multi-tenant sleep tracking applications
- Integrating sleep data with other health platforms

## Quick Start

### 1. Get Your API Key

1. Sign up at https://dashboard.asleep.ai
2. Generate an API key for your application
3. Store securely in environment variables (never commit to version control)

### 2. Basic Authentication

All API requests require the `x-api-key` header:

**curl:**
```bash
curl -X GET "https://api.asleep.ai/ai/v1/users/USER_ID" \
  -H "x-api-key: YOUR_API_KEY"
```

**Python:**
```python
import requests

headers = {"x-api-key": "YOUR_API_KEY"}
response = requests.get(
    "https://api.asleep.ai/ai/v1/users/USER_ID",
    headers=headers
)
```

**Node.js:**
```javascript
const axios = require('axios');

const response = await axios.get(
  'https://api.asleep.ai/ai/v1/users/USER_ID',
  {
    headers: { 'x-api-key': 'YOUR_API_KEY' }
  }
);
```

## API Client Structure

Build a reusable API client to handle authentication, error handling, and common operations.

**Key Components:**
- Base URL configuration (`https://api.asleep.ai`)
- API key authentication in headers
- Error handling for common HTTP status codes (401, 403, 404)
- Request methods for all API endpoints
- Session management with persistent connections

**For complete implementations:**
- Python: See `references/python_client_implementation.md`
- Node.js: See `references/nodejs_client_implementation.md`
- REST API details: See `references/rest_api_reference.md`

**Basic Client Structure:**
```python
class AsleepClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.asleep.ai"
        self.session = requests.Session()
        self.session.headers.update({"x-api-key": api_key})

    def _request(self, method: str, path: str, **kwargs):
        # Handle authentication and errors
        # See python_client_implementation.md for full code
        pass
```

## User Management

### Creating Users

Create users before tracking sleep. User IDs are managed by your application.

```python
# Create user with metadata
user_id = client.create_user(metadata={
    "birth_year": 1990,
    "gender": "male",
    "height": 175.5,  # cm
    "weight": 70.0    # kg
})
```

**Available Metadata Fields:**
- `birth_year` (Integer): Birth year
- `birth_month` (Integer): 1-12
- `birth_day` (Integer): 1-31
- `gender` (String): `male`, `female`, `non_binary`, `other`, `prefer_not_to_say`
- `height` (Float): Height in cm (0-300)
- `weight` (Float): Weight in kg (0-1000)

### Retrieving User Information

```python
user_data = client.get_user(user_id)
# Returns: user_id, to_be_deleted status, last_session_info, metadata
```

**Response includes:**
- User ID and deletion status
- Last session information (if available)
- User metadata (demographic information)

### Deleting Users

Permanently removes user and all associated data (sessions, reports).

```python
client.delete_user(user_id)
```

**For detailed examples and response structures:**
- See `references/rest_api_reference.md` (User Management section)
- See `references/python_client_implementation.md` or `references/nodejs_client_implementation.md`

## Session Management

### Retrieving Session Details

Get comprehensive sleep analysis for a specific session.

```python
session = client.get_session(
    session_id="session123",
    user_id="user123",
    timezone="America/New_York"
)

# Access key metrics
print(f"Sleep efficiency: {session['stat']['sleep_efficiency']:.1f}%")
print(f"Total sleep time: {session['stat']['sleep_time']}")
print(f"Sleep stages: {session['session']['sleep_stages']}")
```

**Sleep Stage Values:**
- `-1`: Unknown/No data
- `0`: Wake
- `1`: Light sleep
- `2`: Deep sleep
- `3`: REM sleep

**Key Metrics:**
- `sleep_efficiency`: (Total sleep time / Time in bed) × 100%
- `sleep_latency`: Time to fall asleep (seconds)
- `waso_count`: Wake after sleep onset episodes
- `time_in_bed`: Total time in bed (seconds)
- `time_in_sleep`: Actual sleep time (seconds)
- `time_in_light/deep/rem`: Stage durations (seconds)

### Listing Sessions

Retrieve multiple sessions with date filtering and pagination.

```python
sessions = client.list_sessions(
    user_id="user123",
    date_gte="2024-01-01",
    date_lte="2024-01-31",
    limit=50,
    order_by="DESC"
)
```

**Pagination Example:**
```python
all_sessions = []
offset = 0
limit = 100

while True:
    result = client.list_sessions(
        user_id="user123",
        offset=offset,
        limit=limit
    )
    sessions = result['sleep_session_list']
    all_sessions.extend(sessions)

    if len(sessions) < limit:
        break
    offset += limit
```

### Deleting Sessions

```python
client.delete_session(session_id="session123", user_id="user123")
```

**For detailed session data structures and examples:**
- See `references/rest_api_reference.md` (Session Management section)
- See client implementation references for language-specific examples

## Statistics and Analytics

### Average Statistics

Get aggregated sleep metrics over a time period (max 100 days).

```python
stats = client.get_average_stats(
    user_id="user123",
    start_date="2024-01-01",
    end_date="2024-01-31",
    timezone="UTC"
)

avg = stats['average_stats']
print(f"Average sleep time: {avg['sleep_time']}")
print(f"Average efficiency: {avg['sleep_efficiency']:.1f}%")
print(f"Light sleep ratio: {avg['light_ratio']:.1%}")
print(f"Number of sessions: {len(stats['slept_sessions'])}")
```

**Returned Metrics:**
- Average sleep time, bedtime, wake time
- Average sleep efficiency
- Sleep stage ratios (light, deep, REM)
- List of sessions included in calculation

**For trend analysis and advanced analytics:**
- See `references/python_client_implementation.md` (Analytics section)
- See `references/rest_api_reference.md` (Statistics section)

## Webhook Integration

Webhooks enable real-time notifications for sleep session events.

### Webhook Event Types

1. **INFERENCE_COMPLETE**: Incremental sleep data during tracking (every 5-40 minutes)
2. **SESSION_COMPLETE**: Final comprehensive sleep analysis when session ends

### Setting Up Webhook Endpoint

**Basic Structure:**
```python
@app.route('/asleep-webhook', methods=['POST'])
def asleep_webhook():
    # 1. Verify authentication (x-api-key header)
    # 2. Parse event data
    # 3. Handle event type (INFERENCE_COMPLETE or SESSION_COMPLETE)
    # 4. Process and store data
    # 5. Return 200 response
    pass
```

**Key Implementation Points:**
- Verify `x-api-key` header matches your API key
- Validate `x-user-id` header
- Handle both INFERENCE_COMPLETE and SESSION_COMPLETE events
- Implement idempotency (check if event already processed)
- Process asynchronously for better performance
- Return 200 status immediately

**For complete webhook implementations:**
- Python (Flask): See `references/webhook_implementation_guide.md`
- Node.js (Express): See `references/webhook_implementation_guide.md`
- Webhook payloads: See `references/webhook_reference.md`

### Webhook Best Practices

**Idempotency:**
Check if webhook event was already processed to avoid duplicates.

**Asynchronous Processing:**
Queue webhook events for background processing and respond immediately.

**Error Handling:**
Return 200 even if processing fails internally to prevent retries.

**For detailed patterns:**
- See `references/webhook_implementation_guide.md`
- See `references/production_patterns.md` (Background Jobs section)

## Common Backend Patterns

### 1. API Proxy for Mobile Apps

Create a backend proxy to:
- Hide API keys from mobile clients
- Add custom authentication
- Implement business logic
- Track usage and analytics

**Key endpoints:**
- POST `/api/users` - Create Asleep user for authenticated app user
- GET `/api/sessions/{id}` - Proxy session retrieval with auth
- GET `/api/sessions` - List sessions with filtering
- GET `/api/statistics` - Get aggregated statistics

**For complete implementation:**
- See `references/python_client_implementation.md` (API Proxy section)

### 2. Analytics Dashboard Backend

Aggregate and analyze sleep data across multiple users:
- Calculate comprehensive sleep scores
- Generate weekly/monthly reports
- Analyze cohort sleep patterns
- Provide personalized insights

**Key features:**
- Sleep score calculation (efficiency + consistency + duration)
- Trend analysis over time
- Multi-user aggregation
- Report generation

**For complete implementation:**
- See `references/python_client_implementation.md` (Analytics section)

### 3. Multi-Tenant Application

Manage sleep tracking for multiple organizations or teams:
- Organization-level user management
- Aggregated organization statistics
- Role-based access control
- Per-organization settings

**For complete implementation:**
- See `references/python_client_implementation.md` (Multi-Tenant section)

## Error Handling

### Common Error Codes

- **401 Unauthorized**: Invalid API key
- **403 Forbidden**: Rate limit exceeded or insufficient permissions
- **404 Not Found**: Resource does not exist
- **422 Unprocessable Entity**: Invalid request parameters

### Retry Logic with Exponential Backoff

```python
def retry_with_exponential_backoff(func, max_retries=3, base_delay=1.0):
    for attempt in range(max_retries):
        try:
            return func()
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 403 and "rate limit" in str(e):
                if attempt < max_retries - 1:
                    delay = min(base_delay * (2 ** attempt), 60.0)
                    time.sleep(delay)
                    continue
            raise
```

### Custom Exception Classes

```python
class AsleepAPIError(Exception):
    """Base exception for Asleep API errors"""
    pass

class RateLimitError(AsleepAPIError):
    """Rate limit exceeded"""
    pass

class ResourceNotFoundError(AsleepAPIError):
    """Resource not found"""
    pass
```

**For comprehensive error handling:**
- See `references/python_client_implementation.md` or `references/nodejs_client_implementation.md`
- See `references/production_patterns.md` (Error Recovery section)

## Testing

### Local Webhook Testing

Use ngrok to expose local server for webhook testing:

```bash
# Start local server
python app.py  # or npm start

# Expose with ngrok
ngrok http 5000

# Use ngrok URL in webhook configuration
# Example: https://abc123.ngrok.io/asleep-webhook
```

### Mock API Responses

```python
@patch('requests.Session.request')
def test_create_user(mock_request):
    mock_response = Mock()
    mock_response.json.return_value = {
        "result": {"user_id": "test_user_123"}
    }
    mock_request.return_value = mock_response

    user_id = client.create_user()
    assert user_id == "test_user_123"
```

**For complete testing examples:**
- See `references/python_client_implementation.md` (Testing section)

## Production Best Practices

### Security

1. **API Key Management:**
   - Store in environment variables or secret management system
   - Never commit to version control
   - Rotate keys periodically
   - Use different keys for dev/staging/production

2. **Webhook Security:**
   - Verify `x-api-key` header
   - Use HTTPS endpoints only
   - Implement rate limiting
   - Log all webhook attempts

3. **User Data Privacy:**
   - Encrypt sensitive data at rest
   - Implement proper access controls
   - Handle data deletion requests
   - Comply with GDPR/CCPA

### Performance

1. **Caching:** Cache immutable session data
2. **Rate Limiting:** Protect your backend from overload
3. **Connection Pooling:** Reuse HTTP connections
4. **Batch Processing:** Process multiple requests in parallel

### Monitoring

1. **Logging:** Structured logging for all API requests
2. **Metrics:** Track request duration, error rates, throughput
3. **Health Checks:** Implement `/health`, `/ready`, `/live` endpoints
4. **Alerting:** Alert on error rate spikes or API failures

### Deployment

1. **Configuration:** Environment-based settings with validation
2. **Health Checks:** Support Kubernetes liveness/readiness probes
3. **Graceful Shutdown:** Handle termination signals properly
4. **Error Recovery:** Circuit breaker pattern for API failures

**For comprehensive production patterns:**
- Caching strategies: See `references/production_patterns.md`
- Rate limiting: See `references/production_patterns.md`
- Monitoring: See `references/production_patterns.md`
- Deployment: See `references/production_patterns.md`

## Resources

### Reference Documentation

This skill includes comprehensive reference files:

- `references/python_client_implementation.md`: Complete Python client with all methods, analytics classes, and examples
- `references/nodejs_client_implementation.md`: Complete Node.js client with Express integration
- `references/webhook_implementation_guide.md`: Full webhook handlers in Python and Node.js with best practices
- `references/rest_api_reference.md`: Complete REST API endpoint documentation with request/response examples
- `references/webhook_reference.md`: Webhook integration guide with payload structures
- `references/production_patterns.md`: Caching, rate limiting, monitoring, deployment, and performance optimization

To access detailed information:
```
Read references/python_client_implementation.md
Read references/nodejs_client_implementation.md
Read references/webhook_implementation_guide.md
Read references/rest_api_reference.md
Read references/webhook_reference.md
Read references/production_patterns.md
```

### Official Documentation

- **Main Documentation**: https://docs-en.asleep.ai
- **API Basics**: https://docs-en.asleep.ai/docs/api-basics.md
- **Webhook Guide**: https://docs-en.asleep.ai/docs/webhook.md
- **Dashboard**: https://dashboard.asleep.ai
- **LLM-Optimized Reference**: https://docs-en.asleep.ai/llms.txt

### Related Skills

- **sleeptrack-foundation**: Core concepts, authentication, data structures, and platform-agnostic patterns
- **sleeptrack-ios**: iOS SDK integration for native iOS applications
- **sleeptrack-android**: Android SDK integration for native Android applications

### Support

For technical support and API issues:
- Check Dashboard for API usage and status
- Review error logs and response codes
- Contact support through Asleep Dashboard
