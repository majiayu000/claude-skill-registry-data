---
name: litestar-email
description: "Auto-activate for litestar_email, EmailPlugin, EmailConfig, EmailService, EmailMessage, InMemoryBackend, SMTPConfig, ResendConfig, SendGridConfig, MailgunConfig, or SESConfig. Not for marketing APIs — use vendor SDKs."
---

# litestar-email

`litestar-email` 0.4.0 provides one async sending interface for console, memory,
SMTP, Resend, SendGrid, Mailgun, Amazon SES, and custom backends. Match the
backend already selected by the project; keep message construction independent
from the transport.

## Code Style Rules

- Use `NamedDependency[EmailService]` for handler injection. The plugin
  registers a named Litestar dependency, not a global service singleton.
- Pass recipient collections as `list[str]`. `to`, `cc`, `bcc`, and `reply_to`
  are list fields.
- Pass attachment content as `bytes`. Do file I/O before constructing the
  message and keep that I/O async.
- Await `send_message()` and `send_messages()`. Both return the count sent.
- Keep API keys and SMTP credentials in the project's settings layer.

## Quick Reference

### Install

```bash
pip install "litestar-email>=0.4.0"
pip install "litestar-email[smtp]>=0.4.0"   # aiosmtplib
pip install "litestar-email[ses]>=0.4.0"    # botocore for SigV4
pip install "litestar-email[httpx]>=0.4.0"   # default HTTP transport
pip install "litestar-email[aiohttp]>=0.4.0" # alternative HTTP transport
```

The HTTP API backends select `httpx` by default, but the transport is optional
in `litestar-email` itself. Install the `httpx` or `aiohttp` extra (unless the
project already provides that dependency), and select `aiohttp` only when the
project standardizes on it.

### Configure the Plugin

```python
from os import environ

from litestar import Litestar
from litestar_email import EmailConfig, EmailPlugin, SMTPConfig

email_config = EmailConfig(
    backend=SMTPConfig(
        host="smtp.example.com",
        port=587,
        username=environ["SMTP_USERNAME"],
        password=environ["SMTP_PASSWORD"],
        use_tls=True,
    ),
    from_email="noreply@example.com",
    from_name="Example App",
)

app = Litestar(plugins=[EmailPlugin(config=email_config)])
```

`EmailConfig` fields:

| Field | Default | Contract |
| --- | --- | --- |
| `backend` | `"console"` | Registered name, import path, or built-in backend config object |
| `from_email` | `"noreply@localhost"` | Default sender address |
| `from_name` | `""` | Default display name |
| `fail_silently` | `False` | Backend-specific best-effort delivery behavior |
| `email_service_dependency_key` | `"mailer"` | Litestar DI key |
| `email_service_state_key` | `"mailer"` | Key holding the config in app state |

The dependency and state keys occupy separate namespaces. Change them
independently when the application already uses either key:

```python
email_config = EmailConfig(
    backend="memory",
    email_service_dependency_key="email_service",
    email_service_state_key="email_config",
)
```

### Inject `EmailService`

The handler parameter name must match `email_service_dependency_key`:

```python
from litestar import post
from litestar.di import NamedDependency
from litestar_email import EmailMessage, EmailService


@post("/notifications")
async def send_notification(
    mailer: NamedDependency[EmailService],
) -> dict[str, int]:
    sent = await mailer.send_message(
        EmailMessage(
            subject="Notification",
            body="You have a new notification.",
            to=["recipient@example.com"],
        ),
    )
    return {"sent": sent}
```

`EmailPlugin.on_app_init()` registers:

- `config.provide_service` under `email_service_dependency_key`;
- the public email types in Litestar's signature namespace;
- the `EmailConfig` instance under `email_service_state_key` in app state.

App state does not contain a permanently open `EmailService`. Use
`plugin.get_service(app.state)` or `config.get_service(app.state)` when code
outside handler DI needs a service derived from app state.

### Construct Messages

`subject` and `body` are required constructor arguments. Recipient lists have
empty-list defaults, so provide at least one delivery recipient before sending.

```python
from litestar_email import EmailMessage

message = EmailMessage(
    subject="Monthly report",
    body="The report is attached.",
    from_email="Reports <reports@example.com>",
    to=["owner@example.com"],
    cc=["audit@example.com"],
    bcc=["archive@example.com"],
    reply_to=["support@example.com"],
    headers={"X-Campaign-ID": "monthly-report"},
)
message.attach(
    filename="report.pdf",
    content=b"report content",
    mimetype="application/pdf",
)
message.attach_alternative(
    content="<p>The report is attached.</p>",
    mimetype="text/html",
)
```

