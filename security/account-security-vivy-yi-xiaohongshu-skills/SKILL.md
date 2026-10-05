---
name: account-security
description: Use when protecting Xiaohongshu account from unauthorized access, preventing account theft, recovering compromised accounts, or implementing security measures to safeguard account and follower base
---

# Account Security (账号安全)

## Overview

Account security is the practice of implementing protective measures to prevent unauthorized access to Xiaohongshu accounts, safeguarding personal information and content, and responding effectively to security breaches or account theft.

## When to Use

**Use when**:
- Setting up new account (implement security from start)
- Account has grown in value (followers, content library worth protecting)
- Experiencing suspicious activity
- Recovering from account theft or hack
- Sharing account access (team, assistant)
- Concerned about account safety

**Do NOT use when**:
- Account has no value yet (new account, focus on growth)
- Overly paranoid (basic security sufficient for most)

## Core Pattern

**Before** (vulnerable account):
```
❌ "Simple password '123456', anyone could guess"
❌ "Logged in on public WiFi, account hacked"
❌ "Gave password to assistant, they stole account"
❌ "Account stolen, no way to recover (no proof of ownership)"
❌ "Years of work lost in seconds"
```

**After** (secured account):
```
✅ "Strong unique password + two-factor authentication"
✅ "Only log in on secure networks, devices protected"
✅ "Access log tracks all logins, suspicious activity detected"
✅ "Account recovery plan in place (proof of ownership documented)"
✅ "Team access managed (individual login credentials)"
✅ "Peace of mind: account and followers protected"
```

**5 Security Layers**:
1. **Strong Authentication** - Unique password, 2FA enabled
2. **Secure Access** - Only trusted devices/networks
3. **Access Control** - Manage who can access account
4. **Monitoring** - Track login activity, detect breaches early
5. **Recovery Preparedness** - Document proof of ownership

## Quick Reference

| Security Measure | Protection Level | Implementation | Priority |
|------------------|------------------|----------------|----------|
| **Strong Password** | High | Unique, complex password | Critical |
| **Two-Factor Authentication** | Very High | SMS or authenticator app | Critical |
| **Trusted Devices Only** | Medium | Limit login devices | High |
| **Secure Networks** | Medium | Avoid public WiFi | High |
| **Access Monitoring** | High | Regular login activity review | High |
| **Recovery Plan** | Very High | Document ownership proof | Critical |

## Implementation

### Step 1: Implement Strong Authentication

**Password and 2FA**:
```
Secure Account Access:

1. Create Strong Password
   Password Requirements:
   ✅ Minimum 12 characters (longer is better)
   ✅ Mix of uppercase and lowercase letters
   ✅ Include numbers and symbols
   ✅ No personal information (name, birthday)
   ✅ Not used on any other site (unique)
   ✅ Not a common word or pattern

   Good Password Examples:
   - "Tr0ub4dor&3Horse!Battery" (22 chars, random)
   - "9k$P2m#vL7xQ!zR4" (15 chars, random characters)
   - "Correct-Horse-Battery-Staple-99" (phrase-based, memorable)

   Bad Password Examples:
   ❌ "123456" (too simple)
   ❌ "password" (common word)
   ❌ "xiaohongshu2026" (predictable, app name)
   ❌ "Name123456" (contains personal info)

   Password Management:
   - Use password manager (1Password, LastPass, Bitwarden)
   - Never reuse passwords across sites
   - Change password annually (or if breach suspected)
   - Never share password (except recovery backup)

2. Enable Two-Factor Authentication (2FA)
   What is 2FA:
   - Requires second verification beyond password
   - Typically: code sent to phone or authenticator app
   - Prevents unauthorized access even with password

   Enable in Xiaohongshu:
   - Go to: Settings → Security
   - Find: Two-Factor Authentication
   - Choose: SMS code or Authenticator App
   - Follow: Setup instructions

   Authenticator App (Recommended over SMS):
   - Google Authenticator
   - Authy
   - Microsoft Authenticator
   - 1Password (built-in)

   Benefits:
   ✅ More secure than SMS (SIM hijacking risk)
   ✅ Works offline
   ✅ No phone signal required

   Backup Codes:
   - Generate backup codes during setup
   - Store securely (password manager, safe)
   - Use if lose access to 2FA device

3. Secure Login Credentials
   Storage:
   ✅ Use password manager (encrypted)
   ✅ Never store in plain text (notes app, email)
   ✅ Never share screenshot of password
   ✅ Never write password physically (unless secured safe)

   Sharing (Only if absolutely necessary):
   ✅ Use password manager sharing feature (encrypted)
   ✅ Change password immediately after person no longer needs access
   ✅ Track who has access (access log)

   Emergency Access:
   - Designate trusted contact for emergency access
   - Store sealed envelope with password in safe
   - Use password manager emergency access feature
   - Document for estate planning (digital assets)
```

