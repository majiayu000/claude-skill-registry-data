---
name: go-oauth-cli
description: OAuth2 login for a Go CLI client, with three explicit modes and cached token refresh. Use when a CLI tool authenticates against Google, GitHub, Microsoft, or another OAuth2 provider, when building internal/auth/, or when adding a login command. Triggers on golang.org/x/oauth2, AuthCodeURL, config.Exchange, DeviceAuth, DeviceAccessToken, TokenSource, token.json, credentials.json, --device-login, and --manual. Not for server-side web OAuth where the browser stays on your own site.
user-invocable: false
---

# Go OAuth for CLI Clients

**Three login modes the user picks explicitly, a token cached at `~/.config/[APP_NAME]/token.json`, and automatic refresh on every use.**

This covers a terminal tool obtaining a token for itself. A web server authenticating its own visitors is a different problem with a different session model.

| Mode | Flag | How it works | Environment |
|---|---|---|---|
| Callback | none, the default | opens a browser, a localhost server receives the redirect | interactive desktop |
| Device | `--device-login` | shows a URL and a code, polls until authorized | headless, SSH, a server |
| Manual | `--manual` | shows a URL, the user pastes the authorization code back | last resort, no device flow |

The user selects the mode with a flag and there is no automatic fallback chain, because a chain that silently degrades leaves them watching a browser that will never open. The default reports its own failure and names `--device-login` as the fix.

Not every provider implements device authorization. When it does not, omit `loginWithDevice` and the `--device-login` flag rather than shipping a mode that always fails.

| Provider | Device auth | Device auth URL |
|---|---|---|
| Google | yes | `https://oauth2.googleapis.com/device/code` |
| Microsoft | yes | `https://login.microsoftonline.com/common/oauth2/v2.0/devicecode` |
| GitHub | yes | `https://github.com/login/device/code` |
| Box.com | no | none |

## Output Tiers

| Call | Used for |
|---|---|
| `u.PrintInfo` | instructions and status: "Opening browser...", "Waiting for authorization..." |
| `u.PrintGeneric` | data the user copies: URLs, user codes |
| `u.PromptInput` | the manual-mode paste, which needs a terminal and returns `ErrNoTerminal` without one |
| `u.PrintFatal`, `u.PrintSuccess` | the command layer only |

URLs and codes go through `PrintGeneric` so they arrive unstyled and unprefixed, which is what makes them safe to copy out of a terminal or a pipe.

## Security

The CSRF state token is a 16-byte random hex value validated on the callback flow: the localhost server compares the redirect's `state` against the generated value and rejects a mismatch. The manual flow transfers the code by hand with no automated redirect to validate, so it still sends a `state` parameter where a provider requires one but that parameter is not a CSRF control there. The device flow uses no `state` at all.

`openBrowser` returns an error instead of failing silently, so a headless machine reports the problem immediately rather than after the five-minute callback timeout.

The token file is written at `0600` and the config directory created at `0700`, since a bearer token in a shared home directory is a credential anyone on the box can read.

`AccessTypeOffline` requests a refresh token, without which the user re-authenticates every hour.

## internal/auth/auth.go

```go
package auth

import (
    "context"
    "crypto/rand"
    "encoding/hex"
    "encoding/json/jsontext"
    "encoding/json/v2"
    "errors"
    "fmt"
    "net"
    "net/http"
    "os"
    "os/exec"
    "path/filepath"
    "runtime"
    "strings"
    "time"

    u "github.com/[GITHUB_USER]/[REPO_NAME]/utils"
    "golang.org/x/oauth2"
)

func ConfigDir() string {
    home, err := os.UserHomeDir()
    if err != nil {
        u.PrintFatal("cannot determine home directory", err)
    }
    dir := filepath.Join(home, ".config", "[APP_NAME]")
    if err := os.MkdirAll(dir, 0700); err != nil {
        u.PrintFatal("cannot create config directory", err)
    }
    return dir
}

func LoadCredentials() (*oauth2.Config, error) {
    credPath := filepath.Join(ConfigDir(), "credentials.json")
    data, err := os.ReadFile(credPath)
    if err != nil {
        return nil, fmt.Errorf("create %s with your OAuth client credentials", credPath)
    }
    // Google: google.ConfigFromJSON(data, scopes...)
    // Others: construct oauth2.Config directly with the provider's endpoints
    return config, nil
}

func Login(config *oauth2.Config, mode string) (*oauth2.Token, error) {
    switch mode {
    case "device":
        return loginWithDevice(config)
    case "manual":
        state, err := generateState()
        if err != nil {
            return nil, fmt.Errorf("failed to generate state: %w", err)
        }
        return loginWithManual(config, state)
    default:
        state, err := generateState()
        if err != nil {
            return nil, fmt.Errorf("failed to generate state: %w", err)
        }
        return loginWithCallback(config, state)
    }
}
```