`EmailMessage` does not accept `html_body` or `from_name`. Put a per-message
display name in `from_email`, as shown above. Use
`EmailMultiAlternatives.html_body` for the HTML convenience constructor:

```python
from litestar_email import EmailMultiAlternatives

message = EmailMultiAlternatives(
    subject="Welcome",
    body="Welcome to Example App.",
    to=["user@example.com"],
    html_body="<p>Welcome to <strong>Example App</strong>.</p>",
)
```

The message collections have these exact shapes:

| Field | Type |
| --- | --- |
| `to`, `cc`, `bcc`, `reply_to` | `list[str]` |
| `headers` | `dict[str, str]` |
| `attachments` | `list[tuple[str, bytes, str]]` |
| `alternatives` | `list[tuple[str, str]]` |

`recipients()` returns `to + cc + bcc`; it does not include `reply_to`.

### Pick a Backend

| Existing project constraint | Configuration | Extra |
| --- | --- | --- |
| Local output only | `backend="console"` | None |
| Unit or integration tests | `backend="memory"` | None |
| SMTP server or Mailpit | `backend=SMTPConfig(...)` | `smtp` |
| Existing Resend account | `backend=ResendConfig(...)` | `httpx` or `aiohttp` |
| Existing SendGrid account | `backend=SendGridConfig(...)` | `httpx` or `aiohttp` |
| Existing Mailgun account | `backend=MailgunConfig(...)` | `httpx` or `aiohttp` |
| Existing AWS SES setup | `backend=SESConfig(...)` | `ses` plus `httpx` or `aiohttp` |
| Project-owned backend | Registered name or backend-class import path | Project-specific |

Backend config fields:

| Config | Fields and defaults |
| --- | --- |
| `SMTPConfig` | `host="localhost"`, `port=25`, `username=None`, `password=None`, `use_tls=False`, `use_ssl=False`, `timeout=30` |
| `ResendConfig` | `api_key=""`, `timeout=30`, `http_transport="httpx"` |
| `SendGridConfig` | `api_key=""`, `timeout=30`, `http_transport="httpx"` |
| `MailgunConfig` | `api_key=""`, `domain=""`, `region="us"`, `timeout=30`, `http_transport="httpx"` |
| `SESConfig` | `region="us-east-1"`, `aws_access_key_id=None`, `aws_secret_access_key=None`, `aws_session_token=None`, `timeout=30`, `http_transport="httpx"` |

For SMTP, `use_tls=True` performs STARTTLS after connecting; `use_ssl=True`
uses implicit TLS. Select the mode required by the SMTP server.

For HTTP backends, `http_transport` accepts `"httpx"`, `"aiohttp"`, or an
`HTTPTransport` class (`from litestar_email.transports import HTTPTransport, HTTPResponse, get_transport`). Keep the default when the project has no transport preference.

For custom backends, subclass `BaseEmailBackend` and either pass its dotted
import path to `EmailConfig(backend="my_app.email.CustomBackend")` or register a
short name with `@email_backend("custom")`. Inspect registered names with
`list_backends()` and resolve classes or instances with `get_backend_class()` or
`get_backend()`. `ConsoleBackend` also accepts `stream: TextIO | None = None`
when instantiated directly.

### Amazon SES Contract

The 0.4.0 SES backend:

- calls the SES API v2 `SendEmail` endpoint with `Simple` content;
- signs the exact transmitted JSON bytes with botocore SigV4;
- uses explicit `SESConfig` credentials when both `aws_access_key_id` and
  `aws_secret_access_key` are set (with optional `aws_session_token`);
- otherwise uses botocore's default credential chain;
- supports text plus the first `text/html` alternative;
- supports `to`, `cc`, `bcc`, and the complete `reply_to` list;
- rejects attachments with `EmailDeliveryError` because `Simple` content does
  not support raw MIME attachments;
- rejects messages with neither a non-empty text body nor an HTML alternative;
- always propagates `EmailRateLimitError` and `EmailAuthenticationError`, even
  when `fail_silently=True` (all HTTP API backends — Resend, SendGrid, Mailgun,
  and SES — always propagate `EmailRateLimitError`).

