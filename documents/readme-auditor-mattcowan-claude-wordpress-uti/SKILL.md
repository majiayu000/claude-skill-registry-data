---
name: readme-auditor
description: WordPress theme and plugin README auditor that verifies accuracy, removes exaggerated claims, and ensures maintainability. Use when reviewing or updating README files for WordPress projects (themes, child themes, plugins) to ensure all claims are verifiable against the actual codebase and that documentation remains accurate over time.
---

# WordPress README Auditor

A hawkish, accuracy-focused README auditor for WordPress themes and plugins that verifies every claim against the actual codebase and removes unmaintainable or exaggerated marketing language.

## Core Principles

1. **Accuracy Over Marketing** - Every claim must be verifiable
2. **Maintainability First** - Avoid metrics that become stale
3. **Evidence-Based** - Cross-reference with actual code
4. **No Exaggeration** - Remove superlatives unless objectively provable
5. **Future-Proof** - Flag claims that will break with updates

## Audit Categories

### 1. Version Requirements

**What to Check:**
- PHP version requirements against actual code usage
- WordPress version requirements against functions/hooks/features used
- Node.js/npm versions (if using build tools) - development only
- Build tool dependencies (if applicable): Vite, webpack, etc.
- CSS framework versions (if applicable): Tailwind, Bootstrap, etc.

**Common Issues:**
```markdown
❌ PHP: 7.4 or higher (but code uses str_contains() - requires PHP 8.0+)
✅ PHP: 8.0 or higher

❌ WordPress: 5.0+ (but code uses wp_body_open() - requires WP 5.2+)
✅ WordPress: 5.2 or higher

❌ Node.js: 18.x or higher (but package.json says >=18.0.0)
✅ Node.js: 18.0.0 or higher (development only)

❌ Tailwind CSS v4 (but package.json shows ^4.1.17)
✅ Tailwind CSS ^4.1.17
```

**How to Verify:**
1. Search codebase for PHP 8.0+ features (see PHP Version Detection section)
2. Search for WordPress functions/hooks and check their minimum WP version
3. Read `package.json` for Node/npm engines and dependencies (if present)
4. Verify actual installed versions match claims
5. Note that Node.js is only required for **development**, not production

### 2. Bundle Size Claims

**Red Flags:**
```markdown
❌ ~5KB CSS + ~0.5KB JS (gzipped) - Becomes stale, hard to maintain
❌ Minimal Bundle Size - Subjective, unmaintainable
❌ Lightning-fast - Unmeasurable superlative
❌ Blazing fast development - Marketing fluff
```

**Acceptable Alternatives:**
```markdown
✅ Optimized bundle sizes through minification and tree-shaking
✅ Production builds include only used CSS utilities (when using utility frameworks)
✅ Minified and concatenated assets for production
✅ Single bundled CSS and JS files reduce HTTP requests
```

**Why This Matters:**
- Bundle sizes change with every feature addition
- "Minimal" is subjective and becomes false over time
- Actual sizes depend on how much code users add
- No automated way to keep this accurate

### 3. Performance Claims

**Unverifiable Claims to Remove:**
```markdown
❌ ⚡ Lightning-fast development
❌ 🔥 Automatic Rebuilds on Save - Implies instant HMR which may not exist
❌ Zero Extra HTTP Requests - May not be true
❌ Blazing fast
❌ Instant builds
❌ Ultra-lightweight
```

**Acceptable Performance Claims (Verifiable):**
```markdown
✅ Assets bundled into single CSS and JS files
✅ Build system with watch mode (if applicable: Vite, webpack, etc.)
✅ Hash-based cache busting for efficient browser caching
✅ Tree-shaking removes unused code (if build tool supports it)
✅ CSS framework JIT/purging includes only used utilities (if applicable)
✅ WordPress enqueue system for proper asset loading
```

### 4. Feature Claims

**What to Verify:**
- "Zero Extra HTTP Requests" - Count actual CSS/JS enqueues in functions.php
- "Single file bundles" - Verify build output (if using build tools)
- "Automatic rebuilds" - Verify watch command exists (npm run watch/dev)
- "Block-ready structure" - Verify blocks directory exists or block registration
- "Gutenberg/Block Editor ready" - Verify blocks or add_theme_support('editor-*')
- "WooCommerce compatible" - Check for WooCommerce hooks/templates
- "Translation ready" - Verify text domain and load_theme_textdomain()
- "Cache-busted assets" - Verify hash-based filenames or version parameter

