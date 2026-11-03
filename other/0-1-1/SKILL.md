---
name: aireg-publish
description: Publish a skill or agent to a registry, or release a new version of one, including an edit made to an installed copy. Use when asked to publish, share, contribute or release a skill or agent, send an edit to an installed skill back to its registry, update one that is already in a registry, publish a project's skills from CI, or fix what registry validation reports.
compatibility: Needs the aireg CLI and git, on macOS or Linux.
license: Apache-2.0
---

# Publish to a registry

A released version is never edited: every change is a new version. Pass `--json` to the CLI
and read `data`.

Pick the path by where the user is working:

- **An installed skill or agent the user edited**: send it home.
- **Outside the registry's repository**, with a skill in some folder: contribute it.
- **A project whose skills should reach a registry on every change**: publish from CI.
- **Inside the registry's repository**: add or version it there, then release.

## An installed skill you edited

`aireg status --json` shows it `edited`. Publish it by name, and don't read `.registry/` to
work out where it came from:

```sh
aireg publish <name> --dry-run --yes --json   # data.artifacts: the version it would release
aireg publish <name> --yes --json
```

- A registry in a folder takes the next version in place.
- A git registry exits 2 with `is a git registry`: publish into a clone instead, as below,
  with `aireg publish <name> --to ../<clone>/<namespace> --yes --json`.
- If a newer version was published since the edit, it refuses. Offer `aireg update` and
  redoing the edit there, or `--force` to publish over it.

## Contribute from any folder

`aireg status --json` lists, in `data.unmanaged`, the skills in this project's harness
folders that aireg does not manage; `aireg status -g --json` lists the user's own. Read one
before publishing it:

```sh
aireg show ./<path> --json
```

A skill is a folder holding `SKILL.md`; an agent is one `.md` file. aireg doesn't publish to
a git registry: it writes the new version into a clone, and git carries it from there. For a
registry in a git repository, the usual case:

```sh
git clone <repository> ../<clone>      # a clone already there: switch to its default branch and pull
ls ../<clone>/artifacts                # the namespaces in use; a new registry has none yet
git -C ../<clone> switch -c publish-<name>
aireg publish ./<path> --to ../<clone>/<namespace> --yes --json
git -C ../<clone> add . && git -C ../<clone> commit -m "publish <name> <version>"
```

- `--to` is read as a folder only when it starts with `.`, `/` or `~`, so keep the `../` or
  use an absolute path. A namespace the registry doesn't have is created without a warning,
  so take one from the list, or agree a new one with the user.
- A clone that is behind gives a version that is already taken, so always pull first.
- A first publish is 0.1.0. A changed artifact gets the next patch version; pass
  `--bump minor` or `--bump major` when the change alters what it does.
- aireg writes the version and the index. `data.artifacts` gives each `version` for the
  commit message. Commit only when an entry has `published: true`; `false` means it matches
  the newest version, and there is nothing to release.
- Ask before `git -C ../<clone> push -u origin publish-<name>` and `gh pr create`. The
  registry's own check gates the pull request, and merging it is the release.

A registry that is a plain folder, declared in this scope, is updated in place:
`aireg publish ./<path> --to <registry>/<namespace> --yes --json`. To leave `--to` out of
later publishes to it, set your own default with
`aireg config set defaults.namespace <registry>/<namespace>`. Publishing to a declared git
registry, by `--to` or by that default, exits 2 with `is a git registry`; take the clone
path then.

## Publish a project's skills from CI

For skills that live in a team's project repository: on every merge, each changed skill goes
to the registry as a new version, in a pull request the registry's own check gates. Unchanged
skills publish nothing. The workflow checks out the registry beside the project, publishes
into that checkout, and opens the pull request; aireg never pushes. Add
`.github/workflows/publish-skills.yml`, filled in here for the registry `acme/ai-registry`
and its `engineering` namespace:

```yaml
name: publish-skills
on:
  push:
    branches: [main]
    paths: [".claude/skills/**"]
permissions:
  contents: read
jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7.0.1
        with:
          persist-credentials: false
      - run: curl -fsSL https://aireg.sh/install | AIREG_VERSION=0.1.1 sh
      - uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7.0.1
        with:
          repository: acme/ai-registry
          path: registry
          token: ${{ secrets.REGISTRY_PUSH_TOKEN }}
          persist-credentials: false
      - run: aireg publish '.claude/skills/*' --to ./registry/engineering --yes
      - uses: peter-evans/create-pull-request@5f6978faf089d4d20b00c7766989d076bb2fc7f1 # v8.1.1
        with:
          path: registry
          token: ${{ secrets.REGISTRY_PUSH_TOKEN }}
          title: Publish skills from ${{ github.repository }}
```

`REGISTRY_PUSH_TOKEN` holds a fine-grained token, or a GitHub App token from
`actions/create-github-app-token`, with Contents and Pull requests read and write on the
registry repository only; `GITHUB_TOKEN` cannot reach another repository. Tell the user how
to create the token and add the secret; never ask for its value.

## Inside the registry

| Task | Command |
| --- | --- |
| Add a new skill | `cd artifacts/<namespace> && aireg skill new <name>` |
| Add a new agent | `cd artifacts/<namespace> && aireg agent new <name>` |
| Bring an existing skill in | `aireg skill new --from <path> --namespace <namespace>` |
| Bring an existing agent in | `aireg publish <file>.md --to ./<namespace> --yes --json`, from the registry's root |
| Change one | `aireg skill bump <name> [patch\|minor\|major]`, then edit the new folder |
| Release | `aireg registry index`, then commit everything it wrote with the change. Ask before `git push`, even when the user asked to release it |

`new` writes `TODO` for every field it cannot know. Replace each: the description says what
the artifact does and when an agent should use it. Choose `minor` or `major` when the change
alters what the skill does; `patch` otherwise.

Never edit `index.json` or an `artifact.json` by hand: `index` writes them. The one hand edit
`versions.json` takes is a status change: to deprecate, archive or yank a version, set its row's
`status` to `deprecated` or `archived`, or `yanked` to `true`, add a `reason`, then run
`aireg registry index`. Never remove a row or change its digest.

## When validation fails

`aireg registry validate` names each problem with its fix. The usual ones:

| It says | Do |
| --- | --- |
| changed after (or since) `<version>` was released | Undo the edit there, run the printed `aireg <kind> bump <name>`, edit the new folder |
| `<field>` is still TODO, or is required | Fill the field in the front matter |
| is not a name | Rename the folder: lowercase letters, digits and hyphens |
| index.json is out of date | `aireg registry index`, then commit |

Never publish credentials, tokens, or anything that names a customer.
