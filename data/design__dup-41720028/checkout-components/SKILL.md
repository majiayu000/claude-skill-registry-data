---
name: checkout-components
description: Next.js checkout UI components with Stripe Elements and payment forms. Use when creating checkout pages, payment forms, subscription UIs, customer portals, or when user mentions Stripe Elements, payment UI, checkout flow, subscription management, or payment forms.
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
---

# Checkout Components

## Purpose

Production-ready Next.js UI components for Stripe payment integration with TypeScript, Tailwind CSS, and accessibility features. Provides complete checkout flows, subscription management, and payment form components.

## Security Requirements

**CRITICAL: API Key Handling**

When using these components:

- Never hardcode Stripe publishable keys in components
- ALWAYS use environment variables: `NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY`
- Use placeholders in all examples: `pk_test_your_stripe_publishable_key_here`
- Never commit actual API keys to git
- Always add `.env` files to `.gitignore`

**Example .env.local:**
```bash
# NEVER COMMIT THIS FILE
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_test_your_stripe_publishable_key_here
STRIPE_SECRET_KEY=sk_test_your_stripe_secret_key_here
STRIPE_WEBHOOK_SECRET=whsec_your_webhook_secret_here
```

## Activation Triggers

- Creating checkout pages
- Implementing payment forms
- Building subscription management UI
- Adding customer portal components
- Integrating Stripe Elements
- Creating payment history displays
- Setting up pricing tables

## Component Overview

### Provider Components
- **StripeProvider.tsx** - Wraps app with Stripe Elements context

### Payment Components
- **CheckoutForm.tsx** - Complete checkout form with card input
- **PaymentMethodForm.tsx** - Standalone payment method input
- **SubscriptionCard.tsx** - Subscription display and management
- **PricingTable.tsx** - Pricing tier comparison table
- **PaymentHistory.tsx** - Transaction history component

## Quick Start

### 1. Install Dependencies

```bash
# Install Stripe React libraries
bash scripts/install-stripe-react.sh
```

**Installs:**
- `@stripe/stripe-js` - Stripe.js loader
- `@stripe/react-stripe-js` - React Elements components
- Type definitions for TypeScript

### 2. Setup Stripe Provider

```bash
# Create provider wrapper in your app
bash scripts/setup-stripe-provider.sh
```

**Creates:**
- `lib/stripe-client.ts` - Stripe client initialization
- `components/providers/stripe-provider.tsx` - Elements provider wrapper
- Environment variable configuration

### 3. Generate Components

```bash
# Generate specific payment component
bash scripts/generate-component.sh checkout-form
bash scripts/generate-component.sh subscription-card
bash scripts/generate-component.sh pricing-table
```

### 4. Validate Setup

```bash
# Validate component structure and configuration
bash scripts/validate-components.sh
```

**Checks:**
- Environment variables configured
- Dependencies installed
- Component structure valid
- TypeScript types correct
- Accessibility compliance

## Component Templates

### StripeProvider Template

Wraps your app with Stripe Elements context:

```typescript
import { StripeProvider } from '@/components/providers/stripe-provider';

export default function RootLayout({ children }) {
  return (
    <html>
      <body>
        <StripeProvider>
          {children}
        </StripeProvider>
      </body>
    </html>
  );
}
```

**Features:**
- Automatic Stripe.js loading
- Error boundary handling
- Loading states
- Theme customization

### CheckoutForm Template

Complete payment form with card input:

```typescript
import { CheckoutForm } from '@/components/payments/checkout-form';

export default function CheckoutPage() {
  return (
    <div className="max-w-md mx-auto p-6">
      <h1 className="text-2xl font-semibold mb-6">Complete Purchase</h1>
      <CheckoutForm
        amount={4999}
        onSuccess={() => router.push('/success')}
        onError={(error) => console.error(error)}
      />
    </div>
  );
}
```

**Features:**
- Card Element with validation
- Real-time error display
- Loading states
- Success/error callbacks
- Responsive design
- ARIA labels

### PaymentMethodForm Template

Standalone payment method collection:

```typescript
import { PaymentMethodForm } from '@/components/payments/payment-method-form';

export default function AddPaymentMethod() {
  return (
    <PaymentMethodForm
      onComplete={(paymentMethodId) => {
        console.log('Payment method created:', paymentMethodId);
      }}
      customerId="cus_xxx"
    />
  );
}
```