**How to Verify:**
1. Check `functions.php` for asset enqueuing (wp_enqueue_style/script)
2. Run build and verify output matches claims (if using build tools)
3. Check `package.json` for documented commands (if present)
4. Verify directory structure matches documentation
5. Search for WordPress-specific function calls (blocks, WooCommerce, etc.)

### 5. File Structure Documentation

**WordPress Theme/Plugin Required Files:**
```markdown
# WordPress Theme (Required)
style.css                  → Theme header with metadata
functions.php              → Theme functionality
screenshot.png             → Theme screenshot (880x660 recommended)
index.php                  → Main template file

# WordPress Child Theme (Required)
style.css                  → Must have "Template: parent-theme-slug"
functions.php              → Enqueue parent and child styles

# WordPress Plugin (Required)
main-plugin-file.php       → Plugin header with metadata

# Block Theme (Additional)
theme.json                 → Theme configuration
templates/                 → Block template files
parts/                     → Block template parts
```

**Build Tool Files (If Applicable):**
```markdown
# Modern Build Setup (Optional)
dist/                      → Build output directory
src/                       → Source files
package.json               → Node dependencies and scripts
vite.config.js             → Vite config (if using Vite)
webpack.config.js          → Webpack config (if using webpack)
tailwind.config.js         → Tailwind config (if using Tailwind)
postcss.config.js          → PostCSS config (if using PostCSS)
```

**Common Issues:**
- Missing required WordPress files (style.css, functions.php)
- Outdated paths from previous versions
- Example files that don't exist
- Missing directories in actual structure
- Renamed files not updated in docs
- Build tool configs documented but not present

**How to Verify:**
1. Verify all WordPress required files exist
2. Check style.css header has required fields
3. For each custom path mentioned, verify it exists
4. Check build output matches documented structure (if applicable)
5. Verify example file paths are accurate

### 6. Command Documentation

**What to Check (If Using Build Tools):**
```markdown
README says: `npm run watch` → package.json must have this script
README says: `npm run build` → package.json must have this script
README says: `npm run dev` → Check if this exists or is wrong
README says: `npm run preview` → package.json must have this script

Note: Classic WordPress themes without build tools won't have these commands
```

**Common Issues:**
```markdown
❌ npm run dev (if script doesn't exist)
❌ Commands documented but no package.json present
❌ Commands with wrong descriptions
❌ Missing required flags or arguments
❌ Claiming "no build step" but has package.json with build scripts
```

**How to Verify:**
1. Check if package.json exists (indicates build tool usage)
2. If present, read package.json scripts section
3. Compare every documented command
4. Verify descriptions match actual behavior
5. If no build tools, ensure README doesn't document build commands
6. Test that commands work as described

### 7. Code Examples

**What to Check:**
- Syntax matches actual project patterns
- Function names exist in codebase
- WordPress hooks are used correctly
- Examples follow WordPress Coding Standards
- CSS framework classes are valid (if applicable)
- Text domain matches actual theme/plugin text domain

**Common Issues:**
```php
❌ // Example uses old function name
function my_old_function() {}

✅ // Example matches actual implementation
function generatepress_child_enqueue_assets() {}

❌ // Missing text domain or wrong domain
__('Hello', 'wrong-domain')

✅ // Correct text domain
__('Hello', 'actual-theme-slug')

❌ // Old WordPress function
posts_nav_link()

✅ // Modern WordPress function
the_posts_pagination()
```

**How to Verify:**
1. Search codebase for functions used in examples
2. Verify WordPress hooks match actual usage
3. Check that examples match WordPress Coding Standards
4. Verify text domain matches style.css or plugin header
5. Test that examples actually work

### 8. Configuration Claims

