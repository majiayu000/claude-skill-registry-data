---
name: docgen
description: Author and modify documentation for projects that use Gehtsoft's docgen utility. Use this skill whenever the user mentions docgen, .ds files, the doc/ directory of a repository, project.xml or project.proj for documentation, or wants to write/edit/build/debug API documentation in any codebase that uses docgen. Also use it whenever the user asks about generating C#, C++, or Java API documentation that follows Gehtsoft conventions, even if they don't say "docgen" explicitly.
---

# Gehtsoft docgen

Docgen is Gehtsoft's documentation tool. It reads hand-written `.ds` source files plus auto-generated `.ds` files (extracted from C# XML doc comments via `Asm2Xml`, or from C++/Java via `doxygen`) and produces HTML, CHM, or Markdown output through XSLT templates.

Use this skill to:

- Set up a new docgen project for a C#, C++, or Java codebase.
- Add or edit `.ds` content (articles, namespace overviews, class/member descriptions).
- Wire up auto-generation from source code so "voids" in hand-written docs get filled automatically.
- Diagnose why generated docs look wrong, links break, or auto-generated content is being silently overridden.

## The mental model

There are three layers; understanding all three is the difference between fixing problems quickly and chasing ghosts.

```
Source code  --[extractor]--> raw XML  --[XSLT]--> auto-generated .ds
                                                          |
                                                          v
   hand-written .ds (index, articles, key namespaces) --[docgen]--> HTML/CHM/MD
```

- **Extractor** depends on language: `Asm2Xml` for C# DLLs (uses Mono.Cecil); `doxygen` for C++ and Java sources.
- **XSLT** uses templates bundled with docgen. Reference them via `%docgen%` (the docgen install root): `%docgen%/template/cs2ds/main.xsl` for C#, `%docgen%/template/doxygen2ds/main.xsl` for C++/Java. The template emits `.ds` files into a `prepare/.../dst` or `src/raw` directory.
- **docgen** parses every `.ds` listed in `<dg:source>`, builds a model keyed by `@key`, and renders through an output template such as `%docgen%/template/html/main.xsl`.

## Three workflows

Pick the one that matches the user's project before scaffolding.

### 1. 100% manual

Everything is hand-written. No `prepare/` step, no `raw/` folder. Use this when:
- The codebase is small or the docs are narrative (tutorials, guides) more than reference.
- The user wants tight editorial control.

Layout:
```
doc/
├── project.proj    # MSBuild target MakeDoc
├── project.xml     # docgen config; <dg:source> lists hand-written files only
├── doc.bat         # dotnet build project.proj /t:MakeDoc
├── src/
│   ├── index.ds
│   ├── articles/
│   └── ...
└── dst/            # output (gitignored)
```

### 2. C# auto + manual

A two-stage build. The `prepare/` stage runs `Asm2Xml` on built DLLs and an XSLT (`cs2ds/main.xsl`) to emit `.ds` files. The main stage consumes hand-written files **plus** the generated files.

Layout:
```
doc/
├── project.proj            # main MSBuild
├── project.xml             # main docgen config
├── doc.bat
├── prepareproject.xml      # docgen project for the cs2ds conversion
├── preparesettings.xml     # cs2ds tuning (assembly path, namespaces to strip)
├── prepare.bat             # dotnet build project.proj /t:Scan,Raw
├── obj/raw.xml             # Asm2Xml output (intermediate)
├── src/
│   ├── index.ds
│   ├── ns/                 # hand-written namespace/class overviews
│   ├── null.ds             # stub for prepareproject.xml
│   └── raw/                # auto-generated .ds files
└── dst/
```

Two assembly patterns exist:
- **Single-stage merged**: main `project.xml` lists both `src/ns/` and `src/raw/`. `Scan` and `Raw` targets live in the same `project.proj` as `MakeDoc`. Simpler.
- **Two-stage isolated**: `prepare/` is its own MSBuild sub-project with its own `project.proj`; the main build doesn't run prepare automatically. Useful for multi-language projects.

The single-stage pattern is the recommended default for new projects.

