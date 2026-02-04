---
name: aws-iam-setup
description: Configure AWS IAM users, roles, policies, and identity federation
sasmp_version: "1.3.0"
bonded_agent: 01-aws-fundamentals
bond_type: PRIMARY_BOND
---

# AWS IAM Setup Skill

Configure secure identity and access management for AWS resources.

## Quick Reference

| Attribute | Value |
|-----------|-------|
| AWS Service | IAM |
| Complexity | Medium |
| Est. Time | 15-30 min |
| Prerequisites | AWS account, admin access |

## Parameters

### Required
| Parameter | Type | Description | Validation |
|-----------|------|-------------|------------|
| entity_type | string | user, role, group, policy | enum |
| entity_name | string | Name for the entity | ^[a-zA-Z0-9+=,.@_-]{1,64}$ |
| action | string | create, update, delete, attach | enum |

### Optional
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| path | string | / | IAM path for organization |
| max_session_duration | int | 3600 | Role session duration (seconds) |
| permissions_boundary | string | null | ARN of permissions boundary |
| tags | object | {} | Resource tags |

## Implementation

### Create IAM User
```bash
# Create user with console access
aws iam create-user --user-name $USERNAME --path /developers/

# Create access keys
aws iam create-access-key --user-name $USERNAME

# Attach managed policy
aws iam attach-user-policy \
  --user-name $USERNAME \
  --policy-arn arn:aws:iam::aws:policy/PowerUserAccess
```

### Create IAM Role
```bash
# Create role with trust policy
aws iam create-role \
  --role-name $ROLE_NAME \
  --assume-role-policy-document file://trust-policy.json \
  --max-session-duration 7200

# Attach policy
aws iam attach-role-policy \
  --role-name $ROLE_NAME \
  --policy-arn arn:aws:iam::aws:policy/ReadOnlyAccess
```

### Trust Policy Example
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {"Service": "ec2.amazonaws.com"},
      "Action": "sts:AssumeRole"
    }
  ]
}
```

## Retry Logic

```python
def iam_operation_with_retry(operation, max_retries=3):
    for attempt in range(max_retries):
        try:
            return operation()
        except iam.exceptions.LimitExceededException:
            time.sleep(2 ** attempt)
    raise Exception("Max retries exceeded")
```

## Troubleshooting

### Common Issues
| Symptom | Cause | Solution |
|---------|-------|----------|
| EntityAlreadyExists | Duplicate name | Use unique name or update |
| MalformedPolicyDocument | Invalid JSON | Validate policy syntax |
| LimitExceeded | Too many entities | Delete unused or request increase |

### Debug Checklist
- [ ] Policy JSON valid?
- [ ] Trust relationship allows assumed principal?
- [ ] Path matches organization standards?
- [ ] MFA configured for privileged users?

## Security Best Practices

1. **Least Privilege**: Grant minimum required permissions
2. **Use Roles**: Prefer roles over long-term credentials
3. **MFA Required**: Enforce MFA for console access
4. **No Root Usage**: Never use root for daily operations
5. **Regular Rotation**: Rotate access keys every 90 days

## Test Template

```python
def test_iam_role_creation():
    # Arrange
    role_name = "test-role-" + str(uuid.uuid4())[:8]

    # Act
    role = create_iam_role(role_name, trust_policy)

    # Assert
    assert role["Arn"].endswith(role_name)

    # Cleanup
    delete_iam_role(role_name)
```

## Assets

- `assets/iam-policies.yaml` - Common policy templates

## References

- [IAM Best Practices](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html)
- [Policy Reference](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies.html)