**What to Check:**
```markdown
README claims: "CSS framework JIT mode enabled"
→ Verify in framework config (tailwind.config.js, etc.)

README claims: "ES6+ JavaScript"
→ Verify build target in vite.config.js or webpack.config.js

README claims: "CSS minification"
→ Check if this is actually configured in build tool

README claims: "Block theme with theme.json"
→ Verify theme.json exists and is valid

README claims: "Custom block patterns"
→ Verify patterns directory or registration code exists
```

**How to Verify:**
1. Read configuration files mentioned (both WordPress and build tool configs)
2. Verify claims match actual config
3. Check for outdated configuration info
4. Verify theme.json schema version if present
5. Ensure config examples are current

### 9. Dependency Documentation

**What to Check:**
```markdown
README lists: @tailwindcss/postcss: ^4.1.17
→ package.json must have matching or compatible version

README claims: "Tailwind CSS v4" (or Bootstrap, Foundation, etc.)
→ package.json should show matching version

README claims: "Built with Vite" (or webpack, Gulp, etc.)
→ package.json should show build tool as dependency

README claims: "WordPress 6.0+" required
→ Verify actual WordPress functions used require this version
```

**How to Verify:**
1. Compare README dependency list with package.json (if applicable)
2. Verify version numbers are accurate or use ranges (4.x, 6.0+)
3. Check for dependencies mentioned but not installed
4. Flag dependencies installed but not documented
5. Verify WordPress version requirements against actual functions used
6. Note whether dependencies are development-only or production

### 10. Workflow Claims

**What to Verify:**
```markdown
⚠️ "Unlike a typical [build-tool] project, there is no HMR"
→ Verify this is accurate (check build tool config server settings)

✅ "Refresh browser to see changes"
→ Acceptable - accurate description of manual workflow when HMR is disabled
→ Verify this matches actual watch mode behavior

✅ "Build tool watches files and rebuilds on change"
→ Acceptable - describes actual watch mode behavior, not instant HMR
→ Confirm watch script exists and works as described

✅ "Classic theme - no build step required"
→ Acceptable - verify no package.json and no built assets

⚠️ "Instant preview with HMR"
→ Verify HMR is actually configured and works with WordPress
```

### 11. WordPress-Specific Claims

**Common WordPress Claims to Verify:**

```markdown
❌ "SEO Optimized"
→ Too vague - remove or specify what SEO features exist

❌ "Accessibility Ready"
→ Cannot claim without official WordPress Accessibility review
→ Use "Accessibility considerations" or "Follows WCAG guidelines"

❌ "Gutenberg Ready" / "Block Editor Ready"
→ Verify actual blocks exist or add_theme_support('editor-*') called

✅ "Custom block patterns included"
→ Verify patterns directory or register_block_pattern() calls exist

✅ "Translation ready with .pot file included"
→ Verify load_theme_textdomain() and .pot file exists

✅ "WooCommerce template overrides"
→ Verify woocommerce/ template directory exists

❌ "Multisite compatible"
→ Hard to verify - remove unless specifically tested

✅ "Uses WordPress enqueue system"
→ Verify wp_enqueue_style() and wp_enqueue_script() usage

❌ "100% GPL compatible"
→ All themes/plugins must be GPL - remove redundant claim
→ Exception: Can mention if using GPL-compatible third-party resources
```

**WordPress Version Detection:**
```markdown
# Check minimum WordPress version based on functions used:
wp_body_open()                    → WordPress 5.2+
register_block_type()             → WordPress 5.0+ (Gutenberg)
theme.json                        → WordPress 5.8+ (Full Site Editing)
block_template_part()             → WordPress 5.9+
wp_is_block_theme()               → WordPress 5.9+
wp_enqueue_block_style()          → WordPress 5.9+
```

**How to Verify:**
1. Search for WordPress-specific function calls
2. Check WordPress.org theme requirements against claims
3. Verify blocks directory or block registration code
4. Check for translation files and text domain usage
5. Look for WooCommerce-specific code or templates
6. Search for multisite-specific functions (if claimed)
7. Verify theme support declarations (add_theme_support)

### 12. WordPress Coding Standards

**Security & Sanitization:**
```markdown
✅ Code uses proper escaping functions
→ Verify esc_html(), esc_attr(), esc_url(), wp_kses() usage

✅ Code uses proper sanitization
→ Verify sanitize_text_field(), sanitize_email(), etc. usage

✅ Nonces used for form submissions
→ Verify wp_nonce_field() and wp_verify_nonce() usage

❌ "Secure and sanitized"
→ Too vague - either remove or be specific about security measures
```

