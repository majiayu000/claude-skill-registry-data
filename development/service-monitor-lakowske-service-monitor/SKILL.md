---
name: service-monitor
description: Monitor service health at raspberrypi.local:8000. Check service status, add monitored services, view notifications, and manage health check configuration.
---

# Service Monitor Skill

This skill enables management of the service-monitor application running at http://raspberrypi.local:8000.

## Overview

The service-monitor is a FastAPI application that monitors the health of various services by periodically checking their health endpoints. It tracks service status (UP, DOWN, DEGRADED, UNKNOWN) and provides notifications when services change state.

## API Base URL

```
http://raspberrypi.local:8000
```

## Key Concepts

### Service Statuses
- **UP**: Service is healthy and responding as expected
- **DOWN**: Service is unreachable or timing out
- **DEGRADED**: Service is responding but not with expected status/content
- **UNKNOWN**: Service has never checked in or status is uncertain

### Service Types

1. **Services** (`/services/*`): Runtime status of monitored services
   - Tracks current health state
   - Receives check-ins from services
   - Can be manually removed

2. **Monitored Services** (`/monitored-services/*`): Configuration for automatic monitoring
   - Defines health check URLs and intervals
   - Automatically polls services and updates their status
   - Persistent configuration stored in `monitored_services.json`

## Common Operations

### 1. Get All Services Status

Get the current status of all services being monitored:

```bash
curl -s http://raspberrypi.local:8000/services | jq .
```

**Response**: Array of ServiceInfo objects with:
- `service_name`: Name of the service
- `status`: Current status (up/down/degraded/unknown)
- `last_check_in`: ISO timestamp of last check
- `message`: Status message
- `metadata`: Additional metadata (health_url, response_time, etc.)
- `check_in_count`: Total number of check-ins

### 2. Get Specific Service Status

```bash
curl -s http://raspberrypi.local:8000/services/{service_name} | jq .
```

### 3. Get Services by Status

Filter services by their current status:

```bash
curl -s http://raspberrypi.local:8000/services/status/{status} | jq .
```

Where `{status}` is one of: `up`, `down`, `degraded`, `unknown`

### 4. Remove a Service

Remove a service from monitoring (this removes runtime status, not configuration):

```bash
curl -X DELETE http://raspberrypi.local:8000/services/{service_name}
```

### 5. List Monitored Services Configuration

Get all configured monitored services:

```bash
curl -s http://raspberrypi.local:8000/monitored-services | jq .
```

**Response**: Object with:
- `success`: Boolean
- `services`: Array of MonitoredService configurations
- `total`: Number of configured services

### 6. Get Specific Monitored Service Configuration

```bash
curl -s http://raspberrypi.local:8000/monitored-services/{service_name} | jq .
```

### 7. Add or Update Monitored Service

Add a new service to be monitored automatically:

```bash
curl -X POST http://raspberrypi.local:8000/monitored-services \
  -H "Content-Type: application/json" \
  -d '{
    "name": "my-service",
    "health_url": "http://localhost:3000/health",
    "check_interval_seconds": 60,
    "timeout_seconds": 10,
    "expected_status_code": 200,
    "enabled": true,
    "check_response_body": false,
    "expected_body_content": null
  }'
```

**MonitoredService Schema**:
- `name` (required): Unique service name
- `health_url` (required): HTTP/HTTPS URL to check
- `check_interval_seconds` (default: 60): How often to check
- `timeout_seconds` (default: 10): Request timeout
- `expected_status_code` (default: 200): Expected HTTP status for healthy service
- `enabled` (default: true): Whether monitoring is enabled
- `check_response_body` (default: false): Validate response body
- `expected_body_content` (optional): Expected substring in response body

### 8. Update Monitored Service Configuration

```bash
curl -X PUT http://raspberrypi.local:8000/monitored-services/{service_name} \
  -H "Content-Type: application/json" \
  -d '{
    "name": "my-service",
    "health_url": "http://localhost:3000/health",
    "check_interval_seconds": 30,
    "timeout_seconds": 5,
    "expected_status_code": 200,
    "enabled": true,
    "check_response_body": false,
    "expected_body_content": null
  }'
```

**Note**: The `name` in the request body must match `{service_name}` in the URL.

### 9. Remove Monitored Service

Remove a service from automatic monitoring configuration:

