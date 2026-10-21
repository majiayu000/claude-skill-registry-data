---
name: website-contact-form
description: >
  Add a contact form to a new-website site that needs no server and no setup: the
  visitor fills in a few fields, presses a button, and their own email program opens
  with a message to the owner, ready to send. Nothing is sent or stored by the site.
  Adds a form component, its texts in English and German, one small script of the
  site's own (so a strict Content-Security-Policy holds), and tests/mail-form.spec.ts.
  The owner's address is always shown under the form for visitors without a mail
  program or without JavaScript. Run when new-website Q2 asks for a contact form, or
  later when the owner wants one. Trigger phrases: "contact form", "add a form",
  "enquiry form", "visitors should be able to write to us", "kontaktformular". Not
  for newsletter sign-up, file uploads, or anything that has to be stored.
---

# Website contact form — the visitor's own mail program sends it

Our suggestion for contact on a small site: a short form whose button opens the
visitor's own email program with a message to the owner already written. The visitor
reads it, presses Send, and it arrives like any other email. There is no server work,
no account and no setting behind it.

## Why this form (say this to the owner, in your own words)

- **Nothing to set up.** No account, no password or token, no change to the domain's
  mail settings. It works on any host, today, and on a preview address too.
- **No spam through the form.** It sends nothing, so there is nothing for a bot to
  fill in and fire off: every message needs a real mail account and a person pressing
  Send. Spam sent straight to the address is another matter, the same as for any
  address on any site; the form keeps it out of the page as plain text, as the
  starter's email link does, which stops the simple address collectors.
- **No company in between.** The message goes from the visitor's mailbox to the
  owner's, like any email. So the privacy page needs no paragraph about a service
  that handles messages: its section on contact by email already covers it (§4).
- **The visitor keeps a copy** in their Sent folder, and the owner answers with Reply.

And the honest weak spots, so the owner hears them from you first:

- **Some visitors have no mail program set up.** Someone who reads mail only in a
  browser (webmail), or sits at a shared computer, presses the button and gets
  nothing, or a mail program they never use. That is why the plain address always
  shows under the form, ready to copy, and the line after the button says to use it
  if nothing opened.
- **The site never learns whether the visitor pressed Send.** A message can be
  written, opened and then not sent. No form counts sent messages here.

If the owner needs either of those solved (messages from every visitor whatever their
setup, or a count of them), this is the wrong tool: see §0.

## 0. Is this the right tool? (ask before installing)

1. **Is a form wanted at all?** For a handful of enquiries a year, the plain email link
   the starter already has (`<EmailLink>`) does the job. Say so.
2. **Is "the visitor's own mail program sends it" enough?** Yes for nearly every small
   site. No when the owner must receive messages from visitors who only use webmail, or
   must know how many were sent. Then say plainly that this skill does not fit, and
   point to `new-website/references/WEBSITE_ARCHITECTURE.md` Tier 2: a form that sends
   through a server, which needs a mail service, settings only the owner can create,
   and a paragraph on the privacy page. Not built by this skill.
3. **Are file uploads or a newsletter sign-up wanted?** Different problems; not this.

## 1. What it adds to the site

| File | From this skill's `templates/` | What it is |
|---|---|---|
| `src/components/MailForm.astro` | `MailForm.astro` | the form, and the address line under it |
| `src/components/mail-form-text.ts` | `mail-form-text.ts` | everything the form says, in English and German, and the longest message it takes |
| `public/js/mail-form.js` | `mail-form.js` | the script: shows the form, builds the `mailto:` link, opens it |
| `tests/mail-form.spec.ts` | `mail-form.spec.ts` | the form as a visitor meets it: the link the button opens (address, subject, every field, encoding), an empty field, labels and keyboard order, the page without JavaScript, a strict Content-Security-Policy, and every text against the site's tone rules |

The templates are in this skill's `templates/` folder, beside this SKILL.md; the bundled
copy of the skill on a handed-off repo has them too. Install all four.

**How it works, in one paragraph.** The owner's address goes into the HTML encoded the
way `EmailLink` encodes it (`src/lib/obfuscate.ts`), never as plain text. The script, a
file of the site's own under `public/js/` rather than an inline script, so a strict
`script-src 'self'` policy lets it run, shows the form, and when the button is pressed
decodes the address and opens `mailto:<address>?subject=…&body=…`. The body is the
visitor's message as typed, less any empty space (spaces, tabs, blank lines) at its very
start and end: they write their own greeting and sign-off, and their mail program says
who they are. Every other field the visitor filled in follows under it as "Label:
value", so a field the owner adds later goes into the mail by its label with no change
to the script. Without JavaScript the form stays hidden, since it could do nothing, and
the address line under it is what the visitor sees.

