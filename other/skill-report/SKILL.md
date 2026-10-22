---
name: skill-report
description: >-
  Reports a mistake a devkit skill should have prevented to the devkit's own issue tracker,
  as a "skill missed" issue drafted from the session where it happened: the request, what
  Claude did, the fix, and the Umbraco and devkit versions, with confidential details
  removed. Shows the draft and posts only on the user's yes. Use when the user says Claude
  got something wrong that the devkit should have caught, or asks to report a skill miss.
user-invocable: true
argument-hint: [optional: what went wrong]
---

# skill-report

Turn a miss into an issue on the devkit's tracker, from the project where it happened. Each
report becomes a `real-bug` eval, so the devkit stops making the same mistake. The issue is
public: nothing gets posted until the user has read the draft and said yes.

## Scope

- IN: one miss per report. Claude wrote or advised something wrong, in a project with the
  devkit loaded, and a devkit skill should have prevented it.
- OUT: a bug in the project's own code that Claude didn't cause (that's `investigate-bug`),
  a bug in Umbraco itself (that goes to the CMS tracker), a feature request for the devkit,
  and a repeatable trap that isn't the devkit's fault (that's a `.claude/memory/` `gotcha`,
  or `project-retro` if nothing already caught it). Say which it is and stop.

## Argument

`$ARGUMENTS` may describe the miss in the user's words. If it's empty, take the miss from the
session: the request, the wrong answer, and the correction that followed. If the session
doesn't hold the miss, ask for the three template fields below in one message.

## Steps

1. **Find the tracker.** Read `homepage` from the devkit's `plugin.json`, in the
   `.claude-plugin/` folder two levels above this skill's folder. That's the repo to report
   to. Never guess it.
2. **Gather the facts.** Fill each field of the tracker's "A skill missed something" form:
   - **What you asked Claude:** the request as the user typed it, or close to it.
   - **What Claude did:** the code or answer, and why it's wrong. Keep only the lines that
     show the mistake.
   - **What would have been right:** the fix, with a link to the docs, CMS source, or commit
     that proves it, if the session has one. Never invent a link.
   - **Umbraco and devkit versions:** the Umbraco version from the project's `Umbraco.Cms*`
     package references, and the devkit `version` from the same `plugin.json`.
   - **Skill you'd expect to cover it:** the devkit skill whose description fits the
     mistake, or blank if none clearly does.
3. **Remove what isn't the user's to share.** The project may be private and the issue is
   not. Replace with neutral stand-ins (`MyPackage`, `example.com`, `<secret>`):
   - secrets: keys, tokens, passwords, connection strings;
   - client, customer, and employee names, emails, and other personal data;
   - internal hostnames, URLs, and file paths outside the repo;
   - private code beyond the few lines that show the mistake.

   If the stand-ins would hide the mistake itself, say so and ask the user how to word it.
4. **Hold a security hole back.** If the mistake left a vulnerability in code that has
   shipped or is live, a public issue tells attackers where to look. Describe the missed
   rule in general terms only: no package name, endpoint, or exploit steps. If it can't be
   reported without those, tell the user to fix and release first, and stop.
5. **Look for a duplicate.** `gh issue list --repo <owner/repo> --label skill-missed --state
   all --search "<key words>"`. If one matches, offer to add the new case as a comment on it
   instead of opening a new issue.
6. **Show the draft.** The title (`Skill missed: <one line>`), then the body with one `###`
   heading per form field, using the form's field labels. Then ask: post it, change it, or
   drop it.
7. **Post only on a yes.** `gh issue create --repo <owner/repo> --title "<title>" --label
   skill-missed --body-file <draft>`. If `gh` can't post the label, post without it; the
   title prefix still marks it. If `gh` isn't installed or logged in, give the user the
   form link, `<homepage>/issues/new?template=skill-missed.yml`, and the drafted field text
   to paste in. Never post a version the user hasn't seen.

## Hand off

The issue link, or the form link and the draft if it wasn't posted. One line.