`Login` takes the mode as a string so the command layer maps flags to a mode and the auth package owns the flows, which keeps Cobra out of a package a test can drive directly.

```go
func loginWithCallback(config *oauth2.Config, state string) (*oauth2.Token, error) {
    listener, err := net.Listen("tcp", "127.0.0.1:0")
    if err != nil {
        return nil, fmt.Errorf("cannot start callback server: %w", err)
    }
    port := listener.Addr().(*net.TCPAddr).Port
    config.RedirectURL = fmt.Sprintf("http://localhost:%d", port)

    authURL := config.AuthCodeURL(state, oauth2.AccessTypeOffline, oauth2.ApprovalForce)

    codeCh := make(chan string, 1)
    errCh := make(chan error, 1)

    mux := http.NewServeMux()
    mux.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
        if r.URL.Query().Get("state") != state {
            errCh <- fmt.Errorf("state mismatch, possible CSRF attack")
            http.Error(w, "State mismatch", http.StatusBadRequest)
            return
        }
        code := r.URL.Query().Get("code")
        if code == "" {
            errCh <- fmt.Errorf("no auth code in callback")
            http.Error(w, "Missing code", http.StatusBadRequest)
            return
        }
        fmt.Fprint(w, "<html><body><h2>Authentication successful</h2><p>You can close this tab.</p></body></html>")
        codeCh <- code
    })

    srv := &http.Server{Handler: mux}
    go func() {
        if err := srv.Serve(listener); !errors.Is(err, http.ErrServerClosed) {
            errCh <- err
        }
    }()
    defer srv.Close()

    u.PrintInfo("Opening browser for authentication...")
    if err := openBrowser(authURL); err != nil {
        return nil, fmt.Errorf("cannot open browser, use 'login --device-login' for headless environments")
    }
    u.PrintInfo("Waiting for authorization in browser...")
    u.PrintGeneric(authURL)

    var code string
    select {
    case code = <-codeCh:
    case err := <-errCh:
        return nil, err
    case <-time.After(5 * time.Minute):
        return nil, fmt.Errorf("authentication timed out")
    }

    token, err := config.Exchange(context.Background(), code)
    if err != nil {
        return nil, fmt.Errorf("token exchange failed: %w", err)
    }
    if err := SaveToken(token); err != nil {
        return nil, err
    }
    return token, nil
}
```

Port 0 lets the operating system pick a free port, so two instances of the tool do not collide on a hardcoded one. The redirect URL is built from the port that was actually assigned.

```go
func loginWithDevice(config *oauth2.Config) (*oauth2.Token, error) {
    config.Endpoint.DeviceAuthURL = "[DEVICE_AUTH_URL]"

    da, err := config.DeviceAuth(context.Background())
    if err != nil {
        return nil, fmt.Errorf("device authorization failed: %w", err)
    }

    u.PrintInfo("To authenticate, visit the URL below and enter the code:")
    u.PrintGeneric(fmt.Sprintf("  URL:  %s", da.VerificationURI))
    u.PrintGeneric(fmt.Sprintf("  Code: %s", da.UserCode))
    u.PrintInfo("Waiting for authorization...")

    token, err := config.DeviceAccessToken(context.Background(), da)
    if err != nil {
        return nil, fmt.Errorf("device token exchange failed: %w", err)
    }
    if err := SaveToken(token); err != nil {
        return nil, err
    }
    return token, nil
}
```

`DeviceAuth` and `DeviceAccessToken` come from `golang.org/x/oauth2` and handle the polling interval and backoff, so nothing here loops on its own.

```go
func loginWithManual(config *oauth2.Config, state string) (*oauth2.Token, error) {
    config.RedirectURL = "http://localhost"
    authURL := config.AuthCodeURL(state, oauth2.AccessTypeOffline, oauth2.ApprovalForce)

    u.PrintInfo("Visit this URL to authenticate:")
    u.PrintGeneric(authURL)
    u.PrintInfo("After authorizing, copy the 'code' parameter from the redirect URL.")

    code, err := u.PromptInput("Paste the authorization code:", "4/0Axx...")
    if err != nil {
        return nil, fmt.Errorf("input error: %w", err)
    }
    if code == "" {
        return nil, fmt.Errorf("no code provided")
    }

    token, err := config.Exchange(context.Background(), extractCode(code))
    if err != nil {
        return nil, fmt.Errorf("token exchange failed: %w", err)
    }
    if err := SaveToken(token); err != nil {
        return nil, err
    }
    return token, nil
}

// extractCode accepts either a bare code or the whole redirect URL the user copied.
func extractCode(input string) string {
    if !strings.Contains(input, "code=") {
        return input
    }
    _, query, found := strings.Cut(input, "?")
    if !found {
        return input
    }
    for param := range strings.SplitSeq(query, "&") {
        if k, v, ok := strings.Cut(param, "="); ok && k == "code" {
            return v
        }
    }
    return input
}
```

