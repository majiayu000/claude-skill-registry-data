---
name: run
description: Launch this project's app (server, CLI, web page) and check that it actually works
---
# Run the app

1. Find how it starts: FORGE.md/README, package.json scripts ("dev", "start"), manage.py, app.py/main.py,
   Makefile, docker-compose. If dependencies are missing, install them (ask first if that's large).
2. Start it:
   - Servers and dev servers run in the background (run_shell moves them there automatically); note the
     port from the log, then check the page with web_fetch http://localhost:<port>/ and open_url it
     so the user sees it.
   - A CLI or script: run it with a realistic example input.
   - A static site: open_url the index.html (file:///…).
3. Check it works: the page loads without errors, the main action does what it should, the log has
   no tracebacks. Read the log file with read_file if something looks wrong, fix, and try again.
4. Tell the user the address or command, what you checked, and how to stop it (process tool).
