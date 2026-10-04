---
name: aws-cognito
description: |
  Use when working with Aws Cognito — aWS Cognito user pool analysis, identity
  pool management, authentication flow analysis, and MFA status tracking. Covers
  user statistics, app client configuration, password policy review, Lambda
  trigger inspection, and federation setup.
connection_type: aws
preload: false
---

# AWS Cognito Skill

Analyze AWS Cognito user and identity pools with parallel execution and anti-hallucination guardrails.

**Relationship to other AWS skills:**

- `aws-cognito/` → Cognito-specific analysis (user pools, identity pools, auth flows)
- `aws/` → "How to execute" (parallel patterns, throttling, output format)

## CRITICAL: Parallel Execution Requirement

**ALL independent operations MUST run in parallel using background jobs (&) and wait.**

```bash
#!/bin/bash
export AWS_PAGER=""

for pool_id in $pools; do
  describe_user_pool "$pool_id" &
done
wait
```

## Helper Functions

```bash
#!/bin/bash
export AWS_PAGER=""

# List user pools
list_user_pools() {
  aws cognito-idp list-user-pools --max-results 60 \
    --output text \
    --query 'UserPools[].[Id,Name,Status,CreationDate,LastModifiedDate]'
}

# Get user pool details
describe_user_pool() {
  local pool_id=$1
  aws cognito-idp describe-user-pool --user-pool-id "$pool_id" \
    --output text \
    --query 'UserPool.[Id,Name,Status,EstimatedNumberOfUsers,MfaConfiguration,Policies.PasswordPolicy.[MinimumLength,RequireUppercase,RequireLowercase,RequireNumbers,RequireSymbols]]'
}

# List app clients for a user pool
list_app_clients() {
  local pool_id=$1
  aws cognito-idp list-user-pool-clients --user-pool-id "$pool_id" \
    --output text \
    --query 'UserPoolClients[].[ClientId,ClientName]'
}

# Get app client details
describe_app_client() {
  local pool_id=$1 client_id=$2
  aws cognito-idp describe-user-pool-client --user-pool-id "$pool_id" --client-id "$client_id" \
    --output text \
    --query 'UserPoolClient.[ClientName,ExplicitAuthFlows,AllowedOAuthFlows,AllowedOAuthScopes,SupportedIdentityProviders]'
}

# List identity pools
list_identity_pools() {
  aws cognito-identity list-identity-pools --max-results 60 \
    --output text \
    --query 'IdentityPools[].[IdentityPoolId,IdentityPoolName]'
}

# Get identity pool details
describe_identity_pool() {
  local pool_id=$1
  aws cognito-identity describe-identity-pool --identity-pool-id "$pool_id" \
    --output text \
    --query '[IdentityPoolId,IdentityPoolName,AllowUnauthenticatedIdentities,CognitoIdentityProviders[0].ProviderName]'
}
```

## Common Operations

### 1. User Pool Inventory with Security Posture

```bash
#!/bin/bash
export AWS_PAGER=""
POOLS=$(aws cognito-idp list-user-pools --max-results 60 --output text --query 'UserPools[].Id')
for pool in $POOLS; do
  aws cognito-idp describe-user-pool --user-pool-id "$pool" \
    --output text \
    --query 'UserPool.[Id,Name,EstimatedNumberOfUsers,MfaConfiguration,Policies.PasswordPolicy.MinimumLength,AccountRecoverySetting.RecoveryMechanisms[0].Name]' &
done
wait
```

### 2. MFA Configuration Analysis

```bash
#!/bin/bash
export AWS_PAGER=""
POOLS=$(aws cognito-idp list-user-pools --max-results 60 --output text --query 'UserPools[].Id')
for pool in $POOLS; do
  {
    mfa=$(aws cognito-idp describe-user-pool --user-pool-id "$pool" \
      --output text \
      --query 'UserPool.[Name,MfaConfiguration]')
    printf "%s\tMFA:%s\n" "$pool" "$mfa"
  } &
done
wait
```

### 3. Auth Flow and App Client Audit

