---
name: stripe
description: >
  Install and use the official Stripe Claude Code plugin (stripe@claude-plugins-official),
  connect Stripe MCP (mcp.stripe.com), and implement modern Stripe payments with Checkout
  Sessions, PaymentIntents, SetupIntents, and Billing — never legacy Charges. Use when
  building Stripe checkout, subscriptions, webhooks, Connect, restricted keys, test cards,
  or running /plugin install stripe@claude-plugins-official / /explain-error / /test-cards.
license: MIT
version: "1.0.0"
compatibility: >
  Claude Code with marketplace claude-plugins-official for plugin install; Stripe account
  or Stripe CLI sandbox; never commit sk_live secrets.
metadata:
  author: cheshire-terminal
  version: "1.0.0"
  homepage: https://docs.stripe.com
  plugin: stripe@claude-plugins-official
  pluginSource: https://github.com/stripe/ai/tree/main/providers/claude/plugin
  mcp: https://mcp.stripe.com
  store: https://cheshireterminal.ai/skills-store
---

# Stripe (official Claude plugin + modern APIs)

## When to use

- User asks to install Stripe for Claude: **`/plugin install stripe@claude-plugins-official`**
- Building one-time payments, subscriptions, webhooks, Connect marketplaces
- Debugging Stripe API errors or needing test card numbers
- Choosing Checkout Sessions vs PaymentIntents vs SetupIntents

## 1) Install the official plugin (Claude Code)

In Claude Code (requires marketplace **claude-plugins-official**):

```text
/plugin install stripe@claude-plugins-official
```

CLI equivalent:

```bash
claude plugin install stripe@claude-plugins-official
```

Restart Claude Code after install if components do not appear.

### What the plugin provides

| Component | Purpose |
|-----------|---------|
| **MCP server `stripe`** | HTTP MCP at `https://mcp.stripe.com` (see `.mcp.json`) |
| **`/test-cards`** | Stripe test card numbers by scenario (success, 3DS, declines) |
| **`/explain-error`** | Explain Stripe error codes + handling patterns |
| **Skills** | `stripe-best-practices`, `upgrade-stripe`, Connect recommend, projects, directory |

Official source tree: [stripe/ai → providers/claude/plugin](https://github.com/stripe/ai/tree/main/providers/claude/plugin)

### Install this store skill (agent clients)

```bash
# Single package from this repo
npx skills add ./skills-store/stripe
npx skills add Solizardking/cheshire-terminal --path skills-store/stripe

# Whole Cheshire skills store
npx skills add ./skills-store
```

## 2) Stripe MCP connection

Plugin MCP config shape:

```json
{
  "mcpServers": {
    "stripe": {
      "type": "http",
      "url": "https://mcp.stripe.com"
    }
  }
}
```

Authenticate MCP with Stripe per [Stripe MCP docs](https://docs.stripe.com/mcp). Prefer **restricted API keys** (`rk_…`) over full secret keys (`sk_…`). Never commit live secrets; use env vars / Claude secrets only.

## 3) Modern payment patterns (required)

Prefer higher-level APIs. **Never recommend the Charges API.**

| Building… | Use |
|-----------|-----|
| One-time on-session payments | **Checkout Sessions** (`checkout.sessions.create`) |
| Custom embedded UI | Checkout Sessions + **Payment Element** (`ui_mode: 'custom'` when possible) |
| Off-session / merchant-driven charge modeling | **PaymentIntents** |
| Save method for later | **SetupIntents** (not Sources/Tokens) |
| Subscriptions / recurring | Billing APIs + Checkout Sessions |
| Simple no-code | Payment Links |

Details: [references/payments.md](references/payments.md) · [references/plugin-commands.md](references/plugin-commands.md)

### Critical rules (from official best practices)

1. **Do not** use Charges API — migrate to Checkout Sessions or PaymentIntents.
2. **Do not** pass `payment_method_types` except Terminal (`card_present`) — enable dynamic payment methods.
3. Prefer **restricted keys** (`rk_`) over secret keys for agents and CI.
4. Verify **webhooks** with signing secrets; never trust client-only success UI.
5. Use latest Stripe API version / SDK unless the user pins one.

## 4) Plugin helpers

| Command / skill | When |
|-----------------|------|
| `/test-cards` | Need test PANs for success / 3DS / decline scenarios (test mode only) |
| `/explain-error` | Stripe error code or message needs plain-English fix + sample handling |
| `stripe-best-practices` skill | Architecture choices (Checkout vs PI, Connect, Billing, security) |

## 5) Secrets & safety

```bash
# Env names only in repos — never sk_live values
STRIPE_SECRET_KEY=          # prefer rk_ restricted
STRIPE_PUBLISHABLE_KEY=
STRIPE_WEBHOOK_SECRET=
```

Sandbox without full account: install Stripe CLI and use `stripe sandbox create` when appropriate.

## 6) Cheshire context

Cheshire Terminal primarily uses Solana / x402 rails. Use this skill when:

- Adding **fiat** billing (subscriptions, seats) beside crypto
- Prototyping checkout with Stripe while keeping Solana for on-chain flows
- Agents need Stripe MCP tools inside Claude Code

Do **not** replace Solana/x402 as the only payment path unless the product owner asks.

## Operating checklist

1. Install plugin: `/plugin install stripe@claude-plugins-official`
2. Confirm MCP `https://mcp.stripe.com` is connected
3. Choose Checkout Sessions / PaymentIntents / SetupIntents (not Charges)
4. Wire webhooks before going live
5. Use `/test-cards` in test mode; `/explain-error` on failures
