---
name: setup-deployer
description: Interactive guide for installing and configuring AWS Deployer infrastructure - builds Lambda functions, deploys CloudFormation stacks, and sets up multi-account targets and GitHub OIDC integration.
---

# AWS Deployer Setup and Configuration

This skill guides users through the complete setup and configuration of **AWS Deployer** ([github.com/savaki/aws-deployer](https://github.com/savaki/aws-deployer)), a serverless CloudFormation deployment automation system that orchestrates infrastructure deployments using AWS Step Functions, Lambda, and DynamoDB.

## What is AWS Deployer?

AWS Deployer is a serverless system that automates CloudFormation deployments across single or multiple AWS accounts. It:
- Monitors S3 for CloudFormation templates and automatically deploys them
- Uses Step Functions to orchestrate complex multi-stage deployments
- Supports promotion workflows (dev → staging → production)
- Integrates with GitHub Actions via OIDC for secure CI/CD
- Provides optional web UI for deployment monitoring

## Your Task

When this skill is invoked, you are helping the user set up AWS Deployer from scratch. Your role is to **interactively guide** them through the complete setup process:

1. **Gather requirements** - Ask about their deployment needs (single vs multi-account, custom domain, etc.)
2. **Verify prerequisites** - Ensure they have AWS CLI, Go, S3 bucket, and necessary permissions
3. **Build the project** - Guide them to compile all Lambda functions
4. **Deploy infrastructure** - Help construct and execute the CloudFormation deployment command
5. **Configure targets** - Set up deployment targets for multi-account mode (if applicable)
6. **Setup GitHub integration** - Configure OIDC roles and secrets for CI/CD
7. **Verify setup** - Confirm all infrastructure is deployed correctly

**Important**: This is an **interactive, step-by-step process**. Don't just provide all the instructions at once. Ask questions, wait for responses, verify each step is complete before moving to the next one, and adapt to the user's specific needs.

## Prerequisites Check

Before starting, verify the user has:

- AWS CLI installed and configured with appropriate credentials
- Go 1.24+ installed
- An S3 bucket for artifacts (ask for bucket name or help create one)
- IAM permissions to create:
  - Lambda functions
  - Step Functions state machines
  - DynamoDB tables
  - IAM roles and policies
  - CloudFormation stacks
- For multi-account: IAM roles in target accounts
- For custom domain: Route 53 hosted zone in the deployment account managing the domain's nameservers

## Setup Process

### 1. Gather Requirements

Ask the user:

1. **Environment name**: What environment are they setting up? (dev, stg, prd)
2. **Deployment mode**: Single-account or multi-account deployments?
3. **S3 bucket**: Do they have an existing artifacts bucket, or should one be created?
4. **Custom domain**: Do they want to set up a custom domain for the API Gateway? (optional)
   - **Important**: The AWS account must manage the domain's nameservers via Route 53
   - The Route 53 hosted zone must already exist
   - They'll need the Hosted Zone ID
5. **Authorization**: Should access be restricted to specific email addresses? (optional)
6. **AWS Region**: Which region to deploy to? (default: us-east-1)

### 2. Build the Project

Guide the user to build all Lambda functions:

```bash
make build
```

Verify the build succeeded by checking for `.zip` files in the `build/` directory.

### 3. Set Up Custom Domain Prerequisites (Optional)

If the user wants a custom domain, guide them through these prerequisites:

**Verify Route 53 Hosted Zone:**
```bash
# List hosted zones to find the Zone ID
aws route53 list-hosted-zones-by-name --dns-name example.com

# Verify nameservers are properly configured
aws route53 get-hosted-zone --id <ZONE_ID>
```

**Important**: The domain's nameservers at the registrar must point to the AWS Route 53 nameservers shown in the hosted zone.

**Create/Verify ACM Certificate:**
```bash
# Request a certificate (if not already exists)
aws acm request-certificate \
  --domain-name deployer.example.com \
  --validation-method DNS \
  --region <region>

# List certificates to find the ARN
aws acm list-certificates --region <region>

# Get certificate details and validation records
aws acm describe-certificate --certificate-arn <CERTIFICATE_ARN> --region <region>
```

**Important**:
- The ACM certificate must be in the same region as the deployment
- DNS validation records must be added to Route 53
- Wait for certificate status to be `ISSUED` before deploying

**Verify Certificate is Issued:**
```bash
aws acm describe-certificate \
  --certificate-arn <CERTIFICATE_ARN> \
  --region <region> \
  --query 'Certificate.Status' \
  --output text
```

Should return `ISSUED` before proceeding.

### 4. Deploy Infrastructure

Help construct the deployment command based on their requirements:

**Basic deployment:**
```bash
ENV=dev S3_BUCKET=<bucket-name> make deploy
```

**With custom domain:**
```bash
ENV=prd \
  S3_BUCKET=<bucket-name> \
  ZONE_ID=Z1234567890ABC \
  DOMAIN_NAME=deployer.example.com \
  CERTIFICATE_ARN=arn:aws:acm:us-east-1:123456789012:certificate/abc-123 \
  make deploy
```

**With all optional parameters:**
```bash
ENV=prd \
  S3_BUCKET=<bucket-name> \
  DEPLOYMENT_MODE=multi \
  ALLOWED_EMAIL=admin@example.com \
  ZONE_ID=Z1234567890ABC \
  DOMAIN_NAME=deployer.example.com \
  CERTIFICATE_ARN=arn:aws:acm:... \
  make deploy
```

Monitor the CloudFormation deployment and help troubleshoot any errors.

### 5. Verify Infrastructure

After deployment, verify the CloudFormation stack deployed successfully:

```bash
# Check CloudFormation stack status
aws cloudformation describe-stacks \
  --stack-name <env>-aws-deployer \
  --query 'Stacks[0].StackStatus' \
  --output text
```

Should return `CREATE_COMPLETE` or `UPDATE_COMPLETE`.

If the stack deployed successfully, all resources (Lambda functions, DynamoDB tables, Step Functions, Parameter Store) are configured automatically.

### 6. Set Up Deployment Targets (Multi-Account Mode Only)

If using multi-account mode, configure deployment targets:

**Build the CLI:**
```bash
make build-cli
```

**Configure initial environment:**
```bash
aws-deployer targets config \
  --env <env> \
  --default \
  --initial-env dev
```

**Set up deployment targets for each environment:**

Note: `--downstream-env` specifies where this environment promotes TO (the next environment in the pipeline).

For dev (promotes to staging):
```bash
aws-deployer targets set \
  --env <env> \
  --target-env dev \
  --default \
  --accounts "123456789012" \
  --regions "us-east-1" \
  --downstream-env "staging"
```

For staging (promotes to prd):
```bash
aws-deployer targets set \
  --env <env> \
  --target-env staging \
  --default \
  --accounts "123456789012" \
  --regions "us-east-1,us-west-2" \
  --downstream-env "prd"
```

For production (final environment, no promotion):
```bash
aws-deployer targets set \
  --env <env> \
  --target-env prd \
  --default \
  --accounts "123456789012,987654321098" \
  --regions "us-east-1,us-west-2,eu-west-1"
```

**Verify target configuration:**
```bash
aws-deployer targets list --env <env>
```

### 7. Set Up GitHub Repository for CI/CD

For each repository that will use AWS Deployer:

**Prerequisites:**
- GitHub Personal Access Token (PAT) with `repo` scope stored in AWS Secrets Manager
- Your AWS credentials must have `secretsmanager:GetSecretValue` permission for the GitHub PAT secret

**Create the GitHub PAT secret (if not already exists):**
```bash
# Create the secret with your GitHub PAT
aws secretsmanager create-secret \
  --name github/pat-token \
  --secret-string '{"github_pat":"ghp_xxxxxxxxxxxxx"}'
```

**Create GitHub OIDC role and secrets:**
```bash
aws-deployer setup-github \
  --role-name github-actions-<repo-name> \
  --repo owner/repository-name \
  --bucket <artifacts-bucket> \
  --github-token-secret github/pat-token
```

This creates:
- IAM OIDC provider for GitHub
- IAM role with S3 access scoped to the repository path
- GitHub repository secret with the role ARN (using the PAT from Secrets Manager)

**Provide the user with a sample GitHub Actions workflow:**

```yaml
name: Deploy to AWS
on: [push]

permissions:
  id-token: write
  contents: read

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Configure AWS Credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: ${{ secrets.AWS_ROLE_ARN }}
          aws-region: us-east-1

      - name: Build and package
        run: |
          # Build your application and create CloudFormation template
          # Generate cloudformation-params.json with standard parameters

          REPO="<repo>"
          BRANCH="${{ github.ref_name }}"
          SHA_SHORT="${{ github.sha }}"
          SHA_SHORT="${SHA_SHORT:0:6}"
          VERSION="${{ github.run_number }}.${SHA_SHORT}"
          S3_PREFIX="${REPO}/${BRANCH}/${VERSION}"

          cat > cloudformation-params.json <<EOF
          {
            "Env": "dev",
            "Version": "${VERSION}",
            "S3Bucket": "<bucket>",
            "S3Prefix": "${S3_PREFIX}"
          }
          EOF

      - name: Upload to S3
        run: |
          REPO="<repo>"
          BRANCH="${{ github.ref_name }}"
          SHA_SHORT="${{ github.sha }}"
          SHA_SHORT="${SHA_SHORT:0:6}"
          VERSION="${{ github.run_number }}.${SHA_SHORT}"
          S3_PATH="s3://<bucket>/${REPO}/${BRANCH}/${VERSION}/"

          aws s3 cp cloudformation.template "${S3_PATH}"
          aws s3 cp cloudformation-params.json "${S3_PATH}"
```

**Important**: Your CloudFormation templates should always expect these standard parameters:
- `Env` - Environment name (dev, staging, prd)
- `Version` - Build version in format `{build_number}.{commit_hash}`
- `S3Bucket` - Artifacts bucket name
- `S3Prefix` - S3 path to artifacts in format `{repo}/{branch}/{version}`

### 8. Multi-Account IAM Setup (Multi-Account Mode Only)

For multi-account deployments, set up IAM roles in target accounts:

```bash
aws-deployer setup-aws \
  --account-id <target-account-id> \
  --admin-account-id <deployer-account-id> \
  --role-name AWSCloudFormationStackSetExecutionRole
```

This creates the execution role that CloudFormation StackSets need in each target account.

## Troubleshooting

Help the user diagnose common issues:

### S3 Trigger Not Working
- Verify S3 bucket notification is configured correctly
- Check Lambda permissions to be invoked by S3
- Review S3 trigger Lambda logs

### Step Function Not Starting
- Verify `state-machine-arn` in Parameter Store
- Check DynamoDB stream configuration
- Review trigger-build Lambda logs

### Multi-Account Deployment Failures
- Verify target accounts are configured in DynamoDB
- Check IAM execution roles exist in target accounts
- Verify StackSet administration role has permissions
- Review check-stackset-status Lambda logs for detailed errors

### Lock Acquisition Timeouts
- Check if another deployment is running
- Verify lock TTL hasn't expired prematurely
- Review acquire-lock Lambda logs

### Parameter Store Access Issues
- Verify Lambda IAM roles have `ssm:GetParameter*` permissions
- Check parameter paths match the environment name
- Consider using `DISABLE_SSM=true` for local development

## Completion Verification

Verify the setup is complete by checking the CloudFormation stack status:

```bash
# Check stack status
aws cloudformation describe-stacks \
  --stack-name <env>-aws-deployer \
  --query 'Stacks[0].StackStatus' \
  --output text
```

Should return `CREATE_COMPLETE` or `UPDATE_COMPLETE`.

**If the CloudFormation stack deployed successfully, all infrastructure resources are automatically created:**
- Lambda functions with correct IAM permissions
- DynamoDB tables (builds, targets, deployments, locks)
- Step Function state machines (single and multi-account)
- S3 bucket notification configuration
- Parameter Store values
- API Gateway and custom domain (if configured)

**Additional verification for multi-account setups:**
- [ ] Deployment targets configured (if using multi-account mode)
- [ ] Target account IAM roles created (if using multi-account mode)

**Additional verification for GitHub integration:**
- [ ] GitHub repository configured with OIDC role
- [ ] Test deployment completed successfully

## Next Steps

After setup is complete, guide the user to:

1. Use the `deploy` skill to test their first deployment
2. Review CLAUDE.md for development workflow
3. Read MULTI.md for multi-account deployment details (if applicable)
4. Explore DEPLOYMENT_TARGETS.md for advanced target configuration
5. Set up monitoring and alerting for Step Functions
6. Configure additional repositories for automated deployments

## Reference Commands

Keep these handy for the user:

```bash
# View build history
aws dynamodb query \
  --table-name <env>-aws-deployer--builds \
  --key-condition-expression "pk = :pk" \
  --expression-attribute-values '{":pk":{"S":"<repo>/<env>"}}'

# Update Parameter Store
aws ssm put-parameter \
  --name "/<env>/aws-deployer/<param>" \
  --value "<value>" \
  --overwrite

# View Step Function executions
aws stepfunctions list-executions \
  --state-machine-arn <arn> \
  --max-results 10

# Tail Lambda logs
aws logs tail /aws/lambda/<env>-aws-deployer-<function> --follow

# Update Lambda code
make update-lambda-code

# Full redeployment
make clean-version && make deploy
```
