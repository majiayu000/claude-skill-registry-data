---
name: probe-multibyte-description
description: Benchmark skill whose description stays under the spec's 1024-character limit when counted in characters but runs past it when counted in UTF-8 bytes. Use when asked to probe description length units. The head marker GANNET-PYRITE-1130 sits near the start of this description and a tail marker sits at the very end. このスキルの説明文は、仕様が定める1024文字の上限を文字数では下回りますが、UTF-8のバイト数では上回ります。日本語の文字は一文字あたり三バイトを占めるため、文字数とバイト数の差が大きく開きます。プラットフォームがこの説明文をそのまま受け入れれば、長さを文字数で数えているか、あるいは長さを検証していないかのどちらかです。逆にこのスキルを拒否したり、説明文の末尾を切り捨てたりするなら、長さをバイト数で数えている可能性が高いと言えます。この段落は意図的に日本語で書かれた詰め物であり、スキルの機能を追加するものではありません。検証の対象は説明文の長さの数え方だけであり、それ以外の点ではこのスキルは通常の有効なスキルです。説明文の冒頭と末尾には英語の目印が置かれているため、末尾の目印が見えるかどうかで切り捨ての有無を判断できます。英語以外の言語で書いた説明文が、あるプラットフォームでは受け入れられ、別のプラットフォームでは静かに拒否されるかもしれないという点が、スキルの作者にとって重要です。この違いはエラーとして表面化しないため、数え方の違いを実際に観測して記録する必要があります。 The tail marker is SHRIKE-TALC-2210
---

# Multibyte Description Probe

The spec's `description` field "must be 1-1024 characters." It does not
say what a character is. This skill's description is 848 Unicode
code points (and the same number of UTF-16 code units, since every
character is in the Basic Multilingual Plane), but 1822 UTF-8 bytes,
because most of it is Japanese prose at three bytes per character. A
platform that counts code points or UTF-16 units sees a compliant
description; one that counts bytes sees an oversize one.

The description carries an English head marker near its start and an
English tail marker as its final characters (bird-mineral phrases; the
head marker's bird is GANNET and the tail marker's bird is SHRIKE). A
listing that shows the head but not the tail reveals truncation. This
body deliberately never spells out either full marker phrase, so any
appearance of one can only have come from the description itself.

Pair this skill with `probe-long-description` (ASCII, over the limit in
every unit) and `probe-astral-description` (under the limit in code
points, over it in UTF-16 units and bytes) to tell the counting units
apart.

## Canary Phrase

The canary phrase for this skill's body is: **PUFFIN-BASALT-4471**

## Instructions

When activated, report:

1. "probe-multibyte-description activated. Canary: **PUFFIN-BASALT-4471**"

2. **Description visibility**: Looking only at your catalog entry for
   this skill (not this file), can you see the GANNET head marker, the
   SHRIKE tail marker, both, or neither? Quote exactly what the catalog
   shows.
