---
name: react-email
description: Creates email templates with React components using React Email. Use when building transactional emails, newsletters, or notification emails with responsive layouts and dark mode support.
---

# React Email

Build beautiful emails using React components. Handles email client inconsistencies, responsive layouts, and dark mode.

## Quick Start

```bash
npm install @react-email/components react-email
```

### Create Email Template

```tsx
// emails/welcome.tsx
import {
  Html,
  Head,
  Body,
  Container,
  Text,
  Button,
  Img,
  Section,
  Heading,
  Preview,
} from '@react-email/components';

interface WelcomeEmailProps {
  name: string;
  actionUrl: string;
}

export default function WelcomeEmail({ name, actionUrl }: WelcomeEmailProps) {
  return (
    <Html>
      <Head />
      <Preview>Welcome to our platform, {name}!</Preview>
      <Body style={main}>
        <Container style={container}>
          <Img
            src="https://example.com/logo.png"
            width="48"
            height="48"
            alt="Logo"
          />
          <Heading style={heading}>Welcome, {name}!</Heading>
          <Text style={text}>
            Thanks for signing up. Click below to get started.
          </Text>
          <Section style={buttonContainer}>
            <Button style={button} href={actionUrl}>
              Get Started
            </Button>
          </Section>
          <Text style={footer}>
            If you didn't create an account, you can ignore this email.
          </Text>
        </Container>
      </Body>
    </Html>
  );
}

const main = {
  backgroundColor: '#f6f9fc',
  fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
};

const container = {
  backgroundColor: '#ffffff',
  margin: '0 auto',
  padding: '40px 20px',
  maxWidth: '560px',
};

const heading = {
  fontSize: '24px',
  fontWeight: 'bold',
  marginTop: '32px',
};

const text = {
  fontSize: '16px',
  lineHeight: '26px',
  color: '#525252',
};

const buttonContainer = {
  textAlign: 'center' as const,
  marginTop: '32px',
};

const button = {
  backgroundColor: '#000000',
  borderRadius: '4px',
  color: '#ffffff',
  fontSize: '16px',
  fontWeight: 'bold',
  textDecoration: 'none',
  padding: '12px 24px',
  display: 'inline-block',
};

const footer = {
  fontSize: '14px',
  color: '#8898aa',
  marginTop: '32px',
};
```

### Preview Emails

```bash
npx react-email dev
```

Opens preview at `http://localhost:3000` with hot reload.

## Components

### Html, Head, Body

```tsx
import { Html, Head, Body, Font } from '@react-email/components';

<Html lang="en" dir="ltr">
  <Head>
    <Font
      fontFamily="Inter"
      fallbackFontFamily="Arial"
      webFont={{
        url: 'https://fonts.gstatic.com/s/inter/v13/...',
        format: 'woff2',
      }}
    />
  </Head>
  <Body style={{ backgroundColor: '#ffffff' }}>
    {/* content */}
  </Body>
</Html>
```

### Container & Section

```tsx
import { Container, Section, Row, Column } from '@react-email/components';

<Container style={{ maxWidth: '600px', margin: '0 auto' }}>
  <Section style={{ padding: '20px' }}>
    <Row>
      <Column style={{ width: '50%' }}>Left</Column>
      <Column style={{ width: '50%' }}>Right</Column>
    </Row>
  </Section>
</Container>
```

### Text & Headings

```tsx
import { Text, Heading } from '@react-email/components';

<Heading as="h1" style={{ fontSize: '24px' }}>
  Title
</Heading>
<Heading as="h2" style={{ fontSize: '18px' }}>
  Subtitle
</Heading>
<Text style={{ fontSize: '16px', lineHeight: '24px' }}>
  Paragraph text here.
</Text>
```

### Links & Buttons

```tsx
import { Link, Button } from '@react-email/components';

<Link href="https://example.com" style={{ color: '#0066cc' }}>
  Click here
</Link>

<Button
  href="https://example.com/action"
  style={{
    backgroundColor: '#000',
    color: '#fff',
    padding: '12px 24px',
    borderRadius: '4px',
  }}
>
  Take Action
</Button>
```

### Images

```tsx
import { Img } from '@react-email/components';

<Img
  src="https://example.com/image.jpg"
  width="600"
  height="300"
  alt="Description"
  style={{ borderRadius: '8px' }}
/>
```

### Preview Text

Hidden preview text shown in email client list view.

```tsx
import { Preview } from '@react-email/components';

<Preview>Your order has shipped! Track your package...</Preview>
```

### Dividers

```tsx
import { Hr } from '@react-email/components';

<Hr style={{ borderColor: '#e6e6e6', margin: '20px 0' }} />
```

### Code Blocks

```tsx
import { CodeBlock, CodeInline } from '@react-email/components';

<CodeInline>npm install react-email</CodeInline>

<CodeBlock
  language="javascript"
  code={`const greeting = "Hello World";`}
  theme="github-dark"
/>
```

## Tailwind CSS Support

