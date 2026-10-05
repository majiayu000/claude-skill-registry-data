---
name: react-email
description: React Email + Resend — transactional email templates using React components.
---

# React Email + Resend Reference

> Local repo: `repos/react-email`
> Components source: `repos/react-email/packages/`
> Docs: https://react.email/docs

---

## 1. Setup

```bash
npm install @react-email/components resend
npm install -D react-email
```

### Project Structure

```
emails/
  welcome.tsx
  password-reset.tsx
  invoice.tsx
  notification.tsx
```

### Dev Server (Preview Emails)

```json
// package.json
{
  "scripts": {
    "email:dev": "email dev --dir emails --port 3030"
  }
}
```

```bash
npm run email:dev
# Opens http://localhost:3030 with live preview of all templates
```

---

## 2. Components Reference

### Core Layout Components

```typescript
import {
  Html,        // <html> wrapper — sets lang, dir
  Head,        // <head> — meta tags, title
  Preview,     // Preview text shown in inbox list (hidden in body)
  Body,        // <body> with default styles
  Container,   // Centered max-width wrapper (580px default)
  Section,     // <table> section — groups content blocks
  Row,         // <tr> table row
  Column,      // <td> table cell
} from '@react-email/components'
```

### Content Components

```typescript
import {
  Text,        // <p> paragraph
  Heading,     // <h1>-<h6>
  Link,        // <a> styled link
  Button,      // CTA button (uses <a> with padding for click area)
  Img,         // <img> with alt text
  Hr,          // <hr> divider
  CodeBlock,   // Syntax-highlighted code
  CodeInline,  // Inline code
  Markdown,    // Render markdown content
  Font,        // Load web fonts
} from '@react-email/components'
```

---

## 3. Email Templates

### Welcome Email

```typescript
// emails/welcome.tsx
import {
  Html,
  Head,
  Preview,
  Body,
  Container,
  Section,
  Text,
  Button,
  Img,
  Hr,
  Link,
} from '@react-email/components'

interface WelcomeEmailProps {
  userName: string
  loginUrl: string
}

export default function WelcomeEmail({ userName, loginUrl }: WelcomeEmailProps) {
  return (
    <Html lang="en">
      <Head />
      <Preview>Welcome to our platform, {userName}!</Preview>
      <Body style={body}>
        <Container style={container}>
          <Img
            src="https://myapp.com/logo.png"
            width={120}
            height={40}
            alt="MyApp"
            style={logo}
          />

          <Section style={section}>
            <Text style={heading}>Welcome, {userName}!</Text>
            <Text style={paragraph}>
              Thanks for signing up. We're excited to have you on board.
              Here's what you can do to get started:
            </Text>

            <ul style={list}>
              <li style={listItem}>Complete your profile</li>
              <li style={listItem}>Explore the dashboard</li>
              <li style={listItem}>Create your first project</li>
            </ul>

            <Button style={button} href={loginUrl}>
              Get Started
            </Button>
          </Section>

          <Hr style={hr} />

          <Text style={footer}>
            If you didn't create this account, you can safely ignore this email.
          </Text>
          <Text style={footer}>
            <Link href="https://myapp.com" style={footerLink}>
              MyApp
            </Link>{' '}
            · 123 Main St · San Francisco, CA 94105
          </Text>
        </Container>
      </Body>
    </Html>
  )
}

// Styles — MUST be inline objects (email clients don't support <style> or CSS classes)
const body: React.CSSProperties = {
  backgroundColor: '#f6f9fc',
  fontFamily:
    '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif',
}

const container: React.CSSProperties = {
  backgroundColor: '#ffffff',
  margin: '0 auto',
  padding: '40px 20px',
  maxWidth: '580px',
  borderRadius: '8px',
}

const logo: React.CSSProperties = {
  margin: '0 auto 24px',
  display: 'block',
}

const section: React.CSSProperties = {
  padding: '0 20px',
}

const heading: React.CSSProperties = {
  fontSize: '24px',
  fontWeight: '600',
  color: '#1a1a1a',
  margin: '0 0 16px',
}

const paragraph: React.CSSProperties = {
  fontSize: '16px',
  lineHeight: '26px',
  color: '#484848',
  margin: '0 0 16px',
}

const list: React.CSSProperties = {
  paddingLeft: '20px',
  margin: '0 0 24px',
}

const listItem: React.CSSProperties = {
  fontSize: '16px',
  lineHeight: '28px',
  color: '#484848',
}

const button: React.CSSProperties = {
  backgroundColor: '#2563eb',
  borderRadius: '6px',
  color: '#ffffff',
  fontSize: '16px',
  fontWeight: '600',
  textDecoration: 'none',
  textAlign: 'center' as const,
  display: 'block',
  width: '100%',
  padding: '12px 0',
}

const hr: React.CSSProperties = {
  borderColor: '#e6ebf1',
  margin: '32px 0',
}

const footer: React.CSSProperties = {
  color: '#8898aa',
  fontSize: '12px',
  lineHeight: '16px',
  textAlign: 'center' as const,
  margin: '0 0 8px',
}

const footerLink: React.CSSProperties = {
  color: '#8898aa',
  textDecoration: 'underline',
}

// Preview props for dev server
WelcomeEmail.PreviewProps = {
  userName: 'Jane Doe',
  loginUrl: 'https://myapp.com/login',
} satisfies WelcomeEmailProps
```

