---
name: onboard-external-telemetry
description: Activate when users want to connect external data sources, cloud logs, SaaS applications, or third-party telemetry into LimaCharlie. Guides beginners through identifying requirements, obtaining credentials, and configuring adapters.
---

# External Telemetry Onboarding

I'll help you connect an external data source to LimaCharlie. We'll go through this step by step together - I'll ask you questions and guide you through exactly what to do at each stage.

Let's get started!

---

## How to Use This Skill (Instructions for Claude)

**CRITICAL**: This skill is designed to be **incremental and conversational**. You must:
- ✅ Ask ONE question at a time
- ✅ WAIT for the user to respond before continuing
- ✅ Provide ONLY information relevant to their current step
- ✅ Confirm completion of each step before moving to the next
- ✅ Link to detailed docs rather than showing everything upfront

**DO NOT**:
- ❌ Show all steps upfront
- ❌ Provide comprehensive reference tables unless asked
- ❌ Explain all concepts before starting
- ❌ Continue without user confirmation

---

## Conversation Flow Guide

### Step 1: Identify Data Source Category

**ASK**: "What type of data source are you connecting?"

**OPTIONS**:
1. Cloud provider (AWS, Azure, Google Cloud)
2. SaaS application (Microsoft 365, Okta, Slack, etc.)
3. Security tool (CrowdStrike, firewall, EDR)
4. Network device (firewall via Syslog, router logs)
5. Something else / Not sure

**WAIT for user response. DO NOT continue until they answer.**

---

### Step 2: Get Specific Source (Conditional on Step 1)

#### If User Selected: Cloud Provider

**ASK**: "Which cloud provider?"
- AWS
- Microsoft Azure
- Google Cloud Platform

**WAIT for response.**

**Then ASK**:
- If AWS: "Which AWS service? CloudTrail, GuardDuty, or something else?"
- If Azure: "What Azure logs? Event Hub, Monitor, Entra ID, or Defender?"
- If GCP: "Which GCP service? Cloud Storage, Pub/Sub, or something else?"

**WAIT for response.**

**Then PROCEED to Step 3** with their specific source in mind.

#### If User Selected: SaaS Application

**ASK**: "Which SaaS application?"

**COMMON OPTIONS** (offer these as suggestions):
- Microsoft 365 / Office 365
- Okta
- Google Workspace
- Slack
- Other (have them specify)

**WAIT for response.**

**Then PROCEED to Step 3** with their specific source.

#### If User Selected: Security Tool

**ASK**: "Which security tool?"

**COMMON OPTIONS**:
- CrowdStrike Falcon
- Microsoft Defender
- SentinelOne
- Sophos
- Carbon Black
- Other (have them specify)

**WAIT for response.**

**Then PROCEED to Step 3** with their specific source.

#### If User Selected: Network Device

**ASK**: "What type of device and how does it send logs?"
- Firewall via Syslog (Palo Alto, Fortinet, etc.)
- Router or switch via Syslog
- Custom application logs
- Other

**WAIT for response.**

**If Syslog**: Note that this will require on-premises adapter deployment.

**Then PROCEED to Step 3** with their specific source.

#### If User Selected: Something Else / Not Sure

**ASK**: "Tell me more about the data source. What system or service has the logs you want to collect?"

**WAIT for response.**

**HELP them identify** the category based on their description, then route to appropriate path above.

---

### Step 3: Check Prerequisites

**Based on their specific source**, ask:

**SAY**: "To connect [SOURCE], we'll need [specific credentials/info]. Do you already have [LIST EXACTLY WHAT THEY NEED], or should I show you how to get them?"

**Examples by source**:

**For AWS CloudTrail**:
"To connect AWS CloudTrail, we'll need:
- An AWS Access Key ID and Secret Access Key
- The S3 bucket name where CloudTrail logs are stored (or SQS queue URL if you prefer)

Do you already have these, or should I walk you through creating them?"

**For Microsoft 365**:
"To connect Microsoft 365, we'll need:
- Azure Tenant ID
- Azure App Registration with Client ID and Client Secret
- API permissions configured

Do you already have an Azure App Registration set up for this, or should I guide you through creating one?"

