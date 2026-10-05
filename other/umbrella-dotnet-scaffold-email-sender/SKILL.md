---
name: umbrella-dotnet-scaffold-email-sender
description: 'Scaffold a Razor-view-based email sender (interface, implementation, Razor views, DI registration) following the Umbrella UmbrellaRazorEmailSender pattern: core-layer interface so domain services can send email without referencing the Web layer, Web-layer implementation with view rendering, and per-domain view folder conventions.'
---

# Scaffold Email Sender

## Purpose

Add a notification email sender that renders Razor views to HTML and sends them via the app's configured `IEmailSender`. Follows the `UmbrellaRazorEmailSender` base class pattern: one sender class per notification domain (e.g. orders, invoices, account security), each exposing one strongly-typed `Send<What>Async` method per email.

The layering trick this pattern encodes: the **interface and email models live in a core-layer project** so Core.Logic services (and Web code) can trigger emails, while the **implementation lives in the Web server project** because Razor view rendering requires the ASP.NET Core view engine.

## Discovery (read these before writing anything)

1. Read 1–2 existing email senders in `Web\<AppName>.Web.Server\Services\Notifications\Email\` to confirm project-specific conventions (constructor extras such as `IOptions<MailOptions>`, exception type).
2. Find where existing email sender interfaces live — typically a core-layer `Services\Notifications\Email\Abstractions\` folder — and where their models live (`...\Models\<Domain>\`).
3. Read `Web\<AppName>.Web.Server\Views\Notifications\Email\` to confirm the shared email layout path (e.g. `~/Views/Shared/Layouts/_EmailLayout.cshtml`) and an existing `_ViewImports.cshtml`.
4. Read the `// Email` (or equivalent) section of `Web\<AppName>.Web.Server\IServiceCollectionExtensions.cs` for the registration style.
5. Identify the Web-layer exception type (e.g. `<AppName>WebServerException`).

## Step 1 -- Create the email models (core layer)

**Folder:** `<CoreProject>\Services\Notifications\Email\Models\<Domain>\`

One plain `record`/`class` per email carrying only what the view renders:

```csharp
namespace IndyRecords.Core.Common.Services.Notifications.Email.Models.Order;

public sealed record OrderConfirmationNotificationModel(string OrderNumber, DateTime OrderDate, string CustomerName);
```

No Web-layer types — these models are rendered by the view but owned by the core layer so domain services can construct them.

## Step 2 -- Create the interface (core layer)

**File:** `<CoreProject>\Services\Notifications\Email\Abstractions\I<Domain>NotificationEmailSender.cs`

```csharp
using IndyRecords.Core.Common.Services.Notifications.Email.Models.Order;

namespace IndyRecords.Core.Common.Services.Notifications.Email.Abstractions;

public interface IOrderNotificationEmailSender
{
	Task SendOrderConfirmationNotificationAsync(string email, OrderConfirmationNotificationModel model, CancellationToken cancellationToken = default);
}
```

One method per email. Every method is async with `CancellationToken cancellationToken = default` last. Methods that email a fixed/configured address (e.g. an admin inbox) omit the `email` parameter and read the address from options inside the implementation.

## Step 3 -- Create the implementation (Web server project)

**File:** `Web\<AppName>.Web.Server\Services\Notifications\Email\<Domain>NotificationEmailSender.cs`

```csharp
using IndyRecords.Core.Common.Services.Notifications.Email.Abstractions;
using IndyRecords.Core.Common.Services.Notifications.Email.Models.Order;
using Umbrella.AspNetCore.WebUtilities.Emails;
using Umbrella.AspNetCore.WebUtilities.Razor.Abstractions;
using Umbrella.Utilities.Email.Abstractions;

namespace IndyRecords.Web.Server.Services.Notifications.Email;

public class OrderNotificationEmailSender : UmbrellaRazorEmailSender, IOrderNotificationEmailSender
{
	public OrderNotificationEmailSender(
		ILogger<OrderNotificationEmailSender> logger,
		IEmailSender emailSender,
		IRazorViewToStringRenderer viewToStringRenderer)
		: base(logger, emailSender, viewToStringRenderer)
	{
	}

