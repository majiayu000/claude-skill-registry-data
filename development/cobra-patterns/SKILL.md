---
name: cobra-patterns
description: Production-ready Cobra CLI patterns including command structure, flags (local and persistent), nested commands, PreRun/PostRun hooks, argument validation, and initialization patterns used by kubectl and hugo. Use when building Go CLIs, implementing Cobra commands, creating nested command structures, managing flags, validating arguments, or when user mentions Cobra, CLI development, command-line tools, kubectl patterns, or Go CLI frameworks.
allowed-tools: Bash, Read, Write, Edit
---

# Cobra Patterns Skill

Production-ready patterns for building powerful CLI applications with Cobra, following best practices from kubectl, hugo, and other production CLIs.

## Instructions

### 1. Choose CLI Structure Pattern

Select the appropriate CLI structure based on your use case:

- **simple**: Single command with flags (quick utilities)
- **flat**: Root command with subcommands at one level
- **nested**: Hierarchical command structure (kubectl-style)
- **plugin**: Extensible CLI with plugin support
- **hybrid**: Mix of built-in and dynamic commands

### 2. Generate Cobra CLI Structure

Use the setup script to scaffold a new Cobra CLI:

```bash
cd /home/gotime2022/.claude/plugins/repos/cli-builder/skills/cobra-patterns
./scripts/setup-cobra-cli.sh <cli-name> <structure-type>
```

**Structure types:** `simple`, `flat`, `nested`, `plugin`, `hybrid`

**Example:**
```bash
./scripts/setup-cobra-cli.sh myctl nested
```

**What This Creates:**
- Complete directory structure with cmd/ package
- Root command with initialization
- Example subcommands
- Flag definitions (local and persistent)
- Cobra initialization (cobra init pattern)
- Go module configuration
- Main entry point

### 3. Command Structure Patterns

#### Basic Command Structure

```go
var exampleCmd = &cobra.Command{
    Use:   "example [flags]",
    Short: "Brief description",
    Long:  `Detailed description with examples`,
    Args:  cobra.ExactArgs(1),
    Run: func(cmd *cobra.Command, args []string) {
        // Command logic
    },
}
```

#### Command with Lifecycle Hooks

```go
var advancedCmd = &cobra.Command{
    Use:   "advanced",
    Short: "Advanced command with hooks",
    PersistentPreRun: func(cmd *cobra.Command, args []string) {
        // Runs before command execution (inherited by children)
    },
    PreRun: func(cmd *cobra.Command, args []string) {
        // Runs before command execution (local only)
    },
    Run: func(cmd *cobra.Command, args []string) {
        // Main command logic
    },
    PostRun: func(cmd *cobra.Command, args []string) {
        // Runs after command execution (local only)
    },
    PersistentPostRun: func(cmd *cobra.Command, args []string) {
        // Runs after command execution (inherited by children)
    },
}
```

#### Command with Error Handling

```go
var robustCmd = &cobra.Command{
    Use:   "robust",
    Short: "Command with proper error handling",
    RunE: func(cmd *cobra.Command, args []string) error {
        // Return errors instead of os.Exit
        if err := validateInput(args); err != nil {
            return fmt.Errorf("validation failed: %w", err)
        }

        if err := executeOperation(); err != nil {
            return fmt.Errorf("operation failed: %w", err)
        }

        return nil
    },
}
```

### 4. Flag Management Patterns

#### Persistent Flags (Global Options)

```go
func init() {
    // Available to this command and all subcommands
    rootCmd.PersistentFlags().StringVarP(&cfgFile, "config", "c", "", "config file")
    rootCmd.PersistentFlags().BoolVarP(&verbose, "verbose", "v", false, "verbose output")
    rootCmd.PersistentFlags().StringVar(&logLevel, "log-level", "info", "log level")
}
```

#### Local Flags (Command-Specific)

```go
func init() {
    // Only available to this specific command
    createCmd.Flags().StringVarP(&name, "name", "n", "", "resource name")
    createCmd.Flags().IntVar(&replicas, "replicas", 1, "number of replicas")
    createCmd.Flags().BoolVar(&dryRun, "dry-run", false, "simulate operation")

    // Mark required flags
    createCmd.MarkFlagRequired("name")
}
```

#### Flag Groups and Validation

```go
func init() {
    // Mutually exclusive flags (only one allowed)
    createCmd.MarkFlagsMutuallyExclusive("json", "yaml", "text")

    // Required together (all or none)
    createCmd.MarkFlagsRequiredTogether("username", "password")

    // At least one required
    createCmd.MarkFlagsOneRequired("file", "stdin", "url")

    // Custom flag completion
    createCmd.RegisterFlagCompletionFunc("format", func(cmd *cobra.Command, args []string, toComplete string) ([]string, cobra.ShellCompDirective) {
        return []string{"json", "yaml", "text"}, cobra.ShellCompDirectiveNoFileComp
    })
}
```

