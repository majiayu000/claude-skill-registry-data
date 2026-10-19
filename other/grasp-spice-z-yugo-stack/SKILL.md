---
name: grasp
description: Explain a pull request so a reviewer can understand it fast, big picture first. Produces a layered summary that first explains the feature itself (what it is, key terms), then a very short plain-English hook for the change, a fixed five-stop map of where the change sits in the system (Who, Screen, Endpoint, Logic, Data), numbered parts, a "live for users today?" line, a concrete before/after use case, and collapsible overview and detail. Use this whenever someone asks to review, summarize, explain, or understand a PR, diff, branch, or set of agent-written changes, or pastes a PR link or number, even if they only say "what does this PR do?" or "help me review this".
---

# grasp: understand a PR, big picture first

Explain a pull request to a reviewer who did not write it. Often the PR was written by an AI agent, and often the reviewer does not know this part of the product well.

## Principles

Every rule in this skill comes from one of these principles. When a PR does not fit the template, follow the principles.

1. **Understanding, not reading.** The hard part of a review is not the size of the diff. It is knowing why the change exists and what it does to real people. Every line of the output must help with that.
2. **Fixed abstraction levels.** Start at the highest level and go down one level at a time: feature, change, system map, use case, overview, detail. Never mix high-level and low-level detail in one place. Each level must make sense without the levels below it. Deeper levels are optional for the reader, so put them in toggles.
3. **Same shape every time.** A stable structure becomes a mental model. The reader learns once where to look, and does not get lost. Do not add, remove, rename, or reorder sections. The five-stop map always has the same five stops.
4. **Context before change.** A reviewer cannot judge a change to something they do not understand. Explain the feature first, then the change.
5. **The whole picture.** Show where the change sits in the system. For frontend code: which screen and which feature use it. For backend code: which endpoints and which callers run it. For shared code: everything else that uses it.
6. **Concrete over abstract.** One real person doing one real action, before and after, is easier to understand than any general description. Then show what happens in nearby situations.
7. **Before and after, always.** For behavior and for code: what was true before, what is true now.
8. **Plain English for every reader.** Assume the reader may not be a native English speaker. Start with a tiny hook sentence. Use short sentences and common words, with no idioms. Keep technical names exact. Write in English only.
9. **Do not trust the description.** A PR description says what the author meant to do. Agent-written descriptions can be confident and incomplete. Check the code, and name what the description plays down: changes outside a feature flag, shared code, changed behavior of existing endpoints.
10. **Honest about limits.** Never invent files, endpoints, callers, or numbers. When unsure, write it as something to check. Always list what you could not verify.

## Workflow

### 1. Get the PR

Use whatever this environment offers. Do not assume a specific tool. Try in this order and stop when you have enough:

1. A tool that can read the PR from its host (GitHub CLI such as `gh pr view <n> --json title,body,files` and `gh pr diff <n>`, a GitHub, GitLab, or Bitbucket connector, an issue tracker connector).
2. Local git: `git log` and `git diff <base>...<head>` for the branch.
3. Text the user pasted (description, diff, link contents).

You need: title, description, list of changed files, and the diff. Also look for linked issues and whether the PR is part of a stack or series (for example "1/4", "Depends on #123", "Builds on #456").

If you only have the description and not the diff, continue, but say so in the "Not checked" line of the output.

### 2. Find the big picture in the codebase

*Principles 5 and 9.*

The PR description is not enough. If you can read the repository, search it. This is what turns a summary into understanding.

- **Frontend change:** find where the changed component is rendered. Follow it up to a route or page. Name the screen the way a user would ("Settings → Billing → Invoices"), not the file name.
- **Backend change:** find which endpoint, job, or event handler runs the changed code. Find who calls that endpoint (which app, which screen).
- **Shared code** (hooks, utils, shared libs): find every other place that imports it. These are the hidden blast radius.
- **Flags:** find every feature flag the change checks. Find whether the flag is on anywhere (description, config, flag files). Then find any changed code that runs **outside** the flag. This is often the riskiest line in the PR and the description often treats it as a side note.
- **Deploy order:** check if frontend and backend must ship in a specific order.

If you cannot search the repo, say what you could not check. Never invent file names, endpoints, callers, or numbers.

### 3. Explain the feature

*Principle 4.*

Before describing the change, explain the feature the PR touches, for a reader who has never used it.

- **What it is:** one sentence, in the user's words. "A work order is a record of repair work on a vehicle."
- **Who uses it and how it normally works:** one or two sentences. Focus on the behavior this PR changes, so the change makes sense next.
- **Key terms:** pick 3 to 5 words that appear later in the summary and that an outsider would not know (domain words, status names, internal concepts). Give each a one-line meaning.

