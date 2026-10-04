---
name: save
description: Persist a proven ad-hoc mcx chain as a durable named chain. Use only when the user explicitly asks to save, register, name, preserve, or reuse an MCP workflow. Writes the proven source to a script file when necessary, registers it with mcx, verifies execution by name, and confirms the generated personal skill. Do not use merely because an ad-hoc chain succeeded.
---

# Save an mcx chain

Persist only an already-understood workflow. If the chain has not run
successfully yet, invoke `/mcx:new` first and prove the digest before saving it.

## Procedure

1. Confirm the user explicitly requested persistence.
2. Reuse the exact proven source. If it came from a heredoc, write it to
   `chains/<name>.<ext>` with a one-line opening comment that describes the
   workflow. Do not redesign the chain while saving it.
3. Keep inputs in `args` and emit only the proven compact digest. Add a JSON
   Schema only when validation is useful and its shape is known.
4. Register the script:

   ```sh
   mcx register ./chains/<name>.<ext>
   ```

   The filename, extension, and opening comment supply the default name,
   language, and description. Use overrides only when the user requested them.
5. Run the registered name with the same representative args and verify that its
   digest matches the ad-hoc run:

   ```sh
   mcx run '{"...":"..."}' <name>
   ```

6. Confirm that `mcx list` shows the user-layer chain and that registration
   synchronized its generated personal skill.

Registration stores the source inline in the user registry. Never register a
workflow proactively; successful one-time execution is not consent to persist.
