---
name: ship
description: Take any mobile app, on any stack, from a working build to the App Store and Google Play. Works out the stack, sweeps the code for known rejection traps, fixes what it can, bumps the version, builds and tests the release, writes the store listing and privacy answers, uploads and submits with the user's yes, and handles rejections. Works for Expo, React Native, Flutter, native iOS and Android, Capacitor, .NET MAUI, Kotlin Multiplatform, and web apps that need wrapping first. Use when the user wants to ship, release, submit, upload, publish, get into the App Store or Google Play, cut a build, or respond to a rejection.
---

# Ship

Get the app out of the user's laptop and into the stores. Many users have never shipped
before and built the app with AI, so explain each step in plain words and never assume
they know what a provisioning profile, a version code or an app bundle is.

Read these in this skill's folder before starting:

- `references/stacks.md`: where each stack keeps its version, and how it builds and uploads.
- `references/traps.md`: things that got real apps rejected, with sources.
- `references/facts.md`: numbers that change (fees, limits, deadlines).
- `references/board.md`: the status board's file and rows.
- `references/payments.md`: store products and RevenueCat, in the order they must be set up.
- `references/play-closed-test.md`: Google Play click by click, from creating the app to a running closed test and the production application. Give the user these steps, never a summary from memory.
- `references/levels.md`: what each release level includes.
- `references/domains.md`: domains, hosts and email for the store pages.
- `references/rulebooks.md`: the full Apple and Google rulebooks for the sweep.

## The one rule

**Store rules change. Never state one from memory.** Before telling the user what a
store requires, or how to find something in App Store Connect or Play Console, open
the source link for it in the references or search the current official docs. If what
you find differs from the reference, follow the current docs, tell the user what
changed, and update the entry and its **Last checked** date. Console screens move
often, so give navigation steps only from docs fetched now.

## Where answers are kept

If the project has a rules file (`CLAUDE.md` or `AGENTS.md`) with a **Settings** table,
read it and keep shipping answers there. If not, keep them in `SHIPPING.md` at the
project root, created from `templates/shipping.md`, so the next release starts where
this one ended. Do not require the setup skill; `/ship` must work on a project that has
never seen The Last Mile.

## The status board

Keep `store/status.json`, one row per thing between the app and the stores, and show
it with `scripts/board.mjs`: an animated page that works on a phone, and a board in
the terminal. Give every row the user must act on a link straight to where it gets
done. `references/board.md` has the format, the rows, the links, and when to show it.
Pages the session's network blocks are checked from GitHub by a small workflow
(`templates/last-mile-checks.yml`); install it in GitHub projects, as that file says.
**On an update the board is off by default,** and short when it is asked for. See
"First release and update are two different jobs" in step 0, and the update rows in
`references/board.md`.

**`/ship status`, or the user asking where things stand,** means the board, never a
text summary alone:

