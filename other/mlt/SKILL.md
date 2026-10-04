---
name: mlt
description: Use the installed MLT framework and melt command for multitrack service graphs, producers, playlists, filters, transitions, links, consumers, XML serialization, playback, rendering, and editor-compatible timeline work with runtime service discovery.
disable-model-invocation: true
author: Alan Guice (Badgids)
license: Apache-2.0
---

# MLT

## Workflow

1. Read `../../references/MLT_TOOLKIT.md`.
2. If `melt` is available, query the installed producers, consumers, filters, transitions, links, profiles, or the exact service needed.
3. Model the composition as producers/chains, playlists, tracks/tractors, filters, transitions, and consumers rather than as opaque editor UI commands.
4. Use MLT XML for durable service-graph serialization.
5. Keep reusable project resources project-relative.
6. Parse generated XML and, when `melt` is installed and useful, load or render it for an integration check.
7. Route actual Kdenlive or Shotcut project requests to `editor-project-export` rather than assuming generic MLT XML is editor-native.

## Done

The MLT graph or operation is structurally valid, uses only known/verified services when runtime compatibility matters, and requested outputs were actually produced when execution was requested.
