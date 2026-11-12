---
name: report
description: Open the user's dashboard, the main screen of the tool. Use when the user says /report, "show me my applications", "how is the search going", "what needs me", "open the dashboard", or wants to answer a form's question, change a status, or turn the daily run on or off without typing commands.
model: claude-sonnet-5-5
effort: low
---

# /report: the dashboard

Run from the repo root:

```
npx jev report --open
```

It starts a page on the user's own machine (`http://127.0.0.1:4545`) and
opens it. Nothing leaves the machine. The command keeps running until they
press Ctrl-C. The page has four screens:

- **Today.** One line (sent today, waiting, ready to apply to), the
  totals, and three small charts.
- **Needs you.** Everything only they can do, each with its button:
  - a question a form asked that their profile could not answer. They
    type or pick the answer and press "Save for next run". Nothing is
    sent then: the job goes back in the queue and the next `/apply` or
    daily run fills it with that answer. "Remember for future applications" keeps the
    answer as a standing answer. A question about the right to work has no
    box: that answer is one per country and lives in the profile
    (`/profile`).
  - a form open and waiting (an emailed code, a robot check, a sign-in):
    "Show the form" brings it to the front, "Find the email" opens their
    mail at a search for it. They do it, then `/resume`.
  - a form clicked and never confirmed: "I got a confirmation", or "It was
    not sent".
  - an email the tool could not place: they pick the application and what
    it says.
- **Applications.** Every job, with tabs, a filter, a status select, a
  notes box, and the reply that came back.
- **Automation.** The daily run: an "Apply automatically" switch with a
  time, the next run, "Pause future runs" (removes the schedule),
  "Stop it after this application" while a run is working, their daily
  rules as a form, and today's result in one line. Turning the switch on installs the schedule;
  that is their click, not yours.

`npx jev report --static applications/report.html` writes a snapshot page
with Today and Applications only, for keeping or sending. Nothing can be
changed from a snapshot.
