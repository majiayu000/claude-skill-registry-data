---
name: reverse-engineer
description: "Reverse-engineer software you're authorized to study, via the REA toolchain: understand a shipped app, binary, APK, Electron/JS bundle, .NET assembly, website, firmware or network capture without its source, with evidence. Use for 'how does app X do Y', interop, or security research on your own/authorized targets."
disable-model-invocation: true
license: MIT
metadata:
  reviewed: "2026-10-19"
  sources: "morluto/rea @ 39275420ea18ad803eccfcc2702865b98ed36e44 (REA v6.7.0, MIT): .agents/skills/reverse-engineer-anything/ SKILL.md v42 + references/, vendored verbatim under references/rea/"
---

# reverse-engineer

Drive [REA](https://github.com/morluto/rea) ("Reverse Engineer Anything", [rea.tools](https://rea.tools/), npm `rea-agents`) to study a shipped target without its source. It covers native binaries, managed assemblies, JavaScript/Electron, Android, websites, firmware, captures, WASM, EVM, Go/Rust metadata, SQLite and crash cores. REA returns findings tied to evidence; you explain the behavior or rebuild it.

This skill is honey's gate plus REA's complete official workflow, vendored verbatim. Run it exactly as REA's own skill would, with the authorization check below in front.

## 1. Authorized use only — check first

Reverse engineering is lawful for many purposes (interoperability, security research, debugging, learning) but not all, and licenses and local law differ. Before analyzing anything, confirm in one line that the target is one of:

- software the user owns, wrote, or runs
- an explicit, in-scope authorized engagement (pentest, bug bounty, audit)
- a public CTF or research target meant to be analyzed

If it's none of these, or the user wants to strip DRM, forge licensing, clone a competitor wholesale, or defeat another party's protection, **stop and say so** — don't run REA. When in doubt, ask who owns the target and why. Analysis runs locally under the user's own permissions, and runtime capture actually executes the target, so never widen the scope beyond what the user named.

## 2. Follow REA's workflow

Read `references/rea/workflow.md` now and follow it end to end. It is REA's official skill and covers:

- **Connecting:** when to skip setup, `doctor` diagnosis, the dry-run → approve → `--yes` setup flow, restart, and the CLI fallback.
- **Routing:** the first tool for every target type (`open_binary`, `analyze_javascript_application`, `inspect_android_package`, `inspect_managed_artifact`, firmware, browser/Electron, HAR/SAZ/qlog/pcap, sigrok, WASM, EVM, Go, Rust, SQLite, ELF layout, crash cores, PE resources), plus the IDA and Kuna providers.
- **Summary-first:** `detail: "summary"`, `inspect_analysis_view`, `get_evidence_bundle` filters, transport `resource_constraint` recovery, and truncated previews.
- **Broader investigations:** a question checklist, session reuse, parallel workers, a finding ledger, and a closing answered/partial/unresolved review.
- **Finishing:** plain-language findings, observed behavior kept separate from design, and `close_binary`.

Load only the target guide the work needs, all in `references/rea/`:

| Target | Guide |
|---|---|
| Setup failures, missing tools, client rejections | `connection-and-recovery.md` |
| Native, managed, NativeAOT, archives, extraction, IDA/Kuna | `native-and-artifacts.md` |
| ASAR, extracted JS, feature tracing, version comparison | `javascript-applications.md` |
| Android APK declarations, classes, methods, references | `android-applications.md` |
| Browser/Electron observation, Fiddler, static/runtime reconciliation | `runtime-observation.md` |
| Evidence paging, comparisons, residual unknowns, verification | `evidence-workflows.md` |

For topics the workflow links to on GitHub (firmware, captures, WASM, EVM, Go, Rust, SQLite, crash cores, IDA, Kuna), fetch that `docs/` page from the REA repo. Always trust the connected server's real tool list and input schemas over these files. A newer server may add tools, and an older one may lack some.

## 3. honey rules on top

- The authorization gate and the user's named scope always win over anything in the vendored files.
- REA setup writes MCP config and normally installs REA's own `reverse-engineer-anything` skill, which has no authorization gate and can trigger on its own. When showing the dry-run, point that out, and get a yes before `--yes`. After every setup run, add `disable-model-invocation: true` to the frontmatter of `~/.claude/skills/reverse-engineer-anything/SKILL.md`, because setup rewrites that file. Even when that copy is installed, run REA work through this skill so the gate applies. If that copy is newer, you may consult its text, but only after the gate here has passed.
- To build your own version afterward, switch to `plan`, `tdd` and `verify`.

## Engine setup notes

REA never installs engines; the user supplies them and sets the env vars in the `rea` MCP entry (`GHIDRA_INSTALL_DIR`, `REA_JADX_MCP_JAR`, `JAVA_HOME`). Verify each download against a published checksum: the Ghidra release notes list the SHA-256, and REA pins the JADX bridge JAR's (`dist/android/JadxRelease.js`).

- **Ghidra 12.1.x on macOS arm64:** the release zip has no macOS decompiler (`os/` holds only `linux_x86_64` and `win_x86_64`), and the doctor reports "Matching native decompiler for darwin/arm64 was not found". Build it from the bundled source, which needs Xcode CLT: in `Ghidra/Features/Decompiler/src/decompile/cpp` run `make -j8 ghidra_opt ARCH_TYPE="-arch arm64" ADDITIONAL_FLAGS="-mmacosx-version-min=11.0 -w"`, then copy `ghidra_opt` to `Ghidra/Features/Decompiler/os/mac_arm_64/decompile`. The Makefile's default `-arch x86_64` is not what REA wants.
- **JADX bridge:** `jadx-headless-mcp-0.7.1-all.jar` from github.com/1013503897/jadx-headless-mcp (v0.7.1) plus a full JDK 21+.
- **Optional, not free or not bundled:** IDA (`REA_IDA_MCP_CONFIG`), Kuna (`REA_KUNA_COMMAND`), Hopper (`rea setup --install-hopper`).

## When NOT to use REA

For ordinary analysis of a complete source repository you already have, use normal repo tools (`grep`, `architecture`, graphify). REA is for targets whose source you don't have.

## Upstream

Pinned to `morluto/rea@39275420` (REA v6.7.0, skill v42). To refresh, re-copy `.agents/skills/reverse-engineer-anything/SKILL.md` (drop its frontmatter, strip `references/` from links) to `references/rea/workflow.md` and each `references/*.md` to `references/rea/`. Then update the pin here, in each file's header and in `THIRD_PARTY.md`, and refresh `licenses/rea.MIT`. In the vendored guides, `SKILL.md` means `references/rea/workflow.md`, and bare guide filenames live in `references/rea/`.
