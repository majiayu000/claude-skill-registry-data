---
name: managing-forks
description: Manages parallel conversation branches using git worktrees. Use when you want to explore multiple solution approaches simultaneously, need to try different implementations, or want to checkpoint your current conversation state before branching into alternative paths.
---

# Managing Forks - Conversation Branching for Claude Code

This skill enables you to create and manage parallel conversation branches (forks) using git worktrees. Each fork is an independent workspace where you can explore different approaches to solving a problem.

## When to Use This Skill

Use fork management when:
- The user wants to try multiple implementation approaches in parallel
- You need to explore different solutions without losing your current progress
- The user asks to "fork" the conversation or try alternatives
- Working on a feature and want to experiment with different designs
- The user wants to checkpoint the current state before making major changes

## Core Commands

### Creating Forks

**Basic Fork Creation:**
```bash
src/fork_create.sh <number>
```

Creates N parallel fork branches from the current conversation checkpoint.

Example:
```bash
src/fork_create.sh 3
```
Creates 3 parallel branches, each with its own git worktree.

**Fork with Target Branch:**
```bash
src/fork_create.sh <number> --target <branch-name>
```

Creates N forks that all target a specific branch (useful for feature development).

Example:
```bash
src/fork_create.sh 3 --target feature-auth
```
Creates 3 forks from and targeting the `feature-auth` branch. All forks will merge back to this branch.

### Listing Forks

```bash
src/fork_list.sh
```

Shows all active fork branches with their metadata, creation time, status, and worktree paths.

### Viewing Fork Hierarchy

```bash
src/fork_tree.sh
```

Displays a visual tree representation of all forks and their parent-child relationships. Useful for understanding nested fork structures.

### Switching Between Forks

```bash
src/fork_switch.sh <fork-id>
```

Switches the working environment to a different fork branch.

Example:
```bash
src/fork_switch.sh fork-1730678901-a1b2c3d4-2
```

### Checking Fork Status

```bash
src/fork_status.sh
```

Shows the current fork's status, including git status, worktree information, and fork metadata.

### Merging Forks

```bash
src/fork_merge.sh <source-fork-id>
```

Merges changes from another fork branch into the current branch.

Example:
```bash
src/fork_merge.sh fork-1730678901-a1b2c3d4-1
```

### Deleting Forks

```bash
src/fork_delete.sh <fork-id>
```

Deletes a fork branch, its worktree, and associated metadata. Prompts for confirmation.

Example:
```bash
src/fork_delete.sh fork-1730678901-a1b2c3d4-3
```

## Workflow Examples

### Example 1: Exploring Multiple Implementation Approaches

User asks: "I want to try implementing this feature using both REST and GraphQL approaches"

Response workflow:
1. Create 2 forks: `src/fork_create.sh 2 --target feature-api`
2. In fork-1: Implement using REST
3. In fork-2: Implement using GraphQL
4. User evaluates both approaches
5. Merge the preferred approach back to feature-api

### Example 2: Trying Different Design Patterns

User asks: "Let's explore both MVC and Clean Architecture for this"

Response workflow:
1. Ensure current work is committed
2. Create 2 forks: `src/fork_create.sh 2 --target feature-refactor`
3. Switch to fork-1: Implement MVC pattern
4. Switch to fork-2: Implement Clean Architecture
5. User compares both implementations
6. Merge chosen pattern back

### Example 3: Nested Forks for Sub-Experiments

User asks: "In the GraphQL approach, let's try two different schema designs"

Response workflow:
1. Switch to the GraphQL fork
2. Create nested forks: `src/fork_create.sh 2 --target graphql-schema`
3. Implement different schemas in each nested fork
4. Merge best schema back to GraphQL fork
5. Eventually merge GraphQL fork to main feature branch

## Best Practices

### Before Creating Forks

1. **Commit current work**: Ensure git working directory is clean
   ```bash
   git add . && git commit -m "checkpoint before forking"
   ```

2. **Check you're in a git repository**:
   ```bash
   git status
   ```

