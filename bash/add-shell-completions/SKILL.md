---
name: add-shell-completions
description: Add shell completion support via a 'completion' subcommand for bash, zsh, and fish. Generic pattern for any Commander.js CLI, with static and dynamic completion examples.
---

# Add Shell Completions

## Goal

Add a `completion` subcommand that outputs shell completion scripts for bash, zsh, and fish.

## Implementation

### 1. Create Completion Command

```ts
program
  .command('completion')
  .description('Output shell completion script')
  .argument('<shell>', 'Shell type: bash, zsh, or fish')
  .action((shell: string) => {
    switch (shell) {
      case 'bash':
        process.stdout.write(generateBashCompletion())
        break
      case 'zsh':
        process.stdout.write(generateZshCompletion())
        break
      case 'fish':
        process.stdout.write(generateFishCompletion())
        break
      default:
        throw new UserError(`Unknown shell: ${shell}. Supported: bash, zsh, fish`)
    }
  })
```

### 2. Bash Completion Script

```ts
function generateBashCompletion(): string {
  // Replace MYCLI and mycli with your CLI name
  return `
_mycli_completions() {
  local cur prev commands
  COMPREPLY=()
  cur="\${COMP_WORDS[COMP_CWORD]}"
  prev="\${COMP_WORDS[COMP_CWORD-1]}"
  commands="<list your subcommands here>"

  case "\${prev}" in
    mycli)
      COMPREPLY=( $(compgen -W "\${commands}" -- "\${cur}") )
      return 0
      ;;
    completion)
      COMPREPLY=( $(compgen -W "bash zsh fish" -- "\${cur}") )
      return 0
      ;;
  esac

  if [[ "\${cur}" == -* ]]; then
    COMPREPLY=( $(compgen -W "--help --version <your global flags>" -- "\${cur}") )
  fi
}
complete -F _mycli_completions mycli
`.trim()
}
```

### 3. Zsh Completion Script

```ts
function generateZshCompletion(): string {
  return `
#compdef mycli

_mycli() {
  local -a commands
  commands=(
    'command1:Description of command 1'
    'command2:Description of command 2'
    'completion:Output shell completion script'
  )

  _arguments -C \\
    '1:command:->command' \\
    '*::arg:->args'

  case $state in
    command)
      _describe 'command' commands
      ;;
    args)
      case $words[1] in
        command1)
          _arguments \\
            '--flag1[Description]:value:' \\
            '--flag2[Description]'
          ;;
        completion)
          _arguments '1:shell:(bash zsh fish)'
          ;;
      esac
      ;;
  esac
}

_mycli "$@"
`.trim()
}
```

### 4. Dynamic Completions

For values that depend on runtime state (e.g., available environments, project names):

```bash
# In bash completion, call the CLI with --json for machine-readable output
local items=$(mycli list --json 2>/dev/null | jq -r '.[]' 2>/dev/null)
COMPREPLY=( $(compgen -W "${items}" -- "${cur}") )
```

### 5. User Setup Instructions

Print setup instructions when running `mycli completion`:

```bash
# Bash: Add to ~/.bashrc
eval "$(mycli completion bash)"

# Zsh: Add to ~/.zshrc
eval "$(mycli completion zsh)"

# Fish: Run once
mycli completion fish > ~/.config/fish/completions/mycli.fish
```

### 6. Testing

```bash
mycli completion bash | bash  # Should not error
mycli completion zsh          # Should output valid zsh script
mycli completion fish         # Should output valid fish script
```
