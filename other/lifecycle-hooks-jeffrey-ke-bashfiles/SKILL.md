---
name: lifecycle-hooks
description: Identify code where a stable process contains special-case logic on behalf of outside participants. Refactor using lifecycle hooks so the process broadcasts events and participants respond independently. Use when adding a new participant requires editing the process loop, or when you find isinstance checks or feature flags inside a generic loop.
argument-hint: [file-or-function to analyze]
---

# Lifecycle Hooks

## The Core Problem

You have a stable process — a training loop, a request cycle, a test runner — and objects that want to participate at specific moments. The naive approach leaks knowledge of every participant into the process:

```python
for epoch in range(num_epochs):
    epoch_info = run_epoch(...)
    eval_info = eval_model(...)

    if wandb_enabled:
        wandb.log(...)
    if checkpoint_enabled and eval_info.avg_val_loss < best_loss:
        save_checkpoint(...)
    if early_stopping_enabled and plateau_detected:
        break
```

Adding a Slack notifier, a CSV logger, or a learning rate plotter means opening this loop and adding another branch. The process now *knows* about every participant.

**The telltale sign**: when you catch yourself writing special-case logic *inside* a process on behalf of *outside* things, you need lifecycle hooks. The process should be deaf to who's watching.

## Why It Happens: Heterogeneous Participants

The training loop runs the same steps every epoch — forward, backward, step, log. That part never changes. But the *things watching the loop* differ wildly:

- WandB wants to call `watch(model)` once, then log metrics every epoch
- A checkpoint saver wants to save to disk when val loss improves
- An early stopper wants to abort the loop when loss plateaus
- A diagnostics logger wants to write to a file

These are **heterogeneous participants** — objects that care about the same events but do completely different things in response. The loop doesn't know or care what they do. It just broadcasts: "training is starting," "epoch is done," "training ended." Each participant decides whether and how to respond.

## Red Flags

### You're writing `isinstance` inside a loop

```python
for logger in loggers:
    if isinstance(logger, WandbLogger):
        logger.watch(model)
```

The loop is now aware of specific types. That's the process knowing too much about its participants.

### Adding a participant requires editing the process

If you have to open the training loop, request handler, or test runner to add new behavior, the boundary is wrong. New participants should be addable without touching the process.

### You have feature flags controlling behavior inside a loop

```python
if config['use_wandb']:
    ...
if config['early_stopping']:
    ...
```

Each flag is a participant trying to get in through the back door.

### You need a comment to explain who a block is "for"

```python
# wandb-specific
if run is not None:
    run.log(...)
```

The comment is admitting that participant-specific logic is living inside a generic process.

## The Solution: Lifecycle Hooks

Define a base class with no-op hooks at each moment the process wants to broadcast:

```python
class Logger:
    def on_train_start(self, model) -> None: pass
    def on_epoch_end(self, epoch_info, eval_info) -> None: pass
    def on_train_end(self) -> None: pass
```

Each participant overrides only what it cares about:

```python
class WandbLogger(Logger):
    def on_train_start(self, model) -> None:
        self._run.watch(model)

    def on_epoch_end(self, epoch_info, eval_info) -> None:
        self._run.log({"train_loss": epoch_info.avg_train_loss, ...})

    def on_train_end(self) -> None:
        self._run.finish()


class CheckpointSaver(Logger):
    def on_epoch_end(self, epoch_info, eval_info) -> None:
        if eval_info.avg_val_loss < self._best_loss:
            self._best_loss = eval_info.avg_val_loss
            save_checkpoint(...)
```

The process is now closed to modification:

```python
for logger in loggers:
    logger.on_train_start(checkpoint.model)

for epoch in range(num_epochs):
    epoch_info = run_epoch(...)
    eval_info = eval_model(...)
    for logger in loggers:
        logger.on_epoch_end(epoch_info, eval_info)

for logger in loggers:
    logger.on_train_end()
```

Adding tensorboard, a Slack notifier, or an early stopper means writing a new class — zero changes to the loop.

## Hook Signature Design

Each hook's signature is a contract: it declares exactly what that moment in the process has to offer.

- `on_train_start(model)` — the model exists and is ready; nothing else has happened yet
- `on_epoch_end(epoch_info, eval_info)` — one epoch of results are available
- `on_train_end()` — training is complete; no new information

Don't be tempted to pass a fat object like `artifacts` or `**kwargs` to avoid thinking about the signature. A vague signature is a dishonest contract — the caller can't know what's actually needed, and participants can silently receive things they didn't ask for.

If different participants need different things at the same moment, that's a sign the hook is at the right granularity. Each participant declares what it uses via its override signature.

## What This Is

This pattern is the **Observer** pattern (also called Publish/Subscribe at larger scale), and the specific form — a base class with no-op hook methods — is the **Template Method** pattern applied to extension points rather than algorithms.

You'll recognize it in:
- PyTorch Lightning: `on_train_epoch_end`, `on_validation_end`
- pytest: `setup`, `teardown`, `pytest_runtest_call`
- React (class components): `componentDidMount`, `componentDidUpdate`
- Django signals: `post_save`, `pre_delete`

The underlying insight is always the same: **stable process, variable participants**. The process defines the moments; the participants decide what to do at each one.