### Password Reset Email

```typescript
// emails/password-reset.tsx
import {
  Html,
  Head,
  Preview,
  Body,
  Container,
  Section,
  Text,
  Button,
  Hr,
  CodeInline,
} from '@react-email/components'

interface PasswordResetProps {
  resetUrl: string
  otp?: string
  expiresInMinutes: number
}

export default function PasswordResetEmail({
  resetUrl,
  otp,
  expiresInMinutes,
}: PasswordResetProps) {
  return (
    <Html lang="en">
      <Head />
      <Preview>Reset your password</Preview>
      <Body style={body}>
        <Container style={container}>
          <Section style={section}>
            <Text style={heading}>Password Reset</Text>
            <Text style={paragraph}>
              We received a request to reset your password. Click the button below
              to choose a new password.
            </Text>

            <Button style={button} href={resetUrl}>
              Reset Password
            </Button>

            {otp && (
              <>
                <Text style={paragraph}>
                  Or use this one-time code:
                </Text>
                <Section style={codeContainer}>
                  <CodeInline style={codeStyle}>{otp}</CodeInline>
                </Section>
              </>
            )}

            <Text style={paragraph}>
              This link expires in {expiresInMinutes} minutes. If you didn't
              request a password reset, you can safely ignore this email.
            </Text>
          </Section>

          <Hr style={hr} />
          <Text style={footer}>
            For security, this request was received from a web browser.
            If you did not request this change, no action is needed.
          </Text>
        </Container>
      </Body>
    </Html>
  )
}

const body: React.CSSProperties = {
  backgroundColor: '#f6f9fc',
  fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
}

const container: React.CSSProperties = {
  backgroundColor: '#ffffff',
  margin: '0 auto',
  padding: '40px 20px',
  maxWidth: '580px',
  borderRadius: '8px',
}

const section: React.CSSProperties = { padding: '0 20px' }

const heading: React.CSSProperties = {
  fontSize: '24px',
  fontWeight: '600',
  color: '#1a1a1a',
  margin: '0 0 16px',
}

const paragraph: React.CSSProperties = {
  fontSize: '16px',
  lineHeight: '26px',
  color: '#484848',
  margin: '0 0 16px',
}

const button: React.CSSProperties = {
  backgroundColor: '#dc2626',
  borderRadius: '6px',
  color: '#ffffff',
  fontSize: '16px',
  fontWeight: '600',
  textDecoration: 'none',
  textAlign: 'center' as const,
  display: 'block',
  width: '100%',
  padding: '12px 0',
  margin: '0 0 24px',
}

const codeContainer: React.CSSProperties = {
  background: '#f4f4f5',
  borderRadius: '6px',
  padding: '16px',
  textAlign: 'center' as const,
  margin: '0 0 24px',
}

const codeStyle: React.CSSProperties = {
  fontSize: '32px',
  fontWeight: '700',
  letterSpacing: '6px',
  color: '#1a1a1a',
}

const hr: React.CSSProperties = { borderColor: '#e6ebf1', margin: '32px 0' }
const footer: React.CSSProperties = {
  color: '#8898aa',
  fontSize: '12px',
  textAlign: 'center' as const,
}

PasswordResetEmail.PreviewProps = {
  resetUrl: 'https://myapp.com/reset?token=abc123',
  otp: '847291',
  expiresInMinutes: 15,
} satisfies PasswordResetProps
```

