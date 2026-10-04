---
name: iris
description: "Iris — Rainbow Messenger. Reads your Gmail inbox, scores every email by urgency and sender importance, drafts replies for the top 5, and produces a daily action list. Saves 45+ minutes per day. Works with any Gmail account via app password — no OAuth dance required."
version: "1.0.4"
metadata:
  openclaw:
    requires:
      env: [GMAIL_ADDRESS, GMAIL_APP_PASSWORD]
      bins: [python3, pip3]
    primaryEnv: GMAIL_ADDRESS
    emoji: "🌈📬"
    homepage: https://clawhub.ai/occupythemilkyway/iris
    tags: [email, gmail, inbox, triage, productivity, iris, ai-drafts, time-saving]
    envVars:
      - name: GMAIL_ADDRESS
        required: true
        description: Your Gmail address (e.g. you@gmail.com)
      - name: GMAIL_APP_PASSWORD
        required: true
        description: "Gmail app password — create at myaccount.google.com/apppasswords (NOT your regular password). Choose: Mail → Other"
      - name: SCAN_COUNT
        required: false
        description: "Number of recent emails to scan (default: 50)"
        default: "50"
      - name: VIP_SENDERS
        required: false
        description: "Comma-separated list of important sender email addresses or domains that should always score high"
        default: ""
      - name: YOUR_NAME
        required: false
        description: "Your name for personalising draft replies (e.g. Alex)"
        default: ""
      - name: YOUR_ROLE
        required: false
        description: "Your role for context-aware replies (e.g. Product Manager)"
        default: ""
---

# Iris — Inbox Intelligence

Read your last 50 emails, score every one by urgency, get draft replies for your top 5, and see a clean action list — all in under 2 minutes.

## What you get

- **Urgency scoring** (0-100) based on keywords, sender importance, age, and reply signals
- **Priority inbox**: top 5 emails that need action today, with one-click draft replies
- **Noise filter**: newsletters, no-reply addresses, and marketing email suppressed automatically
- **VIP tracking**: set specific senders or domains that always score high
- **Daily report saved** to markdown — reference it any time during the day

## Setup (one-time, 2 minutes)

1. Go to **myaccount.google.com/apppasswords**
2. Create an app password — select **Mail** → **Other (Custom name)**
3. Copy the 16-character password
4. Set `GMAIL_APP_PASSWORD` to that password (not your Google login password)

## 🔒 Security

Connects to: `imap.gmail.com` (your credentials, read-only). No external services contacted.
App passwords only scope to the specific app — revoke them instantly in Google Account settings.

---

## Step 1 — Install

```bash
pip3 install rich --break-system-packages --quiet
```

---


---

## ⚡ Upgrade to Iris Pro

👉 **Get Iris Pro** → **ko-fi.com/s/f75940a0ce** — $9 one-time

```bash
openclaw skills install iris-pro
# Set LICENSE_KEY env var to your key from Ko-fi, then run
```

💰 **Bundle deal:** all 5 Pro skills for **$29** → **ko-fi.com/s/7625accf3f** (save $16)

## Step 2 — Triage your inbox

