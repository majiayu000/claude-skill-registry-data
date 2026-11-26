---
name: permissions
description: Read before sharing something, making a group or a sharing link, or when a call is refused for who may reach what, and before an app reaches what it didn't make.
metadata:
  title: "Permissions"
  subtitle: "Who can see and change what"
  about: "Share what you make with people, groups or a link, and choose who can see or change it. Make groups for your family or team."
  category: Admin
---

Permissions says who may do what, as relation tuples: an artifact, a relation, and who. An app reaches an
artifact only if a tuple says so, both for whoever it runs for and for the app. Without it, or another
app deciding, nobody but the network's first owner does anything.

Its words:

- **Relation tuple**: one line of who may do what, as in Zanzibar: an artifact, a relation (`owner`, `editor`, `viewer`,
  `installer`, `parent`, `member`) and a subject, as in SpiceDB and OpenFGA. An owner is an editor, and an editor is a viewer. A
  user, a group, everyone, a server, an app and the holder of a sharing link are all a subject. Whoever asks for a
  call is its actor. Avoid: fact, grant.

- An artifact is named by where its blobs are, and its name starts with whose it is:
  `users/alice/made/notes/7` is alice's, `groups/family/made/notes/2` is the group's. An app's tool that
  makes something answers with its name. A group is the artifact `groups/<name>`, and the network `network`.
  An app is whoever's deployed it, `users/alice/apps/<name>`, and its own artifact is whoever's it runs for,
  `users/alice/own/<name>`, even where it's installed for the network, unless it says its data is the network's:
  the network's are `network/apps/<name>` and `network/own/<name>`.
- Who is a user (`users/alice`), a group, meaning its members (`groups/family`), `everyone` in the network, a
  app by its artifact's name, or a sharing link's holder (`users/alice/links/...`).
- `owner`, `editor` and `viewer` are what someone may do: an owner is an editor, and an editor is a viewer.
  Whoever a user's artifact's name starts with owns it. What was made for a group (`groups/family/made/...`) or
  the network (`network/made/...`) its members see and its owners own, as a GitHub organization's members read its
  repositories: an owner lets others change it with `editor`, of all of it (`--artifact groups/family/made`) or of
  one app's (`--artifact network/made/vault`), and `--who groups/family` (or `everyone`) lets every member. A
  member asking for a group or the network calls an app's tool that only reads if they see what that app made for
  it, and any other if they may change it. A group's or the network's apps, and what those keep, are their owners',
  and the network's owner owns everything. Whoever has a relation to an artifact has it to everything in it by its
  name, and to a user or a group to everything that's theirs: a group's owner owns its apps and what they keep. `member` puts a user or
  a group in a group. `parent` names another artifact as who, and gives whoever has a relation to that one the
  same relation to this.
- `installer` of the network (or of a group) may install apps for it, as its owner does, and nothing more an owner
  may: `share --artifact network --relation installer --who users/carol`, which only an owner writes or removes.
  `users --artifact network --relation installer` lists who may, owners among them; anyone in the network sees it.
- `share` writes a tuple and `unshare` removes one, or finds it already gone. An owner or an editor shares with viewers and editors, and
  only an owner adds an owner, a group's member or a parent. `unshare` refuses to remove the last owner of the network or of a group. Whoever asks shares only what they may themselves,
  whoever the call runs for. `shared` lists an artifact's tuples,
  and `check` says whether someone may reach it.
- `transfer` moves something an app made (`users/alice/made/git-repos/notes`) to another owner, `--to users/bob`,
  `groups/family` or `network`, as GitHub's transfer of a repo does: it's then
  `users/bob/made/git-repos/notes`, with its history, its other shares and its links, and whoever it was whose has
  nothing of it unless it's shared back. Its owner, or the network's owner, moves it, and a transfer to someone it
  isn't the mover's to give to (a network's owner owns everything, so anyone) waits in `transfers` until they, or
  whoever owns the group or network it's to, `accept` it (or `decline`: whoever asked takes it back too). They're
  notified, never emailed. Its old name says where it went (`moved`). It's refused where the app that made it doesn't
  hook `permissions.transferred`, which it's told of the move by to keep what it lists true, and for what's encrypted:
  the key stays its first owner's, since a key reaches another only by their passkey.
- `forget` removes every tuple that names someone taken out of the network, so whoever joins by their name next
  inherits nothing. Taking someone out (`sign-in_remove_person`) calls it, and it refuses anyone still in.
- `groups` lists the groups whoever asks is in, each with what it's called, its members and owners.
- `group` makes a group called what it's given (The Smiths is `groups/the-smiths`), with whoever asks as its
  owner and first member. A member has a call run for the group, with the group's artifacts:
  `ONE_SUBJECT=groups/family` before a command, and an app opened from the group's Home Screen page. Every user is a member
  of the network.
- `link` makes a sharing link to an artifact, as a viewer or an editor. Whoever holds the link reaches the
  artifact without signing in, through the tools that take a link's holder, until its tuple is removed with
  `unshare`. The link is answered once and kept nowhere, so pass it on then. It starts with whose the artifact
  is, and at the network's address it's `<the address>/link/<the link>`.
- An app reaches something made by another app only once it has a relation to it too:
  `share --artifact users/alice/made/notes/7 --relation viewer --who users/alice/apps/reader`.
- Sharing, and taking it away, are a person's decisions. Do them when asked to, and say what you did.

In an app, nothing of this is called: `OneCore.Call.reach(call, name, "editor")` gives the artifact or
raises with the reason, and `OneCore.Call.reaches?/3` asks. An app whose own tools are for some users only
asks for a relation to its own artifact, such as who may approve:
`OneCore.Call.reaches?(call, OneCore.Artifact.name(call.own), "editor")`.
