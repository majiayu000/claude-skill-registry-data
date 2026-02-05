---
name: aws-cloudformation
description: Infrastructure as Code with CloudFormation templates and stacks
sasmp_version: "1.3.0"
bonded_agent: 08-aws-devops
bond_type: PRIMARY_BOND
---

# AWS CloudFormation Skill

Create and manage infrastructure as code with CloudFormation.

## Quick Reference

| Attribute | Value |
|-----------|-------|
| AWS Service | CloudFormation |
| Complexity | Medium-High |
| Est. Time | 10-60 min |
| Prerequisites | IAM permissions |

## Parameters

### Required
| Parameter | Type | Description | Validation |
|-----------|------|-------------|------------|
| stack_name | string | Stack name | ^[a-zA-Z][-a-zA-Z0-9]{0,127}$ |
| template_path | string | Template file path | Valid YAML/JSON |

### Optional
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| parameters | object | {} | Stack parameters |
| capabilities | array | [] | CAPABILITY_IAM, etc. |
| tags | object | {} | Resource tags |
| termination_protection | bool | false | Prevent deletion |
| rollback_on_failure | bool | true | Rollback on error |

## Template Structure

```yaml
AWSTemplateFormatVersion: '2010-09-09'
Description: 'Production VPC with 3-tier architecture'

Parameters:
  Environment:
    Type: String
    AllowedValues: [dev, staging, prod]

Mappings:
  RegionMap:
    us-east-1:
      AMI: ami-12345678

Conditions:
  IsProd: !Equals [!Ref Environment, prod]

Resources:
  VPC:
    Type: AWS::EC2::VPC
    Properties:
      CidrBlock: 10.0.0.0/16
      Tags:
        - Key: Name
          Value: !Sub ${Environment}-vpc

Outputs:
  VPCId:
    Value: !Ref VPC
    Export:
      Name: !Sub ${Environment}-VPCId
```

## Implementation

### Deploy Stack
```bash
# Validate template
aws cloudformation validate-template \
  --template-body file://template.yaml

# Create stack
aws cloudformation create-stack \
  --stack-name my-stack \
  --template-body file://template.yaml \
  --parameters ParameterKey=Environment,ParameterValue=prod \
  --capabilities CAPABILITY_IAM CAPABILITY_NAMED_IAM \
  --tags Key=Environment,Value=Production \
  --enable-termination-protection

# Wait for completion
aws cloudformation wait stack-create-complete --stack-name my-stack
```

### Update Stack
```bash
# Create change set (preview changes)
aws cloudformation create-change-set \
  --stack-name my-stack \
  --change-set-name my-changes \
  --template-body file://template.yaml \
  --parameters ParameterKey=Environment,ParameterValue=prod

# Review changes
aws cloudformation describe-change-set \
  --stack-name my-stack \
  --change-set-name my-changes

# Execute change set
aws cloudformation execute-change-set \
  --stack-name my-stack \
  --change-set-name my-changes
```

## Nested Stacks Pattern

```yaml
Resources:
  VPCStack:
    Type: AWS::CloudFormation::Stack
    Properties:
      TemplateURL: https://s3.amazonaws.com/bucket/vpc.yaml
      Parameters:
        Environment: !Ref Environment

  DatabaseStack:
    Type: AWS::CloudFormation::Stack
    DependsOn: VPCStack
    Properties:
      TemplateURL: https://s3.amazonaws.com/bucket/rds.yaml
      Parameters:
        VPCId: !GetAtt VPCStack.Outputs.VPCId
```

## Troubleshooting

### Common Issues
| Symptom | Cause | Solution |
|---------|-------|----------|
| CREATE_FAILED | Resource error | Check events for details |
| UPDATE_ROLLBACK | Update failed | Review change set |
| DELETE_FAILED | Resource in use | Remove dependencies |
| ROLLBACK_COMPLETE | Creation failed | Delete and fix |

### Debug Checklist
- [ ] Template valid (`validate-template`)?
- [ ] Required capabilities specified?
- [ ] Parameters have valid values?
- [ ] IAM has required permissions?
- [ ] Resource dependencies correct?
- [ ] No circular references?

### Stack Events Analysis
```bash
# Get stack events
aws cloudformation describe-stack-events \
  --stack-name my-stack \
  --query 'StackEvents[?ResourceStatus==`CREATE_FAILED`]'
```

### Common Errors
```
Resource handler returned message: ... → Provider-specific error
Circular dependency between resources → Use DependsOn carefully
Export ... cannot be updated → Update dependent stacks first
Template format error → Check YAML syntax
```

## Best Practices

1. **Use Change Sets**: Always preview before updating
2. **Enable Termination Protection**: For production stacks
3. **Use Nested Stacks**: For reusable components
4. **Export Outputs**: For cross-stack references
5. **Use Stack Policies**: Protect critical resources
6. **Version Templates**: Store in Git

## Test Template

```python
def test_cloudformation_template():
    # Arrange
    template_body = open('template.yaml').read()

    # Act - Validate
    response = cfn.validate_template(TemplateBody=template_body)

    # Assert
    assert 'Parameters' in response
    assert response['Capabilities'] == ['CAPABILITY_IAM']

    # Act - Create stack (dry run)
    # Use change set with no execute for testing
```

## Assets

- `assets/vpc-template.yaml` - Production VPC template

## References

- [CloudFormation User Guide](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/)
- [Best Practices](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/best-practices.html)
