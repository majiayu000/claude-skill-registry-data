---
name: go-spf13-viper
description: "Configuration management with spf13/viper. Covers layered precedence (flags > env > files), binding, unmarshaling, and hot reloading."
metadata:
  model: models/gemini-3.1-pro-preview
  last_modified: Wed, 06 May 2026 06:25:00 GMT
---

## Precedence Order

Viper resolves keys by checking sources in this specific order (highest priority first):
1. **Explicit `Set`**: `viper.Set("port", 8080)`
2. **Flags**: Bound via `BindPFlag` from Cobra.
3. **Environment Variables**: `SetEnvPrefix`, `AutomaticEnv`.
4. **Config Files**: YAML, JSON, TOML, etc.
5. **Key/Value Remote Store**: Etcd, Consul.
6. **Default Values**: `viper.SetDefault("port", 8080)`.

## Best Practices

1. **Set Prefix and Replacer** — Always use `SetEnvPrefix` to avoid name collisions and `SetEnvKeyReplacer(strings.NewReplacer(".", "_"))` to support nested keys in environment variables (e.g., `DB.HOST` becomes `MYAPP_DB_HOST`).
2. **Handle File Not Found** — Don't fail the app if the config file is missing; many environments (like CI or Docker) might rely solely on environment variables.
3. **Use `mapstructure` Tags** — When unmarshaling into a struct, always provide explicit tags. Viper doesn't handle casing perfectly by default.
4. **Test Isolation** — Never use the global `viper` instance in tests. It creates state leakage between test cases. Use `viper.New()` instead.
5. **Bind Early** — Bind Cobra flags to Viper in `init()` or `PersistentPreRunE`.

## Configuration Example

```go
func initConfig() {
    v := viper.New() // isolated instance for testability
    v.SetConfigName("config")
    v.AddConfigPath(".")
    v.SetEnvPrefix("APP")
    v.SetEnvKeyReplacer(strings.NewReplacer(".", "_"))
    v.AutomaticEnv()

    if err := v.ReadInConfig(); err != nil {
        if _, ok := err.(viper.ConfigFileNotFoundError); !ok {
            log.Fatalf("error reading config: %s", err)
        }
    }
}
```

## Unmarshaling into a Struct

```go
type Config struct {
    Port int    `mapstructure:"port"`
    DB   struct {
        Host string `mapstructure:"host"`
        User string `mapstructure:"user"`
    } `mapstructure:"db"`
}

var cfg Config
if err := v.Unmarshal(&cfg); err != nil {
    log.Fatalf("unable to decode into struct: %v", err)
}
```

## Binding to Cobra Flags

```go
func init() {
    rootCmd.PersistentFlags().Int("port", 8080, "App port")
    viper.BindPFlag("port", rootCmd.PersistentFlags().Lookup("port"))
}
```

## Anti-patterns

- ❌ **`AutomaticEnv()` without a Replacer** — Nested config keys won't be reachable via environment variables.
- ❌ **Hardcoding the Global `viper`** — Makes unit tests for configuration logic impossible to run in parallel.
- ❌ **Crashing on missing config file** — Prevents users from running the app with just flags or env vars.
- ❌ **Implicit struct mapping** — Missing `mapstructure` tags leads to fields being silently ignored or incorrectly mapped.
- ❌ **Binding flags in `RunE`** — Binding happens after flags are parsed, so the bound values won't be available to Viper during execution.
