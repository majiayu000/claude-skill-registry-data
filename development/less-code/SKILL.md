---
name: less-code
description: "Use when refactoring, sizing a diff, sequencing an addition or rewrite, or about to add a guard, an abstraction, a layer, or a new value passed through the stack. Remove first, then make the smallest change that solves the problem."
disable-model-invocation: true
kind: principle
---

# Less code

Writing code is free for you. That's the problem: it makes adding more than the job needs easy. So act like the person who has to maintain it and gets tired reading it. Get the most done with the least code.

## Don't add code for things that don't happen

Every guard and every extra layer is code we read, test, and keep forever. If it protects against something that never happens, we're paying for nothing.

- **Name the failure before you write the guard.** Null check, try/catch, retry, fallback. Which caller passes null? Which call actually throws? What state makes the fallback run? If you can't answer, don't write it.
- **No abstraction until the second real case.** No interface with one implementation. No config option nobody asked for. No generic version of a specific problem. No layer that just calls the next layer. Write the concrete version. When a real second case shows up, pull the abstraction out then. It's cheap at that point because the tests already exist.
- **Watch for "might".** "This might be null." "We might need another provider." If the reason for the code is "might", stop. Either it does happen and you can show it, or the code goes.

## Remove first, then build

Deleting before you add gives you a simpler base, so the next change ends up smaller and less likely to break something.

- **Look for things to delete first.** When asked to refactor, improve, or extend something, check what can come out before adding anything.
- **Cut before you polish.** Get down to the minimum, then spend effort on quality. Polishing code that's about to be deleted is wasted.
- **Build for how it's actually used.** Not for edge cases nobody has hit. Read the usage before designing for it.
- **Features drag guards behind them.** Persistence, retry on startup, schema migration. Each one needs validators to defend its inputs. A feature outside the spec costs more than the feature itself.
- **Same rule for prose.** Trim repeated instructions in prompts and skills. If a reference file says nothing new, delete it instead of leaving a stub.

## Keep the change small

- **Smallest diff that solves the problem.** Fewer lines beat nicer-looking boilerplate.
- **Keep calls flat.** If answering a question takes more than three files or layers, flatten it. A function that hides real work behind a clean signature is fine. A chain of functions that just call the next one is not.
- **Make each decision once.** Don't repeat the same check in several places. Decide it in one spot and pass the result along.
- **Don't thread new values through everything.** If the task wants a new field pushed through types, schemas, pipelines, and handlers, stop and look for a shorter path. If it's exhausting to thread, it's probably the wrong approach.
- **Clean up the small stuff.** Tiny pass-throughs and repeated choices add up. Remove them before they spread.
- **Leave it a little cleaner than you found it.** Rename one variable, split one function, delete one dead branch while you're in there. Hand back something simpler that does the same or more.

## The test

If a person would find this code tiring to maintain, it's the wrong solution. Be lazy. Keep it simple.