```python
import os, imaplib, email, re
from email.header import decode_header
from email.utils import parsedate_to_datetime
from datetime import datetime, timezone
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

FENCE = chr(96) * 3

console = Console()

GMAIL_ADDR = os.environ.get("GMAIL_ADDRESS", "").strip()
GMAIL_PASS = os.environ.get("GMAIL_APP_PASSWORD", "").strip()
try:
    SCAN_COUNT = int(os.environ.get("SCAN_COUNT", "50"))
except ValueError:
    console.print("[yellow]⚠️  SCAN_COUNT must be a whole number — defaulting to 50[/yellow]")
    SCAN_COUNT = 50
VIP_RAW    = os.environ.get("VIP_SENDERS", "")
VIP_LIST   = [v.strip().lower() for v in VIP_RAW.split(",") if v.strip()]
YOUR_NAME  = os.environ.get("YOUR_NAME", "").strip()
YOUR_ROLE  = os.environ.get("YOUR_ROLE", "").strip()

if not GMAIL_ADDR or not GMAIL_PASS:
    console.print(Panel(
        "[red]GMAIL_ADDRESS and GMAIL_APP_PASSWORD are both required.[/red]\n\n"
        "How to create an app password:\n"
        "1. Go to [bold]myaccount.google.com/apppasswords[/bold]\n"
        "2. Select Mail → Other (Custom name)\n"
        "3. Copy the 16-character password\n"
        "4. Set GMAIL_APP_PASSWORD to that value",
        title="[bold red]⚙️  Setup Required[/bold red]",
        border_style="red"
    ))
    raise SystemExit(1)

URGENT_KEYWORDS = [
    "urgent", "asap", "deadline", "immediately", "action required", "time sensitive",
    "overdue", "past due", "invoice", "payment due", "legal", "lawsuit", "critical",
    "emergency", "final notice", "expires", "expiring", "last chance",
]
REPLY_KEYWORDS = [
    "?", "question", "can you", "could you", "please", "request",
    "following up", "follow-up", "reminder", "let me know", "thoughts",
]
QUESTION_KW = ["?", "question", "can you", "could you", "help", "assist"]
NOISE_PATTERNS = [
    r"unsubscribe", r"newsletter", r"no-reply@", r"noreply@",
    r"marketing@", r"notifications?@", r"donotreply@",
    r"@.*\.(mailchim|sendgrid|constantcontact|klaviyo)",
]
NOISE_SUBJECTS = [
    "sale", "% off", "deal", "offer", "promo", "subscribe", "newsletter",
    "weekly digest", "monthly update", "announcement",
]

def decode_str(s):
    if not s:
        return ""
    parts = decode_header(s)
    result = []
    for part, enc in parts:
        if isinstance(part, bytes):
            try:
                result.append(part.decode(enc or "utf-8", errors="replace"))
            except Exception:
                result.append(part.decode("utf-8", errors="replace"))
        else:
            result.append(str(part))
    return " ".join(result)

def is_noise(sender: str, subject: str) -> bool:
    text = (sender + " " + subject).lower()
    for pat in NOISE_PATTERNS:
        if re.search(pat, text):
            return True
    for kw in NOISE_SUBJECTS:
        if kw in subject.lower():
            return True
    return False

def score_email(subject: str, snippet: str, sender: str, age_hours: float, has_replied: bool) -> int:
    score = 50
    subj_low = subject.lower()
    snip_low = snippet.lower()
    # Urgency keywords
    for kw in URGENT_KEYWORDS:
        if kw in subj_low or kw in snip_low:
            score += 20
            break
    # Reply needed
    for kw in REPLY_KEYWORDS:
        if kw in subj_low or kw in snip_low:
            score += 10
            break
    # VIP sender
    sender_low = sender.lower()
    for vip in VIP_LIST:
        if vip in sender_low:
            score += 25
            break
    # Age penalty/boost
    if age_hours < 2:
        score += 5
    elif age_hours < 24:
        score += 0
    elif age_hours > 48:
        score -= 10
    elif age_hours > 120:
        score -= 20
    # Has been replied to
    if has_replied:
        score -= 15
    return max(0, min(score, 100))

# ── Connect to Gmail ──────────────────────────────────────────────────────────
console.print(Panel.fit(
    f"[bold cyan]🌈 Iris — Inbox Intelligence[/bold cyan]\n"
    f"Scanning [yellow]{SCAN_COUNT}[/yellow] recent emails from [green]{GMAIL_ADDR}[/green]",
    border_style="cyan"
))

try:
    mail = imaplib.IMAP4_SSL("imap.gmail.com", 993)
    mail.login(GMAIL_ADDR, GMAIL_PASS)
    mail.select("INBOX", readonly=True)
except imaplib.IMAP4.error as e:
    console.print(Panel(
        f"[red]IMAP login failed:[/red] {e}\n\n"
        "Checklist:\n"
        "• Is GMAIL_ADDRESS correct? (full email, not just username)\n"
        "• Is GMAIL_APP_PASSWORD a 16-char app password (not your Google password)?\n"
        "• Did you enable IMAP in Gmail Settings → See all settings → Forwarding and POP/IMAP?",
        title="[bold red]Login Error[/bold red]",
        border_style="red"
    ))
    raise SystemExit(1)
except Exception as e:
    console.print(f"[red]Connection error: {e}[/red]")
    raise SystemExit(1)

_, msg_ids = mail.search(None, "ALL")
all_ids = msg_ids[0].split() if msg_ids and msg_ids[0] else []
if not all_ids:
    console.print(Panel("[yellow]Inbox is empty — nothing to triage.[/yellow]", border_style="yellow"))
    raise SystemExit(0)

recent_ids = all_ids[-SCAN_COUNT:] if len(all_ids) > SCAN_COUNT else all_ids
recent_ids = list(reversed(recent_ids))  # newest first

# ── Fetch and score emails ────────────────────────────────────────────────────
emails_data = []
now = datetime.now(timezone.utc)

console.print(f"[dim]Fetching {len(recent_ids)} emails…[/dim]")
for uid in recent_ids:
    try:
        _, raw = mail.fetch(uid, "(RFC822.HEADER FLAGS)")
        if not raw or not raw[0]:
            continue
        raw_header = raw[0][1] if isinstance(raw[0], tuple) else raw[0]
        msg = email.message_from_bytes(raw_header)
        subject = decode_str(msg.get("Subject", "(no subject)"))
        sender  = decode_str(msg.get("From", ""))
        date_str = msg.get("Date", "")
        flags_raw = raw[0][0] if isinstance(raw[0], tuple) else b""
        has_replied = b"\\Answered" in flags_raw

        # Parse date
        try:
            sent_dt = parsedate_to_datetime(date_str)
            if sent_dt.tzinfo is None:
                sent_dt = sent_dt.replace(tzinfo=timezone.utc)
            age_hours = (now - sent_dt).total_seconds() / 3600
        except Exception:
            age_hours = 0

        # Fetch snippet
        body_snippet = ""
        try:
            _, raw_body = mail.fetch(uid, "(BODY[TEXT]<0.300>)")
            if raw_body and raw_body[0] and isinstance(raw_body[0], tuple):
                raw_b = raw_body[0][1]
                if raw_b:
                    body_snippet = raw_b.decode("utf-8", errors="replace").strip()[:200]
        except Exception:
            pass

        noise = is_noise(sender, subject)
        urgency = score_email(subject, body_snippet, sender, age_hours, has_replied)

        # Extract sender name and email
        sender_match = re.search(r'"?([^"<]+)"?\s*<([^>]+)>', sender)
        if sender_match:
            sender_name  = sender_match.group(1).strip()
            sender_email = sender_match.group(2).strip()
        else:
            sender_name  = sender
            sender_email = sender

        emails_data.append({
            "uid":          uid,
            "subject":      subject,
            "sender":       sender_name,
            "sender_email": sender_email,
            "age_hours":    age_hours,
            "snippet":      body_snippet,
            "urgency":      urgency,
            "is_noise":     noise,
            "replied":      has_replied,
        })
    except Exception:
        continue

mail.logout()

# ── Sort and filter ───────────────────────────────────────────────────────────
actionable = [e for e in emails_data if not e["is_noise"]]
noise      = [e for e in emails_data if e["is_noise"]]
actionable.sort(key=lambda e: -e["urgency"])

# ── Display: Priority inbox ───────────────────────────────────────────────────
console.print()
priority_table = Table(
    title=f"📬 Priority Inbox — {len(actionable)} actionable emails",
    box=box.ROUNDED, border_style="cyan"
)
priority_table.add_column("Score",   style="red",    width=7,  justify="right")
priority_table.add_column("From",    style="yellow", width=22)
priority_table.add_column("Subject", style="white",  width=40)
priority_table.add_column("Age",     style="dim",    width=8)
priority_table.add_column("Status",  style="green",  width=10)

for e in actionable[:20]:
    age_str = (f"{int(e['age_hours'])}h" if e["age_hours"] < 48
               else f"{int(e['age_hours'] // 24)}d")
    status  = "✅ replied" if e["replied"] else ""
    score_colour = "red" if e["urgency"] >= 70 else "yellow" if e["urgency"] >= 50 else "dim"
    priority_table.add_row(
        f"[{score_colour}]{e['urgency']}[/{score_colour}]",
        e["sender"][:20],
        e["subject"][:38],
        age_str,
        status,
    )

console.print(priority_table)

# ── Display: Draft replies ────────────────────────────────────────────────────
sig = f"\n\n—\n{YOUR_NAME or 'Best'}{', ' + YOUR_ROLE if YOUR_ROLE else ''}"
top5 = [e for e in actionable if not e["replied"]][:5]

console.print()
for e in top5:
    subj_low = e["subject"].lower()
    snip_low = e["snippet"].lower()
    greeting = f"Hi {e['sender'].split()[0]},"
    if any(k in subj_low or k in snip_low for k in ["urgent", "asap", "deadline", "overdue"]):
        body = "Thank you for flagging this — I'll look into it right away and get back to you shortly."
    elif any(k in subj_low or k in snip_low for k in QUESTION_KW):
        body = "Thanks for your message. To answer your question: [your answer here]\n\nLet me know if you need anything else."
    elif "re:" in subj_low or "fwd:" in subj_low:
        body = "Thanks for the follow-up. Here's where things stand: [brief update]\n\nHappy to jump on a call if that's easier."
    else:
        body = "Thanks for reaching out. I've reviewed your message and [your response here]."
    draft = f"{greeting}\n\n{body}{sig}"
    console.print(Panel(
        draft,
        title=f"[bold]📝 Draft: Re: {e['subject'][:45]}[/bold]  [dim](urgency: {e['urgency']})[/dim]",
        border_style="yellow"
    ))

# ── Display: Stats ────────────────────────────────────────────────────────────
console.print()
console.print(Panel(
    f"📊 [bold]Summary[/bold]\n\n"
    f"Scanned:    [yellow]{len(emails_data)}[/yellow] emails\n"
    f"Actionable: [cyan]{len(actionable)}[/cyan]  |  "
    f"Noise: [dim]{len(noise)}[/dim]  |  "
    f"Already replied: [green]{sum(1 for e in actionable if e['replied'])}[/green]\n"
    f"High priority (70+): [red]{sum(1 for e in actionable if e['urgency'] >= 70)}[/red]",
    border_style="cyan"
))

# ── Save report ───────────────────────────────────────────────────────────────
date_str    = datetime.now().strftime("%Y-%m-%d")
report_file = f"inbox_report_{date_str}.md"
with open(report_file, "w", encoding="utf-8") as f:
    f.write(f"# 🌈 Iris — Inbox Report — {date_str}\n\n")
    f.write(f"**Scanned:** {len(emails_data)}  **Actionable:** {len(actionable)}  **Noise:** {len(noise)}\n\n")
    f.write("## Priority Emails\n\n| Score | From | Subject | Age |\n|-------|------|---------|-----|\n")
    for e in actionable[:20]:
        age_str = f"{int(e['age_hours'])}h" if e["age_hours"] < 48 else f"{int(e['age_hours']//24)}d"
        f.write(f"| {e['urgency']} | {e['sender']} | {e['subject']} | {age_str} |\n")
    f.write("\n## Draft Replies\n\n")
    for e in top5:
        subj_low = e["subject"].lower()
        snip_low = e["snippet"].lower()
        greeting = f"Hi {e['sender'].split()[0]},"
        if any(k in subj_low or k in snip_low for k in ["urgent", "asap", "deadline"]):
            body = "Thank you for flagging this — I'll look into it right away."
        elif any(k in subj_low or k in snip_low for k in QUESTION_KW):
            body = "Thanks for your message. To answer your question: [your answer here]"
        else:
            body = "Thanks for reaching out. [your response here]"
        f.write(f"### Re: {e['subject']}\n\n{FENCE}\n{greeting}\n\n{body}{sig}\n{FENCE}\n\n")

console.print(Panel(
    f"[green]✅ Done![/green]  Report saved to [cyan]{report_file}[/cyan]",
    border_style="green"
))
```
