---
name: dify-plugin-builder
description: >-
  Build and package a Dify plugin (a .difypkg file) from a description of what the tool should do.
  Use this whenever the user wants to create, build, or package a Dify plugin / tool plugin / 插件 /
  .difypkg — e.g. "做一个把文本转成可下载文件的Dify插件", "帮我做个Dify工具插件调用某个API",
  "build a Dify plugin that converts markdown to PDF", "package this as a .difypkg". Trigger even if
  they don't say ".difypkg". The skill scaffolds the plugin from a proven template, fills in the
  tool logic, and packages it correctly for air-gapped/内网 Dify with bundled offline wheels.
---

# Dify Plugin Builder

Scaffold, implement, and package a **Dify tool plugin** into an installable `.difypkg` for
air-gapped/内网 Dify. Assume the target Dify server cannot reach the internet. The template and
packaging scripts encode several non-obvious gotchas that otherwise cost hours.

## Non-negotiable delivery rule

Every generated plugin must be **fully offline installable**: `requirements.txt` must use
`--no-index` + `--find-links=./wheels/`, and `wheels/*.whl` must be included in the `.difypkg`.
Do not deliver a plugin package that depends on the Dify server reaching PyPI.

## Workflow

1. **Understand the tool.** What does it take in, what does it produce (text / structured JSON /
   a downloadable file)? Does it need network or a credential/API key?
2. **Scaffold the plugin.** Prefer the deterministic scaffold over manual copying:
   `python3 scripts/scaffold_plugin.py /tmp/<plugin_name> --name <plugin_name> --author <author_id> --label-zh "<中文名>" --label-en "<English name>" --description-zh "<中文描述>" --description-en "<English description>"`
   Use `--mode downloadable-file|text|json`; the default is a downloadable-file tool that already
   uses `meta["filename"]`.
3. **Fill in or replace the tool logic** (see `references/plugin-guide.md` for the full SDK
   reference):
   - `manifest.yaml`: set `author`, `name`, labels, description. `author` must be lowercase
     `[a-z0-9_]`; it forms the `provider_id` prefix.
   - `provider/<provider>.yaml` + `.py`: rename, set identity. No credentials → leave
     `_validate_credentials` returning. Needs an API key → declare it and validate.
   - `tools/<tool>.yaml` + `.py`: define parameters and the `_invoke` logic. The template's example
     tool returns a downloadable file — adapt or replace it.
   - Rename the referenced files and update the `source:` / `tools:` paths to match.
4. **Prepare offline dependencies** (required):
   - If this machine can reach PyPI for the target platform:
     `bash scripts/fetch_offline_wheels.sh /tmp/<plugin_name> 3.12 manylinux2014_aarch64`
   - If not, copy wheels from a plugin already verified on the same Dify server:
     `python3 scripts/prepare_offline_plugin.py /tmp/<plugin_name> --wheels-from /path/to/verified/wheels`
   - If neither is available, stop and ask for the target server platform or a verified wheels
     directory. Do not package an online-only plugin.
5. **Package:** `bash scripts/pack_plugin.sh /tmp/<plugin_name> <plugin_name>.difypkg`
   The script uses `zip -D` (no directory entries) — required, or install fails with
   `read tools: is a directory`. It also refuses to package unless offline requirements and
   `wheels/*.whl` are present.
6. **Deliver the `.difypkg`** and tell the user how to install (Dify → 插件 → 安装插件 → 本地文件),
   plus any post-install step (select a model, fill credentials).

## Offline dependency source

The Dify plugin daemon installs Python deps during plugin install. In our scenario it has no
internet. Always bundle wheels. `manylinux2014_aarch64` is common for ARM64 servers; use
`manylinux2014_x86_64` for x86_64. If unsure, ask for the server architecture before packaging.

## Output a downloadable file from a tool (common, and full of traps)

`self.create_blob_message(blob=bytes, meta={...})` is the way. Two traps the template already handles:

- **Filename:** dify-api reads `meta["filename"]` (NOT `file_name`). Wrong key → file is named with a
  random hash.
- **Extension / clickable download:** the file's URL ends in an extension guessed from the mime type
  (yaml/many types → `.bin`). The *downloaded* name comes from `meta["filename"]` only when the
  request URL has `?as_attachment=true`. So in the **workflow** that calls this tool, append
  `&as_attachment=true` to the file's `url` before presenting it (a small code node can do this).

Full SDK details (message types, `session.file.upload`, signing) are in
`references/plugin-guide.md` — read it before writing non-trivial tool logic.

## Sanity-check before packaging

```bash
python3 -m py_compile /tmp/<plugin_name>/main.py /tmp/<plugin_name>/provider/*.py /tmp/<plugin_name>/tools/*.py
python3 -c "import yaml,glob; [yaml.safe_load(open(f)) for f in glob.glob('/tmp/<plugin_name>/**/*.yaml',recursive=True)]"
```
After packaging, confirm `目录条目=0` and `manifest在根=1` (the script prints both).

When changing this skill, run:

```bash
python3 -m unittest tests.test_plugin_builder
```
