---
name: email-dev
description: Email template development with React Email and Tailwind CSS. Use when creating or modifying email templates, testing email rendering, or building email HTML from React components.
---

# Email Template Development

This skill guides the development of email templates using React Email with Tailwind CSS.

## When to use this skill

- Creating new email templates
- Modifying existing email templates
- Testing email rendering in different clients
- Debugging email template styling
- Compiling React Email to production HTML

## Quick Commands

```bash
make dev-emails    # Start React Email dev server (http://localhost:3001)
make build-emails  # Compile React Email to HTML with Jinja2 variables
```

## Development Workflow

### 1. Start Development Server

```bash
make dev-emails
```

Opens React Email preview UI at http://localhost:3001:
- Live preview of all templates
- Mobile/desktop view toggle
- Built-in Tailwind CSS support
- Auto-reload on changes

### 2. Create or Edit Templates

Templates location: `backend/emails/templates/`

**Shared Components:**
- `_BaseLayout.tsx`: Main email layout wrapper with Tailwind support
- `_Button.tsx`: Styled button component

**Example Template:**
```tsx
import { Button, Html, Text, Tailwind } from '@react-email/components';
import { BaseLayout } from './_BaseLayout';

interface WelcomeEmailProps {
  userName: string;
  loginUrl: string;
}

export const WelcomeEmail = ({ userName, loginUrl }: WelcomeEmailProps) => (
  <BaseLayout previewText="Welcome to Arive!">
    <Text className="text-lg font-semibold text-foreground mb-4">
      Hello {userName}!
    </Text>
    <Text className="text-muted-foreground mb-6">
      Thanks for joining Arive. Get started by logging in:
    </Text>
    <Button href={loginUrl} className="bg-primary text-primary-foreground">
      Log In Now
    </Button>
  </BaseLayout>
);

WelcomeEmail.PreviewProps = {
  userName: "John Doe",
  loginUrl: "https://app.tryarive.com/login",
} as WelcomeEmailProps;

export default WelcomeEmail;
```

### 3. Use Tailwind CSS Classes

The email templates support Tailwind CSS, which gets compiled to inline styles:

```tsx
<div className="bg-neutral-50 p-4 rounded-lg border border-neutral-200">
  <Text className="text-foreground font-semibold">Important Notice</Text>
  <Text className="text-muted-foreground text-sm">Details here...</Text>
</div>
```

**Available Theme Colors:**
- `text-foreground` / `bg-foreground`
- `text-background` / `bg-background`
- `text-primary` / `bg-primary`
- `text-muted` / `bg-muted`
- `text-muted-foreground`
- Full neutral gray scale: `neutral-50` through `neutral-950`

Config: `backend/emails/tailwind.config.ts`

### 4. Add Jinja2 Variables

Props in React components become Jinja2 template variables:

**React:**
```tsx
interface MyEmailProps {
  userName: string;
  confirmUrl: string;
}

export const MyEmail = ({ userName, confirmUrl }: MyEmailProps) => (
  <BaseLayout>
    <Text>Hello {userName}</Text>
    <Button href={confirmUrl}>Confirm</Button>
  </BaseLayout>
);
```

**Compiled HTML:**
```html
<p>Hello {{ userName }}</p>
<a href="{{ confirmUrl }}">Confirm</a>
```

### 5. Register Template Variables

Edit `backend/emails/scripts/build.ts`:

```typescript
const TEMPLATE_VARIABLES: Record<string, Record<string, string>> = {
  'WelcomeEmail': {
    userName: 'John Doe',
    loginUrl: 'https://app.tryarive.com/login',
  },
  'MyNewEmail': {
    userName: 'Test User',
    confirmUrl: 'https://app.tryarive.com/confirm/abc123',
  },
};
```

### 6. Build Production Templates

```bash
make build-emails
```

This compiles:
- React Email components → HTML
- Tailwind CSS classes → inline styles
- Props → Jinja2 variables
- Output: `backend/templates/emails-react/*.html.jinja2`

### 7. Use Template in Backend

Add method to `EmailService` in `backend/app/lib/email.py`:

