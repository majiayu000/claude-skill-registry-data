---
name: dependency-analysis
description: How to evaluate libraries for health, security, license compatibility, and size impact before adopting or continuing to use them.
compatibility: opencode
metadata:
  audience: dependency-analyst
  purpose: dependency-evaluation
---
## What I do

Provide a systematic framework for evaluating software dependencies. Every library you depend on is code you don't control — this skill helps you assess whether that trade-off is worth it and when it stops being worth it.

## When to use me

Load this skill when evaluating a new dependency for adoption, auditing existing dependencies for risk, or deciding whether to replace a library with an alternative.

## Health signals

A library's health predicts whether it will receive bug fixes, security patches, and compatibility updates. Evaluate these signals together — no single metric is conclusive.

### Commit frequency

- **Healthy**: Regular commits (weekly to monthly) over the past year. Doesn't need to be daily — mature libraries often have lower commit frequency.
- **Warning**: No commits in 6+ months on a library that's not "finished" (i.e., it interacts with changing ecosystems like web frameworks, language runtimes, or APIs).
- **Exception**: Some libraries are genuinely complete (e.g., a math utility). No commits is fine if there are no open bugs and the library's domain is stable.

### Issue response time

- Check the last 20 issues. How quickly does a maintainer respond? A response within a week is healthy. Issues sitting unanswered for months is a warning.
- Distinguish between "acknowledged and triaged" (healthy) and "no response at all" (warning). Not every issue needs an immediate fix, but silence signals abandonment.

### Release cadence

- Regular releases (even if infrequent) indicate active maintenance.
- A long gap between the last commit and the last release means fixes exist but aren't being shipped. This is sometimes worse than no commits — users can't get patches without building from source.

### Bus factor

- How many people have committed in the past year? A library maintained by a single person is a risk — if that person stops, the library stops.
- Check if the library is backed by an organization or company. Organizational backing isn't a guarantee, but it reduces single-point-of-failure risk.
- Check if there are documented maintainer succession plans or multiple people with release permissions.

### Community signals

- Stars and download counts indicate adoption but not quality.
- More useful: Are there active forks? Are PRs from external contributors being merged? Is there a discussion forum or Discord with actual activity?

## Vulnerability assessment

### CVE databases

- Check the library against the National Vulnerability Database (NVD), GitHub Advisory Database, and language-specific advisory databases (e.g., RustSec for Rust, npm advisories for JavaScript).
- Look at not just current vulnerabilities but the history. A library with frequent critical CVEs may have systemic security problems in its design, not just individual bugs.

### Dependency tree depth

- A library with 3 dependencies is easier to audit than one with 300. Deep dependency trees increase the surface area for vulnerabilities.
- Map the transitive dependency tree. You're responsible for vulnerabilities in every transitive dependency, even if you didn't choose them directly.
- Watch for duplicate dependencies at different versions — this can indicate incompatibility issues and increases attack surface.

### Transitive risks

- A direct dependency may be healthy, but its dependencies may not be. Check the health signals of significant transitive dependencies (especially those that handle network, crypto, or parsing).
- Use tools like `npm audit`, `cargo audit`, `pip audit`, or `go vuln check` to scan the full tree.

## License compatibility

### Copyleft vs permissive

- **Permissive** (MIT, Apache 2.0, BSD): Use freely in commercial and open-source projects. Minimal obligations (typically attribution only).
- **Weak copyleft** (LGPL, MPL): Can be used in proprietary software if the library itself remains open and modifications to it are shared. Dynamic linking is generally safe; static linking may trigger copyleft obligations.
- **Strong copyleft** (GPL, AGPL): Requires derivative works to be released under the same license. Using a GPL library in a proprietary project typically means the entire project must be GPL. AGPL extends this to network use — even SaaS deployments trigger the obligation.

### Commercial use restrictions

- Some licenses include non-commercial clauses (CC-BY-NC) or field-of-use restrictions. These are incompatible with most commercial projects.
- Check for "dual licensing" where the open-source license is restrictive but a commercial license is available for purchase.
- Check for license changes between versions. Some libraries have changed from permissive to restrictive licenses in recent major versions.