### Invoice Email

```typescript
// emails/invoice.tsx
import {
  Html,
  Head,
  Preview,
  Body,
  Container,
  Section,
  Row,
  Column,
  Text,
  Button,
  Hr,
} from '@react-email/components'

interface LineItem {
  description: string
  quantity: number
  unitPrice: number
}

interface InvoiceEmailProps {
  customerName: string
  invoiceNumber: string
  invoiceDate: string
  dueDate: string
  lineItems: LineItem[]
  invoiceUrl: string
}

export default function InvoiceEmail({
  customerName,
  invoiceNumber,
  invoiceDate,
  dueDate,
  lineItems,
  invoiceUrl,
}: InvoiceEmailProps) {
  const subtotal = lineItems.reduce((sum, item) => sum + item.quantity * item.unitPrice, 0)
  const tax = subtotal * 0.1
  const total = subtotal + tax

  const formatCurrency = (amount: number) =>
    new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(amount)

  return (
    <Html lang="en">
      <Head />
      <Preview>Invoice {invoiceNumber} — {formatCurrency(total)} due {dueDate}</Preview>
      <Body style={body}>
        <Container style={container}>
          <Section style={header}>
            <Row>
              <Column>
                <Text style={heading}>Invoice</Text>
              </Column>
              <Column style={{ textAlign: 'right' }}>
                <Text style={invoiceNum}>#{invoiceNumber}</Text>
              </Column>
            </Row>
          </Section>

          <Section style={section}>
            <Text style={paragraph}>Hi {customerName},</Text>
            <Text style={paragraph}>
              Here's your invoice for the current billing period.
            </Text>

            <Row>
              <Column><Text style={label}>Invoice Date</Text></Column>
              <Column><Text style={value}>{invoiceDate}</Text></Column>
            </Row>
            <Row>
              <Column><Text style={label}>Due Date</Text></Column>
              <Column><Text style={value}>{dueDate}</Text></Column>
            </Row>
          </Section>

          <Hr style={hr} />

          {/* Table header */}
          <Section style={section}>
            <Row>
              <Column style={{ width: '60%' }}>
                <Text style={tableHeader}>Description</Text>
              </Column>
              <Column style={{ width: '15%' }}>
                <Text style={tableHeader}>Qty</Text>
              </Column>
              <Column style={{ width: '25%' }}>
                <Text style={{ ...tableHeader, textAlign: 'right' }}>Amount</Text>
              </Column>
            </Row>
            <Hr style={thinHr} />

            {lineItems.map((item, i) => (
              <Row key={i}>
                <Column style={{ width: '60%' }}>
                  <Text style={cellText}>{item.description}</Text>
                </Column>
                <Column style={{ width: '15%' }}>
                  <Text style={cellText}>{item.quantity}</Text>
                </Column>
                <Column style={{ width: '25%' }}>
                  <Text style={{ ...cellText, textAlign: 'right' }}>
                    {formatCurrency(item.quantity * item.unitPrice)}
                  </Text>
                </Column>
              </Row>
            ))}

            <Hr style={thinHr} />
            <Row>
              <Column style={{ width: '75%' }}>
                <Text style={{ ...cellText, fontWeight: '600' }}>Total</Text>
              </Column>
              <Column style={{ width: '25%' }}>
                <Text style={{ ...cellText, textAlign: 'right', fontWeight: '700', fontSize: '18px' }}>
                  {formatCurrency(total)}
                </Text>
              </Column>
            </Row>
          </Section>

          <Section style={section}>
            <Button style={button} href={invoiceUrl}>
              View & Pay Invoice
            </Button>
          </Section>
        </Container>
      </Body>
    </Html>
  )
}

const body: React.CSSProperties = {
  backgroundColor: '#f6f9fc',
  fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
}
const container: React.CSSProperties = {
  backgroundColor: '#ffffff', margin: '0 auto', padding: '40px 20px', maxWidth: '580px', borderRadius: '8px',
}
const header: React.CSSProperties = { padding: '0 20px' }
const section: React.CSSProperties = { padding: '0 20px' }
const heading: React.CSSProperties = { fontSize: '28px', fontWeight: '700', color: '#1a1a1a', margin: '0' }
const invoiceNum: React.CSSProperties = { fontSize: '14px', color: '#8898aa', textAlign: 'right' as const, margin: '8px 0 0' }
const paragraph: React.CSSProperties = { fontSize: '16px', lineHeight: '26px', color: '#484848', margin: '0 0 12px' }
const label: React.CSSProperties = { fontSize: '14px', color: '#8898aa', margin: '4px 0' }
const value: React.CSSProperties = { fontSize: '14px', color: '#1a1a1a', margin: '4px 0', textAlign: 'right' as const }
const tableHeader: React.CSSProperties = { fontSize: '12px', color: '#8898aa', textTransform: 'uppercase' as const, margin: '0' }
const cellText: React.CSSProperties = { fontSize: '14px', color: '#1a1a1a', margin: '8px 0' }
const hr: React.CSSProperties = { borderColor: '#e6ebf1', margin: '24px 0' }
const thinHr: React.CSSProperties = { borderColor: '#e6ebf1', margin: '8px 0' }
const button: React.CSSProperties = {
  backgroundColor: '#2563eb', borderRadius: '6px', color: '#ffffff', fontSize: '16px',
  fontWeight: '600', textDecoration: 'none', textAlign: 'center' as const, display: 'block',
  width: '100%', padding: '12px 0', margin: '24px 0 0',
}

InvoiceEmail.PreviewProps = {
  customerName: 'Jane Doe',
  invoiceNumber: 'INV-2024-001',
  invoiceDate: 'March 1, 2024',
  dueDate: 'March 15, 2024',
  lineItems: [
    { description: 'Pro Plan — Monthly', quantity: 1, unitPrice: 29 },
    { description: 'Additional seats (3)', quantity: 3, unitPrice: 10 },
  ],
  invoiceUrl: 'https://myapp.com/invoice/INV-2024-001',
} satisfies InvoiceEmailProps
```