### Step 2: Control Access Points

**Secure Login Locations and Devices**:
```
Limit Account Access:

1. Trusted Devices Only
   Device Management:
   ✅ Only use personal devices (phone, computer)
   ✅ Avoid public computers (library, internet cafe)
   ✅ Log out from shared devices after use
   ✅ Remove old devices from account (device list)

   Manage Devices in Xiaohongshu:
   - Go to: Settings → Security → Login Devices
   - Review: All devices with account access
   - Remove: Unrecognized or old devices
   - Enable: "Trusted devices only" (if available)

   Device Security:
   ✅ Use device passcode/biometrics (Face ID, fingerprint)
   ✅ Keep OS updated (security patches)
   ✅ Use antivirus/anti-malware (computers)
   ✅ Encrypt device storage (full disk encryption)

2. Secure Networks
   Safe Networks:
   ✅ Home WiFi (secured with strong password)
   ✅ Cellular data (4G/5G)
   ✅ Work VPN (if using work network)

   Avoid:
   ❌ Public WiFi (coffee shop, airport, hotel)
   ❌ Unsecured networks (no password required)
   ❌ Shared networks (neighbor's WiFi)

   If Must Use Public WiFi:
   ✅ Use VPN (virtual private network)
   ✅ Avoid logging into accounts (if possible)
   ✅ Log out immediately after use
   ✅ Don't save passwords on device

   VPN Recommendations:
   - ExpressVPN
   - NordVPN
   - Surfshark
   - Orbot (free, open source)

3. Browser and App Security
   Browser Security:
   ✅ Use updated browser (Chrome, Firefox, Safari)
   ✅ Enable browser password manager (encrypted storage)
   ✅ Use privacy extensions (HTTPS Everywhere, Privacy Badger)
   ✅ Clear cookies/cache after using public computer

   App Security:
   ✅ Keep Xiaohongshu app updated
   ✅ Only download from official app store (not third-party)
   ✅ Review app permissions (location, contacts, etc.)
   ✅ Lock app with biometrics (if available)

   Anti-Phishing:
   ✅ Verify URL (xiaohongshu.com, not typos)
   ✅ Don't click suspicious links in DMs or emails
   ✅ Verify official communications (Xiaohongshu won't ask for password)
   ✅ Report phishing attempts

4. Session Management
   Auto-Logout Settings:
   ✅ Enable "Logout after X minutes of inactivity"
   ✅ Set to: 15-30 minutes (balance security vs convenience)
   ✅ Always log out after use (shared or public devices)

   Active Sessions:
   - Go to: Settings → Security → Active Sessions
   - Review: All currently active sessions
   - Terminate: Unrecognized sessions
   - Regular: Check weekly

   Login Notifications:
   ✅ Enable: "New login notification"
   ✅ Receive: SMS/email for new logins
   ✅ Respond: Immediately if not you
```

### Step 3: Monitor Account Activity

