---
name: credential-activation
description: Configure environment credentials for skills that require API keys or secrets. Use when a skill reports missing credentials, or when setting up a new space that will use authenticated services (Mailgun, OpenAI, external APIs).
version: 1.0.0
allowed-tools: Bash, Read, Write
metadata:
  context: TeamDay space environment
---

# Credential Activation Skill

Configure credentials for skills that require API keys, tokens, or secrets.

## Overview

Many skills require external API credentials to function:
- **notify-user**: Mailgun API key and domain
- **Custom integrations**: OpenAI, Anthropic, Stripe, etc.

This skill helps you:
1. **Identify** which credentials a skill needs
2. **Check** if credentials are already configured
3. **Guide users** through the setup process
4. **Verify** credentials are working

## How Credentials Work in TeamDay

```
┌─────────────────────────────────────────────────────────┐
│  TeamDay UI (Space Settings > Secrets)                  │
│  User adds: MAILGUN_API_KEY = "key-abc123..."          │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│  Firestore (spaces/{spaceId}/secrets)                   │
│  Encrypted storage                                       │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│  Agent Execution (computer service)                     │
│  Secrets injected as environment variables              │
│  process.env.MAILGUN_API_KEY = "key-abc123..."         │
└─────────────────────────────────────────────────────────┘
```

**Key Points:**
- Credentials are stored securely in Firestore (not in files)
- Injected as environment variables during agent execution
- Available to scheduled jobs via the same mechanism
- Never stored in plaintext in the space directory

## Check Credential Status

Before using a skill that requires credentials, check if they're available:

```bash
# Generic check for any credential
check_credential() {
  local var_name=$1
  if [ -n "${!var_name}" ]; then
    echo "✅ $var_name: configured"
    return 0
  else
    echo "❌ $var_name: not configured"
    return 1
  fi
}

# Check multiple credentials
check_credential "MAILGUN_API_KEY"
check_credential "MAILGUN_DOMAIN"
check_credential "NOTIFICATION_EMAIL"
```

## Credential Requirements by Skill

### notify-user (Mailgun)

| Variable | Required | Description |
|----------|----------|-------------|
| `MAILGUN_API_KEY` | Yes | Private API key from Mailgun dashboard |
| `MAILGUN_DOMAIN` | Yes | Verified sending domain |
| `MAILGUN_REGION` | No | `US` (default) or `EU` |
| `MAILGUN_FROM_EMAIL` | No | Sender address (defaults to agent@domain) |
| `NOTIFICATION_EMAIL` | Yes | Default recipient email |

**Setup Instructions for User:**

```
To configure Mailgun for email notifications:

1. Sign up at https://www.mailgun.com/ (free tier available)

2. Get your API key:
   - Go to Settings > API Keys
   - Copy your "Private API key"

3. Set up a domain (or use sandbox for testing):
   - Go to Sending > Domains
   - Add and verify your domain (follow DNS instructions)
   - Or use the provided sandbox domain for testing

4. In TeamDay:
   - Open your Space settings
   - Go to "Secrets" tab
   - Add the following secrets:

     MAILGUN_API_KEY: your-private-api-key
     MAILGUN_DOMAIN: mg.yourdomain.com
     MAILGUN_REGION: US (or EU if using EU region)
     NOTIFICATION_EMAIL: your-email@example.com

5. For sandbox domains only:
   - Go to Mailgun > Sending > Overview
   - Add your email to "Authorized Recipients"
   - Click the verification link in your email
```

### Custom OpenAI Integration

| Variable | Required | Description |
|----------|----------|-------------|
| `OPENAI_API_KEY` | Yes | OpenAI API key |
| `OPENAI_ORG_ID` | No | Organization ID (if applicable) |

**Setup Instructions:**

```
To configure OpenAI API access:

1. Get your API key:
   - Go to https://platform.openai.com/api-keys
   - Create a new API key

2. In TeamDay:
   - Open your Space settings
   - Go to "Secrets" tab
   - Add:

     OPENAI_API_KEY: sk-...your-key...
```

### Custom Anthropic Integration

| Variable | Required | Description |
|----------|----------|-------------|
| `ANTHROPIC_API_KEY` | Yes | Anthropic API key |

**Setup Instructions:**

```
To configure Anthropic API access:

1. Get your API key:
   - Go to https://console.anthropic.com/
   - Navigate to API Keys
   - Create a new key

2. In TeamDay:
   - Open your Space settings
   - Go to "Secrets" tab
   - Add:

     ANTHROPIC_API_KEY: sk-ant-...your-key...
```

## Activation Workflow

When a skill reports missing credentials, follow this workflow:

### Step 1: Identify Required Credentials

```bash
# Check skill's SKILL.md for credential requirements
# Look for the metadata.credentials section
```

### Step 2: Check Current Status

