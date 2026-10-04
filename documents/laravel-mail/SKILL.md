---
model_tier: medium
name: laravel-mail
description: "Use when building Laravel emails — Mailables, Markdown templates, queued sending, attachments, previews — even when the user says 'send this as an email' without naming Mailables."
domain: engineering
workspaces:
  - engineering
packs:
  - laravel
trust:
  level: professional
install:
  default: false
  removable: true
---

# laravel-mail

## When to use

Use this skill when building email functionality:
- Mailable classes with HTML/Blade or Markdown templates
- Queued email sending
- Attachments and inline images
- Mail testing and previewing

For **simple notification emails** (one-off messages), see [laravel-notifications](../laravel-notifications/SKILL.md).
Use Mailables when you need full control over the email template.

## Procedure: Create a Mailable

1. **Inspect existing mailables** — Review `app/Mail/` for naming, base class, queueing convention, and the templates in `resources/views/emails/` for the project's markdown style.
2. **Generate class** — `php artisan make:mail InvoiceMail --markdown=emails.invoice`.
3. **Configure** — Set subject, from, attachments, queuing (`ShouldQueue`).
4. **Create template** — Markdown template in `resources/views/emails/`.
5. **Verify** — Send test email, confirm rendering and delivery.

### Example

```bash
php artisan make:mail InvoiceMail --markdown=emails.invoice
```

```php
declare(strict_types=1);

namespace App\Mail;

use App\Models\Invoice;
use Illuminate\Bus\Queueable;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Mail\Mailable;
use Illuminate\Mail\Mailables\Content;
use Illuminate\Mail\Mailables\Envelope;
use Illuminate\Queue\SerializesModels;

class InvoiceMail extends Mailable implements ShouldQueue
{
    use Queueable;
    use SerializesModels;

    public function __construct(
        private readonly Invoice $invoice,
    ) {}

    public function envelope(): Envelope
    {
        return new Envelope(
            subject: 'Invoice #' . $this->invoice->getNumber(),
            replyTo: ['billing@example.com'],
        );
    }

    public function content(): Content
    {
        return new Content(
            markdown: 'emails.invoice',
            with: [
                'invoice' => $this->invoice,
                'url' => route('invoices.show', $this->invoice->getId()),
            ],
        );
    }

    /** @return array<int, \Illuminate\Mail\Mailables\Attachment> */
    public function attachments(): array
    {
        return [
            Attachment::fromPath('/path/to/invoice.pdf')
                ->as('invoice-' . $this->invoice->getNumber() . '.pdf')
                ->withMime('application/pdf'),
        ];
    }
}
```

## Markdown templates

```blade
{{-- resources/views/emails/invoice.blade.php --}}
<x-mail::message>
# Invoice {{ $invoice->getNumber() }}

Thank you for your order. Here is your invoice summary:

<x-mail::table>
| Item | Amount |
|:-----|-------:|
@foreach ($invoice->getItems() as $item)
| {{ $item->getName() }} | {{ $item->getFormattedAmount() }} |
@endforeach
| **Total** | **{{ $invoice->getFormattedTotal() }}** |
</x-mail::table>

<x-mail::button :url="$url">
View Invoice
</x-mail::button>

Thanks,<br>
{{ config('app.name') }}
</x-mail::message>
```

## Sending mail

```php
// Send immediately
Mail::to($user)->send(new InvoiceMail($invoice));

// Queue for background sending (preferred)
Mail::to($user)->queue(new InvoiceMail($invoice));

// Send later
Mail::to($user)->later(now()->addMinutes(10), new InvoiceMail($invoice));

// Multiple recipients
Mail::to($users)
    ->cc($manager)
    ->bcc('archive@example.com')
    ->send(new InvoiceMail($invoice));
```

## Testing

```php
// Assert mail was sent
Mail::fake();

// ... trigger action ...

Mail::assertSent(InvoiceMail::class, function (InvoiceMail $mail) use ($user) {
    return $mail->hasTo($user->getEmail());
});

Mail::assertNotSent(InvoiceMail::class);
Mail::assertNothingSent();
Mail::assertQueued(InvoiceMail::class);
```

