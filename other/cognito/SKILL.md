---
type: skill
name: cognito
description: AWS Cognito user authentication and authorization service. Use when setting up user pools, configuring identity pools, implementing OAuth flows, managing user attributes, or integrating with social identity providers.
last_updated: "2026-01-07"
doc_source: https://docs.aws.amazon.com/cognito/latest/developerguide/
---

# AWS Cognito

Amazon Cognito provides authentication, authorization, and user management for web and mobile applications. Users can sign in directly or through federated identity providers.

## Table of Contents

- [Core Concepts](#core-concepts)
- [Common Patterns](#common-patterns)
- [CLI Reference](#cli-reference)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)
- [Security Checks](#security-checks)
- [External Accessibility Probe](#external-accessibility-probe)
- [References](#references)

## Core Concepts

### User Pools

User directory for sign-up and sign-in. Provides:
- User registration and authentication
- OAuth 2.0 / OpenID Connect tokens
- MFA and password policies
- Customizable UI and flows

### Identity Pools (Federated Identities)

Provide temporary AWS credentials to access AWS services. Users can be:
- Cognito User Pool users
- Social identity (Google, Facebook, Apple)
- SAML/OIDC enterprise identity
- Anonymous guests

### Tokens

| Token | Purpose | Lifetime |
|-------|---------|----------|
| **ID Token** | User identity claims | 1 hour |
| **Access Token** | API authorization | 1 hour |
| **Refresh Token** | Get new ID/Access tokens | 30 days (configurable) |

## Common Patterns

### Create User Pool

**AWS CLI:**

```bash
aws cognito-idp create-user-pool \
  --pool-name my-app-users \
  --policies '{
    "PasswordPolicy": {
      "MinimumLength": 12,
      "RequireUppercase": true,
      "RequireLowercase": true,
      "RequireNumbers": true,
      "RequireSymbols": true
    }
  }' \
  --auto-verified-attributes email \
  --username-attributes email \
  --mfa-configuration OPTIONAL \
  --user-attribute-update-settings '{
    "AttributesRequireVerificationBeforeUpdate": ["email"]
  }'
```

### Create App Client

```bash
aws cognito-idp create-user-pool-client \
  --user-pool-id us-east-1_abc123 \
  --client-name my-web-app \
  --generate-secret \
  --explicit-auth-flows ALLOW_USER_SRP_AUTH ALLOW_REFRESH_TOKEN_AUTH \
  --supported-identity-providers COGNITO \
  --callback-urls https://myapp.com/callback \
  --logout-urls https://myapp.com/logout \
  --allowed-o-auth-flows code \
  --allowed-o-auth-scopes openid email profile \
  --allowed-o-auth-flows-user-pool-client \
  --access-token-validity 60 \
  --id-token-validity 60 \
  --refresh-token-validity 30 \
  --token-validity-units '{
    "AccessToken": "minutes",
    "IdToken": "minutes",
    "RefreshToken": "days"
  }'
```

### Sign Up User

```python
import boto3
import hmac
import hashlib
import base64

cognito = boto3.client('cognito-idp')

def get_secret_hash(username, client_id, client_secret):
    message = username + client_id
    dig = hmac.new(
        client_secret.encode('utf-8'),
        message.encode('utf-8'),
        digestmod=hashlib.sha256
    ).digest()
    return base64.b64encode(dig).decode()

response = cognito.sign_up(
    ClientId='client-id',
    SecretHash=get_secret_hash('user@example.com', 'client-id', 'client-secret'),
    Username='user@example.com',
    Password='SecurePassword123!',
    UserAttributes=[
        {'Name': 'email', 'Value': 'user@example.com'},
        {'Name': 'name', 'Value': 'John Doe'}
    ]
)
```

### Confirm Sign Up

```python
cognito.confirm_sign_up(
    ClientId='client-id',
    SecretHash=get_secret_hash('user@example.com', 'client-id', 'client-secret'),
    Username='user@example.com',
    ConfirmationCode='123456'
)
```

### Authenticate User

```python
response = cognito.initiate_auth(
    ClientId='client-id',
    AuthFlow='USER_SRP_AUTH',
    AuthParameters={
        'USERNAME': 'user@example.com',
        'SECRET_HASH': get_secret_hash('user@example.com', 'client-id', 'client-secret'),
        'SRP_A': srp_a  # From SRP library
    }
)

# For simple password auth (not recommended for production)
response = cognito.admin_initiate_auth(
    UserPoolId='us-east-1_abc123',
    ClientId='client-id',
    AuthFlow='ADMIN_USER_PASSWORD_AUTH',
    AuthParameters={
        'USERNAME': 'user@example.com',
        'PASSWORD': 'password',
        'SECRET_HASH': get_secret_hash('user@example.com', 'client-id', 'client-secret')
    }
)

tokens = response['AuthenticationResult']
id_token = tokens['IdToken']
access_token = tokens['AccessToken']
refresh_token = tokens['RefreshToken']
```

### Refresh Tokens

```python
response = cognito.initiate_auth(
    ClientId='client-id',
    AuthFlow='REFRESH_TOKEN_AUTH',
    AuthParameters={
        'REFRESH_TOKEN': refresh_token,
        'SECRET_HASH': get_secret_hash('user@example.com', 'client-id', 'client-secret')
    }
)
```

### Create Identity Pool

```bash
aws cognito-identity create-identity-pool \
  --identity-pool-name my-app-identities \
  --allow-unauthenticated-identities \
  --cognito-identity-providers \
    ProviderName=cognito-idp.us-east-1.amazonaws.com/us-east-1_abc123,\
ClientId=client-id,\
ServerSideTokenCheck=true
```

### Get AWS Credentials

```python
import boto3

cognito_identity = boto3.client('cognito-identity')

# Get identity ID
response = cognito_identity.get_id(
    IdentityPoolId='us-east-1:12345678-1234-1234-1234-123456789012',
    Logins={
        'cognito-idp.us-east-1.amazonaws.com/us-east-1_abc123': id_token
    }
)
identity_id = response['IdentityId']

# Get credentials
response = cognito_identity.get_credentials_for_identity(
    IdentityId=identity_id,
    Logins={
        'cognito-idp.us-east-1.amazonaws.com/us-east-1_abc123': id_token
    }
)

credentials = response['Credentials']
# Use credentials['AccessKeyId'], credentials['SecretKey'], credentials['SessionToken']
```

## CLI Reference

### User Pool

| Command | Description |
|---------|-------------|
| `aws cognito-idp create-user-pool` | Create user pool |
| `aws cognito-idp describe-user-pool` | Get pool details |
| `aws cognito-idp update-user-pool` | Update pool settings |
| `aws cognito-idp delete-user-pool` | Delete pool |
| `aws cognito-idp list-user-pools` | List pools |

### Users

| Command | Description |
|---------|-------------|
| `aws cognito-idp admin-create-user` | Create user (admin) |
| `aws cognito-idp admin-delete-user` | Delete user |
| `aws cognito-idp admin-get-user` | Get user details |
| `aws cognito-idp list-users` | List users |
| `aws cognito-idp admin-set-user-password` | Set password |
| `aws cognito-idp admin-disable-user` | Disable user |

### Authentication

| Command | Description |
|---------|-------------|
| `aws cognito-idp initiate-auth` | Start authentication |
| `aws cognito-idp respond-to-auth-challenge` | Respond to MFA |
| `aws cognito-idp admin-initiate-auth` | Admin authentication |

## Best Practices

### Security

- **Enable MFA** for all users (at least optional)
- **Use strong password policies**
- **Enable advanced security features** (adaptive auth)
- **Verify email/phone** before allowing sign-in
- **Use short token lifetimes** for sensitive apps
- **Never expose client secrets** in frontend code

### User Experience

- **Use hosted UI** for quick implementation
- **Customize UI** with CSS
- **Implement proper error handling**
- **Provide clear password requirements**

### Architecture

- **Use identity pools** for AWS resource access
- **Use access tokens** for API Gateway
- **Store refresh tokens securely**
- **Implement token refresh** before expiry

## Troubleshooting

### User Cannot Sign In

**Causes:**
- User not confirmed
- Password incorrect
- User disabled
- Account locked (too many attempts)

**Debug:**

```bash
aws cognito-idp admin-get-user \
  --user-pool-id us-east-1_abc123 \
  --username user@example.com
```

### Token Validation Failed

**Causes:**
- Token expired
- Wrong user pool/client ID
- Token signature invalid

**Validate JWT:**

```python
import jwt
import requests

# Get JWKS
jwks_url = f'https://cognito-idp.us-east-1.amazonaws.com/us-east-1_abc123/.well-known/jwks.json'
jwks = requests.get(jwks_url).json()

# Decode and verify (use python-jose or similar)
from jose import jwt

claims = jwt.decode(
    token,
    jwks,
    algorithms=['RS256'],
    audience='client-id',
    issuer='https://cognito-idp.us-east-1.amazonaws.com/us-east-1_abc123'
)
```

### Hosted UI Not Working

**Check:**
- Callback URLs configured correctly
- Domain configured for user pool
- OAuth settings enabled

```bash
# Check domain
aws cognito-idp describe-user-pool \
  --user-pool-id us-east-1_abc123 \
  --query 'UserPool.Domain'
```

### Rate Limiting

**Symptom:** `TooManyRequestsException`

**Solutions:**
- Implement exponential backoff
- Request quota increase
- Cache tokens appropriately

## Security Checks

Key security controls to validate for Cognito User Pools:

| Check | CLI | Confirmed (Issue) | False Positive |
|:------|:----|:------------------|:---------------|
| Advanced security features | `aws cognito-idp describe-user-pool --user-pool-id {{id}} --query 'UserPool.UserPoolAddOns'` | `AdvancedSecurityMode = OFF` | `AdvancedSecurityMode = ENFORCED` |
| MFA enforced | `aws cognito-idp describe-user-pool --user-pool-id {{id}} --query 'UserPool.MfaConfiguration'` | `MfaConfiguration = OFF` | `MfaConfiguration = ON or OPTIONAL` |
| Password policy strength | `aws cognito-idp describe-user-pool --user-pool-id {{id}} --query 'UserPool.Policies.PasswordPolicy'` | `MinimumLength < 8` or `RequireNumbers/Symbols = false` | Strong policy configured |
| App client secret | `aws cognito-idp list-user-pool-clients --user-pool-id {{id}}` then `aws cognito-idp describe-user-pool-client --user-pool-id {{id}} --client-id {{client_id}} --query 'UserPoolClient.ClientSecret'` | No secret (public client used for server-side flow) | Secret present |
| Token validity (refresh token) | `aws cognito-idp describe-user-pool-client --user-pool-id {{id}} --client-id {{client_id}} --query 'UserPoolClient.RefreshTokenValidity'` | `RefreshTokenValidity > 30` days | 30 days or less |

---

## External Accessibility Probe

Use when the question is "is this Cognito hosted UI publicly reachable?" Tests the hosted UI endpoint and validates TLS configuration.

**Step 1 — Discover hosted UI domain:**
```bash
aws cognito-idp describe-user-pool \
  --user-pool-id {{pool_id}} \
  --region {{region}} \
  --query 'UserPool.{Domain:Domain,CustomDomain:CustomDomain}' \
  --output json
```

If `Domain` is set → hosted UI is at `https://{{domain}}.auth.{{region}}.amazoncognito.com`
If `CustomDomain` is set → use that domain instead.
If both are null → no hosted UI configured, probe not applicable.

**Step 2 — Probe hosted UI endpoint:**
```bash
curl -sI --max-time 10 https://{{domain}}.auth.{{region}}.amazoncognito.com/login
```

| Response | Meaning |
|:---------|:--------|
| HTTP 200 or 302 | Hosted UI is publicly reachable — expected for Cognito |
| Connection refused / timeout | Hosted UI not responding — investigate |

Note: A reachable hosted UI is normal for Cognito. The finding is in the *configuration* (MFA, advanced security) not the reachability itself.

**Step 3 — TLS/SSL validation:**
```bash
testssl.sh {{domain}}.auth.{{region}}.amazoncognito.com
```

AWS manages TLS for Cognito hosted UI. Validate that deprecated protocols (TLS 1.0/1.1) are not negotiated. See `skills/testssl/SKILL.md` for interpretation.

**Scoring:** TLS issues on the hosted UI endpoint → Score 4-5 depending on severity. Configuration issues (MFA off, weak password policy) → Score 4 with CLI evidence. Hosted UI reachability alone → not a finding.

---

## References

- [Cognito Developer Guide](https://docs.aws.amazon.com/cognito/latest/developerguide/)
- [Cognito User Pools API](https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/)
- [Cognito Identity API](https://docs.aws.amazon.com/cognitoidentity/latest/APIReference/)
- [Cognito CLI Reference](https://docs.aws.amazon.com/cli/latest/reference/cognito-idp/)