```python
async def send_welcome_email(
    self,
    to_email: str,
    user_name: str,
    login_url: str,
) -> None:
    """Send welcome email to new user."""
    await self._send_email(
        template_name="WelcomeEmail.html.jinja2",
        to_email=to_email,
        subject="Welcome to Arive!",
        template_vars={
            "userName": user_name,
            "loginUrl": login_url,
        },
    )
```

Call from route handler:

```python
@post("/register")
async def register_user(
    data: RegisterRequest,
    email_service: EmailService,
) -> UserResponse:
    user = await create_user(data)
    await email_service.send_welcome_email(
        to_email=user.email,
        user_name=user.name,
        login_url=f"https://app.tryarive.com/login",
    )
    return user
```

## Template Structure

```
backend/emails/
├── templates/           # React Email source (.tsx)
│   ├── _BaseLayout.tsx  # Shared layout component
│   ├── _Button.tsx      # Shared button component
│   ├── WelcomeEmail.tsx # Example template
│   └── MyEmail.tsx      # Your new template
├── scripts/
│   ├── build.ts         # Build script (React → HTML)
│   └── watch.ts         # Dev server script
├── tailwind.config.ts   # Tailwind CSS config
└── package.json         # npm dependencies

backend/templates/emails-react/  # Compiled output (generated)
├── WelcomeEmail.html.jinja2
└── MyEmail.html.jinja2
```

## Design System Guidelines

### Colors
Use semantic color names that match the frontend:
- **Foreground**: Main text color (`text-foreground`)
- **Muted**: Secondary text (`text-muted-foreground`)
- **Primary**: Brand color for CTAs (`bg-primary`)
- **Neutral grays**: Backgrounds and borders (`bg-neutral-50`, `border-neutral-200`)

### Typography
```tsx
<Text className="text-2xl font-bold text-foreground">Heading</Text>
<Text className="text-base text-foreground">Body text</Text>
<Text className="text-sm text-muted-foreground">Caption</Text>
```

### Spacing
```tsx
<div className="p-6">           {/* Padding */}
<div className="mb-4">          {/* Margin bottom */}
<div className="space-y-4">     {/* Vertical spacing between children */}
```

### Layout
```tsx
<Container className="max-w-xl">  {/* Max width container */}
  <Section className="bg-neutral-50 rounded-lg p-6">
    {/* Content */}
  </Section>
</Container>
```

## Testing Email Rendering

### 1. Preview in Dev Server
- Check desktop and mobile views
- Test all interactive elements
- Verify spacing and alignment

### 2. Send Test Emails

```python
# In backend shell or test script
from app.lib.email import EmailService

email_service = EmailService()
await email_service.send_welcome_email(
    to_email="your-email@example.com",
    user_name="Test User",
    login_url="https://app.tryarive.com/login",
)
```

### 3. Email Client Testing
Test in multiple email clients:
- Gmail (web + mobile app)
- Outlook (web + desktop)
- Apple Mail (macOS + iOS)
- Others as needed

## Common Issues

### Styles not applying
- **Tailwind not compiling**: Run `make build-emails`
- **Inline styles missing**: Check Tailwind config includes all classes
- **Email client stripping styles**: Use supported CSS properties only

### Variables not rendering
- **Jinja2 syntax errors**: Check template output in `backend/templates/emails-react/`
- **Missing variables**: Verify TEMPLATE_VARIABLES in `build.ts`
- **Type mismatches**: Ensure props match template variables

### Images not loading
- **Relative paths**: Use absolute URLs for images
- **CORS issues**: Ensure image hosting allows email embedding
- **Size**: Optimize images for email (< 100KB recommended)

## Best Practices

1. **Mobile-first**: Design for mobile screens, test responsive behavior
2. **Inline styles**: Tailwind automatically inlines, but verify after build
3. **Alt text**: Always include alt text for images
4. **Preheader text**: Set via `previewText` prop in BaseLayout
5. **CTA buttons**: Make them prominent and tap-friendly (44px min height)
6. **Dark mode**: Consider email client dark mode support
7. **Accessibility**: Use semantic HTML and proper color contrast

## Production Deployment

Before deploying:
1. Run `make build-emails` to compile templates
2. Commit compiled templates in `backend/templates/emails-react/`
3. Templates are included in Docker image build
4. No Node.js runtime needed in production

Backend serves templates via Litestar's JinjaTemplateEngine at runtime.
