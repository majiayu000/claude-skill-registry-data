---
name: git-repos
description: Read before making, cloning, pushing to or reading a git repo in the network, or opening a pull request on a repo you can't push to.
metadata:
  title: "Git Repos"
  subtitle: "Code, kept in your network"
  about: "Git hosting of your own: repos for you, your groups or everyone, with branches, history and pull requests, on every device you use."
  category: Developer tools
---

Git Repos is git hosting in the network. A repo is a person's, a group's or the network's, and is named as any artifact
is: `users/alice/made/git-repos/notes`. Its address for git is `one::` and its name, the same on every device that has
`one`:

    git clone one::users/alice/made/git-repos/notes

Each repo is also named as it's shown, `owner/name`: a person's username, a group's, or the network's own command
(`ptc/the-ptc-app`), as GitHub shows an organisation. Any tool takes either as `repo`, and so does `git clone one::alice/notes`.

Git signs in as the device does, with no password. `one` puts `git-remote-one` beside itself on the PATH the first
time it runs, which is what git runs for `one::` addresses; where it couldn't, link it there: `ln -s one
git-remote-one`, or on Windows `mklink /H git-remote-one.exe one.exe`.

- `create --name notes` makes an empty repo, yours, or a group's with `ONE_SUBJECT=groups/<name>`. Then push to it from a
  repo you have: `git remote add origin one::users/alice/made/git-repos/notes` and `git push -u origin main`.
- `list` lists every repo you may read, with who can see it (`private`, `everyone` or a `group`), its description (its
  README's first line). `branches`, `tree`, `file`, `log` and `commit` read one without cloning it:
  a folder or a file at a ref, the history, one commit's diff.
- Who reads and who pushes is sharing, as for anything: `permissions share --artifact <repo> --relation viewer` (reads
  and clones, and opens pull requests) or `editor` (pushes, and merges pull requests). A group's members push to its
  repos. Share only when asked.
- A push moves a branch only from where you fetched it. If someone pushed first, git says `fetch first`: fetch,
  rebase or merge, and push again. Nothing pushed is lost.

To change a repo you may read but not push to, open a pull request: commit it on a branch of yours, push it to
`refs/pull/<name>`, a short name of your own for it, and tell its owner. The commit's subject is its title.

    git push origin HEAD:refs/pull/fix-typo

Pushing there again updates it. `pull_requests` lists a repo's pull_requests with their commits. Whoever pushes to the
repo `merge`s one, which fast-forwards the branch it's for or merges it, or `close`s it; whoever opened it can
close it too. A pull request that doesn't merge cleanly says which files conflict: fetch the branch it's for, merge it
into yours, and push the pull_request again. `git fetch origin refs/pull/fix-typo` fetches one to look at.

A repo's owner, or the network's owner, moves it to another owner with `permissions transfer` (Transfer… in a repo's
menu): `--artifact users/alice/made/git-repos/notes --to users/bob`. It keeps its history, its shares and its links, and
its old address says where it went. Moved to someone by anyone but the network's owner, it waits for them to accept it.

`remove` puts a repo you own in Recently Deleted, gone for everyone until `restore` brings it back as it was, beside
a repo made at its name since as `notes-2`, which it answers with. After 30 days it's purged for good. The tool `git` is what `git-remote-one` calls; don't call it yourself.
