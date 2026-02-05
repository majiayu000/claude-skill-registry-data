---
name: debian-packaging
description: Expert Debian package builder specializing in git-buildpackage, debhelper, and Debian Policy compliance. Use for .deb packaging, debian/ directory work, dpkg operations, and package maintenance. Triggers on "Debian", ".deb", "dpkg", "debhelper", "gbp", "pbuilder", "lintian", "dch".
---

Modern Debian packaging expert focused on git-buildpackage workflows, clean builds (sbuild/pbuilder), quality assurance (lintian/piuparts), and patch management (quilt/gbp-pq). Follows current best practices with debhelper 13+ and Debian Policy compliance.

## Core Principles

1. **Version control first** - Always use git-buildpackage for reproducible builds
2. **Policy compliance** - Follow [Debian Policy](https://www.debian.org/doc/debian-policy/) strictly
3. **Clean builds** - Test in isolated chroots (sbuild/pbuilder), never build as root
4. **Quality gates** - Run lintian (no errors), piuparts, and autopkgtest before upload
5. **Patch documentation** - All patches need DEP-3 headers explaining what/why
6. **Pristine upstream** - Keep upstream sources unmodified, use debian/patches/ for changes

## Git-Buildpackage Configuration

**~/.gbp.conf** (essential setup):
```ini
[DEFAULT]
pristine-tar = True
pristine-tar-commit = True
upstream-branch = upstream/latest
debian-branch = debian/latest
pbuilder = True  # or builder = sbuild
sign-tags = True  # optional
keyid = YOUR_GPG_KEY_ID  # optional
```

**debian/gbp.conf** (project-specific):
```ini
[DEFAULT]
upstream-tag = v%(version)s  # adjust to match upstream's tag pattern
```

## Importing Upstream Sources

**From tarballs:**
```bash
# Initialize repo
git init --initial-branch=debian/latest mypackage.git
cd mypackage.git

# Import upstream tarball
gbp import-orig /path/to/mypackage-1.0.tar.gz

# Create debian/watch for auto-updates
# See: https://manpages.debian.org/man/uscan
```

**From git repository:**
```bash
# Clone upstream
git clone https://upstream.example.com/mypackage.git
cd mypackage.git

# Rename to debian branch
git branch -m debian/latest

# Configure upstream tag pattern in debian/gbp.conf
```

**Update to new version:**
```bash
# With debian/watch configured:
gbp import-orig --uscan

# Or specify tarball directly:
gbp import-orig ../mypackage-1.1.tar.gz
```

## Branch Structure (DEP-14)

- **debian/latest** - Main packaging branch
- **upstream/latest** - Upstream source history
- **pristine-tar** - Binary delta for exact tarball reproduction
- **patch-queue/debian/latest** - Temporary branch for patch development (gbp pq)

## Essential debian/ Files

**debian/control** - Package metadata
- Source section: name, maintainer, build dependencies, standards version
- Binary section(s): name, dependencies, description, architecture
- Use `${shlibs:Depends}` and `${misc:Depends}` for automatic dependencies

**debian/rules** - Build instructions (executable)
```makefile
#!/usr/bin/make -f
export DEB_BUILD_MAINT_OPTIONS = hardening=+all

%:
	dh $@

# Override only when needed:
#override_dh_auto_install:
#	dh_auto_install -- --with-custom-option
```

**debian/changelog** - Version history (RFC 5322 format)
- Managed with `dch` command
- Version format: `epoch:upstream-debian` (e.g., `1.2.3-1`)
- Generate from git: `gbp dch --auto`

**debian/copyright** - License information (DEP-5 machine-readable format)
- Use copyright review tools: `licensecheck -r .`

**debian/source/format** - Source package format
- `3.0 (quilt)` for non-native packages (has upstream + Debian changes)
- `3.0 (native)` for Debian-only packages (rare)

**debian/watch** - Upstream version tracking
- For auto-detection with `gbp import-orig --uscan`
- Examples: https://manpages.debian.org/man/uscan#WATCH_FILE_EXAMPLES

## Common debian/ Files

- **debian/compat** or **debhelper-compat** - Debhelper compatibility level (use 13+)
- **debian/install** - Files to install when dh_auto_install is insufficient
- **debian/patches/** - Quilt patch series with DEP-3 headers
- **debian/tests/** - autopkgtest integration tests

## Clean Build Setup

**sbuild** (recommended, used by official buildds):
```bash
sudo apt install sbuild
sudo sbuild-adduser $LOGNAME
# Logout and re-login

# Create chroot
sudo sbuild-createchroot --include=eatmydata,ccache,gnupg unstable \
    /srv/chroot/unstable-amd64-sbuild http://deb.debian.org/debian

# Build package
sbuild -A -d unstable
```

**pbuilder** (alternative):
```bash
sudo apt install pbuilder
sudo pbuilder create --distribution unstable
gbp buildpackage  # uses pbuilder if pbuilder=True in ~/.gbp.conf
```

## Git-Buildpackage Workflow

**Daily development:**
```bash
# Edit sources and debian/ files
git add .
git commit -m "Description of changes"

# Update changelog
dch -i  # or: gbp dch --auto

# Build and test
gbp buildpackage --git-pbuilder
```

**Managing patches (quilt):**
```bash
# Apply patches
quilt push -a

# Create new patch
quilt new fix-something.patch
quilt edit file.c
quilt refresh
quilt header -e  # Add DEP-3 header

# Unapply before committing
quilt pop -a
git add debian/patches/
git commit
```

**Managing patches (gbp pq):**
```bash
# Import patches to patch-queue branch
gbp pq import

# Make changes and commit
git commit -a -m "Fix something"

# Export back to debian/patches/
gbp pq export

# Commit exported patches
git add debian/patches/
git commit
```

## DEP-3 Patch Headers

Required in all patches:
```
Description: One-line summary
 Longer explanation of what this patch does and why.
Author: Your Name <you@example.com>
Origin: vendor|upstream|other
Bug: https://bugs.upstream.example.com/123
Bug-Debian: https://bugs.debian.org/123456
Forwarded: yes|no|not-needed|https://url
Last-Update: 2025-01-15
---
```

## Quality Assurance

**lintian** - Policy compliance checker:
```bash
# Comprehensive check
lintian -EvIL +pedantic ../mypackage_*.changes

# Fix all errors (E:), investigate warnings (W:)
```

**piuparts** - Install/remove testing:
```bash
sudo piuparts --log-level info \
    --basetgz /var/cache/pbuilder/base.tgz \
    ../mypackage_*.deb
```

**autopkgtest** - Integration testing:
```bash
# Define tests in debian/tests/control
# Run with:
autopkgtest ../mypackage_*.changes -- unshare
```

**wrap-and-sort** - Consistent formatting:
```bash
wrap-and-sort -ast  # Sort and wrap debian/control and other files
```

## Common Workflows

### New package from scratch
```bash
# 1. Get upstream source and create git repo
git init --initial-branch=debian/latest mypackage.git
cd mypackage.git
gbp import-orig /path/to/mypackage-1.0.tar.gz

# 2. Initialize debian/ directory
git archive HEAD --prefix=mypackage-1.0/ -o ../mypackage_1.0.orig.tar.gz
tar xzf ../mypackage_1.0.orig.tar.gz && cd mypackage-1.0
debmake  # or dh_make
mv debian/* ../debian/
cd .. && rm -rf mypackage-1.0

# 3. Edit debian/ files (control, rules, copyright, changelog, watch)

# 4. Build and test
gbp buildpackage
lintian -EvIL +pedantic ../mypackage_*.changes
```

### Update to new upstream version
```bash
# With debian/watch:
gbp import-orig --uscan

# Or with tarball:
gbp import-orig ../mypackage-1.1.tar.gz

# Update changelog
dch -v 1.1-1 "New upstream release"

# Refresh patches if needed
gbp pq rebase

# Build and test
gbp buildpackage
```

### Fix bug with patch
```bash
# Option 1: quilt
quilt new fix-bug-123.patch
quilt edit src/file.c
quilt refresh
quilt header -e  # Add DEP-3 header
quilt pop -a

# Option 2: gbp pq
gbp pq import
# Make changes and commit with good message
gbp pq export

# Update changelog
dch -i
# Add entry: "* Fix bug #123 (Closes: #123)"

# Build and test
gbp buildpackage
```

### Prepare for upload
```bash
# 1. Ensure changelog is correct
dch -r  # Change UNRELEASED to unstable/experimental

# 2. Commit changelog
git commit debian/changelog -m "Release X.Y-Z"

# 3. Build with tagging
gbp buildpackage --git-tag

# 4. Push to Salsa
git push --all --follow-tags
```

## Version Numbering

**Format:** `[epoch:]upstream-debian`

Examples:
- `1.2.3-1` - First Debian package of upstream 1.2.3
- `1.2.3-2` - Second Debian revision (bug fixes, no upstream changes)
- `1:1.0-1` - With epoch (when upstream versioning changed)
- `1.2.3-1~bpo12+1` - Backport to bookworm
- `1.2.3-1+deb12u1` - Security update for stable

**Native packages:**
- Version: `1.2.3` (no Debian revision)
- Only for Debian-specific tools

## Build Commands

```bash
# Standard build
gbp buildpackage

# Build for specific distribution/architecture
gbp buildpackage --git-dist=bookworm --git-arch=arm64

# Build without tagging
gbp buildpackage --git-ignore-new

# Generate source-only upload
gbp buildpackage --git-builder='dpkg-buildpackage -S'
```

## Anti-patterns

**Never do:**
- Build as root or outside clean chroot
- Skip lintian checks or ignore errors
- Edit upstream source without documenting in debian/patches/
- Commit with UNRELEASED in changelog before tagging
- Use debhelper compat < 13
- Mix unrelated changes in single changelog entry
- Hardcode paths or architecture names in debian/rules
- Modify files without quilt/gbp-pq tracking
- Push to Salsa with failing tests
- Upload without testing in clean environment

**Always do:**
- Run lintian, piuparts before every upload
- Document patches with complete DEP-3 headers
- Use `${shlibs:Depends}` and `${misc:Depends}` in debian/control
- Test package install/remove in clean chroot
- Follow DEP-14 branch naming (upstream/latest, debian/latest)
- Use pristine-tar for reproducibility
- Keep git history clean and commits atomic

## Troubleshooting

**lintian errors:**
- Read error description carefully
- Check Debian Policy Manual section referenced
- Look at well-maintained similar packages for examples

**Build failures:**
- Check build log in ../build-area/ or /var/cache/pbuilder/result/
- Missing build-deps: add to debian/control Build-Depends
- Test with `DH_VERBOSE=1` for detailed output

**Patch conflicts:**
```bash
gbp pq import  # Will show conflicts
# Resolve conflicts in patch-queue branch
gbp pq rebase
gbp pq export
```

**Clean source tree:**
```bash
debian/rules clean  # or: debclean
quilt pop -a  # Unapply all patches
git clean -dfx  # Remove untracked files (careful!)
```

## Resources

- **Debian Policy:** https://www.debian.org/doc/debian-policy/
- **Git-buildpackage manual:** https://honk.sigxcpu.org/projects/git-buildpackage/manual-html/
- **DEP-14 (branch naming):** https://dep-team.pages.debian.net/deps/dep14/
- **DEP-3 (patch headers):** https://dep-team.pages.debian.net/deps/dep3/
- **Debian Developer's Reference:** https://www.debian.org/doc/manuals/developers-reference/
- **Salsa (Debian GitLab):** https://salsa.debian.org/

## Environment Setup

**~/.bashrc additions:**
```bash
export DEBEMAIL="your@email.domain"
export DEBFULLNAME="Your Name"
alias lintian='lintian -iIEcv --pedantic --color auto'
```

Remember: Debian packaging values **correctness over convenience**. Every shortcut creates technical debt that blocks package acceptance. When in doubt, check Policy and study well-maintained packages.