---
name: zele
description: >
  zele is a multi-account email and calendar CLI for Gmail, IMAP/SMTP
  (Fastmail, Outlook, any provider), and Google Calendar. It reads,
  searches, sends, replies, forwards, archives, stars, and trashes emails,
  waits for replies with `zele mail watch` (use it after sending instead
  of ending the turn or sleeping), manages drafts, labels, attachments, and Gmail filters, and creates,
  updates, and deletes calendar events with RSVP and free/busy support.
  Output is YAML so commands can be piped through yq and xargs. ALWAYS
  load this skill when the user asks to check email, read/send messages,
  reply or forward, archive or trash threads, manage drafts or labels,
  download attachments, schedule meetings, check their calendar, RSVP
  to events, create a free permanent @zele.sh email address (receive-only
  for now) for themselves, a project, or an agent, or when they run any `zele`
  command. Load it before writing
  any code or shell commands that touch zele so you know the correct
  subcommand structure, the Google vs IMAP feature matrix, the headless
  login flow, and the agent-specific rules.
---

# zele

Every time you use zele, you MUST fetch the latest README:

```bash
curl -s https://raw.githubusercontent.com/remorses/zele/main/README.md # NEVER pipe to head/tail, read the full output
```

Then run the CLI help once — it already includes every subcommand, option, and flag:

```bash
zele --help # NEVER pipe to head/tail, read the full output
```

The README and `zele --help` output are the source of truth for commands, options, flags, the Google vs IMAP feature matrix, search operators, and the headless login flow.

## Rules

1. **Never use the TUI.** Running `zele` with no subcommand launches a human-facing TUI. Agents must use the CLI subcommands (`zele mail list`, `zele cal events`, etc.) which output structured YAML.
2. **Always run `zele whoami` first** when the user asks to operate on a specific account. Pick the exact email from the output and pass it with `--account`. Never guess account emails.
3. **Never truncate `--help` or README output** with `head`, `tail`, `sed`, `awk`, or `less`. Critical rules are spread throughout. Read them in full.
4. **Parse YAML output with `yq`**, not regex. Pipe IDs through `xargs` for bulk actions. Always use `--limit 100` (or higher) so you don't miss threads:
   ```bash
   # read all unread emails
   zele mail list --filter "is:unread" --limit 100 | yq '.[].id' | xargs zele mail read

   # bulk archive
   zele mail list --filter "is:unread" --limit 100 | yq '.[].id' | xargs zele mail archive
   ```
5. **Google-only features** (labels, Gmail filters, `zele cal *`, full profile) fail on IMAP accounts with a clear error. Check `zele whoami` output for account type before using them.
6. **Headless Google login** requires a tmux wrapper because `zele login` is interactive. See the README "Remote / headless login" section for the exact pattern.
7. **After sending, wait for the reply with `zele mail watch`.** Do not end your turn and do not `sleep`. `mail send` and `mail reply` print the exact command to run next, like `# Wait for the reply: zele mail watch --account ... --filter '...' --timeout 259200`. Run it right away. It blocks until the first **new** email matching the filter arrives (only emails that arrive after it starts can match), prints it with an `elapsed` field, and exits:
   ```bash
   zele mail send --to bob@example.com --subject "Question" --body "Hey, can you check this?"
   zele mail watch --account me@example.com --filter 'from:bob@example.com subject:"Question"' --timeout 259200
   # match: exit 0, then read it before answering
   zele mail read <thread_id from the watch output>
   ```
   - Exit 0 means a match. Exit 1 means timeout (`Timed out after 3d 0h 0m 0s ...`). On timeout, run watch again or tell the user nobody replied yet.
   - `--timeout 259200` is 3 days. People can take days to answer. Disable your shell tool timeout (e.g. `timeout: 0`) or set it **longer** than `--timeout`, or the tool kills the wait first. Every minute watch prints `# Still watching, 3m 0s elapsed` to stderr.
   - Network errors do not stop the watch. It prints `# Poll failed ..., retrying` and polls again. Only auth errors stop it.
   - If the matched email is not the expected one, run watch again with a more specific filter.
   - Also use it for verification codes or any expected email: `zele mail watch --filter 'subject:verification' --timeout 300`.