1. Create `store/status.json` if it does not exist (step 0's checks fill it), else
   refresh its rows from what can be checked now.
2. Run `scripts/board.mjs` on it.
3. Hand the user the page as `references/board.md` says (an artifact, or the file
   rendered in the app), then give its gist in two lines.
4. Commit and push `store/status.json` the way the project's rules say, and stop.

**`/ship sweep`, or the user asking to check the app without releasing it,** means
step 0's stack, platforms and first release questions, then step 1 in full, then stop:

1. Run the rejection sweep and report it as step 1 says.
2. Fix the blockers that are code, one at a time, with the user's yes for each.
3. List what is left: blockers that need the user, and questions nobody could answer.
4. Stop. No version bump, no release build, no store listing, nothing uploaded. Say
   that a clean sweep is not an approval, and that `/ship` picks up from here.

## The ship journal

Shipping a first app is a story people want to read, and nobody remembers the details
afterwards. Keep `store/journal.md` (from `templates/journal.md`), starting at the
first `/ship` run and ending when the app is live on both stores:

- Add an entry whenever the release moves: a blocker found or cleared, a console step
  done, a build uploaded, a review answered. Say what happened, who did it, roughly how
  long it took, and what was caught that would otherwise have cost a rejection or a week.
- Write the user's own words down exactly when they say something worth quoting, with
  their permission to use them.
- Ask for screenshots at the moments worth showing (console screens, the first
  release build on a phone, the approval email) and save them in `store/ship-journal/`.
- Keep the scoreboard current, including the stats: one more session each time a
  session moves the release, days since the first run, the user's hands on time in
  consoles, and tokens when the session can see them (say "not visible" otherwise,
  never guess). The point of the stats is a better process, so record what it cost
  next to what shipped, at the level chosen. Never record keys, passwords, tokens or anything
  personal, in the text or in a screenshot.

## Scope and permission

- Check the app's code, config, assets and docs, and the official store pages.
- Do not query or change live services (databases, payment dashboards, analytics)
  unless the user asks. Note anything risky there as a question instead.
- **Ask before anything that leaves the machine:** uploading a build, uploading
  metadata or screenshots, and above all submitting for review. Say what will be sent
  and where, then wait for a yes. A yes covers that one step, not the rest.
- Never paste or print signing keys, passwords or API keys. Point to where they live.

## 0. Where you stand

Work this out from the files before asking anything, then show it in a few lines:

1. **Stack:** match the project against the detection table in `references/stacks.md`.
   If it is a web app with no native project, follow that file's web app section
   first: it needs a native wrapper, and Apple rejects wrappers that add nothing over
   the website (see the minimum functionality trap).
2. **Platforms and level:** read **Platforms** and **Release level** from the rules
   file's Settings. If either is missing, ask (one question each) and save the answer:
   iOS, Android or both; and Quick ship, Standard or Full features. If Platforms
   is web only, stop and say so: there is no store release, and a deploy is the
   release. Offer the search-pages skill if the site needs to be found.
   `references/levels.md` says what each level includes. Plan only that much, and
   leave out the rows for a platform that is not shipping.
3. **First release or update:** look for an existing bundle ID or package name, a
   previous version tag, a shipped build, or ask. **This is the question that decides
   the shape of everything below, so settle it before you plan anything.** See "two
   different jobs" at the end of this step.
4. **Accounts:** for a first release, ask whether the user has an Apple Developer
   Program membership and a Google Play developer account. Fees and the closed testing
   rule for new personal Google accounts are in `references/facts.md`; tell the user
   early, because the Google one can delay an Android launch by weeks. When they reach
   it, walk them through `references/play-closed-test.md` step by step.

5. **Web pages (a first release, or an update that moved one):** the stores need
   public pages before submission: a privacy policy
   (both stores, and linked inside the app, so its address must be final before the
   build), a support page (Apple), and an account deletion page (Google, if the app
   has accounts). Apple also requires that an app with account creation lets people
   start account deletion inside the app, and Google requires a contact email on the
   store listing. A custom domain is not a store requirement. Free hosting such as
   GitHub Pages works. Recommend a domain anyway when the app will need a contact
   email on it, invite or share links that open the app (universal links and App
   Links need a site the developer controls), or a name that should not move later.
   Ask which the user has; if neither, put the pages on the plan as an early task.
   Write down in the rules file where the pages are hosted, especially when another
   repo's server serves them, and check that host can answer links that open the app
   before relying on it (`references/domains.md`, "When the site lives elsewhere").
   `references/domains.md` covers registrars, hosts and email forwarding.

### First release and update are two different jobs

Settle question 3 before you plan anything, and **say which one this is in the first
line of your reply.** It changes the shape of everything below.

**A first release is a project.** Two developer accounts to open and pay for, web
pages that must exist at their final addresses before the build is made, a listing
written from nothing, and a review that has never seen the app. Twenty odd things
across two consoles, most of them not done. Work every step below in full, and keep
the status board, because nobody can hold that in their head.

**An update is a small, repeatable job: what changed, does any of it break a rule,
test it, ship it.** Everything the first release set up is still true. The accounts
exist, the pages are up, the listing is written, the app has passed review before.
None of that is worth putting in front of anyone. So on an update:

- **Skip 4 and 5 above.** Raise an account or a page only when something about it has
  actually broken.
- **Scope the sweep to what changed** (step 1).
- **Default to no board.** Give the user the release's test checklist and whatever
  blocks the upload, and nothing else. Make a board only if they ask where things
  stand, and then only the update rows in `references/board.md`.
- **The plan is three lines:** what is in this release, what blocks it, what to test.

The failure this exists to prevent happened in a real session. The first release
shape was run on an app that had been live for months. It produced twenty settled
rows, a progress ring reading 55 percent of work finished in May, generic console
links, and a set of long standing findings presented as though they had just been
discovered. The user said they had never seen any of it before, that it read as a
pile of new problems, and that they only wanted to go through the release checklist.
They were right, and the sweep's one real finding was lost in the noise.

End this step with a plan sized to the job: for a first release, the steps ahead,
which need the user, and the first thing only they can do (often paying for an
account) so they can start it now, written into `store/status.json` and shown as the
board. For an update, the three lines above, and no board unless asked.

## 1. Rejection sweep

This is the step that saves days. Run the fact-check skill on the traps that apply, so
the rules are current, then check each one **against the app, not the docs**:

- Search the iOS build's bundled text for other platforms' names, list the Android
  release manifest's permissions, open the icon and splash, find the account deletion
  screen, try to buy without signing in. `references/stacks.md` says where each stack
  keeps these.
- Walk every trap under **Apple** and **Google Play** that applies, and the section for
  this stack under **Stack specific**.
- Then walk the full rulebooks in `references/rulebooks.md`, section by section, from
  their saved copies. The traps are what has caught apps before; the rulebooks are
  everything else. List every section with "applies" or "does not apply" in one line,
  and check the ones that apply against the app, including its bundled content and
  copy, not only its code.
- Also check what a reviewer sees first: the icon and splash are the app's own, not a
  template's; nothing says "lorem ipsum", "TODO" or "test"; every button on the first
  screens does something.
- A rule about the store listing is checked against the **live listing**, not the
  project's draft of it. A repo's copy of its own description can be a draft, a
  fragment, or last year's. Read what the stores are serving today, and say which
  store the rule belongs to: a Google policy about the description says nothing
  about the Apple one, and reporting it against both is noise.

**On an update the sweep has two halves, and only one of them is this release's
business.**

- **What changed since the last approved build** is checked in full, and anything
  wrong there blocks: no reviewer has ever seen it. Find that boundary from the build
  that actually shipped, not from the version bump, which happens when a build is cut
  and not when it goes out.
- **Everything else** has already passed review, sometimes many times. Check it, then
  report the whole half as **one line at the end** and offer to write it to the
  project's backlog. No row, no colour, no progress bar, and no decision asked of
  someone who is trying to ship. "Three long standing things I would fix eventually,
  want them written down?" is the entire report. Dropping a months old finding on a
  user mid release reads as a new emergency, and buries the one thing that is real.

For an update to an app that is already live, some rules allow exceptions granted in
the store consoles (for example, Google's declarations for photo and video
permissions). Before calling one of those a blocker, ask whether the app already has
the exception; if nobody can say, report it as a question, not a blocker.

For a live app, also find when each finding shipped (`git log -S "<the string>"` on the
file that adds it). Something that has passed review in many releases is a risk the
reviewers have not enforced yet, not a certain rejection: say so, with the date, and
still fix it, because enforcement changes without notice. Something added since the
last approved release is the likeliest blocker.

**When there is a board, that judgement picks the row's state,** so the difference
survives into what the user looks at instead of dying in the report. A finding that
has already shipped through approved releases is `risk`. `blocked` is for something
that stops the upload, or that has never been through review, which on a live app
usually means something added since the last approved build. Most of a live app's
findings are risks, so a sweep that paints them all as blockers buries the one row
that is actually stopping the release.

Report blockers first, each with the file and line, the rule and its source, then the
passes in one line each. Offer to fix the blockers that are code. Fix them one at a
time and show each change.

Lead with the answer to the question the user actually has, which on an update is
"can I ship this". Say how many things block it, in a sentence, before anything else.
If the answer is none, say that first and plainly.

## 2. Version bump

- Bump the user facing version: patch for fixes, minor for new features, 1.0.0 for a
  first release.
- Bump the build number. Google rejects any `versionCode` it has already seen; Apple
  rejects a repeated build number within the same version (from experience). One
  counter shared by iOS and Android that always goes up satisfies both.
- `references/stacks.md` lists where each stack keeps both. If a value is set in more
  than one place, confirm they agree after the bump.
- If the project has `RELEASE_TEST_CHECKLIST.md`, move its **Pending** items into a new
  **Verify on <version>** block and drop the previous one.
- Commit the bump on its own.

## 3. Build

If the settings record how builds are made, use that. Otherwise offer the default for
the stack from `references/stacks.md`, explain it in one line, and record the answer.

- iOS needs a Mac with Xcode for a local build. Without one, a cloud build service is
  the way (Expo's EAS Build, Codemagic, Xcode Cloud, GitHub Actions on macOS).
- Android needs an app bundle (`.aab`), signed with an upload key. If the user has no
  upload key yet, explain that losing it means asking Google for an upload key reset
  in Play Console, which takes time, then help create and back it up.
- Before a cloud build, run the stack's free local checks first (for Expo: Expo
  Doctor, `eas config`, a local prebuild; see the trap "Run the free checks before
  spending a cloud build"). A failed cloud build costs quota.
- Check the build meets the stores' current minimums (Xcode and SDK version for Apple,
  target API level for Google) in `references/facts.md`.

## 4. Test the release build

A release build is not the development build. Some code only fails here.

- Install it on a real device. On iOS a release build installed straight from Xcode
  (or the stack's release run command) is enough. TestFlight is an option, mostly for
  getting builds to other people, never a required step: many people submit straight
  to review. On Android a release build on a device works too; Play Billing purchases
  need a build uploaded to a Play testing track (see `references/payments.md`).
- Open the app cold, go through the main thing it does start to finish, sign in, reach
  any paywall, and buy in the sandbox if it sells anything.
- If the project has `RELEASE_TEST_CHECKLIST.md`, work through **Verify on <version>**
  and tick items with evidence. The see-it-work skill can smoke test every screen.
- If crash reporting is installed, confirm a deliberate test error from this build
  arrives.

## 5. Store listing

Draft everything in `templates/store-listing.md`, saved as `store/listing.md` in the
project (or wherever the project keeps it), and show the user before uploading.

- **Copy and screenshots:** run the store-listing skill. It picks keywords by who
  owns each phrase, writes the name, subtitle, keyword field, descriptions, release
  notes and the first three screenshot captions within the limits in
  `references/facts.md`, and keeps the evidence in `store/keywords.md`. If it is not
  installed: write for the person who would use the app, from what the code actually
  does, nothing it cannot do yet, and capture screenshots at the sizes in
  `references/facts.md` with realistic content, not an empty state.
- **Privacy answers:** list every SDK and every network call that sends data
  (analytics, crash reporting, ads, sign in, payments, the app's own server). Map each
  to the data types Apple's privacy labels and Play's Data safety form ask about, and
  draft the answers. Mark each one as found in code or a guess, and tell the user the
  answers are theirs to confirm: they are a legal statement.
- **Privacy policy and support pages:** both must load. If the user has none, draft a
  privacy policy from the privacy answers and suggest a place to host it.
- **Review notes:** if the app has sign in, a demo account the reviewer can use, and
  how to reach anything hidden behind a purchase or a setting.

## 6. Upload and submit

Follow the upload path for the stack in `references/stacks.md`. Ask before each upload.

- **Command line first.** Use the stack's own tool (`eas submit`, Xcode's upload,
  Gradle Play Publisher, fastlane) when the project has it, or offer to set it up.
  fastlane's `deliver` and `supply` can upload listing text and screenshots too.
- **What only the user can do** (and say so plainly): enrolling and paying for
  developer accounts, accepting agreements, tax and banking, creating API keys, and any
  form the stores only offer in their consoles. Check the current docs for which forms
  are console only before saying so. For each, give the steps from docs fetched now,
  then wait.
- **Submit for review** only when the user says to. Then tell them what happens next
  and roughly how long, from the stores' current pages.

## 7. If the review comes back rejected

1. Read the message. It names a guideline or a policy.
2. Fix only what it asks for. Unrelated changes invite new questions.
3. Draft a reply in two or three polite sentences saying what changed. If the reviewer
   misunderstood, explain with a screenshot.
4. Bump the build number, rebuild, upload and resubmit, asking before each upload.
5. Record the rejection with its date and guideline in the project's gotchas or
   `SHIPPING.md`.
6. If it would catch other apps and is not already in `references/traps.md`, offer to
   report it to The Last Mile. Fill in the report yourself from what just happened, so
   the user only has to say yes:
   - **Fields:** store, stack, what happened (month and year, the reviewer's wording),
     the guideline, what fixed it, how to check for it, and an official source if one
     was read during the fix.
   - **Strip the project out:** no app name, screen names, copy, user data, keys,
     URLs or account ids. Word it for any app.
   - Show the draft. On a yes, open it with
     `gh issue create --repo namedtoaster/the-last-mile --title "Trap: <plain words>" --body <the fields as headed sections>`.
     Without `gh`, give the user the form link
     `https://github.com/namedtoaster/the-last-mile/issues/new?template=this-caught-me.yml`
     with the draft to paste.

## 8. After it ships

- Record the release in the settings: version, build number, date, store links.
- Clear the shipped **Verify on** block from the release checklist, if there is one.
- Tag the release in git (`v<version>`), if the project tags releases.
- Add the final entry to `store/journal.md`, then offer to draft a launch post or
  thread from it: the story in the user's own words, with the screenshots.
- Tell the user it's live, with the store links. Then one line on what comes next:
  shipping was the last mile, and getting people to use it is the next one.
