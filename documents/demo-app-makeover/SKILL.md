---
name: demo-app-makeover
description: >
  Turn a production CommCare app into a polished demo version in a demo project space: simpler,
  picture-led, teaching, with walkthroughs for review. Use when someone wants a demo-ready copy of
  an app. Needs the HQ app.
---

# Demo app makeover

Takes a production Learn or Deliver app and produces a demo version a funder can watch on a
phone: fewer and clearer modules, plain words, a picture on every screen, a Learn flow that
really teaches, and one quiet icon set. It works in a **demo project space**, never on the
production app, and it builds to [`_demo-app-taste.md`](../_demo-app-taste.md), the record of
Lily Olson's demo judgment. Read that file before starting, every time.

The procedure is the one that worked on 2026-10-26, when Lily and ACE turned Learn Kangaroo Care
into its demo version in EU `connect-demo` (builds 31 → 99, about 2.5 hours). It is written so the
next makeover needs fewer rounds: the taste is applied up front instead of being discovered note
by note.

A demo makeover is **project work, not a run.** It never starts `/ace:run`, never creates a
Connect opportunity, and never touches the production app. It is tracked in the canopy project
**Connect Demos** (one task per app), and its documents go in that project's folder.

## Inputs

| Parameter | Used for | Resolver |
|---|---|---|
| `source_domain`, `source_app_id`, `source_server` | the production app to start from | explicit arg; else the requester's email |
| `demo_domain`, `demo_server` | the demo project space the demo version lives in | explicit arg; default `connect-demo` on `eu`, from the Connect Demos context doc |
| `demo_app_id` | the demo version, when it already exists | explicit arg; else the context doc's Apps; else created in step 3 |
| `reviewer` | who approves (name + email) | explicit arg; else the requester |
| `reviewer_notes` | the reviewer's notes, verbatim | explicit arg |
| `source_materials` | training decks or protocols the content must follow | explicit arg; optional |
| `audience` | who the worker is and where | explicit arg; else the app's own content; else ask |
| `task` | the board task tracking this app | the Connect Demos project; created in step 1 if absent |

## Products

- **The demo app** in `demo_domain`, built and released in that space, plus an untouched **backup** of the starting app next to it, named `<App> (original backup)`.
- **Backups of every lookup table changed**, as JSON in the task's Drive folder (not only in a scratchpad).
- These docs, all rendered Google Docs in the task's folder under `Projects/Connect Demos/`:
  - the **plan doc** (from `demo-app-critique`);
  - the **walkthrough doc**: captioned screenshots in the order a worker sees them, a before/after table, **Decisions I made for you** and **Needs you**;
  - an **image and icon samples** doc, when images change;
  - the **teaching coverage** doc.
- **Context doc updates:** Decisions lines added to the Connect Demos context doc, and the app's ids added to its Apps.

## Terminology

Every string a worker or reviewer reads follows [`skills/_terminology.md`](../_terminology.md):
**Connect**, never "CommCare Connect", and US spelling (enrollment, counseling). Identifiers
keep their spelling.

## Process

1. **Open the work in the project.** Find or create the Connect Demos task for this app
   (`canopy agent add --slug ace --project "Connect Demos" …`). **One session owns an app's
   edits at a time.** If another session or turn is already editing it, say so and stand down,
   or ask it to stand down. Two writers on one HQ app overwrite each other. (On 2026-10-26, an
   inbox turn and the chat session both picked up the same build until one stood down.)
2. **Get into the demo space.**
   - The reviewer invites `ace@dimagi-ai.com` to `demo_domain` as **Admin**.
   - Accept from ACE's inbox. `scripts/clone-setup-checklist.ts accept-invites` covers US only (ace#3297). For EU, sign in to `eu.commcarehq.org` with a Playwright script, open the join link from the email, and read back ACE's role.
   - Scripts go in the session scratchpad. **Never write into the plugin cache.**
3. **Back up before the first edit.**
   - If the app isn't in the demo space yet, bring it in. A linked copy (`commcare_linked_app_copy`) needs the two domains linked; otherwise import the app's source.
   - Copy the starting app to `<App> (original backup)` in the same space: `commcare_linked_app_copy` with the same domain on both sides and `linked: false`.
   - Save every lookup table the app reads (`commcare_get_lookup_table_rows`) as JSON in the task folder. A Learn test's question bank usually lives there.
