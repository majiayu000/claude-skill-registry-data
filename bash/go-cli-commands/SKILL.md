---
name: go-cli-commands
description: The surface a Go CLI command exposes - the baseline every tool starts at, the two purchases on top of it, flag conventions, positional arguments, enum flags, a file-shaped value, and a flag that reads stdin. Use when adding or changing a flag, deciding whether a value should be a flag, a prompt, or a pipe, naming a value that spans lines, declaring Args, or validating a fixed set of allowed values. Triggers on PersistentFlags, BoolVar, StringVarP, SortFlags, cobra.NoArgs, ExactArgs, RangeArgs, pflag.Value, MarkFlagRequired, MarkFlagsOneRequired, MarkFlagsRequiredTogether, MarkFlagsMutuallyExclusive, MarkStdinLine, MarkStdinStream, and a flag whose value is -. Not for the shape of the command tree itself.
user-invocable: false
---

# Go CLI Commands

**What a command offers its caller: the arguments it takes, the flags it reads, and the ways a value reaches it.**

## The Command Surface

Every tool starts at one baseline and buys anything past it deliberately. The baseline is `tool <command> <args> --flags`: arguments name what is acted on, flags change how, and that is the whole surface a command gets without anyone asking for more. A `<thing>-file` flag is part of that baseline, so a command that reads its value out of a file, or that can work through many of them, registers one without asking.

Two extras sit on top. Neither is built unless the user asked for it, or it was offered while the surface was being designed and accepted.

| Purchase | What it adds |
|---|---|
| An interactive prompt | a value the user types when the flag is absent |
| Stdin eligibility | a flag reading its value from a pipe when given `-` |

Each purchase adds a path every later change has to keep working, so it is proposed while the surface is being designed rather than discovered halfway through an implementation. A command that looks like it wants one is raised as an offer. Both purchases can sit on a `<thing>-file` flag: `--url-file` exists on its own, while `--url-file -` and a prompt behind it are bought.

Three channels carry a value into a command, and which one a given value uses is a decision rather than a preference.

| Channel | Carries | Where it lives |
|---|---|---|
| Config and environment | credentials, endpoints, anything set once and reused | `~/.config/[APP_NAME]/`, and `[APP_NAME]_*` variables |
| Flags | everything else a single run needs | `init()` on the command that reads them |
| Prompts | a choice among options the user has not seen yet, or a secret that would land in shell history | a `utils` prompt helper |

Precedence, highest first: an explicit flag, then the environment, then the config file, then the built-in default. The flag wins because it is the most specific thing the caller said in this invocation. A value piped in belongs to the flag tier rather than to a tier of its own, since it arrives as that flag's value.

## Flags

Flags are registered in `init()`, one call per flag, next to the command they belong to.

A boolean flag takes a long name and no shorthand. A single letter standing for a switch abbreviates nothing the reader can recover, and it collides with the next switch somebody adds. A flag that takes a value may have a shorthand, because the value sitting beside it already says what it is.

```go
cmd.Flags().BoolVar(&flags.all, "all", false, "Include all items")
cmd.Flags().BoolVar(&flags.force, "force", false, "Overwrite an existing file")
cmd.Flags().StringVarP(&flags.name, "name", "n", "default", "Description")
cmd.Flags().IntVarP(&flags.count, "count", "c", 10, "Number of items")
cmd.Flags().StringSliceVarP(&flags.tags, "tag", "t", []string{}, "Tags (repeatable)")
cmd.Flags().DurationVarP(&flags.timeout, "timeout", "T", 30*time.Second, "Request timeout")
```

A flag registers at the level that reads it. `PersistentFlags` on the root is for what the whole tree honors, which in practice is `--debug` and nothing else; `PersistentFlags` on a parent command covers that group; everything else is `Flags()` on the command itself. A flag registered a level too high appears in the help of every command that ignores it.

Flag names stay unique across the whole tree, and Cobra does not catch a collision. `AddFlagSet` skips any flag whose name already exists (`pflag@v1.0.9 flag.go:914`), so a subcommand's local `--workers` shadows the root's persistent `--workers` with no error at registration and none at parse, and the subcommand reads a value the caller never set.

`SortFlags` stays at its default of `true` (`pflag@v1.0.9 flag.go:1270`), so `--help` lists flags alphabetically. A reader hunting one flag in the help output finds it faster than a reader reconstructing the order they were declared in.

`MarkFlagRequired` states a requirement Cobra enforces before `Run` is reached, which produces a usage message rather than a nil dereference:

```go
cmd.Flags().StringVarP(&flags.input, "input", "i", "", "Input file (required)")
cmd.MarkFlagRequired("input")
```

An environment variable supplies a default rather than being read inside `Run`, which is what puts the flag above it in precedence and makes `--help` show the value the command will actually use. A variable the tool owns is namespaced with the tool's name; one belonging to another tool keeps that tool's name.

```go
defaultToken := os.Getenv("GITHUB_TOKEN")
cmd.Flags().StringVarP(&flags.token, "token", "t", defaultToken, "GitHub token (or GITHUB_TOKEN env)")
```

Three markers state a relationship between flags that Cobra enforces at parse time, which is where the caller can still fix it (`cobra@v1.10.2 flag_groups.go`):

| The relationship | Marker |
|---|---|
| both flags only mean something together | `cmd.MarkFlagsRequiredTogether("cert", "key")` |
| at least one of the set is needed | `cmd.MarkFlagsOneRequired("file", "url")` |
| the flags contradict each other | `cmd.MarkFlagsMutuallyExclusive("file", "url")` |

