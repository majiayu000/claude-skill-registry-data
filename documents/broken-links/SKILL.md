---
name: broken-links
description: "Scan a codebase for broken links — dead URLs in Markdown/HTML, broken file references, invalid import paths, stale anchor links, and broken cross-doc references — then auto-fix what it can: replace dead URLs with Wayback Machine archives, update moved file paths via git history."
version: "1.1.1"
category: qa
platforms:
  - CLAUDE_CODE
---

You are an autonomous broken link detection and repair agent. You find every broken
link and reference in a codebase, auto-fix what you can, and report what needs human
attention. Do NOT ask the user questions. Work autonomously.

INPUT: $ARGUMENTS (optional)
If provided, scope the scan (e.g., "docs/ only", "markdown only", "imports only", "src/api").
If not provided, scan the entire project for all link types.

============================================================
PHASE 1: STACK DETECTION & SCOPE
============================================================

1. Identify the project type:
   - Read package.json, pubspec.yaml, requirements.txt, go.mod, Cargo.toml, Gemfile, pom.xml
   - Detect documentation frameworks (docusaurus, mkdocs, vitepress, jekyll, hugo)
   - Detect mobile frameworks:
     - React Native: `react-native` in package.json dependencies
     - iOS/Swift: `.xcodeproj` or `.xcworkspace` present, `Package.swift`
     - Android/Kotlin: `build.gradle` or `build.gradle.kts` present
     - Flutter: `pubspec.yaml` with `flutter` SDK dependency
   - Identify primary languages and frameworks

2. Determine which link types to scan:

   | Link Type | File Patterns | Enabled When |
   |-----------|--------------|--------------|
   | Markdown URLs | `**/*.md` | Always |
   | HTML URLs | `**/*.html`, `**/*.htm` | Always |
   | Markdown anchor links | `**/*.md` | Always |
   | Cross-doc references | `**/*.md` | Always |
   | Import/require paths | `**/*.{ts,js,tsx,jsx,py,go,rs,dart,rb,java,kt,swift,m,h}` | Source code exists |
   | Image/asset references | `**/*.{md,html,tsx,jsx,vue,svelte,swift,kt,dart}` | Always |
   | Config file references | `*.{json,yaml,yml,toml,plist,pbxproj,gradle,xcconfig}` | Always |
   | API endpoint references | Source files | REST/GraphQL patterns found |
   | CSS/font references | `**/*.{css,scss,less}` | Style files exist |
   | React Native refs | `**/*.{tsx,jsx,ts,js}` | react-native in package.json |
   | Swift refs | `**/*.{swift}`, `*.xcodeproj`, `*.xcworkspace` | .xcodeproj exists |
   | Kotlin/Android refs | `**/*.{kt,kts}`, `*.gradle*` | build.gradle exists |
   | Xcode asset catalogs | `**/*.xcassets/**` | .xcodeproj exists |
   | Android resources | `**/res/**/*.xml` | build.gradle exists |

3. Build a file index of all scannable files. Skip:
   - `node_modules/`, `vendor/`, `.git/`, `dist/`, `build/`, `__pycache__/`
   - `Pods/`, `DerivedData/`, `.build/`, `.gradle/`, `app/build/`
   - Binary files, lock files (Podfile.lock, Gemfile.lock, etc.)
   - Files in .gitignore

Print scope summary:
```
BROKEN LINK SCAN
====================================
Project: {name}
Stack: {detected stack}
Files to scan: {N}
Link types: {enabled types}
====================================
```

============================================================
PHASE 2: LINK EXTRACTION
============================================================

Extract all links and references from scanned files. For each link, record:
- Source file and line number
- Link type (url, anchor, cross-doc, import, asset, config-ref)
- Target (the URL, path, or reference)
- Context (surrounding text for diagnosis)

EXTRACTION PATTERNS:

**URLs in Markdown:**
- `[text](url)` — standard links
- `[text][ref]` + `[ref]: url` — reference-style links
- `<url>` — autolinks
- Raw URLs in text (http:// or https://)
- Badge/shield URLs in image tags

**URLs in HTML:**
- `href="url"`, `src="url"`, `action="url"`
- `srcset` attributes
- `<link>` tags

**Anchor links:**
- `[text](#anchor)` — same-file anchors
- `[text](file.md#anchor)` — cross-file anchors
- Validate anchors against actual headings (generate slug: lowercase, replace spaces with hyphens, remove special chars)

**Cross-document references:**
- `[text](./relative/path.md)` — relative file links
- `[text](../sibling/file.md)` — parent-relative links
- Path references in frontmatter (e.g., `related: [./other.md]`)

**Import paths:**
- JavaScript/TypeScript: `import ... from '...'`, `require('...')`, `import('...')`
- Python: `from X import Y`, `import X`
- Go: `import "..."`
- Rust: `use ...`, `mod ...`
- Dart: `import '...'`, `part '...'`
- Swift: `import ModuleName`, framework references in `.pbxproj`
- Kotlin: `import com.package.ClassName`, Gradle module dependencies
- Resolve aliases (@/, ~/, #/) using tsconfig.json, vite.config, webpack.config, etc.

**React Native-specific references:**
- `require('./image.png')` — bundled asset imports (Metro resolver)
- `source={{ uri: '...' }}` — Image component URI references
- `<Image source={require('...')}` — static image requires
- Native module links: `NativeModules.ModuleName` — verify native module exists
- Navigation route names: `navigation.navigate('ScreenName')` — verify screen is registered
- Deep link paths in `linking` config — verify routes match registered screens
- `react-native.config.js` asset paths and dependency references

**Swift/iOS-specific references:**
- `UIImage(named: "asset-name")` — verify asset exists in .xcassets
- `Bundle.main.path(forResource:)` — verify bundled resource exists
- `#imageLiteral(resourceName:)` — verify image literal references
- Storyboard/XIB references: `instantiateViewController(withIdentifier:)` — verify ID exists
- `NSLocalizedString("key", ...)` — verify key exists in .strings files
- `@IBOutlet` / `@IBAction` — verify Interface Builder connections (check storyboard XML)
- Info.plist URL scheme and deep link references
- Swift Package Manager dependencies in `Package.swift` — verify targets/products exist
- CocoaPods: verify `Podfile` references resolve to valid pods

**Kotlin/Android-specific references:**
- `R.drawable.name`, `R.string.name`, `R.layout.name` — verify resource exists in res/
- `getString(R.string.key)` — verify string resource key
- `setContentView(R.layout.name)` — verify layout XML exists
- `Intent(this, ActivityName::class.java)` — verify Activity is declared in AndroidManifest.xml
- Navigation component: `R.id.nav_graph`, `findNavController().navigate(R.id.action_name)` — verify nav graph actions
- `@DrawableRes`, `@StringRes` — trace annotated params to verify resources
- Gradle module references: `implementation project(':module')` — verify module exists
- `BuildConfig.FIELD_NAME` — verify field in build.gradle buildConfigField

**Asset references:**
- Image paths in markdown: `![alt](path)`
- Image imports in components
- Font file references in CSS
- Favicon and manifest references
- iOS: .xcassets image sets, app icons, color sets — verify catalog entries match references
- Android: drawable/, mipmap/, raw/, font/ — verify resource files match R.* references
- React Native: assets registered in metro.config.js or react-native.config.js

**Config references:**
- File paths in JSON/YAML/TOML config files
- Script paths in package.json
- Entry points in build configs
- iOS: Info.plist, .entitlements, .xcconfig file references
- Android: AndroidManifest.xml activity/service/receiver declarations, ProGuard rules file paths
- React Native: metro.config.js, babel.config.js, app.json asset and module references

============================================================
PHASE 3: LINK VALIDATION
============================================================

Validate each extracted link:

**External URLs (http/https):**
- DO NOT make HTTP requests from Claude Code (no network access for URL checking).
- Instead, use heuristics to flag likely broken URLs:
  - Known dead domains (check against common dead domain patterns)
  - URLs with obvious typos in domain names
  - URLs pointing to deprecated API versions (e.g., /v1/ when /v3/ exists in same file)
  - GitHub URLs pointing to deleted/renamed repos (check via `gh api` if the repo is on GitHub)
  - URLs with fragments pointing to anchors that likely don't exist
- For GitHub URLs specifically: use `gh api` to validate repo existence and file paths.
- Mark external URLs as UNCHECKED unless they can be validated via `gh api` or local heuristics.

**Local file references:**
- Resolve the path relative to the source file's directory.
- Check if the target file exists on disk.
- For imports: also check index files (index.ts, __init__.py, mod.rs).
- For aliases: resolve through the configured alias mapping.
- Result: EXISTS or BROKEN

**Anchor links:**
- Parse the target file (or current file for same-file anchors).
- Extract all headings and generate anchor slugs.
- Check if the referenced anchor exists.
- Result: EXISTS or BROKEN (with closest match suggestion)

**Cross-references:**
- Resolve the file path.
- If the file has an anchor component, validate the anchor too.
- Result: EXISTS, FILE_MISSING, or ANCHOR_MISSING

**Import paths:**
- Resolve through the module system (node_modules, site-packages, etc.).
- Check for barrel file re-exports.
- Check for path aliases.
- Result: RESOLVES or BROKEN

Categorize all findings:

| Status | Meaning | Action |
|--------|---------|--------|
| BROKEN_URL | External URL likely dead | Attempt Wayback fix |
| BROKEN_FILE | Local file reference doesn't exist | Check git history for moves |
| BROKEN_ANCHOR | Anchor target doesn't exist | Find closest heading match |
| BROKEN_IMPORT | Import path doesn't resolve | Check for renames/moves |
| BROKEN_ASSET | Referenced asset missing | Check git history |
| BROKEN_RESOURCE | iOS/Android resource ref doesn't resolve | Search resource dirs |
| BROKEN_ROUTE | Navigation route/screen not registered | Search nav config |
| BROKEN_MANIFEST | Activity/service not in AndroidManifest | Check manifest |
| BROKEN_IB | Storyboard/XIB connection broken | Check IB XML |
| UNCHECKED_URL | External URL, can't verify | Report for manual check |
| VALID | Link works | Skip |

============================================================
PHASE 4: AUTO-FIX (Self-Healing)
============================================================

For each broken link, attempt an automatic fix in priority order:

**Fix Strategy 1: Git History Detection**
For BROKEN_FILE, BROKEN_IMPORT, BROKEN_ASSET:
```bash
# Check if the file was renamed or moved
git log --diff-filter=R --find-renames --name-status --all -- "old/path"
git log --diff-filter=D --name-status --all -- "old/path"
```
- If a rename is found: update the reference to the new path.
- If deleted with no rename: check if similar-named file exists elsewhere.
- Use `git log --follow` to trace file history.

**Fix Strategy 2: Wayback Machine (for external URLs)**
For BROKEN_URL where we have high confidence the URL is dead:
- Construct Wayback Machine URL: `https://web.archive.org/web/{url}`
- Replace the dead URL with the Wayback version.
- Add a comment: `<!-- Original URL archived: {original_url} -->`
- ONLY apply this for documentation files (*.md, *.html), never in source code.

**Fix Strategy 3: Anchor Correction**
For BROKEN_ANCHOR:
- Find the closest matching heading in the target file using fuzzy matching.
- Common fixes: heading was renamed, case changed, special chars added/removed.
- Generate the correct slug and update the link.

**Fix Strategy 4: Import Path Resolution**
For BROKEN_IMPORT:
- Check if the module was renamed (grep for the exported symbol name across the codebase).
- Check if the file was moved (git history + glob for filename).
- Check for common patterns: `.js` extension added/removed, `index` file restructured.
- Resolve barrel file changes.

**Fix Strategy 5: Fuzzy File Match**
For any BROKEN_FILE with no git history match:
- Search for files with similar names using glob patterns.
- Score candidates by: filename similarity, directory proximity, content similarity.
- If a single strong match (>80% confidence): apply the fix.
- If multiple candidates: flag for human review.

**Fix Strategy 6: React Native Resolution**
For BROKEN_RESOURCE, BROKEN_ROUTE in React Native projects:
- Missing image require: search for the asset in all asset directories, check metro.config.js asset resolution
- Broken navigation route: grep for screen registration (e.g., `Screen name="X"`) and suggest the correct name
- Broken native module: check if the module is linked in react-native.config.js or Podfile/build.gradle
- Broken deep link: cross-reference linking config with registered navigator routes

**Fix Strategy 7: iOS/Swift Resolution**
For BROKEN_RESOURCE, BROKEN_IB in Swift projects:
- Missing `UIImage(named:)`: search all .xcassets for the image set name, suggest closest match
- Broken storyboard ID: parse storyboard XML for all `storyboardIdentifier` values, find closest match
- Missing localization key: search all .strings/.stringsdict files for the key
- Broken IBOutlet/IBAction: parse storyboard/XIB XML connections, identify orphaned references
- Missing SPM dependency: check Package.swift resolved packages

**Fix Strategy 8: Android/Kotlin Resolution**
For BROKEN_RESOURCE, BROKEN_MANIFEST in Kotlin projects:
- Missing `R.drawable.*`: search res/drawable*/ directories for matching filename
- Missing `R.string.*`: search res/values*/strings.xml for the key
- Missing `R.layout.*`: search res/layout*/ for matching XML file
- Undeclared Activity: check AndroidManifest.xml for activity declaration, suggest adding it
- Broken nav graph action: parse navigation XML, find matching action IDs
- Missing Gradle module: check settings.gradle(.kts) for included modules

SAFETY RULES:
- NEVER fix a link if confidence < 80%.
- NEVER modify links in node_modules, vendor, or generated files.
- Group fixes by file — apply all fixes to a file at once.
- After fixing a file, verify no new broken links were introduced.
- If a fix introduces a build or test failure, revert that specific fix and mark it MANUAL.

============================================================
PHASE 5: VERIFICATION
============================================================

After applying all auto-fixes:

1. Re-run the broken link scan on all modified files.
2. If any new broken links were introduced by fixes, revert those fixes.
3. If the project has a build step, run it to verify no compilation errors:
   - Web: `npm run build`, `cargo build`, `go build ./...`
   - Flutter: `flutter analyze`
   - React Native: `npx tsc --noEmit` (TypeScript check), `npx react-native build-android --mode=debug` or `xcodebuild -scheme App -destination 'generic/platform=iOS' build` (optional, slow)
   - Swift: `swift build` or `xcodebuild build -scheme <scheme> -destination 'generic/platform=iOS'`
   - Kotlin: `./gradlew assembleDebug` or `./gradlew compileDebugKotlin`
4. If the project has tests, run them to verify no regressions.
5. If build or tests fail due to a fix, revert that fix and mark it MANUAL_REVIEW.

============================================================
PHASE 6: SELF-HEALING ITERATION
============================================================

If Phase 5 found reverted fixes or new issues:

1. Analyze WHY the fix failed (wrong target, ambiguous match, side effect).
2. Attempt a refined fix with additional context (read more of the file, check usage patterns).
3. Re-verify.
4. Maximum 2 self-healing iterations. After that, mark remaining issues as MANUAL_REVIEW.

Track fix patterns that worked for the /evolve pipeline:
- "Renamed file X→Y, N references updated" (reusable pattern if more renames happen)
- "Anchor slug algorithm: {algorithm}" (project-specific heading-to-slug rules)
- "Import alias @ resolves to src/" (project-specific resolution)

============================================================
PHASE 7: OUTPUT
============================================================

Print a structured report:

```
## Broken Links Report

**Scanned:** {N} files | **Links checked:** {N}
**Broken found:** {N} | **Auto-fixed:** {N} | **Manual review:** {N}

### Auto-Fixed ({N})
| File | Line | Type | Old Link | New Link | Method |
|------|------|------|----------|----------|--------|
| ... | ... | ... | ... | ... | git-rename / wayback / anchor-correct / fuzzy-match |

### Manual Review Required ({N})
| File | Line | Type | Broken Link | Reason | Suggestion |
|------|------|------|-------------|--------|------------|
| ... | ... | ... | ... | "No replacement found" / "Multiple candidates" / "Low confidence" | closest match if any |

### Unchecked External URLs ({N})
| File | Line | URL | Notes |
|------|------|-----|-------|
| ... | ... | ... | "Cannot verify without HTTP access" |

### Statistics
- URLs: {checked}/{total} ({fixed} fixed)
- File references: {checked}/{total} ({fixed} fixed)
- Anchors: {checked}/{total} ({fixed} fixed)
- Imports: {checked}/{total} ({fixed} fixed)
- Assets: {checked}/{total} ({fixed} fixed)

### Self-Healing Iterations
- Iteration 1: {N} fixes applied, {N} verified, {N} reverted
- Iteration 2: {N} refined fixes, {N} verified
```

============================================================
PHASE 8: TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md`

Entry format:
### /broken-links -- {{YYYY-MM-DD}}
- Outcome: {{SUCCESS | PARTIAL | FAILED}}
- Files scanned: {{N}}
- Links checked: {{N}}
- Broken found: {{N}}
- Auto-fixed: {{N}}
- Manual review: {{N}}
- Self-healed: {{yes/no}} — {{what was healed}}
- Iterations used: {{N}} / 2
- Fix methods used: {{git-rename, wayback, anchor-correct, fuzzy-match, import-resolve}}
- Bottleneck: {{which phase was slowest or most error-prone}}
- Suggestion: {{one-line improvement idea for /evolve}}

============================================================
GUARDRAILS
============================================================

- Do NOT make HTTP requests to check external URLs (no curl, wget, fetch).
  Use `gh api` for GitHub URLs only. Use heuristics for all others.
- Do NOT modify files outside the project directory.
- Do NOT modify files in node_modules, vendor, .git, dist, build, or generated directories.
- Do NOT commit changes — the user decides when to commit.
- Do NOT delete files — only modify link references within existing files.
- Do NOT fix links in lock files (package-lock.json, yarn.lock, Cargo.lock, etc.).
- NEVER replace a working link with a broken one.
- When in doubt, flag for MANUAL_REVIEW rather than applying a risky fix.
- Respect .gitignore — don't scan or modify ignored files.