**Detect Suspicious Activity Early**:
```
Security Monitoring Routine:

1. Regular Login Review
   Weekly Check:
   ✅ Review login history (Settings → Security)
   ✅ Check: Location, device, time of each login
   ✅ Verify: All logins were you
   ✅ Investigate: Any unrecognized login

   What to Look For:
   ⚠️ Login from different city/country
   ⚠️ Login from unknown device
   ⚠️ Login at unusual time (3 AM when you were asleep)
   ⚠️ Multiple failed login attempts

2. Content and Activity Monitoring
   Weekly Check:
   ✅ Review posts you didn't create
   ✅ Check DMs you didn't send
   ✅ Verify comments you didn't write
   ✅ Monitor: Follower count sudden changes

   Signs of Account Breach:
   ⚠️ Posts or stories you didn't create
   ⚠️ DMs sent to your followers (spam, scams)
   ⚠️ Comments you didn't write
   ⚠️ Sudden follower drop (mass unfollow by hacker)
   ⚠️ Bio or profile changed
   ⚠️ Password suddenly stops working

3. Follower and Engagement Monitoring
   Watch For:
   ⚠️ Sudden follower drop (hacker unfollowing everyone)
   ⚠️ Unusual engagement patterns (spam likes/comments)
   ⚠️ Followers receiving spam from your account
   ⚠️ Reports from followers: "Are you hacked? You sent me weird DM"

   Action:
   - If followers report suspicious activity:
     ✅ Thank them for reporting
     ✅ Immediately check account security
     ✅ Post public announcement if confirmed hacked

4. Third-Party App Access
   Review Connected Apps:
   - Go to: Settings → Security → Connected Apps/Third-Party Access
   - Review: All apps with account access
   - Remove: Apps you don't recognize or no longer use
   - Revoke: Old permissions (apps not used in 6+ months)

   Only Authorize:
   ✅ Official apps (Xiaohongshu analytics tools)
   ✅ Reputable third-party apps (well-known brands)
   ✅ Apps you actively use

   Never Authorize:
   ❌ Apps promising free followers/likes (scams)
   ❌ Unfamiliar apps (can steal account access)
   ❌ Apps requesting excessive permissions

5. Set Up Security Alerts
   Enable Notifications:
   ✅ New login from new device
   ✅ Password change
   ✅ Email/phone change
   ✅ New connected app
   ✅ Unusual activity detected

   Response to Alerts:
   ⚠️ Immediate action required
   ✅ Verify: Was this you?
   ✅ If not: Change password immediately, enable 2FA
   ✅ If yes: No action needed (legitimate activity)
```

### Step 4: Manage Team Access

