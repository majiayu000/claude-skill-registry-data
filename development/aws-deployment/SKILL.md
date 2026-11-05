---
name: aws-deployment
description: Deep knowledge about deploying applications to AWS (EC2, ECS, S3, CloudFront, Cloud Run).
type: transform
tier: library
domain: deploy
trigger: "when deploying to AWS"
---

## Context
Deploying {{project_name}} ({{project_type}}) to Amazon Web Services (AWS).
You will follow a strict 6-phase Deployment Lifecycle Contract. 

## Instructions

Execute the following phases in order:

### Phase 1: Authentication
1. Verify the presence of AWS credentials (`AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`, or `AWS_PROFILE`).
2. Run `aws sts get-caller-identity` to confirm authentication.
3. If using an IAM role (e.g., in GitHub Actions via OIDC), ensure the role is successfully assumed.

### Phase 2: Build
1. Prepare the artifacts for deployment.
2. If containerized (ECS, AppRunner, EKS): run `docker build -t <image-name> .`
3. If static site (S3/CloudFront): run your framework's build command (e.g., `npm run build`).
4. If Node.js/Python on EC2: bundle the application code.

### Phase 3: Install / Provisioning
1. Ensure the target AWS resources exist.
2. If using S3: run `aws s3 ls s3://<bucket-name>` to verify bucket presence. Create it if it doesn't exist.
3. If using ECR: authenticate Docker to ECR (`aws ecr get-login-password --region <region> | docker login --username AWS --password-stdin <account-id>.dkr.ecr.<region>.amazonaws.com`).
4. If using EC2: ensure you have the correct key pairs or Session Manager access.

### Phase 4: Deploy
1. Ship the artifact to AWS.
2. S3/CloudFront: `aws s3 sync dist/ s3://<bucket-name> --delete`. Then invalidate cache: `aws cloudfront create-invalidation --distribution-id <id> --paths "/*"`.
3. ECS: Push image to ECR, then update the ECS service (`aws ecs update-service --cluster <cluster> --service <service> --force-new-deployment`).
4. EC2 (File-based): Use `scp` to copy files, SSH in, install dependencies, and restart PM2/Systemd.

### Phase 5: Checking
1. Verify the deployment was successful.
2. Curl the application's public URL or load balancer to check for an HTTP 200 OK status.
3. Check AWS logs via CloudWatch (`aws logs tail ...`) if you encounter errors.
4. For ECS, check `aws ecs describe-services` to ensure running count matches desired count.

### Phase 6: Update / Rollback
1. If Phase 5 fails, immediately initiate a rollback.
2. S3/CloudFront: Restore previous files (requires versioning enabled on S3) or sync from a previous build artifact.
3. ECS: Update the service to use the previous task definition revision.
4. Note the failure in the progress log.

## Validation
- [ ] AWS authentication succeeds.
- [ ] Build succeeds.
- [ ] Artifacts are transferred.
- [ ] Health check (curl) returns 200 OK.