### License compliance checklist

1. Read the actual license text, not just the SPDX identifier
2. Verify all transitive dependencies have compatible licenses
3. Check for NOTICE files or additional terms beyond the license
4. Document the license in your project's dependency manifest
5. Set up automated license scanning in CI to catch new incompatible dependencies

## Size and bloat

### Bundle size impact

For frontend dependencies:
- Check the minified + gzipped size. Use tools like bundlephobia.com or `import-cost` editor plugins.
- Compare the size to the functionality you're actually using. If you need one utility function from a 50KB library, consider copying the function or finding a smaller alternative.

### Tree-shaking compatibility

- Libraries that export ESM modules and have proper `sideEffects: false` configuration can be tree-shaken — unused exports are removed from the bundle.
- Libraries that use CommonJS, have side effects in module initialization, or export a single large object cannot be tree-shaken.
- Check the library's `package.json` for `module`, `exports`, and `sideEffects` fields.

### Runtime impact

- Some libraries add significant runtime overhead (heavy initialization, frequent GC pressure, large memory footprint). Profile before adopting in performance-sensitive paths.
- Check if the library spawns threads, opens connections, or allocates large buffers on import.

## Alternative evaluation

### When to switch

Consider switching when:
- The current library is unmaintained and has known vulnerabilities with no fix
- The current library's license has changed to something incompatible
- A clearly superior alternative exists that the team has bandwidth to migrate to
- The current library is the source of recurring bugs or performance problems
- The current library doesn't support a required platform, runtime, or language version

### When NOT to switch

- The current library works fine and the alternative is just "newer" or "more popular"
- The migration cost exceeds the benefit over the remaining lifetime of the project
- The alternative is less mature — early adoption of shiny new libraries is its own risk

### Migration cost assessment

Before recommending a switch, estimate:
1. How many call sites use the current library? (Search the codebase.)
2. Are the APIs similar enough for mechanical replacement, or does each call site need manual attention?
3. Does the new library handle all the edge cases the current one handles? (Check test coverage.)
4. What's the testing cost? Every integration with the new library needs verification.
5. Can the migration be done incrementally with an adapter pattern, or is it all-or-nothing?

## Supply chain security

### Lockfile integrity

- Always commit lockfiles (`package-lock.json`, `Cargo.lock`, `go.sum`, `poetry.lock`). Without a lockfile, builds are non-reproducible and vulnerable to dependency confusion.
- Review lockfile changes in PRs. A lockfile diff that adds unexpected dependencies or changes versions you didn't intend is a signal to investigate.

### Provenance

- Verify that published packages match their source code. Some registries support provenance attestation (npm with Sigstore, Python with PEP 740).
- Prefer packages published from CI (with provenance) over those published from a developer's local machine.

### Typosquatting risks

- Before adopting a new package, verify the name is correct. `lodash` vs `1odash`, `requests` vs `request` — typosquatting is a real attack vector.
- Check the package's author, repository link, and download count. A package with the right name but 50 downloads and no linked repository is suspicious.
- Use tools that detect known typosquatting packages in your dependency tree.

## Evaluation summary format

When reporting on a dependency evaluation, structure the findings as:

```
## {Library name} v{version}

**Recommendation**: Adopt / Keep / Replace / Remove
**Risk level**: Low / Medium / High

### Health
- Maintainers: {count}, last activity: {date}
- Release cadence: {description}
- Open issues: {count}, avg response time: {duration}

### Security
- Known CVEs: {count}, unpatched: {count}
- Dependency tree depth: {count} direct, {count} transitive
- Last audit: {date}

### License
- License: {SPDX identifier}
- Compatible with project: Yes / No / Requires review
- Transitive license risks: {description}

### Size
- Bundle size: {size} min+gzip
- Tree-shakeable: Yes / No

### Alternatives considered
- {Alternative 1}: {one-line comparison}
- {Alternative 2}: {one-line comparison}

### Migration cost (if recommending replacement)
- Estimated effort: {description}
- Call sites to update: {count}
- Incremental migration possible: Yes / No
```
