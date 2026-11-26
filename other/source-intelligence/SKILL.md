---
name: source-intelligence
description: Guide for agents to help users extract OpenAPI specs from source code using NightVision Source Intelligence. Use when running openapi extract (also spelled swagger extract), identifying framework support, troubleshooting extraction, handling unresolved variables, comparing API specs, or understanding Code Traceback.
allowed-tools: Bash
---

# NightVision Source Intelligence

Use this skill when helping users generate OpenAPI specifications from their source code using `nightvision openapi extract`. Source Intelligence reads the source locally and deterministically (no running application or compilation needed, no source code uploaded, no LLM reads the code) and annotates the spec with source file paths and line numbers (Code Traceback) so that vulnerabilities found during DAST scans trace back to exact code locations.

The `nightvision openapi` command group needs CLI 0.18.0 or later. On an earlier release (`nightvision version`), use `nightvision swagger` in its place; later releases accept both names. `--no-target` needs CLI 0.19.0 or later; on an earlier release, use `--no-upload` in its place.

## Agent workflow

When a user asks to extract or document their API:

1. **Check prerequisites** — verify the NightVision CLI is available (`nightvision --help`)
2. **Examine the repo** — identify the backend languages and web frameworks and check them against the support matrix (see [references/framework-support.md](references/framework-support.md)). The CLI detects project roots and languages on its own; pass `--lang` only to restrict a run to one language
3. **Run extraction** — execute `nightvision openapi extract` with the appropriate flags, using `--no-target` if the user has no target yet (see [Choosing where the spec goes](#choosing-where-the-spec-goes)). On success, the CLI prints `"OpenAPI file extracted successfully."` and writes the spec to the output path (default: `openapi-spec.yml`)
4. **Review the output** — read the generated spec to check completeness. Handle unresolved variables if the run created `nv.config`
5. **Compare coverage** — if the user has an existing spec, run `nightvision openapi diff` to show what was discovered vs. what was documented
6. **Upload to target** — attach the spec to a NightVision target for scanning

**Related skills:** Use `scan-configuration` for target/auth setup, `ci-cd-integration` for pipeline integration, `scan-triage` for interpreting scan results.

## Supported languages and frameworks

`--lang` is optional: the CLI detects project roots and languages automatically. Use it only to restrict a run to one language.

| Language | `--lang` value | Frameworks (verified with CLI 0.22.7 and later) |
|----------|----------------|------------|
| Python | `python` | Django REST Framework, Flask, Flask-RESTful, FastAPI, Starlette, Connexion; Django URLconf (with gaps) |
| Java | `java` | Spring Boot MVC, Spring Data REST, Spring Boot Actuator, JAX-RS/Jersey (javax and jakarta), Micronaut, Quarkus, Dropwizard; Spring WebFlux annotated controllers |
| JavaScript/TypeScript | `js` | Express 4 and 5, NestJS, Fastify, Hono; oRPC (with gaps) |
| C# | `csharp` | ASP.NET Core controllers, Minimal APIs (incl. `MapGroup`), ASP.NET Web API 2 |
| Go | `go` | net/http (Go 1.22+ method patterns), Gin, Echo, Fiber v2 and v3, chi, gorilla/mux; httprouter (with gaps) |
| PHP | `php` | Laravel |
| Ruby | `ruby` | Rails; Grape (partial) |

Not supported today (0 routes): aiohttp, Sanic, Tornado, Litestar, Quart, Koa, hapi, Restify, AdonisJS, Next.js route handlers, Spring WebFlux functional `RouterFunction`, Javalin, Vert.x, Struts, NancyFX, ServiceStack, FastEndpoints, Carter, fasthttp, Sinatra, Hanami, Symfony, Slim, Lumen. For these, scan the running app with the crawler, upload an existing spec, or record traffic instead (see `scan-configuration`).

The CLI also accepts the aliases `dotnet` (C#) and `typescript` (JavaScript/TypeScript); the MCP `run-source-intelligence` tool accepts the same values. Plain Java servlets, Kotlin sources, and `.jsx`/`.tsx` files are not read; `.mjs`, `.cjs`, `.mts` and `.cts` are read alongside `.js` and `.ts`. A project needs its normal skeleton to be detected: `config/application.rb` for Rails, a `.csproj` for C#, a `main.ts` with `NestFactory` for NestJS. See [references/framework-support.md](references/framework-support.md) for what to check in the output per framework and for component coverage, and the [Framework Support Index](https://docs.nightviz.ai/source-intelligence/frameworks/) for the published matrix.

## Running extraction

```bash
# Try extraction before creating a target (output defaults to openapi-spec.yml);
# languages and project roots are detected automatically
nightvision openapi extract . --no-target

# Restrict a repository with several languages to one of them
nightvision openapi extract . --lang js --no-target

# Specify output file and format
nightvision openapi extract . -o api-spec.json --file-format json --no-target

# Extract and upload directly to a NightVision target
nightvision openapi extract . -t my-api -p my-project --lang python

# Upload nothing, when code-derived files must not leave the machine
nightvision openapi extract . -o openapi-spec.yml --lang java --no-upload

# Scan multiple source directories
nightvision openapi extract ./service-a ./service-b --lang python --no-target

# Extend an existing spec (add discovered endpoints to it)
nightvision openapi extract . --lang python --extend existing-spec.yml --no-target

# Exclude directories from analysis
nightvision openapi extract . --lang python --exclude vendor,generated --no-target

# Include code snippets in the spec (useful for debugging)
nightvision openapi extract . --lang python --dump-code --no-target
```

### Choosing where the spec goes

Every run needs one of these, or it fails with `no target given`:

| Flags | Use when |
|-------|----------|
| `-t` / `-T` (target name / UUID) | The user has an API target to scan; the spec is uploaded to NightVision and to the target |
| `--no-target` | The user has no target yet, is trying Source Intelligence, or wants to review the spec first |
| `--no-upload` | The user says code-derived files must not leave their machine |

Default to `--no-target` when there is no target; do not reach for `--no-upload` just because there is no target. With `--no-target` the spec is still uploaded to NightVision, just not to a target; `--no-upload` uploads nothing. `--no-target` cannot be combined with `-t` or `-T`. Without a target, the spec carries a default title and server instead of the target's name and URL.

### Extraction fallback for CI

Extraction exits non-zero when it finds no routes, for example on an unsupported framework, and also when the spec was written but the upload failed. Guard against both in pipelines without hiding the result: fall back to a backup spec only when no spec was written, keep the diagnostics file as a build artifact, and print why the fallback was taken.

```bash
if ! nightvision openapi extract . -t $TARGET; then
  if [ -e openapi-spec.yml ]; then
    echo "Spec extracted but the upload failed; keeping openapi-spec.yml"
  else
    echo "Source Intelligence produced no spec; see openapi-spec.diagnostics.json"
    cp backup-openapi-spec.yml openapi-spec.yml
  fi
fi
```

## Reports beyond the spec

The same `openapi extract` run can write two more reports. Both are written beside the spec and are uploaded with it unless `--no-upload` is given.

```bash
# Weak and quantum-vulnerable cryptography: algorithms, modes, key sizes and JWT settings in
# Python and JavaScript code, plus committed keys, certificates and TLS configuration in any language
nightvision openapi extract . -t my-api -p my-project --weak-crypto

# Hardcoded credentials (redacted report: <output>-credentials.json holds no credential value)
nightvision openapi extract . --no-target --credentials

# Seal found credentials to your own public key instead (the sealed file is never uploaded)
nightvision openapi extract . --no-target --credentials-key ./my-public-key.pem
```

- With a target (`-t`), the `--weak-crypto` report is stored with that target and appears on the target's **Quantum readiness** tab in the web app next to the runtime findings from scans (CLI 0.22.5 or later; JavaScript code analysis needs CLI 0.22.7 or later).
- Each upload replaces the target's previous source report, and findings it does not contain are resolved. Keep every upload to a target on the same scope: the same code paths, `--root-path` (set it to the repository's top level), `--lang`, `--exclude` and import settings. A narrower run resolves findings it never looked at; a run from another root re-reports everything as new. If quantum readiness is off for the organization, the upload is refused with a message and the extract still succeeds.
- Routes whose handlers call an LLM SDK (OpenAI, Anthropic, Bedrock, Gemini, LangChain and others, in Python, C#, Go, JavaScript/TypeScript, Ruby and PHP, CLI 0.22.2 or later) are tagged in the spec with `x-nv-dast-sinks: [llm-query]` (and `llm-tool-call` when tools are passed). When that spec is uploaded to a target, those routes fill the target's **LLM Endpoints** list automatically, so scans keep ordinary attack payloads off them. See `scan-configuration` for AI endpoint scanning.

## Handling unresolved variables

When static analysis can't resolve a variable (e.g., an API prefix read from an environment variable), it appears as a literal placeholder in the spec. NightVision generates an `nv.config` file to fix this.

**Steps:**
1. Run extraction — if unresolved variables exist, `nv.config` is created in the first detected project root, which need not be the spec's directory
2. Open `nv.config` — find the `replacements` object with `null` values
3. Replace `null` with the actual values (check the app's config files, environment vars, etc.)
4. Re-run extraction — the tool reads `nv.config` and substitutes the values. You can also use `-c` / `--config` to explicitly specify the config file path: `nightvision openapi extract . --lang python -c path/to/nv.config --no-target`

```json
// nv.config example
{
  "replacements": {
    "Microsoft.AspNetCore.Builder.WebApplication.Services...ApiPrefix": null
  }
}
```

The agent should help the user find the actual value by searching their config files (`appsettings.json`, `.env`, `settings.py`, etc.) and updating `nv.config`.

## Comparing API specs

Use `openapi diff` to measure coverage or detect breaking changes:

```bash
# Summary diff (paths and schemas counts)
nightvision openapi diff original-spec.yml discovered-spec.yml

# Show only path-level changes (endpoints added/removed/modified)
nightvision openapi diff original-spec.yml discovered-spec.yml --paths

# Show only schema changes
nightvision openapi diff original-spec.yml discovered-spec.yml --schemas

# Show the full diff (paths and schemas together, with details)
nightvision openapi diff original-spec.yml discovered-spec.yml --full-diff

# Save diff output to file
nightvision openapi diff original-spec.yml discovered-spec.yml -o diff-report.txt
```

Common use cases:
- **Coverage analysis** — compare a hand-written spec against the discovered one to find undocumented shadow APIs
- **PR checks** — diff specs from the base branch vs. PR branch to detect breaking API changes
- **Audit** — verify that all endpoints are documented

## Detecting project roots

`openapi detect` lists the project roots and languages that extraction would analyze; it does not find existing OpenAPI/Swagger files, so search the filesystem for those. The `detect` command takes no positional arguments — use `-p` to specify the root folder:

```bash
# Detect project roots in the current directory
nightvision openapi detect

# Detect in a specific directory
nightvision openapi detect -p ./path/to/code

# Save detection results as JSON
nightvision openapi detect -o detection-results.json
```

## Code Traceback

The generated spec includes `x-source` annotations on each endpoint with the file path and line number where the route is declared. When this spec is used for DAST scanning:

- Vulnerabilities found by NightVision link directly to the source code
- GitHub Security Alerts, Azure Boards work items, and Jenkins Warnings show the exact file and line
- Developers see where to fix, not just what to fix

This is why using NightVision-generated specs (vs. hand-written ones) significantly improves the triage experience.

## Diagnosing an empty or partial result

Every run that returns analysis results writes a diagnostics file beside the requested output, with the output's extension replaced (`openapi-spec.yml` gets `openapi-spec.diagnostics.json`). It is written even when no route was found. Summarize it with `openapi diagnose`, which runs offline and needs no login:

```bash
nightvision openapi diagnose openapi-spec.yml
```

Read it in this order:

1. `Result` and `Roots`: which project roots and languages were detected, and how many files, entry points and paths each root contributed. `no file interpreted: <language>` means the language was detected but no source of it was read (for example a Kotlin project detected as Java).
2. `Unresolved imports`, group `framework`: imports of a web framework the analyzer does not model. This group is filled for Python, PHP and C#; for the other languages look through `third-party` for a framework name (for example `koa`, `github.com/kataras/iris`, `sinatra`).
3. `Containment`: a recovered framework, handler or language-phase failure means part of the result is missing.
4. `Losses`: discoveries the analyzer knowingly dropped.

For C# projects the diagnostics file also lists `unmodeledFrameworks`, the web packages a project references that the analyzer does not model.

## Troubleshooting

| Issue | Cause | Fix |
|-------|-------|-----|
| No endpoints found | Unsupported framework, a project root that was not detected, or `--lang` restricting the run to the wrong language | Run `nightvision openapi diagnose <output>` and check the roots table and the unresolved framework imports; omit `--lang` to let the CLI detect languages; check the support matrix |
| Unresolved variables in paths | Config values read from env vars without defaults | Fill in `nv.config` replacements and re-run |
| Incomplete routes | Custom routing, non-standard framework usage | NightVision relies on standard framework patterns; custom routing may not be detected |
| Extraction fails entirely | Syntax errors in source, missing files | Read the CLI log, and the diagnostics file beside the requested output if the run wrote one (the output's extension is replaced, so `openapi-spec.yml` gets `openapi-spec.diagnostics.json`); `--diagnostics` only embeds a summary in a generated spec |
| Spec missing sub-routes | Code in subdirectories not scanned | Pass multiple paths: `nightvision openapi extract ./src ./lib --no-target` |

For unsupported frameworks or components, contact support@nightviz.ai.
