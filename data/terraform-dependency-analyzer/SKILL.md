---
name: terraform-dependency-analyzer
description: Analyzes and visualizes resource dependencies in Terraform configurations, identifies circular dependencies, and suggests optimal resource ordering. This skill should be used when users need to understand resource relationships, troubleshoot dependency issues, optimize apply order, or refactor complex configurations.
---

# Terraform Dependency Analyzer

This skill helps analyze and optimize resource dependencies in Terraform configurations.

## When to Use

Use this skill when:
- Understanding resource relationships and dependencies
- Troubleshooting circular dependency errors
- Optimizing resource creation order
- Refactoring complex configurations
- Documenting infrastructure dependencies

## Dependency Types

### Implicit Dependencies

Terraform automatically detects dependencies through resource attribute references:
- Most common and preferred method
- Created when one resource references another's attributes
- Example: `subnet_id = aws_subnet.main.id`

### Explicit Dependencies

Use `depends_on` only when implicit dependencies aren't sufficient:
- Cross-resource timing requirements
- Dependencies not expressed through attributes
- Ensuring proper creation/deletion order
- Should be used sparingly

## Analysis Workflow

### 1. Generate Dependency Graph

```bash
# Create visual dependency graph
terraform graph | dot -Tpng > graph.png

# View as text
terraform graph
```

### 2. Identify Resource Relationships

Parse configuration to map dependencies:
- Read through resource definitions
- Note attribute references between resources
- Identify explicit `depends_on` declarations
- Map out dependency chains

### 3. Check for Circular Dependencies

**Common causes:**
- Security groups with mutual ingress rules
- Resources referencing each other's attributes
- Module outputs creating circular references

**Solution approaches:**
- Break cycles using separate rule resources
- Restructure resource relationships
- Use data sources to break circular references

## Common Dependency Patterns

### VPC Infrastructure
1. VPC → Internet Gateway, Subnets
2. Subnets → NAT Gateway, Route Tables
3. Route Tables → Route Table Associations
4. Security Groups → EC2/RDS instances

### IAM Resources
1. IAM Role → IAM Policy Attachments
2. IAM Role → Resources using the role

### Database Setup
1. VPC, Subnets → DB Subnet Group
2. Security Group → RDS Instance
3. RDS Instance → Application resources

## Troubleshooting

### Circular Dependency Errors

**Process:**
1. Identify the resources in the cycle from error message
2. Determine which reference creates the cycle
3. Break the cycle by:
   - Using separate rule resources (for security groups)
   - Restructuring resource relationships
   - Using data sources instead of direct references

### Slow Apply Times

**Analysis:**
- Check for unnecessary `depends_on` statements forcing sequential creation
- Identify resources that could be created in parallel
- Look for bottleneck resources blocking multiple dependencies

**Optimization:**
- Remove explicit dependencies when implicit ones exist
- Group independent resources together
- Use modules to organize related resources

## Optimization Guidelines

### Minimize Explicit Dependencies

- Prefer implicit dependencies through attribute references
- Only use `depends_on` when absolutely necessary
- Remove redundant explicit dependencies

### Maximize Parallelization

- Ensure independent resources have no unnecessary dependencies
- Group related resources in modules
- Avoid creating artificial dependency chains

### Use Modules Effectively

- Organize resources by logical grouping
- Use module outputs to express dependencies
- Keep module dependencies clear and minimal

## Analysis Checklist

- [ ] Generated dependency graph
- [ ] Identified all resource relationships
- [ ] Checked for circular dependencies
- [ ] Verified implicit dependencies are sufficient
- [ ] Removed unnecessary `depends_on` statements
- [ ] Identified opportunities for parallelization
- [ ] Documented critical dependency chains
