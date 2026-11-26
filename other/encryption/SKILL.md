---
name: encryption
description: Read before an app keeps something that whoever stores the network's data mustn't read, and when a call says something is encrypted and no server may open it, or that a device doesn't hold someone's key.
metadata:
  title: "Encryption"
  subtitle: "Data only you can read"
  about: "Encrypts what your apps keep, so whoever stores your network's data can't read it. Your Vault is kept this way."
  category: Admin
---

Encryption keeps an artifact's blobs encrypted in the bucket, so whoever runs the bucket can't read them, and nor
can a server that doesn't act for its owner. The Vault keeps its items this way.

Its words:

- **Encrypted artifact**: an artifact whose blobs are encrypted before they're stored, so only holders of its key read
  it. For passwords and the keys that reach devices. Avoid: sealed.

- Someone's key is made the first time their passkey unlocks it, on the network's sign-in page, and kept only
  encrypted: to that passkey, to each device it lets in, and in their recovery key. No server ever holds it. A
  passkey can only do this with WebAuthn's PRF, whose output, which only the device it's used on ever has, derives a
  key the person's key is encrypted to; one without PRF says so in Sign In & Security, and Unlock with Passkey
  offers to make one that has it. Another passkey of theirs unlocks it once a device that holds the key encrypts it
  to that passkey, when its person allows it there (`sign-in`'s `encrypt_for_passkeys`).
- Keys reach servers and devices only by a person's passkey, on the sign-in page: Unlock with Passkey
  (`sign-in`'s `unlock_with_passkey`). There the passkey opens its person's key, and with it a group's or the
  network's key that's encrypted to theirs (`wrapped`, one for each of its owners); lets in the device that asked
  (`ask`); and hands the keys of what's encrypted for them to every server that acts for them and is waiting, and
  takes them from one that no longer does, as a new epoch, signed by its owner. The page keeps what it encrypted with
  `store`, which nothing but a holder of the key can fill in. No tool, agent or server hands a key over.
- Every server that acts for whose it is should hold their key for it, since any of them may run its calls, and no
  other should. `key`'s `access` says, for each artifact encrypted for someone, its `epoch`, which servers hold it,
  which are waiting for it (`missing`) and which hold it and no longer act for them (`extra`), and Telemetry has an
  alert open while that's so (`check`, every 10 minutes). Sign In & Security shows a row for each key servers are
  waiting for, with Use Passkey, and the network's owners are notified once when a server starts waiting
  (`sign-in`'s `check`, which `check` calls). A call that no server can open says which are waiting.
- Choosing a server is adding it (`add_server`, `add_member`): one that acts for someone holds their keys once
  their passkey hands them over. Taking it off removes its relation tuple at the next handover, and what's written
  after is under a key it was never handed. What it read before, it read.
- What that trusts: whoever can use your passkey can open your key, the same as whoever can sign in as you. The PRF
  output and the key it opens stay on the device, in the sign-in page; what's kept, with the passkey, is the key it
  derives and your key encrypted to it, which no server opens. The PRF is asked with a salt of the network's own,
  so a passkey gives each network a different key. The page comes from the network's edge, so whoever can change
  the edge's code could take what a passkey opens there, as they could change the page you sign in on. And a device
  that holds a key unencrypted, as `one` on a computer does, can always hand it on, whatever servers check: making
  servers verify a passkey's assertion before they take a key wouldn't stop that, so they don't. Trust the devices
  you let hold your key as you trust yourself; `tooling/keys.ts` does from one what a passkey does, for a network
  being built.
- When every passkey and device that held the key is gone, its person lets a new device in with their recovery
  key, which a device that holds the key shows them. Without it, or a passkey that unlocks it, nobody is let in
  again. A recovery key is a secret: never ask for one in a chat, and never repeat one.
- An assistant has no passkey, so it hands no key over: its person does, in Sign In & Security or the Vault.

An app keeps something encrypted by requiring this app:

    def requires, do: %{"encryption" => "to keep your notes unreadable"}

    def call("keep", %{"text" => text}, call) do
      encryption = OneCore.Call.app(call, "encryption")
      notes = encryption.encrypted(call, OneCore.Call.make(call, "notes"))
      OneCore.Artifact.write(notes, "note", encryption.secret(call, text))
      "Kept."
    end

- `encrypted(call, artifact)` gives the artifact, encrypted: `OneCore.Artifact` reads and writes it as any
  other, and what reaches the bucket is encrypted. On a server that wasn't chosen, the call ends there and a
  server that was runs it instead, so nothing after `encrypted` runs where the artifact can't be opened. A
  blob's name and size aren't hidden, so name blobs by what says nothing. The names under `keys/` are this
  app's.
- A database is encrypted by giving it the artifact: `database.transaction(%{call | own: notes, folder:
  Path.join(OneCore.Server.home(), OneCore.Artifact.name(notes))}, schema, fun)`. A server that wasn't chosen
  never opens it, so it takes no lease. The server writing it keeps a working copy on its own disk, as it does
  of any database. An app's scheduled jobs are kept in its own artifact's database, which then isn't the one
  to encrypt: keep what's encrypted in an artifact the app makes.
- What a person types that's secret is encrypted on their device, by an input that says so: `%{type: "string",
  format: "secret", unlocked_on: "unlocked_on"}`, where `unlocked_on` names a read-only tool of the app that
  answers `encryption.unlocked_on(call, artifact)`, all of it: the list of servers its owner chose comes with
  their signature, which a device checks before it encrypts to them. The app, `one` and an agent's MCP on a device
  all encrypt it before it's sent, and `encryption.secret(call, input)` opens it on a chosen server. So no hook, log or other
  server reads it. What arrives as it was typed is refused.
- `servers(artifact)` lists the servers that hold its keys.
- Never answer with what's encrypted, raise it or log it: a tool's answer goes to agents and into what clients
  keep.
