---
name: fast-io
description: >-
  Cloud file management and collaboration platform. Complete agent guide with
  all 14 consolidated tools using action-based routing — parameters, workflows,
  ID formats, and constraints. Use this skill when the user needs to store
  files, create branded shares (Send/Receive/Exchange), or query documents
  using built-in RAG AI. Supports transferring ownership to humans, managing
  workspaces, and real-time collaboration. Provides a free agent plan with
  50 GB storage and 5,000 monthly credits.
license: Proprietary
compatibility: >-
  Requires network access. Connects to the Fast.io MCP server at mcp.fast.io
  via Streamable HTTP (/mcp) or SSE (/sse).
metadata:
  author: fast-io
  version: "1.43.0"
homepage: "https://fast.io"
---

# Fast.io MCP Server -- AI Agent Guide

**Version:** 1.43
**Last Updated:** 2026-02-09

The definitive guide for AI agents using the Fast.io MCP server. Covers why and how to use the platform: product capabilities, the free agent plan, authentication, core concepts (workspaces, shares, intelligence, previews, comments, URL import, ownership transfer), 10 end-to-end workflows, and all 14 consolidated tools with action-based routing.

> **Versioned guide.** This guide is versioned and updated with each server release. The version number at the top of this document tracks tool parameters, ID formats, and API behavior changes. If you encounter unexpected errors, the guide version may have changed since you last read it.

> **Platform reference.** For a comprehensive overview of Fast.io's capabilities, the agent plan, key workflows, and upgrade paths, see [references/REFERENCE.md](references/REFERENCE.md).

---

## 1. Overview

**Store files. Share with humans. Query with AI. All through one API -- free.**

Fast.io is a cloud storage and collaboration platform that gives AI agents a complete file management, sharing, and intelligence layer. Upload outputs, create branded data rooms, ask questions about documents using built-in RAG, and hand everything off to a human when the job is done. No infrastructure to manage, no subscriptions to set up, no credit card required.

### The Problem Fast.io Solves

AI agents generate files, reports, datasets, and deliverables -- but getting those outputs to humans is messy. You end up cobbling together S3 buckets, presigned URLs, email attachments, and custom download pages. Every agent reinvents file sharing, and none of it looks professional.

When agents need to *understand* documents -- not just store them -- they have to download files, parse dozens of formats, build search indexes, and manage their own RAG pipeline. That is a lot of infrastructure for what should be a simple question: "What does this document say?"

| Problem | Fast.io Solution |
|---------|-----------------|
| Nowhere professional to put agent outputs | Branded workspaces and data rooms with file preview for 10+ formats |
| Sharing files with humans is awkward | Purpose-built shares (Send, Receive, Exchange) with link sharing, passwords, expiration |
| Collecting files from humans is harder | Receive shares let humans upload directly to you -- no email attachments |
| Understanding document contents | Built-in AI reads, summarizes, and answers questions about your files |
| Building a RAG pipeline from scratch | Enable intelligence on a workspace and files are automatically indexed, summarized, and queryable |
| Finding the right file in a large collection | Semantic search finds files by meaning, not just filename |
| Handing a project off to a human | One-click ownership transfer -- human gets the org, agent keeps admin access |
| Tracking what happened | Full audit trail with AI-powered activity summaries |
| Cost | Free. 50 GB storage, 5,000 monthly credits, no credit card |

### MCP Server

This MCP server exposes 14 consolidated tools that cover the full Fast.io REST API surface. Every authenticated API endpoint has a corresponding tool action, and the server handles session management automatically.

Once a user authenticates, the auth token is stored in the server session and automatically attached to all subsequent API calls. There is no need to pass tokens between tool invocations.

### Server Endpoints

- **Production:** `mcp.fast.io`
- **Development:** `mcp.fastdev1.com`

Two transports are available on each:

- **Streamable HTTP at `/mcp`** -- the preferred transport for new integrations.
- **SSE at `/sse`** -- a legacy transport maintained for backward compatibility.

### MCP Resources

The server exposes two MCP resources that clients can read directly via `resources/list` and `resources/read`:

| URI | Name | Description | MIME Type |
|-----|------|-------------|-----------|
| `skill://guide` | skill-guide | Full agent guide (this document) with all 14 tools, workflows, and platform documentation | `text/markdown` |
| `session://status` | session-status | Current authentication state: `authenticated` boolean, `user_id`, `user_email`, `token_expires_at` (Unix epoch), `token_expires_at_iso` (ISO 8601) | `application/json` |

### MCP Prompts

The server provides 5 guided prompts for complex, multi-step operations via `prompts/list` and `prompts/get`:

| Prompt | Description |
|--------|-------------|
| `get-started` | Complete onboarding: create account, org, and workspace. Covers new agents, returning users, API key auth, browser login (PKCE), and invited agents. |
| `add-file` | Add a file from text content, binary upload (with blob staging), or URL import (Google Drive, OneDrive, Dropbox). Helps choose the right method. |
| `ask-ai` | Guide for AI chat. Explains scoping (folder/file scope vs attachments), intelligence requirements, polling. |
| `comment-conversation` | Agent-human collaboration via comments on files. Read/write anchored comments (image regions, video timestamps, PDF pages), reply in threads, react with emoji, and construct deep-link URLs so humans land directly on the conversation. |
| `catch-up` | Understand what happened. AI-powered activity summaries, event search with filters, real-time change monitoring with activity-poll, and the polling loop pattern. |

### Additional References

- **Agent guide (this file):** `/skill.md` on the MCP server -- tool documentation, workflows, and constraints.
- **REST API reference:** `https://api.fast.io/llms.txt` -- endpoint documentation for the underlying Fast.io API.
- **Platform guide:** `https://fast.io/agents.md` -- capabilities, agent plan details, key workflows, and upgrade paths.

---

## 2. Authentication (Critical First Step)

Authentication is required before calling any tool except these unauthenticated tools:

- `auth` with actions: `signin`, `signup`, `set-api-key`, `pkce-login`, `email-check`, `password-reset-request`, `password-reset`
- `download` with action: `quickshare-details`

### Choosing the Right Approach

There are three ways to use Fast.io as an agent, depending on whether you are operating autonomously or assisting an existing human user.

**Option 1: Autonomous Agent -- Create an Agent Account**

If you are operating independently (storing files, running workflows, building workspaces for users), create your own agent account with `auth` action `signup`. Agent accounts get the free agent plan (50 GB, 5,000 monthly credits) and can transfer orgs to humans when ready. This is the recommended path for autonomous agents. See **Agent Account Creation** below for steps.

**Option 2: Assisting a Human -- Use Their API Key**

If a human already has a Fast.io account and wants your help managing their files, workspaces, or shares, they can create an API key for you to use. No separate agent account is needed -- you operate as the human user. The human creates a key at Settings -> Devices & Agents -> API Keys (direct link: `https://go.fast.io/settings/api-keys`). Call `auth` with action `set-api-key` and the key to authenticate -- the key is validated and stored in the session automatically. API keys are a 1:1 replacement for JWT tokens: they work as Bearer tokens with the same permissions as the account owner and do not expire unless revoked. Agents can also manage API keys programmatically with `auth` actions `api-key-create`, `api-key-list`, and `api-key-delete`.

**Option 3: Agent Account Invited to a Human's Org**

If you want your own agent identity but need to work within a human's existing organization, create an agent account with `auth` action `signup`, then have the human invite you to their org with `member` action `add` (entity_type `org`) or to a workspace with `member` action `add` (entity_type `workspace`). Alternatively the human can invite via the UI: Settings -> Your Organization -> Manage People. This gives you access to their workspaces and shares while keeping your own account separate. After accepting invitations with `user` action `accept-all-invitations`, use `auth` action `signin` to authenticate normally. **Note:** If the human only invites you to a workspace (not the org), the org will appear as external -- see **Internal vs External Orgs** in the Organizations section.

**Option 4: Browser Login (PKCE)**

If you prefer not to send a password through the agent, use browser-based PKCE login. Call `auth` action `pkce-login` (optionally with an `email` hint) to get a login URL. The user opens the URL in a browser, signs in (email/password or SSO like Google/Microsoft), and approves access. The browser displays an authorization code which the user copies back to the agent. Call `auth` action `pkce-complete` with the code to finish signing in. This is the most secure option — no credentials pass through the agent.

| Scenario | Recommended Approach |
|----------|---------------------|
| Operating autonomously, storing files, building for users | Create an agent account with your own org (Option 1) |
| Helping a human manage their existing account | Ask the human to create an API key for you (Option 2) |
| Working within a human's org with your own identity | Create an agent account, have the human invite you (Option 3) |
| Building something to hand off to a human | Create an agent account, build it, then transfer the org (Option 1) |
| Signing in without sending a password through the agent | Browser-based PKCE login (Option 4) |

**Credit limits by account type:** Agent accounts (Options 1, 3) can transfer orgs to humans when credits run out -- see Ownership Transfer in section 3. Human accounts (Option 2) cannot use the transfer/claim API; direct the human to upgrade their plan at `https://go.fast.io/settings/billing` or via `org` action `billing-create`.

### Standard Sign-In Flow

1. Call `auth` with action `signin`, `email` and `password`.
2. The server returns a JWT `auth_token` and stores it in the session automatically.
3. All subsequent tool calls use this token without any manual passing.

### Agent Account Creation

When creating a new account (Options 1 and 3 above), agents **MUST** use `auth` action `signup` which automatically registers with `agent=true`. Never sign up as a human account. Agent accounts provide:

- `account_type` set to `"agent"`
- Free agent plan assigned automatically
- Transfer/claim workflow enabled for handing orgs off to humans

**Steps:**

1. Optionally call `auth` action `email-check` with the desired `email` to verify it is available for registration before attempting signup.
2. Call `auth` action `signup` with `first_name`, `last_name`, `email`, and `password`. The `agent=true` flag is sent automatically by the MCP server.
3. The account is created and a session is established automatically -- the agent is signed in immediately.
4. **Verify your email** (required before using most endpoints): Call `auth` action `email-verify` with `email` to send a verification code, then call `auth` action `email-verify` again with `email` and `email_token` to validate the code.
5. No credit card is required. No trial period. No expiration. The account persists indefinitely.

### Two-Factor Authentication Flow

1. Call `auth` action `signin` with `email` and `password`.
2. If the response includes `two_factor_required: true`, the returned token has limited scope.
3. Call `auth` action `2fa-verify` with the 2FA `code` (TOTP, SMS, or WhatsApp).
4. The server replaces the limited-scope token with a full-scope token automatically.

### Browser Login (PKCE) Flow

1. Call `auth` action `pkce-login` (optionally with `email` to pre-fill the sign-in form).
2. The tool returns a `login_url` — present it to the user to open in a browser.
3. The user signs in (email/password or SSO) and clicks Approve.
4. The browser displays an authorization code. The user copies it.
5. Call `auth` action `pkce-complete` with the `code` to exchange it for an access token.
6. The session is established automatically — all subsequent tool calls are authenticated.

### Checking Session Status