`extractCode` accepts the full redirect URL because that is what a browser address bar gives the user, and asking them to isolate one query parameter by hand invites a truncated paste.

```go
func LoadToken() (*oauth2.Token, error) {
    data, err := os.ReadFile(filepath.Join(ConfigDir(), "token.json"))
    if err != nil {
        return nil, fmt.Errorf("run '[APP_NAME] login' first")
    }
    var token oauth2.Token
    if err := json.Unmarshal(data, &token); err != nil {
        return nil, fmt.Errorf("corrupt token file, run '[APP_NAME] login' again")
    }
    return &token, nil
}

func SaveToken(token *oauth2.Token) error {
    data, err := json.Marshal(token, jsontext.WithIndent("  "))
    if err != nil {
        return fmt.Errorf("failed to marshal token: %w", err)
    }
    if err := os.WriteFile(filepath.Join(ConfigDir(), "token.json"), data, 0600); err != nil {
        return fmt.Errorf("failed to save token: %w", err)
    }
    return nil
}

// GetHTTPClient is the entry point every authenticated call uses.
func GetHTTPClient() (*http.Client, error) {
    config, err := LoadCredentials()
    if err != nil {
        return nil, err
    }
    token, err := LoadToken()
    if err != nil {
        return nil, err
    }

    src := config.TokenSource(context.Background(), token)
    fresh, err := src.Token()
    if err != nil {
        return nil, fmt.Errorf("token refresh failed, run '[APP_NAME] login' again")
    }
    if fresh.AccessToken != token.AccessToken {
        if err := SaveToken(fresh); err != nil {
            return nil, err
        }
    }
    return oauth2.NewClient(context.Background(), src), nil
}

func generateState() (string, error) {
    b := make([]byte, 16)
    if _, err := rand.Read(b); err != nil {
        return "", err
    }
    return hex.EncodeToString(b), nil
}

func openBrowser(url string) error {
    var cmd *exec.Cmd
    switch runtime.GOOS {
    case "darwin":
        cmd = exec.Command("open", url)
    default:
        cmd = exec.Command("xdg-open", url)
    }
    return cmd.Run()
}
```

`GetHTTPClient` writes the token back only when the refresh actually produced a new one, so a read-only run does not rewrite the file on every invocation.

## cmd/login.go

```go
package cmd

import (
    "github.com/spf13/cobra"
    "github.com/[GITHUB_USER]/[REPO_NAME]/internal/auth"
    u "github.com/[GITHUB_USER]/[REPO_NAME]/utils"
)

var loginFlags struct {
    deviceLogin bool
    manual      bool
}

var loginCmd = &cobra.Command{
    Use:   "login",
    Short: "Authenticate with [SERVICE_NAME]",
    Run: func(cmd *cobra.Command, args []string) {
        config, err := auth.LoadCredentials()
        if err != nil {
            u.PrintFatal("failed to load credentials", err)
        }

        mode := "default"
        if loginFlags.deviceLogin {
            mode = "device"
        } else if loginFlags.manual {
            mode = "manual"
        }

        if _, err := auth.Login(config, mode); err != nil {
            u.PrintFatal("login failed", err)
        }
        u.PrintSuccess("authenticated successfully, token saved")
    },
}

func init() {
    rootCmd.AddCommand(loginCmd)

    loginCmd.Flags().BoolVar(&loginFlags.deviceLogin, "device-login", false, "Use device code flow (for headless/SSH environments)")
    loginCmd.Flags().BoolVar(&loginFlags.manual, "manual", false, "Manually paste authorization code (last resort)")
    loginCmd.MarkFlagsMutuallyExclusive("device-login", "manual")
}
```

## Placeholders

| Placeholder | Replace with |
|---|---|
| `[APP_NAME]` | the CLI tool's name, used for the config directory and error messages |
| `[REPO_NAME]` | the module path segment |
| `[SERVICE_NAME]` | the service being authenticated against |
| `[DEVICE_AUTH_URL]` | the provider's device authorization endpoint |
