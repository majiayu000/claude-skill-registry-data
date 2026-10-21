---
name: cv
description: Build, tailor, render and approve the CV, then upload the approved version to JobCubby.
disable-model-invocation: true
---

# /cv

Files: `templates/`, `scripts/`, `docs/`, `examples/` and `routines/` are in the method root, `${CLAUDE_PLUGIN_ROOT}` (the clone holding this skill when that is not replaced by a path); every other relative path is in the workspace, the current folder. Before acting on the person's behalf, read `profile.md`, `docs/rules.md` and the workspace `rules.md`; the workspace one wins on conflict.

The CV is markdown in `cv/`, rendered to PDF by `scripts/render.mjs`. `cv/base.md` is the master; variants are separate files (`cv/de.md`, `cv/backend.md`, `cv/acme.md`). The markdown contract is `templates/cv.md`: one `# Name`, header lines, then only these sections: Summary, Technical Skills, Work Experience, Education, Achievements, Certifications, Language Skills, Hobbies. Entries under Work Experience and Education are `### dates | role`. The renderer rejects anything else and skips empty sections.

## Approval

Every CV file carries `approved:` in its frontmatter. Empty means not approved. Approved means `approved: <YYYY-MM-DD> <hash>`, the hash being the output of:

```bash
grep -v '^approved:' cv/<file>.md | shasum -a 256 | cut -c1-12
```

The **approval check** passes only when the date is set and the hash recomputed now equals the stored one, so any edit after approval, by this skill or by hand, fails it. Every edit this skill makes to a CV file also empties `approved:` in the same write. Only a CV that passes the check, and the PDF rendered from it, goes to JobCubby, LinkedIn or any board.

Modes:
- `/cv` with no `cv/base.md` yet and a file in `cv/old/`: convert the existing CV into the contract, then fix only what is marked.
- `/cv` with no CV at all: full interview, then render.
- `/cv` with an existing one: review, propose fixes (including the confirmed "Add now" tags in the latest `reports/stack-radar-<date>.md` that the CV lacks), re-render.
- `/cv variant <name> for <posting URL or pasted text>`: a tailored copy from `base.md`.
- `/cv render [file]`: just render.

Every mode that changes a CV ends with Showing and approving.

## Building from the CV they already have

The old CV's text is in `cv/old/<name>.txt`, written by `/profile` step 0. If `cv/old/` holds a CV with no `.txt` beside it, tell the person to run `/profile` first and stop.

1. Read that text and `profile.md`.
2. Write it into the contract as `cv/base.md`, starting from a copy of `templates/cv.md`: the same jobs, dates, employers, projects and education; the skills line in the order from `profile.md`; each bullet rewritten into the ABCD shape where its content allows it and kept as written where it does not. Nothing is added that the old CV or `profile.md` does not say.
3. Append ` (?)` to every bullet that has no result and no number, to every technology that only appears in the skills line, and to anything that contradicts `profile.md` (a date, a title level, a years figure).
4. Walk the marks with the person, top to bottom, a few at a time: "what changed because you did it?" for a bullet, "used in real work or a real project?" for a technology, "which one is right?" for a contradiction. Every mark is resolved or the line is removed before rendering; no placeholder survives.
5. Apply the defaults below (language, variants, photo, birth date, hobbies), run the checks, render.

A CV that already follows the contract (a `base.md` from another clone) needs only steps 3 to 5.

## Building from scratch

Ask nothing that `profile.md` already says. Interview section by section, in the person's language, and write the markdown as you go, starting from a copy of `templates/cv.md`. Defaults to propose:

- Language of the base CV: English (recommended: most postings and all ATS parsers read it); the market's language.
- Variants: base plus one per market language they apply in (recommended); base only.
- Photo: on, casual outdoor headshot (recommended for Germany and most of Europe); off for markets that do not expect one.
- Birth date: on where the market expects it (recommended for Germany); off.
- Bullets per job: by tenure as below (recommended); the person's own count.
- Hobbies: two or three real ones (recommended: they make the person memorable); none.

