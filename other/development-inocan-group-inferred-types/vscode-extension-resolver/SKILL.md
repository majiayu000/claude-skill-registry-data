---
name: VSCode Extension Resolver
description: Use this skill when VSCode extensions fail to build in nix configuration, when adding new VSCode extensions, or when debugging extension-related build errors. Handles systematic search across nixpkgs, vscode-marketplace, and open-vsx sources with incremental testing.
allowed-tools:
  - Read
  - Edit
  - Bash
  - Grep
  - Glob
---

# VSCode Extension Resolver

Expert agent for resolving VSCode extension build failures and finding correct extension sources in nix-vscode-extensions.

## Instructions

Your goal is to systematically identify working extension sources and fix build failures through incremental testing.

### Diagnosis Process

1. **Identify Failure**
   - Read error output from `home-manager build`
   - Identify which extension(s) failed
   - Note error type: hash mismatch, attribute not found, marketplace 500, etc.

2. **Check Current Configuration**
   - Read `modules/vscode/extensions.nix`
   - Verify function signature includes `nix-vscode-extensions` parameter
   - Identify which source block the failed extension is in

3. **Test Source Availability**
   Try sources in priority order:

   **First: nixpkgs curated** (most reliable)
   ```bash
   nix eval --impure --expr 'let pkgs = import <nixpkgs> {}; in builtins.attrNames pkgs.vscode-extensions' | grep -i "publisher"
   ```

   **Second: vscode-marketplace**
   Check if available in marketplace overlay

   **Third: open-vsx**
   Alternative registry for open source extensions

   **Last: custom build**
   Use `pkgs.vscode-utils.buildVscodeMarketplaceExtension` only when necessary

4. **Incremental Testing Strategy**
   - Create minimal test configuration with known-working extensions
   - Add ONE failed extension at a time
   - Run `home-manager build --flake . --impure` after each addition
   - Document which source works for each extension

5. **Cache Issues**
   If seeing stale errors about extensions that were removed:
   ```bash
   nix-collect-garbage -d
   ```
   Then retry build

### Fix Patterns

**Attribute not found:**
```nix
# Try different source
# FROM:
nix-vscode-extensions.extensions.${pkgs.system}.vscode-marketplace.publisher.extension
# TO:
pkgs.vscode-extensions.publisher.extension
# OR TO:
nix-vscode-extensions.extensions.${pkgs.system}.open-vsx.publisher.extension
```

**Marketplace 500 errors:**
- Marketplace URLs are unreliable
- Switch to nixpkgs curated or open-vsx
- Never use direct marketplace URLs

**Hash mismatch:**
- Extension version changed
- Get new hash:
```bash
nix-prefetch-url "https://marketplace.visualstudio.com/_apis/public/gallery/publishers/PUBLISHER/vsextensions/NAME/VERSION/vspackage"
```

**Custom build requirement:**
```nix
(pkgs.vscode-utils.buildVscodeMarketplaceExtension {
  mktplcRef = {
    name = "extension-name";
    publisher = "publisher-name";
    version = "1.0.0";
    sha256 = "sha256-hash-from-nix-prefetch-url";
  };
})
```

### Output Format

**During diagnosis:**
```
Analyzing failure...
- Failed extension: [publisher.extension]
- Error type: [attribute-not-found | hash-mismatch | etc]
- Current source: [nixpkgs | marketplace | open-vsx]

Testing alternative sources...
```

**After resolution:**
```
✓ Resolved: [extension-name]
Source: [which source worked]

Updated extensions.nix:
- Moved to [source-block]
- [any special notes]

Testing build: home-manager build --flake . --impure
```

**If multiple extensions:**
```
Resolved [N] extensions:
✓ extension1 → nixpkgs
✓ extension2 → marketplace
✗ extension3 → not available (suggest alternative)

Next: Test build with all changes
```

### Working Configuration Pattern

Ensure `modules/vscode/extensions.nix` follows this structure:

```nix
{ config, lib, pkgs, nix-vscode-extensions, ... }@inputs:

with lib;
let
  cfg = config.programs.vscode;
in {
  # ... options ...

  config = mkIf cfg.enable {
    programs.vscode.extensions = with pkgs.vscode-extensions; [
      # nixpkgs curated (most reliable)
      # ...
    ] ++ (with nix-vscode-extensions.extensions.${pkgs.system}.vscode-marketplace; [
      # marketplace extensions
      # ...
    ]);
  };
}
```

### Special Cases

**Extension not in any source:**
- Search for alternative extensions with same functionality
- Check if extension was renamed
- Note if only available via manual install

**Version-specific requirements:**
- Some extensions require specific VSCode version
- Note compatibility in comments

**Publisher renamed:**
- Extensions sometimes change publishers
- Try old and new publisher names

### Constraints

- **NEVER** apply changes without successful build first
- **ALWAYS** test incrementally (one extension at a time)
- **ALWAYS** verify function signature includes `nix-vscode-extensions`
- **ALWAYS** clean cache if seeing stale errors
- Keep user informed of testing progress

## Examples

**Simple attribute error:**
```
Failed: ms-python.python (attribute not found in marketplace)
→ Check nixpkgs curated
→ Found: pkgs.vscode-extensions.ms-python.python
→ Move to nixpkgs block
→ Test build ✓
```

**Hash mismatch:**
```
Failed: publisher.extension (hash mismatch)
→ Use nix-prefetch-url to get new hash
→ Update custom build block
→ Test build ✓
```

**Not available:**
```
Failed: obscure.extension (not found anywhere)
→ Search for alternatives
→ Suggest: similar-publisher.similar-extension
```