### 5. Nested Command Patterns

#### Root Command Setup

```go
// cmd/root.go
var rootCmd = &cobra.Command{
    Use:   "myctl",
    Short: "A production-grade CLI tool",
    Long: `A complete CLI application built with Cobra.

This application demonstrates production patterns including
nested commands, flag management, and proper error handling.`,
}

func Execute() error {
    return rootCmd.Execute()
}

func init() {
    cobra.OnInitialize(initConfig)

    // Global flags
    rootCmd.PersistentFlags().StringVar(&cfgFile, "config", "", "config file")
    rootCmd.PersistentFlags().BoolVarP(&verbose, "verbose", "v", false, "verbose output")

    // Add subcommands
    rootCmd.AddCommand(getCmd)
    rootCmd.AddCommand(createCmd)
    rootCmd.AddCommand(deleteCmd)
}

func initConfig() {
    // Initialize configuration, logging, etc.
}
```

#### Subcommand with Children (kubectl-style)

```go
// cmd/create/create.go
var createCmd = &cobra.Command{
    Use:   "create",
    Short: "Create resources",
    Long:  `Create various types of resources`,
}

func init() {
    // Add nested subcommands
    createCmd.AddCommand(createDeploymentCmd)
    createCmd.AddCommand(createServiceCmd)
    createCmd.AddCommand(createConfigMapCmd)
}

// cmd/create/deployment.go
var createDeploymentCmd = &cobra.Command{
    Use:   "deployment [name]",
    Short: "Create a deployment",
    Args:  cobra.ExactArgs(1),
    RunE: func(cmd *cobra.Command, args []string) error {
        return createDeployment(args[0])
    },
}
```

#### Command Groups (Organized Help)

```go
func init() {
    // Define command groups
    rootCmd.AddGroup(&cobra.Group{
        ID:    "basic",
        Title: "Basic Commands:",
    })
    rootCmd.AddGroup(&cobra.Group{
        ID:    "management",
        Title: "Management Commands:",
    })

    // Assign commands to groups
    getCmd.GroupID = "basic"
    createCmd.GroupID = "management"
}
```

### 6. Argument Validation Patterns

```go
// No arguments allowed
var noArgsCmd = &cobra.Command{
    Use:  "list",
    Args: cobra.NoArgs,
    RunE: func(cmd *cobra.Command, args []string) error {
        return listResources()
    },
}

// Exactly n arguments
var exactArgsCmd = &cobra.Command{
    Use:  "get <name>",
    Args: cobra.ExactArgs(1),
    RunE: func(cmd *cobra.Command, args []string) error {
        return getResource(args[0])
    },
}

// Range of arguments
var rangeArgsCmd = &cobra.Command{
    Use:  "delete <name> [names...]",
    Args: cobra.RangeArgs(1, 5),
    RunE: func(cmd *cobra.Command, args []string) error {
        return deleteResources(args)
    },
}

// Custom validation
var customValidationCmd = &cobra.Command{
    Use: "custom",
    Args: func(cmd *cobra.Command, args []string) error {
        if len(args) < 1 {
            return fmt.Errorf("requires at least 1 argument")
        }
        for _, arg := range args {
            if !isValid(arg) {
                return fmt.Errorf("invalid argument: %s", arg)
            }
        }
        return nil
    },
    RunE: func(cmd *cobra.Command, args []string) error {
        return processArgs(args)
    },
}

// Valid args with completion
var validArgsCmd = &cobra.Command{
    Use:       "select <resource>",
    ValidArgs: []string{"pod", "service", "deployment", "configmap"},
    Args:      cobra.OnlyValidArgs,
    RunE: func(cmd *cobra.Command, args []string) error {
        return selectResource(args[0])
    },
}
```

### 7. Initialization and Configuration Patterns

#### cobra.OnInitialize Pattern

```go
var (
    cfgFile string
    config  Config
)

func init() {
    // Register initialization functions
    cobra.OnInitialize(initConfig, initLogging, initClient)

    rootCmd.PersistentFlags().StringVar(&cfgFile, "config", "", "config file")
}

func initConfig() {
    if cfgFile != "" {
        viper.SetConfigFile(cfgFile)
    } else {
        home, err := os.UserHomeDir()
        cobra.CheckErr(err)

        viper.AddConfigPath(home)
        viper.SetConfigType("yaml")
        viper.SetConfigName(".myctl")
    }

    viper.AutomaticEnv()

    if err := viper.ReadInConfig(); err == nil {
        fmt.Fprintln(os.Stderr, "Using config file:", viper.ConfigFileUsed())
    }
}

func initLogging() {
    // Setup logging based on flags
}

func initClient() {
    // Initialize API clients, connections, etc.
}
```