### Notification Email

```typescript
// emails/notification.tsx
import {
  Html,
  Head,
  Preview,
  Body,
  Container,
  Section,
  Text,
  Button,
  Hr,
} from '@react-email/components'

interface NotificationEmailProps {
  title: string
  message: string
  actionLabel?: string
  actionUrl?: string
}

export default function NotificationEmail({
  title,
  message,
  actionLabel,
  actionUrl,
}: NotificationEmailProps) {
  return (
    <Html lang="en">
      <Head />
      <Preview>{title}</Preview>
      <Body style={body}>
        <Container style={container}>
          <Section style={section}>
            <Text style={heading}>{title}</Text>
            <Text style={paragraph}>{message}</Text>

            {actionLabel && actionUrl && (
              <Button style={button} href={actionUrl}>
                {actionLabel}
              </Button>
            )}
          </Section>

          <Hr style={hr} />
          <Text style={footer}>
            You're receiving this because you have notifications enabled.
          </Text>
        </Container>
      </Body>
    </Html>
  )
}

const body: React.CSSProperties = {
  backgroundColor: '#f6f9fc',
  fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
}
const container: React.CSSProperties = {
  backgroundColor: '#ffffff', margin: '0 auto', padding: '40px 20px', maxWidth: '580px', borderRadius: '8px',
}
const section: React.CSSProperties = { padding: '0 20px' }
const heading: React.CSSProperties = { fontSize: '20px', fontWeight: '600', color: '#1a1a1a', margin: '0 0 12px' }
const paragraph: React.CSSProperties = { fontSize: '16px', lineHeight: '26px', color: '#484848', margin: '0 0 24px' }
const button: React.CSSProperties = {
  backgroundColor: '#2563eb', borderRadius: '6px', color: '#ffffff', fontSize: '16px',
  fontWeight: '600', textDecoration: 'none', textAlign: 'center' as const, display: 'block',
  width: '100%', padding: '12px 0',
}
const hr: React.CSSProperties = { borderColor: '#e6ebf1', margin: '32px 0' }
const footer: React.CSSProperties = { color: '#8898aa', fontSize: '12px', textAlign: 'center' as const }

NotificationEmail.PreviewProps = {
  title: 'New comment on your post',
  message: 'John Smith commented on "Getting Started with TypeScript": "Great article! Really helped me understand generics."',
  actionLabel: 'View Comment',
  actionUrl: 'https://myapp.com/posts/getting-started/comments',
} satisfies NotificationEmailProps
```

