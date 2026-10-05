---
name: linkedin-publisher
description: Draft, format, attach media, save, verify, and safely publish LinkedIn posts through an authenticated browser. Use for LinkedIn post preparation, draft editing, media upload, publication, or troubleshooting the current Shadow DOM composer; do not use for generic social copy with no LinkedIn delivery.
---

# LinkedIn Publisher

Prepare reader-friendly LinkedIn posts, preserve the user's authenticated browser session, and keep publication behind an explicit final confirmation.

## Browser and authority

- Honor an explicitly requested browser surface. When the user requests the in-app browser, use the Browser skill and do not switch to Chrome, a connector, or an API.
- Use the existing signed-in session. Do not inspect cookies, local storage, tokens, passwords, or session files.
- Treat entering or editing post text, uploading media, saving a draft, and publishing as external mutations. Obtain the confirmation required by the active browser policy.
- Never click `Post` until the user gives a fresh, explicit confirmation after seeing or approving the final text, media, audience, and link state.
- Draft authorization does not authorize publication.
- Before creating a draft, inspect the Feed-level `Start a post` control for an existing `Draft:` preview. LinkedIn may restore that draft directly instead of creating a separate one. Do not overwrite, discard, or repurpose an existing draft unless the user explicitly authorizes that exact draft change; otherwise preserve it and report that it blocks an isolated draft test.

## Sensitive-information gate

Treat every LinkedIn post as public content unless the user explicitly selects a narrower audience. Before entering text or uploading media, inspect the complete public payload for sensitive information. Repeat the check immediately before publication.

Review all of these surfaces:

- Post body, hashtags, mentions, and alternative text.
- Images, screenshots, charts, captions, visible browser or application chrome, and embedded metadata that the platform may expose.
- Destination URLs, link previews, filenames, document titles, and quoted log or code excerpts.

Look specifically for:

- Passwords, tokens, API keys, cookies, session identifiers, private keys, access codes, or connection strings.
- Private IP addresses, internal hostnames, usernames, email addresses, phone numbers, precise locations, or personal identifiers.
- Internal filesystem paths, database locations, customer or project names, issue IDs, private repository details, unpublished commit identifiers, or non-public architecture and performance data.
- Screenshot artifacts such as terminals, browser tabs, account names, notifications, QR codes, timestamps, machine names, or internal dashboards.

Do not upload or enter the original content when a suspected secret or private identifier is present. Prepare a sanitized local copy, remove unnecessary metadata, and verify the rendered replacement. If redaction would change the meaning or ownership is unclear, stop and ask the user which public wording to use.

Never treat a file's location in `.manifest`, a private repository, or an ignored directory as evidence that its contents are safe to publish.

## Recommended copy shape

LinkedIn currently permits up to 3,000 characters in an ordinary post. See [LinkedIn Help: Post and share updates](https://www.linkedin.com/help/linkedin/answer/a528176).

For an image-led engineering post or a teaser for a longer article, default to:

- 100-140 English words.
- Roughly 700-900 characters.
- A strong first one or two lines before the feed truncation point.
- Short paragraphs, one concrete observation, one key conclusion, and an optional call to action.
- Three to five relevant hashtags at the end.

This is a readability default, not a platform limit. Preserve longer text when the user wants a self-contained technical explanation or when removing detail would weaken the argument.

Avoid reproducing an entire Medium article in the LinkedIn post. Use LinkedIn to establish the problem, reveal the non-obvious finding, and give readers a reason to continue.

## Normal workflow

1. Read or prepare the authoritative post text and confirm which media and destination link are in scope.
2. Complete the sensitive-information gate on the text, media, alternative text, filenames, and destination link before transmitting any of them to LinkedIn.
3. Open LinkedIn Feed in the authenticated browser and check whether `Start a post` already exposes a `Draft:` preview.
4. If no draft exists, prefer the visible `Start a post` flow for text-only posts. If a draft exists, preserve it unless the user explicitly authorizes replacing or editing that specific draft.
5. For an image post, prefer the Feed-level `Photo` button, upload the sanitized local file through the file chooser, and continue to the post composer.
6. Enter the body, confirm the audience, and add useful alternative text when requested.
7. Read back the logical text, media state, audience, and final button state.
8. Save as a draft unless the user has explicitly requested publication and has confirmed the final version.
9. Reopen a saved draft and verify that both text and media persisted.
10. Mark the tab for user handoff when the user may inspect or publish later.

When uploading a file, start the file-chooser waiter before clicking the control and attach a rejection handler immediately. Use an absolute local path. Prefer a real `input[type=file]` when one is available.

## LinkedIn Shadow DOM failure mode

LinkedIn may render its composer inside the open Shadow Root hosted by `div#interop-outlet`. In that version of the UI:

- `document.activeElement` is the Shadow Host.
- The real editor is `document.activeElement.shadowRoot.activeElement`.
- The editor is a `contenteditable` element labeled `Text editor for creating content`.

Some browser-control layers compare only the first-level active element with the inner editor. Typical symptoms are:

- `Active element is no longer the expected input target`.
- `fill`, `type`, paste, or key presses return an error or make no change.
- Shadow DOM buttons report a successful click but do not advance the UI.
- `Add media` does not open a file chooser.

Try the normal workflow first. If these symptoms are reproduced, read and follow [references/shadow-dom-workaround.md](references/shadow-dom-workaround.md).

## Verification gates

Before saving or publishing, verify:

- The sensitive-information gate passes for the final rendered text, image, alternative text, filename, and link preview. Do not rely only on the original local source inspection.
- The logical body matches the approved source text after normalizing LinkedIn paragraph nodes.
- The intended image is attached and no unintended test link or preview remains.
- The audience is the intended value, commonly `Anyone`.
- Hashtags are recognized and not accidentally duplicated.
- The `Post` button is enabled, but remains unclicked unless separately confirmed.

After saving, wait for `Draft successfully saved.`, reopen the draft, and repeat the text and media checks. A transient DOM match before saving is not persistence proof.

## Publication

Immediately before publication, summarize the exact body, media, audience, link state, and sensitive-information review result, then request fresh confirmation. After confirmation:

1. Prefer the visible, high-level `Post` button interaction.
2. If the confirmed click is a known no-op because of the Shadow DOM defect, explain the exact fallback and obtain confirmation again before using a lower-level page action.
3. Verify the resulting feed item or success notification. Do not infer success merely because the composer closed.
