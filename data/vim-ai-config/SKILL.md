---
name: vim-ai-config
description: Manage vim-ai plugin configuration files including .vimrc settings, custom roles, API keys, and model configurations. Use when user requests help with vim-ai setup, modifying vim-ai behavior, adding custom roles, changing AI models, updating prompts, or troubleshooting vim-ai issues.
---

# vim-ai Configuration Management Skill

This skill helps you manage and configure the vim-ai plugin for Vim/Neovim.

## What This Skill Does

This skill provides guidance and assistance for:
- Modifying vim-ai configuration in `.vimrc` or `init.vim`
- Managing custom roles in the roles configuration file
- Updating API keys and authentication settings
- Configuring AI models, endpoints, and parameters
- Customizing vim-ai UI and behavior
- Creating keyboard shortcuts and mappings
- Troubleshooting vim-ai issues

## Key Configuration Files

All configuration files are located on the user's system. Reference the [file paths documentation](file-paths.md) to locate the exact files to modify based on the user's request.

## How to Use This Skill

1. **Identify the user's goal** - What aspect of vim-ai do they want to configure?
2. **Locate the relevant file** - Use [file-paths.md](file-paths.md) to find which file needs to be modified
3. **Fetch current documentation** - Use [documentation-sources.md](documentation-sources.md) to get the latest vim-ai documentation
4. **Read the current configuration** - Always read the existing file before making changes
5. **Make targeted modifications** - Edit only what's necessary, preserving existing settings
6. **Test and verify** - Confirm changes work as expected

## Important Principles

- **Always read before writing**: Check current configuration before making changes
- **Preserve existing settings**: Don't overwrite unrelated configurations
- **Use official documentation**: Fetch latest docs from sources in [documentation-sources.md](documentation-sources.md)
- **Verify paths**: Confirm files exist at locations specified in [file-paths.md](file-paths.md)
- **Test changes**: Help user verify modifications work correctly

## Workflow Steps

1. Read [file-paths.md](file-paths.md) to determine which files need modification
2. Use WebFetch to get current vim-ai documentation from [documentation-sources.md](documentation-sources.md)
3. Read the existing configuration files using the Read tool
4. Make precise edits using the Edit tool (never overwrite entire files unnecessarily)
5. Document what was changed and why
6. Provide testing instructions

## Examples of What You Can Help With

- "Add a custom role for code review to vim-ai"
- "Change vim-ai to use GPT-4 instead of GPT-3.5"
- "Update my OpenAI API key for vim-ai"
- "Create a keyboard shortcut for AI chat in vim"
- "Configure vim-ai to use a different temperature setting"
- "Set up vim-ai to work with a local AI endpoint"
- "Fix vim-ai not loading in Neovim"

## Next Steps

When helping users, always:
1. Consult [file-paths.md](file-paths.md) for file locations
2. Check [documentation-sources.md](documentation-sources.md) for current vim-ai documentation URLs
3. Read existing files before making changes
4. Use targeted edits rather than complete rewrites
