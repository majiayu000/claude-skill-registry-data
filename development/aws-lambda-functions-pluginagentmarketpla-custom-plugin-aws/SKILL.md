---
name: aws-lambda-functions
description: Build optimized serverless functions with Lambda
sasmp_version: "1.3.0"
bonded_agent: 07-aws-serverless
bond_type: PRIMARY_BOND
---

# AWS Lambda Functions Skill

Develop high-performance serverless functions with best practices.

## Quick Reference

| Attribute | Value |
|-----------|-------|
| AWS Service | Lambda |
| Complexity | Medium |
| Est. Time | 5-15 min |
| Prerequisites | IAM Role, (Optional) VPC |

## Parameters

### Required
| Parameter | Type | Description | Validation |
|-----------|------|-------------|------------|
| function_name | string | Function name | ^[a-zA-Z0-9-_]{1,64}$ |
| runtime | string | Runtime environment | python3.12, nodejs20.x, etc. |
| handler | string | Handler function | module.function |
| role_arn | string | Execution role ARN | Valid IAM role ARN |

### Optional
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| memory_mb | int | 128 | Memory allocation (128-10240) |
| timeout | int | 3 | Timeout seconds (1-900) |
| architecture | string | x86_64 | x86_64 or arm64 |
| environment | object | {} | Environment variables |
| vpc_config | object | null | VPC configuration |

## Execution Flow

```
1. Package code and dependencies
2. Create/update function
3. Configure triggers
4. Set concurrency limits
5. Test invocation
6. Monitor cold starts
```

## Implementation

### Create Function
```bash
# Create deployment package
zip -r function.zip . -x "*.git*"

# Create function
aws lambda create-function \
  --function-name my-function \
  --runtime python3.12 \
  --architectures arm64 \
  --handler main.handler \
  --role arn:aws:iam::123456789012:role/lambda-role \
  --zip-file fileb://function.zip \
  --memory-size 1024 \
  --timeout 30 \
  --environment "Variables={LOG_LEVEL=INFO}" \
  --tracing-config Mode=Active
```

### Handler Template (Python)
```python
import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def handler(event, context):
    """
    Lambda handler function.

    Args:
        event: Trigger event data
        context: Runtime context (request_id, memory_limit, etc.)

    Returns:
        Response object or value
    """
    try:
        logger.info(f"Event: {json.dumps(event)}")

        # Business logic here
        result = process_event(event)

        return {
            "statusCode": 200,
            "body": json.dumps(result)
        }
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
```

### Handler Template (Node.js)
```javascript
export const handler = async (event, context) => {
    console.log('Event:', JSON.stringify(event));

    try {
        const result = await processEvent(event);

        return {
            statusCode: 200,
            body: JSON.stringify(result)
        };
    } catch (error) {
        console.error('Error:', error);
        return {
            statusCode: 500,
            body: JSON.stringify({ error: error.message })
        };
    }
};
```

## Memory/CPU Optimization

| Memory | vCPU | Network | Use Case |
|--------|------|---------|----------|
| 128 MB | 0.08 | Low | Simple transforms |
| 512 MB | 0.33 | Low | Basic API handlers |
| 1024 MB | 0.58 | Medium | Standard workloads |
| 1769 MB | 1.0 | Medium | CPU-bound tasks |
| 3008 MB | 2.0 | High | Parallel processing |
| 10240 MB | 6.0 | Very High | Data processing |

## Cold Start Mitigation

1. **Use arm64**: ~34% better price-performance
2. **Minimize package**: Only required dependencies
3. **Use Layers**: Shared dependencies
4. **Provisioned Concurrency**: Pre-warmed functions
5. **SnapStart (Java)**: Cached initialization
6. **Avoid VPC**: Unless necessary (+1s cold start)

## Troubleshooting

### Common Issues
| Symptom | Cause | Solution |
|---------|-------|----------|
| Timeout | Long execution | Increase timeout, optimize code |
| OOM (signal: killed) | Memory exceeded | Increase memory |
| Import error | Missing dependency | Check package includes deps |
| Permission denied | IAM role | Update execution role |

### Debug Checklist
- [ ] Handler path correct (file.function)?
- [ ] All dependencies packaged?
- [ ] Execution role has permissions?
- [ ] Environment variables set?
- [ ] Memory sufficient for workload?
- [ ] Timeout appropriate?
- [ ] VPC has NAT for internet?

### CloudWatch Log Patterns
```
Task timed out after X.XX seconds → Increase timeout
Runtime exited with error: signal: killed → Increase memory
Unable to import module → Check handler path/dependencies
ECONNREFUSED → Check VPC/security group
```

## Test Template

```python
def test_lambda_handler():
    # Arrange
    event = {"key": "value"}
    context = MockContext()

    # Act
    response = handler(event, context)

    # Assert
    assert response["statusCode"] == 200
    body = json.loads(response["body"])
    assert "result" in body
```

## Observability

### X-Ray Tracing
```python
from aws_xray_sdk.core import xray_recorder

@xray_recorder.capture('process_data')
def process_data(data):
    # Traced function
    pass
```

### Structured Logging
```json
{
  "level": "INFO",
  "message": "Processing request",
  "request_id": "abc-123",
  "function_name": "my-function",
  "cold_start": true
}
```

## Assets

- `assets/lambda-template.py` - Python handler template

## References

- [Lambda Developer Guide](https://docs.aws.amazon.com/lambda/latest/dg/)
- [Lambda Best Practices](https://docs.aws.amazon.com/lambda/latest/dg/best-practices.html)
