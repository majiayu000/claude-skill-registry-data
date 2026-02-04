---
name: Phishing Attacks
description: |
  The assistant guides users through phishing attack simulation tools and techniques for penetration testing and security awareness. Activate when users ask about "phishing simulation," "social engineering testing," "Shellphish," "WiFi phishing," "credential harvesting," or "security awareness training."
version: "1.0.0"
tags:
  - phishing
  - social-engineering
  - shellphish
  - wifiphisher
  - security-awareness
---

# Phishing Attacks

## Purpose

Demonstrate phishing attack techniques for authorized penetration testing and security awareness training. Enable security professionals to assess organizational susceptibility to social engineering attacks and improve employee security awareness.

## Inputs/Prerequisites

- Kali Linux or similar security distribution
- Written authorization for phishing simulation
- Target scope and employee consent
- Network adapter supporting monitor mode (for WiFi attacks)
- Understanding of social engineering principles

**DISCLAIMER:** This content is for educational and authorized penetration testing purposes only. Never conduct phishing attacks without explicit written authorization.

## Outputs/Deliverables

- Phishing campaign results and metrics
- Captured credentials (for authorized testing)
- Security awareness training recommendations
- Vulnerability assessment report
- Remediation guidance

## Core Workflow

### 1. Understanding Phishing

**What is Phishing?**

Phishing uses deceptive tactics to trick people into revealing sensitive information like passwords or financial details. It exploits human psychology and familiarity with trusted services.

**Attack Types:**

| Type | Description | Vector |
|------|-------------|--------|
| Email Phishing | Fake emails impersonating trusted entities | Email |
| Spear Phishing | Targeted attacks on specific individuals | Email |
| Whaling | Targeting executives and VIPs | Email |
| Vishing | Voice-based social engineering | Phone |
| Smishing | SMS-based phishing | Text message |
| Clone Phishing | Duplicating legitimate emails | Email |
| WiFi Phishing | Evil twin access points | WiFi |

**Why Phishing Works:**
- Leverages trust in familiar brands
- Exploits urgency and fear
- Targets human habits and routines
- Bypasses technical security controls

### 2. Shellphish Tool

Shellphish creates phishing pages for common websites to demonstrate credential harvesting vulnerabilities.

**Installation:**

```bash
# Navigate to installation directory
cd Desktop

# Clone repository
git clone https://github.com/thelinuxchoice/shellphish.git

# Enter directory
cd shellphish
ls

# Set permissions
chmod 744 shellphish.sh

# Launch tool
./shellphish.sh
```

**Available Templates:**

Shellphish includes templates for popular platforms:
- Social Media: Facebook, Instagram, Twitter/X, LinkedIn, Snapchat
- Email: Gmail, Yahoo, Outlook
- Streaming: Netflix
- Gaming: Steam, Origin, PlayStation
- Other: GitHub, StackOverflow, GitLab

**Using Shellphish:**

```bash
# Launch the tool
./shellphish.sh

# Select template (e.g., 4 for Twitter)
4

# Choose hosting method:
# 1: Localhost
# 2: Ngrok (recommended for external testing)
2

# Tool starts PHP and Ngrok servers
# Provides phishing URL: https://xxxx.ngrok.io
```

**Attack Workflow:**

1. **Select Target Platform** - Choose template matching target organization
2. **Generate Link** - Use Ngrok for HTTPS capability
3. **Craft Pretext** - Create convincing email narrative
4. **Deliver Payload** - Send phishing email with link
5. **Capture Credentials** - Monitor for incoming credentials

**Sample Email Template:**

```
Subject: Security Alert: Unusual Login Attempt Detected

Dear User,

We detected a suspicious login attempt on your account from:
- Location: Unknown
- Device: Windows PC
- Time: [Current Date/Time]

If this wasn't you, please secure your account immediately by
verifying your identity.

[Verify Now] <- Phishing Link

Best regards,
Security Team
```

**Credential Capture:**

When target enters credentials:
- Shellphish displays IP address, browser, location
- Credentials shown in plaintext
- Target redirected to legitimate site

### 3. Wifiphisher Tool

Wifiphisher performs automated WiFi phishing attacks by creating rogue access points.

**Requirements:**
- Kali Linux
- Two WiFi adapters:
  - One supporting AP (access point) mode
  - One supporting monitor mode

**Attack Phases:**

1. **Deauthentication** - Jam target access point, disconnect clients
2. **Evil Twin Creation** - Clone target AP settings, create rogue AP
3. **Credential Capture** - Serve phishing page to connected victims

**Installation:**

```bash
# Install Wifiphisher
apt update
apt install wifiphisher

# Or install from source
git clone https://github.com/wifiphisher/wifiphisher.git
cd wifiphisher
python setup.py install
```

**Basic Usage:**