#### Viper Integration

```go
import (
    "github.com/spf13/cobra"
    "github.com/spf13/viper"
)

func init() {
    // Bind flags to viper
    rootCmd.PersistentFlags().String("output", "json", "output format")
    viper.BindPFlag("output", rootCmd.PersistentFlags().Lookup("output"))

    // Set defaults
    viper.SetDefault("output", "json")
    viper.SetDefault("timeout", 30)
}

func Execute() error {
    // Access config via viper
    output := viper.GetString("output")
    timeout := viper.GetInt("timeout")

    return rootCmd.Execute()
}
```

### 8. Production Patterns

#### Kubectl-Style Command Structure

```go
// Organize commands by resource type
// myctl get pods
// myctl create deployment
// myctl delete service

var getCmd = &cobra.Command{
    Use:   "get",
    Short: "Display resources",
}

var createCmd = &cobra.Command{
    Use:   "create",
    Short: "Create resources",
}

func init() {
    // Resource-specific subcommands
    getCmd.AddCommand(getPodsCmd)
    getCmd.AddCommand(getServicesCmd)

    createCmd.AddCommand(createDeploymentCmd)
    createCmd.AddCommand(createServiceCmd)
}
```

#### Hugo-Style Plugin Commands

```go
// Support external commands (hugo server, hugo new, etc.)
func init() {
    rootCmd.AddCommand(serverCmd)
    rootCmd.AddCommand(newCmd)

    // Auto-discover plugin commands
    discoverPluginCommands(rootCmd)
}

func discoverPluginCommands(root *cobra.Command) {
    // Look for executables like "myctl-plugin-*"
    // Add them as dynamic commands
}
```

#### Context and Cancellation

```go
var longRunningCmd = &cobra.Command{
    Use:   "process",
    Short: "Long-running operation",
    RunE: func(cmd *cobra.Command, args []string) error {
        ctx := cmd.Context()

        // Respect context cancellation (Ctrl+C)
        return processWithContext(ctx)
    },
}

func processWithContext(ctx context.Context) error {
    ticker := time.NewTicker(1 * time.Second)
    defer ticker.Stop()

    for {
        select {
        case <-ctx.Done():
            return ctx.Err()
        case <-ticker.C:
            // Do work
        }
    }
}
```

### 9. Validation and Testing

Use validation scripts to ensure CLI compliance:

```bash
# Validate command structure
./scripts/validate-cobra-cli.sh <cli-directory>

# Test command execution
./scripts/test-cobra-commands.sh <cli-binary>

# Generate shell completions
./scripts/generate-completions.sh <cli-binary>
```

**Validation Checks:**
- All commands have Use, Short, and Long descriptions
- Flags are properly defined and documented
- Required flags are marked
- Argument validation is implemented
- RunE is used for error handling
- Commands are organized in logical groups

### 10. Shell Completion Support

```go
var completionCmd = &cobra.Command{
    Use:   "completion [bash|zsh|fish|powershell]",
    Short: "Generate completion script",
    Long: `Generate shell completion script.

Example usage:
    # Bash
    source <(myctl completion bash)

    # Zsh
    source <(myctl completion zsh)

    # Fish
    myctl completion fish | source

    # PowerShell
    myctl completion powershell | Out-String | Invoke-Expression
`,
    DisableFlagsInUseLine: true,
    ValidArgs:             []string{"bash", "zsh", "fish", "powershell"},
    Args:                  cobra.ExactArgs(1),
    RunE: func(cmd *cobra.Command, args []string) error {
        switch args[0] {
        case "bash":
            return cmd.Root().GenBashCompletion(os.Stdout)
        case "zsh":
            return cmd.Root().GenZshCompletion(os.Stdout)
        case "fish":
            return cmd.Root().GenFishCompletion(os.Stdout, true)
        case "powershell":
            return cmd.Root().GenPowerShellCompletionWithDesc(os.Stdout)
        default:
            return fmt.Errorf("unsupported shell: %s", args[0])
        }
    },
}
```

## Available Scripts

- **setup-cobra-cli.sh**: Scaffold new Cobra CLI with chosen structure
- **validate-cobra-cli.sh**: Validate CLI structure and patterns
- **test-cobra-commands.sh**: Test all commands and flags
- **generate-completions.sh**: Generate shell completion scripts
- **add-command.sh**: Add new command to existing CLI
- **refactor-flags.sh**: Reorganize flags (local to persistent, etc.)