1. **Header.** Name, title line (role plus main stack in brackets, no level unless `profile.md` says so), city, birth date, phone, email, links, work authorization line, availability line, languages in brackets if the market expects it.
2. **Technical Skills.** One bold group label per line, technologies separated by ` | `, in the order from `profile.md`. Years in brackets on the first line. Exact ATS spellings: `TypeScript` not `TS`, `Node.js` not `NodeJS`, `CI/CD` with the slash, `React` (add `React.js` only if the person wants both).
3. **Work Experience.** Newest first. For every job ask: dates, role, employer with city or "Remote", one-line project definition (where the company is from, what the product is, who uses it, how many), bullets, technologies used. Bullet count follows tenure: two for up to a year, three or four for one to two years, four or five for longer, and the most recent job may carry more. Every bullet has the ABCD shape: an active past-tense verb (built, led, designed, cut), what was done, how or why it was done (the method, tool or reason, whichever matters more), and the result with a number: users, revenue, time saved, load time before and after, components adopted, bugs reduced, team size. Ask "what changed because you did it?" until a number or a concrete outcome appears. Append ` (?)` to anything the person is unsure about and resolve it before rendering.
4. **Education, Achievements, Certifications, Language Skills, Hobbies.** Short lines separated by ` | `.
5. **Photo.** Ask for a file in `photos/`. What works: taken by someone else, outdoors in daylight, smart-casual, a real smile, plain or natural background, space around the head so the square crop has room. What does not: selfies, passport photos, sunglasses, other people in frame, old photos. If they have none that fits, say they can generate one from their own photos with ChatGPT or Gemini and drop it in, and nothing more. The template crops to a square, so any ratio works. Photo and birth date are frontmatter switches, off for markets that do not want them.
6. **Market conventions.** Read `docs/markets/<market>.md` when it exists. For Germany: no summary paragraph, photo and birth date on. A closing line with place, date and signature appears only when `sign_place` is set in the frontmatter (with `signature` pointing at an image in `photos/`); set it only when the person asks.

## Checks before rendering

Every rule in `docs/rules.md` "Writing on my behalf", plus:

- Every technology confirmed: "Have you used X in real work or a real project?" A "no" means it stays out, however often postings ask for it; `/stack-radar` handles that gap.
- A bullet that reads like a posting is rewritten as what they did.
- Metrics present where they exist. Chronology complete (a gap is fine; a wrong date is not).
- Plain text only: no tables, columns, icons or skill bars in the markdown.
- Consistency as a format rule: one date format, one way of writing employers (with or without legal suffixes), one bullet style, the same spacing between jobs. A convention started in the first entry holds to the last.

## Rendering

```bash
node "${CLAUDE_PLUGIN_ROOT}/scripts/render.mjs" cv/base.md
```

The output is `cv/<Firstname_Lastname>_CV.pdf` (suffix from `version:` for variants, `Lebenslauf` for German) plus one PNG per page. Open the PNGs and look: two pages at most, no orphan headings, header lines not wrapping, photo present if expected. Fix the markdown (not the template) for content problems; fix `templates/cv.html` only when the design itself is wrong.

## Showing and approving

Show the person the rendered pages (the PNGs) and the PDF path, then ask:

1. Approve this CV as rendered (recommended once every mark is resolved and the checks pass)
2. Change something first (say what)

On 2, apply the change, re-render and ask again. On 1, compute the hash and write `approved: <today> <hash>` into that file's frontmatter. Done when the approval check passes for the file.

## After approval

Run the approval check on the file; when it fails, go back to Showing and approving.

- Upload the PDF to JobCubby as a labelled resume version (`upload_resume`, label = version and date, for example `Lebenslauf 2026-10-10`). The file goes in as base64: `base64 -i cv/<file>.pdf | tr -d '\n' > /tmp/cv.b64`, check its size, then `cat` it once and pass it as `data`. Base64 over about 190 KB exceeds the tool-output limit: shrink the photo in `photos/` (a 600 px square is enough), re-render, upload. Every version a sweep may send (per market and language) must exist there. Set it as default when it replaces the master (`set_default_resume`). Keep the plain-text content current (`update_resume` with the markdown text).
- For `cv/base.md`, push the approved content to the JobCubby profile: `update_profile` with headline (the CV title line), summary, skills in the CV's order, work history and education, as the CV states them. Read the existing profile first and send only what changed.
- If `.data.git/` exists, run `"${CLAUDE_PLUGIN_ROOT}/scripts/data" save "cv <name>"`.
- Update "Files" in `profile.md` if a new version should be used for a market.
- Tell the person to run `/profiles` next, so LinkedIn and the boards carry the approved CV.

## Tailoring a variant

From `base.md`: reorder technologies within a skills line by the posting, as `docs/rules.md` "Writing on my behalf" allows; the title is the role's title, translated, never the posting's sentences (same level rule); pick the language. Metrics, chronology and the confirmed technologies stay as in `base.md`. Save as `cv/<slug>.md` with `version: <slug>` and `approved:` empty, render, then show and approve it like the base. Note in the JobCubby application which version was sent.