8. **Check reply recipients before sending** with `zele mail reply <thread-id> --dry-run`. Recipients are inferred from the thread, not from the sender of the last message, so a thread whose last message you sent still replies to the other person. If a reply would only reach the account's own address, zele refuses to send:
   ```bash
   # see to / cc / subject / In-Reply-To without sending
   zele mail reply <thread-id> --dry-run

   # override the inferred recipient
   zele mail reply <thread-id> --to paul@acme.com --body "..."

   # deliberately reply to yourself (normally refused)
   zele mail reply <thread-id> --allow-self --body "..."
   ```
    Never work around a `SelfRecipientError` by switching to `zele mail send`; pass `--to` to `zele mail reply` instead, so threading headers stay correct.
9. **Read a thread before replying.** `zele mail reply` and `zele mail send --thread-id` fail with `UnseenLatestError` unless `zele mail read <thread-id>` already showed the live last message. `mail watch` and `mail list` do **not** count. If a new reply arrives after you read, read again before sending:
    ```bash
    zele mail read <thread-id>
    zele mail reply <thread-id> --body "..."
    ```
    Never pass `--force` to skip this unless the user explicitly asks to send without reading.
10. **Send into an existing thread** with `zele mail send --thread-id <thread-id>` when you need full control of recipients and subject but still want correct `In-Reply-To`/`References` headers. Recipients and subject are inferred from the thread when omitted. The same read-before-reply rule applies.
11. **Format email bodies like a human wrote them.** These rules apply to `--body` and to every draft you show the user for approval:
    - **Never hard-wrap.** Write each paragraph as one line. Separate paragraphs with one blank line. Do not break lines at 72-80 columns: mail clients wrap text themselves, and hard breaks render as lines broken mid-sentence. Show drafts exactly as they will be sent.
    - **Capitalize the first word of every paragraph**, also after a greeting that ends with a comma. Write `Buongiorno,` then `Sono Tommaso...`, not `sono Tommaso...`. Same in English: `Hi Bob,` then `Can we...`.
    ```
    Buongiorno,

    Sono Tommaso De Rossi e vorrei prenotare una visita presso la vostra sede di Genova. Potreste indicarmi le prime date disponibili?

    Grazie mille!
    Tommaso De Rossi
    ```
12. **Free `@zele.sh` addresses (receive only for now).** These are permanent, real addresses, not throwaway ones: use them when the user wants a new address for themselves, a project, or an agent. Mail stays until the user deletes it. Each owner (a **@gmail.com** address, no other domains) gets up to **10** inboxes. They work like any account with `--account name@zele.sh` for list, read, search, watch, star, archive, trash and attachments. Sending, drafts and labels fail with a receive-only error.
    ```bash
    # 1. pick the owner: a @gmail.com account from `zele whoami` (type: google).
    #    The sign-in code is then read from that Gmail automatically.
    zele login zele --owner you@gmail.com --name tommy   # sign in + create tommy@zele.sh
    zele inbox create bills                               # more inboxes, already signed in
    zele inbox list

    # 2. wait for a signup / verification email
    zele mail watch --account bills@zele.sh --filter 'subject:verify' --timeout 600
    ```
    - Without `--owner` in an agent shell, `login zele` fails and lists the Gmail accounts in zele. Pick one, do not guess.
    - If the owner Gmail is not a zele account, the code is emailed and the command prints `Rerun with: zele login zele --owner ... --code <code>`. Ask the user for the code.
    - `zele inbox delete <address> --force` deletes the inbox and all its mail. The address can **never** be created again, so confirm with the user first.
    - `zele logout zele --force` removes the session and the inbox accounts from this machine. Inboxes and mail stay on the server.