Use SMTP or another attachment-capable backend when the message includes
files. Do not imply that SES 0.4.0 sends raw MIME content.

### Service Lifecycle

```python
from litestar_email import EmailConfig, EmailMessage, SMTPConfig

config = EmailConfig(
    backend=SMTPConfig(host="localhost", port=1025),
    from_email="noreply@example.com",
)

messages = [
    EmailMessage(subject="One", body="First", to=["one@example.com"]),
    EmailMessage(subject="Two", body="Second", to=["two@example.com"]),
]

async with config.provide_service() as mailer:
    sent = await mailer.send_messages(messages)
```

Outside a service context, each `send_message()` or `send_messages()` call
creates, opens, and closes a backend. Inside `config.provide_service()` or
`async with EmailService(config)`, calls reuse one open backend until context
exit. Litestar DI consumes the provider as an async iterator and performs the
same cleanup.

`send_messages([])` returns `0`. `send_message(message)` delegates to
`send_messages([message])` and returns `0` or `1`.

### Exception Hierarchy

```text
EmailError
├── EmailBackendError
├── EmailDeliveryError
│   ├── EmailConnectionError
│   ├── EmailAuthenticationError
│   └── EmailRateLimitError
└── MissingDependencyError (also inherits ImportError)
```

`EmailRateLimitError.retry_after` is `int | None`. Unknown backend names raise
`ValueError`; missing optional packages raise `MissingDependencyError`.
Catch specific delivery failures before `EmailDeliveryError`:

```python
from litestar_email import (
    EmailAuthenticationError,
    EmailConnectionError,
    EmailDeliveryError,
    EmailRateLimitError,
)

try:
    await mailer.send_message(message)
except EmailRateLimitError as exc:
    await schedule_retry(delay=exc.retry_after or 60)
except EmailAuthenticationError:
    await alert_operators("Email credentials were rejected")
except EmailConnectionError:
    await schedule_retry(delay=30)
except EmailDeliveryError:
    await record_delivery_failure()
```

### In-Memory Testing

`InMemoryBackend.outbox` is a class-level list shared by every memory backend
instance. Clear it around each test:

```python
from collections.abc import Iterator

import pytest
from litestar_email import EmailConfig, EmailMessage
from litestar_email.backends import InMemoryBackend


@pytest.fixture(autouse=True)
def clear_email_outbox() -> Iterator[None]:
    InMemoryBackend.clear()
    yield
    InMemoryBackend.clear()


@pytest.mark.anyio
async def test_welcome_email() -> None:
    config = EmailConfig(backend="memory", from_email="test@example.com")

    async with config.provide_service() as mailer:
        sent = await mailer.send_message(
            EmailMessage(
                subject="Welcome",
                body="Thanks for signing up.",
                to=["user@example.com"],
            ),
        )

    assert sent == 1
    assert len(InMemoryBackend.outbox) == 1
    assert InMemoryBackend.outbox[0].subject == "Welcome"
```

For direct backend tests, use `backend = config.get_backend()` and await
`backend.send_messages([...])`. In-memory inspection uses `InMemoryBackend.outbox`.

<workflow>

## Workflow

1. Inspect the project's existing provider, network policy, and dependency
   extras. Keep its backend unless the user asks to migrate.
2. Build one `EmailConfig` with the selected backend config and default sender.
3. Register `EmailPlugin(config=...)` and inject the configured dependency key
   with `NamedDependency[EmailService]`.
4. Construct `EmailMessage` with plain text. Add HTML through
   `attach_alternative()` or `EmailMultiAlternatives`.
5. Load attachment bytes asynchronously, then call `attach()`.
6. Reuse a service context for batches. Let Litestar DI manage request-scoped
   service cleanup in handlers.
7. Use `backend="memory"` in tests and clear `InMemoryBackend.outbox` between
   tests.
8. For slow or retryable delivery, use the queue system already present in the
   project. Choose `litestar-queues` or `litestar-saq` only when it matches the
   existing stack.

</workflow>

<guardrails>

## Guardrails

- Do not pass `html_body` to `EmailMessage`; only
  `EmailMultiAlternatives` defines that field.
- Do not pass file paths as attachments. Pass
  `(filename, content_bytes, mimetype)` or call `attach()`.