**Features:**
- Save cards for future use
- Update existing payment methods
- Validation and error handling
- Loading indicators

### SubscriptionCard Template

Display and manage subscriptions:

```typescript
import { SubscriptionCard } from '@/components/payments/subscription-card';

export default function SubscriptionPage() {
  return (
    <SubscriptionCard
      subscription={{
        id: 'sub_xxx',
        status: 'active',
        currentPeriodEnd: new Date('2025-12-01'),
        plan: { name: 'Pro Plan', amount: 2999 }
      }}
      onCancel={() => handleCancellation()}
      onUpdate={() => handleUpdate()}
    />
  );
}
```

**Features:**
- Status badge display
- Renewal date
- Cancel/upgrade actions
- Usage tracking
- Billing history link

### PricingTable Template

Compare pricing tiers:

```typescript
import { PricingTable } from '@/components/payments/pricing-table';

const plans = [
  {
    id: 'price_free',
    name: 'Free',
    price: 0,
    features: ['10 API calls/month', 'Basic support']
  },
  {
    id: 'price_pro',
    name: 'Pro',
    price: 2999,
    features: ['1000 API calls/month', 'Priority support', 'Advanced features']
  }
];

export default function Pricing() {
  return <PricingTable plans={plans} onSelectPlan={(planId) => handleCheckout(planId)} />;
}
```

**Features:**
- Responsive grid layout
- Feature comparison
- Call-to-action buttons
- Highlight recommended plan
- Annual/monthly toggle

### PaymentHistory Template

Display transaction history:

```typescript
import { PaymentHistory } from '@/components/payments/payment-history';

export default function BillingPage() {
  return (
    <PaymentHistory
      customerId="cus_xxx"
      limit={10}
      onLoadMore={() => loadMorePayments()}
    />
  );
}
```

**Features:**
- Paginated transaction list
- Invoice download links
- Status indicators
- Date formatting
- Search and filter

## Styling Customization

All components use Tailwind CSS and support customization:

### Element Styling

Customize Stripe Elements appearance:

```typescript
const appearance = {
  theme: 'stripe',
  variables: {
    colorPrimary: '#0070f3',
    colorBackground: '#ffffff',
    colorText: '#000000',
    colorDanger: '#df1b41',
    fontFamily: 'system-ui, sans-serif',
    spacingUnit: '4px',
    borderRadius: '4px'
  }
};

<Elements stripe={stripePromise} options={{ appearance }}>
  <CheckoutForm />
</Elements>
```

### Component Classes

Override default Tailwind classes:

```typescript
<CheckoutForm
  className="custom-checkout"
  buttonClassName="bg-blue-600 hover:bg-blue-700"
  errorClassName="text-red-600 text-sm"
/>
```

## TypeScript Types

All components include full TypeScript support:

```typescript
import type {
  CheckoutFormProps,
  PaymentMethodFormProps,
  SubscriptionCardProps,
  PricingTableProps,
  PaymentHistoryProps
} from '@/types/payments';
```

**Type Definitions:**
- Props interfaces
- Stripe object types
- Event handlers
- Error types
- Response types

## Error Handling

Components provide comprehensive error handling:

```typescript
<CheckoutForm
  onError={(error) => {
    switch (error.type) {
      case 'card_error':
        // Show user-friendly message
        toast.error(error.message);
        break;
      case 'validation_error':
        // Handle validation errors
        break;
      default:
        // Generic error handling
        console.error(error);
    }
  }}
/>
```

**Error Types:**
- Card validation errors
- Payment processing errors
- Network errors
- Configuration errors

## Accessibility Features

All components follow WCAG 2.1 AA standards:

- Proper ARIA labels
- Keyboard navigation support
- Focus management
- Screen reader friendly
- Error announcements
- Color contrast compliance

**Example:**
```typescript
<button
  type="submit"
  aria-label="Complete payment"
  aria-disabled={isProcessing}
  className="focus:ring-2 focus:ring-blue-500"
>
  {isProcessing ? 'Processing...' : 'Pay Now'}
</button>
```

## Testing

### Component Testing

```bash
# Validate all components
bash scripts/validate-components.sh

# Test specific component
bash scripts/validate-components.sh CheckoutForm
```