---

## 4. Sending with Resend

```bash
npm install resend
```

### Server-Side Send

```typescript
// lib/resend.ts
import { Resend } from 'resend'

export const resend = new Resend(process.env.RESEND_API_KEY!)
```

```typescript
// app/api/send-welcome/route.ts
import { resend } from '@/lib/resend'
import WelcomeEmail from '@/emails/welcome'
import { NextResponse } from 'next/server'

export async function POST(req: Request) {
  const { email, name } = await req.json()

  const { data, error } = await resend.emails.send({
    from: 'MyApp <hello@myapp.com>',
    to: [email],
    subject: `Welcome to MyApp, ${name}!`,
    react: WelcomeEmail({
      userName: name,
      loginUrl: 'https://myapp.com/login',
    }),
  })

  if (error) {
    return NextResponse.json({ error }, { status: 500 })
  }

  return NextResponse.json({ id: data?.id })
}
```

### Send from Server Action

```typescript
'use server'
import { resend } from '@/lib/resend'
import PasswordResetEmail from '@/emails/password-reset'

export async function sendPasswordReset(email: string, resetUrl: string) {
  await resend.emails.send({
    from: 'MyApp <security@myapp.com>',
    to: [email],
    subject: 'Reset your password',
    react: PasswordResetEmail({
      resetUrl,
      expiresInMinutes: 15,
    }),
  })
}
```

### Send from Supabase Edge Function

```typescript
// supabase/functions/send-email/index.ts
import { Resend } from 'npm:resend'

const resend = new Resend(Deno.env.get('RESEND_API_KEY')!)

Deno.serve(async (req) => {
  const { to, subject, html } = await req.json()

  const { data, error } = await resend.emails.send({
    from: 'MyApp <hello@myapp.com>',
    to: [to],
    subject,
    html, // pre-rendered HTML string
  })

  if (error) {
    return new Response(JSON.stringify({ error }), { status: 500 })
  }

  return new Response(JSON.stringify({ id: data?.id }), {
    headers: { 'Content-Type': 'application/json' },
  })
})
```

### Render to HTML String (for non-Resend providers)

```typescript
import { render } from '@react-email/components'
import WelcomeEmail from '@/emails/welcome'

const html = await render(
  WelcomeEmail({ userName: 'Jane', loginUrl: 'https://myapp.com' })
)

// Use with any email provider: SendGrid, SES, Postmark, etc.
await sendWithSES({ to: email, subject: 'Welcome!', html })
```

---

## 5. Best Practices

### Inline Styles Only

Email clients strip `<style>` tags and ignore CSS classes. All styles MUST be inline:

```typescript
// GOOD — inline style object
<Text style={{ fontSize: '16px', color: '#484848' }}>Hello</Text>

// BAD — className (won't work in email)
<Text className="text-base text-gray-600">Hello</Text>
```

### Table-Based Layout for Outlook

Outlook uses Word's HTML renderer. Use `<Section>`, `<Row>`, `<Column>` (which render as tables) for reliable layout:

```typescript
// Two-column layout that works in Outlook
<Section>
  <Row>
    <Column style={{ width: '50%', verticalAlign: 'top' }}>
      <Text>Left column</Text>
    </Column>
    <Column style={{ width: '50%', verticalAlign: 'top' }}>
      <Text>Right column</Text>
    </Column>
  </Row>
</Section>
```

### Images

- Always set `width` and `height` attributes (prevents layout shift)
- Use absolute URLs (relative paths won't resolve in email clients)
- Add meaningful `alt` text (images are blocked by default in many clients)
- Host images on a CDN, not your app server

### Testing

- Use `react-email dev` for live preview during development
- Test in real email clients: Gmail, Outlook, Apple Mail, Yahoo
- Use Resend's preview feature or Litmus/Email on Acid for cross-client testing
- Keep email width under 600px for mobile compatibility