```bash
# Launch with default settings
wifiphisher

# Specify interface
wifiphisher -aI wlan0 -jI wlan1

# Use specific phishing scenario
wifiphisher --essid "Free_WiFi" -p firmware-upgrade
```

**Phishing Scenarios:**

| Scenario | Description |
|----------|-------------|
| firmware-upgrade | Prompt for WPA password during "update" |
| oauth-login | Social media login portal |
| plugin-update | Browser plugin update page |

**Attack Flow:**

```
1. Victim connected to legitimate WiFi

2. Wifiphisher:
   - Scans for target networks
   - Sends deauth packets to disconnect victim
   - Creates identical AP (Evil Twin)
   - Sets up captive portal

3. Victim:
   - Device auto-reconnects to stronger signal
   - Opens browser → sees phishing page
   - Enters WiFi password

4. Attacker:
   - Captures WPA credentials
   - Can perform MitM attacks
```

### 4. Email Phishing Best Practices

**Crafting Convincing Emails:**

```
DO:
✓ Match sender domain closely
✓ Use proper grammar and formatting
✓ Include legitimate-looking logos
✓ Create sense of urgency
✓ Personalize with target information

DON'T:
✗ Use obvious fake domains
✗ Include spelling errors
✗ Make impossible claims
✗ Use threatening language excessively
✗ Request excessive information
```

**Social Engineering Pretexts:**

| Pretext | Trigger |
|---------|---------|
| Password expiry | Fear of losing access |
| Security alert | Urgency to protect account |
| Payment issue | Financial concern |
| Document shared | Curiosity |
| IT support | Authority compliance |

### 5. Detection and Defense

**Email Indicators of Phishing:**

```
Check for:
- Sender address doesn't match domain
- Generic greetings ("Dear Customer")
- Urgent or threatening language
- Suspicious links (hover to preview)
- Requests for sensitive information
- Unexpected attachments
- Poor grammar/spelling
```

**Technical Defenses:**

```bash
# Check SPF records
dig txt domain.com | grep spf

# Check DKIM
dig txt selector._domainkey.domain.com

# Check DMARC
dig txt _dmarc.domain.com
```

**Organizational Defenses:**

| Control | Purpose |
|---------|---------|
| Security Awareness Training | Educate employees |
| Email Filtering | Block malicious emails |
| Multi-Factor Authentication | Reduce credential impact |
| Phishing Simulations | Test and improve readiness |
| Reporting Mechanisms | Easy suspicious email reporting |

### 6. Security Awareness Training

**Training Resources:**

```
Google Phishing Quiz: https://phishingquiz.withgoogle.com/
Free online assessment for phishing recognition
```

**Key Training Topics:**
- Recognizing suspicious emails
- Verifying sender identity
- Hovering before clicking
- Reporting procedures
- Password hygiene

## Quick Reference

### Phishing Indicators Checklist

```
□ Check sender email address carefully
□ Hover over links before clicking
□ Look for urgency or threats
□ Verify through official channels
□ Never enter credentials from email links
□ Report suspicious emails immediately
```

### Tool Commands

```bash
# Shellphish
git clone https://github.com/thelinuxchoice/shellphish.git
cd shellphish && chmod 744 shellphish.sh && ./shellphish.sh

# Wifiphisher
wifiphisher -aI wlan0 -jI wlan1 -p firmware-upgrade

# GoPhish (enterprise phishing platform)
./gophish
```

## Constraints

- **Legal**: Must have written authorization
- **Ethical**: Purpose should be defensive/educational
- **Scope**: Only target authorized systems/users
- **Data**: Captured credentials must be handled securely
- **Reporting**: Full disclosure to client required

## Examples

### Example 1: Authorized Phishing Test

```bash
# Set up Shellphish with Gmail template
./shellphish.sh
# Select Gmail (option varies)
# Use Ngrok for HTTPS

# Send controlled test email to authorized users
# Monitor and document results
# Report findings to security team
```

### Example 2: WiFi Security Assessment

```bash
# With authorization from network owner
wifiphisher --essid "CompanyWiFi" -p firmware-upgrade

# Document captured credentials
# Report vulnerability to client
# Recommend WPA3 and user training
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Ngrok not connecting | Check internet connection, firewall |
| Templates not loading | Verify shellphish installation |
| WiFi adapter not detected | Check driver compatibility |
| Deauth not working | Verify monitor mode capability |
| Credentials not captured | Check PHP server running |
| Target suspicious | Improve email pretext quality |

## Reporting Findings

**Phishing Assessment Report Should Include:**
- Executive summary
- Methodology used
- Number of emails sent
- Click-through rate
- Credential submission rate
- User segments most vulnerable
- Comparison to benchmarks
- Recommendations for improvement
- Training material suggestions
