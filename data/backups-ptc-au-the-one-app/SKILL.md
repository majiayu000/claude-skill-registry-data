---
name: backups
description: Read when someone asks about backups, wants their network backed up to a disk or to S3-compatible storage, wants something they lost brought back, or has lost the network's bucket.
metadata:
  title: "Backups"
  subtitle: "Copies of everything, kept safe"
  about: "Backs up your whole network, everyone's, to a disk on one of your machines or to cloud storage. Bring back anything you lost, or everything at once."
  category: Admin
---

Backups are copies of the whole network, every person's and group's data, to a folder on one of the network's
machines (as on a disk plugged into it) or to S3-compatible storage. They're the network's: an owner of it uses these
tools for the network (`ONE_SUBJECT=network`, and `subject: "network"` from an app).

- A backup holds the network's blobs as they are, so it's trusted as the network's own storage is: what's encrypted
  there, like a Vault item, is encrypted in the backup too, and the rest isn't. Whoever can reach a destination
  restores from it; no key is needed.
- `destinations` lists where backups go, each with when it last finished, how long it took, how big it is, its backups,
  and what's wrong if anything is. It says how often backups are made and which
  are kept.
- `add` adds a destination. A folder is a whole path on a machine that runs the service `Backups.Disk` (`services`, then
  `install_service` on the machine the disk is on). S3-compatible storage is its `endpoint`, its `bucket` (and a
  folder in it after a `/`) and an `item` in the network's Vault, with fields `access_key_id` and
  `secret_access_key`, switched on for `backups`: ask for it with `vault_request`, `app: "backups"`, for the
  network. A destination is tried before it's added.
- `now` backs up at once and answers with what was sent. `schedule` sets how often it happens by itself: every
  `hour`, `day` (the usual) or `week`, or `never`. Every backup is kept for a day, then one a day for a week, one
  a week for a month and one a month for a year.
- `check` reads a destination's newest backup back whole and compares every object with what was sent. A problem it
  finds, or a backup that failed, shows on the destination in `destinations`.
- `restore` brings back what a backup holds that's gone from the network, by how its names start: `users/alice/`
  for a person, `users/alice/own/notes/` for what one app keeps for them (and `users/alice/made/notes/` for
  what it made them), or one blob's whole name. It changes nothing that's there, so it can't put a database back
  to an earlier moment over what's there now. Settings › Backups does the same, for a person, an app or a file.
- `remove` stops backing up to a destination. What's there stays.
- A destination whose last backup failed, or with none finished within its schedule and a day, needs its owners: it's
  the red count on Backups in Settings (`badge`), Telemetry's `backup` alert, and the network's owner is notified once, until
  it's backed up again.

When the bucket itself is gone, the network is restored into an empty one on any machine, with no network running:

    one restore --from <destination> --to <empty bucket>

A destination or a bucket is a folder, or `https://<endpoint>/<bucket>[/<folder>]` with `--from-keys` or `--to-keys`
naming a file of `ACCESS_KEY_ID=` and `SECRET_ACCESS_KEY=` lines. `--list` lists a destination's backups, and `--backup`
picks one. Then a server is started on the bucket: the first one is the network's, and its other servers are added
again.
