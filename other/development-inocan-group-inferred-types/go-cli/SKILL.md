---
name: go-cli
description: CLI application patterns and best practices
sasmp_version: "1.3.0"
bonded_agent: 06-go-cli
bond_type: SECONDARY_BOND
---

# Go CLI Skill

Supplementary CLI patterns and utilities.

## Overview

Additional CLI patterns for argument parsing, progress indicators, and user interaction.

## Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| feature | string | yes | - | Feature: "progress", "prompt", "color" |

## Core Topics

### Argument Validation
```go
var cmd = &cobra.Command{
    Use:   "process [file]",
    Args:  cobra.ExactArgs(1),
    RunE: func(cmd *cobra.Command, args []string) error {
        file := args[0]
        if _, err := os.Stat(file); os.IsNotExist(err) {
            return fmt.Errorf("file not found: %s", file)
        }
        return process(file)
    },
}
```

### Progress Bar
```go
func DownloadWithProgress(url, dest string) error {
    resp, err := http.Get(url)
    if err != nil {
        return err
    }
    defer resp.Body.Close()

    file, err := os.Create(dest)
    if err != nil {
        return err
    }
    defer file.Close()

    bar := progressbar.DefaultBytes(resp.ContentLength, "downloading")
    _, err = io.Copy(io.MultiWriter(file, bar), resp.Body)
    return err
}
```

### Interactive Prompt
```go
func ConfirmAction(message string) bool {
    reader := bufio.NewReader(os.Stdin)
    fmt.Printf("%s [y/N]: ", message)

    input, _ := reader.ReadString('\n')
    input = strings.TrimSpace(strings.ToLower(input))

    return input == "y" || input == "yes"
}
```

### Colored Output
```go
import "github.com/fatih/color"

var (
    successColor = color.New(color.FgGreen).SprintFunc()
    errorColor   = color.New(color.FgRed).SprintFunc()
    warnColor    = color.New(color.FgYellow).SprintFunc()
)

func PrintSuccess(msg string) {
    fmt.Println(successColor("✓"), msg)
}

func PrintError(msg string) {
    fmt.Fprintln(os.Stderr, errorColor("✗"), msg)
}
```

## Troubleshooting

### Failure Modes
| Symptom | Cause | Fix |
|---------|-------|-----|
| Colors not showing | No TTY | Check isatty |
| Input hangs | Stdin closed | Handle EOF |

## Usage

```
Skill("go-cli")
```
