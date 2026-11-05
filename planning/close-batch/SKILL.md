---
name: close-batch
description: Close a planning batch whose units are all approved - move open items, finish the time log, mark it done, and delete the batch folder. Use when every unit of the batch has an approved review, or the user says "close batch N".
---

# Close a batch

1. **Check** that every unit of `batches/NN/` has a last review round that says "approved". If not, list the ones that wait and stop.
2. **Move what is open**: proposed units stay in `proposed/` (tell the user they wait for approval); open items in the report go to a later unit, `LATER.md` or `USER.md`. Nothing open stays only in the folder.
3. **Time log**: every unit and change round has a complete row (times, effort before and after, the wrong factor, stats).
4. **Background**: when the last unit of a topic is done, remove its section from `BACKGROUND.md`.
5. **Mark** the batch done in `BATCHES.md`, then `git rm -r batches/NN` and commit `Done: Batch N` with the main commit. Git keeps the units, reviews and report.
6. **Calibrate** every 2 batches: compare agent time per effort level and the factors that were wrong most often; propose changes to `EFFORT.md` to the user.
7. **Report**: the batch is closed, what moved where, what waits for approval, the passes now due (`PASSES.md`; run them with `/passes` before the next batch), and the next batch's 5 units.