- `auth` action `status` -- checks the local Durable Object session. No API call is made. Returns authentication state, user ID, email, and token expiry.
- `auth` action `check` -- validates the token against the Fast.io API. Returns the user ID if the token is still valid.

### Session Expiry

JWT tokens last **1 hour**. API keys (used when assisting a human) do not expire unless revoked. When a JWT session expires, tool calls return a clear error indicating that re-authentication is needed. Call `auth` action `signin` again to establish a new session. The MCP server does not auto-refresh tokens.

**Tip:** For long-running sessions, use `auth` action `status` to check remaining token lifetime before starting a multi-step workflow. If the token is close to expiring, re-authenticate first to avoid mid-workflow interruptions.

### Signing Out

Call `auth` action `signout` to clear the stored session from the Durable Object.

---

## 3. Core Concepts

### Organizations

Organizations are the top-level container in Fast.io. Every user belongs to one or more organizations. Organizations have:

- **Members** with roles: owner, admin, member, guest, view.
- **Billing and subscriptions** managed through Stripe integration.
- **Workspaces** that belong to the organization.
- **Plan limits** that govern storage, transfer, AI tokens, and member counts.

Organizations are identified by a 19-digit numeric profile ID or a domain string.

**IMPORTANT:** When creating orgs, agents MUST use `org` action `create` which automatically assigns `billing_plan: "agent"`. This ensures the org gets the free agent plan (50 GB, 5,000 credits/month). Do not use any other billing plan for agent-created organizations.

#### Org Discovery (IMPORTANT)

To discover all available orgs, agents **must call both actions**:

1. `org` action `list` -- returns internal orgs where you are a direct member (`member: true`)
2. `org` action `discover-external` -- returns external orgs you access via workspace membership only (`member: false`)

**An agent that only checks `org` action `list` will miss external orgs entirely and won't discover the workspaces it's been invited to.** External orgs are the most common pattern when a human invites an agent to help with a specific project -- they add the agent to a workspace but not to the org itself.

#### Internal vs External Orgs

**Internal orgs** (`member: true`) -- orgs you created or were invited to join as a member. You have org-level access: you can see all workspaces (subject to permissions), manage settings if you're an admin, and appear in the org's member list.

**External orgs** (`member: false`) -- orgs you can access only through workspace membership. You can see the org's name and basic public info, but you cannot manage org settings, see other workspaces, or add members at the org level. Your access is limited to the specific workspaces you were explicitly invited to.

**Example:** A human invites your agent to their "Q4 Reports" workspace. You can upload files, run AI queries, and collaborate in that workspace. But you cannot create new workspaces in their org, view their billing, or access their other workspaces. The org shows up via `org` action `discover-external` -- not `org` action `list`. If the human later invites you to the org itself, the org moves from external to internal.

### Workspaces

Workspaces are file storage containers within organizations. Each workspace has:

- Its own set of **members** with roles (owner, admin, member, guest).
- A **storage tree** of files and folders (storage nodes).
- Optional **AI features** for RAG-powered chat.
- **Shares** that can be created within the workspace.
- **Archive/unarchive** lifecycle management.
- **50 GB included storage** on the free agent plan, with files up to 1 GB per upload.
- **File versioning** -- every edit creates a new version, old versions are recoverable.
- **Full-text and semantic search** -- find files by name, content, or meaning.

Workspaces are identified by a 19-digit numeric profile ID.

#### Intelligence: On or Off

Workspaces have an **intelligence** toggle that controls whether AI features are active:

**Intelligence OFF** -- the workspace is pure file storage. You can still attach files directly to an AI chat conversation (up to 20 files, 200 MB total), but files are not persistently indexed. This is fine for simple storage and sharing where you do not need to query your content.

**Intelligence ON** -- the workspace becomes an AI-powered knowledge base. Every file uploaded is automatically ingested, summarized, and indexed. This enables:

- **RAG (retrieval-augmented generation)** -- scope AI chat to entire folders or the full workspace and ask questions across all your content. The AI retrieves relevant passages and answers with citations.
- **Semantic search** -- find files by meaning, not just keywords. "Show me contracts with indemnity clauses" works even if those exact words do not appear in the filename.
- **Auto-summarization** -- short and long summaries generated for every file, searchable and visible in the UI.
- **Metadata extraction** -- AI pulls key metadata from documents automatically.

Intelligence defaults to ON for workspaces created via the API by agent accounts. If you are just using Fast.io for storage and sharing, disable it to conserve credits. If you need to query your content, leave it enabled.

**Agent use case:** Create a workspace per project or client. Enable intelligence if you need to query the content later. Upload reports, datasets, and deliverables. Invite the human stakeholders. Everything is organized, searchable, and versioned.

For full details on AI chat types, file context modes, AI state, and how intelligence affects them, see the **AI Chat** section below.

### Shares

Shares are purpose-built spaces for exchanging files with people outside your workspace. They can exist within workspaces and have three types:

| Mode | What It Does | Agent Use Case |
|------|-------------|----------------|
| **Send** | Recipients can download files | Deliver reports, exports, generated content |
| **Receive** | Recipients can upload files | Collect documents, datasets, user submissions |
| **Exchange** | Both upload and download | Collaborative workflows, review cycles |

#### Share Features

- **Password protection** -- require a password for link access
- **Expiration dates** -- shares auto-expire after a set period
- **Download controls** -- enable or disable file downloads
- **Access levels** -- Members Only, Org Members, Registered Users, or Public (anyone with the link)
- **Custom branding** -- background images, gradient colors, accent colors, logos
- **Post-download messaging** -- show custom messages and links after download
- **Up to 3 custom links** per share for context or calls-to-action
- **Guest chat** -- let share recipients ask questions in real-time
- **AI-powered auto-titling** -- shares automatically generate smart titles from their contents
- **Activity notifications** -- get notified when files are sent or received
- **Comment controls** -- configure who can see and post comments (owners, guests, or both)

#### Two Storage Modes

When creating a share with `share` action `create`, the `storage_mode` parameter determines how files are stored:

- **`room`** (independent storage, default) -- The share has its own isolated storage. Files are added directly to the share and are independent of any workspace. This creates a self-contained data room -- changes to workspace files do not affect the room, and vice versa. Use for final deliverables, compliance packages, archived reports, or any scenario where you want an immutable snapshot.

- **`shared_folder`** (workspace-backed) -- The share is backed by a specific folder in a workspace. The share displays the live contents of that folder -- any files added, updated, or removed in the workspace folder are immediately reflected in the share. No file duplication, so no extra storage cost. To create a shared folder, pass `storage_mode=shared_folder` and `folder_node_id={folder_opaque_id}` when creating the share. **Note:** Expiration dates are not allowed on shared folder shares since the content is live.

Both modes look the same to share recipients -- a branded data room with file preview, download controls, and all share features. The difference is whether the content is a snapshot (room) or a live view (shared folder).

Shares are identified by a 19-digit numeric profile ID.

**Agent use case:** Generate a quarterly report, create a Send share with your client's branding, set a 30-day expiration, and share the link. The client sees a professional, branded page with instant file preview -- not a raw download link.

### Storage Nodes

Files and folders are represented as storage nodes. Each node has an opaque ID (a 30-character alphanumeric string, displayed with hyphens, e.g. `f3jm5-zqzfx-pxdr2-dx8z5-bvnb3-rpjfm4`). The special value `root` refers to the root folder of a workspace or share, and `trash` refers to the trash folder.

Key operations on storage nodes: list, create-folder, move, copy, rename, delete (moves to trash), purge (permanently deletes), restore (recovers from trash), search, add-file (link an upload), and add-link (create a share reference).

Nodes have versions. Each file modification creates a new version. Version history can be listed and files can be restored to previous versions.

### Notes

Notes are a storage node type (alongside files and folders) that store markdown content directly on the server. They live in the same folder hierarchy as files, are versioned like any other node, and appear in storage listings with `type: "note"`.

#### Creating and Updating Notes

Create notes with `workspace` action `create-note` and update with `workspace` action `update-note`.

**Creating:** Provide `workspace_id`, `parent_id` (folder opaque ID or `"root"`), `name` (must end in `.md`, max 100 characters), and `content` (markdown text, max 100 KB).

**Updating:** Provide `workspace_id`, `node_id`, and at least one of `name` (must end in `.md`) or `content` (max 100 KB).

| Constraint | Limit |
|------------|-------|
| Content size | 100 KB max |
| Filename | 1-100 characters, must end in `.md` |
| Markdown validation | Code blocks and emphasis markers must be balanced |
| Rate limit | 2 per 10s, 5 per 60s |

#### Notes as Long-Term Knowledge Grounding

In an intelligent workspace, notes are automatically ingested and indexed just like uploaded files. This makes notes a way to bank knowledge over time -- any facts, context, or decisions stored in notes become grounding material for future AI queries.

When an AI chat uses folder scope (or defaults to the entire workspace), notes within that scope are searched alongside files. The AI retrieves relevant passages from notes and cites them in answers.

Key behaviors:

- Notes are ingested for RAG when workspace intelligence is enabled
- Notes within a folder scope are included in scoped queries
- Notes with `ai_state: ready` are searchable via RAG
- Notes can also be attached directly to a chat via `files_attach` (if they have a ready preview)

**Use cases:**

- Store project context, decisions, and rationale. Months later, ask "Why did we choose vendor X?" and the AI retrieves the note.
- Save research findings in a note. Future AI chats automatically use those findings as grounding.
- Create reference documents (style guides, naming conventions) that inform all future AI queries in the workspace.

#### Other Note Operations

Notes support the same storage operations as files and folders: move (via `storage` action `move`), copy (`storage` action `copy`), delete/trash (`storage` action `delete`), restore (`storage` action `restore`), version history (`storage` action `version-list`), and details (`storage` action `details`).

#### Linking Users to Notes

- **Note in workspace context** (opens workspace with note panel): `https://{domain}.fast.io/workspace/{folder_name}/storage/root?note={note_id}`
- **Note preview** (standalone view): `https://{domain}.fast.io/workspace/{folder_name}/preview/{note_id}`

### AI Chat

AI chat lets agents ask questions about files stored in workspaces and shares. Two chat types are available, each with different file context options.

**AI chat is read-only.** It can read, analyze, search, and answer questions about file contents, but it cannot modify files, change workspace settings, manage members, or access events. Any action beyond reading file content — uploading, deleting, moving files, changing settings, managing shares, reading events — must be done through the MCP tools directly. Do not attempt to use AI chat as a general-purpose tool for workspace management.

#### Two Chat Types

- **`chat`** — Basic AI conversation with no file context from the workspace index. Use for general questions only.
- **`chat_with_files`** — AI grounded in your files. Two mutually exclusive modes for providing file context:
  - **Folder/file scope (RAG)** — limits the retrieval search space. Requires intelligence enabled; files must be in `ready` AI state.
  - **File attachments** — files read directly by the AI. No intelligence required; files must have a ready preview. Max 20 files, 200 MB total.

Both types augment answers with web knowledge when relevant.

#### File Context: Scope vs Attachments

For `chat_with_files`, choose one of these mutually exclusive approaches:

| Feature | Folder/File Scope (RAG) | File Attachments |
|---------|------------------------|------------------|
| How it works | Limits RAG search space | Files read directly by AI |
| Requires intelligence | Yes | No |
| File readiness requirement | `ai_state: ready` | Ready preview |
| Best for | Many files, knowledge retrieval | Specific files, direct analysis |
| Max references | 100 folder refs (subfolder tree expansion) or 100 file refs | 20 files / 200 MB |
| Default (no scope given) | Entire workspace | N/A |

**Scope parameters** (requires intelligence):

- `folders_scope` — comma-separated `nodeId:depth` pairs (depth 1-10, max 100 subfolder refs). Defines a search boundary — the RAG backend finds files within scoped folders automatically. Just pass folder IDs with depth; do not enumerate individual files. A folder with thousands of files and few subfolders works fine.
- `files_scope` — comma-separated `nodeId:versionId` pairs (max 100). Limits RAG to specific indexed files. Both `nodeId` AND `versionId` are required and must be non-empty — get `versionId` from the file's `version` field in `storage` action `list` or `details` responses.
- **If neither is specified, the default scope is the entire workspace (all indexed files).** This is the recommended default — omit scope parameters unless you specifically need to narrow the search.

**Attachment parameter** (no intelligence required):

- `files_attach` — comma-separated `nodeId:versionId` pairs (max 20, 200 MB total). Both `nodeId` AND `versionId` are required and must be non-empty. Files are read directly, not via RAG.

**Do not** list folder contents and pass individual file IDs as `files_scope` when you mean to search a folder — use `folders_scope` with the folder's nodeId instead. `files_scope` is only for targeting specific known file versions.

`files_scope`/`folders_scope` and `files_attach` are mutually exclusive — sending both will error.

#### Intelligence and AI State

The workspace intelligence toggle (see Workspaces above) controls whether uploaded files are auto-ingested, summarized, and indexed for RAG. When intelligence is enabled, each file has an `ai_state` indicating its readiness:

| State | Meaning |
|-------|---------|
| `disabled` | AI processing disabled for this file |
| `pending` | Queued for processing |
| `in_progress` | Currently being ingested and indexed |
| `ready` | Complete — available for folder/file scope queries |
| `failed` | Processing failed |

Only files with `ai_state: ready` are included in folder/file scope searches. Check file state via `storage` action `details` with `context_type: "workspace"`.

**When to enable intelligence:** You need scoped RAG queries, cross-file search, auto-summarization, or a persistent knowledge base.

**When to disable intelligence:** The workspace is for storage/sharing only, or you only need to analyze specific files via attachments. Saves credits (ingestion costs 10 credits/page, 5 credits/sec for video).

Even with intelligence off, `chat_with_files` with file attachments still works.

#### How to Phrase Questions

**With folder/file scope (RAG):** Write questions likely to match content in indexed files. The AI searches the scope, retrieves passages, and cites them.

- Good: "What are the payment terms in the vendor contracts?"
- Good: "Summarize the key findings from the Q3 analysis reports"
- Bad: "Tell me about these files" — too vague, no specific content to match
- Bad: "What's in this workspace?" — cannot meaningfully search for "everything"

**With file attachments:** Be direct — the AI reads the full file content. No retrieval step.

- "Describe this image in detail"
- "Extract all dates and amounts from this invoice"
- "Convert this CSV data into a summary table"

**Personality:** The `personality` parameter controls the tone and length of AI responses. Pass it when creating a chat or sending a message:

- `concise` — short, brief answers
- `detailed` — comprehensive answers with context and evidence (default)

Use `concise` when you need a quick fact, a yes/no answer, or a brief summary. Use `detailed` (or omit the parameter) when you need thorough analysis with supporting evidence and citations. The personality can also be overridden per follow-up message.

**Controlling verbosity in questions:** You can also guide verbosity through how you phrase the question itself:

- "In one sentence, what is the main conclusion of this report?"
- "List only the file names that mention GDPR compliance, no explanations"
- "Give me a brief summary — 2-3 bullet points max"

Combining `personality: "concise"` with a direct question produces the shortest answers and uses the fewest AI credits.

#### Chat Parameters

Create a chat with `ai` action `chat-create` (with `context_type: "workspace"`) or `ai` action `chat-create` (with `context_type: "share"`):

- `type` (required) — `chat` or `chat_with_files`
- `query_text` (required for workspace, optional for share) — initial message, 2-12,768 characters
- `personality` (optional) — `concise` or `detailed` (default: `detailed`)
- `privacy` (optional) — `private` or `public` (default: `public`)
- `files_scope` (optional) — `nodeId:versionId,...` (max 100, requires `chat_with_files` + intelligence). Both parts required and non-empty. **Omit to search all files (recommended default).**
- `folders_scope` (optional) — `nodeId:depth,...` (depth 1-10, max 100 subfolder refs, requires `chat_with_files` + intelligence). Folder scope = search boundary, not file enumeration. **Omit to search all files (recommended default).**
- `files_attach` (optional) — `nodeId:versionId,...` (max 20 / 200 MB, both parts required and non-empty, mutually exclusive with scope params)

#### Follow-up Messages

Send follow-ups with `ai` action `message-send` (with `context_type: "workspace"` or `"share"`). The chat type is inherited from the parent chat. Each follow-up can update the scope, attachment, and personality parameters.

#### Waiting for AI Responses

After creating a chat or sending a message, the AI response is asynchronous. Message states progress: `ready` → `in_progress` → `complete` (or `errored`).

**Recommended:** Call `ai` action `message-read` (with `context_type: "workspace"` or `"share"`) with the returned `message_id`. The tool polls automatically (up to 15 attempts, 2-second intervals, ~30 seconds). If the response is still processing after that window, use `event` action `activity-poll` with the workspace/share ID instead of calling the read action in a loop — see Activity Polling in section 7.

#### Response Citations

Completed AI responses include citations pointing to source files:

- `nodeId` — storage node opaque ID
- `versionId` — file version opaque ID
- `entries[].page` — page number
- `entries[].snippet` — text excerpt
- `entries[].timestamp` — audio/video timestamp

#### Linking Users to AI Chats

Append `?chat={chat_opaque_id}` to the workspace storage URL:

`https://{domain}.fast.io/workspace/{folder_name}/storage/root?chat={chat_id}`

#### Share AI Chats

Shares support AI chat with identical capabilities. All workspace AI endpoints have share equivalents accessible via `ai` actions with `context_type: "share"`.

### AI Share / Export

Generate temporary markdown-formatted download URLs for files that can be pasted into external AI tools (ChatGPT, Claude, etc.). Use `ai` action `share-generate` (with `context_type: "workspace"` or `"share"`). URLs expire after 5 minutes. Limits: 25 files maximum, 50 MB per file, 100 MB total.

### Profile IDs

Organizations, workspaces, and shares are all identified by 19-digit numeric profile IDs. These appear throughout the tool parameters as `workspace_id`, `share_id`, `org_id`, `profile_id`, and `member_id`.

Most endpoints also accept custom names as identifiers:
| Profile Type | Numeric ID | Custom Name |
|-------------|-----------|-------------|
| Workspace | 19-digit ID | Folder name (e.g., `my-project`) |
| Share | 19-digit ID | URL name (e.g., `q4-financials`) |
| Organization | 19-digit ID | Domain name (e.g., `acme`) |
| User | 19-digit ID | Email address (e.g., `user@example.com`) |

### QuickShares

QuickShares are temporary public download links for individual files in workspaces (not available for shares). They can be accessed without authentication. Expires in seconds from creation (default 10,800 = 3 hours, max 86,400 = 24 hours). Max file size: 1 GB. Each quickshare has an opaque identifier used to retrieve metadata and download the file.

### File Preview

Files uploaded to Fast.io get automatic preview generation. When humans open a share or workspace, they see the content immediately -- no "download and open in another app" friction.

Supported preview formats:

- **Images** -- full-resolution with auto-rotation and zoom
- **Video** -- HLS adaptive streaming (50--60% faster load than raw video)
- **Audio** -- interactive waveform visualization
- **PDF** -- page navigation, zoom, text selection
- **Spreadsheets** -- grid navigation with multi-sheet support
- **Code and text** -- syntax highlighting, markdown rendering

Use `storage` action `preview-url` (with `context_type: "workspace"` or `"share"`) to generate preview URLs. Use `storage` action `preview-transform` (with `context_type: "workspace"` or `"share"`) for image resize, crop, and format conversion.

**Agent use case:** Your generated PDF report does not just appear as a download link. The human sees it rendered inline, can flip through pages, zoom in, and comment on specific sections -- all without leaving the browser.

### Comments and Annotations

Humans and agents can leave feedback directly on files, anchored to specific content using the `reference` parameter:

- **Image comments** -- anchored to spatial regions (normalized x/y/width/height coordinates)
- **Video comments** -- anchored to timestamps with spatial region selection
- **Audio comments** -- anchored to timestamps or time ranges
- **PDF comments** -- anchored to specific pages with optional text snippet selection
- **Threaded replies** -- single-level threading only; replies to replies are auto-flattened to the parent
- **Emoji reactions** -- one reaction per user per comment; adding a new reaction replaces the previous one
- **Mention tags** -- reference users and files inline using bracket syntax: `@[profile:id]`, `@[user:opaqueId:Display Name]`, `@[file:fileId:filename.ext]`. Get IDs from member lists, user details, or storage listings. The display name segment is optional for profile tags but recommended for user and file tags

Comments use JSON request bodies (`Content-Type: application/json`), unlike most other endpoints which use form-encoded data.

**Listing comments:** Use `comment` action `list` for per-file comments and `comment` action `list-all` for all comments across a workspace or share. Both support `sort`, `limit` (2-200), `offset`, `include_deleted`, `reference_type` filter, and `include_total`.

**Adding comments:** Use `comment` action `add` with `profile_type`, `profile_id`, `node_id`, and `text`. Optionally include `parent_comment_id` for replies and `reference` to anchor to a specific position. Supports mention tags in the body. Two character limits apply: total body including tags max 8,192 chars, display text (body with `@[...]` tags stripped) max 2,048 chars.

**Deleting comments:** `comment` action `delete` is recursive -- deleting a parent also removes all replies. `comment` action `bulk-delete` is NOT recursive -- replies to deleted comments are preserved.

**Linking users to comments:** The preview URL opens the comments sidebar automatically. Deep link query parameters let you target a specific comment or position:

| Parameter | Format | Purpose |
|-----------|--------|---------|
| `?comment={id}` | Comment opaque ID | Scrolls to and highlights a specific comment for 2 seconds |
| `?t={seconds}` | e.g. `?t=45.5` | Seeks to timestamp for audio/video comments |
| `?p={pageNum}` | e.g. `?p=3` | Navigates to page for PDF comments |

Workspace: `https://{org.domain}.fast.io/workspace/{folder_name}/preview/{file_opaque_id}?comment={comment_id}`

Share: `https://go.fast.io/shared/{custom_name}/{title-slug}/preview/{file_opaque_id}?comment={comment_id}`