	public async Task SendOrderConfirmationNotificationAsync(string email, OrderConfirmationNotificationModel model, CancellationToken cancellationToken = default)
	{
		cancellationToken.ThrowIfCancellationRequested();
		Guard.IsNotNull(model);

		try
		{
			await SendEmailAsync(model, email, "Order Confirmed", "OrderConfirmationNotification", cancellationToken: cancellationToken);
		}
		catch (Exception exc) when (Logger.WriteError(exc, new { model }))
		{
			throw new IndyRecordsWebServerException("There has been a problem sending the order confirmation email.", exc);
		}
	}

	protected override string GetFullViewPath(string viewName) => $"~/Views/Notifications/Email/Order/{viewName}.cshtml";
}
```

**Rules:**

- Constructor: `ILogger<T>`, `IEmailSender`, `IRazorViewToStringRenderer` passed to `: base(...)`; extras (e.g. `IOptions<MailOptions>` for configured addresses) stored as `private readonly` fields after them.
- Every method: `ThrowIfCancellationRequested` first, `Guard` the model, try/catch with `Logger.WriteError(exc, new { model })` rethrowing the Web-layer exception type. The base `SendEmailAsync` already logs and wraps rendering/sending failures — the outer catch adds the app-specific exception type.
- `GetFullViewPath` maps a bare view name to the domain's view folder. The base class passes through paths already starting with `~`.
- **Attachments**: build `EmailAttachment` instances inside the try, send, and dispose them in a `finally` block — they hold streams.

## Step 4 -- Create the Razor views

**Folder:** `Web\<AppName>.Web.Server\Views\Notifications\Email\<Domain>\`

One `.cshtml` per email plus a `_ViewImports.cshtml` importing the models namespace:

```cshtml
@model OrderConfirmationNotificationModel

@{
	ViewData["Title"] = "Order Confirmed";
	ViewData["HiddenIntroText"] = "Order Confirmed";
	Layout = "~/Views/Shared/Layouts/_EmailLayout.cshtml";
}

<p>Your order <strong>@Model.OrderNumber</strong> placed on @Model.OrderDate.ToShortDateString() has been confirmed.</p>
```

Use the project's shared email layout; set `Title` and `HiddenIntroText` (preview text) in `ViewData`. Keep markup email-safe: inline-friendly HTML, no scripts, no external stylesheets.

If the project has no shared email layout yet, create a minimal `_EmailLayout.cshtml` under `Views\Shared\Layouts\` and flag it for design review.

## Step 5 -- Register in DI

**File:** `Web\<AppName>.Web.Server\IServiceCollectionExtensions.cs` — the `// Email` section, alphabetical order:

```csharp
_ = services.AddScoped<IOrderNotificationEmailSender, OrderNotificationEmailSender>();
```

`IRazorViewToStringRenderer` and `IEmailSender` are registered by the app's Umbrella wiring (`AddUmbrellaAspNetCoreWebUtilities` and the configured email provider) — do not re-register them.

## Analyzer compatibility

Before finishing, read `.ai-shared\bundles\umbrella\analyzer-compatibility.md` and build the affected projects with their installed analyzers enabled. Treat diagnostics introduced by the generated or changed code as defects in this workflow.

## Verification

1. Interface and models are in a core-layer project with no Web-layer `using` directives.
2. Implementation inherits `UmbrellaRazorEmailSender` and the interface, is registered with `AddScoped`.
3. `GetFullViewPath` points at the domain view folder and every view name used by a `SendEmailAsync` call has a matching `.cshtml`.
4. Views set `Layout`, `Title` and `HiddenIntroText`, and `_ViewImports.cshtml` covers the model namespace.
5. Every attachment created is disposed in a `finally` block.
6. Build the server project; Razor views compile (`RazorCompileOnBuild` projects surface view errors at build time).