**The spec needs `toneViolations`** from the site's `tests/_helpers.ts`, the tone rules
its pages are held to. A site made from an older starter lacks it, and `npm run check`
says `has no exported member 'toneViolations'`. Then first bring that file up to date
from the starter's (`new-website/templates/astro/tests/_helpers.ts`): take
`toneViolations` and the rules above it, keep the site's own `PAGES`. Take the
starter's `tests/tone.spec.ts` with it, so the pages and the form read one list. Before
replacing the site's `tone.spec.ts`, compare its rules and its `ALLOWLIST` with the
starter's: a word the site added goes into the same place in `_helpers.ts`, or the site
loses it.

## 2. Install (on a branch, as a pull request: `AGENTS.md` §2)

1. Copy the four files to the places in §1 (`mkdir -p public/js` first).
2. Put the form on a page, inside that page's `<Base>`:
   ```astro
   ---
   import MailForm from '../components/MailForm.astro';
   ---
   <MailForm to="<the address messages go to>" subject="<what the visitor comes for>" />
   ```
   Ask the owner for the address. The starter's encoding takes only plain addresses:
   letters, digits and `. _ % + -` before the `@`, and the build stops with a clear
   message on anything else. A **new** `/contact` page is a new page: work through
   `AGENTS.md` §6 (`PAGES`, `llms.txt`, share card, a link to it). One form per page:
   its ids are fixed.

   **The subject line** (`subject`, required: the build stops without it). It is the
   first thing the visitor reads in their mail program, and what stays in their Sent
   folder. So let it name what they came for, in their words, rather than the website:
   an architects' office "Anfrage Bauvorhaben", a holiday flat "Booking request", a
   consultant "Project enquiry". The mail then starts as their own request, not as a
   message to a website. Take it from the site's offer and the primary action in
   `CONTENT_GUIDE.md`, in the page's language, and keep it short, about 40 characters,
   so a mail program's list shows all of it. A page for one offer can pass its own.
   Propose one or two and let the owner choose: these are their customers' first words
   to them. The plain address under the form carries the same subject.
3. **Language.** The form speaks the language of the page it is on, by itself: a page
   built with `<Base lang="de">` on an English site gets a German form. `Base.astro`
   hands the page's language down (`Astro.locals.lang`); on a site with several
   languages it is the page's locale.
   `lang="…"` overrides; then set `LANG` in the spec too (step 4). English and German
   are built in, with no form of address in German, so the form fits a "du" site and a
   "Sie" site. Any other language: "Add a language" below, first. A form in a language
   with no texts stops the build.

   **A site made from an older starter** lacks the line in `Base.astro`. On a site
   without Astro's language routing, a form without `lang` then stops the build with a
   message naming the line (with routing, the page's locale stands in). Add
   `Astro.locals.lang = lang;` after the props in `Base.astro`, and the declaration
   `declare namespace App { interface Locals { lang?: string } }` to `src/env.d.ts`:
   create the file from the starter's if the site has none, and keep what a site's own
   file already declares. Without the declaration, `npm run check` fails on the line.
4. In `tests/mail-form.spec.ts` set `PAGE` (the page with the form), `TO` and
   `SUBJECT` (the address and the subject from step 2). The spec fails while one is
   empty, and holds the subject to the site's tone rules. `LANG` only if the page passes
   `lang`. One copy guards one form:
   with the form on pages in two languages, copy it once per language
   (`tests/mail-form.de.spec.ts`), each with its own `PAGE` and `SUBJECT`.
5. **Fields.** The form asks for the message, nothing else: the visitor's name and
   email address come with their mail, and they greet and sign as they like. A field
   the owner wants (a phone number, a date) goes inside the form with a `<label for>`
   and a `name`, before the button. It reaches the mail under the message as "Label:
   value", and the spec's label and keyboard test then needs that field in its `order`
   list. A field that asks for more personal data than the message also goes into the
   privacy page (§4).
6. `npm run check && npm test`.

### Add a language

On a new site in that language, or when a site gains it later. Translate from the
English, all of it in one go.

1. **Read the site's voice first**: its `CONTENT_GUIDE.md` (in German the register, "du"
   or "Sie") and the tone rules in `tests/_helpers.ts`. Where the language allows, do as
   the German texts do and address nobody.
2. In `src/components/mail-form-text.ts`, copy the `en` entry of `TEXT` under the
   language's two-letter code (`fr`, not `fr-CA`) and translate every value; the
   comment above `TEXT` says where each one shows. `npm run check` fails while one is
   missing, and the spec holds every text to the tone rules. For a language without
   rules of its own in `tests/_helpers.ts` that is the ban on the long dash alone: read
   the texts against step 1 yourself, and if the owner speaks the language, ask them to
   read the form once.
