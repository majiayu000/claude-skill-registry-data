---
name: git-workflow-secrets
kind: pattern
rule: deploy-flow
description: Pattern of rule deploy-flow. Load when working with keys of external services — where they live, how the owner's key differs from the environment key, what each state of an integration row means and why a green probe does not promise a working feature.
---
<!-- rt-kit v0.34.0 · patterns/git-workflow-secrets.md · 6c412d3da7e7 · правится надстройкой, не здесь -->

# Keys of external services

Pattern of the rule `deploy-flow`. What must be true meanwhile — the law
`docs/constitution/delivery.md`.

## When to use

- A feature that goes outside is silent: mails do not leave, translations do not update.
- A key of an external service is being created or changed.
- It is being analysed what exactly is rolled out and what the application lacks to work —
  including a key that lives in the environment and has no screen.

## A rollout secret is not a key of an external service

The keys of this pattern live in the storage or in the production stack, and the application
reads them. Rollout secrets — the node access key, the registry password, the intake address and
token — are not read by the application at all: the pipeline reads them, they lie in the
repository settings, and the storage knows nothing of them.

Hence a different course on a miss. A missing service key is silent on the screen: the feature
does not work, and the application answers. A missing rollout secret brings down a pipeline step,
and the application is never reached at all — it is analysed in the step's log, not in the
browser.

How a rollout secret is created and what checks its rights is said by the pattern of working with
images — `git-workflow-docker`, if the tree has laid it out. Here the border remains: whoever came
for a rollout secret reads on not in this text.

## A key created by the owner lives in the storage, not in the environment

Such a key lies as a row in the storage, encrypted with the secrets encryption key; next to it an
open hint of the last characters and the outcome of the last probe. One service reads it and
gives it to those who go outside.

**There is no fallback path to the environment.** A variable of the same name in the production
stack means nothing: the application does not read it. One key is taken from the environment —
the one that encrypts all the others. Losing it makes the recorded keys unreadable, and creating
them anew is useless until it is back.

Such keys the owner creates themselves, on the integrations screen. **The agent does not enter
keys:** entering an access key into a field is forbidden to it whoever asks.

## Not every key of an external service is created by the owner

The storage holds keys the owner creates themselves and differently for each property. A key that
is the same for the whole application stays in the environment, and it has no integrations
screen.

The halves of such a pair — the backend key and the key baked into the build — lie on different
sides of delivery, and exactly one can be filled. Then the feature is neither off nor on: the
widget is not drawn, the server waits for a token. The application calls such a state broken and
says so by a log line and the startup digest — what stands in it is described by the rule
`observability`.

Hence the order of analysis for a key from the environment: it is read not on the integrations
screen but in the startup digest in the container logs — in which of its lists the feature name
stands.

## An integration row speaks in five states

The order of analysis matters — the storage state overrides everything else:

| What is shown                         | What it means                                                              |
| ------------------------------------- | -------------------------------------------------------------------------- |
| state unknown                         | the answer has not come yet; nothing to claim                              |
| storage unavailable                   | there is no encryption key; keys cannot be created, and the owner is not at fault |
| not set                               | there is no secret row at all — the key was never created                  |
| nothing to decrypt with               | the row exists, and the encryption key has changed; creating anew is useless |
| unchecked · working · not working     | the key is recorded; from here the probe judges                            |

Hence the short path of analysis: a mail or a translation is silent — first open this screen, not
the logs. "Not set" answers the question whole, and ten days of silent mail turned out to be
exactly that, not the server.

## A green probe promises less than it seems

The probe asks the service for what it gives out by the key: the list of domains, the list of
models. It sends no mail and makes no paid request — but it does not prove the feature works
either:

- the list of models is given out with an empty balance too, while the request itself is refused
  for lack of funds. The row is green meanwhile;
- the mail probe checks the sender address against the list of confirmed ones — but only if the
  address is already filled. With an empty address it answers "working", and mails will not leave.

So after entering a key the feature itself is checked, not the row: save a record and make sure
the warning did not come; wait for the first enquiry and see the mail.

## Moving a key from the environment into the storage is not done by a migration

The secret is encrypted by the application, so a query to the storage cannot move it: the
migration creates the table and does not touch values. A key moved from the environment into the
settings must be created by the owner on the same day the edit is rolled out — otherwise the
feature goes silent silently. Checked on the same integrations screen right after the rollout.

## Common misses

- **Looking for the key by a search over the production stack and drawing a conclusion.** The
  value lies there, the application does not read it, and the tail of the last characters matches
  the one recorded in the storage — a match of the hint and the variable proves nothing except
  that the owner created the same key.
- **Going to the logs before the screen.** The logs will tell about the external service's
  refusal, and the screen — "not set"; the second is more precise and costs one click.
- **Taking the absence of errors as a sign of work.** Neither mail nor translation brings the
  request down: the enquiry is saved, the record is saved, and nothing leaves outside.
- **Creating the key anew on "nothing to decrypt with".** This is not about the key but about
  the encryption key; a new one will lie next to it and will not be read either.
