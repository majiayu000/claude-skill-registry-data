---
name: python-settings
description: Use when a program reads configuration from its environment — writing or extending a settings class, deciding whether a field gets a default, carrying a secret, or deciding where the settings object is built and how its values reach the code that uses them. Owns one settings class per configured component, the non-strict namespace, no default on a required field or a tunable, the secret type and where it is unwrapped, derived values, validation that only normalizes or rejects, construction at the composition root, and what a library reads (nothing, when published). The prefix's name is `naming`; nothing built at import time is `python-packaging`. - Also when asked for a config class, an env var, a `.env` file, a `BaseSettings` subclass, an API key or password field, a timeout or pool-size default, `os.getenv` in a module, or where to build the settings object.
---

# Python — Settings

A program's configuration arrives from its environment, and one kind of class reads it: the settings
class. This skill owns what that class declares, which of its fields may default, how a secret travels
through it, and where the object is built. It holds in any Python program — a service of either
architecture family, a CLI tool, a library — because every one of them either reads configuration or is
handed it.

## When to use vs. neighbours

- What a settings class or its environment prefix is called, the nested-prefix collision, and the stem a
  shared library reads → `naming` (its rule 7 and **One environment prefix per settings class**).
- A settings object, client or engine built at module level → `python-packaging` rule 8, which owns
  building nothing at import time; this skill owns where the settings object is built instead.
- A field's annotation → `python-style`; keeping a secret out of a log line → `python-logging`.
- Building settings inside a test, `monkeypatch.setenv`, and dotenv files leaking into a test run →
  `test-principles`.
- Renaming an environment variable that is already deployed → `naming`'s **Renaming**; the name is a
  frozen external contract.
- Where the composition root is and how it binds settings — examples only, each in its family plugin:
  the container (`hex-wiring`, in `pyhouse-hex`) or the process definition (`flat-layered`, in
  `pyhouse-flat`). Where a settings module sits in the package is that family's layout.
- A threshold the domain itself reasons about (a maximum, a retention period) → the settings class still
  reads it; turning it into a domain value is the family's (`hex-domain-model`'s tunable, in `pyhouse-hex`).

## Template — pydantic-settings

`qux_settings.py`, the settings module of the component it configures — one component, one class, and
the module named for that class (`python-packaging`), never a bare `settings.py`:

```python
# only where the system takes a credential
from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

__all__ = ["QuxSettings"]


class QuxSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="MYAPP_QUX_",
        env_file=".env",  # only where the project keeps a dotenv file for development, never in a CLI tool
        extra="ignore",
        hide_input_in_errors=True,
    )

    url: str
    # only where the system takes a credential
    api_key: SecretStr
    timeout_seconds: float
```

Each `model_config` key is one rule: `env_prefix` is the component's namespace (rule 2), `env_file` reads
the local dotenv file where one exists and the real environment where it does not (rule 2),
`extra="ignore"` keeps the namespace non-strict (rule 2), and `hide_input_in_errors` keeps a failed
build from printing the values it was given, a secret among them (rule 7). `url` and `api_key` are
required and have no default (rules 4 and 8); `timeout_seconds` is a tunable and has none either (rule 5). `SecretStr` is
this binding's secret type and `.get_secret_value()` its unwrap (rules 7 and 9); a derived value is a
`@property` on the class (rule 10), a validator a `@field_validator` (rule 12). The module builds
nothing: the composition root calls the class — `settings = QuxSettings()` inside `main()`, or in the
container's provider method — and a missing required variable fails there (rule 13).

## Other bindings

- **Another settings library** — `environ-config`, `dynaconf`, attrs with converters. The prefix becomes
  that library's own prefix argument, the secret its secret wrapper, the validator its converter or
  validator hook. Every rule below is unchanged.
- **The standard library alone.** A frozen dataclass with a `from_env(environ: Mapping[str, str])`
  classmethod that reads only its own prefixed keys, raises naming the variable when a required one is
  missing, and wraps each secret in a small class whose `__repr__` does not print it; the composition
  root passes `os.environ` in. What the library did for free — the missing-value error, coercion, the
  non-strict namespace — becomes a few lines written once. The rules are identical.

## Rules

1. **One settings class per configured component.** An external system, a store, and the process's own
   knobs are three components and three classes; one class holding several components' fields is
   forbidden. A component with nothing to configure has no class. It declares the fields its consumer
   reads, in the form the deployment supplies them, and no others; a field copied from another
   component's class is dead configuration.
2. **Each class reads its own environment namespace, and the namespace is non-strict.** Every field is
   read under the component's own prefix — its name, and keeping it disjoint from every other prefix, are
   `naming`'s rule 7. A variable inside the namespace that the class does not declare never fails
   startup: the process environment is shared with the deployment and with every other settings class,
   so strictness turns an unrelated variable into an outage. Where the project keeps a local dotenv file
   for development, the class reads it when it is present and the real environment when it is not, so
   one class serves both without a branch. A program run from arbitrary directories — a CLI tool —
   reads no dotenv file, because whichever one sits in the working directory is not its own. A variable
   whose name a platform fixes is mapped onto the component's own name by the deployment, never read by
   an alias in code that reaches outside the namespace.