**Control Shared Account Access**:
```
Team Access Security:

1. Individual Login Credentials (Best Practice)
   Instead of Sharing Password:
   ✅ Use Xiaohongshu Business/Team features (if available)
   ✅ Each team member has own login
   ✅ Grant specific permissions (content, analytics, messages)
   ✅ Revoke access when team member leaves

   Benefits:
   ✅ No password sharing
   ✅ Access audit trail (who did what)
   ✅ Easy to revoke individual access
   ✅ No need to change password when team leaves

2. If Password Sharing is Necessary
   Minimize Risk:
   ✅ Use password manager sharing feature (encrypted)
   ✅ Share only with trusted individuals
   ✅ Document who has access (access log)
   ✅ Change password when access no longer needed

   Access Log Template:
   Date | Team Member | Purpose | Access Revoked
   -----|-------------|---------|---------------
   [date] | [Name] | [Content creation] | [date]

   Agreement:
   "Team Access Agreement for @[account]

    You are being granted access to this Xiaohongshu account
    for the purpose of: [specific purpose].

    Responsibilities:
    - Use account only for stated purpose
    - Do not share password with anyone
    - Log out after each session
    - Report any security issues immediately

    Access will be revoked: [condition or date]

    By accepting this access, you agree to these terms."

3. Regular Access Audits
   Monthly Review:
   ✅ Who currently has access?
   ✅ Do they still need access?
   ✅ Revoke access for former team members
   ✅ Change password if access shared externally

   Revocation Checklist:
   ✅ Team member left company
   ✅ Project completed (no longer needs access)
   ✅ Security concern (suspicious activity)
   ✅ Regular rotation (every 6 months change password)

4. Team Training
   Educate Team Members:
   ✅ Password security (don't share, don't write down)
   ✅ Phishing awareness (recognize scams)
   ✅ Device security (use secure devices only)
   ✅ Reporting protocol (what to do if breach suspected)

   Training Checklist:
   - Onboarding: Security overview during training
   - Regular: Quarterly security reminders
   - Updates: Immediately after security incident

   Security Briefing Template:
   "Account Security Briefing

    Your access to @[account] is a privilege and responsibility.

    Security Requirements:
    1. Never share password with anyone
    2. Only log in from secure, trusted devices
    3. Use official Xiaohongshu app (not third-party)
    4. Report suspicious activity immediately
    5. Log out after each session

    If you suspect breach:
    1. Stop using account immediately
    2. Report to account owner immediately
    3. Don't attempt to fix yourself (may destroy evidence)

    Your access helps us create great content.
    Let's keep the account secure!"
```

### Step 5: Prepare Recovery Plan

**Document Proof of Ownership**:
```
Account Recovery Preparation:

1. Document Ownership Evidence
   Gather and Secure:
   ✅ Account creation date (screenshot or note)
   ✅ Original email/phone used to create account
   ✅ Account ID (find in settings or profile URL)
   ✅ Historical content (screenshots of old posts)
   ✅ Follower growth screenshots (over time)
   ✅ Brand partnerships documentation (contracts, emails)
   ✅ Account screenshots (profile, bio, content)

   Organization:
   - Create: "Account Recovery" folder (secure, encrypted)
   - Include: All above evidence
   - Update: Add new evidence periodically
   - Backup: Store in multiple secure locations (cloud + physical)

2. Alternative Contact Methods
   Verify Account Ownership:
   ✅ Linked email address (access to email)
   ✅ Linked phone number (access to phone)
   ✅ Connected social media (prove identity via other accounts)
   ✅ Official website (mention account on official site)

   Keep Updated:
   ✅ Email address current and accessible
   ✅ Phone number current
   ✅ Recovery email separate from primary email (backup)

3. Recovery Contact Information
   Document for Xiaohongshu Support:
   ✅ Account username (handle)
   ✅ Account display name
   ✅ Account ID (if available)
   ✅ Original creation email
   ✅ Original creation phone number
   ✅ Current email (if different)
   ✅ Current phone (if different)
   ✅ Linked social media accounts
   ✅ Official website (if applicable)

   Recovery Letter Template:
   "Account Recovery Request

   Xiaohongshu Support Team,

   I am requesting recovery of my account @[username].

   Account Details:
   - Username: @[username]
   - Display Name: [name]
   - Account ID: [if available]
   - Created: [approximate date]

   Ownership Evidence:
   1. Original email: [email]
   2. Original phone: [phone number]
   3. Current email: [email]
   4. Current phone: [phone number]
   5. Connected accounts: @[other1], @[other2]
   6. Official website: [URL]

   Security Incident:
   [Describe what happened: hacked, lost access, etc.]

   Attached: [Ownership evidence documentation]

   Please assist in recovering my account.
   I can provide additional verification if needed.

   Contact:
   [Your Name]
   [Email]
   [Phone]

   Thank you,
   [Your Name]"

4. Backup Communication Channels
   Followers Can Reach You If Account Compromised:
   ✅ Secondary Xiaohongshu account (backup account)
   ✅ Other social media (Weibo, Douyin, WeChat)
   ✅ Email list (owned audience)
   ✅ Website/blog (owned platform)

   Announcement Template (If Account Hacked):
   "⚠️ ACCOUNT SECURITY NOTICE ⚠️

    My main account @[username] has been compromised.

    If you receive any suspicious DMs or see unusual posts,
    please know that is NOT me.

    I'm working with Xiaohongshu support to recover the account.

    In the meantime, follow me here for updates:
    - Backup account: @[backupusername]
    - Weibo: @[weibo]
    - WeChat: [ID]

    Thank you for your patience and support.
    I will keep you updated!

    - [Your Name]"

5. Incident Response Plan
   If Account Breached:
   Immediate Actions (First 5 Minutes):
   ✅ Change password (if still have access)
   ✅ Enable 2FA (if not already enabled)
   ✅ Check connected apps (revoke all)
   ✅ Check active sessions (terminate all except yours)
   ✅ Contact Xiaohongshu support (report breach)

   Document Breach:
   ✅ Screenshot suspicious activity
   ✅ Note timeline (when first noticed)
   ✅ List what attacker did (posts, DMs, changes)
   ✅ Preserve evidence (don't delete attacker's posts yet)

   Communication:
   ✅ Inform team members (if applicable)
   ✅ Post announcement (if account accessible)
   ✅ Communicate via backup channels (if locked out)

   Follow-Up:
   ✅ Work with Xiaohongshu support
   ✅ Provide ownership evidence
   ✅ Secure account once recovered (change password, enable 2FA)
   ✅ Review and update security (prevent future breaches)
   ✅ Inform followers (account recovered, what to expect)
```