3. **The address hint** a visitor without JavaScript reads ("name [at] example [dot]
   com") takes its word for "dot" from `DOT_WORD` in `src/lib/obfuscate.ts` (English and
   German there); add the language's word, or the hint says "dot".
4. The page and its test, as in §2 steps 3 and 4.

## 3. Try it once (the owner)

It works the same on a laptop as on the live site, since there is nothing on a server
to wait for. After `npm run build && npm run preview`, or on the preview address of the
pull request:

1. The owner fills in the form and presses the button. Their mail program opens with a
   new message: to the address from §2, the subject line and the message as they
   typed it, umlauts and line breaks included.
2. They send it to themselves and see it arrive.
3. Nothing opened: their computer has no mail program set up for `mailto:` links. That
   is exactly what some visitors meet, and why the address shows under the form. On a
   Mac it is set in Mail's settings, on Windows under default apps; in Chrome a webmail
   such as Gmail can ask to open these links. Not a fault of the form.

## 4. The privacy page

The starter's privacy page already has a section on contact by email ("4. Contact by
email", German "4. Kontakt per E-Mail"), naming the name, the address and the message.
That is what this form produces: an email, sent by the visitor. **Nothing to add**, and
no processor paragraph, since no service handles the message on the way.

Check two things only: the section is still there (a rewritten privacy page may have
lost it; then write it, covering what is processed, why, the legal basis and how long
it is kept), and any field added in §2 step 5 that asks for more than the message is
named in it. Like the kit's other legal drafts, a baseline, not legal advice.

**With Plausible on**, a press of the button sends one "Email Tap" event, the same one
the starter's email link sends (nothing typed goes with it). Section 3 of the starter's
privacy page (EN `privacy.astro`; German `_datenschutz.astro`, served as
`datenschutz.astro` once a German site renames it) already says so ("a button that opens your
email program"). An older site's privacy page may lack that sentence, and its own
`src/components/EmailLink.astro`, which shows the address under the form, may not count
clicks yet (no `addEventListener` in it). Take whatever is missing from the starter: the
sentence, the click listener, or both. The form sends its event
either way, so the sentence is not optional on a site that runs Plausible. In Plausible's
installer leave "Form submissions" unticked: whether Plausible would count this form a
second time was not checked.

**In analytics server mode** (`ANALYTICS.mode: 'server'`, new-website Q5) the button is
not counted: no Plausible script runs, so the form's call does nothing, and counting it
from the server would mean passing what the visitor typed through it (owner's decision,
2026-10-15). The mail program opens as before. The privacy page's server-mode slots
already leave the button out.

## 5. What it does not do

- **No sending, no storage, no count of sent messages.** The site never learns whether
  a message was sent. The owner's mailbox is the record. With Plausible on, the press of
  the button is counted (§4): a visitor who asked to write, not an opened mail program
  and not a message.
- **No help for a visitor without a mail program**, beyond the address under the form
  and the sentence that points to it.
- **Very long messages.** The form stops at 2,000 typed characters (`LIMITS` in
  `mail-form-text.ts`). In the link they become more: about 2,800 for English prose,
  more with umlauts and line breaks. Some mail programs cut a very long link, and at
  what length was not measured, so a long message may arrive cut in some of them. The
  visitor sees it before pressing Send, and can write on in their mail program.
- **The address line under a strict Content-Security-Policy.** The form works under
  `script-src 'self'` (the spec proves it). The address under it, the starter's
  `EmailLink`, decodes through an inline script, so under such a policy it stays as the
  readable "name [at] example [dot] com" hint and cannot be clicked. The starter's own
  policy (`public/_headers`) allows inline scripts, so a site that kept it is not
  affected.
- **Not checked in every mail program.** The link follows the standard for `mailto:`
  links (RFC 6068), and the spec checks it to the character. How each mail program
  shows it was not tried beyond the owner's own (§3).

## Boundaries (do not duplicate)

- Which hosting tier a site needs: `new-website` §1 Q2 and
  `references/WEBSITE_ARCHITECTURE.md`.
- Getting the suite green, and what else to test on a new feature: `website-qa` §1b.
- The privacy page as a whole: the starter's `privacy.astro` and `_datenschutz.astro`.
- The address link alone, with no form: the starter's `EmailLink`.

## Done means

The owner chose the form knowing its weak spots; it is on its page in the site's
language with the right address; `npm test` is green with `PAGE` and `TO` set; the
privacy page's section on contact by email is in place; and the owner has opened one
message from it in their own mail program and seen it arrive.