4. **Critique and plan.** Run `demo-app-critique` with the reviewer's notes and source materials.
   Share the plan doc with the reviewer (edit access) and send the reply. **Ask once, up front,
   for standing approval to release each build in the demo space** (step 9). Phones only see
   released builds, and asking per build stalls a fast review.
5. **Wait for approval of the plan.** Take answers from wherever they arrive: doc comments, the
   thread, or the chat. When the requester asks for it ("build it all out before we look again"),
   build everything with defaults. Record each default in the walkthrough's **Decisions I made
   for you**, so the reviewer can overturn it.
6. **Apply the changes, in this order** (structure first, so later passes edit the final
   shape):
   1. **Remove and merge modules** (rubric §3). When a removed module did hidden setup work, such
      as a chatbot sign-up flag, move that work into a form the worker already completes. Then
      check whether anything in the space reads it (data forwarding, connections, conditional
      alerts). Say so if nothing does.
   2. **Rename** (§2), using § Renames below.
   3. **Reorder** modules and screens (§2, §4), and set end-of-form navigation to return to the
      module list.
   4. **Fix flow honesty** (§3): every "go to X" prompt and the rule that unlocks X use one
      condition. Match forms by name, not position, so a reorder can't break the rule.
   5. **Rewrite content** (§1, §4, §5): plain words, one framing line per module, bullets,
      bolded key facts, and in-module checks with right and wrong feedback and try-again (see
      § Teaching checks).
   6. **Fix the test bank** (§5): distinct and plausible options, wording that matches the
      module, percentages shown as percentages.
   7. **Images and icons** (§6, §7), using § Images and § Icons. Show samples and get approval
      before any upload.
   8. **Build** (`commcare_make_build`) and confirm the build has no errors.
7. **Verify as a worker.**
   - Walk the app in Web Apps at phone width (≈412 px) as a test worker. Once-only forms such as a starting quiz need a fresh test worker each time.
   - Screenshot every screen and **look at each screenshot yourself**.
   - Pass the certification test end to end.
   - Then run `demo-app-critique` on the demo app. A finding it raises becomes a fix, or a line in **Needs you**.
8. **Publish the walkthrough.**
   - Captioned screenshots in worker order, a before/after table, **Decisions I made for you** and **Needs you**.
   - Share it with the reviewer, and reply on their thread with the build number.
   - State plainly what was not checked: a real phone, other languages, test submissions left in the space.
9. **Release, so the reviewer sees it.**
   - Release each build in the demo space under the standing approval from step 4. The demo app is linked to no Connect opportunity, so a release reaches only the demo space's own users.
   - Tell the reviewer: **"Update App"** on a phone (Sync refreshes data, not the app), or refresh Web Apps.
   - If the reviewer can't see a change, check which build they're running before anything else.
10. **Run review rounds.** The reviewer tests on a phone and sends notes rapid-fire (rubric §8).
    For each note:
    - answer any direct question first;
    - if a builder is already running, fold the note into its build;
    - reply with the build number when it lands.

    Once they are testing hands-on, don't send screenshots with every change unless asked. Keep a
    list of anything they deferred and remind them of it.
11. **Close the round.**
    - Update the walkthrough with everything since the last version.
    - Publish the teaching coverage doc.
    - Clean up test submissions, or list them.
    - Add each decision to the context doc's Decisions with the date and who made it.
    - When the reviewer's taste moved past the rubric, update [`_demo-app-taste.md`](../_demo-app-taste.md) in the same PR as any procedure change, and add a Change Log line here.
    - File an issue for each ACE gap hit along the way (CLAUDE.md § File ACE issues mid-run).

### Renames

A module name appears in more places than its tile. For each rename:

- Change the menu name, the form name, and the form's title label.
- Change the **Connect learn-module name and description** inside the form source.
- Change any text in other forms that names it, such as "go back and tap Get Certified".
- Change every language the app carries. Set **English last**: HQ's name setters write to the
  session's current language, and on 2026-10-26 one rename landed on the Hausa label first.
- Labels can carry a plain and a markdown version. Web Apps shows the markdown one, so change both.
- Read the form back and count: 0 old names, N new.

### Teaching checks

- **One check after each screen** that teaches a tested fact. Ask it in different words from the
  test.
- **Feedback on every answer:** "✅ Correct! *why*" for a right answer, "❌ Not quite. *why*. Try
  again." for a wrong one.
