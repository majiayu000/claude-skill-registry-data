---
name: profiles
description: Bring LinkedIn and every board profile in sources.md in line with the approved CV.
disable-model-invocation: true
---

# /profiles

Files: `templates/`, `scripts/`, `docs/`, `examples/` and `routines/` are in the method root, `${CLAUDE_PLUGIN_ROOT}` (the clone holding this skill when that is not replaced by a path); every other relative path is in the workspace, the current folder. Before acting on the person's behalf, read `profile.md`, `docs/rules.md` and the workspace `rules.md`; the workspace one wins on conflict.

Arguments: `/profiles` (LinkedIn), `/profiles all` (LinkedIn plus every `login: yes` source in `sources.md` that has a profile), `/profiles <platform>`.

A platform carries only what the approved CV says, plus the contact facts and the location-by-market table from `profile.md`.

## 1. Approved CV

Run the approval check from `/cv` on `cv/base.md` and on every market version a platform in scope will get:

```bash
grep -v '^approved:' cv/<file>.md | shasum -a 256 | cut -c1-12
```

It passes when the frontmatter has `approved: <date> <hash>` and the hash equals this output. When any file fails, stop: name the file and tell the person to run `/cv` and approve it. Nothing goes to a platform before every file in scope passes.

## 2. Plan

Read the current state of each platform in scope in the Playwright browser, then write one list for the person: every text to set, per platform and field, and every planned deletion (a stored CV, a skill, an entry the CV does not carry).

**LinkedIn:**

1. **Photo**: the CV photo.
2. **Name**: exactly as in the CV.
3. **Headline**: the CV title line.
4. **About**, three paragraphs, first person, concrete nouns and numbers:
   - Who I am: role, years, core area; what I am doing now or did last, with one number from the CV. One personal line from the CV's hobbies is fine if it is specific.
   - Stack: "I work with ..." followed by the technologies from the CV skills lines, in the CV's order, separated by commas or bars, no years.
   - Industries and settings: the kinds of companies and products in the CV's project lines, where, in what kind of environment.
5. **Experience**: roles, companies and dates copied 1:1 from the CV. One line per role, no bullet lists.
6. **Skills**: exactly the technologies in the CV skills lines, in the CV's order; skills the CV does not list go on the deletion list. Tell the person which five skills are worth asking endorsements for.
7. **Certifications, languages, awards**: everything the CV lists; entries it does not list go on the deletion list.
8. **Contact**: the profile email, the GitHub link.
9. **Location**: the default city and phone from the location-by-market table, never a regional variant.
10. **Open to work**: titles from the CV title line and the profile targets, locations per the location-by-market table, work modes from the profile.
11. **Résumé for Easy Apply**: the approved CV PDF in the job application settings; older stored files go on the deletion list.

**Other platforms** (XING, Djinni, hh.ru, Wellfound, Instaffo, getmatch and similar), in the platform's language:

- Title identical to the CV title (translated for the platform's language).
- Photo identical to the CV photo.
- City and phone per the location-by-market table in `profile.md`; the "about" text agrees with the city.
- Stack line as in the CV skills lines.
- Exactly one CV uploaded, the approved version for that market; every other stored CV goes on the deletion list.
- Dates and employers identical to the CV.
- Visibility set to the widest setting the platform offers.

Show the whole list and ask for the go. Done when the person has said go, or has struck items and said go for the rest.

## 3. Apply

Apply every item on the approved list in the Playwright browser: open each section's edit dialog, replace the text, save, verify on the public profile view. The agent does the editing on every platform; the person is told only what sits behind a confirmation code or a challenge page.

## 4. Report

Per platform: what changed, what still differs from the CV, and the few things only a human can do (endorsement requests, a verification code).

Remind the person once that recruiters read their other public profiles too (Instagram, Facebook, X, GitHub bio) and anything controversial, sloppy or unprofessional costs interviews. Leave those accounts untouched.
