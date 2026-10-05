---




name: aws-iam
description: Implements AWS Identity and Access Management (IAM) for securely managing users, groups, roles, and permissions in the AWS ecosystem.
license: MIT
compatibility: opencode
metadata:
  version: "1.1.1"
  domain: cloud
  triggers: aws iam, identity management, access control, permissions, user management
  archetypes: [implementation, access management]
  anti_triggers: [overly permissive policies]
  response_profile:
    verbosity: medium
    directive_strength: high
    abstraction_level: operational

  role: implementation
  scope: implementation
  output-format: code



---





## Comprehensive Guide to AWS IAM
AWS Identity and Access Management (IAM) enables organizations to manage access and user identities effectively. Here’s an in-depth exploration of its features and best practices:

### Key Features:
- **Secure Control of Access**: Manage permissions to AWS resources securely, ensuring only authorized users have access.
- **Multi-Factor Authentication (MFA)**: Increase security by requiring multiple forms of verification.
- **Identity Federation**: Allows users to log into AWS using external identity providers like Google or Facebook.

### Best Practices:
1. **Principle of Least Privilege**: Always assign the least amount of privilege necessary for users to perform their tasks effectively. This minimizes security risks associated with human error or unauthorized access.
2. **Utilize IAM Roles for AWS Services**: Instead of hardcoding credentials, assign roles to AWS services that require access to other AWS services, thereby enhancing security posture.
3. **Implement MFA**: Add an additional layer of security by requiring Multi-Factor Authentication for sensitive operations.
4. **Regularly Audit Permissions**: Use AWS IAM Access Analyzer and CloudTrail to monitor user permissions and remove any unnecessary ones periodically.

### Implementation Example: Creating a User and Assigning Permissions
```python
import json
import boto3
from botocore.exceptions import ClientError

# Create IAM client
client = boto3.client('iam')

# Function to create a new IAM user

def create_user(user_name):
    try:
        client.create_user(UserName=user_name)
        print(f"User '{user_name}' created successfully.")
    except ClientError as e:
        print(f"Error creating user: {e}")

# Function to attach a policy to the user

def attach_policy(user_name, policy_arn):
    try:
        client.attach_user_policy(
            UserName=user_name,
            PolicyArn=policy_arn
        )
        print(f"Policy '{policy_arn}' attached to user '{user_name}'.")
    except ClientError as e:
        print(f"Error attaching policy: {e}")

# Create user and assign permissions
user_name = 'NewUser'
create_user(user_name)
attach_policy(user_name, 'arn:aws:iam::aws:policy/ReadOnlyAccess')
```

### FAQs About AWS IAM Functionality:
- **Q: Can IAM roles be used in Lambda functions?**  
Yes! AWS Lambda functions can assume IAM roles to get necessary permissions dynamically.
- **Q: How do I audit IAM usage?**  
Utilize AWS CloudTrail for tracking user activity and AWS Config rules to evaluate IAM configurations.
- **Q: Is it possible to enforce tagging for resource access?**  
Absolutely! IAM allows you to create policies that enforce tag-based access control, helping align permissions with resources effectively.

By leveraging AWS IAM, organizations can build a robust security framework to manage access and permissions efficiently in their AWS environments, helping gain better control over sensitive data and operations.
---

---

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

> Authoritative documentation links for this skill's domain. The model follows markdown links at load time to resolve external references and inline content.

- [Primary Documentation](https://docs.aws.amazon.com/IAM/latest/UserGuide/introduction.html)
- [API Reference or Getting Started](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies.html)
- [Configuration Guide](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles.html)
- [Best Practices](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html)
- [Common Patterns or Tutorials](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_management_scheduled-change.html)