**For Okta**:
"To connect Okta, we'll need:
- Your Okta URL (like https://yourcompany.okta.com)
- An Okta API token

Do you have an API token already, or should I show you how to create one?"

**WAIT for user response.**

---

### Step 4: Guide Credential Creation (If Needed)

**IF user says they need help creating credentials:**

**SAY**: "No problem! I'll walk you through it step by step."

**Then provide ONLY the steps for their specific source**, using the conversation templates below.

**IMPORTANT**:
- Show steps ONE AT A TIME
- After each step, ask them to confirm completion
- Wait for confirmation before showing next step
- If they get stuck, link to detailed walkthrough in EXAMPLES.md

**IF user says they already have credentials:**

**SAY**: "Great! Let's move on to creating your Installation Key."

**PROCEED to Step 5.**

---

### Step 5: Create Installation Key

**SAY**: "Now I'll create an Installation Key for your adapter. This authenticates it with LimaCharlie."

**EXPLAIN briefly**: "An Installation Key identifies which organization the adapter belongs to and can include tags to organize your sensors."

**ASK**: "What tags would you like on this adapter? For example, for AWS CloudTrail, you might use 'aws,cloudtrail'. Or just press enter for default tags."

**WAIT for response.**

**THEN**: Use MCP to create the key:

```bash
limacharlie installation_key create \
  --description "[SOURCE] Adapter" \
  --tags "[TAGS from user or sensible defaults]"
```

**SAY**: "Installation Key created! Moving on to the adapter configuration."

---

### Step 6: Generate Adapter Configuration

**SAY**: "I'm going to create the configuration file for your adapter. I'll need you to provide the credentials you gathered."

**For each credential**, ask ONE AT A TIME:

**Example for AWS CloudTrail**:
1. "What's your AWS Access Key ID?"
2. [WAIT]
3. "What's your AWS Secret Access Key?"
4. [WAIT]
5. "What's your S3 bucket name?"
6. [WAIT]

**Then GENERATE** the complete YAML configuration based on their source type.

**SHOW the configuration** and **EXPLAIN key parts**:

```yaml
# Example shown to user with explanations
s3:
  client_options:
    hostname: aws-cloudtrail-logs          # Display name in LimaCharlie
    identity:
      installation_key: [GENERATED_KEY]     # From Step 5
      oid: [ORG_ID]                         # Your organization
    platform: aws                           # Tells LC this is AWS data
    sensor_seed_key: aws-cloudtrail-prod    # Unique ID for this adapter
  bucket_name: [THEIR_BUCKET]
  secret_key: [THEIR_SECRET]
  access_key: [THEIR_ACCESS_KEY]
```

**ASK**: "Does this look correct? Should I proceed with deploying this configuration?"

**WAIT for confirmation.**

---

### Step 7: Deploy and Validate

**IF user confirms**:

**SAY**: "Deploying your adapter now..."

**Execute deployment** via MCP or provide CLI command:

```bash
limacharlie adapter create --config [config-file.yaml]
```

**THEN SAY**: "Adapter deployed! Let me check its status..."

**Check sensor status**:

```bash
limacharlie sensor list --filter "hostname:[THEIR_HOSTNAME]"
```

**Based on results**:

**IF online**:
"Great! Your adapter is online. Depending on the source, it may take a few minutes for data to start appearing. For [SOURCE], expect about [TYPICAL_DELAY]."

**IF offline/error**:
"I see the adapter is showing [STATUS/ERROR]. Let me help you troubleshoot this."

**THEN**: Guide them through validation or troubleshooting based on their specific situation.

---

### Step 8: Verify Data Flow

**SAY**: "Let's verify data is flowing. Based on [SOURCE], we should see events within [TIME_FRAME]."

**WAIT** the appropriate amount of time for their source:
- AWS CloudTrail: 5-15 minutes
- Microsoft 365: 5-30 minutes (warn: initial subscription can take up to 12 hours)
- Okta: 1-2 minutes
- CrowdStrike: Real-time to 1 minute
- Syslog: Real-time (seconds)

**Then check events**:

```bash
limacharlie events query --sensor-id [SID] --limit 10
```

**Based on results**:

**IF events present**:
"Perfect! I can see [EVENT_TYPES] coming in. Your [SOURCE] integration is working correctly."

**ASK**: "Would you like help with anything else, like setting up detection rules for this data?"

**IF no events**:
"I don't see events yet. This could be normal depending on timing, or there might be an issue. Let me help you troubleshoot."

**PROCEED** to troubleshooting section or link to TROUBLESHOOTING.md.

---

## Conversation Templates by Source

Use these as scripts for the most common sources. Follow them closely for consistent user experience.

### Template: AWS CloudTrail via S3

**After identifying AWS CloudTrail in Step 2:**

**Claude**: "Great! AWS CloudTrail via S3. This is a cloud-to-cloud connection, so no software to install. Let me check - do you already have an AWS IAM user with S3 read access set up for this, or should I guide you through creating one?"

**User**: [Response]

**IF need help**:

**Claude**: "No problem! Here's what we'll do:

**First**, let's make sure CloudTrail is enabled and logging to S3:
1. Go to the AWS Console → CloudTrail → Trails
2. Do you see an active trail there?"

**[WAIT for response]**

**User**: "Yes, I see a trail"

**Claude**: "Perfect! What's the S3 bucket name it's logging to? You can see it in the trail details."

**[WAIT for response]**

**User**: "my-cloudtrail-bucket"

**Claude**: "Got it. Now let's create IAM credentials:

1. Go to AWS Console → IAM → Users → Create user
2. Name it 'limacharlie-cloudtrail-reader'
3. Select 'Access key - Programmatic access'
4. Click Next

Let me know when you're at the permissions step."

**[WAIT]**

**User**: "I'm there"

**Claude**: "Great! Now:

1. Click 'Attach policies directly'
2. Click 'Create policy' (it opens a new tab)
3. Switch to the JSON tab
4. Paste this policy:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": ["s3:GetObject", "s3:ListBucket"],
      "Resource": [
        "arn:aws:s3:::my-cloudtrail-bucket/*",
        "arn:aws:s3:::my-cloudtrail-bucket"
      ]
    }
  ]
}
```

5. Name it 'LimaCharlie-S3-CloudTrail-Read'
6. Click Create policy

Let me know when that's done."

**[Continue step by step until they have credentials]**

**[Then proceed to Step 5: Create Installation Key]**

---

### Template: Microsoft 365

**After identifying Microsoft 365 in Step 2:**

**Claude**: "Excellent! Microsoft 365 audit logs are very valuable. To connect, we need to set up an Azure App Registration with the right permissions. Have you done this before, or should I walk you through it?"

**User**: [Response]

**IF need help**:

**Claude**: "I'll guide you step by step. First:

1. Open the Azure Portal (portal.azure.com)
2. Go to Azure Active Directory (or 'Microsoft Entra ID')
3. Click 'App registrations' in the left menu
4. Click 'New registration'

Are you there now?"

**[WAIT]**

**User**: "Yes"

**Claude**: "Perfect! Now:

1. Name it 'LimaCharlie-M365-Audit'
2. For 'Supported account types', select 'Accounts in this organizational directory only'
3. Leave Redirect URI blank
4. Click Register

Once it's created, you'll see an Overview page. Copy these three values for me:
- Application (client) ID
- Directory (tenant) ID

Paste them here when ready."

**[WAIT for values]**

**Claude**: "Great! Now let's create a client secret:

1. In your app registration, click 'Certificates & secrets' on the left
2. Click 'New client secret'
3. Description: 'LimaCharlie Adapter Secret'
4. Expires: 24 months (or whatever your policy requires)
5. Click Add
6. **IMMEDIATELY COPY the secret value** - you can only see it once

Paste the secret here (I'll keep it secure)."

**[Continue through API permissions, admin consent, etc. ONE STEP AT A TIME]**

---

### Template: Okta

**After identifying Okta in Step 2:**

**Claude**: "Perfect! Okta integration is straightforward. Do you already have an Okta API token, or should I show you how to create one?"

**User**: [Response]

**IF need help**:

**Claude**: "Easy! Here's what to do:

1. Log in to your Okta Admin Console
2. Go to Security → API
3. Click the 'Tokens' tab
4. Click 'Create Token'

Are you there?"

**[WAIT]**

**User**: "Yes"

**Claude**: "Great! Now:

1. Name it 'LimaCharlie System Log Reader'
2. Click 'Create Token'
3. **Copy the token value immediately** - you can only see it once
4. Paste it here"

**[WAIT]**

**User**: [Token value]

**Claude**: "Got it! One more thing - what's your Okta URL? It's the domain you use to access Okta, like https://dev-123456.okta.com or https://yourcompany.okta.com"

**[WAIT]**

**[Then proceed to Step 5: Create Installation Key]**

---

### Template: CrowdStrike Falcon

**After identifying CrowdStrike in Step 2:**

**Claude**: "CrowdStrike Falcon! This gives you real-time EDR events. Have you created API credentials in the Falcon console before, or is this your first time?"

**User**: [Response]

**IF need help**:

**Claude**: "I'll walk you through it:

1. Log in to the CrowdStrike Falcon Console (falcon.crowdstrike.com)
2. Go to Support and resources → API Clients and Keys
3. Click 'Create API client'

Let me know when you're there."

**[WAIT]**

**User**: "I'm there"

**Claude**: "Perfect! Now:

1. Client Name: 'LimaCharlie Event Streaming'
2. For API Scopes, check: **Event streams: Read**
3. Click Create

You'll see a Client ID and Client Secret. Copy both and paste them here (one per line)."

**[WAIT for credentials]**

**[Then proceed to Step 5: Create Installation Key]**

---

### Template: Firewall Syslog (On-Premises)

**After identifying Firewall/Syslog in Step 2:**

**Claude**: "Got it - firewall logs via Syslog. This will require running the LimaCharlie adapter binary on a server that can receive syslog from your firewall.

Do you have a Linux server (Ubuntu, CentOS, etc.) where you can run the adapter?"

**User**: [Response]

**IF yes**:

**Claude**: "Perfect! What type of firewall are you using? (Palo Alto, Fortinet, pfSense, or something else?) This helps me create the right parsing configuration."

**[WAIT]**

**User**: [Firewall type]

**Claude**: "Great! Here's what we'll do step by step:

**Step 1: Download the adapter on your Linux server**

Run these commands on your server:

```bash
wget https://downloads.limacharlie.io/sensor/linux/64 -O lc_adapter
chmod +x lc_adapter
sudo mv lc_adapter /usr/local/bin/
```

Let me know when that's done."

**[WAIT]**

**[Continue ONE STEP AT A TIME: create config file, test listening, configure firewall, create systemd service, validate]**

---

## Quick Concept Definitions (Show Only When Needed)

Use these when the user asks "what is X?" or when you need to briefly explain something during the flow.

**Installation Key**:
"An Installation Key is like an authentication token that connects your adapter to your LimaCharlie organization. It also includes tags to help organize your sensors."

**Sensor Seed Key**:
"The sensor_seed_key is a unique name you choose for this adapter. Using the same seed key if you redeploy keeps the same sensor identity in LimaCharlie."

**Platform Type**:
"The platform tells LimaCharlie what format your data is in (json, aws, text, etc.) so it can parse it correctly."

**Cloud-to-Cloud vs On-Prem**:
"Cloud-to-cloud means LimaCharlie connects directly to the vendor's API - no software to install. On-prem means you run a small adapter binary on your infrastructure to collect local data."

**For deeper explanations**, link to [REFERENCE.md](REFERENCE.md).

---

## When User Gets Stuck or Has Errors

### If User Reports an Error

**ASK**: "What's the exact error message you're seeing?"

**WAIT for error text.**

**THEN**: Based on the error:

**If authentication error** (401, 403, invalid credentials):
"This looks like an authentication issue. Let's verify your credentials..."
- Walk through checking specific credential for their source
- Link to [TROUBLESHOOTING.md - Authentication Errors](TROUBLESHOOTING.md#authentication-and-permission-errors)

**If connection error** (timeout, refused):
"This looks like a network connectivity issue. Let's check..."
- Verify network access
- Link to [TROUBLESHOOTING.md - Connection Issues](TROUBLESHOOTING.md#connection-and-network-issues)

**If no data appearing**:
"This is common - some sources have delays. For [THEIR_SOURCE], typical delay is [TIME]. Has it been that long?"
- If yes: troubleshoot
- If no: "Let's wait a bit longer, then check again"
- Link to [TROUBLESHOOTING.md - Data Not Appearing](TROUBLESHOOTING.md#data-not-appearing)

**If parsing error**:
"Looks like the data format doesn't match the parsing configuration. Let's look at a sample event..."
- Guide through checking raw data
- Link to [TROUBLESHOOTING.md - Parsing Errors](TROUBLESHOOTING.md#parsing-and-mapping-errors)

### If User Wants More Details

**IF user asks**: "Can I see all the adapter types?" or "What are all my options?"

**LINK**: "Absolutely! See [REFERENCE.md - Complete Adapter Type Catalog](REFERENCE.md#complete-adapter-type-catalog) for all 50+ adapter types."

**IF user asks**: "Show me a complete example from start to finish"

**LINK**: "Sure! Check out [EXAMPLES.md](EXAMPLES.md) - it has 6 detailed walkthroughs including AWS, Microsoft 365, Okta, and more."

---

## When to Activate This Skill

Activate when users say:
- "I want to connect [data source] to LimaCharlie"
- "How do I ingest [cloud provider] logs?"
- "Set up [SaaS app] integration"
- "Onboard external telemetry"
- "Add a new data source"
- "Connect my [firewall/security tool]"
- "I need help getting data into LimaCharlie"

---

**Remember**: Guide incrementally, ask one question at a time, wait for responses, and only show information relevant to their current step. Link to detailed docs rather than showing everything upfront.