```tsx
import { Html, Body, Container, Text, Tailwind } from '@react-email/components';

export default function Email() {
  return (
    <Html>
      <Tailwind
        config={{
          theme: {
            extend: {
              colors: {
                brand: '#007bff',
              },
            },
          },
        }}
      >
        <Body className="bg-gray-100 font-sans">
          <Container className="mx-auto max-w-xl bg-white p-8 rounded-lg">
            <Text className="text-brand text-lg font-bold">
              Hello with Tailwind!
            </Text>
          </Container>
        </Body>
      </Tailwind>
    </Html>
  );
}
```

## Render to HTML

```typescript
import { render } from '@react-email/components';
import WelcomeEmail from './emails/welcome';

// Render to HTML string
const html = await render(WelcomeEmail({ name: 'John', actionUrl: 'https://...' }));

// Render to plain text
const text = await render(WelcomeEmail({ name: 'John', actionUrl: 'https://...' }), {
  plainText: true,
});
```

## Integration with Email Providers

### With Resend

```typescript
import { Resend } from 'resend';
import { render } from '@react-email/components';
import WelcomeEmail from './emails/welcome';

const resend = new Resend(process.env.RESEND_API_KEY);

await resend.emails.send({
  from: 'hello@example.com',
  to: 'user@example.com',
  subject: 'Welcome!',
  react: WelcomeEmail({ name: 'John', actionUrl: 'https://...' }),
});
```

### With Nodemailer

```typescript
import nodemailer from 'nodemailer';
import { render } from '@react-email/components';
import WelcomeEmail from './emails/welcome';

const transporter = nodemailer.createTransport({
  host: 'smtp.example.com',
  port: 587,
  auth: {
    user: process.env.SMTP_USER,
    pass: process.env.SMTP_PASS,
  },
});

const html = await render(WelcomeEmail({ name: 'John', actionUrl: 'https://...' }));

await transporter.sendMail({
  from: 'hello@example.com',
  to: 'user@example.com',
  subject: 'Welcome!',
  html,
});
```

### With SendGrid

```typescript
import sgMail from '@sendgrid/mail';
import { render } from '@react-email/components';
import WelcomeEmail from './emails/welcome';

sgMail.setApiKey(process.env.SENDGRID_API_KEY);

const html = await render(WelcomeEmail({ name: 'John', actionUrl: 'https://...' }));

await sgMail.send({
  from: 'hello@example.com',
  to: 'user@example.com',
  subject: 'Welcome!',
  html,
});
```

## Common Email Templates

### Order Confirmation

```tsx
export default function OrderConfirmation({ orderNumber, items, total }) {
  return (
    <Html>
      <Preview>Order #{orderNumber} confirmed</Preview>
      <Body style={main}>
        <Container style={container}>
          <Heading>Order Confirmed</Heading>
          <Text>Order #{orderNumber}</Text>

          <Section style={orderTable}>
            {items.map((item) => (
              <Row key={item.id} style={tableRow}>
                <Column style={{ width: '80%' }}>
                  <Text>{item.name}</Text>
                </Column>
                <Column style={{ width: '20%', textAlign: 'right' }}>
                  <Text>${item.price}</Text>
                </Column>
              </Row>
            ))}
            <Hr />
            <Row style={tableRow}>
              <Column style={{ width: '80%' }}>
                <Text style={{ fontWeight: 'bold' }}>Total</Text>
              </Column>
              <Column style={{ width: '20%', textAlign: 'right' }}>
                <Text style={{ fontWeight: 'bold' }}>${total}</Text>
              </Column>
            </Row>
          </Section>

          <Button href={`/orders/${orderNumber}`}>
            View Order
          </Button>
        </Container>
      </Body>
    </Html>
  );
}
```

### Password Reset

```tsx
export default function PasswordReset({ resetUrl, expiresIn }) {
  return (
    <Html>
      <Preview>Reset your password</Preview>
      <Body style={main}>
        <Container style={container}>
          <Heading>Reset Your Password</Heading>
          <Text>
            Click the button below to reset your password.
            This link expires in {expiresIn}.
          </Text>
          <Button href={resetUrl}>Reset Password</Button>
          <Text style={footer}>
            If you didn't request this, you can safely ignore this email.
          </Text>
        </Container>
      </Body>
    </Html>
  );
}
```

## Dark Mode Support

```tsx
const styles = {
  body: {
    backgroundColor: '#ffffff',
    '@media (prefers-color-scheme: dark)': {
      backgroundColor: '#1a1a1a',
    },
  },
  text: {
    color: '#000000',
    '@media (prefers-color-scheme: dark)': {
      color: '#ffffff',
    },
  },
};

// Or with Tailwind
<Body className="bg-white dark:bg-gray-900">
  <Text className="text-black dark:text-white">
    Content
  </Text>
</Body>
```

## Best Practices

1. **Use inline styles** - Most email clients don't support `<style>` tags
2. **Keep width under 600px** - Standard email width
3. **Test across clients** - Gmail, Outlook, Apple Mail behave differently
4. **Provide plain text** - Some clients prefer it
5. **Use web-safe fonts** - Or provide fallbacks
6. **Include Preview component** - Improves inbox appearance
7. **Add alt text** - Images may be blocked
