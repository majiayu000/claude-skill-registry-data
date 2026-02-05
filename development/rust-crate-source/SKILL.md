---
name: rust-crate-source
description: Clone and explore Rust crate source code. Use when user wants to read source code for a Rust crate, explore a crate's implementation, understand how a crate works, or needs context about a Rust library.
---

# Rust Crate Source Explorer

This skill clones Rust crate repositories from crates.io to explore their source code. It fetches the repository URL from the crates.io API, clones to `/tmp/rust-crates/`, and checks out the appropriate version tag.

## When to Use

Use this skill when the user:
- Wants to explore or read source code for a Rust crate
- Wants to understand how a crate is implemented
- Needs context about a Rust library's internals
- Mentions "crate source", "explore crate", "how does X crate work"
- Asks to look at the implementation of a specific crate feature

## How to Use

### Step 1: Fetch Crate Info

Query the crates.io API to get the repository URL and latest version:

```bash
CRATE_NAME="serde"  # replace with the actual crate name
mkdir -p /tmp/rust-crates
CRATE_INFO=$(curl -sH "User-Agent: rust-crate-explorer" "https://crates.io/api/v1/crates/$CRATE_NAME")
REPO_URL=$(echo "$CRATE_INFO" | jq -r '.crate.repository')
VERSION=$(echo "$CRATE_INFO" | jq -r '.crate.max_version')
echo "Repository: $REPO_URL"
echo "Version: $VERSION"
```

### Step 2: Clone Repository

Clone if not already cached:

```bash
if [ ! -d "/tmp/rust-crates/$CRATE_NAME" ]; then
  git clone "$REPO_URL" "/tmp/rust-crates/$CRATE_NAME"
fi
```

### Step 3: Checkout Version Tag

Try common tag naming patterns to match the crate version:

```bash
cd "/tmp/rust-crates/$CRATE_NAME"
git fetch --tags
git checkout "v$VERSION" 2>/dev/null || \
git checkout "$VERSION" 2>/dev/null || \
git checkout "$CRATE_NAME-$VERSION" 2>/dev/null || \
echo "No matching tag found, using HEAD"
```

### Step 4: Explore the Source

Use Read, Glob, and Grep tools to explore the crate source at:
`/tmp/rust-crates/$CRATE_NAME/`

For workspace crates, the main source is typically in `src/` or a subdirectory matching the crate name.

## Example Workflow

User asks: "How does serde handle derive macros?"

```bash
# fetch and clone
CRATE_NAME="serde"
mkdir -p /tmp/rust-crates
CRATE_INFO=$(curl -sH "User-Agent: rust-crate-explorer" "https://crates.io/api/v1/crates/$CRATE_NAME")
REPO_URL=$(echo "$CRATE_INFO" | jq -r '.crate.repository')
VERSION=$(echo "$CRATE_INFO" | jq -r '.crate.max_version')

if [ ! -d "/tmp/rust-crates/$CRATE_NAME" ]; then
  git clone "$REPO_URL" "/tmp/rust-crates/$CRATE_NAME"
fi

cd "/tmp/rust-crates/$CRATE_NAME"
git fetch --tags
git checkout "v$VERSION" 2>/dev/null || git checkout "$VERSION" 2>/dev/null || echo "Using HEAD"
```

Then explore with Glob/Read tools to find derive macro implementations.

## Notes

- **Missing repository**: Some crates don't set the repository field; the API will return `null`
- **Version tags**: Not all crates tag releases; fall back to HEAD if no tag matches
- **Monorepos**: Large projects (tokio, serde) may have multiple crates in subdirectories
- **Dependencies**: Requires `jq` for JSON parsing
- **Temp storage**: Repos are stored in `/tmp/rust-crates/` and will be cleaned on reboot
