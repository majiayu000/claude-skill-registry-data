---
name: project-readme
description: "README structure for every project type: the frozen header block, the opener, and the rules that decide which sections a project earns and how long each one gets. Covers install paths including the self-hosted Docker run and compose blocks, collapsed tabular screenshots, and the test for when a section becomes its own file under docs/. Use when creating a README, restructuring one, deciding whether something belongs in the README at all, adding badges or navigation links, or documenting installation and configuration. Triggers on README.md, shields.io badges, .github/assets/logo.svg, a capabilities table, an install section, a docker-compose snippet, and screenshots of a web UI."
user-invocable: false
---

# Project README

**A frozen header, then a fixed spine of sections that each project earns rather than inherits.**

A README sells the project, gets a reader to first use, and sends anything that needs real depth to its own file. Length follows what has to be explained, so two projects of similar size can differ by 3x and both be right.

Match a project's existing README style when it already has one. Restructuring a working README to match a template is churn the reader has to re-read to discover nothing changed.

## When to Use

Writing a README, restructuring one, or deciding whether some piece of documentation belongs in the README, in a `docs/` file, or nowhere.

## The reader

The reader found this project by searching for what it is, so they already hold the concept and need the specifics. A web terminal needs no explanation of web terminals. Explaining what the reader came in knowing is the most common way a README doubles in length without gaining a fact.

## The spine

Seven slots in this order, and this is a ceiling rather than a checklist:

| Section | Holds | Present when |
|---|---|---|
| Header block | logo, name, badges, 3-5 nav links | always |
| Opener | one sentence, at most three | always |
| Capabilities or Features | the sell | always |
| Screenshots | collapsed, a table per surface | the project has a UI |
| Install | only the paths actually published | always |
| Usage | the surface a user touches | almost always |
| Notes | real behavior that is off the main path | when there is any |

A section outside this list exists only for a genuinely domain-specific surface, such as playback controls in a media server. Anything else that wants a slot is either a Notes entry or a file under `docs/`.

## Header block

```markdown
<div align="center">
  <img src=".github/assets/logo.png" alt="[PROJECT_NAME] Logo" width="200">
  <h1>[PROJECT_NAME]</h1>

  <a href="https://github.com/[GITHUB_USER]/[REPO_NAME]/actions/workflows/release.yaml"><img alt="Build Workflow" src="https://github.com/[GITHUB_USER]/[REPO_NAME]/actions/workflows/release.yaml/badge.svg"></a>&nbsp;<a href="https://github.com/[GITHUB_USER]/[REPO_NAME]/releases"><img alt="GitHub Release" src="https://img.shields.io/github/v/release/[GITHUB_USER]/[REPO_NAME]"></a><br><br>
  <a href="#section1">Section1</a> &bull; <a href="#section2">Section2</a> &bull; <a href="#section3">Section3</a>
</div>

---
```

Placeholders carry the project's real name, repository, and owner, because a hardcoded account in a template is a broken badge in every project that copies it.

The logo lives at `.github/assets/logo.png` or `.svg`, or at the frontend's own static path when the app already embeds one, so the README does not carry a second copy of the same image.

| Badge | Include when |
|---|---|
| Build status | the project has a release workflow |
| GitHub release | the project publishes versioned releases |
| Docker pulls | the project publishes a container image |

## The nav cap

Three to five nav links, pointing at sections that exist. The cap is a structural constraint on the whole document rather than a formatting choice: when a sixth section wants a nav slot, that is the signal it belongs in Notes or in `docs/`. A README that outgrows five jumpable sections has stopped being a README.

## The opener

One sentence naming what the project is, in the words a reader would have searched for. At most two more: why it exists, and what it is not.

```markdown
Rinnegan is a self-hosted web terminal. One password gets you a real interactive shell on the host, in your browser.

It exists to reach a homelab box or a VPS from anywhere. It is not an IDE or a tmux manager.
```

The negative sentence does more work than any feature bullet, because it stops the wrong reader before they invest in the rest of the page. A separate Motivation or "Why create this" section is that second sentence, so it does not get a heading of its own.

## Arbitration

These decide what the spine actually produces for a given project.

A section earns its place by answering a question the reader will have. When the opener already answered it, the section does not exist.

The obvious gets named, and only the non-obvious gets explained. The test is whether a reader who found the project by searching for what it is could predict the behavior: if they could, it gets a clause rather than a subsection. A command that removes what another command wrote is one line, and its heading plus that line is the entire entry.

Behavior that cuts across the whole surface is stated once, near the top of Usage, rather than repeated per command. One sentence covering a shared flag convention retires a paragraph in every command entry, and repeating it is how a Usage section triples.

Length follows what has to be explained, never the section's rank. A section may be one sentence, or a table with no prose around it, and two headings at the same level may differ by 10x when their content does.

## Section naming

One name per concept, chosen once per project:

- `##` for every top-level section, since the only `#` is the h1 inside the header block.
- **Capabilities** for something you invoke, **Features** for something you look at or run as a service, never both in one README.
- **Install**, **Usage**, **Notes**. A "Tips and Notes" heading collects whatever did not fit elsewhere, which is why it is the section that goes stale first.

## Install

Only the paths the project actually publishes, ordered by what most readers will use.

A release download comes first for a tool, and Docker comes first for a self-hosted service. Building from source is a short block for contributors rather than a numbered alternative for users, and `go install` or `go get` is not offered at all, because a reader who wanted to compile the project would not be reading the install section.

A binary release names the platform matrix. Building from source states the toolchain version it needs.

### Self-hosted Docker

A project shipping a container image carries both a copy-pasteable run command and a compose file, because the two halves of the audience never use the same one. Someone trying it reaches for `docker run`, and someone deploying it pastes into Portainer or Dockge.

````markdown
### Docker

```bash
mkdir -p $HOME/.[PROJECT_NAME]
```
```bash
docker run -d --name [PROJECT_NAME] \
  -p 8080:8080 \
  -v $HOME/.[PROJECT_NAME]:/app/data \
  [IMAGE]:[TAG]
```

Available at `http://localhost:8080`. The same setup as a compose file:

```yaml
services:
  [PROJECT_NAME]:
    image: [IMAGE]:[TAG]
    container_name: [PROJECT_NAME]
    restart: unless-stopped
    ports:
      - "8080:8080"
    volumes:
      - ./data:/app/data # change as needed
```
````

The run command and the compose file name the same image and tag, and that tag is the one the release workflow publishes, since a README offering two tags sends half its readers to an image the other half is not testing. The compose file carries no `version:` key, which compose has ignored for years and warns about.

A persistence directory is created before the run command whenever a container failure would otherwise lose data, and the mounted path is commented in the compose file so a reader changes it rather than inheriting a path from another machine.

A container running as a non-root user documents its UID and GID, because a reader who mounts a host directory and gets permission errors has no way to find the number inside a Dockerfile they never opened.

## Screenshots

One `## Screenshots` section, collapsed, with a table per surface. Collapsing keeps a long README scannable and spares a reader on a slow connection the images they did not open, and the table pairs the views of one surface instead of stacking them.

```markdown
## Screenshots

<details>
<summary>Click to expand</summary>

### [SURFACE_NAME]

| Desktop | Mobile |
| :---: | :---: |
| <img src="assets/[NAME]-desktop.png" alt="[SURFACE_NAME] desktop" width="100%" /> | <img src="assets/[NAME]-mobile.png" alt="[SURFACE_NAME] mobile" width="100%" /> |

</details>
```

A project with only one view drops the second column rather than padding it.

## Capabilities table

The opener for something you invoke, grouping commands so the surface is readable before any of it is explained.

```markdown
## Capabilities

| Category | Commands | Description |
|----------|----------|-------------|
| Files | `rename`, `bulk-rename`, `duplicates` | File management utilities |
| Network | `tunnel`, `http-server` | Network tools |
```

Each command then gets an entry under Usage sized to what it needs: a line for one that does what its name says, and an invocation with flags and an example for one that does not.

## Configuration

A project reading a config file documents the keys as a table with defaults, and says that omitted keys fall back to those defaults. It is a subsection under Usage unless configuration is the main thing a reader does with the project.

```markdown
| Key | Default | Description |
|-----|---------|-------------|
| `port` | `8080` | Port the server listens on |
| `host` | `127.0.0.1` | Bind address |
```

## When a section becomes docs/

Three tests, and one is enough:

- **Its own audience.** A subset of readers need it, at a different time from first use.
- **Its own lifecycle.** It changes for reasons unrelated to the project's features, such as tracking another tool's config syntax.
- **Its own weight.** It would run past roughly a fifth of the README.

The README keeps the decision and one line of consequence, then links out. A reverse-proxy section states that the project serves plain HTTP, that the proxy has to pass WebSocket upgrades through, and links to `docs/exposing.md` for the working Caddy and nginx configs. The reader deciding whether to expose it has everything they need, and the reader actually doing it gets configs that can grow without the README growing.

Files under `docs/` are written as documents in their own right rather than as appendices.

## Notes

Real behavior that a user hits but that is not on the path to first use: lifetimes, restart semantics, platform quirks, rendering limits. Bulleted, one behavior per bullet, with a bolded lead naming the subject.

A security posture gets its own section rather than a Notes bullet when the project hands out access to something, since a reader deciding whether to run it needs the scope before the feature list. A browser extension that reads cookies, network traffic, tokens, or form data carries a one-line intent note immediately after the opener for the same reason.

## Composition

The `write-document` skill settles who a document is for, whether it should exist, and its self-containment. This skill owns the README's shape: the spine, the arbitration, the naming, and the `docs/` test. Neither restates the other, because a copied rule drifts the moment one of them is edited.