**Translation & Internationalization:**
```markdown
✅ "Translation ready"
→ Verify all strings use __(), _e(), _n(), etc.
→ Verify text domain matches theme/plugin slug
→ Check for load_theme_textdomain() or load_plugin_textdomain()
→ Verify .pot file exists (if claiming translation ready)

❌ Translation functions without text domain
→ Flag missing or incorrect text domains
```

**Data Handling:**
```markdown
✅ Uses WordPress database API
→ Verify $wpdb->prepare() for custom queries
→ No raw SQL without preparation

✅ Uses WordPress options API
→ get_option(), update_option(), add_option()

✅ Uses WordPress transients
→ get_transient(), set_transient() for cached data
```

**How to Verify:**
1. Search for output that may need escaping
2. Verify form inputs are sanitized
3. Check translation function usage and text domains
4. Look for direct database queries (should use $wpdb->prepare)
5. Verify options and transients usage
6. Check for deprecated WordPress functions

## Audit Process

### Step 1: Version Requirements Audit
1. Search PHP files for PHP 8.0+ features (see PHP Version Detection)
2. Search for WordPress functions and determine minimum WP version
3. Read package.json engines field (if present - development only)
4. Read package.json dependencies (if present)
5. Verify style.css or plugin header for WordPress version requirement
6. Compare with README requirements section
7. Flag any mismatches
8. **Important:** Note that Node.js/npm are only required for **development**, not for running WordPress

### Step 2: Remove Unmaintainable Metrics
1. Find all specific size claims (KB, MB)
2. Find all performance superlatives (lightning, blazing, ultra, instant)
3. Find all "zero", "minimal", "maximum" claims
4. Replace with verifiable, maintainable descriptions

### Step 3: Verify File Structure
1. Verify WordPress required files exist (style.css, functions.php, etc.)
2. Check style.css or plugin header has required metadata
3. List all paths mentioned in README
4. Check each path exists in codebase
5. Verify build output matches documentation (if using build tools)
6. Flag missing or renamed files

### Step 4: Verify Commands (If Using Build Tools)
1. Check if package.json exists
2. Extract all `npm run X` commands from README
3. Read package.json scripts section
4. Compare documented vs actual commands
5. Test command descriptions match behavior
6. If no build tools, ensure README doesn't document build commands

### Step 5: Verify Code Examples
1. Extract all code blocks from README
2. Check function names exist in codebase
3. Verify WordPress hooks are used correctly
4. Check text domains match theme/plugin slug
5. Verify syntax matches WordPress Coding Standards
6. Test that examples work

### Step 6: Cross-Reference Configuration
1. List all configuration claims
2. Read WordPress config files (style.css, theme.json, plugin header)
3. Read build tool config files (if present)
4. Verify claims match reality
5. Update outdated information

### Step 7: WordPress-Specific Verification
1. Verify WordPress version requirements against actual functions used
2. Check WordPress-specific claims (Gutenberg, WooCommerce, etc.)
3. Verify translation readiness if claimed
4. Check for proper escaping and sanitization if security is mentioned
5. Verify theme support declarations match claims

## Red Flag Patterns

### Marketing Language to Remove
- "⚡ Lightning-fast" → "Fast development builds"
- "🔥 Blazing" → Remove emoji and superlative
- "Ultra-lightweight" → "Optimized"
- "Minimal bundle size" → "Optimized bundle sizes"
- "Zero overhead" → Specific technical description
- "Instant compilation" → "Optimized compilation"
- "Revolutionary" → Remove entirely
- "Best-in-class" → Remove entirely

### Specific Metrics to Remove
- "~5KB CSS + ~0.5KB JS (gzipped)" → "Minified and tree-shaken bundles"
- "99% smaller than X" → Remove comparison
- "Loads in under 100ms" → Remove specific timing
- "100x faster" → Remove multiplier claims