## Common Mistakes

| Mistake | Why Happens | Fix |
|---------|-------------|-----|
| Weak password (easy to guess) | Want memorable password | Use password manager, generate random strong password |
| No 2FA enabled | Don't think will be hacked | Enable 2FA immediately (critical security layer) |
| Sharing password with too many people | Convenient for team | Use individual logins, minimize shared access |
| Using public WiFi for login | Convenient, free data | Use cellular data or VPN, never use public WiFi |
| Not monitoring login activity | Don't think to check | Review login history weekly, remove unrecognized devices |
| Not having recovery plan | Think won't need it | Document ownership evidence before breach happens |
| Not revoking access for former team members | Forget or don't think matters | Change password immediately when team member leaves |
| Clicking phishing links | Looks legitimate | Verify URL, never click suspicious links in DMs/emails |

## Real-World Impact

**Case Study: Account Security Recovery**
- **Before**: Weak password "12345678", no 2FA, logged in on public WiFi, account stolen (500k followers lost)
- **After**: Implemented security (strong password, 2FA, secure access only), recovered account with ownership evidence
- **Result**: Account recovered in 7 days, zero security breaches since, peace of mind

**Data-Backed Insights**:
- 60% of account thefts could be prevented with strong password + 2FA
- Accounts without 2FA are 10x more likely to be compromised
- Public WiFi use accounts for 30% of account breaches
- 80% of users who don't monitor login activity don't realize they're hacked for days/weeks
- Recovery success rate: 90% when ownership evidence documented, 20% without
- Average time to recover hacked account: 7-14 days (with proper evidence)
- Team access accounts are 3x more likely to be breached than personal accounts
- Password reuse is #1 cause of account breaches (data breaches on other sites)

## Related Skills

**REQUIRED**: Use violation-handling (respond if account used for policy violations)
**REQUIRED**: Use account-authentication (verified accounts get priority support for recovery)

**Recommended for account security**:
- **private-domain** (build owned audience as backup)
- **content-calendar** (document content library for ownership evidence)
- **team-management** (manage team access securely)
- **crisis-management** (respond to account breach publicly)

**Use account-security WITH**:
- account-authentication (protect verified status with security)
- violation-handling (secure account prevents policy violations from attackers)
- private-domain (backup channels if account compromised)