3. **Plan your forks**: Think about how many parallel approaches you need

### During Fork Work

1. **Stay organized**: Use descriptive commit messages in each fork
2. **Document differences**: Note why each approach differs
3. **Test independently**: Each fork should be tested on its own
4. **Use fork status**: Regularly check `src/fork_status.sh` to see where you are

### After Fork Work

1. **Evaluate results**: Compare implementations across forks
2. **Merge carefully**: Use `src/fork_merge.sh` to combine best elements
3. **Clean up**: Delete unused forks with `src/fork_delete.sh`
4. **Document decisions**: Note why you chose one approach over another

## Technical Details

### What Happens When You Create a Fork

1. **Git worktree creation**: Each fork gets an isolated git worktree
2. **Checkpoint saving**: Current conversation state is saved to JSON
3. **Branch creation**: New git branch created for the fork
4. **Metadata storage**: Fork information stored in `~/.claude-code/forks/`
5. **Terminal session**: If tmux is available, creates dedicated session

### Fork Data Structure

```
~/.claude-code/forks/
├── fork-xxx-1/
│   ├── checkpoint.json     # Conversation state
│   ├── metadata.json       # Fork metadata
│   ├── worktree/          # Git worktree
│   └── launch.sh          # Launcher script
├── fork-xxx-2/
│   └── ...
└── .fork-groups.json      # Fork group relationships
```

### Metadata Fields

Each fork stores:
- `fork_id`: Unique identifier
- `parent_id`: Parent fork (for nested forks)
- `target_branch`: Target branch for merging (if specified)
- `branch_number`: Position in fork group
- `total_branches`: Total forks in group
- `worktree_path`: Path to git worktree
- `status`: active/archived
- `created_at`: ISO timestamp

## Error Handling

### Common Issues

**"Not in a git repository"**
- Solution: Navigate to a git repository before creating forks

**"Worktree already exists"**
- Solution: Run `git worktree prune` to clean up stale worktrees

**"Fork not found"**
- Solution: Run `src/fork_list.sh` to see available forks

**"Cannot create worktree"**
- Solution: Ensure uncommitted changes are committed or stashed

### Recovery

If forks become corrupted:
1. List all worktrees: `git worktree list`
2. Prune stale worktrees: `git worktree prune`
3. Clean fork data: `rm -rf ~/.claude-code/forks/<bad-fork-id>`

## Limitations

- Maximum 10 forks can be created at once (configurable)
- Fork IDs are auto-generated and not human-readable
- Worktrees must be on the same filesystem
- Each fork requires disk space for its worktree

## Integration with Terminal Multiplexing

### tmux Mode (Recommended)

When tmux is installed:
- Each fork gets a dedicated tmux session
- Easy switching with `tmux attach -t fork-<id>`
- Multiple panes can be created in each session

### Fallback Modes

When tmux is not available:
- **macOS**: Generates iTerm2/Terminal.app launcher scripts
- **Linux**: Creates shell launcher scripts
- **Basic**: Simple directory switching

## Configuration

User configuration is stored in `~/.config/fork-yeah/config.yaml`:

```yaml
terminal:
  mode: auto  # auto, tmux, macos, linux, basic

fork:
  max_forks: 10
  auto_checkpoint: true

display:
  use_colors: true
  tree_ascii: true
```

## Tips for Effective Fork Usage

1. **Communicate clearly**: Tell the user which fork you're working in
2. **Use target branches**: Always specify `--target` for feature work
3. **Keep forks focused**: Each fork should explore one specific approach
4. **Document as you go**: Add commit messages explaining your choices
5. **Merge incrementally**: Don't wait until the end to merge good ideas
6. **Visualize often**: Use `src/fork_tree.sh` to stay oriented

## Related Documentation

- Full user guide: `README.md`
- Troubleshooting: `docs/TROUBLESHOOTING.md`
- Marketplace info: `MARKETPLACE.md`
- Configuration reference: `config/config.yaml`