Parameters can be combined -- e.g. `?comment={id}&t=45.5` to deep link to a video comment at a specific timestamp. In shares, the comments sidebar only opens if the share has comments enabled.

**Agent use case:** You generate a design mockup. The human comments "Change the header color" on a specific region of the image. You read the comment, see exactly what region they are referring to via the `reference.region` coordinates, and regenerate.

### URL Import

Agents can import files directly from URLs without downloading them locally first. Fast.io's server fetches the file, processes it, and adds it to your workspace or share.

- Supports any HTTP/HTTPS URL
- Supports OAuth-protected sources: **Google Drive, OneDrive, Dropbox**
- Files go through the same processing pipeline (preview generation, AI indexing if intelligence is enabled, virus scanning)

Use `upload` action `web-import` with the source URL, target profile, and parent node ID. Use `upload` action `web-status` to check progress and `upload` action `web-list` to list active import jobs.

**Security note:** The `upload` action `web-import` instructs the **Fast.io cloud server** to fetch the URL -- not the agent's local environment. The Fast.io server is a public cloud service with no access to your local network, internal systems, or private infrastructure. It can only reach publicly accessible URLs and supported OAuth-authenticated cloud storage providers. This is functionally equivalent to the agent downloading a file and re-uploading it; the same data is transferred, just more efficiently since the server handles it directly. No internal or private data is exposed beyond what the agent could already access through its own network requests.

**Agent use case:** A user says "Add this Google Doc to the project." You call `upload` action `web-import` with the URL. Fast.io downloads it server-side, generates previews, indexes it for AI, and it appears in the workspace. No local I/O.

### Ownership Transfer

The primary way agents deliver value: build something, then give it to a human. Also the recommended action when the agent plan runs out of credits and API calls start returning 402 Payment Required -- transfer the org to a human who can upgrade to a paid plan.

**IMPORTANT: Account type restriction.** The transfer/claim workflow (`org` actions `transfer-token-create`, `transfer-token-list`, `transfer-token-delete`, `transfer-claim`) is only available when the agent created an **agent account** (via `auth` action `signup`) and that agent account owns the org. If the agent is signed in with a **human account** (via `auth` action `signin`), the transfer/claim API cannot be used. Human-owned orgs must be upgraded directly by the human through the Fast.io dashboard.

**The flow:**

1. Agent creates an agent account with `auth` action `signup` and an org with `org` action `create`, sets up workspaces with `org` action `create-workspace`, uploads files, configures shares
2. Agent generates a transfer token (valid 72 hours) with `org` action `transfer-token-create`
3. Agent sends the claim URL to the human: `https://go.fast.io/claim?token=<token>`
4. Human clicks the link and claims the org with their account

**When to transfer:**

- The org is ready for human use (workspaces configured, files uploaded, shares set up)
- The agent plan runs out of credits (402 Payment Required) -- transfer so the human can upgrade
- The human explicitly asks to take over the org

**Managing transfer tokens:**