### 3. Doxygen auto + manual (C++ / Java)

Same shape as the C# pattern, but the extractor is `doxygen` (configured by a `Doxyfile`) and the XSLT is `doxygen2ds/main.xsl`. Per-language prepare directories are typical when documenting multiple languages:

```
doc/
├── prepare/
│   ├── cpp/   Doxyfile + project.proj + prepareproject.xml + dst/
│   └── java/  Doxyfile + project.proj + prepareproject.xml + dst/
├── src/
│   ├── cpp/   hand-written + .ds copied from prepare/cpp/dst/
│   └── java/  same
└── ...
```

## The merge mechanism (read this carefully)

Every `.ds` element has a `@key` (e.g., `Foo.Bar` for a namespace, `Foo.Bar.MyClass` for a class). Docgen parses every file in `<dg:source>` order and builds one model. When two files define the same `@key`, the **first one wins**.

Behavior depends on the element type:

| Element  | First-defined behavior                              | Member merge?                          |
|----------|-----------------------------------------------------|----------------------------------------|
| `@group` | First wins; later duplicates silently removed       | No                                     |
| `@class` | First wins for class-level fields (brief, etc.)     | **Yes** — non-conflicting members from later class are added |
| `@member`| First wins; later duplicate members silently dropped| n/a                                    |
| `@article`| First wins                                         | n/a                                    |

**The class-level member merge is the whole reason for the dual-source pattern.** Hand-write a `@class` block in `src/ns/` documenting only the methods you care about; let the auto-generated `src/raw/` file fill in the rest. As long as the class `@key` matches, members merge automatically.

**The merge is silent.** No warning, no error if a hand-written entry shadows an auto-generated one. If something looks wrong:
- A class `@brief` you wrote isn't appearing → check whether another file (loaded earlier) defines the same class.
- An auto-generated method isn't showing up → check whether you wrote a `@member` with the same key (often a CRC-suffixed name) in a hand-written file.

**Order of `<dg:source>` matters.** Put hand-written first, auto-generated last. Always.

```xml
<dg:source>
    <dg:file name="src/index.ds" encoding="utf-8" />
    <dg:folder name="src/ns" encoding="utf-8" />
    <dg:folder name="src/raw" encoding="utf-8" />  <!-- last -->
</dg:source>
```

## Common tasks — quick reference

### "Set up docgen for this project"

1. Identify the workflow (manual / C# / doxygen) by asking the user or inspecting the codebase.
2. Create `doc/` at the repository root.
3. Copy from the matching scaffold tree under `assets/`:
   - `assets/manual-only/` — 100% hand-written.
   - `assets/csharp-single-stage/` — C# library with auto-generation (recommended default for new C# projects).
   - `assets/doxygen-cpp-only/` — C++ library with doxygen auto-generation.
   - `assets/doxygen-java-only/` — Java library with doxygen auto-generation.
   - `assets/doxygen-multilang/` — both C++ and Java in one docs site.
4. Replace the `REPLACE_WITH_*` placeholders in the copied files (project name, project title, assembly path, source paths).
5. For C# scaffolds: ensure the library's `.csproj` has `<GenerateDocumentationFile>true</GenerateDocumentationFile>`, then run `prepare.bat` once to populate `src/raw/`, then `doc.bat` to build.
6. For doxygen scaffolds: set `INPUT` in each `Doxyfile`, run `prepare.bat` from each `prepare/<lang>/`, copy generated `.ds` files into `doc/src/<lang>/`, then `doc.bat` from `doc/`.
7. See `assets/README.md` for the per-scaffold checklist; see `references/source-extraction.md` for what each prepare file does.

### "Document this class / namespace by hand"

1. Decide where the file goes: namespace overviews → `src/ns/Namespace.Name.ds`; cross-cutting articles → `src/articles/topic.ds`.
2. Write a `@group` (for a namespace) or `@class` (for a single class) block. Set `@key` to the fully-qualified name; set `@ingroup` to the parent group's `@key`.
3. For a class, document only the members worth highlighting — auto-generation will fill the rest as long as `@key` matches.
4. See `references/ds-format.md` for the tag and BBCode reference.

### "Override a specific auto-generated method or property"

Auto-generated `@member` keys for methods/overloaded members carry a CRC suffix (e.g. `Tessellate.A1B2C3D4`) so different overloads don't collide. To override one with a hand-written version you must use the **same key**, suffix included — otherwise both members appear in the rendered docs as separate entries.

1. After running `prepare.bat`, open the generated file: `src/raw/<Namespace>.<Class>.ds`.
2. Find the `@member` block whose `@name` (or signature) matches the method you want to override. Note its `@key` — copy it verbatim, CRC suffix included.
3. In your hand-written `src/ns/<Namespace>.<Class>.ds`, write a `@class` block with `@key=<Namespace>.<Class>` and inside it a `@member` block using the **exact** key from step 2.
4. The first-defined-wins merge rule (see "The merge mechanism" above) silently shadows the auto-generated member with yours. Other members of the class still come from `src/raw/`.
5. After the next `prepare.bat`, re-verify the suffix hasn't changed (it normally won't unless the signature changed).