- **The worker can't continue on a wrong answer:** a constraint on the check, with the
  explanation as its message. Checks are not scored.
- **A test that draws random questions from a table draws them once, when the form opens.** If
  the draw sits in a calculate that re-runs, Web Apps re-draws after every answer, so questions
  repeat and the score is wrong (found and fixed in the KC Get Certified form).

### Images

- **Keep real photos** that fit. **Keep a detailed clinical diagram** over any generated
  replacement, cropping out text that contradicts the app (rubric §6).
- Generate the rest with Dimagi's Content Generator, invoked the way `app-media-coverage` does
  (`run-content-generator.ts <input.json> <out.png>` under the resolved `$ACE_ROOT`), with one
  shared style directive plus one scene sentence per image.
  Observed limits (2026-10-26):
  - **No reference-image input.** It can't copy a diagram's level of detail, and its prompt
    rewrite flattens line-art cues into flat vector art.
  - **It drifts to light-skinned babies and bare chests.** Name the skin tone of every person and
    every body part ("every baby, face, arms and legs, warm dark-brown"), and describe adults as
    fully clothed.
  - **Output is 1920×1152 whatever framing you ask for.** Crop afterwards.
  - **Run one request at a time.** Four of eight parallel requests failed with an upstream 503.
- **Fix a small defect by hand-editing the image** (a pompom, a stray mark, a crop, an opened
  shirt) rather than regenerating it. A regeneration fixes one thing and changes three others.
- **Check every image at full size yourself before anyone sees it:** skin tone (the baby's
  first), background, any text, the action shown, and agreement with the screen text.
- **Show samples before uploading:** a samples doc that puts new and original side by side, with
  your own notes on each image's weak points.
- Upload at ≤1000 px wide (`commcare_upload_multimedia`), set it in every language, and check the
  build's source references the new file and not the old one.

### Icons

- Draw the set as SVG, rendered to 256 px PNG: one line weight, one color, white background.
- Take the color from the original icons, e.g. the median of their hue band.
- Show a contact sheet with each icon large and at tile size, with 2–3 alternatives for any icon
  the reviewer is unsure about.
- Set menu and form icons in every language. Check how each looks next to HQ's completion check
  badge.

## MCP Tools Used

- CommCare HQ (`ace-connect`):
  - read: `commcare_list_apps`, `commcare_get_form_source`, `commcare_get_lookup_table_rows`, `commcare_download_ccz`
  - copy and edit: `commcare_linked_app_copy`, `commcare_patch_xform`, `commcare_upload_multimedia`, `commcare_set_menu_display`. Lookup-table rows were edited in place through HQ's `api/v0.5/lookup_table_item/` endpoint (2026-10-26); `commcare_lookup_table_append_rows` only appends.
  - build and release: `commcare_make_build`, `commcare_release_build`
  - EU: the session-based atoms can't sign in yet (ace#3299). Use a signed-in Playwright script against the same endpoints until that is fixed.
- Nova: only when the source app is a Nova app. Then edit through Nova's private work and redeploy (`app-modify` steps 4–8), never by patching the HQ form XML.
- Google Drive (`ace-gdrive`): `drive_upload_binary`, `drive_share_with_person`, `drive_list_permissions`
- Publishing: `canopy gdoc publish --agent ace --project "Connect Demos"` via `skills/gdoc-writer`
- Email: `bin/ace-email` for thread replies (the only send path)

## Mode Behavior

- **Auto:** builds approved changes and releases in the demo space under the standing approval.
  Never touches the production app or any Connect opportunity.
- **Review:** the plan, each image sample sheet and each outbound reply wait for the reviewer's
  yes. App edits inside an approved plan don't.

## Related skills

- `demo-app-critique`: the read-only rubric pass used in steps 4 and 7.
- `app-modify`: changing a **live** app on a live opportunity. A demo makeover never does that.
- `app-media-coverage`: attaching media to Nova-built apps in `/ace:run`. Its generator calls
  share the limits listed under § Images.
- `demo-data-setup` / `/ace:demo`: Labs dashboard demos with synthetic data. That is a different
  kind of demo.

## Change Log

| Date | Change | Author |
|------|--------|--------|
| 2026-10-26 | Initial version, distilled from Lily Olson's Learn Kangaroo Care demo session (EU `connect-demo`, builds 31–99) at Jonathan's request | ACE |