```bash
#!/bin/bash
export AWS_PAGER=""
POOL_ID=$1
CLIENTS=$(aws cognito-idp list-user-pool-clients --user-pool-id "$POOL_ID" \
  --output text --query 'UserPoolClients[].ClientId')
for client in $CLIENTS; do
  aws cognito-idp describe-user-pool-client --user-pool-id "$POOL_ID" --client-id "$client" \
    --output text \
    --query 'UserPoolClient.[ClientName,ExplicitAuthFlows[],AllowedOAuthFlows[],TokenValidityUnits.AccessToken]' &
done
wait
```

### 4. Lambda Trigger Configuration

```bash
#!/bin/bash
export AWS_PAGER=""
POOLS=$(aws cognito-idp list-user-pools --max-results 60 --output text --query 'UserPools[].Id')
for pool in $POOLS; do
  aws cognito-idp describe-user-pool --user-pool-id "$pool" \
    --output text \
    --query 'UserPool.[Name,LambdaConfig.[PreSignUp,PostConfirmation,PreAuthentication,PostAuthentication,CustomMessage,DefineAuthChallenge]]' &
done
wait
```

### 5. Identity Pool Federation Analysis

```bash
#!/bin/bash
export AWS_PAGER=""
ID_POOLS=$(aws cognito-identity list-identity-pools --max-results 60 --output text --query 'IdentityPools[].IdentityPoolId')
for pool in $ID_POOLS; do
  aws cognito-identity describe-identity-pool --identity-pool-id "$pool" \
    --output text \
    --query '[IdentityPoolName,AllowUnauthenticatedIdentities,CognitoIdentityProviders[].ProviderName,SupportedLoginProviders]' &
done
wait
```

## Anti-Hallucination Rules

1. **User Pool vs Identity Pool** - User Pools handle authentication (sign-up/sign-in). Identity Pools handle authorization (AWS credentials). They are separate resources.
2. **EstimatedNumberOfUsers is approximate** - This is an estimate, not an exact count. For precise counts, use `list-users` with pagination (expensive for large pools).
3. **MFA values** - Valid MfaConfiguration values: OFF, ON, OPTIONAL. "ON" means required for all users. "OPTIONAL" means per-user choice.
4. **Auth flow names** - Valid ExplicitAuthFlows: ALLOW_USER_PASSWORD_AUTH, ALLOW_USER_SRP_AUTH, ALLOW_REFRESH_TOKEN_AUTH, ALLOW_CUSTOM_AUTH, ALLOW_ADMIN_USER_PASSWORD_AUTH. Do not invent others.
5. **Client secret** - Some app clients have secrets, some do not. Public clients (SPAs, mobile) should NOT have secrets.

## Output Format

Present results as a structured report:
```
Aws Cognito Report
══════════════════
Resources discovered: [count]

Resource       Status    Key Metric    Issues
──────────────────────────────────────────────
[name]         [ok/warn] [value]       [findings]

Summary: [total] resources | [ok] healthy | [warn] warnings | [crit] critical
Action Items: [list of prioritized findings]
```

Target ≤50 lines of output. Use tables for multi-resource comparisons.

## Counter-Rationalizations

| Shortcut | Counter | Why |
|----------|---------|-----|
| "I'll skip discovery and check known resources" | Always run Phase 1 discovery first | Resource names change, new resources appear — assumed names cause errors |
| "The user only asked for a quick check" | Follow the full discovery → analysis flow | Quick checks miss critical issues; structured analysis catches silent failures |
| "Default configuration is probably fine" | Audit configuration explicitly | Defaults often leave logging, security, and optimization features disabled |
| "Metrics aren't needed for this" | Always check relevant metrics when available | API/CLI responses show current state; metrics reveal trends and intermittent issues |
| "I don't have access to that" | Try the command and report the actual error | Assumed permission failures prevent useful investigation; actual errors are informative |

## Common Pitfalls

- **list-users rate limit**: `list-users` has aggressive throttling (5 requests/second). Use sparingly with `--limit` and `--pagination-token`.
- **Regional service**: Cognito is regional. User pools in us-east-1 are not visible in eu-west-1.
- **Custom domains**: Cognito custom domains require ACM certificates in us-east-1 (same as CloudFront).
- **CloudWatch statistics syntax**: Use spaces not commas: `--statistics Average Maximum`.
- **Token validity**: Default access token validity is 60 minutes. Refresh token validity defaults to 30 days. Check `TokenValidityUnits` for actual units.