- `org` action `transfer-token-list` -- check for existing pending tokens before creating new ones
- `org` action `transfer-token-delete` -- revoke a token if the transfer is no longer needed
- `org` action `transfer-claim` -- claim an org using a token (used by the receiving human's agent)

**What happens after transfer:**

- Human becomes the owner of the org and all workspaces
- Agent retains admin access (can still manage files and shares)
- Human gets a free plan (credit-based, no trial period)
- Human can upgrade to Pro or Business at any time

**Agent use case:** A user says "Set up a project workspace for my team." You create the org, build out the workspace structure, upload templates, configure shares for client deliverables, invite team members -- then transfer ownership. The human walks into a fully configured platform. You stay on as admin to keep managing things.

**402 Payment Required use case (agent account):** While working, the agent hits credit limits. Call `org` action `transfer-token-create`, send the claim URL to the human, and explain they can upgrade to continue. The agent keeps admin access and resumes work once the human upgrades.

**402 Payment Required use case (human account):** The agent cannot transfer the org. Instead, inform the user that their org has run out of credits and they need to upgrade their billing plan. Direct them to the Fast.io dashboard or use `org` action `billing-create` to update to a paid plan.

### Permission Parameter Values

Several tools use permission parameters with specific allowed values. Use these exact strings when calling the tools.

#### Organization Creation (`org` action `create`)

| Parameter | Allowed Values | Default |
|-----------|----------------|---------|
| `perm_member_manage` | `Owner only`, `Admin or above`, `Member or above` | `Member or above` |
| `industry` | `unspecified`, `technology`, `healthcare`, `financial`, `education`, `manufacturing`, `construction`, `professional`, `media`, `retail`, `real_estate`, `logistics`, `energy`, `automotive`, `agriculture`, `pharmaceutical`, `legal`, `government`, `non_profit`, `insurance`, `telecommunications`, `research`, `entertainment`, `architecture`, `consulting`, `marketing` | `unspecified` |
| `background_mode` | `stretched`, `fixed` | `stretched` |

#### Workspace Creation (`org` action `create-workspace`) and Update (`workspace` action `update`)

| Parameter | Allowed Values | Default |
|-----------|----------------|---------|
| `perm_join` | `Only Org Owners`, `Admin or above`, `Member or above` | `Member or above` |
| `perm_member_manage` | `Admin or above`, `Member or above` | `Member or above` |

#### Share Creation (`share` action `create`)

| Parameter | Allowed Values | Default |
|-----------|----------------|---------|
| `type` | `send`, `receive`, `exchange` | `exchange` |
| `storage_mode` | `independent`, `workspace_folder` | `independent` |
| `access_options` | `Only members of the Share or Workspace`, `Members of the Share, Workspace or Org`, `Anyone with a registered account`, `Anyone with the link` | `Only members of the Share or Workspace` |
| `invite` | `owners`, `guests` | `owners` |
| `notify` | `never`, `notify_on_file_received`, `notify_on_file_sent_or_received` | `never` |
| `display_type` | `list`, `grid` | `grid` |
| `intelligence` | `true`, `false` | `false` |
| `comments_enabled` | `true`, `false` | `true` |
| `download_enabled` | `true`, `false` | `true` |
| `guest_chat_enabled` | `true`, `false` | `false` |
| `workspace_style` | `true`, `false` | `true` |
| `background_image` | `0`-`128` | `0` |

**Share constraints:**

- Receive and Exchange shares cannot use `Anyone with the link` access -- this option is only available for Send shares.
- Password protection (`password` parameter) is only allowed when `access_options` is `Anyone with the link`.
- Expiration (`expires` parameter in MySQL format `YYYY-MM-DD HH:MM:SS`) is not allowed on `workspace_folder` shares.
- `custom_name` must be 10-100 characters, alphanumeric + unicode.
- `title` (or `name`) must be 2-80 characters.
- Color parameters (`accent_color`, `background_color1`, `background_color2`) accept JSON strings.
- `create_folder` creates a new workspace folder for the share when used with `storage_mode='workspace_folder'`.

---

## 4. Agent Plan -- Free Tier

The agent plan is a free tier designed for AI agents. No credit card, no trial period, no expiration. Enough resources to build and demonstrate value, with room to grow when the org transfers to a human on a paid plan.

### Resource Limits

| Resource | Included |
|----------|----------|
| **Price** | $0 -- no credit card, no trial period, no expiration |
| **Storage** | 50 GB |
| **Max file size** | 1 GB |
| **Monthly credits** | 5,000 (resets every 30 days) |
| **Workspaces** | 5 |
| **Shares** | 50 |
| **Members per workspace** | 5 |
| **Share invitations** | 10 per share |
| **Account auto-deletion** | Never |

### Credit Costs

All platform activity consumes credits from the monthly 5,000 allowance:

| Resource | Cost |
|----------|------|
| Storage | 100 credits/GB |
| Bandwidth | 212 credits/GB |
| AI chat tokens | 1 credit per 100 tokens |
| Document pages ingested | 10 credits/page |
| Video ingested | 5 credits/second |
| Audio ingested | 0.5 credits/second |
| Images ingested | 5 credits/image |
| File conversions | 25 credits/conversion |

When credits run out, the org enters a reduced-capability state and API calls return 402 Payment Required. The org is never deleted. Use `org` action `limits` to check current credit usage and remaining balance.

**When you hit 402 or run low on credits:**

- **Agent account (created via `auth` action `signup`):** Transfer the org to the human. Call `org` action `transfer-token-create` to generate a transfer token, then send the human the claim URL: `https://go.fast.io/claim?token=<token>`. Once they claim the org they can upgrade to a paid plan with unlimited credits. You retain admin access and can resume work immediately after the upgrade. This is the expected workflow -- agents build on the free plan, then hand off to humans who pay when they are ready.
- **Human account (signed in via `auth` action `signin`):** You cannot use the transfer/claim API. Tell the user they need to upgrade the org's billing plan directly. They can do this from the Fast.io dashboard or by calling `org` action `billing-create` to update their subscription to a paid plan.

### After Transfer -- Human Plan Options

Once an agent transfers an org to a human, the human gets a free plan (credit-based, no trial period) and can upgrade:

| Feature | Agent (Free) | Free (Human) | Pro | Business |
|---------|-------------|--------------|-----|----------|
| Monthly credits | 5,000 | 5,000 | Unlimited | Unlimited |
| Storage | 50 GB | 50 GB | 1 TB | 5 TB |
| Max file size | 1 GB | 1 GB | 25 GB | 50 GB |
| Workspaces | 5 | 5 | 10 | 1,000 |
| Shares | 50 | 50 | 1,000 | 50,000 |

The transfer flow is the primary way agents deliver value: set everything up on the free agent plan, then hand it off. The human upgrades when they are ready, and the agent retains admin access to keep managing things.

---

## 5. Tool Categories

The 14 tools use action-based routing. Each tool covers a specific area of the Fast.io platform and exposes multiple actions.

### auth

Authentication, sign-in/sign-up, two-factor authentication, API key management, and OAuth session management. This is always the starting point for any agent interaction.

**Actions:** signin, signout, signup, check, session, status, set-api-key, email-check, email-verify, password-reset-request, password-reset, 2fa-verify, 2fa-status, 2fa-enable, 2fa-disable, 2fa-send, 2fa-verify-setup, pkce-login, pkce-complete, api-key-create, api-key-list, api-key-get, api-key-delete, oauth-list, oauth-details, oauth-revoke, oauth-revoke-all

### user

Retrieve and update the current user profile, search for other users, manage invitations, upload and delete user assets (profile photos), check account eligibility, and list shares the user belongs to.

**Actions:** me, update, search, close, details-by-id, profiles, allowed, org-limits, list-shares, invitation-list, invitation-details, accept-all-invitations, asset-upload, asset-delete, asset-types, asset-list

### org

Organization CRUD, member management, billing and subscription operations, workspace creation, invitation workflows, asset management (upload, delete), organization discovery, and ownership transfer.

**Actions:** list, details, create, update, close, public-details, limits, list-workspaces, list-shares, create-workspace, billing-plans, billing-create, billing-cancel, billing-details, billing-activate, billing-reset, billing-members, billing-meters, members, invite-member, remove-member, update-member-role, member-details, leave, transfer-ownership, join, invitations-list, invitation-update, invitation-delete, transfer-token-create, transfer-token-list, transfer-token-delete, transfer-claim, discover-all, discover-available, discover-check-domain, discover-external, asset-upload, asset-delete, asset-types, asset-list

### workspace

Workspace-level settings, lifecycle operations (update, delete, archive, unarchive), listing and importing shares, managing workspace assets, workspace discovery, notes (create, update), and quickshare management.

**Actions:** list, details, update, delete, archive, unarchive, members, list-shares, import-share, available, check-name, create-note, update-note, quickshare-get, quickshare-delete, quickshares-list

### share

Share CRUD, public details, archiving, password authentication, asset management, and share name availability checks.

**Actions:** list, details, create, update, delete, public-details, archive, unarchive, password-auth, members, available, check-name, quickshare-create

### storage

File and folder operations within workspaces and shares. List, create folders, move, copy, delete, rename, purge, restore, search, add files from uploads, add share links, transfer nodes, manage trash, version operations, file locking, and preview/transform URL generation. Requires `context_type` parameter (`workspace` or `share`).

**Actions:** list, details, search, trash-list, create-folder, copy, move, delete, rename, purge, restore, add-file, add-link, transfer, version-list, version-restore, lock-acquire, lock-status, lock-release, preview-url, preview-transform

### upload

File upload operations. Single-step text file upload, chunked upload lifecycle (create session, upload chunks as plain text, staged binary blobs, or legacy base64, finalize, check status, cancel), web imports from external URLs, upload limits and file extension restrictions, and session management.

**Actions:** create-session, chunk, finalize, status, cancel, list-sessions, cancel-all, chunk-status, chunk-delete, text-file, web-import, web-list, web-cancel, web-status, limits, extensions

### download

Generate download URLs and ZIP archive URLs for workspace files, share files, and quickshare links. MCP tools cannot stream binary data -- these actions return URLs that can be opened in a browser or passed to download utilities. Requires `context_type` parameter (`workspace` or `share`) for file-url and zip-url actions.

**Actions:** file-url, zip-url, quickshare-details

### ai

AI-powered chat with RAG in workspaces and shares. Create chats, send messages, read AI responses (with polling), list and manage chats, publish private chats, generate AI share markdown, track AI token usage, and auto-title generation. Requires `context_type` parameter (`workspace` or `share`).

**Actions:** chat-create, chat-list, chat-details, chat-update, chat-delete, chat-publish, message-send, message-list, message-details, message-read, share-generate, transactions, autotitle

### comment

Comments are scoped to `{entity_type}/{parent_id}/{node_id}` where entity_type is `workspace` or `share`, parent_id is the 19-digit profile ID, and node_id is the storage node opaque ID. List comments on files (per-node and profile-wide with sort/limit/offset/filter params), add comments with optional reference anchoring (image regions, video/audio timestamps, PDF pages with text selection), single-level threaded replies, recursive single delete, non-recursive bulk delete, get comment details, and emoji reactions (one per user per comment). Comments use JSON request bodies.

**Actions:** list, list-all, add, delete, bulk-delete, details, reaction-add, reaction-remove

### event

Search the audit/event log with rich filtering, get AI-powered summaries of activity, retrieve full details for individual events, list recent activity, and long-poll for activity changes.

**Actions:** search, summarize, details, activity-list, activity-poll

### member

Member management for organizations, workspaces, and shares. Add, remove, update roles, transfer ownership, leave, join, and join via invitation. Requires `entity_type` parameter (`workspace` or `share`).

**Actions:** add, remove, details, update, transfer-ownership, leave, join, join-invitation

### invitation

Invitation management for organizations, workspaces, and shares. List invitations, list by state, update, and delete. Requires `entity_type` parameter (`workspace` or `share`).

**Actions:** list, list-by-state, update, delete

### asset

Asset management (upload, delete, list, read) for organizations, workspaces, shares, and users. Requires `entity_type` parameter (`org`, `workspace`, `share`, or `user`).

**Actions:** upload, delete, types, list, read

---

## 6. Common Workflows

### 1. Create an Account and Sign In

See **Choosing the Right Approach** in section 2 for which option fits your scenario.

**Option 1 -- Autonomous agent (new account):**

1. Optionally call `auth` action `email-check` with the desired `email` to verify availability.
2. `auth` action `signup` with `first_name`, `last_name`, `email`, and `password` -- registers as an agent account (agent=true is sent automatically) and signs in immediately.
3. `auth` action `email-verify` with `email` -- sends a verification code. Then `auth` action `email-verify` with `email` and `email_token` -- validates the code. Required before using most endpoints.
4. `org` action `create` to create a new org on the agent plan, or `org` action `list` to check existing orgs.

**Option 2 -- Assisting a human (API key):**

1. The human creates an API key at `https://go.fast.io/settings/api-keys` and provides it to the agent.
2. Call `auth` action `set-api-key` with the API key. The key is validated against the API and stored in the session -- all subsequent tool calls are authenticated automatically. No account creation needed.
3. `org` action `list` and `org` action `discover-external` to discover all available organizations (see **Org Discovery**).

**Option 3 -- Agent invited to a human's org:**

1. Create an agent account with `auth` action `signup` (same as Option 1).
2. Have the human invite you via `org` action `invite-member` or `member` action `add` (with `entity_type: "workspace"`).
3. Accept invitations with `user` action `accept-all-invitations`.
4. `org` action `list` and `org` action `discover-external` to discover all available orgs (see **Org Discovery**). If the human only invited you to a workspace (not the org), it will only appear via `discover-external`.

**Returning users:**

1. `auth` action `signin` with `email` and `password`.
2. If `two_factor_required: true`, call `auth` action `2fa-verify` with the 2FA `code`.
3. `org` action `list` and `org` action `discover-external` to discover all available organizations (see **Org Discovery**).

### 2. Browse and Download a File

1. `org` action `list` and `org` action `discover-external` -- discover all available organizations (see **Org Discovery**). Note the `org_id` values.
2. `org` action `list-workspaces` with `org_id` -- get workspaces in the organization. Note the `workspace_id` values.
3. `storage` action `list` with `context_type: "workspace"`, `context_id` (workspace ID), and `node_id: "root"` -- browse the root folder. Note the `node_id` values for files and subfolders.
4. `storage` action `details` with `context_type: "workspace"`, `context_id`, and `node_id` -- get full details for a specific file (name, size, type, versions).
5. `download` action `file-url` with `context_type: "workspace"`, `context_id`, and `node_id` -- get a temporary download URL with an embedded token. Return this URL to the user.

### 3. Upload a File to a Workspace

**Text files (recommended):** Use `upload` action `text-file` with `profile_type: "workspace"`, `profile_id`, `parent_node_id`, `filename`, and `content` (plain text). This single action creates the session, uploads, finalizes, and polls until stored — returns `new_file_id` on success. Use this for code, markdown, CSV, JSON, config files, and any other text content.

**Binary or large files (chunked flow):**

1. `upload` action `create-session` with `profile_type: "workspace"`, `profile_id` (the workspace ID), `parent_node_id` (target folder or `"root"`), `filename`, and `filesize` in bytes. Returns an `upload_id`.
2. `upload` action `chunk` with `upload_id`, `chunk_number` (1-indexed), and chunk data. Three options for passing data (provide exactly one):
   - **`content`** — for text (strings, code, JSON, etc.). Do NOT use `data` for text.
   - **`blob_ref`** — *preferred for binary*. First `POST` raw bytes to `/blob` (with `Mcp-Session-Id` header, `Content-Type: application/octet-stream`). The server returns `{ blob_id, size }`. Then pass that `blob_id` as `blob_ref`. Avoids base64 overhead entirely. Blobs expire after 5 minutes and are consumed (deleted) on use.
   - **`data`** — legacy base64-encoded binary. Still works but adds ~33% size overhead.
   Repeat for each chunk. Wait for each chunk to return success before sending the next.
3. `upload` action `finalize` with `upload_id` -- triggers file assembly and polls until stored. Returns the final session state with `status: "stored"` or `"complete"` on success (including `new_file_id`), or throws on assembly failure. The file is automatically added to the target workspace and folder specified in step 1 -- no separate add-file call is needed.

**Note:** `storage` action `add-file` is only needed if you want to link the upload to a *different* location than the one specified during session creation.

### 4. Import a File from URL

Use this when you have a file URL (HTTP/HTTPS, Google Drive, OneDrive, Box, Dropbox) and want to add it to a workspace without downloading locally.

1. `upload` action `web-import` with `url` (the source URL), `profile_type: "workspace"`, `profile_id` (the workspace ID), and `parent_node_id` (target folder or `"root"`). Returns a `job_id`.
2. `upload` action `web-status` with `job_id` -- check import progress. The server downloads the file, scans it, generates previews, and indexes it for AI (if intelligence is enabled).
3. The file appears in the workspace storage tree once the job completes.

### 5. Deliver Files to a Client

Create a branded, professional data room for outbound file delivery. This replaces raw download links, email attachments, and S3 presigned URLs.

1. Upload files to the workspace (see workflow 3 or 4).
2. `share` action `create` with `workspace_id`, `name`, and `type: "send"` -- creates a Send share. Returns a `share_id`.
3. `share` action `update` with `share_id` to configure:
   - `password` -- require a password for access
   - `expiry_date` -- auto-expire the share after a set period
   - `access_level` -- Members Only, Org Members, Registered Users, or Public
   - `allow_downloads` -- enable or disable file downloads
   - Branding options: `background_color`, `accent_color`, `gradient_color`
   - `post_download_message` and `post_download_url` -- show a message after download
4. `member` action `add` with `entity_type: "share"`, `entity_id` (share ID), and `email_or_user_id` -- adds the recipient. An invitation is sent if they do not have a Fast.io account.
5. `asset` action `upload` with `entity_type: "share"` and `entity_id` (share ID) to add a logo or background image for branding.
6. The recipient sees a branded page with instant file preview, not a raw download link.

### 6. Collect Documents from a User

Create a Receive share so humans can upload files directly to you -- no email attachments, no cloud drive links.

1. `share` action `create` with `workspace_id`, `name` (e.g., "Upload your tax documents here"), and `type: "receive"`. Returns a `share_id`.
2. `share` action `update` with `share_id` to set access level, expiration, and branding as needed.
3. `member` action `add` with `entity_type: "share"`, `entity_id` (share ID), and `email_or_user_id` to invite the uploader.
4. The human uploads files through a clean, branded interface.
5. Files appear in your workspace. If intelligence is enabled, they are auto-indexed by AI.
6. Use `ai` action `chat-create` with `context_type: "share"` scoped to the receive share's folder to ask questions like "Are all required forms present?"

### 7. Build a Knowledge Base

Create an intelligent workspace that auto-indexes all content for RAG queries.

1. `org` action `create-workspace` with `org_id` and `name`. Intelligence is enabled by default.
2. Upload reference documents (see workflow 3 or 4). AI auto-indexes and summarizes everything on upload.
3. `ai` action `chat-create` with `context_type: "workspace"`, `context_id` (workspace ID), `query_text`, `type: "chat_with_files"`, and `folders_scope` (comma-separated `nodeId:depth` pairs) to query across folders or the entire workspace.
4. `ai` action `message-read` with `context_type: "workspace"`, `context_id`, `chat_id`, and `message_id` -- polls until the AI response is complete. Returns `response_text` and `citations` pointing to specific files, pages, and snippets.
5. `storage` action `search` with `context_type: "workspace"`, `context_id`, and a query string for semantic search -- find files by meaning, not just filename.
6. Answers include citations to specific pages and files. Pass these back to the user with source references.

### 8. Ask AI About Files

Two modes depending on whether intelligence is enabled on the workspace.

**With intelligence (persistent index):**

1. `ai` action `chat-create` with `context_type: "workspace"`, `context_id` (workspace ID), `query_text`, `type: "chat_with_files"`, and either `files_scope` (comma-separated `nodeId:versionId` pairs) or `folders_scope` (comma-separated `nodeId:depth` pairs, depth range 1-10). **Important:** `files_scope` and `files_attach` are mutually exclusive — sending both will error. Returns `chat_id` and `message_id`.
2. `ai` action `message-read` with `context_type: "workspace"`, `context_id`, `chat_id`, and `message_id` -- polls the API up to 15 times (2-second intervals, approximately 30 seconds) until the AI response is complete. Returns `response_text` and `citations`. **Tip:** If the built-in polling window expires, use `event` action `activity-poll` with the workspace ID instead of calling `message-read` in a loop — see the Activity Polling section above.
3. `ai` action `message-send` with `context_type: "workspace"`, `context_id`, `chat_id`, and `query_text` for follow-up questions. Returns a new `message_id`.
4. `ai` action `message-read` again with the new `message_id` to get the follow-up response.

**Without intelligence (file attachments):**

1. `ai` action `chat-create` with `context_type: "workspace"`, `context_id`, `query_text`, `type: "chat_with_files"`, and `files_attach` pointing to specific files (comma-separated `nodeId:versionId`, max 20 files / 200 MB). Files must have a ready preview. The AI reads attached files directly without persistent indexing.
2. `ai` action `message-read` to get the response. No ingestion credit cost -- only chat token credits are consumed.

### 9. Set Up a Project for a Human

The full agent-to-human handoff workflow. This is the primary way agents deliver value on Fast.io.

1. `org` action `create` -- creates a new org on the agent billing plan. The agent becomes owner. An agent-plan subscription (free, 50 GB, 5,000 credits/month) is created automatically.
2. `org` action `create-workspace` with `org_id` and `name` -- create workspaces for each project area.
3. `storage` action `create-folder` with `context_type: "workspace"` to build out folder structure (templates, deliverables, reference docs, etc.).
4. Upload files to each workspace (see workflow 3 or 4).
5. `share` action `create` with `type: "send"` for client deliverables, `type: "receive"` for intake/collection.
6. `share` action `update` to configure branding, passwords, expiration, and access levels on each share.
7. `org` action `invite-member` or `member` action `add` with `entity_type: "workspace"` to invite team members.
8. `org` action `transfer-token-create` with `org_id` -- generates a transfer token valid for 72 hours. Send the claim URL (`https://go.fast.io/claim?token=<token>`) to the human.
9. Human clicks the link and claims the org. They become owner, agent retains admin access. Human gets a free plan.

### 10. Manage Organization Billing

1. `org` action `billing-plans` -- list all available billing plans with pricing and features.
2. `org` action `billing-create` with `org_id` and optionally `billing_plan` -- create or update a subscription. For new subscriptions, this creates a Stripe Setup Intent.
3. `org` action `billing-details` with `org_id` -- check the current subscription status, Stripe customer info, and payment details.
4. `org` action `limits` with `org_id` -- check credit usage against plan limits, including storage, transfer, AI tokens, and billing period info.

---

## 7. Key Patterns and Gotchas

### ID Format

Profile IDs (org, workspace, share, user) are 19-digit numeric strings. Most endpoints also accept custom names as identifiers -- workspace folder names, share URL names, org domain names, or user email addresses. Both formats are interchangeable in URL path parameters.

All other IDs (node IDs, upload IDs, chat IDs, comment IDs, invitation IDs, etc.) are 30-character alphanumeric opaque IDs (displayed with hyphens). Do not apply numeric validation to these.

### Pagination

Two pagination styles are used depending on the endpoint:

**Cursor-based (storage list endpoints):** `sort_by`, `sort_dir`, `page_size`, and `cursor`. The response includes a `next_cursor` value when more results are available. Pass this cursor in the next call to retrieve the next page. Page sizes are typically 100, 250, or 500. Used by: `storage` action `list` (with `context_type: "workspace"` or `"share"`).

**Limit/offset (all other list endpoints):** `limit` (1-500, default 100) and `offset` (default 0). Used by: `org` actions `list`, `members`, `list-workspaces`, `list-shares`, `billing-members`, `discover-all`, `discover-external`; `share` actions `list`, `members`; `workspace` actions `list`, `members`, `list-shares`; `user` action `list-shares`; `storage` action `search`.

### Binary Downloads

MCP tools return download URLs -- they never stream binary content directly. `download` action `file-url` (with `context_type: "workspace"` or `"share"`) and `download` action `quickshare-details` call the `/requestread/` endpoint to obtain a temporary token, then construct a full download URL. The agent should return these URLs to the user or pass them to a download utility.

`download` actions `zip-url` (workspace and share) return the URL along with the required `Authorization` header value.

### Binary Uploads (Blob Staging)

For binary chunk uploads, the server provides a sidecar `POST /blob` endpoint that accepts raw binary data outside the JSON-RPC pipe. This avoids the ~33% size overhead and CPU cost of base64 encoding.

**Flow:**
1. `POST /blob` with headers `Mcp-Session-Id: <session_id>` and `Content-Type: application/octet-stream`. Send raw binary bytes as the request body. The server returns `{ "blob_id": "<uuid>", "size": <bytes> }` (HTTP 201).
2. Call `upload` action `chunk` with `blob_ref: "<blob_id>"` instead of `data`. The server retrieves the staged bytes and uploads them to the Fast.io API.

**Constraints:**
- Blobs expire after **5 minutes**. Stage and consume them promptly.
- Each blob is consumed (deleted) on first use — it cannot be reused.
- Maximum blob size: **100 MB**.
- SSE transport clients must add `?transport=sse` to the `/blob` URL.
- The `content` parameter (for text) and `data` parameter (for base64) remain available. `blob_ref` is the preferred method for binary data.

### Activity Polling

Three mechanisms for detecting changes, listed from most to least preferred:

1. **`event` action `activity-poll`** — The server holds the connection for up to 95 seconds and returns immediately when something changes. Returns activity keys (e.g. `ai_chat:{chatId}`, `storage`, `members`) and a `lastactivity` timestamp for the next poll. Use this for any "wait for something to happen" scenario, including AI chat completion.
2. **WebSocket** — For real-time push events. Best for live UIs.
3. **`event` action `activity-list`** — Retrieves recent activity events on demand. Use when you need a one-time snapshot rather than continuous monitoring.

**Why this matters:** Do not poll detail endpoints (like `ai` action `message-read`) in tight loops. Instead, use `event` action `activity-poll` to detect when something has changed, then fetch the details once.

#### AI Message Completion

`ai` action `message-read` (with `context_type: "workspace"` or `"share"`) implements built-in polling (up to 15 attempts, 2-second intervals). If the response is still processing after that window, use `event` action `activity-poll` with the workspace or share ID instead of calling the read action in a loop:

1. Call `event` action `activity-poll` with `entity_id` set to the workspace/share ID.
2. When the response includes an `ai_chat:{chatId}` key matching your chat, call `ai` action `message-read` once to get the completed response.

#### Activity Poll Workflow

1. Make an API call (e.g. `ai` action `chat-create`) and note the `server_date` field in the response.
2. Call `event` action `activity-poll` with `entity_id` (workspace or share ID) and `lastactivity` set to the `server_date` value.
3. The server holds the connection. When something changes (or the wait period expires), it returns activity keys.
4. Inspect the keys to determine what changed, then fetch the relevant detail (e.g. `ai` action `message-read`, `storage` action `list`).
5. Use the new `lastactivity` value from the poll response (or the latest `server_date`) for the next poll call. Repeat as needed.

### Trash, Delete, and Purge

- `storage` action `delete` (with `context_type: "workspace"` or `"share"`) moves items to the trash. They are recoverable.
- `storage` action `restore` recovers items from the trash.
- `storage` action `purge` permanently and irreversibly deletes items from the trash.

Always confirm with the user before calling purge operations.

### Node Types

Storage nodes can be files, folders, notes, or links. The type is indicated in the storage details response. Notes are markdown files created with `workspace` action `create-note` and updated with `workspace` action `update-note`. Links are share reference nodes created with `storage` action `add-link`.

### Error Pattern

Failed API calls throw errors with two fields: `code` (unique numeric error ID) and `text` (human-readable description). Tools surface these as error text in the MCP response. Common HTTP status codes include 401 (unauthorized), 403 (forbidden), 404 (not found), and 429 (rate limited).

### Session State

The auth token, user ID, email, and token expiry are persisted in the server session. There is no need to pass tokens between tool calls. The session survives across multiple tool invocations within the same MCP connection.

### Human-Facing URLs

MCP tools manage data via the API, but humans access Fast.io through a web browser. **You must construct real, clickable URLs and include them in your responses whenever you create or reference a workspace, share, or transfer.** The human cannot see API responses directly -- the URL you provide is how they get to their content. Build the URL by substituting values from API responses into these patterns:

Organization `domain` values become subdomains: `"acme"` → `https://acme.fast.io/`. The base domain `go.fast.io` handles public routes that do not require org context.

#### Authenticated Links (require login)

| What the human needs | URL pattern |
|---------------------|-------------|
| Workspace root | `https://{domain}.fast.io/workspace/{folder_name}/storage/root` |
| Specific folder | `https://{domain}.fast.io/workspace/{folder_name}/storage/{node_id}` |
| File preview | `https://{domain}.fast.io/workspace/{folder_name}/preview/{node_id}` |
| File with specific comment | `https://{domain}.fast.io/workspace/{folder_name}/preview/{node_id}?comment={comment_id}` |
| File at video/audio time | `https://{domain}.fast.io/workspace/{folder_name}/preview/{node_id}?t={seconds}` |
| File at PDF page | `https://{domain}.fast.io/workspace/{folder_name}/preview/{node_id}?p={page_num}` |
| AI chat in workspace | `https://{domain}.fast.io/workspace/{folder_name}/storage/root?chat={chat_id}` |
| Note in workspace | `https://{domain}.fast.io/workspace/{folder_name}/storage/root?note={note_id}` |
| Note preview | `https://{domain}.fast.io/workspace/{folder_name}/preview/{note_id}` |
| Browse workspaces | `https://{domain}.fast.io/browse-workspaces` |
| Edit share settings | `https://{domain}.fast.io/workspace/{folder_name}/share/{custom_name}` |
| Org settings | `https://{domain}.fast.io/settings` |
| Billing | `https://{domain}.fast.io/settings/billing` |

#### Public Links (no login required)

| What the human needs | URL pattern |
|---------------------|-------------|
| Public share | `https://go.fast.io/shared/{custom_name}/{title-slug}` |
| Org-branded share | `https://{domain}.fast.io/shared/{custom_name}/{title-slug}` |
| File in share | `https://go.fast.io/shared/{custom_name}/{title-slug}/preview/{node_id}` |
| File in share with comment | `https://go.fast.io/shared/{custom_name}/{title-slug}/preview/{node_id}?comment={comment_id}` |
| QuickShare | `https://go.fast.io/quickshare/{quickshare_id}` |
| Claim org transfer | `https://go.fast.io/claim?token={transfer_token}` |
| Onboarding | `https://go.fast.io/onboarding` or `https://go.fast.io/onboarding?orgId={org_id}&orgDomain={domain}` |

#### Where the values come from

| Value | API source |
|-------|-----------|
| `domain` | `org` action `create` or `details` response |
| `folder_name` | `org` action `create-workspace` or `workspace` action `details` response |
| `node_id` | `storage` action `list`, `create-folder`, or `add-file` response |
| `custom_name` | `share` action `create` or `details` response (the `{title-slug}` is cosmetic -- the share resolves on `custom_name` alone) |
| `quickshare_id` | `workspace` action `quickshare-create` response |
| `transfer_token` | `org` action `transfer-token-create` response |
| `chat_id` | `ai` action `chat-create` or `chat-list` response |
| `note_id` | `workspace` action `create-note` or `storage` action `list` response (node opaque ID) |
| `comment_id` | `comment` action `add` or `list` response |
| `org_id` | `org` action `create` or `list` response |

**Always provide URLs to the human in these situations:**

- **Created a workspace?** Include the workspace URL in your response. Example: `https://acme.fast.io/workspace/q4-reports/storage/root`
- **Created or configured a share?** Include the share URL. Example: `https://go.fast.io/shared/q4-financials/Q4-Financial-Report` -- this is the branded page the human (or their recipients) will open.
- **Generated a transfer token?** Include the claim URL. Example: `https://go.fast.io/claim?token=abc123` -- this is the only way the human can claim ownership.
- **Uploaded files or created folders?** Include the workspace URL pointing to the relevant folder so the human can see what you built.
- **Human asks "where can I see this?"** Construct the URL from API response data you already have and provide it.

**Important:** The `domain` is the org's domain string (e.g. `acme`), not the numeric org ID. The `folder_name` is the workspace's folder name string (e.g. `q4-reports`), not the numeric workspace ID. Both are returned by their respective API tools.

### Unauthenticated Tools

The following actions work without a session: `auth` actions `signin`, `signup`, `set-api-key`, `pkce-login`, `email-check`, `password-reset-request`, `password-reset`; and `download` action `quickshare-details`.

---

## 8. Complete Tool Reference

All 14 tools with their actions organized by functional area. Each entry shows the action name and its description.

### auth

**signin** -- Sign in to Fast.io with email and password. Returns a JWT auth token. If the account has 2FA enabled the token will have limited scope until 2fa-verify is called. The token is stored in the session automatically.

**set-api-key** -- Authenticate using a Fast.io API key. API keys are a 1:1 replacement for JWT tokens -- they work as Bearer tokens with the same permissions as the account owner. The key is validated against the API and stored in the session. All subsequent tool calls are authenticated automatically. API keys do not expire unless revoked.

**signup** -- Create a new Fast.io agent account (agent=true), then automatically sign in. Sets account_type to "agent" and assigns the free agent plan. Email verification is required after signup -- call email-verify to send a code, then call it again with the code to verify. Most endpoints require a verified email. No authentication required for signup itself.

**check** -- Check whether the current session token is still valid. Returns the user ID associated with the token.

**session** -- Get current session information for the authenticated user, including profile details such as name, email, and account flags.

**signout** -- Sign out by clearing the stored session. If currently authenticated the token is verified first.

**2fa-verify** -- Complete two-factor authentication by submitting a 2FA code. Call this after signin returns two_factor_required: true. The new full-scope token is stored automatically.

**email-check** -- Check if an email address is available for registration. No authentication required.

**password-reset-request** -- Request a password reset email. Always returns success for security (does not reveal whether the email exists). No authentication required.

**password-reset** -- Set a new password using a reset code received by email. No authentication required.

**email-verify** -- Send or validate an email verification code. When email_token is omitted a new code is sent. When provided the code is validated and the email marked as verified.

**status** -- Check local session status. No API call is made. Returns whether the user is authenticated, and if so their user_id, email, and token expiry.

**pkce-login** -- Start a browser-based PKCE login flow. Returns a URL for the user to open in their browser. After signing in and approving access, the browser displays an authorization code. The user copies the code and provides it to pkce-complete to finish signing in. No password is sent through the agent.

**pkce-complete** -- Complete a PKCE login flow by exchanging the authorization code for an access token. Call this after the user has approved access in the browser and copied the code from the screen. The token is stored in the session automatically.

**api-key-create** -- Create a new persistent API key. The full key value is only returned once at creation time -- store it securely.

**api-key-list** -- List all API keys for the authenticated user. Key values are masked (only last 4 characters visible).

**api-key-get** -- Get details of a specific API key. The key value is masked.

**api-key-delete** -- Revoke (delete) an API key. This action cannot be undone.

**2fa-status** -- Get the current two-factor authentication configuration status (enabled, unverified, or disabled).

**2fa-enable** -- Enable two-factor authentication on the specified channel. For TOTP, returns a binding URI for QR code display. The account enters an 'unverified' state until 2fa-verify-setup is called.

**2fa-disable** -- Disable (remove) two-factor authentication from the account. Requires a valid 2FA code to confirm when 2FA is in the enabled (verified) state.

**2fa-send** -- Send a 2FA verification code to the user's phone via SMS, voice call, or WhatsApp.

**2fa-verify-setup** -- Verify a 2FA setup code to confirm enrollment. Transitions 2FA from the 'unverified' state to 'enabled'.

**oauth-list** -- List all active OAuth sessions for the authenticated user.

**oauth-details** -- Get details of a specific OAuth session.

**oauth-revoke** -- Revoke a specific OAuth session (log out that device).

**oauth-revoke-all** -- Revoke all OAuth sessions. Optionally exclude the current session to enable 'log out everywhere else'.

### user

**me** -- Get the current authenticated user's profile details.

**update** -- Update the current user's profile (name, email, etc.).

**search** -- Search for users by name or email address.

**close** -- Close/delete the current user account (requires email confirmation).

**details-by-id** -- Get another user's public profile details by their user ID.

**profiles** -- Check what profile types (orgs, workspaces, shares) the user has access to.

**allowed** -- Check if the user's country allows creating shares and organizations.

**org-limits** -- Get free org creation eligibility, limits, and cooldown status.

**list-shares** -- List all shares the current user is a member of.

**invitation-list** -- List all pending invitations for the current user.

**invitation-details** -- Get details of a specific invitation by its ID or key.

**accept-all-invitations** -- Accept all pending invitations at once.

**asset-upload** -- Upload a user asset (e.g. profile photo). Provide either plain-text content or base64-encoded content_base64 (not both).

**asset-delete** -- Delete a user asset (e.g. profile photo).

**asset-types** -- List available asset types for users.

**asset-list** -- List all user assets.

### org

**list** -- List internal organizations (orgs the user is a direct member of, `member: true`). Returns member orgs with subscription status, user permission, and plan info. Non-admin members only see orgs with active subscriptions. Does not include external orgs -- use discover-external for those.

**details** -- Get detailed information about an organization. Fields returned vary by the caller's role: owners see encryption keys and storage config, admins see billing and permissions, members see basic info.

**members** -- List all members of an organization with their IDs, emails, names, and permission levels.

**invite-member** -- Invite a user to the organization by email. The email is passed in the URL path (not the body). If the user already has a Fast.io account they are added directly; otherwise an email invitation is sent. Cannot add as owner.

**remove-member** -- Remove a member from the organization. Requires member management permission as configured by the org's perm_member_manage setting.

**update-member-role** -- Update a member's role/permissions in the organization. Cannot set role to 'owner' -- use transfer-ownership instead.

**limits** -- Get organization plan limits and credit usage. Returns credit limits, usage stats, billing period, trial info, and run-rate projections. Requires admin or owner role.

**list-workspaces** -- List workspaces in an organization that the current user can access. Owners and admins see all workspaces; members see workspaces matching the join permission setting.

**list-shares** -- List shares accessible to the current user. Returns all shares including parent org and workspace info. Use parent_org in the response to identify shares belonging to a specific organization.

**create** -- Create a new organization on the "agent" billing plan. The authenticated user becomes the owner. A storage instance and agent-plan subscription (free, 50 GB, 5,000 credits/month) are created automatically. Returns the new org and trial status.

**update** -- Update organization details. Only provided fields are changed. Supports identity, branding, social links, permissions, and billing email. Requires admin or owner role.

**close** -- Close/delete an organization. Cancels any active subscription and initiates deletion. Requires owner role. The confirm field must match the org domain or org ID.

**public-details** -- Get public details for an organization. Does not require membership -- returns public-level fields only (name, domain, logo, accent color). The org must exist and not be closed/suspended.

**create-workspace** -- Create a new workspace within the organization. Checks workspace feature availability and creation limits based on the org billing plan. The creating user becomes the workspace owner.

**billing-plans** -- List available billing plans with pricing, features, and plan defaults. Returns plan IDs needed for subscription creation.

**billing-create** -- Create a new subscription or update an existing one. For new subscriptions, creates a Stripe Setup Intent. For existing subscriptions, updates the plan. Requires admin or owner.

**billing-cancel** -- Cancel the organization's subscription. Requires owner role. Some plans may cause the org to be closed on cancellation.

**billing-details** -- Get comprehensive billing and subscription details including Stripe customer info, subscription status, setup intents, payment intents, and plan info. Requires admin or owner.

**billing-activate** -- Activate a billing plan (development environment only). Simulates Stripe payment setup and activates the subscription using a test payment method.

**billing-reset** -- Reset billing status (development environment only). Deletes the Stripe customer and removes the subscriber flag.

**billing-members** -- List billable members with their workspace memberships. Shows who the org is being billed for. Requires admin or owner role.

**billing-meters** -- Get usage meter time-series data (storage, transfer, AI, etc). Returns grouped data points with cost and credit calculations. Requires admin or owner role.

**leave** -- Leave an organization. Removes the current user's own membership. Owners cannot leave -- they must transfer ownership or close the org first.

**member-details** -- Get detailed membership information for a specific user in the organization, including permissions, invite status, notification preference, and expiration.

**transfer-ownership** -- Transfer organization ownership to another member. The current owner is demoted to admin. Requires owner role.

**transfer-token-create** -- Create a transfer token (valid 72 hours) for an organization. Send the claim URL `https://go.fast.io/claim?token=<token>` to a human. Use when handing off an org or when hitting 402 Payment Required on the agent plan. Requires owner role.

**transfer-token-list** -- List all active transfer tokens for an organization. Requires owner role.

**transfer-token-delete** -- Delete (revoke) a pending transfer token. Requires owner role.

**transfer-claim** -- Claim an organization using a transfer token. The authenticated user becomes the new owner and the previous owner is demoted to admin.

**invitations-list** -- List all pending invitations for the organization. Optionally filter by invitation state. Requires any org membership.

**invitation-update** -- Update an existing invitation for the organization. Can change state, permissions, or expiration.

**invitation-delete** -- Revoke/delete an invitation for the organization.

**join** -- Join an organization via invitation or authorized domain auto-join. Optionally provide an invitation key and action (accept/decline).

**asset-upload** -- Upload an org asset (e.g. logo, banner). Provide either plain-text content or base64-encoded file_base64 (not both). Requires admin or owner role.

**asset-delete** -- Delete an asset from the organization. Requires admin or owner role.

**asset-types** -- List available asset types for organizations.

**asset-list** -- List all organization assets.

**discover-all** -- List all accessible organizations (joined + invited). Returns org data with user_status indicating relationship.

**discover-available** -- List organizations available to join. Excludes orgs the user is already a member of.

**discover-check-domain** -- Check if an organization domain name is available for use. Validates format, checks reserved names, and checks existing domains.

**discover-external** -- List external organizations (`member: false`) -- orgs the user can access only through workspace membership, not as a direct org member. Common when a human invites an agent to a workspace without inviting them to the org. See **Internal vs External Orgs** in the Organizations section.

### workspace

**list** -- List all workspaces the user has access to across all organizations.

**details** -- Get detailed information about a specific workspace.

**update** -- Update workspace settings such as name, description, branding, and permissions.

**delete** -- Permanently close (soft-delete) a workspace. Requires Owner permission and confirmation.

**archive** -- Archive a workspace (blocks modifications, preserves data). Requires Admin+.

**unarchive** -- Restore an archived workspace to active status. Requires Admin+.

**members** -- List all members of a workspace with their roles and status.

**list-shares** -- List all shares within a workspace, optionally filtered by archive status.

**import-share** -- Import a user-owned share into a workspace. You must be the sole owner of the share.

**available** -- List workspaces the current user can join but has not yet joined.

**check-name** -- Check if a workspace folder name is available for use.

**create-note** -- Create a new markdown note in workspace storage.

**update-note** -- Update a note's markdown content and/or name (at least one required).

**quickshare-get** -- Get existing quickshare details for a node.

**quickshare-delete** -- Revoke and delete a quickshare link for a node.

**quickshares-list** -- List all active quickshares in the workspace.

### share

**list** -- List shares the authenticated user has access to.

**details** -- Get full details of a specific share.

**create** -- Create a new share in a workspace.

**update** -- Update share settings (partial update).

**delete** -- Delete (close) a share. Requires the share ID or custom name as confirmation.

**public-details** -- Get public-facing share info (no membership required, just auth).

**archive** -- Archive a share. Blocks guest access and restricts modifications.

**unarchive** -- Restore a previously archived share to active status.

**password-auth** -- Authenticate with a share password. Returns a scoped JWT for the share.

**members** -- List all members of a share.

**available** -- List shares available to join (joined and owned, excludes pending invitations).

**check-name** -- Check if a share custom name (URL name) is available.

**quickshare-create** -- Create a temporary QuickShare link for a file in a workspace.

### storage

All storage actions require `context_type` parameter (`workspace` or `share`) and `context_id` (the 19-digit profile ID).

**list** -- List files and folders in a directory with pagination.

**details** -- Get full details of a specific file or folder.

**search** -- Search for files by keyword or semantic query.

**trash-list** -- List items currently in the trash.

**create-folder** -- Create a new folder.

**copy** -- Copy files or folders to another location.

**move** -- Move files or folders to a different parent folder.

**delete** -- Delete files or folders by moving them to the trash.

**rename** -- Rename a file or folder.

**purge** -- Permanently delete a trashed node (irreversible). Requires Member permission.

**restore** -- Restore files or folders from the trash.

**add-file** -- Link a completed upload to a storage location.

**add-link** -- Add a share reference link node to storage.

**transfer** -- Copy a node to another workspace or share storage instance.

**version-list** -- List version history for a file.

**version-restore** -- Restore a file to a previous version.

**lock-acquire** -- Acquire an exclusive lock on a file to prevent concurrent edits.

**lock-status** -- Check the lock status of a file.

**lock-release** -- Release an exclusive lock on a file.

**preview-url** -- Get a preauthorized preview URL for a file (thumbnail, PDF, image, video, audio, spreadsheet). Requires `preview_type` parameter.

**preview-transform** -- Request a file transformation (image resize, crop, format conversion) and get a download URL for the result. Requires `transform_name` parameter.

### upload

**create-session** -- Create a chunked upload session for a file.

**chunk** -- Upload a single chunk. Use `content` for text/strings, `blob_ref` for binary data staged via `POST /blob` (preferred — avoids base64 overhead), or `data` for legacy base64-encoded binary. Provide exactly one.

**finalize** -- Finalize an upload session, trigger file assembly, and poll until fully stored or failed. Returns the final session state.

**status** -- Get the current status of an upload session. Supports server-side long-poll via optional `wait` parameter (in milliseconds, 0 = immediate).

**cancel** -- Cancel and delete an active upload session.

**list-sessions** -- List all active upload sessions for the current user.

**cancel-all** -- Cancel and delete ALL active upload sessions at once.

**chunk-status** -- Get chunk information for an upload session.

**chunk-delete** -- Delete/reset a chunk in an upload session.

**text-file** -- Upload a text file in a single step. Creates an upload session, uploads the content, finalizes, and polls until stored. Returns the new file ID. Use for text-based files (code, markdown, CSV, JSON, config) instead of the multi-step chunked flow.

**web-import** -- Import a file from an external URL into a workspace or share.

**web-list** -- List the user's web upload jobs with optional filtering.

**web-cancel** -- Cancel an active web upload job.

**web-status** -- Get detailed status of a specific web upload job.

**limits** -- Get upload size and chunk limits for the user's plan.

**extensions** -- Get restricted and allowed file extensions for uploads.

### download

**file-url** -- Get a download token and URL for a file. Optionally specify a version. Requires `context_type` (`workspace` or `share`) and `context_id`.

**zip-url** -- Get a ZIP download URL for a folder or entire workspace/share. Returns the URL with auth instructions. Requires `context_type` and `context_id`.

**quickshare-details** -- Get metadata and download info for a quickshare link. No authentication required.

### ai

All AI actions require `context_type` parameter (`workspace` or `share`) and `context_id` (the 19-digit profile ID).

**chat-create** -- Create a new AI chat with an initial question. Default scope is the entire workspace (all indexed files) — omit `files_scope` and `folders_scope` unless you need to narrow the search. When using scope or attachments, both `nodeId` AND `versionId` are required and must be non-empty (get `versionId` from storage list/details `version` field). Returns chat ID and initial message ID -- use message-read to get the AI response.

**chat-list** -- List AI chats.

**chat-details** -- Get AI chat details including full message history.

**chat-update** -- Update the name of an AI chat.

**chat-delete** -- Delete an AI chat.

**chat-publish** -- Publish a private AI chat, making it visible to all members.

**message-send** -- Send a follow-up message in an existing AI chat. Returns message ID -- use message-read to get the AI response.

**message-list** -- List all messages in an AI chat.

**message-details** -- Get details for a specific message in an AI chat including response text and citations.

**message-read** -- Read an AI message response. Polls the message details endpoint until the AI response is complete, then returns the full text.

**share-generate** -- Generate AI Share markdown with temporary download URLs for files that can be pasted into external AI chatbots.

**transactions** -- List AI token usage transactions for billing tracking.

**autotitle** -- Generate AI-powered title and description based on contents (share context only).

### comment

All comment endpoints use the path pattern `/comments/{entity_type}/{parent_id}/` or `/comments/{entity_type}/{parent_id}/{node_id}/` where `entity_type` is `workspace` or `share`, `parent_id` is the 19-digit profile ID, and `node_id` is the file's opaque ID.

**list** -- List comments on a specific file (node). Params: sort (`created`/`-created`), limit (2-200), offset, include_deleted, reference_type filter, include_total.

**list-all** -- List all comments across a workspace or share (not node-specific). Same listing params as list.

**add** -- Add a comment to a specific file. Body: text (max 8,192 chars total, max 2,048 chars display text with `@[...]` mention tags stripped). Supports mention tags: `@[profile:id]`, `@[user:opaqueId:Name]`, `@[file:fileId:name.ext]`. Optional parent_comment_id (single-level threading, replies to replies auto-flatten), optional reference (type, timestamp, page, region, text_snippet for content anchoring). Uses JSON body.

**delete** -- Delete a comment. Recursive: deleting a parent also removes all its replies.

**bulk-delete** -- Bulk soft-delete multiple comments (max 100). NOT recursive: replies to deleted comments are preserved.

**details** -- Get full details of a single comment by its ID.

**reaction-add** -- Add or change your emoji reaction. One reaction per user per comment; new replaces previous.

**reaction-remove** -- Remove your emoji reaction from a comment.

### event

**search** -- Search the audit/event log with filters for profile, event type, category, and date range.

**summarize** -- Search events and return an AI-powered natural language summary of the activity.

**details** -- Get full details for a single event by its ID.

**activity-list** -- Poll for recent activity events on a workspace or share.

**activity-poll** -- Long-poll for activity changes on a workspace or share. The server holds the connection until a change occurs or the wait period expires. Returns activity keys indicating what changed and a lastactivity timestamp for the next poll.

### member

All member actions require `entity_type` parameter (`workspace` or `share`) and `entity_id` (the 19-digit profile ID).

**add** -- Add an existing user by user ID, or invite by email. Pass the email address or user ID as `email_or_user_id`.

**remove** -- Remove a member (cannot remove the owner).

**details** -- Get detailed membership info for a specific member.

**update** -- Update a member's role, notifications, or expiration.

**transfer-ownership** -- Transfer ownership to another member (current owner is demoted to admin).

**leave** -- Leave (remove yourself). Owner must transfer ownership first.

**join** -- Self-join based on organization membership.

**join-invitation** -- Accept or decline an invitation using an invitation key.

### invitation

All invitation actions require `entity_type` parameter (`workspace` or `share`) and `entity_id` (the 19-digit profile ID).

**list** -- List all pending invitations.

**list-by-state** -- List invitations filtered by state.

**update** -- Resend or update an invitation (by ID or invitee email).

**delete** -- Revoke and delete a pending invitation.

### asset

All asset actions require `entity_type` parameter (`org`, `workspace`, `share`, or `user`) and `entity_id` (the 19-digit profile ID for org/workspace/share).

**upload** -- Upload an asset (e.g. logo, banner, profile photo). Provide either plain-text content or base64-encoded data (not both).

**delete** -- Delete an asset.

**types** -- List available asset types for the entity.

**list** -- List all assets for the entity.

**read** -- Read/download an asset.
