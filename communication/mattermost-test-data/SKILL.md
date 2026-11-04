---
name: mattermost-test-data
description: Backfill realistic test data into a Mattermost server using the Mattermost MCP tools. Creates users, teams, channels, and natural conversations. Use when the user asks to populate a Mattermost instance, create test data, set up a demo environment, seed conversations, or backfill a Mattermost server. Also provides guidance on reading, searching, and interacting with Mattermost via MCP tools.
---

# Mattermost Test Data & MCP Usage

Populate a Mattermost server with realistic test data and interact with it using the connected Mattermost MCP tools.

## Available MCP Tools

### Write Operations
| Tool | Purpose |
|------|---------|
| `create_user` | Create user accounts (username, email, password, names, nickname, optional profile_image) |
| `create_team` | Create teams (name, display_name, type O=open/I=invite, description, optional team_icon) |
| `create_channel` | Create channels (name, display_name, type O=public/P=private, team_id, purpose, header) |
| `create_post` | Post as the authenticated bot/admin user (channel_id, message, optional root_id for replies, optional attachments) |
| `create_post_as_user` | Post as a specific user via username/password login - critical for realistic multi-user conversations |
| `add_user_to_team` | Add a user to a team by user_id and team_id |
| `add_user_to_channel` | Add a user to a channel by user_id and channel_id |
| `dm_self` | Send a DM to yourself (the authenticated user) |

### Read Operations
| Tool | Purpose |
|------|---------|
| `get_channel_info` | Look up channel by ID, display_name, or name. Optional team_id scope |
| `get_channel_members` | List members of a channel with pagination |
| `get_team_info` | Look up team by ID, display_name, or name |
| `get_team_members` | List members of a team with pagination |
| `read_channel` | Read recent posts from a channel (limit, since timestamp) |
| `read_post` | Read a specific post and its thread |
| `search_posts` | Search posts by query, optional team_id/channel_id scope |
| `search_users` | Search users by username, email, or name |

## Test Data Creation Workflow

Follow this order to avoid missing dependencies:

### Step 1: Gather Requirements from User

Ask the user what kind of environment they want. If they don't specify, offer a default scenario. Key questions:
- **Theme**: What kind of team? (engineering, sales, support, devops, etc.)
- **Scale**: How many users, channels, and messages?
- **Conversation topics**: Any specific scenarios to demonstrate?
- **Realism level**: Casual startup vs formal enterprise tone?

Merge user instructions with the defaults below. User instructions always take priority.

### Step 2: Create the Team

```
create_team:
  name: url-friendly-name (lowercase, hyphens)
  display_name: Human Readable Name
  type: O (open) or I (invite-only)
  description: Brief team description
```

Save the returned `team_id` for subsequent calls.

### Step 3: Create Users

Create users with realistic, diverse profiles. For each user, define a **persona** that guides their communication style throughout all conversations.

Guidelines:
- Use `first.last` format for usernames
- Use realistic email addresses (e.g., `first.last@example.com`)
- Use password `Testpassword1!` for all test users (simple, meets complexity requirements)
- Give each user a distinct role and communication style
- Vary seniority levels (lead, senior, mid, junior, etc.)

Save each returned `user_id`.

**Persona template** (track internally, do not post):
```
Name: [Full Name]
Username: [first.last]
Role: [Job title]
Style: [Communication traits - e.g., concise and technical, friendly and verbose, asks lots of questions]
Expertise: [Domain strengths]
```

### Step 4: Add Users to Team

Call `add_user_to_team` for each user with the team_id from Step 2.

### Step 5: Create Channels

Create channels appropriate for the team theme. Always include:
- A **general** channel for announcements and broad discussion
- A **random** channel for casual/off-topic conversation
- 2-4 **topic-specific** channels matching the team's domain

For each channel, provide a meaningful `purpose` and `header`.

Save each returned `channel_id`.

### Step 6: Add Users to Channels

Call `add_user_to_channel` for each user+channel combination. Not every user needs to be in every channel - match membership to roles.

