---
name: spike-contract
description: Frame a spike so its result is a decision, with the question, the cheapest experiment, a numeric exit criterion, the measured result and the machine it ran on. Use when asked to "spike", "prototype to find out", "de-risk", or "check whether X is feasible", and when writing the spikes section of a plan or README.
---

# The spike contract

A spike answers one question with the cheapest experiment that can answer it, and it is judged
against a number written down before the experiment ran. Everything else is a prototype
looking for a purpose.

## Before running anything, write the row

Each spike gets one entry, in the project's spikes README or the plan's addendum:

- **Question** — one sentence, answerable yes/no or with a number. "Can the core simulate
  14 million cells at one tick per second on the target machine?"
- **Cheapest experiment** — the smallest thing that produces the number. A throwaway script,
  a synthetic dataset, a stub of the real path. Name what is faked.
- **Exit criterion** — the number and the comparison. "Under 800 ms per tick, mean of 100
  ticks." Written before the run, not adjusted after.
- **Status** — `not started`, `running`, `passed`, `failed`, `inconclusive`, with the date.
- **Machine** — the hardware and OS the budget was measured on. A budget measured on a
  laptop does not transfer to CI or to the target machine without saying so.

## Run it

- Record the exact command and the raw output, in the row or in a linked file.
- Run enough times to see the variance. Report the mean and the spread, not the best run.
- If the experiment had to change mid-way, update the row's experiment line and say why. If
  the criterion had to change, that is a new spike.

## Read the result against the number

- **Passed** means the measured number met the criterion on the named machine. Nothing else
  is "passed".
- **Failed** is a result, not a setback. Write what was learned and what the next cheapest
  experiment would be.
- **Inconclusive** means the experiment could not produce the number. Say what blocked it.

Never read a spike against impressions. "It felt fast" and "it seemed to work" are not
statuses.

## Order and dependency

Run the spike that could invalidate the most other work first. Name the fallback if it fails,
so the plan already knows what happens on a `failed`.