3. **Only a settings class reads the environment.** No other module reads an environment variable; code
   that needs a configured value is handed it.
4. **A required field has no default.** A missing value fails loudly when the settings object is built,
   which rule 13 puts before any work.
5. **A tunable with no single right value carries no default.** A timeout, a pool size, a batch size is
   set from what the deployment observes and can afford; a default is one deployment's tuning frozen into
   a template, and it converts a missing variable into a silent wrong answer instead of a startup failure.
   In a program its users run rather than a deployment configures — a CLI tool — a tunable may carry
   the documented default the tool ships with; a value the user picks per run is an argument (rule 15).
6. **An optional field's default is safe for production.** A value that is genuinely optional and absent
   is `None`, never a placeholder string, and the default of a switch is the side that fails safe.
7. **A value that must not appear in a log, a repr or a traceback carries a type that keeps it out of
   them** — passwords, API keys, signing secrets, connection strings with a password in them. A bare
   string is printed by every default repr in the program, so the type is what makes disclosure
   impossible rather than merely discouraged.
8. **Never default a secret the component requires.** A missing secret crashes the process at startup. A
   credential that is genuinely optional — a store that may run unauthenticated — is `None` when absent.
9. **A secret is unwrapped only at the point of use** — where the component that puts it on the wire is
   constructed: the engine, adapter or client that sends it, which then holds it privately. A derived
   value that assembles a connection string unwraps its parts only to build it, and returns it
   secret-typed again (rule 7). Where one transport client is shared by several components, each unwraps
   its own secret in its own constructor and sends it per request — a secret set on the shared transport
   rides to every upstream that transport reaches. Never into a log field, an exception's context, or an
   intermediate string built for anything else. A request URL is such a string: where the upstream accepts
   the secret anywhere else (a header), it never rides in the URL, which the client logs and prints in its
   errors. An upstream that takes it only there has that request log kept below the level the program
   emits.
10. **A value assembled from other fields is computed on the settings object, never reassembled by its
    consumers** — a connection string, a composite URL, a normalized form. One place decides how the
    parts go together, so changing the recipe is one edit rather than a search. It exists only where a
    consumer reads it: a client taking host, port and credentials as separate arguments gets those fields
    and no assembled string.
11. **Two components do not share fields by importing one settings class from another.** Each is
    self-contained; copy the field if both genuinely need it.
12. **Field validation only normalizes or rejects.** Normalization accepts an environment-friendly form
    and stores the canonical one (an escaped newline in a multi-line key); rejection refuses a value that
    would cause silent misbehaviour (an algorithm outside an allowlist). Nothing else — no IO, no
    lookups; that work belongs to the code that uses the value. The message names the variable, because
    it is read at startup.
13. **Settings are built at the program's composition root and passed down as values.** The composition
    root is the one place a program assembles its objects: a service's container or process
    definition, a CLI command's entry function, a migration environment, the test infrastructure. It
    constructs each settings class once — calling the class is enough — and hands the object, or the
    values it holds, to what it constructs. A factory function around the constructor is written only
    when it adds something the call does not, a cache (`python-packaging` rule 8) or assembly from several sources. Never at
    import time (`python-packaging` rule 8), and never below the root — owning a settings class is not
    permission for a component to build it, and a client, repository or unit of work that builds its
    own settings cannot be given different ones. A container's provider method is the composition root
    and constructs the class directly. The root builds every settings class before the program serves
    or takes work; a root that builds on first use — a container that resolves lazily — forces each
    settings class once at start, so a missing variable stops the process instead of failing the first
    operation that needs it.
14. **A published library reads no environment.** Its importer is the program with a composition root,
    so the library's constructors and functions take plain values and the importer's own settings supply
    them. A library shared inside one repository may declare a settings class under its own stem
    (`naming`); the importing program's root builds it, like any other.
15. **A value chosen per invocation is an argument, not a setting.** Settings hold what a deployment or a
    machine decides; what a caller picks each time it runs a command or calls a function is a
    command-line argument or a parameter.

## Inlined typing / import rules

- Fields are real types, and the settings library coerces the string: `port: int`, `enabled: bool`,
  `timeout_seconds: float` — never a `str` parsed later. Optional is `T | None = None`, never `T = ""`
  (`python-style`).
- Import a validator decorator only when the class defines one — an unused import is a lint failure.
- A type checker in strict mode needs the settings library's plugin, where it ships one, to accept a
  no-argument construction; `python-toolchain` configures it.
- No `from __future__ import annotations` (`python-style`).

## Package wiring

The settings module re-exports its class like any other module (`python-packaging`).

## Hard stops

- Choosing or checking an environment prefix, or renaming a deployed variable → stop, use `naming`.
- A settings object built at module level → stop, `python-packaging` rule 8 owns building nothing at
  import time; rule 13 here says where it is built instead.
- Building settings inside a test, setting variables for one, or a dotenv file leaking into a test run
  → stop, use `test-principles`.