- Do not pass a string to `reply_to`; pass `list[str]`.
- Do not read app state as an open service by default. The plugin stores its
  `EmailConfig` there and derives services from it.
- Do not configure a named API backend separately from its settings. Use
  `backend=ResendConfig(...)`, `backend=SendGridConfig(...)`,
  `backend=MailgunConfig(...)`, or `backend=SESConfig(...)`.
- Do not send SES attachments. Select an attachment-capable backend.
- Do not assume `fail_silently=True` suppresses every exception. Rate-limit
  failures (`EmailRateLimitError`) on HTTP API backends and SES authentication
  failures (`EmailAuthenticationError`) always propagate.
- Do not hard-code API keys, SMTP passwords, or AWS credentials.
- Do not force a provider migration. Match the project's deployed backend and
  operational constraints.

</guardrails>

<validation>

## Validation

- [ ] `litestar-email>=0.4.0` and the selected backend extra are installed.
- [ ] `EmailPlugin(config=...)` is registered.
- [ ] The handler name matches `email_service_dependency_key`.
- [ ] Handler injection uses `NamedDependency[EmailService]`.
- [ ] `EmailMessage` supplies `subject`, `body`, and a delivery recipient.
- [ ] Attachments are byte triples and the selected backend supports them.
- [ ] HTML content is stored in `alternatives`, not passed to `EmailMessage`.
- [ ] SMTP TLS mode matches the server.
- [ ] SES messages contain no attachments and contain text or HTML.
- [ ] Batch sends reuse a managed service context.
- [ ] Tests clear and assert `InMemoryBackend.outbox`.
- [ ] Delivery exceptions are caught from most specific to least specific.
- [ ] Secrets come from the project's settings layer.

</validation>

<example>

## Example

```python
from dataclasses import dataclass
from html import escape

from litestar import Litestar, post
from litestar.di import NamedDependency
from litestar.params import JSONBody
from litestar_email import (
    EmailConfig,
    EmailMessage,
    EmailPlugin,
    EmailService,
)


@dataclass
class Notification:
    recipient: str
    subject: str
    text: str


@post("/notifications")
async def create_notification(
    data: JSONBody[Notification],
    mailer: NamedDependency[EmailService],
) -> dict[str, int]:
    message = EmailMessage(
        subject=data.subject,
        body=data.text,
        to=[data.recipient],
    )
    message.attach_alternative(
        content=f"<p>{escape(data.text)}</p>",
        mimetype="text/html",
    )
    return {"sent": await mailer.send_message(message)}


email_config = EmailConfig(
    backend="memory",
    from_email="notifications@example.com",
    from_name="Example App",
)

app = Litestar(
    route_handlers=[create_notification],
    plugins=[EmailPlugin(config=email_config)],
)
```

</example>

## References Index

- [Litestar dependency injection](../litestar/references/di-and-dishka.md)
- [Litestar settings](../litestar/references/settings.md)
- [Litestar Queues](../litestar-queues/SKILL.md)
- [Litestar SAQ](../litestar-saq/SKILL.md)
- [Litestar testing](../litestar-testing/SKILL.md)

## Official References

- [PyPI release 0.4.0](https://pypi.org/project/litestar-email/0.4.0/)
- [Message API at v0.4.0](https://github.com/litestar-org/litestar-email/blob/v0.4.0/src/litestar_email/message.py)
- [Configuration API at v0.4.0](https://github.com/litestar-org/litestar-email/blob/v0.4.0/src/litestar_email/config.py)
- [Plugin lifecycle at v0.4.0](https://github.com/litestar-org/litestar-email/blob/v0.4.0/src/litestar_email/plugin.py)
- [Service lifecycle at v0.4.0](https://github.com/litestar-org/litestar-email/blob/v0.4.0/src/litestar_email/service.py)
- [Exception hierarchy at v0.4.0](https://github.com/litestar-org/litestar-email/blob/v0.4.0/src/litestar_email/exceptions.py)
- [SES backend at v0.4.0](https://github.com/litestar-org/litestar-email/blob/v0.4.0/src/litestar_email/backends/ses.py)
- [Tagged tests at v0.4.0](https://github.com/litestar-org/litestar-email/tree/v0.4.0/src/tests)

## Shared Styleguide Baseline

- [General Principles](../litestar-styleguide/references/general.md)
- [Python](../litestar-styleguide/references/python.md)
- [Litestar](../litestar-styleguide/references/litestar.md)
