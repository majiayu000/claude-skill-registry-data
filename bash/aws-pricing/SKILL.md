---
name: aws-pricing
description: |
  Use when working with Aws Pricing — aWS pricing helper for cost queries.
  ALWAYS use get_aws_cost script for pricing questions. Use when: - User asks
  about AWS resource costs or pricing - User wants to compare pricing across
  regions - User needs spot, on-demand, or reserved pricing info Triggers: aws
  pricing, aws cost, how much does, ec2 price, rds cost, s3 pricing.
connection_type: aws
preload: false
---

# AWS Pricing Helper

**MANDATORY RULE**: Always answer pricing questions with the `get_aws_cost` helper. NEVER call external search tools or guess prices.

The helper script `get_pricing_aws.sh` lives in the sandbox skills directory.
**You must source it before use:**

```bash
source ./_skills/connections/aws/aws-pricing/scripts/get_pricing_aws.sh
```

Run `get_aws_cost` without stderr redirection or grep filtering so the agent receives the raw response.
If multiple pricing lookups are required, place every call in a single Bash script (one script per task).

## Usage

```bash
source ./_skills/connections/aws/aws-pricing/scripts/get_pricing_aws.sh
get_aws_cost <resource> <region> [options]
```

## Supported Resources

| Category | Resources |
|----------|-----------|
| EC2 | t3.micro, m5.large, g4dn.xlarge, c6i.large |
| RDS | db.t3.micro, db.r5.large |
| ElastiCache | cache.t3.micro, cache.r5.large |
| S3 | s3-standard, s3-ia, s3-glacier, s3-glacier-deep |
| Lambda | lambda-128mb, lambda-1gb, lambda-3gb |
| DynamoDB | dynamodb-ondemand, dynamodb-provisioned |
| EFS | efs-standard, efs-ia |
| EBS | gp3-100gb, io2-500gb, st1-1tb |
| CloudFront | cloudfront-standard |
| API Gateway | apigateway-rest, apigateway-http |
| SQS | sqs-standard, sqs-fifo |
| SNS | sns-standard |
| Route53 | route53-hosted-zone, route53-query |
| ALB | alb-standard |
| NAT Gateway | natgw-standard |
| VPC Endpoints | vpce-gateway, vpce-interface |

## Parameters

- `resource`: Auto-detected from the naming pattern above
- `region`: AWS location string (e.g., "Asia Pacific (Singapore)", "US East (N. Virginia)")
- `options`: `--spot` (include spot pricing), `--detailed` (verbose output), `--no-reserved` (skip reserved pricing)

## Examples

```bash
get_aws_cost t3.micro "US East (N. Virginia)" --spot
get_aws_cost db.t3.micro "Asia Pacific (Singapore)"
get_aws_cost s3-standard "US East (N. Virginia)"
get_aws_cost lambda-1gb "US East (N. Virginia)"
get_aws_cost cloudfront-standard "US East (N. Virginia)"
get_aws_cost apigateway-rest "US East (N. Virginia)"
get_aws_cost sqs-standard "US East (N. Virginia)"
```

## Output

Human-readable pricing data with service details, region, specs, on-demand, reserved, and spot pricing where available.
If a resource is unsupported, the helper prints guidance for querying the AWS Pricing API manually.

## Output Format

Present results as a structured report:
```
Aws Pricing Report
══════════════════
Resources discovered: [count]

Resource       Status    Key Metric    Issues
──────────────────────────────────────────────
[name]         [ok/warn] [value]       [findings]

Summary: [total] resources | [ok] healthy | [warn] warnings | [crit] critical
Action Items: [list of prioritized findings]
```

Target ≤50 lines of output. Use tables for multi-resource comparisons.

## Anti-Hallucination Rules

1. **NEVER assume resource names** — always discover via CLI/API in Phase 1 before referencing in Phase 2.
2. **NEVER fabricate metric names or dimensions** — verify against the service documentation or `--help` output.
3. **NEVER mix CLI commands between service versions** — confirm which version/API you are targeting.
4. **ALWAYS use the discovery → verify → analyze chain** — every resource referenced must have been discovered first.
5. **ALWAYS handle empty results gracefully** — an empty response is valid data, not an error to retry.

## Counter-Rationalizations

| Shortcut | Counter | Why |
|----------|---------|-----|
| "I'll skip discovery and check known resources" | Always run Phase 1 discovery first | Resource names change, new resources appear — assumed names cause errors |
| "The user only asked for a quick check" | Follow the full discovery → analysis flow | Quick checks miss critical issues; structured analysis catches silent failures |
| "Default configuration is probably fine" | Audit configuration explicitly | Defaults often leave logging, security, and optimization features disabled |
| "Metrics aren't needed for this" | Always check relevant metrics when available | API/CLI responses show current state; metrics reveal trends and intermittent issues |
| "I don't have access to that" | Try the command and report the actual error | Assumed permission failures prevent useful investigation; actual errors are informative |