### Step 7: Create Conversations

This is the most important step. Use `create_post_as_user` to post as each user with their username and password.

#### Conversation Quality Guidelines

**Message variety:**
- Mix short responses ("Sounds good!", "On it.") with detailed technical messages
- Include markdown formatting where natural (code blocks, bullet lists, bold)
- Some messages should reference external links or tools
- Vary message length by persona (seniors write concisely, juniors explain more)

**Thread usage:**
- Use `root_id` to create threaded replies for detailed discussions
- Not every message needs a thread - quick acknowledgments stay in main channel
- Threads should have 2-5 replies typically, occasionally more for complex topics

**Persona consistency:**
- The team lead coordinates, makes decisions, celebrates wins
- Senior engineers give concise technical guidance
- Junior engineers ask questions, share what they learned
- Each person has a distinct voice

**Natural flow:**
- Conversations should reference each other implicitly ("as we discussed in #incidents")
- Include realistic work artifacts (deployment commands, config snippets, monitoring queries)
- Show collaboration: someone asks a question, others help, problem gets resolved

#### Conversation Templates

For each channel, create 2-4 distinct conversation threads. Example patterns:

**Problem-solving thread:**
1. Someone reports an issue
2. Others investigate and discuss
3. Solution is found and confirmed
4. Brief wrap-up or action items

**Coordination thread:**
1. Someone proposes a plan or schedule
2. Others confirm availability or raise concerns
3. Plan is finalized

**Knowledge-sharing thread:**
1. Someone shares an article, tool, or technique
2. Brief discussion about applicability
3. Maybe a follow-up action

**Casual thread (for #random):**
1. Light topic (weekend, conference, food)
2. A few friendly replies
3. Naturally fizzles out

## Tips for Realistic Data

- **Don't over-emoji.** Real engineers use them sparingly. One or two per conversation, not every message.
- **Include imperfections.** Occasional typos, self-corrections ("wait, I meant..."), or "nvm, found it" messages.
- **Reference real tools.** Mention Grafana, Terraform, Kubernetes, Jenkins, GitHub, etc. by name.
- **Show team dynamics.** The lead praises good work. The junior asks for help. The senior mentors casually.
- **Keep it proportional.** 3-5 messages per simple thread, 6-10 for complex discussions. Don't create 50-message threads.

## Reading and Searching Data

### Find existing data
```
search_users: term="john"            # Find users by name/email
get_team_info: team_display_name="Engineering"  # Find team by name
get_channel_info: channel_display_name="General" # Find channel by name
```

### Read conversations
```
read_channel: channel_id="...", limit=50        # Recent messages
read_channel: channel_id="...", since="2024-01-01T00:00:00Z"  # Since timestamp
read_post: post_id="...", include_thread=true   # Full thread
search_posts: query="deployment", team_id="..." # Search by keyword
```

### Inspect membership
```
get_team_members: team_id="...", limit=50, page=0
get_channel_members: channel_id="...", limit=50, page=0
```

## Common Pitfalls

- **Channel name vs display_name**: `name` must be URL-friendly (lowercase, hyphens, no spaces). `display_name` is what users see.
- **Team type**: Use `O` for open, `I` for invite-only. Most test scenarios want `O`.
- **Channel type**: Use `O` for public, `P` for private.
- **Post ordering**: Posts appear in creation order. Create them in the order you want them to appear.
- **Thread replies**: Set `root_id` to the parent post's ID. The `channel_id` must match the parent post's channel.
- **User passwords**: When using `create_post_as_user`, you need the password you set during user creation. Keep it consistent.
- **IDs are 26 characters**: All Mattermost IDs (team, channel, user, post) are exactly 26 alphanumeric characters.

## Example: Minimal Quick Setup

For a fast demo with minimal data:

1. Create team "demo-team"
2. Create 3 users (lead, senior, junior)
3. Add users to team
4. Create 2 channels (general, project)
5. Add users to channels
6. Create 5-8 messages per channel with 1-2 threaded discussions

This produces a believable workspace in ~30 tool calls.
