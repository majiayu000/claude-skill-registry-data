---
name: go-cli-tools
description: Build production CLI tools with Cobra, Viper, and terminal UI
sasmp_version: "1.3.0"
bonded_agent: 06-go-cli
bond_type: PRIMARY_BOND
---

# Go CLI Tools Skill

Build professional command-line applications with Go.

## Overview

Complete guide for building CLI tools with Cobra, Viper configuration, terminal UI, and cross-platform support.

## Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| framework | string | no | "cobra" | CLI framework |
| config_format | string | no | "yaml" | Config: "yaml", "json", "toml" |
| interactive | bool | no | false | Include interactive prompts |

## Core Topics

### Cobra Setup
```go
var rootCmd = &cobra.Command{
    Use:     "myapp",
    Short:   "My CLI application",
    Version: version,
    PersistentPreRunE: func(cmd *cobra.Command, args []string) error {
        return initConfig()
    },
}

func Execute() int {
    if err := rootCmd.Execute(); err != nil {
        fmt.Fprintln(os.Stderr, err)
        return 1
    }
    return 0
}

func init() {
    rootCmd.PersistentFlags().StringVarP(&cfgFile, "config", "c", "", "config file")
    rootCmd.PersistentFlags().BoolVarP(&verbose, "verbose", "v", false, "verbose output")
}
```

### Subcommands
```go
var serveCmd = &cobra.Command{
    Use:   "serve",
    Short: "Start the server",
    RunE: func(cmd *cobra.Command, args []string) error {
        port, _ := cmd.Flags().GetInt("port")
        return runServer(port)
    },
}

func init() {
    serveCmd.Flags().IntP("port", "p", 8080, "server port")
    rootCmd.AddCommand(serveCmd)
}
```

### Viper Configuration
```go
func initConfig() error {
    if cfgFile != "" {
        viper.SetConfigFile(cfgFile)
    } else {
        home, _ := os.UserHomeDir()
        viper.AddConfigPath(home)
        viper.AddConfigPath(".")
        viper.SetConfigName(".myapp")
        viper.SetConfigType("yaml")
    }

    viper.SetEnvPrefix("MYAPP")
    viper.AutomaticEnv()
    viper.SetEnvKeyReplacer(strings.NewReplacer(".", "_"))

    if err := viper.ReadInConfig(); err != nil {
        if _, ok := err.(viper.ConfigFileNotFoundError); !ok {
            return fmt.Errorf("config: %w", err)
        }
    }
    return nil
}
```

### Output Formatting
```go
type OutputFormat string

const (
    FormatJSON  OutputFormat = "json"
    FormatYAML  OutputFormat = "yaml"
    FormatTable OutputFormat = "table"
)

func PrintOutput(data interface{}, format OutputFormat) error {
    switch format {
    case FormatJSON:
        enc := json.NewEncoder(os.Stdout)
        enc.SetIndent("", "  ")
        return enc.Encode(data)
    case FormatYAML:
        out, err := yaml.Marshal(data)
        if err != nil {
            return err
        }
        fmt.Print(string(out))
        return nil
    case FormatTable:
        return printTable(data)
    default:
        return fmt.Errorf("unknown format: %s", format)
    }
}
```

### Signal Handling
```go
func runWithGracefulShutdown(fn func(ctx context.Context) error) error {
    ctx, cancel := context.WithCancel(context.Background())
    defer cancel()

    sigCh := make(chan os.Signal, 1)
    signal.Notify(sigCh, syscall.SIGINT, syscall.SIGTERM)

    errCh := make(chan error, 1)
    go func() {
        errCh <- fn(ctx)
    }()

    select {
    case err := <-errCh:
        return err
    case sig := <-sigCh:
        fmt.Printf("\nReceived %s, shutting down...\n", sig)
        cancel()
        return <-errCh
    }
}
```

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | General error |
| 2 | Invalid usage |
| 64 | Command line error |
| 65 | Data format error |

## Troubleshooting

### Failure Modes
| Symptom | Cause | Fix |
|---------|-------|-----|
| Exit 0 on error | Using Run not RunE | Switch to RunE |
| Flag undefined | Missing init() | Register in init() |
| Config not loaded | Wrong path | Check viper paths |

## Usage

```
Skill("go-cli-tools")
```