```bash
curl -X DELETE http://raspberrypi.local:8000/monitored-services/{service_name}
```

This will:
- Stop the automatic health checking
- Remove the service from configuration file
- Not remove the service's current status from `/services`

### 10. Manually Trigger Health Check

Immediately check the health of a monitored service:

```bash
curl -X POST http://raspberrypi.local:8000/monitored-services/{service_name}/check
```

**Response**:
```json
{
  "success": true,
  "service_name": "my-service",
  "status": "up",
  "message": "Health check passed (200)",
  "metadata": {
    "health_url": "http://localhost:3000/health",
    "http_status_code": "200",
    "response_time_ms": "45.23"
  }
}
```

### 11. Get Notification History

View notification history for all services:

```bash
curl -s http://raspberrypi.local:8000/notifications/history | jq .
```

### 12. Check Service Monitor Health

Check if the service-monitor itself is healthy:

```bash
curl -s http://raspberrypi.local:8000/health | jq .
```

**Response**:
```json
{
  "status": "healthy",
  "timestamp": "2025-10-23T20:00:00Z",
  "uptime_seconds": 3600.5,
  "monitored_services": 5
}
```

## Usage Guidelines

When using this skill:

1. **Always use `jq` for formatting** JSON responses for better readability
2. **Check monitored services first** to see what's configured
3. **Use `/services` for current status**, `/monitored-services` for configuration
4. **Add services to monitored-services** for automatic health checking
5. **Handle errors gracefully** - API returns appropriate HTTP status codes
6. **Use manual checks** (`/monitored-services/{name}/check`) for immediate verification

## Example Workflows

### Add a New Service to Monitor

1. Check if service already exists:
   ```bash
   curl -s http://raspberrypi.local:8000/monitored-services/my-service
   ```

2. If not found, add it:
   ```bash
   curl -X POST http://raspberrypi.local:8000/monitored-services \
     -H "Content-Type: application/json" \
     -d '{
       "name": "my-service",
       "health_url": "http://localhost:3000/health",
       "check_interval_seconds": 60,
       "timeout_seconds": 10,
       "expected_status_code": 200,
       "enabled": true
     }'
   ```

3. Verify it's being monitored:
   ```bash
   curl -s http://raspberrypi.local:8000/services/my-service | jq .
   ```

### Check Service Health Status

1. Get all services and their status:
   ```bash
   curl -s http://raspberrypi.local:8000/services | jq '.[] | {name: .service_name, status: .status, message: .message}'
   ```

2. Get only problematic services:
   ```bash
   curl -s http://raspberrypi.local:8000/services/status/down | jq .
   curl -s http://raspberrypi.local:8000/services/status/degraded | jq .
   ```

### Update Service Configuration

1. Get current configuration:
   ```bash
   curl -s http://raspberrypi.local:8000/monitored-services/my-service | jq .service
   ```

2. Update with new settings:
   ```bash
   curl -X PUT http://raspberrypi.local:8000/monitored-services/my-service \
     -H "Content-Type: application/json" \
     -d '{
       "name": "my-service",
       "health_url": "http://localhost:3000/health",
       "check_interval_seconds": 30,
       "timeout_seconds": 10,
       "expected_status_code": 200,
       "enabled": true
     }'
   ```

### Remove a Service

1. Stop monitoring (removes from configuration):
   ```bash
   curl -X DELETE http://raspberrypi.local:8000/monitored-services/my-service
   ```

2. Optionally, remove current status:
   ```bash
   curl -X DELETE http://raspberrypi.local:8000/services/my-service
   ```

## Error Handling

The API uses standard HTTP status codes:
- **200**: Success
- **201**: Created (for new check-ins)
- **204**: No Content (successful deletion)
- **400**: Bad Request (invalid parameters)
- **404**: Not Found (service doesn't exist)
- **422**: Validation Error (invalid request body)
- **500**: Internal Server Error

Always check the response status and handle errors appropriately.

## Integration Notes

- The service-monitor runs on `raspberrypi.local:8000`
- Configuration is persisted in `monitored_services.json` at the project root
- Web dashboard available at `http://raspberrypi.local:8000/`
- API documentation at `http://raspberrypi.local:8000/docs`
- Service automatically checks for "stale" services that haven't checked in
- Notifications are sent when services change state (if configured)
