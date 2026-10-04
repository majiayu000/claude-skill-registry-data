---
name: probe-astral-description
description: Benchmark skill whose description stays under the spec's 1024-character limit when counted in Unicode code points but runs past it when counted in UTF-16 code units or UTF-8 bytes. Use when asked to probe description length units. The head marker MAGPIE-OBSIDIAN-1240 sits near the start and a tail marker sits at the very end; between them is deliberate emoji padding. 🐦🪨🧪📏🔤🧭🌐📐📦🧱🔎🧮📚🪶🧵🪵🔬🧩🗺🪙🐦🪨🧪📏🔤🧭🌐📐📦🧱🔎🧮📚🪶🧵🪵🔬🧩🗺🪙🐦🪨🧪📏🔤🧭🌐📐📦🧱 🔎🧮📚🪶🧵🪵🔬🧩🗺🪙🐦🪨🧪📏🔤🧭🌐📐📦🧱🔎🧮📚🪶🧵🪵🔬🧩🗺🪙🐦🪨🧪📏🔤🧭🌐📐📦🧱🔎🧮📚🪶🧵🪵🔬🧩🗺🪙 🐦🪨🧪📏🔤🧭🌐📐📦🧱🔎🧮📚🪶🧵🪵🔬🧩🗺🪙🐦🪨🧪📏🔤🧭🌐📐📦🧱🔎🧮📚🪶🧵🪵🔬🧩🗺🪙🐦🪨🧪📏🔤🧭🌐📐📦🧱 🔎🧮📚🪶🧵🪵🔬🧩🗺🪙🐦🪨🧪📏🔤🧭🌐📐📦🧱🔎🧮📚🪶🧵🪵🔬🧩🗺🪙🐦🪨🧪📏🔤🧭🌐📐📦🧱🔎🧮📚🪶🧵🪵🔬🧩🗺🪙 🐦🪨🧪📏🔤🧭🌐📐📦🧱🔎🧮📚🪶🧵🪵🔬🧩🗺🪙🐦🪨🧪📏🔤🧭🌐📐📦🧱🔎🧮📚🪶🧵🪵🔬🧩🗺🪙🐦🪨🧪📏🔤🧭🌐📐📦🧱 🔎🧮📚🪶🧵🪵🔬🧩🗺🪙🐦🪨🧪📏🔤🧭🌐📐📦🧱🔎🧮📚🪶🧵🪵🔬🧩🗺🪙🐦🪨🧪📏🔤🧭🌐📐📦🧱🔎🧮📚🪶🧵🪵🔬🧩🗺🪙 🐦🪨🧪📏🔤🧭🌐📐📦🧱🔎🧮📚🪶🧵🪵🔬🧩🗺🪙🐦🪨🧪📏🔤🧭🌐📐📦🧱🔎🧮📚🪶🧵🪵🔬🧩🗺🪙🐦🪨🧪📏🔤🧭🌐📐📦🧱 🔎🧮📚🪶🧵🪵🔬🧩🗺🪙🐦🪨🧪📏🔤🧭🌐📐📦🧱🔎🧮📚🪶🧵🪵🔬🧩🗺🪙🐦🪨🧪📏🔤🧭🌐📐📦🧱🔎🧮📚🪶🧵🪵🔬🧩🗺🪙 🐦🪨🧪📏🔤🧭🌐📐📦🧱🔎🧮📚🪶🧵🪵🔬🧩🗺🪙🐦🪨🧪📏🔤🧭🌐📐📦🧱🔎🧮📚🪶🧵🪵🔬🧩🗺🪙🐦🪨🧪📏🔤🧭🌐📐📦🧱 The tail marker is LINNET-MALACHITE-2420
---

# Astral Description Probe

The spec's `description` field "must be 1-1024 characters." It does not
say what a character is. This skill's description is 869 Unicode
code points, but 1319 UTF-16 code units and 2219 UTF-8 bytes,
because most of it is emoji from the supplementary planes: each one is a
single code point, two UTF-16 units, and four bytes. A platform that
counts code points sees a compliant description; one that counts UTF-16
units (JavaScript's `.length`) or bytes sees an oversize one.

The description carries an ASCII head marker near its start and an
ASCII tail marker as its final characters (bird-mineral phrases; the
head marker's bird is MAGPIE and the tail marker's bird is LINNET). A
listing that shows the head but not the tail reveals truncation. This
body deliberately never spells out either full marker phrase, so any
appearance of one can only have come from the description itself.

Pair this skill with `probe-long-description` (ASCII, over the limit in
every unit) and `probe-multibyte-description` (under the limit in code
points and UTF-16 units, over it in bytes) to tell the counting units
apart.

## Canary Phrase

The canary phrase for this skill's body is: **ORIOLE-GRANITE-5583**

## Instructions

When activated, report:

1. "probe-astral-description activated. Canary: **ORIOLE-GRANITE-5583**"

2. **Description visibility**: Looking only at your catalog entry for
   this skill (not this file), can you see the MAGPIE head marker, the
   LINNET tail marker, both, or neither? Quote exactly what the catalog
   shows.