### Unverifiable Claims to Challenge
- "Industry-leading" → Remove
- "Production-ready" → Subjective, remove or clarify
- "Enterprise-grade" → Remove unless you can define it
- "Cutting-edge" → Remove
- "Future-proof" → Remove (nothing is future-proof)

## Output Format

When auditing, provide:

```markdown
## README Audit Report

### ❌ CRITICAL ISSUES (Fix Immediately)

**Line X: PHP Version Requirement**
- **Current:** PHP: 7.4 or higher
- **Issue:** Code uses `str_contains()` which requires PHP 8.0+
- **Found in:** functions.php:182, functions.php:206
- **Fix:** Change to "PHP: 8.0 or higher"

### ⚠️ MAINTAINABILITY ISSUES (Remove/Update)

**Line X: Bundle Size Claim**
- **Current:** 🎯 **Minimal Bundle Size** - ~5KB CSS + ~0.5KB JS (gzipped)
- **Issue:** Specific sizes become stale with each update
- **Fix:** Replace with "Optimized bundle sizes through minification and tree-shaking"

### ℹ️ ACCURACY ISSUES (Verify or Update)

**Line X: Command Documentation**
- **Current:** npm run dev
- **Issue:** package.json has no "dev" script, should be "watch"
- **Fix:** Change to `npm run watch`

### ✅ VERIFIED CLAIMS (Accurate)
- ✅ Build system integration (Vite/webpack/etc.)
- ✅ CSS framework support (Tailwind/Bootstrap/etc.)
- ✅ WordPress enqueue system usage
- ✅ Hash-based cache busting
- ✅ Translation ready with proper text domain
```

## Usage Guidelines

**When to Use This Skill:**
1. Before publishing WordPress theme/plugin to WordPress.org
2. Before releasing README updates
3. After major WordPress or dependency updates
4. When adding new features to README
5. During regular documentation audits
6. Before sharing repository publicly

**How to Use:**
1. Read entire README.md
2. Read WordPress files: style.css (theme header), functions.php, theme.json (if block theme)
3. Read build tool files if present: package.json, build configs
4. Search codebase for PHP version-specific features
5. Search for WordPress function usage to determine minimum WP version
6. Verify every factual claim against actual code
7. Flag all marketing hyperbole
8. Check WordPress-specific claims (Gutenberg, WooCommerce, etc.)
9. Output detailed audit report
10. Recommend specific fixes

**Tone:**
- Hawkish about accuracy
- Ruthless with marketing fluff
- Prioritize maintainability
- Evidence-based recommendations
- Specific line-by-line feedback

## Example Audit Patterns

### Pattern: Version Mismatch
```markdown
❌ **README Line 22:** PHP: 7.4 or higher
📁 **Found in code:** functions.php:182, functions.php:206
💻 **Code uses:** str_contains() - requires PHP 8.0+
✅ **Fix:** Change to "PHP: 8.0 or higher"
```

### Pattern: Stale Metrics
```markdown
⚠️ **README Line 12:** Minimal Bundle Size - ~5KB CSS + ~0.5KB JS (gzipped)
🔍 **Issue:** Specific metrics become outdated, difficult to maintain
✅ **Fix:** Remove specific sizes, use: "Optimized production bundles with minification and tree-shaking"
```

### Pattern: Unverifiable Claims
```markdown
⚠️ **README Line 7:** ⚡ **Vite Build System** - Lightning-fast development
🔍 **Issue:** "Lightning-fast" is unmeasurable marketing language
✅ **Fix:** "Development builds with Vite"
```

### Pattern: Missing Files
```markdown
❌ **README Line 87:** example-block.css
🔍 **Issue:** File path shown as example but doesn't exist
✅ **Fix:** Add note: "(example - create your own)" or remove if not needed
```

### Pattern: WordPress-Specific Claims
```markdown
❌ **README Line 15:** SEO Optimized
🔍 **Issue:** Too vague, no specific SEO features mentioned
✅ **Fix:** Remove or specify: "Semantic HTML structure and schema.org markup"

⚠️ **README Line 28:** Gutenberg Ready
🔍 **Issue:** No blocks or block support found in codebase
📁 **Search results:** No register_block_type() calls, no add_theme_support('editor-*')
✅ **Fix:** Either add block support or remove claim

✅ **README Line 42:** Translation ready with .pot file
📁 **Verified:** load_theme_textdomain() in functions.php:12, languages/theme-slug.pot exists
✅ **Status:** Accurate claim
```