### Integration Testing

Use Stripe test cards:

```
4242 4242 4242 4242 - Success
4000 0000 0000 0002 - Decline
4000 0000 0000 9995 - Insufficient funds
```

## Examples

### Example 1: Complete Checkout Page

Full checkout implementation with cart summary:

```typescript
// See: examples/checkout-page-example.tsx
// Complete page with:
// - Order summary
// - Checkout form
// - Success/error handling
// - Loading states
// - Receipt generation
```

### Example 2: Subscription Management

Subscription portal with upgrade/downgrade:

```typescript
// See: examples/subscription-management-example.tsx
// Complete portal with:
// - Current plan display
// - Pricing comparison
// - Upgrade/downgrade flow
// - Cancellation handling
// - Invoice history
```

### Example 3: Payment Form Integration

Integrate payment form in multi-step flow:

```typescript
// See: examples/payment-form-integration-example.tsx
// Multi-step checkout with:
// - Shipping information
// - Payment details
// - Order confirmation
// - Progress indicator
```

## Environment Setup

Required environment variables:

```bash
# .env.local (NEVER commit this file)
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_test_your_key_here
STRIPE_SECRET_KEY=sk_test_your_key_here
STRIPE_WEBHOOK_SECRET=whsec_your_webhook_secret_here

# Optional
NEXT_PUBLIC_STRIPE_CURRENCY=usd
NEXT_PUBLIC_APP_URL=http://localhost:3000
```

Add to `.gitignore`:
```
.env.local
.env.*.local
.env
```

## Requirements

**Dependencies:**
- Next.js 13+ with App Router
- React 18+
- TypeScript 5+
- Tailwind CSS 3+
- @stripe/stripe-js
- @stripe/react-stripe-js

**Stripe Setup:**
- Stripe account (test mode works)
- Publishable key
- Secret key
- Webhook endpoint configured

## Security Best Practices

1. **Never expose secret keys client-side**
   - Only use `NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY` in components
   - Secret key stays server-side only

2. **Validate on server**
   - Always verify payments server-side
   - Use webhooks for payment confirmations
   - Never trust client-side data

3. **Use HTTPS in production**
   - Required for Stripe integration
   - Protects payment data in transit

4. **Implement CSP headers**
   - Allow Stripe.js domain
   - Restrict other script sources

5. **Handle PCI compliance**
   - Never store card numbers
   - Use Stripe Elements (SAQ A compliant)
   - Let Stripe handle card data

## Troubleshooting

### Stripe.js Not Loading

Check environment variable:
```bash
echo $NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY
```

Verify format starts with `pk_test_` or `pk_live_`

### Payment Intent Creation Fails

Ensure server-side API route exists:
```typescript
// app/api/create-payment-intent/route.ts
import { stripe } from '@/lib/stripe-server';

export async function POST(req: Request) {
  const { amount } = await req.json();

  const paymentIntent = await stripe.paymentIntents.create({
    amount,
    currency: 'usd',
  });

  return Response.json({ clientSecret: paymentIntent.client_secret });
}
```

### Component Not Rendering

Verify StripeProvider wraps component:
```typescript
// Must be wrapped
<StripeProvider>
  <CheckoutForm />
</StripeProvider>
```

## Resources

**Scripts:**
- `scripts/install-stripe-react.sh` - Install dependencies
- `scripts/setup-stripe-provider.sh` - Configure provider
- `scripts/generate-component.sh` - Generate new components
- `scripts/validate-components.sh` - Validate setup

**Templates:**
- `templates/StripeProvider.tsx` - Provider wrapper
- `templates/CheckoutForm.tsx` - Checkout form
- `templates/PaymentMethodForm.tsx` - Payment method input
- `templates/SubscriptionCard.tsx` - Subscription display
- `templates/PricingTable.tsx` - Pricing comparison
- `templates/PaymentHistory.tsx` - Transaction history

**Examples:**
- `examples/checkout-page-example.tsx` - Complete checkout
- `examples/subscription-management-example.tsx` - Subscription UI
- `examples/payment-form-integration-example.tsx` - Multi-step flow

---

**Plugin:** payments
**Version:** 1.0.0
**Category:** UI Components
**Framework:** Next.js + Stripe Elements
