---
name: publisher
version: 1.1.2
description: Publish HTML frontend projects to the PushWebly publishing platform, list published projects, obtain shareable project URLs, change a published app's public/private visibility, and package published HTML projects into Android APKs. Use when Codex needs to publish a local zip project, publish and build an APK, build an APK for an existing published project, toggle an app between public and private, list a user's published projects, or log in/register for this publishing platform. Codex should use HTTP APIs with curl when remote MCP tools are not mounted.
---

# Publisher Skill

Publish HTML frontend projects to the publishing platform and optionally package
them as Android APKs.

Platform URL:

```text
https://pushwebly.com
```

Use "project" in user-facing messages. The canonical API paths are
`/api/projects` and canonical tool names are `project_*`. Deprecated `game_*`
aliases and `gameId` response fields may still appear; treat `gameId` as the
project id.

## Codex Execution Rules

- Prefer mounted `project_*` MCP tools if they exist in the current environment.
- If remote MCP tools are not mounted, use the HTTP APIs with `curl`.
- Do not require Python. Optional scripts, if present, are for CLI/CI users only.
- Ask only for genuinely missing information: credentials, zip path, project
  name, public/private visibility, or private access password preference.
- Never write credentials into a project zip or repository file. Store them only
  in the user's local `~/.publisher/config.json` after consent.
- On Windows/PowerShell, use a temp JSON file for request bodies instead of
  shell-escaping inline JSON.

## Intent Mapping

| User intent | Action | Missing information to ask for |
|---|---|---|
| Publish, ship, upload, put online | Publish project | zip path, project name |
| Make an installable phone app, APK, Android package | Publish and build APK | zip path, project name |
| Build APK for an already published project | Build APK | project id; use project list if needed |
| Make an app private/public, add/remove access password | Change visibility | app URL, target visibility (optional password when private) |
| Show my projects, list published projects | List projects | none if token is available |
| Log in, register, account setup | Login/register | username and password |

If the intent is ambiguous, ask one short question: "Just publish it, or publish
it and build an Android APK too?"

## Publishing Conversation Process

When users express intentions such as publishing, deploying, launching, sharing applications, generating access links, etc., they must enter this process. 

<HARD-GATE>
The publishing process is a blocking finite-state machine. As long as the current step lacks user input, the model must stop advancing, only pose one question for the current step, and wait for the user's response. 
Guessing answers based on context is prohibited.
Automatic selection of public/private is prohibited. 
Automatic generation of access passwords is prohibited, unless the user explicitly chooses to have the system generate them. 
It is prohibited to call the release interface before completing all necessary steps. 
Each response can contain at most one user-facing question. 
</HARD-GATE>

### General Principles of Finite-State Machine

- On entering the flow, first run `S-1` (version check, non-blocking), then proceed in the order of `S0 -> S1 -> S2 -> S3 -> S4`.
- Skipping steps is not allowed (except `S-1`).
- Multiple fields cannot be queried in a single request.
Information that the user has clearly provided can be recorded, and there is no need to ask repeatedly. 
When the user's response is ambiguous, only follow up once for the current field. 
- Only after the current step is completed can we proceed to the next step.
- If waiting for user input is required, do not append explanations, suggestions, or previews of the next step at the end of the response.

---

### S-1: Version Check (first node of the publish flow, non-blocking)

When entering the publish flow, run a version self-check **before** `S0`. This step is **NOT part of the `<HARD-GATE>` blocking rules**: whatever the result — even if the endpoint is unreachable — always continue. Never interrupt publishing because of a version issue.

Steps:

1. Read the local skill version: the `version` field in this file's frontmatter.
2. Query the latest platform version (**no login required**):

   ```bash
   curl -s https://ai-pub.pushwebly.com/api/skill/latest-version
   ```

   The response `data` contains: `version` (latest), `downloadUrl` (cross-platform doc package, unzip-and-use), `downloadUrlWindows` (Windows installer .exe), and `downloadUrlMac` (macOS installer .zip).

