---
name: Setting up Hyperspell
description: Guide the user through integrating Hyperspell into their project
allowed-tools: Bash, Read, Grep, Glob, Write, Edit, TodoWrite
---

# Setup Hyperspell

## Instructions

Copy this checklist and track your progress:

```
Implementation Progress:
- [ ] Step 1: Install the SDK
- [ ] Step 2: Configure the API Key
- [ ] Step 3: Add memories
- [ ] Step 4: Search Memories
- [ ] Step 5: Wrapping up
```

Run the following command and note the output as $START_TIME:

```sh
date -u +%Y-%m-%dT%H:%M:%SZ 
```

### Step 1: Install the Hyperspell SDK

Then, determine whether the hyperspell SDK is already installed. If not, install it (for typescript projects with `npm i hyperspell` or `yarn add hyperspell`, for python projects with ie. `uv add hyperspell` or whatever their package manager for the current project is).

### Step 2: Configure the API Key

When the user evoked this command, they may have passed the folowwing api key as an argument: '$1'

If that string is blank, tell the user to go to https://app.hyperspell.com/api-keys to create an API key and paste it here. 

Then put it in .env.local (or .env if it doesn't exist) as `HYPERSPELL_API_KEY`.

If this project contains an `.env.example`, also put a dummy key in there (`HYPERSPELL_API_KEY=hs-0-xxxxxxxxxxxxxxxxxxxxxx`)

### Step 3: Asking how the user wants to add memories

Hyperspell is a memory and context layer for AI agents and apps. Memories typically come from two sources:

* Your project's end-user connects their accounts (ie. Gmail, Slack, ...) and Hyperspell automatically ingests the content to create memories
* You add the memories manually (ie. through file uploads or tracking conversations).

Display the following explanation to the user (replace `<YOUR PROJECT>` with the name of this project):

```
Hyperspell can create memory from a wide number of different sources, including e-mail, Slack, documents, chat transcripts, or uploaded files.

Most projects want to automatically create memories by letting their users connect their accounts. However, other projects may only need to create memories by directly by uploading files or conversations. How do you want to create memories in <YOUR PROJECT>? 
```

Then, ask the user how they want to ingest memories. Offer this multiple choice menu:

- I want to connect my user's accounts automatically
- I want to add memories directly (upload files or conversations)

Based on their choice, follow the instructions in ./connect_memories.md or  ./upload_memories_directly.md 

### Step 4: Asking how the user wants to use memories

Display the following message to your user:

```
Now that we've created a way to get new memories into Hyperspell, we also need to access them at the right time to give your app the necessary context. Let me analyse your code base and determine the best way to do so.
```

Depending on the nature of this project, there are different ways to use Hyperspell. Determine if this project is using a third party SDK to manage their core agent loops and follow the appropriate instructions:

- For the Vercel AI sdk (the `ai` package in package.json), follow the instructions in ./vercel_ai_sdk.md
- If this project is not using any third-party SDKs, follow the instructions in ./no_sdk.md

## Step 5: Wrapping up

Run the following command again:

```sh
date -u +%Y-%m-%dT%H:%M:%SZ 
```

Compare the output with $START_TIME and calculate how many minutes have passed since we started this skill as DURATION.

Then, euphorically congratulate the user (by name if you know), they've just implemented hyperspell in less than <DURATION> minutes.

Display the following message:

```
This is just the beginning of your journey with Hyperspell. As your project grows, Hyperspell grows with you. If you ever need help, you can use the /hyperspell:help command to get a direct line to the founders, right here from Claude Code.
```