Find this in the repo docs, README files, the linked issue, type and model definitions, UI labels, and the PR itself. Only state what these sources support. If the feature is obvious to anyone (a login page, a search box), keep this to one sentence and skip key terms.

### 4. Split the PR into parts

*Principles 2 and 3.*

Group the changes into **2 to 5 parts** by what they do, not by file. One part = one idea a reviewer can check on its own. Number them (1), (2), (3). If the PR truly does one thing, use one part and skip the parts list.

The same numbers must appear everywhere below: map, use case, overview, detail. That way the reader can follow one part from top to bottom.

### 5. Place it on the five-stop map

*Principles 3 and 5.*

Every PR gets the same five stops, in the same order. This is the reader's mental model. It must never change shape:

| Stop | Meaning |
|---|---|
| Who | The person affected (role, not name): shopper, admin, support agent, developer calling the API |
| Screen | Where they are in the product |
| Endpoint | The API, job, or entry point that runs |
| Logic | The rule or behavior in the backend |
| Data | What is stored or read |

Mark which stops this PR changes with its part numbers. Unchanged stops still appear, so the reader sees the full path. If a stop does not fit perfectly (for example an agent runtime instead of a REST endpoint), keep the stop name and adapt the value.

### 6. Write the use case

*Principles 6 and 7.*

Pick **one concrete person doing one concrete thing**, and walk through it before and after.

- If the PR or issue mentions a real incident or example, use it.
- Otherwise build a realistic one from what you found in step 2. Use a role and a specific action ("A support agent opens an order from two months ago and downloads the invoice").
- Use the seed data or QA steps in the PR if they give concrete values.

Then write **"What else happens"**: 3 to 5 nearby situations. Good ones to check:

- A user without permission tries the same thing.
- The flag is off.
- Shared code reaches another feature.
- Wrong deploy order.
- Edge inputs: empty, expired, too long, duplicate, double click, slow network.
- Something the author says was not tested.

Mark rows that are risks or open questions with ⚠️. These rows are the most valuable part of the review. They often surface what the description does not say. Only claim what the code or description supports. When unsure, phrase it as a check ("Check that…").

### 7. Write the output

Read `references/template.md` and follow it exactly. Read `references/example.md` for a complete example.

Output Markdown. It renders in most places (GitHub, Cursor, VS Code, chat apps, Markdown viewers). The `<details>` blocks become toggles where HTML is supported. In a plain terminal the tags show as text, but the order still gives the layers, so keep them.

**HTML version.** When the user asks for an HTML page, a file to open in a browser, or a visual version, fill `assets/template.html` instead. Keep its HTML and CSS exactly as they are, so every review looks the same (Principle 3). Only replace the placeholders and the repeat and optional blocks, as its header comment explains. It is light theme only. Save it as `pr-review-<number>.html`, then open it or give the user the path. The content is the same as the Markdown version, in the same order.

Reply with the summary directly. If the user asks to post it on the PR, or to save it, do that. Do not post comments on a PR without being asked.

## Writing rules

*Principle 8.*

These apply to every line of the output.

- **Hook: 8 words or fewer.** Subject, verb, object. Example: "Shoppers can save cart items for later."
- **Short sentences.** One idea per sentence. Most sentences under 15 words.
- **Common words.** No idioms or phrasal verbs that confuse non-native readers. Write "suggests", not "nudges". "Move", not "steer". "Do not match", not "drift apart". "Shows", not "surfaces".
- **Keep technical names exact.** Code names, endpoints, flags, and file names stay in `code` format, unchanged. Do not translate or paraphrase them, because the reader will search for them.
- **Name screens the user's way.** "Settings → Billing → Invoices", not `InvoiceListView.tsx`.
- **No filler.** No "This PR aims to", no "comprehensive", no "robust".
- **English only.**

## Size limits

| Layer | Limit |
|---|---|
| About the feature | 3 sentences |
| Key terms | 5 terms, one line each |
| Hook | 8 words |
| Plain summary | 2 sentences |
| Parts | 5 parts, one line each |
| Use case steps | 5 steps per side |
| "What else happens" | 5 rows |
| Overview rows | One or two sentences each |
| Code in detail | Only the lines that changed meaning, about 10 lines per snippet |

If a PR is too big to fit these limits, that is useful information. Say it in the "Live today" line or in Check this ("This PR does 7 things; consider splitting").

## Before you finish

Check your output against this list:

- Could someone who has never used this feature understand the About block?
- Are the domain words used later explained in Key terms?
- Does the hook make sense to someone who knows nothing about this PR?
- Do the part numbers match across map, use case, overview, and detail?
- Is every claim backed by the code, the diff, or the description?
- Did you name any change that runs outside the feature flag?
- Did you list what you could not check?
