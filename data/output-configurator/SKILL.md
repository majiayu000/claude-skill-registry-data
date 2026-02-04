---
name: output-configurator
description: Use this skill when users need help configuring outputs to route telemetry to SIEMs, data lakes, or other destinations.
---

# LimaCharlie Output Configurator

I'll help you set up an output to send data from LimaCharlie to an external system. We'll work through this step by step - I'll ask questions and guide you through exactly what you need.

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
- ❌ Show all stream types upfront
- ❌ List all destination types unless asked
- ❌ Explain all concepts before starting
- ❌ Continue without user confirmation

---

## Conversation Flow Guide

### Step 1: Identify User's Goal

**ASK**: "What do you want to accomplish with this output?"

**OPTIONS**:
1. Send security alerts/detections to a SIEM or monitoring system
2. Archive all events for compliance or long-term storage
3. Get notifications in Slack or other chat platform
4. Stream data to a custom application or webhook
5. Forward logs to traditional infrastructure (Syslog, SFTP)
6. Something else / Not sure

**WAIT for user response. DO NOT continue until they answer.**

---

### Step 2: Choose Destination (Conditional on Step 1)

#### If User Selected: Send Alerts to SIEM

**ASK**: "Which SIEM or monitoring platform?"

**COMMON OPTIONS**:
- Splunk
- Elastic/Elasticsearch
- OpenSearch
- Kafka
- Generic webhook (for other SIEMs)
- Other (have them specify)

**WAIT for response.**

**THEN PROCEED to Step 3** with `detect` stream and their chosen destination.

#### If User Selected: Archive Events

**ASK**: "Which cloud storage?"

**OPTIONS**:
- Amazon S3
- Google Cloud Storage
- Azure Blob Storage
- Google BigQuery
- SFTP server
- Other

**WAIT for response.**

**THEN PROCEED to Step 3** with `event` stream and their chosen destination.

#### If User Selected: Notifications/Chat

**ASK**: "Which platform?"

**OPTIONS**:
- Slack
- Google Chat
- Webhook (for custom chat integrations)
- Email/SMTP
- Other

**WAIT for response.**

**THEN PROCEED to Step 3** with `detect` stream (for alerts) or `audit` stream (for platform changes).

#### If User Selected: Custom Application/Webhook

**ASK**: "What type of data does your application need?"
- Security detections/alerts
- All telemetry events
- Platform audit logs
- Sensor status updates

**WAIT for response.**

**THEN PROCEED to Step 3** with appropriate stream based on their answer.

#### If User Selected: Traditional Infrastructure

**ASK**: "Which destination?"

**OPTIONS**:
- Syslog server
- SFTP server
- Email/SMTP

**WAIT for response.**

**THEN PROCEED to Step 3** with appropriate stream.

#### If User Selected: Something Else / Not Sure

**ASK**: "Tell me more about what you're trying to achieve. Where do you want the data to go, and what will you do with it?"

**WAIT for response.**

**HELP them identify** the appropriate category based on their description, then route to appropriate path above.

---

### Step 3: Explain Stream Choice

**Based on their goal**, explain which stream is appropriate:

**For Security Alerts**:
**SAY**: "For security alerts, we'll use the **Detection stream** (`detect`). This sends only alerts triggered by your Detection & Response rules - much lower volume than all events. These detections include the original event data plus structured metadata about what was detected."

**For All Events/Archival**:
**SAY**: "For archiving all telemetry, we'll use the **Event stream** (`event`). This sends every event from your sensors - process executions, network connections, file changes, etc. This is high volume, so I'll help you set up compression and filtering to manage costs."

**For Platform Changes**:
**SAY**: "For platform monitoring, we'll use the **Audit stream** (`audit`). This captures configuration changes, user actions, and API calls in LimaCharlie itself."

**For Sensor Health**:
**SAY**: "For deployment tracking, we'll use the **Deployment stream** (`deployment`). This shows sensor online/offline status and quota events."

**ASK**: "Does that sound right for what you need?"

**WAIT for confirmation.**

---

### Step 4: Check Prerequisites

**Based on their specific destination**, ask:

**SAY**: "To connect to [DESTINATION], we'll need [specific credentials/config]. Do you already have [LIST EXACTLY WHAT THEY NEED], or should I show you how to get them?"

**Examples by destination**:

**For Splunk**:
"To send data to Splunk, we'll need:
- Your Splunk server URL (like https://splunk.company.com:8088)
- An HEC (HTTP Event Collector) token

Do you already have an HEC token, or should I walk you through creating one?"

**For Amazon S3**:
"To archive to S3, we'll need:
- S3 bucket name
- AWS Access Key ID and Secret Access Key (IAM user with S3 PutObject permission)
- AWS region

Do you have these credentials, or should I guide you through setting that up?"

**For Slack**:
"To send alerts to Slack, we'll need:
- A Slack App with a Bot User OAuth Token
- The channel name (like #security-alerts)

Have you created a Slack App before, or is this your first time?"

**For Elastic/Elasticsearch**:
"To send data to Elasticsearch, we'll need:
- Elasticsearch host address(es)
- Index name
- Authentication (username/password or API key)

Do you have these details, or need help figuring them out?"

**For Generic Webhook**:
"To send to a webhook, I'll need:
- The webhook URL
- Authentication method (if required)

What's the webhook URL where you want to receive the data?"

**WAIT for user response.**

---

### Step 5: Guide Setup (If Needed)

**IF user says they need help:**

**SAY**: "No problem! I'll walk you through it step by step."

**Then provide ONLY the steps for their specific destination**, using the conversation templates below.

**IMPORTANT**:
- Show steps ONE AT A TIME
- After each step, ask them to confirm completion
- Wait for confirmation before showing next step
- If they get stuck, link to detailed walkthrough in EXAMPLES.md

**IF user says they already have credentials:**

**SAY**: "Great! Let's move on to configuring the output."

**PROCEED to Step 6.**

---

### Step 6: Configure Filtering (Optional)

**ASK**: "Do you want to send ALL [stream type] data, or filter to specific events?"

**EXAMPLES of what filtering can do**:
- **For detections**: Send only high-priority alerts (priority > 5)
- **For events**: Send only Windows events, or only process executions
- **For any stream**: Send only events from specific sensors (by tag)

**WAIT for response.**

**IF they want filtering**:

**ASK**: "What should we filter on?"

Based on stream type, offer relevant filters:
- For `detect`: Priority, detection name, detection category, sensor tags
- For `event`: Event type, platform (Windows/Linux/Mac), sensor tags
- For `audit`: Event type, user
- For `deployment`: Event type

**WAIT for filter criteria.**

**Then configure filters** based on their input.

**IF they want all data**:

**SAY**: "Got it - we'll send all [stream type] data to [destination]."

**PROCEED to Step 7.**

---

### Step 7: Generate Output Configuration

**SAY**: "I'm going to create the output configuration now. I'll need the credentials/details from earlier."

**For each credential**, ask ONE AT A TIME:

**Example for Splunk**:
1. "What's your Splunk server URL (including port, like https://splunk.company.com:8088)?"
2. [WAIT]
3. "What's your HEC token?"
4. [WAIT]

**Example for S3**:
1. "What's your S3 bucket name?"
2. [WAIT]
3. "What's your AWS Access Key ID?"
4. [WAIT]
5. "What's your AWS Secret Access Key?"
6. [WAIT]
7. "What region is the bucket in (like us-east-1)?"
8. [WAIT]

**Then GENERATE** the complete output configuration.

**SHOW the configuration** and **EXPLAIN key parts**:

```yaml
# Example for Splunk detection output
name: splunk-detections
stream: detect                                # Sends detection alerts
module: webhook
dest_host: https://splunk.company.com:8088/services/collector/raw
auth_header_name: Authorization
auth_header_value: Splunk XXXXX-YOUR-TOKEN-XXXXX
secret_key: optional-hmac-secret              # For webhook signature validation
```

**ASK**: "Does this look correct? Should I proceed with creating this output?"

**WAIT for confirmation.**

---

### Step 8: Deploy and Test

**IF user confirms**:

**SAY**: "Creating the output now..."

**Execute via MCP or CLI**:

```bash
limacharlie output create --config output-config.yaml
```

**OR provide CLI instructions**:

"You can create this output by:
1. Going to LimaCharlie web UI → Outputs
2. Click 'Add Output'
3. Choose stream type: [stream]
4. Choose module: [destination type]
5. Fill in the details I showed above"

**THEN SAY**: "Now let's test it to make sure data is flowing."

**For `detect` stream**:
"To test, we can trigger a simple detection. Or if you have existing detections firing, we should see them arrive within a few seconds."

**For `event` stream**:
"Events should start flowing immediately. Depending on your filtering, this could be high volume."

**For `audit` stream**:
"Let me trigger a test audit event by making a small config change. You should see it arrive within seconds."

**For `deployment` stream**:
"Deployment events occur when sensors connect/disconnect. If you have sensors online, you may see events soon."

**ASK**: "Can you check [destination] and confirm you're seeing data?"

**WAIT for confirmation.**

---

### Step 9: Verify and Optimize

**Based on their response**:

**IF they see data**:
"Perfect! Your output is working correctly.

A few optimization tips:
- [If S3/GCS] Enable compression to reduce storage costs by ~70%
- [If event stream] Consider adding filters to reduce volume and costs
- [If webhook] Verify HMAC signature to prevent spoofing

Would you like help with any of these?"

**IF they don't see data**:
"Let's troubleshoot. What are you seeing (or not seeing) at [destination]?"

**WAIT for description.**

**Then guide troubleshooting** based on their specific issue (see Error Handling section below).

---

## Conversation Templates by Destination

Use these as scripts for the most common destinations. Follow them closely for consistent user experience.

### Template: Splunk HEC Integration

**After identifying Splunk in Step 2:**

**Claude**: "Splunk is perfect for SIEM integration. Do you already have an HEC (HTTP Event Collector) token, or should I show you how to create one?"

**User**: [Response]

**IF need help**:

**Claude**: "I'll walk you through it:

**Step 1: Enable HEC in Splunk**

1. Log in to Splunk Web
2. Go to Settings → Data Inputs
3. Click 'HTTP Event Collector'

Are you there?"

**[WAIT]**

**User**: "Yes"

**Claude**: "Great! Now:

1. Click 'New Token' (or 'Create New Token')
2. Name it 'LimaCharlie Detections' (or whatever makes sense)
3. Click Next
4. For **Source type**, select `_json`
5. Click Review, then Submit

You'll see your token value. Copy it and paste it here."

**[WAIT for token]**

**User**: [Token value]

**Claude**: "Perfect! One more thing - what's your Splunk server URL?

For Splunk Enterprise, it's usually: `https://your-splunk-server:8088`
For Splunk Cloud, it's: `https://your-host.splunkcloud.com:8088`

What's yours?"

**[WAIT for URL]**

**User**: [URL]

**Claude**: "Got it! Now let me generate the configuration..."

**[Proceed to Step 7: Generate Configuration]**

---

### Template: Amazon S3 Archival

**After identifying S3 in Step 2:**

**Claude**: "S3 is excellent for long-term archival and compliance. Do you already have an S3 bucket and IAM user credentials set up for this, or should I guide you through that?"

**User**: [Response]

**IF need help**:

**Claude**: "I'll guide you step by step.

**Step 1: Create S3 bucket**

1. Go to AWS Console → S3
2. Click 'Create bucket'
3. Choose a unique bucket name (like 'company-limacharlie-events')
4. Select your region (choose one close to you for performance)
5. Leave other settings as default
6. Click Create

Let me know when you've created the bucket and what you named it."

**[WAIT]**

**User**: "Created bucket: my-lc-events"

**Claude**: "Perfect! Now let's create IAM credentials.

**Step 2: Create IAM user**

1. Go to AWS Console → IAM → Users
2. Click 'Create user'
3. Username: 'limacharlie-output'
4. Click Next

Let me know when you're at the permissions step."

**[WAIT]**

**User**: "I'm there"

**Claude**: "Great! Now:

1. Click 'Attach policies directly'
2. Click 'Create policy'
3. Switch to the JSON tab
4. Paste this:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": ["s3:PutObject", "s3:PutObjectAcl"],
      "Resource": "arn:aws:s3:::my-lc-events/*"
    }
  ]
}
```

5. Name it 'LimaCharlie-S3-Write'
6. Create the policy

Then go back to the user creation tab, refresh, and select that policy. Let me know when done."

**[WAIT]**

**[Continue through creating access keys, one step at a time]**

---

### Template: Slack Notifications

**After identifying Slack in Step 2:**

**Claude**: "Slack is perfect for real-time alerts. Have you created a Slack App with a bot token before, or is this your first time?"

**User**: [Response]

**IF need help**:

**Claude**: "I'll walk you through it - it's easier than it sounds!

**Step 1: Create Slack App**

1. Go to https://api.slack.com/apps
2. Click 'Create New App'
3. Choose 'From scratch'
4. Name it 'LimaCharlie' (or whatever you prefer)
5. Select your workspace
6. Click 'Create App'

Let me know when you're at the app's Basic Information page."

**[WAIT]**

**User**: "I'm there"

**Claude**: "Perfect! Now we'll give it permission to post messages.

**Step 2: Add OAuth Scope**

1. Click 'OAuth & Permissions' in the left sidebar
2. Scroll to 'Bot Token Scopes'
3. Click 'Add an OAuth Scope'
4. Select `chat:write`

Done? Let me know."

**[WAIT]**

**User**: "Done"

**Claude**: "Great! Now let's install it.

**Step 3: Install to Workspace**

1. Scroll back up on the same page
2. Click 'Install to Workspace'
3. Click 'Allow'

You'll see a 'Bot User OAuth Token' - it starts with `xoxb-`. Copy that token and paste it here."

**[WAIT for token]**

**User**: [Token]

**Claude**: "Perfect! Last step - what channel do you want alerts in? (like #security-alerts)"

**[WAIT for channel]**

**User**: "#security-alerts"

**Claude**: "Got it! One more thing - you need to invite the bot to that channel. In Slack, go to #security-alerts and type:

`/invite @LimaCharlie`

(or whatever you named your app)

Let me know when that's done."

**[WAIT]**

**[Then proceed to Step 7: Generate Configuration]**

---

### Template: Elastic/Elasticsearch

**After identifying Elastic in Step 2:**

**Claude**: "Elasticsearch integration. Do you have your Elasticsearch connection details (host, credentials), or need help getting those?"

**User**: [Response]

**IF need help**:

**Claude**: "Let's gather the connection details.

First, what's your Elasticsearch host address? It might be:
- `elastic.company.com` (self-hosted)
- A Cloud ID if you're using Elastic Cloud
- Multiple hosts separated by commas

What's yours?"

**[WAIT for host]**

**User**: [Host]

**Claude**: "Got it. Now, what type of authentication does your Elasticsearch use?"
- Username and password
- API key
- No authentication (not recommended)

**[WAIT for auth type]**

**User**: "Username and password"

**Claude**: "Perfect. What's the username?"

**[WAIT]**

**[Continue collecting credentials one at a time]**

**Claude**: "What index name should we use? This is where LimaCharlie data will be stored in Elasticsearch. Common choices are 'limacharlie', 'security-events', or 'edr'."

**[WAIT for index name]**

**[Then proceed to Step 7: Generate Configuration]**

---

### Template: Generic Webhook

**After identifying Webhook in Step 2:**

**Claude**: "Webhook setup. What's the URL where you want to receive events?"

**User**: [URL]

**Claude**: "Got it: [URL]

Does this webhook endpoint require authentication?"

**OPTIONS**:
- API key in header (most common)
- Basic authentication
- Just HMAC signature verification (LimaCharlie adds this automatically)
- No authentication

**[WAIT for response]**

**IF API key**:

**Claude**: "What's the header name for the API key? Common examples are:
- `Authorization`
- `X-API-Key`
- `X-Auth-Token`

What does your endpoint expect?"

**[WAIT for header name]**

**Claude**: "And what's the API key value?"

**[WAIT for key value]**

**IF Basic auth**:

**Claude**: "What's the username?"

**[WAIT]**

**Claude**: "And the password?"

**[WAIT]**

**IF HMAC only or no auth**:

**Claude**: "Got it. I'll set up HMAC signature verification so you can validate the requests are from LimaCharlie. I'll generate a shared secret for this."

**[Then proceed to Step 7: Generate Configuration]**

---

### Template: Syslog Server

**After identifying Syslog in Step 2:**

**Claude**: "Syslog forwarding. What's your syslog server hostname or IP address?"

**User**: [Host]

**Claude**: "What port is your syslog server listening on? (Usually 514 or 6514)"

**[WAIT]**

**User**: [Port]

**Claude**: "Which protocol?"
- TCP
- UDP
- TCP with TLS (most secure)

**[WAIT for protocol]**

**User**: [Protocol]

**IF TLS**:

**Claude**: "Great! For TLS, I'll need the server's certificate. Do you have the certificate file, or should we proceed without certificate verification? (Not recommended for production)"

**[WAIT and handle accordingly]**

**[Then proceed to Step 7: Generate Configuration]**

---

## Quick Concept Definitions (Show Only When Needed)

Use these when the user asks "what is X?" or when you need to briefly explain something during the flow.

**Streams**:
"LimaCharlie has 4 data streams you can output:
- **detect**: Security alerts from D&R rules
- **event**: All telemetry from sensors (high volume)
- **audit**: Platform configuration changes
- **deployment**: Sensor online/offline status"

**HEC Token**:
"HEC stands for HTTP Event Collector - it's Splunk's way of receiving data over HTTP. The token authenticates LimaCharlie to send data to your Splunk instance."

**HMAC Signature**:
"LimaCharlie adds a cryptographic signature to webhook requests in the `lc-signature` header. You can verify this signature using the shared secret to ensure requests are actually from LimaCharlie and haven't been tampered with."

**Filtering**:
"Filters let you control which events get sent to the output. For example, you can send only high-priority detections, only Windows events, or only events from sensors with a specific tag. This reduces volume and costs."

**Bulk Webhook**:
"Bulk webhook batches multiple events into a single HTTP request. This is more efficient than individual webhooks for high-volume streams, reducing both network overhead and costs."

**For deeper explanations**, link to [REFERENCE.md](REFERENCE.md).

---

## When User Gets Stuck or Has Errors

### If User Reports an Error

**ASK**: "What's the exact error message you're seeing, and where are you seeing it?"

**WAIT for error text and context.**

**THEN**: Based on the error:

**If authentication/credential error**:
"This looks like an authentication issue. Let's verify your credentials..."
- Double-check the exact values they provided
- For Splunk: Verify HEC token format (should be UUID)
- For S3: Verify access keys are active and have correct permissions
- For Slack: Verify bot token starts with `xoxb-`
- Link to [TROUBLESHOOTING.md - Authentication Errors](TROUBLESHOOTING.md#authentication-errors)

**If "no data arriving" at destination**:
"Let's troubleshoot the data flow. First, can you check if the output shows as 'active' in LimaCharlie?"

**[WAIT]**

"Now, let's verify data is actually being generated:
- For detect stream: Do you have active D&R rules creating detections?
- For event stream: Do you have sensors connected and generating events?
- For audit stream: Let me trigger a test event by making a config change."

Link to [TROUBLESHOOTING.md - No Data Arriving](TROUBLESHOOTING.md#no-data-arriving)

**If destination unreachable**:
"This looks like a connectivity issue. Let's check:
- Is the URL/hostname correct?
- Is the port correct and accessible from the internet?
- Are there any firewall rules blocking LimaCharlie's IPs?"

Note: "LimaCharlie doesn't have static IPs - we use auto-scaling. Authentication should be via HMAC signatures or API keys, not IP allowlisting."

Link to [TROUBLESHOOTING.md - Connection Issues](TROUBLESHOOTING.md#connection-issues)

**If data format issues**:
"It sounds like the data is arriving but not in the format you expected. Let's look at what you're receiving..."
- Show them the stream structure documentation
- Explain routing vs event object
- Link to [REFERENCE.md - Stream Structures](REFERENCE.md#stream-structures)

### If User Wants More Details

**IF user asks**: "Can I see all the output destination types?" or "What are all my options?"

**LINK**: "Absolutely! See [REFERENCE.md - All Output Destinations](REFERENCE.md#supported-output-destinations) for all 18+ destination types."

**IF user asks**: "Show me a complete example from start to finish"

**LINK**: "Sure! Check out [EXAMPLES.md](EXAMPLES.md) - it has detailed walkthroughs for Splunk, S3, Slack, and more."

**IF user asks**: "How much will this cost?"

**LINK**: "Good question! Output costs depend on volume. See [REFERENCE.md - Output Billing](REFERENCE.md#output-billing) for details. Short answer: detect stream is usually low-cost, event stream can be high-volume so use filtering and compression."

---

## When to Activate This Skill

Activate when users say:
- "I want to send data to [SIEM/storage/platform]"
- "How do I configure Splunk integration?"
- "Set up an output to S3"
- "Forward detections to Slack"
- "Connect LimaCharlie to Elasticsearch"
- "Send events to a webhook"
- "I need to export LimaCharlie data"
- "Configure SIEM integration"

---

**Remember**: Guide incrementally, ask one question at a time, wait for responses, and only show information relevant to their current step. Link to detailed docs rather than showing everything upfront.
