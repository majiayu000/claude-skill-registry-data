---
name: blast-radius
description: "Find what a Roblox change can break across client/server contracts, remotes, saved data, replication, authored Instances, mobile performance, and dependent systems."
---

# Roblox blast-radius review

Inspect the diff, then follow consumers beyond it.

- Trace callers, callees, required modules, remotes, attributes, tags, CollectionService consumers, project mappings, and authored Instance paths.
- Check whether a client/server payload, replicated shape, saved schema, migration, reward identity, cooldown, or lifecycle assumption changed.
- Check reconnects, duplicate requests, player removal, character replacement, round reset, server shutdown, and retry behavior.
- Check mobile CPU, memory, physics, render, network, and instance-count costs.
- Check security boundaries. A client-visible or client-supplied value must not become authority by accident.
- Run the smallest check that proves each material risk. Use source and local automation. Studio playtesting belongs to the user.

Report only concrete risks. Each finding names the failure, evidence path, likelihood, impact, and verification. End with the strongest fact supporting safety and any remaining Studio test.
