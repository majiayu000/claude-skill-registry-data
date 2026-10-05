---




name: aws-sns
description: Implements Amazon Simple Notification Service (SNS) for building and managing message-driven applications through an event-driven architecture.
license: MIT
compatibility: opencode
metadata:
  version: "1.1.1"
  domain: cloud
  triggers: aws sns, event-driven architecture, notification service, publish-subscribe model, scalable messaging
  archetypes: [implementation, event management]
  anti_triggers: [hardcoded notification systems]
  response_profile:
    verbosity: medium
    directive_strength: high
    abstraction_level: operational
  role: implementation
  scope: infrastructure
  output-format: code




---





## Enhanced Content for AWS SNS Skill

### Overview of Amazon SNS
Amazon Simple Notification Service (SNS) is a fully managed service for enabling message-driven application architectures with numerous advantages, including:
- **Decoupled Architecture**: Using a publish-subscribe architecture, it decouples the components of the application allowing for easy scaling and management.
- **Scalable Messaging**: Seamlessly handle the broadcast of messages to various endpoints without the need for manual intervention.
- **Flexibility**: Allows messages to be sent directly to subscribers as push notifications via mobile devices, email, or SQS queues.

### Core Features:
1. **Topic Management**: Create and manage topics with ease for different messaging scenarios.
2. **Enhanced Security**: Utilize IAM policies to control permissions and ensure secure access to your messaging resources.
3. **Integration with Other AWS Services**: Integrate effortlessly with AWS Lambda, Amazon SQS, APIs, and more for creating dedicated workflows.

### Security Best Practices:
- **IAM Policies**: Define least privilege permissions at the IAM policy level to restrict user access to SNS topics or subscriptions.
- **Message Access Logging**: Implement logging with AWS CloudTrail to track access and actions taken on SNS operations for compliance.
- **Use HTTPS**: Secure endpoints using HTTPS to prevent interception during message delivery.

### Example: How to Use AWS SNS with Boto3
```python
import boto3

# Create an SNS client
client = boto3.client('sns')

# Create a new SNS topic
response = client.create_topic(Name='MyTopic')

# Publish a message to the topic
response = client.publish(
    TopicArn=response['TopicArn'],
    Message='This is my first SNS message!',
)
print(response['MessageId'])
```

### FAQs About AWS SNS Functionality:
- **Q: Can I use AWS SNS for mobile notifications?**  
Absolutely! AWS SNS supports the integration of mobile push notifications across various platforms including iOS and Android.
- **Q: How does SNS integrate with Lambda?**  
SNS can trigger Lambda functions upon message delivery, making it suitable for event-driven architectures.
- **Q: Can I send messages to multiple endpoints?**  
Yes, SNS allows messages to be broadcasted to multiple endpoints, including SQS queues, Lambda functions, and HTTP endpoints.

By implementing AWS SNS strategies, businesses can efficiently manage messaging needs, enhance application decoupling, and ensure a secure and scalable infrastructure.

---



### Pattern 2: SNS with Subscriptions and Message Filtering

```python
import boto3
from typing import Optional


def create_topic_and_subscribe(client, topic_name: str, protocol: str, endpoint: str) -> dict:
    """Create an SNS topic with a subscription."""
    topic_resp = client.create_topic(Name=topic_name)
    topic_arn = topic_resp["TopicArn"]

    sub_resp = client.subscribe(
        TopicArn=topic_arn,
        Protocol=protocol,
        Endpoint=endpoint,
    )
    print(f"Created subscription: {sub_resp['SubscriptionArn']} for topic {topic_arn}")
    return {"topic_arn": topic_arn, "subscription_arn": sub_resp["SubscriptionArn"]}


def publish_with_attributes(client, topic_arn: str, message: str,
                             event_type: str = "general") -> dict:
    """Publish a message with attributes for subscriber filtering."""
    response = client.publish(
        TopicArn=topic_arn,
        Message=message,
        MessageAttributes={
            "event_type": {"DataType": "String", "StringValue": event_type},
            "priority": {"DataType": "String", "StringValue": "high"},
        },
    )
    print(f"Published message with attributes to {topic_arn}: {response['MessageId']}")
    return response


def get_topic_attributes(client, topic_arn: str) -> dict:
    """Get all attributes for an SNS topic."""
    return client.get_topic_attributes(TopicArn=topic_arn)
```

## Constraints

### MUST DO
- Configure all AWS resources with explicit tagging for cost allocation, ownership tracking, and compliance
- Use AWS SDK (Boto3) typed clients instead of resource API where type safety matters — prefer client() over resource()
- Implement error handling that distinguishes between retryable (Throttling, RequestLimitExceeded) and non-retryable errors
- Use IAM roles with least-privilege policies scoped to specific actions and resources, never wildcard permissions

### MUST NOT DO
- Do not hardcode AWS credentials — use IAM roles, environment variables, or AWS Secrets Manager
- Avoid unencrypted S3 buckets or RDS instances in production without explicit KMS encryption configuration
- Never launch EC2 instances without specifying a security group and subnet — always use VPC networking explicitly
- Do not use the default endpoint region — always specify the target region explicitly in all SDK calls


## Live References

> Authoritative documentation links for this domain. The model follows markdown links at load time to resolve external references and inline content.

- [Amazon SNS Documentation](https://docs.aws.amazon.com/sns/) — Official AWS SNS documentation covering topics, subscriptions, message publishing, and delivery status
- [SNS vs SQS Architecture Patterns (AWS)](https://aws.amazon.com/sns/faqs/) — AWS FAQ comparing SNS pub/sub patterns with SQS point-to-point queue patterns for messaging design decisions
- [SNS Topic Policies and Permissions](https://docs.aws.amazon.com/sns/latest/dg/sns-topic-policies.html) — Official guide to configuring access policies, permissions, and security for SNS topics
- [SNS Message Attributes and Filtering](https://docs.aws.amazon.com/sns/latest/dg/message-filtering.html) — AWS documentation on using message attributes for subscriber filtering and routing
- [AWS SDK for Python (boto3) with SNS](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html) — Official boto3 reference for programmatic SNS operations in Python applications