## Previewing in browser

```php
// routes/web.php (local only)
Route::get('/mail-preview', function () {
    $invoice = Invoice::factory()->create();
    return new InvoiceMail($invoice);
});
```

## Surviving the mail client

An email is not a web page. Mail clients strip, rewrite, and ignore CSS that
every browser honors, so a template that renders correctly in
`/mail-preview` tells you nothing about the inbox. Markdown templates (above)
give you a tested baseline for free — this section is what to hold to when a
design forces you off them.

**Four requirements, in order of what breaks first:**

1. **Table-based layout, not flexbox or grid.** Use nested `<table>` elements
   with `role="presentation"`, a fixed outer width of 600px, and `cellpadding`
   / `cellspacing` / `border` set to `0`. `display: flex` and
   `display: grid` are unsupported or partially supported in the Windows
   Outlook family and collapse to a single stacked column.
2. **Inline styles, not a `<style>` block.** Write `style="…"` on the element.
   A `<head><style>` block is stripped outright by some webmail clients, and
   class selectors then match nothing. Use a CSS inliner at build time if the
   template is authored with classes — never ship the classes unresolved. Keep
   a `<style>` block only for what cannot be inlined (media queries), and treat
   everything in it as optional.
3. **No web fonts, no background images, no external JS.** Declare a font stack
   ending in a system fallback; a remote font silently degrades. Background
   images require the `v:fill` VML fallback in Outlook, so put the color on
   `bgcolor` and treat the image as decoration.
4. **Explicit width and alt text on every image, and no image-only content.**
   Images are blocked by default in several clients, so an email whose call to
   action is an image is an email with no call to action.

**The client list worth testing, and what breaks in each:**

| Client | What breaks |
|---|---|
| **Outlook 2016-2019 / Windows (Word engine)** | `flex`, `grid`, `float`, `max-width`, `border-radius`, background images, `padding` on `<div>`; the strictest target — if it renders, most others do |
| **Outlook.com / Outlook 365 web** | strips `<style>` blocks in some views; rewrites `class` attributes; ignores `margin` on several elements |
| **Gmail web** | clips the message past ~102 KB of HTML with a "view entire message" link — anything below the clip, including the unsubscribe link, is not seen; strips `<style>` when the message is clipped |
| **Gmail app (iOS / Android)** | no support for embedded `<style>` on non-Gmail accounts; media queries ignored there, so the mobile layout must be the fluid default |
| **Apple Mail / iOS Mail** | the most permissive; auto-scales small text and auto-links dates and addresses unless suppressed — a false green if it is the only client you check |
| **Dark mode (Apple Mail, Outlook, Gmail)** | colors are force-inverted; a logo on a hardcoded white background becomes a white box on dark, and `#000` text on a transparent background becomes invisible |

**Verify against a real client, not a preview route.** `/mail-preview` renders in
a browser and proves none of the above. Send to real accounts, or use a
rendering service, before the template ships.

## Core rules

- **Always queue emails** — implement `ShouldQueue` to avoid blocking requests.
- **Use Markdown templates** for consistent styling across email clients.
- **Use Envelope + Content** pattern (Laravel 11+) — not the old `build()` method.
- **Test with `Mail::fake()`** — verify recipients, content, and queuing.
- **Keep Mailables focused** — one Mailable per email type.

## Output format

1. Mailable class with envelope, content, and attachments
2. Blade/Markdown email template
3. Queued mail dispatch integration

## Auto-trigger keywords

- Mailable
- email template
- send mail
- Mail::to
- markdown email
- mail attachment

## Gotcha

- Always queue emails (`ShouldQueue`) — synchronous sending blocks the request.
- The model forgets that mail templates are Blade files — they need to be published/created.
- Don't test email content with `Mail::fake()` alone — it doesn't render the template. Use `Mail::assertSent()` with closure.

## Do NOT

- Do NOT send emails synchronously in request lifecycle — always queue.
- Do NOT use `build()` method — use `envelope()`, `content()`, `attachments()`.
- Do NOT hardcode email addresses — use config or environment variables.
- Do NOT put HTML in Mailable classes — use Blade templates.
