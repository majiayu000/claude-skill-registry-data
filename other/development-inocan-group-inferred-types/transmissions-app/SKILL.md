---
name: transmissions-app
description: Guide for creating new Transmissions applications with decision support for core vs remote development
---

# Transmissions App Creation Skill

This skill guides you through creating a new Transmissions application, helping you choose between core and remote development based on your needs.

## Quick Start Decision Tree

**Choose your development path:**

### Core Development (Recommended for beginners)
- ✅ Simple setup - work directly in framework
- ✅ Easy debugging and testing
- ✅ Good for learning or framework contributions
- ❌ Couples your app with framework repo

**Use when:** Learning, prototyping, or contributing to core

### Remote Development (Recommended for production)
- ✅ Clean separation from framework
- ✅ Independent versioning
- ✅ Can be distributed separately
- ⚠️ Requires module loading setup (has known issues to watch for)

**Use when:** Building production apps, maintaining separate repos

## Workflow

### 1. Gather Information

Ask the user:
- **App name**: What should the app be called? (e.g., `my-data-processor`)
- **Development location**: Core (`src/apps/`) or Remote (`~/hyperdata/trans-apps/apps/`)?
- **App purpose**: Brief description to customize documentation

### 2. Create App Structure

Execute based on chosen path:

#### For Core Development:
```bash
# Copy example app
cp -r src/apps/example-app src/apps/{APP_NAME}

# List created files
ls -la src/apps/{APP_NAME}/
```

#### For Remote Development:
```bash
# Ensure remote apps directory exists
mkdir -p ~/hyperdata/trans-apps/apps

# Copy example app
cp -r src/apps/example-app ~/hyperdata/trans-apps/apps/{APP_NAME}

# List created files
ls -la ~/hyperdata/trans-apps/apps/{APP_NAME}/
```

### 3. Customize Files

Edit the following files in the new app directory:

**about.md** - Update runner path and description:
```markdown
# {APP_NAME}

## Runner

```sh
./trans {APP_NAME}
```

## Description

{USER_PROVIDED_DESCRIPTION}
```

**transmissions.ttl** - Update transmission definition:
```turtle
:{APP_NAME} a :EntryTransmission ;
    :pipe (:p10 :p20 :p30) .
```

**config.ttl** - Customize configuration as needed

### 4. Test the App

#### For Core Apps:
```bash
./trans {APP_NAME} -v
```

#### For Remote Apps:
```bash
./trans ~/hyperdata/trans-apps/apps/{APP_NAME} -v
```

### 5. Iteration

- If tests pass: App is ready for development
- If errors occur:
  - Check transmissions.ttl syntax
  - Verify all processor types exist
  - For remote apps, check [remote-development.md](remote-development.md) for module loading issues

## Next Steps

After basic app creation:
1. Add processors to the pipeline
2. Configure settings in config.ttl
3. Add test cases (see [templates/testing.md](templates/testing.md))
4. Document usage in about.md

## Common Patterns

Reference [templates/app-structure.md](templates/app-structure.md) for:
- Linear pipelines
- Conditional processing
- SPARQL integration
- File processing workflows

## Troubleshooting

**App not found:**
- Core: Check `src/apps/{APP_NAME}/` exists
- Remote: Verify full path is correct

**Processor not found:**
- Check processor type in transmissions.ttl matches registered type
- For custom processors, see the `transmissions-processor` skill

**Remote app loading issues:**
- See [remote-development.md](remote-development.md) for module loading details
- Check path resolution in verbose mode

## Reference

- Example app: `src/apps/example-app/`
- Manual: `docs/manual/user/apps.md`
- Core concepts: `docs/manual/user/concepts.md`
