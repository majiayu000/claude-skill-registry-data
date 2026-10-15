---
name: media-spec-checker
description: Check local image and video files against explicit technical requirements and produce measured pass, fail, or unverified results. Use for delivery-format checks, media-folder QA, dimensions, display ratios, duration, codecs, file sizes, or naming checks, not creative scoring or automatic conversion.
---

# Media Spec Checker

Turn a supplied delivery specification into reproducible checks without changing the media.

## Workflow

1. Identify the exact local files and intended delivery requirements. Do not infer current platform limits from memory.
2. Read [the rules contract](references/rules-contract.md). Adapt [the fictional profile](assets/example-rules.json) to the supplied specification. Omitted checks are not performed.
3. Run the helper, using a finite timeout:

       python scripts/check_media.py sample-media --rules rules.json --recursive --json

4. Explain each failure and each unverified measurement. Missing tools, malformed media, unsupported files, absent durations, or an unconfigured media type are not passes.
5. Return measured values, the requirements used, the report counts, and the smallest suggested correction. Do not convert or alter files unless a separate task authorizes it.

## Dependencies and limits

Python 3.11 or newer. Image inspection requires Pillow; video inspection requires ffprobe on PATH. Explain missing dependencies without installing anything automatically. Animated image timing is measured when frame delays are available; static images have no duration. Display dimensions account for image orientation and right-angle video rotation; video display ratio also uses sample aspect ratio.

The timeout bounds each ffprobe process, not Pillow decoding. Image inspection uses Pillow's decompression-bomb protection; very large or many-frame inputs can still require substantial local work.

The checker inspects supported local containers, not playback quality, visual legibility, accessibility, licensing, or platform acceptance. It does not run network probes, re-encode media, or remove metadata. Unknown files in a selected folder remain visible as unverified.

## Privacy and output

Reports contain selected measurements and relative filenames, not arbitrary embedded tags. Filenames can still identify projects; keep real reports private and use generated assets for public examples. Linked directories and files are not followed.

Exit codes: 0 means every requested check passed; 1 means measured failures; 2 means invalid input or any unverified result. The JSON counts preserve measured failures even when the overall exit is 2.