The hand-rolled equivalent inside `Run` rejects the same combination several lines later, after the body has already done whatever it does before validating.

## Positional Arguments

Every command carrying a `Run` sets `Args`, including the ones taking none. Cobra falls back to `ArbitraryArgs` when `Args` is nil (`cobra@v1.10.2 command.go:1172-1177`), so a command silently swallowing a mistyped subcommand name as a positional and ignoring it is what a project gets by default.

| The command takes | `Args` |
|---|---|
| nothing | `cobra.NoArgs` |
| exactly n | `cobra.ExactArgs(n)` |
| at least n | `cobra.MinimumNArgs(n)` |
| between n and m | `cobra.RangeArgs(n, m)` |
| one value drawn from a known set | `cobra.MatchAll(cobra.ExactArgs(1), cobra.OnlyValidArgs)` |

A command that only groups subcommands leaves `Args` nil, because having no `Run` is exactly what puts `cobra.NoArgs` out of reach. `execute` returns `flag.ErrHelp` for a non-runnable command (`cobra@v1.10.2 command.go:955-957`) before it reaches `ValidateArgs` at `:968`, and `ExecuteC` renders that as help text with a nil error (`command.go:1152-1154`), so `appname feature bogus` prints help and exits zero either way.

On a root with subcommands, `Args` is worse than inert. `Find` calls `legacyArgs` only when `Args` is nil (`cobra@v1.10.2 command.go:775-777`), and that call is the only thing reporting an unknown command on a root with children, so `rootCmd.Args = cobra.NoArgs` turns `appname bogus` from an error into help text and exit zero.

## Enum Flags

A flag with a fixed set of allowed values validates through a `pflag.Value` implementation rather than inside `Run`, so a bad value is rejected before any work starts and `--help` states the set. `pflag.Value` is three methods (`pflag@v1.0.9 flag.go:208`).

```go
type mcpMode string

func (m *mcpMode) String() string { return string(*m) }
func (m *mcpMode) Type() string   { return "mcps|connectors|none" }

func (m *mcpMode) Set(v string) error {
    switch v {
    case "mcps", "connectors", "none":
        *m = mcpMode(v)
        return nil
    }
    return fmt.Errorf("must be one of mcps, connectors, none")
}
```

```go
launchCmd.Flags().Var(&launchFlags.mcp, "mcp", "Which MCP sources to load")
```

`Type()` is what `--help` prints beside the flag, so naming the allowed set there documents the flag without a second sentence of help text.

## Values from Stdin

Stdin eligibility is a purchase and is off by default. A flag reads stdin only once it has been marked, and no command infers a read from stdin not being a terminal. Inferring it means a run with stdin on `/dev/null`, closed, or inherited from a scheduler stores an empty value and reports success, which is the failure nobody notices until they need the value back.

A marked flag given the value `-` takes its value from stdin. The flag keeps the name of the thing it carries, so the invocation says which value came from the pipe without a second flag to point at it.

```
pwmgr add github --password -        # from the pipe
pwmgr add github --password hunter2  # inline, and now in shell history
pwmgr add github                     # prompts, and needs a terminal
```

Exactly one flag may be `-` in a single invocation, and two is an error naming both. There is one stream and no way to say where the first value ends, and an ordering contract to split it would be paid for by every invocation to serve the few that pipe anything at all.

Two read modes, fixed by the marking rather than by what arrives:

| Mode | Marked on | Reads |
|---|---|---|
| `line` | a single-value flag such as `--password` | the first line, discarding the rest |
| `stream` | a `<thing>-file` flag | all of stdin to EOF |

Which flag gets marked follows the shape of the value rather than convenience:

| The value is | Marked | Mode |
|---|---|---|
| inherently single, such as a password or a token | the bare flag | `line` |
| one or many by nature, such as a URL or a host | the `<thing>-file` flag only | `stream` |

A value that could be one or many never gets stdin eligibility on its bare flag. `--url` stays a single URL typed inline and a list arrives as `cat urls.txt | tool probe --url-file -`, because marking `--url` itself lets `cat urls.txt | tool probe --url -` read one URL and drop the other four, which is the one way this design produces a quietly wrong result instead of an error.

```go
func init() {
    addCmd.Flags().StringVar(&addFlags.password, "password", "", "Password, or - to read it from stdin")
    u.MarkStdinLine(addCmd, "password")

    probeCmd.Flags().StringVar(&probeFlags.urlFile, "url-file", "", "File of URLs, one per line, or - for stdin")
    u.MarkStdinStream(probeCmd, "url-file")
}
```

Marking is all a command does. The reading, the one-flag check, the terminal check, and the empty-input check live in the shared resolver in `utils`.

An inline secret is a convenience that leaks: it lands in shell history and is visible in `ps` output for the life of the process. `-` is the path a script takes, and the help text of a secret-bearing flag says so.

## File-Shaped Values

A value that can span lines never gets a bare flag. It gets `<thing>-file`, and one suffix covers both a list of single-line values and a single multi-line blob, with the flag's help text saying which the command expects. The suffix needs no offer behind it, so the flag is registered as soon as the command can take that input from a file.

| The value | The flags |
|---|---|
| one URL, or a list of them | `--url` and `--url-file` |
| an SSH public key, one line | `--ssh-pub-key` |
| an SSH private key, many lines | `--ssh-key-file` only |

`--ssh-key` is not offered at all, because a multi-line value passed as a flag argument survives one shell's quoting rules and not the next one's.