For methods without overloads, the suffix is stable; for overloaded methods, watch out — adding/removing parameters changes the signature CRC and your override will silently stop working (you'll see the auto-generated method reappear). Always copy the key from the generated file rather than trying to compute it.

### "Add a new article"

1. Create `src/articles/topic.ds` (or wherever the project organizes articles).
2. Open with `@article`, set `@key`, `@title`, `@ingroup`, `@brief`, write the body, close with `@end`.
3. If the article is referenced from `index.ds` or another article, add a `[link=topic-key]link text[/link]`.
4. Confirm `<dg:source>` in `project.xml` covers the location (folder include is usually enough).

### "Refresh auto-generated docs after source code changed"

For C#:
```
cd doc && prepare.bat
```
This rebuilds `obj/raw.xml` from the assemblies and regenerates `src/raw/*.ds`.

For doxygen:
```
cd doc/prepare/<lang> && prepare.bat
```
Then copy or sync the generated `.ds` files into the location referenced by the main `project.xml`.

### "Build the docs"

```
cd doc && doc.bat
```
or
```
cd doc && dotnet build project.proj /t:MakeDoc
```

Output lands in `doc/dst/`.

### "Verify the docs before shipping"

The source→`.ds`→HTML transforms have surprises that are **invisible in the source** (see the gotchas in `references/source-extraction.md` and `references/ds-format.md`). Always verify against the *generated `.ds`* and, where possible, the *rendered HTML* — not just the `///` comments or hand-written `.ds`. After a `prepare.bat` / `doc.bat` run, these cheap deterministic checks catch the common failures:

```bash
# Multi-line @brief (a C# <summary> with no blank-line paragraph break dumps everything into @brief)
awk '/@brief=/{b=substr($0,index($0,"=")+1); getline n; gsub(/^[ \t]+/,"",n);
     if (b!="" && n!="") print FILENAME": multi-line @brief -> "b}' src/raw/*.ds

# C# formatting tags that should be docgen BBCode ([c]/[i]/[b]); leave <see cref>/<paramref> as XML
grep -rnoE '</?(c|i|b|u)>' --include=*.cs .

# Line-leading bullet markers that aren't an intentional @list (both consumed .ds and source comments)
grep -rnE '^[[:space:]]*[-*][[:space:]]' src/index.ds src/ns/*.ds src/raw/*.ds
grep -rnE '^[[:space:]]*///[[:space:]]*[-*][[:space:]]' --include=*.cs .

# Raw & in hand-written .ds (must be &amp;, else single & emits unescaped and && loses a character)
# uses -P (PCRE) for the negative lookahead; on macOS/BSD grep without -P, use ripgrep: rg '&(?!amp;|lt;|gt;|quot;|#)'
grep -rPn '&(?!amp;|lt;|gt;|quot;|#)' src/index.ds src/ns/*.ds src/articles/*.ds
```

Also eyeball any `@example` with relative indentation (does it need `!`-prefixed lines?) and any run of `@see` blocks (prefer a "See also" `@headline` + `@list`).

### "Fix broken cross-references"

Docgen validates `[link=key]` against defined `@key` values. The build emits errors listing keys that aren't defined. Typical causes:
- Typo in `@key` or in the link itself.
- Auto-generated raw file shadowed by a hand-written one with a different (older) key.
- An `@import` referencing a key that no longer exists (parser emits `@import key X is not found`).

## Reference files

Read the relevant reference when working on the matching task. Don't load all of them at once.

- `references/project-files.md` — `project.proj`, `project.xml`, `doc.bat` structure with annotated examples. Read when scaffolding or modifying the build.
- `references/ds-format.md` — `.ds` DSL: `@group`, `@article`, `@class`, `@member`, `@param`, `@declaration`, `@example`, `@list`, `@table`; the two inline-formatting syntaxes (markdown `**`/`` ` ``/`#`/`|...|` and BBCode `[b]`/`[c]`/`[link=]`/`[clink=]`/`[img=]`/`[eurl=]`) and when to use each; escaping rules. Read when writing or editing `.ds` content.
- `references/source-extraction.md` — `Asm2Xml` (C#), `doxygen` (C++/Java), `cs2ds`/`doxygen2ds` XSLT, prepare project layout. Read when wiring auto-generation.

## Conventions

These are not enforced by the tool but are the de-facto Gehtsoft standard. Match them when scaffolding so the project blends in with sibling projects:

- Documentation root is `doc/` at the repository root.
- Build artifacts live in `doc/dst/` (gitignored).
- The MSBuild file is `project.proj`; the docgen config is `project.xml`. Don't invent new names.
- A one-liner `doc.bat` wraps the MSBuild invocation: `dotnet build project.proj /t:MakeDoc`.
- A `prepare.bat` (when auto-gen is wired up) runs `Scan,Raw` for C# or `Doxygen,Prepare` for doxygen.
- `simplified-text-syntax=yes` is always set in `<dg:common>`.
- `<dg:source>` order: `index.ds` first, hand-written folders next (`src/ns/`, `src/articles/`), `src/raw/` last.
- Auto-generated `.ds` files go into `src/raw/` (single-stage) or are produced by `prepare/` and either copied into `src/raw/` or referenced directly from `prepare/.../dst/`.
- `src/raw/` is committed to the repo. The docs build does not require source code to be present — it requires having run `prepare.bat` previously.

## Style for `.ds` content

- Keep `@brief` to one sentence. It appears in indexes and tooltips; longer briefs make navigation noisy.
- **Two formatting syntaxes coexist** (both enabled by `simplified-text-syntax=yes`): a compact **markdown** style and the original **BBCode**. Pick by these rules: (a) **match the style already established** in the project/document — don't mix the two within one file for no reason; (b) for **brand-new** documentation, **prefer markdown** (`**bold**`, `` `code` ``, `# heading`, `*`/`0` lists, `|a|b|` tables). Reach for BBCode for what markdown can't express — code-style API links `[clink=key]name[/clink]`, colors, `[sub]`, `[img]`, `[eurl]`. Full mapping and reference in `references/ds-format.md`.
- Use `[clink=key]name[/clink]` for API references (renders the symbol in code style); use `[link=key]text[/link]` (or markdown `[text]key`) for narrative links.
- For multi-line code use `@example` (or a markdown ```` ``` ````-fence) — the fence also preserves indentation, which a bare `@example` body does not.
- Don't duplicate what auto-generation will already provide. Hand-written content earns its place by adding context, examples, or organization that the source can't.

## Diagnosing the silent merge

Because shadow-merges are silent, the diagnostic process when something seems missing or wrong is:

1. Search every `.ds` file under `<dg:source>` for the `@key` in question (`grep -r "@key=Foo.Bar"`).
2. Determine the load order. The first match wins. If the first match is a hand-written stub with no `@brief`, that explains the empty brief.
3. For class members, also grep for the member name — generated keys often have a CRC suffix (`Calculate.A1B2C3D4`) that won't match a hand-written `@key=Calculate`. Different keys mean both members exist and the auto-generated one shows up under a different name.
