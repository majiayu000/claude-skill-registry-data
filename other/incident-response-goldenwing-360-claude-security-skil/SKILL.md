---
name: incident-response
description: Run a structured response to a suspected web or server compromise. Follows SANS PICERL — Preparation, Identification, Containment, Eradication, Recovery, Lessons Learned — and includes a post-mortem template. Invoke when a site is defaced, when malware or webshells appear, when admin accounts arrive unannounced, or when a provider sends an abuse notice.
---

# Incident Response

A practical IR runbook for small teams and solo operators. Built around the SANS PICERL phases: **Preparation → Identification → Containment → Eradication → Recovery → Lessons Learned**.

## When to invoke

You are in incident territory if any of these are true:

- A site you operate is defaced, redirecting, or serving content you did not publish
- A webshell or backdoor file has been found
- An admin/root account appeared that nobody on the team created
- A hosting provider, registrar, or upstream sent an abuse notice
- A credential you control turned up in a public dump
- Traffic is being dropped from your IP by major email/DNS providers (sign of being on a blocklist)

If you only **suspect** something is wrong, treat it as a real incident until you have evidence otherwise. False positives are cheap; missed compromises are expensive.

## Phase 1 — Preparation (before anything happens)

Have these ready before the first incident:

- **Out-of-band contact channel** (Signal/Telegram/phone) — your primary work tool may itself be compromised
- **Backup of last-known-good** for every production system, verified restorable
- **Inventory** of who has access to what (hosting, DNS, registrar, repo, secrets store)
- **A pre-written holding statement** for customers ("we are investigating an issue affecting X, more soon")
- **A way to reach your registrar fast** — domain hijacks are catastrophic and the registrar is often slowest in real time

## Phase 2 — Identification

Goal: confirm a real incident and scope it.

```bash
# Webserver: who is hitting unusual paths?
sudo tail -n 10000 /var/log/nginx/access.log | awk '{print $7}' | sort | uniq -c | sort -rn | head -30

# Auth log: failed + successful root/SSH activity
sudo grep -E 'Failed password|Accepted' /var/log/auth.log | tail -100

# Currently logged-in users + open sessions
who -a
last -n 30

# Listening processes — anything new?
sudo ss -tlnp

# Crontabs at every level
for u in $(cut -d: -f1 /etc/passwd); do sudo crontab -u "$u" -l 2>/dev/null | sed "s|^|[$u] |"; done
sudo ls -la /etc/cron.* /var/spool/cron/

# Recently modified files in sensitive trees
sudo find /var/www /etc /usr/local/bin -mtime -30 -type f 2>/dev/null
```

Document everything you find as you find it. Timestamps in UTC. Append-only — never edit prior entries.

## Phase 3 — Containment

The aim is to stop the bleeding **without destroying evidence**. Do not just delete malicious files immediately; snapshot first.

### Short-term containment

1. **Snapshot** the affected filesystem (`tar`, hosting-panel snapshot, VM snapshot) and the database. Store off-host.
2. **Pull the site off the internet** at the cheapest layer that works:
   - Cloudflare proxy → site-wide maintenance page (rule)
   - Webserver → return 503 from the vhost
   - Last resort → stop the service
3. **Rotate the credentials you know are exposed** — keep a list of every credential you rotate, when, and by whom.
4. **Revoke active sessions** on admin panels and force re-login.
5. **Block known-bad IPs** at the edge if you have a clear indicator.

### Long-term containment (hours/days)

- Move the service to a clean host before recovery if root cause is unclear
- Add WAF rules / CDN rules for the attack pattern
- If lateral movement is plausible (shared hosting, shared SSH keys, shared CI), assume every adjacent system is at risk and apply the same containment there

## Phase 4 — Eradication

You cannot eradicate what you have not understood. Before you wipe and reinstall, answer:

- **Entry vector** — how did the attacker get in?
- **Foothold** — what did they install (webshell, cron, systemd unit, modified binary, DB-resident backdoor)?
- **Persistence** — would a reboot or a file-restore alone evict them?
- **Lateral movement** — did they reach other systems?

Only then:

1. Rebuild from known-good (golden image, fresh OS install, fresh CMS install).
2. Restore data from a backup taken **before** the foothold timestamp. If you cannot determine when the foothold was placed, treat all backups as suspect and restore data selectively (export rows, not full dumps).
3. Patch the entry vector specifically. If you do not know the vector, you have not finished investigating.
4. Re-issue all secrets that touched the compromised system.

## Phase 5 — Recovery

1. Bring the service back up in a staged way — internal first, then a small percentage of traffic, then full.
2. Watch the logs you set up in Phase 2 for repeat indicators.
3. Keep elevated monitoring for at least 30 days. Attackers often return.
4. Notify users if their data may have been exposed. Be honest about what you know and do not know. In most jurisdictions personal-data breaches have legal notification deadlines (e.g. 72 hours under GDPR Art. 33) — check your jurisdiction.

## Phase 6 — Lessons learned

Write the post-mortem within a week, while the details are fresh. Structure:

```
# Post-Mortem — <incident name> — <date>

## Summary
One paragraph: what happened, impact, current state.

## Timeline (UTC)
- 2026-MM-DD HH:MM — first indicator observed
- 2026-MM-DD HH:MM — confirmed incident, containment started
- ...

## Impact
- Systems affected
- Data potentially exposed
- Users notified, regulators notified, etc.

## Root cause
The single technical reason this was possible. Be specific.

## Contributing factors
Process / monitoring / staffing gaps that let it reach production or stay undetected.

## What worked
Things to keep doing.

## Action items
Each with an owner and a due date. Track them somewhere durable (issue tracker).

## Indicators of compromise (IOCs)
File hashes, IPs, user-agents, domain names. Keep these — they are useful for next time.
```

The post-mortem is for learning, not blame. Name what failed; do not name who failed.

## A note on legality and ethics

- Only run this against systems you own or have explicit written authorization for.
- Notify affected users where required by law and where it is the right thing to do regardless.
- Do not "hack back" — it is illegal in most jurisdictions and unhelpful in all of them.
- Preserve evidence in a way that would stand up if law enforcement gets involved.

## What this skill will not do

- It will not help you cover up a breach or delay required notifications.
- It will not perform offensive actions against any system, including ones attacking you.
- It is not a substitute for a qualified IR firm for serious incidents. Know your limits and call for help.
