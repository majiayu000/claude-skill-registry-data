---
name: sounds-like-me
description: "Learns how a person writes and talks from their own captions, newsletters, emails and video transcripts, writes a one-page voice guide with real examples, rewrites any draft to sound like them, and filters out phrases that make text read as machine-written. Use when someone wants a brand voice guide, a draft made to sound like them, AI-sounding phrases removed, or writing checked against their voice. Drafts only; never posts or sends."
---

# Sounds Like Me

Five agents: gather your content, measure your voice, write it down as a one-page guide, rewrite drafts to it, and filter robot phrases. The guide is built from counts and your own quoted lines, not adjectives.

See also `../humanizer`: a generic AI-tell remover that needs no samples. Use this skill when you want text to sound like one specific person.

Not for imitating someone else's voice without their consent.

## What you need

| Content | Connector | Fallback |
|---|---|---|
| Newsletters, scripts, docs | Google Drive, or Project files | Attached or pasted |
| Emails (optional) | Gmail (sent mail) | Pasted |
| Video transcripts | None | YouTube Studio > Subtitles > download your caption file, or "Show transcript" on the video page; in Claude Code, transcribe local files with Whisper. Claude.ai cannot transcribe a video file. |
| Social captions | None | Pasted, or the platform's data download |

Target: 20+ pieces or about 5,000 words, at least two types. Under 10 pieces, every finding is marked "low sample".

## Setup (`start`, or when PROFILE is empty)

Two rounds, accept "skip", show PROFILE back, then suggest `gather`.

1. Where does your writing live (captions, newsletter, blog, emails, scripts, video)?
2. Which pieces sound most like you? Which do not (ghostwritten, rushed)?
3. Do you talk differently on video than in writing? Cover both?
4. Words you always use? Words you would never say?
5. Who do you write for, in one line?
6. Topics, claims or tones that are off limits?

## Commands and routing

| Command | Runs |
|---|---|
| `gather` / `study` / `guide` | 1 / 2 / 3 |
| `build voice` | 1 to 3, one summary |
| `rewrite <text>` | 4, then 5 on the result |
| `filter <text>` | 5 alone |
| `refresh` | add new samples, rerun 2 and 3, show the guide diff |

Before acting as an agent, read its file in `agents/`. In Claude Code you can copy them to `.claude/agents/` to run as real subagents.

- `agents/01-content-gatherer.md`: labelled sample set, transcript how-to, gaps
- `agents/02-voice-studier.md`: measured findings with counts and quotes
- `agents/03-guide-writer.md`: one-page VOICE GUIDE template
- `agents/04-draft-rewriter.md`: rewrite with a fact-lock table
- `agents/05-ai-filter.md`: starter AI-phrase list and swap rule

## Safety rules (every agent)

- Never post, send, publish or schedule. Rewrites are drafts with IDs (W1, W2).
- Learn only from content the user wrote or said. Ghostwritten or guest pieces are excluded or asked about.
- A rewrite changes how something is said, never what it claims: no added facts, numbers, stories, opinions or quotes.
- Every voice rule cites its count and one quoted line from the user's own samples.
- Strip other people's names, emails, numbers and addresses from samples.
- Legal, health or money claims and apologies: keep wording careful and mark NEEDS YOU.

## Shared files

Claude Code: files in `voice/`. Claude.ai: print updated documents at the end so the user can save them to Project knowledge (the VOICE GUIDE is the one to keep).

- `PROFILE`: setup answers
- `SAMPLES`: ID | type | platform | date | words | source
- `VOICE NOTES`: agent 2 findings
- `VOICE GUIDE`: versioned, dated
- `AI PHRASES`: filter list plus user additions
- `DRAFTS`: rewrites awaiting approval

## End of every run

1. One line per agent that ran.
2. Drafts awaiting approval: ID | what | one line.
3. NEEDS YOU items.
4. Missing data and how to fix it.
5. "Nothing has been posted or sent."

Example (fake data):

```
Ran: Gatherer (26 pieces, 7,900 words), Studier, Guide (v1).
Drafts: none yet. VOICE GUIDE v1 saved (11 rules, 2 low confidence).
Gaps: only 2 emails; add 5 sent emails to firm up email rules.
Nothing has been posted or sent.
```