## PHP Version Detection

### PHP 8.0+ Features to Search For:
```php
// String functions (PHP 8.0+)
str_contains()
str_starts_with()
str_ends_with()

// Nullsafe operator (PHP 8.0+)
$obj?->method()

// Named arguments (PHP 8.0+)
function_name(param: $value)

// Match expression (PHP 8.0+)
match ($var) { }

// Constructor property promotion (PHP 8.0+)
public function __construct(public string $prop)

// Union types (PHP 8.0+)
function foo(int|string $param)

// Attributes (PHP 8.0+)
#[Attribute]

// throw expression (PHP 8.0+)
$value = $condition ?? throw new Exception();
```

### PHP 8.1+ Features to Search For:
```php
// Enums (PHP 8.1+)
enum Status { }

// Readonly properties (PHP 8.1+)
public readonly string $prop;

// First-class callable syntax (PHP 8.1+)
$fn = strlen(...)

// Array unpacking with string keys (PHP 8.1+)
$array = [...$array1, ...$array2];

// new in initializers (PHP 8.1+)
public function __construct(private Service $service = new Service())
```

## Maintainability Guidelines

**Remove These Pattern Types:**

1. **Specific Measurements**
   - File sizes, load times, performance metrics
   - In user-facing documentation, replace specific version numbers with version ranges for maintainability (e.g., change "4.1.17" to "4.x"). For dependency specifications, use caret notation or specific versions as recommended above.
   - Exact counts ("supports 50+ features")

2. **Subjective Comparisons**
   - "Better than X"
   - "Faster than Y"
   - "More reliable than Z"

3. **Time-Based Claims**
   - "Latest technology"
   - "Modern approach" (becomes dated)
   - "Cutting-edge"

4. **Absolute Statements**
   - "Zero bugs"
   - "Perfect compatibility"
   - "Never breaks"
   - "Always works"

**Keep These Pattern Types:**

1. **Objective Features**
   - "Build system: Vite" (or webpack, etc.)
   - "CSS Framework: Tailwind CSS 4.x" (or Bootstrap, etc.)
   - "Hash-based cache busting"
   - "WordPress 6.0+ required"

2. **Verifiable Behaviors**
   - "Bundles CSS and JS into single files"
   - "Watches for file changes" (if using build tools)
   - "Minifies production output"
   - "Uses WordPress enqueue system"
   - "Loads text domain for translations"

3. **Architecture Descriptions**
   - "WordPress child theme structure"
   - "Block theme with theme.json"
   - "Custom block patterns included"
   - "Uses build manifest for asset loading" (if applicable)

## Final Checklist

Before completing audit, verify:

- [ ] WordPress required files exist (style.css, functions.php, etc.)
- [ ] PHP version requirements checked against code features
- [ ] WordPress version requirements checked against functions used
- [ ] All specific metrics removed or verified
- [ ] All superlatives challenged or removed
- [ ] All file paths verified to exist
- [ ] All commands verified in package.json (if using build tools)
- [ ] All code examples tested for accuracy
- [ ] Text domains match theme/plugin slug
- [ ] WordPress-specific claims verified (Gutenberg, WooCommerce, etc.)
- [ ] Translation readiness verified if claimed
- [ ] All configuration claims verified
- [ ] All dependencies match package.json (if present)
- [ ] Node.js marked as development-only requirement
- [ ] All marketing fluff removed
- [ ] README is maintainable going forward

## Success Criteria

A good WordPress README audit should:

1. ✅ Verify WordPress, PHP, and dependency version requirements
2. ✅ Find and fix all version mismatches
3. ✅ Verify WordPress-specific claims (blocks, WooCommerce, etc.)
4. ✅ Remove all unmaintainable metrics
5. ✅ Replace marketing language with technical accuracy
6. ✅ Verify all paths and commands
7. ✅ Check WordPress coding standards compliance
8. ✅ Ensure long-term maintainability
9. ✅ Provide specific, actionable fixes
10. ✅ Prioritize accuracy over appeal
