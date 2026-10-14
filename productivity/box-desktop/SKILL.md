---
name: box-desktop
description: >-
  When a task needs your own desktop or browser, such as a website with no
  connector, a GUI app, or a sign-in only the user can complete, read before you
  dispatch the first browser or desktop subagent.
---
# The box desktop

You hold the read-only Screenshot tool to see its current screen, confirm where a flow landed, or check on a running subagent. You cannot click, move, type, press keys, scroll, or wait on the desktop yourself. Delegate every browser and desktop interaction to a subagent. Do not bypass this boundary with Shell-driven GUI automation such as xdotool, or by driving the box browser from Shell: no CDP attach, no Playwright, Puppeteer, or `websocket-client`, no `/json/new`, no cookie-DB scraping, and no page JS eval over DevTools.

- Delegate the outcome, constraints, required values, and success criteria, not browser or desktop steps. Prescribe a modality only when that modality is itself part of the desired result; otherwise let the child choose.

- When you know the destination URL, whether one the user pasted or one you can construct (a site's search/filter URL like `https://www.amazon.com/s?k=bread+flour`), put that exact URL in the task, as specific as the site's query params allow, so the subagent opens it directly instead of clicking through the site to rebuild it.

- For bulk or structured data, don't type it in by hand: generate the file with Shell (e.g. a CSV), inspect it with Read when useful, then have the subagent import or upload it, far faster and more reliable than entering values one by one.

- When it returns, read its report before acting. If it stopped short or hit a step only the user can do, that's your cue to follow up or hand off the box.

- When `request_cookie_origin_approval` is among your tools, try the user's Chrome cookies first for a sign-in. List origins, and if the site is listed, request it. Only when that path is exhausted (not listed, denied, or page still wants a fresh login) do the sign-in in the box browser. Follow that tool's approval and site-exception rules.

- When a page needs the USER to type (login, address, phone, OTP) and `request_user_form` is among your tools, Read and follow the `in-chat-forms` skill first. Have the child open the page and report fresh snapshot targets; use a form only when fields are fillable. Do not jump to `request_box_help` just because a site needs a password.

- For steps that need the user, use `request_box_help` when `request_user_form` is not offered or a form cannot express or reach the step, including non-text/native steps. A structural preflight refusal is final, so don't re-issue the same form. Don't pre-ask "hand you the box?" The handoff is the ask.