## Templates

### Core Templates
- **root.go**: Root command with initialization
- **command.go**: Basic command template
- **nested-command.go**: Subcommand with children
- **main.go**: CLI entry point
- **config.go**: Configuration management with Viper

### Command Templates
- **get-command.go**: Read/retrieve operation
- **create-command.go**: Create operation with validation
- **delete-command.go**: Delete with confirmation
- **list-command.go**: List resources with filtering
- **update-command.go**: Update with partial modifications

### Advanced Templates
- **plugin-command.go**: Extensible plugin support
- **completion-command.go**: Shell completion generation
- **version-command.go**: Version information display
- **middleware.go**: Command middleware pattern
- **context-command.go**: Context-aware command

### Flag Templates
- **persistent-flags.go**: Global flag definitions
- **flag-groups.go**: Flag validation groups
- **custom-flags.go**: Custom flag types
- **viper-flags.go**: Viper-integrated flags

### Testing Templates
- **command_test.go**: Command unit test
- **integration_test.go**: CLI integration test
- **mock_test.go**: Mock dependencies for testing

## Examples

See `examples/` directory for production patterns:
- `kubectl-style/`: Kubectl command organization pattern
- `hugo-style/`: Hugo plugin architecture pattern
- `simple-cli/`: Basic single-level CLI
- `nested-cli/`: Multi-level command hierarchy
- `production-cli/`: Full production CLI with all features

Each example includes:
- Complete working CLI
- Command structure documentation
- Flag management examples
- Test suite
- Shell completion setup

## Best Practices

### Command Organization
1. One command per file for maintainability
2. Group related commands in subdirectories
3. Use command groups for organized help output
4. Keep root command focused on initialization

### Flag Management
1. Use persistent flags for truly global options
2. Mark required flags explicitly
3. Provide sensible defaults
4. Use flag groups for related options
5. Implement custom completion for better UX

### Error Handling
1. Always use RunE instead of Run
2. Return wrapped errors with context
3. Use cobra.CheckErr() for fatal errors
4. Provide helpful error messages with suggestions

### Code Organization
1. Separate command definition from logic
2. Keep business logic in separate packages
3. Use dependency injection for testability
4. Avoid global state where possible

### Documentation
1. Provide both Short and Long descriptions
2. Include usage examples in Long description
3. Document all flags with clear help text
4. Generate and maintain shell completions

### Testing
1. Unit test command functions separately
2. Integration test full command execution
3. Mock external dependencies
4. Test flag validation and argument parsing
5. Verify error messages and exit codes

### Performance
1. Use cobra.OnInitialize for lazy loading
2. Avoid expensive operations in init()
3. Implement context cancellation
4. Profile and optimize hot paths

## Common Workflows

### Creating a New Nested CLI

```bash
# 1. Generate CLI structure
./scripts/setup-cobra-cli.sh myctl nested

# 2. Add commands
cd myctl
../scripts/add-command.sh get
../scripts/add-command.sh create --parent get

# 3. Validate structure
../scripts/validate-cobra-cli.sh .

# 4. Build and test
go build -o myctl
./myctl --help
```

### Adding Authentication to CLI

```bash
# Use authentication template
cp templates/auth-command.go cmd/login.go

# Add persistent auth flags
cp templates/auth-flags.go cmd/root.go

# Implement token management
# Edit cmd/root.go to add initAuth() to cobra.OnInitialize
```

### Implementing kubectl-Style Resource Commands

```bash
# Generate resource-based structure
./scripts/setup-cobra-cli.sh myctl nested

# Add resource commands (get, create, delete, update)
./scripts/add-command.sh get --style kubectl
./scripts/add-command.sh create --style kubectl

# Add resource types as subcommands
./scripts/add-command.sh pods --parent get
./scripts/add-command.sh services --parent get
```

## Troubleshooting

**Commands not showing in help**: Ensure AddCommand() is called in init()

**Flags not recognized**: Check if flag is registered before command execution

**PersistentFlags not inherited**: Verify parent command has PersistentFlags defined

**Completion not working**: Run completion command and source output, check ValidArgs

**Context cancellation ignored**: Ensure you're checking ctx.Done() in long-running operations

## Integration

This skill is used by:
- CLI generation commands - Scaffolding new CLIs
- Code generation agents - Implementing CLI patterns
- Testing commands - Validating CLI structure
- All Go CLI development workflows

---

**Plugin:** cli-builder
**Version:** 1.0.0
**Category:** Go CLI Development
**Skill Type:** Patterns & Templates
