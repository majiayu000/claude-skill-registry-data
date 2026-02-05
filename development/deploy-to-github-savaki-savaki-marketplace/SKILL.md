---
name: deploy-to-github
description: Set up GitHub Actions to deploy this repository via AWS Deployer - creates workflow, updates CloudFormation template with required parameters, and generates parameter files.
---

# Set Up GitHub Actions Deployment for AWS Deployer

This skill automatically configures a GitHub repository to deploy via **AWS Deployer** ([github.com/savaki/aws-deployer](https://github.com/savaki/aws-deployer)).

## Prerequisites

- AWS Deployer infrastructure is already set up (use `setup-deployer` skill if not)
- Working directory is a Git repository with a GitHub remote
- Repository has a `cloudformation.template` file (will be created if missing)
- Optional: `S3_ARTIFACT_BUCKET` environment variable set to your artifacts bucket
- Optional: `AWS_REGION` environment variable set to your AWS region

## Your Task

When this skill is invoked, you will **configure** the repository for GitHub Actions deployment by:

1. **Detecting repository information** - Extract repo name from `.git/config`
2. **Getting configuration** - Check environment variables (`S3_ARTIFACT_BUCKET`, `AWS_REGION`) first, ask only if not set
3. **Detecting build system** - Identify build command from project files
4. **Creating/updating GitHub workflow** - Generate `.github/workflows/deploy.yml`
5. **Updating CloudFormation template** - Ensure required parameters exist
6. **Creating parameter files** - Generate base and environment-specific templates
7. **Explaining OIDC setup** - Provide instructions for running `aws-deployer setup-github` and configuring GitHub secrets

**Important**:
- Check environment variables first: `S3_ARTIFACT_BUCKET` and `AWS_REGION`
- Only ask for values if environment variables are not set
- Default AWS region to `us-west-2` if not set
- Do NOT run the `aws-deployer setup-github` command. Explain to the user how to run it.
- Explain that THREE GitHub secrets are required: `AWS_ROLE_ARN`, `S3_ARTIFACT_BUCKET`, and `AWS_REGION`.

## Step 1: Detect Repository Information

Extract the repository owner and name from Git configuration:

```bash
# Get the remote URL
git config --get remote.origin.url
```

Parse the result to extract `owner/repo`:
- `https://github.com/foo/bar.git` → `foo/bar`
- `git@github.com:foo/bar.git` → `foo/bar`

Store as `REPO_FULL_NAME` (e.g., `foo/bar`)

## Step 2: Get Configuration

**S3 Bucket**:
1. Check if `S3_ARTIFACT_BUCKET` environment variable is set
   ```bash
   echo $S3_ARTIFACT_BUCKET
   ```
2. If set, use that value
3. If not set, ask the user for the S3 artifacts bucket name
   - Example: `my-artifacts-bucket`
   - This will be stored as a GitHub secret `S3_ARTIFACT_BUCKET`

**AWS Region**:
1. Check if `AWS_REGION` environment variable is set
   ```bash
   echo $AWS_REGION
   ```
2. If set, use that value
3. If not set, ask the user to confirm the AWS region, providing options:
   - Default: `us-west-2`
   - Other common options: `us-east-1`, `us-east-2`, `eu-west-1`, `ap-southeast-1`
   - Allow custom input

**Initial Environment**: Default to `dev` (don't ask)

## Step 3: Detect Build Command

Check for common build files and infer the build command:

- `Makefile` with `build` target → `make build`
- `package.json` with `build` script → `npm run build`
- `go.mod` → `go build ./...`
- `pom.xml` → `mvn package`
- `build.gradle` → `gradle build`

If multiple or none found, ask the user for the build command.

## Step 4: Create/Update GitHub Workflow

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to AWS

on:
  push:
    branches:
      - main
      - develop
  workflow_dispatch:

permissions:
  id-token: write
  contents: read

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: ${{ secrets.AWS_ROLE_ARN }}
          aws-region: ${{ secrets.AWS_REGION }}

      - name: Set version variables
        id: version
        run: |
          REPO="<repo-owner>/<repo-name>"
          BRANCH="${{ github.ref_name }}"
          SHA_SHORT="${{ github.sha }}"
          SHA_SHORT="${SHA_SHORT:0:6}"
          VERSION="${{ github.run_number }}.${SHA_SHORT}"
          S3_PREFIX="${REPO}/${BRANCH}/${VERSION}"

          echo "repo=${REPO}" >> $GITHUB_OUTPUT
          echo "branch=${BRANCH}" >> $GITHUB_OUTPUT
          echo "version=${VERSION}" >> $GITHUB_OUTPUT
          echo "s3_prefix=${S3_PREFIX}" >> $GITHUB_OUTPUT

      - name: Build application
        run: |
          <build-command>

      - name: Generate CloudFormation parameters
        run: |
          cat > cloudformation-params.json <<EOF
          {
            "Env": "dev",
            "Version": "${{ steps.version.outputs.version }}",
            "S3Bucket": "${{ secrets.S3_ARTIFACT_BUCKET }}",
            "S3Prefix": "${{ steps.version.outputs.s3_prefix }}"
          }
          EOF

      - name: Upload to S3
        run: |
          S3_PATH="s3://${{ secrets.S3_ARTIFACT_BUCKET }}/${{ steps.version.outputs.s3_prefix }}/"

          # Upload CloudFormation template
          aws s3 cp cloudformation.template "${S3_PATH}"

          # Upload parameters
          aws s3 cp cloudformation-params.json "${S3_PATH}"

          # Upload environment-specific parameters if they exist
          if [ -f cloudformation-params.dev.json ]; then
            aws s3 cp cloudformation-params.dev.json "${S3_PATH}"
          fi
          if [ -f cloudformation-params.prd.json ]; then
            aws s3 cp cloudformation-params.prd.json "${S3_PATH}"
          fi

          # Upload any build artifacts as needed
          # Example: aws s3 cp build/function.zip "${S3_PATH}"

      - name: Deployment info
        run: |
          echo "✓ Deployed version: ${{ steps.version.outputs.version }}"
          echo "✓ S3 path: s3://${{ secrets.S3_ARTIFACT_BUCKET }}/${{ steps.version.outputs.s3_prefix }}/"
          echo "✓ Environment: dev"
```

**Replace placeholders**:
- `<repo-owner>/<repo-name>`: Full repository name from Git (e.g., `mycompany/my-app`)
- `<build-command>`: Detected or user-provided build command

**Note**: The workflow uses `${{ secrets.AWS_REGION }}` which will be configured as a GitHub secret.

## Step 5: Update CloudFormation Template

If `cloudformation.template` exists, read it and check for required parameters.

If any of these parameters are missing, add them:

```yaml
Parameters:
  Env:
    Type: String
    Default: dev
    Description: Environment name (dev, staging, prd)
    AllowedValues:
      - dev
      - staging
      - prd

  Version:
    Type: String
    Description: Build version in format {build_number}.{commit_hash}

  S3Bucket:
    Type: String
    Description: Artifacts bucket name

  S3Prefix:
    Type: String
    Description: S3 path to artifacts in format {repo}/{branch}/{version}
```

If `cloudformation.template` doesn't exist, create a simple example:

```yaml
AWSTemplateFormatVersion: '2010-09-09'
Description: Deployment for <repo-name>

Parameters:
  Env:
    Type: String
    Default: dev
    Description: Environment name (dev, stg, prd, etc)

  Version:
    Type: String
    Description: Build version in format {build_number}.{commit_hash}

  S3Bucket:
    Type: String
    Description: Artifacts bucket name

  S3Prefix:
    Type: String
    Description: S3 path to artifacts in format {repo}/{branch}/{version}

Resources:
  # TODO: Add your infrastructure resources here
  # Example:
  # MyBucket:
  #   Type: AWS::S3::Bucket
  #   Properties:
  #     BucketName: !Sub '${Env}-<repo-name>-${AWS::AccountId}'
  #     Tags:
  #       - Key: Version
  #         Value: !Ref Version
  #       - Key: Environment
  #         Value: !Ref Env
```

**Common usage patterns**:

### Lambda Function
```yaml
MyFunction:
  Type: AWS::Lambda::Function
  Properties:
    FunctionName: !Sub '${Env}-my-function'
    Code:
      S3Bucket: !Ref S3Bucket
      S3Key: !Sub '${S3Prefix}/function.zip'
    Environment:
      Variables:
        VERSION: !Ref Version
```

### ECS Task Definition
```yaml
TaskDefinition:
  Type: AWS::ECS::TaskDefinition
  Properties:
    Family: !Sub '${Env}-my-service'
    ContainerDefinitions:
      - Name: app
        Image: !Sub '${AWS::AccountId}.dkr.ecr.${AWS::Region}.amazonaws.com/my-app:${Version}'
```

## Step 6: Create Parameter Files

### Base Parameters File

Create `cloudformation-params.json` as a template:

```json
{
  "Env": "dev",
  "Version": "1.000000",
  "S3Bucket": "<bucket-name>",
  "S3Prefix": "<repo-owner>/<repo-name>/main/1.000000"
}
```

Replace:
- `<bucket-name>`: S3 bucket name provided by user
- `<repo-owner>/<repo-name>`: Full repo name from Git

**Note**: The GitHub workflow dynamically generates this file during deployment, but this template file:
1. Shows the structure for reference
2. Can be used for local testing (users can modify values manually)

### Environment-Specific Parameter Files

Environment-specific parameter files allow you to override or add parameters per environment. They merge with the base `cloudformation-params.json`.

**How they work**:
- AWS Deployer loads `cloudformation-params.json` first
- Then merges `cloudformation-params.<env>.json` if it exists
- Environment-specific values override base values

**When to use them**:
- Different instance sizes per environment (t3.micro in dev, m5.large in prod)
- Feature flags (debug mode enabled only in dev)
- Environment-specific endpoints or domains
- Different scaling parameters

Create **`cloudformation-params.dev.json`**:
```json
{
}
```

Create **`cloudformation-params.prd.json`**:
```json
{
}
```

**Example with actual parameters**:

If your CloudFormation template has:
```yaml
Parameters:
  InstanceType:
    Type: String
    Default: t3.micro
  EnableDebugMode:
    Type: String
    Default: "false"
```

You might use:

`cloudformation-params.dev.json`:
```json
{
  "InstanceType": "t3.micro",
  "EnableDebugMode": "true"
}
```

`cloudformation-params.prd.json`:
```json
{
  "InstanceType": "m5.large",
  "EnableDebugMode": "false"
}
```

## Step 7: Explain GitHub OIDC Setup

After creating all files, explain to the user how to set up GitHub OIDC authentication and configure the required secrets. Make sure to clearly communicate that they need to:
1. Run the `aws-deployer setup-github` CLI command (you do NOT run it for them)
2. Manually add the `AWS_REGION` GitHub secret
3. Verify all three secrets are configured: `AWS_ROLE_ARN`, `S3_ARTIFACT_BUCKET`, `AWS_REGION`

Provide the following instructions:

---

## Next: Configure GitHub OIDC Authentication

Your repository is now configured for AWS Deployer! Before the GitHub Actions workflow can run, you need to set up GitHub OIDC authentication and configure GitHub secrets.

**Required GitHub Secrets:**
Your workflow requires THREE GitHub secrets to be configured:
1. **`AWS_ROLE_ARN`** - IAM role for GitHub OIDC authentication
2. **`S3_ARTIFACT_BUCKET`** - S3 bucket for storing deployment artifacts
3. **`AWS_REGION`** - AWS region where the deployer is running

### Step 1: Set Up GitHub OIDC with AWS

You need to run the `aws-deployer setup-github` CLI command to configure GitHub OIDC authentication.

**Prerequisites:**

1. **GitHub Personal Access Token (PAT)** stored in AWS Secrets Manager:

   ```bash
   # Create a PAT at https://github.com/settings/tokens with 'repo' scope
   # Then store it in Secrets Manager:
   aws secretsmanager create-secret \
     --name github/pat-token \
     --secret-string '{"github_pat":"ghp_xxxxxxxxxxxxx"}' \
     --region <region>
   ```

2. **AWS Deployer CLI** built and available:

   ```bash
   # Build the CLI if not already available
   cd /path/to/aws-deployer
   make build-cli
   ```

**Run the setup command:**

```bash
aws-deployer setup-github \
  --role-name github-actions-<short-repo-name> \
  --repo <repo-owner>/<repo-name> \
  --bucket <bucket-name> \
  --github-token-secret github/pat-token \
  --region <region>
```

**For your repository:**
```bash
aws-deployer setup-github \
  --role-name github-actions-<short-repo-name> \
  --repo <full-repo-name> \
  --bucket <bucket-name> \
  --github-token-secret github/pat-token \
  --region <region>
```

**What this command does:**
1. Creates GitHub OIDC provider in AWS (if it doesn't exist)
2. Creates IAM role `github-actions-<repo-name>` with S3 upload permissions
3. Adds `AWS_ROLE_ARN` secret to your GitHub repository
4. Adds `S3_ARTIFACT_BUCKET` secret to your GitHub repository

### Step 2: Add Required GitHub Secrets

After running the `aws-deployer setup-github` command, verify that these GitHub secrets exist. You may need to add `AWS_REGION` manually:

**Required secrets:**
- **`AWS_ROLE_ARN`** - Created by `aws-deployer setup-github` command
- **`S3_ARTIFACT_BUCKET`** - Created by `aws-deployer setup-github` command
- **`AWS_REGION`** - **Must be added manually**

**To add AWS_REGION manually:**

1. Go to `https://github.com/<owner>/<repo>/settings/secrets/actions`
2. Click "New repository secret"
3. Name: `AWS_REGION`
4. Value: `<region>` (e.g., `us-west-2`)
5. Click "Add secret"

**Verify all secrets exist:**

Go to `https://github.com/<owner>/<repo>/settings/secrets/actions` and confirm:
- ✓ `AWS_ROLE_ARN` - IAM role ARN for GitHub OIDC
- ✓ `S3_ARTIFACT_BUCKET` - S3 bucket name (e.g., `<bucket-name>`)
- ✓ `AWS_REGION` - AWS region (e.g., `<region>`)

### Step 3: Test the Workflow

Once all secrets are configured:

1. **Push a commit** or click "Run workflow" in the Actions tab
2. **Monitor the deployment** in GitHub Actions
3. **Check AWS Step Functions** for execution status

---

## Monitoring Deployments

After pushing code, monitor the deployment:

### GitHub Actions
- Check the Actions tab: `https://github.com/<owner>/<repo>/actions`
- Review workflow logs for any errors

### AWS Step Functions
```bash
# Get state machine ARN
STATE_MACHINE_ARN=$(aws ssm get-parameter \
  --name "/<env>/aws-deployer/state-machine-arn" \
  --query 'Parameter.Value' \
  --output text)

# List recent executions
aws stepfunctions list-executions \
  --state-machine-arn "${STATE_MACHINE_ARN}" \
  --max-results 10
```

### Lambda Logs
```bash
# S3 trigger logs
aws logs tail /aws/lambda/<env>-aws-deployer-s3-trigger --follow

# Build trigger logs
aws logs tail /aws/lambda/<env>-aws-deployer-trigger-build --follow
```

### DynamoDB Build Records
```bash
# Check build history
aws dynamodb query \
  --table-name <env>-aws-deployer--builds \
  --key-condition-expression "pk = :pk" \
  --expression-attribute-values '{":pk":{"S":"<repo-name>/dev"}}'
```

## Troubleshooting

### "Error: Could not assume role with OIDC"

**Cause**: GitHub OIDC not configured or secrets missing

**Fix**:
1. Run the `aws-deployer setup-github` command shown above
2. Verify all required secrets exist in GitHub repository settings:
   - `AWS_ROLE_ARN`
   - `S3_ARTIFACT_BUCKET`
   - `AWS_REGION`
3. Check IAM role trust policy allows your repository

```bash
aws iam get-role --role-name github-actions-<repo-name> \
  --query 'Role.AssumeRolePolicyDocument'
```

### "S3_ARTIFACT_BUCKET secret not found"

**Cause**: GitHub secret not configured

**Fix**: Run the `aws-deployer setup-github` command to create the secret, or manually add it:
1. Go to `https://github.com/<owner>/<repo>/settings/secrets/actions`
2. Click "New repository secret"
3. Name: `S3_ARTIFACT_BUCKET`
4. Value: Your S3 bucket name

### S3 Upload Succeeds but Deployment Doesn't Start

**Cause**: S3 trigger Lambda not configured or wrong S3 path

**Fix**:
```bash
# Check S3 files were uploaded
aws s3 ls s3://<bucket-name>/<repo-owner>/<repo-name>/ --recursive

# Check S3 trigger Lambda logs
aws logs tail /aws/lambda/<env>-aws-deployer-s3-trigger --since 10m
```

### CloudFormation Stack Fails

**Check stack events**:
```bash
# List stacks for this repo
aws cloudformation describe-stacks \
  --query 'Stacks[?contains(StackName, `<repo-name>`)].{Name:StackName, Status:StackStatus}'

# Get detailed errors
aws cloudformation describe-stack-events \
  --stack-name <env>-<repo-name> \
  --max-items 20
```

## Files Created

After running this skill, you should have:

- [ ] `.github/workflows/deploy.yml` - GitHub Actions workflow
- [ ] `cloudformation.template` - CloudFormation template with required parameters
- [ ] `cloudformation-params.json` - Base parameters template
- [ ] `cloudformation-params.dev.json` - Dev environment parameters (empty initially)
- [ ] `cloudformation-params.prd.json` - Production environment parameters (empty initially)

## Summary

This skill configured your repository for AWS Deployer by:

1. ✓ Detecting repository information from Git
2. ✓ Getting S3 bucket and AWS region (from environment variables or by asking)
3. ✓ Creating GitHub Actions workflow
4. ✓ Ensuring CloudFormation template has required parameters
5. ✓ Creating parameter files for local testing

**Next steps**:
1. Run `aws-deployer setup-github` command to configure GitHub OIDC
2. Add `AWS_REGION` GitHub secret manually
3. Verify all three secrets exist: `AWS_ROLE_ARN`, `S3_ARTIFACT_BUCKET`, `AWS_REGION`
4. Push a commit to trigger your first deployment
5. Add your infrastructure resources to `cloudformation.template`
6. Add environment-specific parameters if needed

For infrastructure setup, use the `setup-deployer` skill.