```bash
# Create a credential check script
check_all_credentials() {
  echo "=== Credential Status ==="
  echo ""

  # Mailgun
  echo "📧 Mailgun (notify-user skill):"
  [ -n "$MAILGUN_API_KEY" ] && echo "  ✅ MAILGUN_API_KEY" || echo "  ❌ MAILGUN_API_KEY"
  [ -n "$MAILGUN_DOMAIN" ] && echo "  ✅ MAILGUN_DOMAIN" || echo "  ❌ MAILGUN_DOMAIN"
  [ -n "$NOTIFICATION_EMAIL" ] && echo "  ✅ NOTIFICATION_EMAIL" || echo "  ❌ NOTIFICATION_EMAIL"
  echo ""

  # OpenAI
  echo "🤖 OpenAI:"
  [ -n "$OPENAI_API_KEY" ] && echo "  ✅ OPENAI_API_KEY" || echo "  ❌ OPENAI_API_KEY"
  echo ""

  # Anthropic
  echo "🧠 Anthropic:"
  [ -n "$ANTHROPIC_API_KEY" ] && echo "  ✅ ANTHROPIC_API_KEY" || echo "  ❌ ANTHROPIC_API_KEY"
}

check_all_credentials
```

### Step 3: Guide User Through Setup

If credentials are missing, provide clear instructions:

```
🔐 Credential Setup Required

The [skill-name] skill requires the following credentials that are not yet configured:

Missing credentials:
- MAILGUN_API_KEY
- MAILGUN_DOMAIN

To configure these credentials:

1. Open TeamDay in your browser
2. Navigate to this space's settings
3. Click on the "Secrets" tab
4. Add the following secrets:

   MAILGUN_API_KEY: [your Mailgun private API key]
   MAILGUN_DOMAIN: [your verified sending domain]

Need help getting these values? Here's how:
[Include service-specific instructions]

Once configured, restart the agent session to pick up the new credentials.
```

### Step 4: Verify Credentials Work

After user configures credentials, verify they work:

```bash
# Mailgun verification
verify_mailgun() {
  if [ -z "$MAILGUN_API_KEY" ] || [ -z "$MAILGUN_DOMAIN" ]; then
    echo "❌ Mailgun credentials not configured"
    return 1
  fi

  # Determine API endpoint
  if [ "$MAILGUN_REGION" = "EU" ]; then
    API="https://api.eu.mailgun.net"
  else
    API="https://api.mailgun.net"
  fi

  # Test API access (list domains)
  RESPONSE=$(curl -s -w "%{http_code}" -o /tmp/mailgun_test.json \
    --user "api:${MAILGUN_API_KEY}" \
    "${API}/v3/domains")

  if [ "$RESPONSE" = "200" ]; then
    echo "✅ Mailgun credentials verified successfully"
    return 0
  else
    echo "❌ Mailgun credential verification failed (HTTP $RESPONSE)"
    cat /tmp/mailgun_test.json
    return 1
  fi
}

verify_mailgun
```

## Creating Credential Documentation

When creating a new skill that requires credentials, document them in the SKILL.md frontmatter:

```yaml
---
name: my-new-skill
description: ...
metadata:
  requires: credential-activation
  credentials:
    - MY_API_KEY
    - MY_SECRET_TOKEN
---
```

And include a "Prerequisites" section in the skill:

```markdown
## Prerequisites

This skill requires the following credentials:

| Variable | Required | Description |
|----------|----------|-------------|
| `MY_API_KEY` | Yes | API key from service dashboard |
| `MY_SECRET_TOKEN` | No | Optional secret for advanced features |

If credentials are not configured, use the `credential-activation` skill to set them up.
```

## Security Best Practices

1. **Never log credentials** - Don't echo or print API keys
2. **Never store in files** - Use TeamDay's secure storage
3. **Use environment variables** - Always access via `$VAR_NAME`
4. **Rotate regularly** - Update keys periodically
5. **Minimum permissions** - Request only needed API scopes

## Scheduled Jobs and Credentials

Credentials configured in TeamDay are automatically available to scheduled jobs:

```
Interactive Session    →    Credentials injected from Firestore
Scheduled Job         →    Same credentials injected automatically
```

No additional setup is needed for scheduled jobs to access credentials that are configured for the space.

## Troubleshooting

### Credentials configured but not available?

1. **Session needs restart**: New credentials are loaded at session start
2. **Wrong space**: Credentials are space-specific
3. **Typo in variable name**: Check exact spelling in TeamDay UI

### Credential verification failing?

1. **Invalid key**: Double-check the key value in service dashboard
2. **Expired key**: Generate a new key
3. **Wrong region**: Some services have regional endpoints
4. **Rate limited**: Wait and retry

### Scheduled job can't access credentials?

1. **Credentials set after job creation**: Re-save the scheduled job
2. **Organization-level vs space-level**: Some credentials may be at org level
3. **Check scheduler logs**: Look for authentication errors