3. Compare local `version` with the returned `version`.

   **Comparison rule**: a version is `major.minor.patch`. Compare **segment by segment as integers, left to right** — major first, then minor, then patch; pad missing segments with 0 (`1.1` means `1.1.0`). Compare as integers, NOT as strings: `1.10.0` is **greater than** `1.9.0` (second segment `10 > 9`); a string compare would get this wrong. Ascending example: `1.0.0 < 1.0.9 < 1.1.0 < 1.2.0 < 1.10.0 < 2.0.0`.

   - Local is **older** (local's integer-segment sequence is less than the returned one): you **MUST** output an update notice to the user before continuing, **and the notice MUST include the actual download URL** (this does not block publishing, but the notice must not be omitted). **Pick the download URL by the user's OS**:

     - Windows → use `downloadUrlWindows`
     - macOS → use `downloadUrlMac`
     - OS unknown, or the matching field is empty → fall back to the generic `downloadUrl`

     Notice text (**output it in the SAME language the user is conversing in** — Chinese if they write Chinese, English if English; do not hard-code one language; the example below is English only as a template; replace the URL with the real selected one; **write the download URL as a clickable Markdown link `[URL](URL)` — do NOT wrap it in backticks as inline code, or the user cannot click it**; never leave a placeholder, never say "a new version exists" without giving the link):

     > Note: a newer Publisher skill version `<version>` is available (you are on `<local version>`). Download: [https://ai-pub.pushwebly.com/downloads/AI_Publisher_skill.exe](https://ai-pub.pushwebly.com/downloads/AI_Publisher_skill.exe) (updating does not affect the current publish).

   - Local equals or is newer: stay silent and continue.
   - Request fails/times out/cannot parse: **silently skip**, go straight to `S0`, do not surface an error.

4. In all cases, proceed to `S0` next. Because this step only notifies (no input, no blocking), the "at most one user-facing question per reply" rule does not apply to it — the version note may share the same reply as the first `S0` question.

---

### S0: Check Account Status

First, check if there is already an available token/local credential. 

- If you already have account credentials: go to `S2`.
- If there are no account credentials: Enter `S1_USERNAME`.
- If unable to check the account status: ask the user if they already have a publishing account.

Ask the user a question:

> I need to confirm the publishing account first: Do you already have an available account or token?

User answer:
- Yes: Require the user to provide or confirm the token/login credentials, then proceed to `S2`.
- No: Enter `S1_USERNAME`.

---

### S1: Registration and Login Process

#### S1_USERNAME: Collect registered username

If there is no username, only ask: 

> Please provide the username to be registered. 

After receiving the username, record it as `username` and enter `S1_PASSWORD`. 

#### S1_PASSWORD: Collection registration password

If there is no password, only ask: 

>Please provide the registration password.

After receiving the password, record it as `password` and enter `S1_VALIDATE`. 

#### S1_VALIDATE: Joint Validation

Only after having both `username` and `password` can the backend interface be called for joint verification. 

Verification passed:
- Create Account
- Complete Login 
- Prompt: `Registration and login successful`
- Enter `S2`

Verification failed:
- Display the specific error reason returned by the backend 
- Only inquire about the item that needs to be corrected 
- Do not terminate the registration process

---

### S2: Inquire about application visibility

If the public or private status has not been clearly defined, only ask: 

> Is this application public? Public means anyone can access it via a link; private requires a 6-digit access password. 

User answer:
- Public / Yes / public: Record `visibility=public`, enter `S4`
- Private / No / private: Record `visibility=private`, enter `S3`
- Unclear: Continue to ask only about this item

---

### S3: Private Access Password

If `visibility=private`, it is necessary to ask whether to customize the password, asking only: 

> Do you want to customize a 6-digit access password? You can also reply "system-generated". 

User answer:
- Provide password: verification must be 6 digits or letters; after passing, record `accessPassword=<user password>` and enter `S4`
- Reply system-generated / Not required / Random: Do not pass `accessPassword`, let the backend generate it, and enter `S4`
- Password format error: Only prompt for the format requirements and re-ask for the password 

---

### S4: Execute Release

Calling the publishing interface is only allowed if one of the following conditions is met:

- `visibility=public`
- `visibility=private` and the user has selected a custom password or a system-generated password

Release Parameters:

Public Application:

```json
{
  "visibility": "public"
}

Private application, custom password: 
{

Default to `public` if the user does not specify visibility. A private access
password must match `^[A-Za-z0-9]{6}$`; otherwise ask for a valid password or let
the backend generate one.

## Token Handling

A Bearer token is required for all publishing APIs.

Use this order:

1. If the user provided a token in the conversation, use it directly.
2. If `~/.publisher/config.json` exists, read the stored username/password and
   log in again to refresh the token.
3. Otherwise ask for username and password. The login endpoint automatically
   registers new accounts.

Login/register endpoint:

```bash
curl -s -X POST https://ai-pub.pushwebly.com/api/auth/login-or-register \
  -H "Content-Type: application/json" \
  -d @login.json
```

Write `login.json` as:

```json
{"username":"alice","password":"plain-text-password"}
```

Use `data.token` from the response as:

```text
Authorization: Bearer <TOKEN>
```

Delete the temp login file after use.

Optional local credential file:

```json
{
  "baseUrl": "https://ai-pub.pushwebly.com",
  "username": "alice",
  "password": "plain-text-password",
  "authorization": "Bearer <TOKEN>",
  "userId": 1
}
```

On Linux/macOS, set mode `600` after writing. On 401, refresh the token once by
logging in again, then retry the failed operation once.

Verify token:

```bash
curl -s https://ai-pub.pushwebly.com/api/auth/verify-token \
  -H "Authorization: Bearer <TOKEN>"
```

## Pre-Publish Checks

Before publishing:

1. Confirm the file exists and has a `.zip` extension.
2. Confirm the zip contains `index.html` or `index.htm`.
3. If the zip has nested directories, confirm the entry file can be located.
4. Confirm the project name is non-empty.
5. Confirm a valid token is available.

## HTTP Operations

### Publish Project

Public:

```bash
curl -s -X POST https://ai-pub.pushwebly.com/api/projects/publish \
  -H "Authorization: Bearer <TOKEN>" \
  -F "project_name=demo" \
  -F "file=@demo.zip"
```

Private with optional custom password:

```bash
curl -s -X POST https://ai-pub.pushwebly.com/api/projects/publish \
  -H "Authorization: Bearer <TOKEN>" \
  -F "project_name=demo" \
  -F "file=@demo.zip" \
  -F "visibility=private" \
  -F "access_password=a1b2c3"
```

For private apps, omit `access_password` to let the backend generate a password.
Always relay the final `accessPassword` from the response to the user.

### List Projects

```bash
curl -s https://ai-pub.pushwebly.com/api/projects/my \
  -H "Authorization: Bearer <TOKEN>"
```

### Change Visibility (public <-> private)

Toggle an already-published app between public and private. The input is the
**app URL**; the backend parses the app identifier from it and verifies the app
belongs to the current user — **you can only change your own apps, not others'**.

```bash
curl -s -X PATCH https://ai-pub.pushwebly.com/api/projects/visibility \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d @visibility.json
```

Write `visibility.json` (to private):

```json
{"url":"https://ai-pub.pushwebly.com/play/aB3xYz/","visibility":"private","accessPassword":"a1b2c3"}
```

Or to public (no password needed; the old password is cleared):

```json
{"url":"https://ai-pub.pushwebly.com/play/aB3xYz/","visibility":"public"}
```

`accessPassword` is optional and only used when switching to private (6 digits or
letters; auto-generated if omitted). The response `data` includes the final
`visibility`, `url`, and — when private — the `accessPassword`. Relay a private
app's URL and password separately, never with `?pwd=`. If the app is not found,
already deleted, or belongs to another user, state the concrete reason and that
only your own apps can be changed.

### Build APK for Existing Project

```bash
curl -s -X POST https://ai-pub.pushwebly.com/api/apk/build \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d @build-apk.json
```

Write `build-apk.json` as:

```json
{"projectId":12}
```

Use `data.apkUrl` from the response as the APK download URL.

### Publish and Build APK

This is the recommended operation when the user wants an installable Android app.

```bash
curl -s -X POST https://ai-pub.pushwebly.com/api/apk/publish-and-build \
  -H "Authorization: Bearer <TOKEN>" \
  -F "project_name=airplane-war" \
  -F "file=@project.zip"
```

For a private app, add:

```bash
-F "visibility=private" -F "access_password=a1b2c3"
```

Omit `access_password` to auto-generate it.

Expected response fields may include:

```json
{
  "gameId": 12,
  "projectName": "airplane-war",
  "playUrl": "https://ai-pub.pushwebly.com/play/aB3xYz/",
  "status": "enabled",
  "apkUrl": "https://ai-pub.pushwebly.com/api/apk/download/airplane-war_aB3xYz.apk",
  "apkFileName": "airplane-war_aB3xYz.apk",
  "apkFileSize": 2300000
}
```

Read `gameId` as the project id.

## MCP Tool Parameters

If `project_*` tools are mounted, use these canonical parameter shapes.

`project_publish`:

```json
{
  "authorization": "Bearer <TOKEN>",
  "projectName": "project-name",
  "zipFilePath": "server-side local zip path",
  "visibility": "public",
  "accessPassword": ""
}
```

`project_list`:

```json
{"authorization": "Bearer <TOKEN>"}
```

`project_update_visibility`:

```json
{
  "authorization": "Bearer <TOKEN>",
  "url": "https://ai-pub.pushwebly.com/play/aB3xYz/",
  "visibility": "private",
  "accessPassword": "a1b2c3"
}
```

`project_build_apk`:

```json
{
  "authorization": "Bearer <TOKEN>",
  "projectId": 12
}
```

`project_publish_and_build_apk`:

```json
{
  "authorization": "Bearer <TOKEN>",
  "projectName": "project-name",
  "zipFilePath": "server-side local zip path",
  "visibility": "public",
  "accessPassword": ""
}
```

## User Reply Formats

Publish only, public:

```text
Project published successfully.

Project name: <projectName>
Access URL: <url>
Visibility: public
Status: enabled
```

Publish only, private:

```text
Private project published successfully.

Project name: <projectName>
Access URL: <url>
Access password: <accessPassword>
Visibility: private

Share the URL and the access password separately. The recipient opens the URL and enters the password on the page. Do not append the password to the URL.
```

Publish and build APK:

```text
Project published successfully.

Project name: <projectName>
Access URL: <playUrl>
APK download: <apkUrl>
```

Build APK only:

```text
APK build complete.

Project name: <projectName>
APK download: <apkUrl>
```

On failure, state the concrete reason and the next retry action. Common reasons:
missing `index.html`/`index.htm`, invalid or expired token, missing zip file,
empty project name, invalid private password, APK timeout, or server missing
Android SDK configuration.

## Notes

- Private apps are opened by entering the password on the access page; share the
  clean URL and the password separately, never appended together. (The backend
  still accepts `?pwd=<password>`, but do not promote that suffixed-link form.)
  After successful entry, the browser stores a cookie.
- APK builds usually take about 1-3 minutes.
- Duplicate APK build requests during an active build are deduplicated.
- Each APK has a unique package name: `com.pushwebly.g{playToken}`.
- Use `project_publish_and_build_apk` for one-step publish plus APK generation.
