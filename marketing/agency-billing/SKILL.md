---
name: agency-billing
description: Integrate Stripe subscription billing including checkout, webhooks, usage metering, plan enforcement, and customer portal. Use when working with payments, Stripe API, subscriptions, pricing tiers, or usage limits.
---

# Social Media Agency Stripe Billing

## Subscription Plans

| Plan | Price | Clients | Posts/mo | Users | Features |
|------|-------|---------|----------|-------|----------|
| Free Trial | $0 (14 days) | 3 | 30 | 1 | Basic scheduling, AI content (limited) |
| Starter | $49/mo | 10 | 200 | 3 | Content calendar, analytics, email reports |
| Professional | $149/mo | 50 | 1,000 | 15 | Approval workflows, multi-platform, API access |
| Enterprise | $399/mo | Unlimited | Unlimited | Unlimited | Custom branding, SSO, priority support, dedicated CSM |

## Payment Flow

```
1. Agency signs up → Free trial (14 days, 3 clients, 30 posts)
2. Trial ends → Must choose plan to continue
3. Click "Upgrade" → POST /api/v1/billing/checkout
   → Creates Stripe Checkout Session
   → Redirects to Stripe-hosted payment page
4. Payment complete → Stripe sends webhook (checkout.session.completed)
5. Backend creates Subscription record, updates org plan tier
6. Monthly renewal → Stripe sends invoice.paid webhook → Reset usage counter
7. Cancel → Stripe sends customer.subscription.deleted → Downgrade to free
```

## Billing Service

```python
# src/agency/services/billing_service.py
import stripe
from agency.config import get_settings

PLAN_PRICE_IDS = {
    "starter": "price_starter_monthly",
    "professional": "price_professional_monthly",
    "enterprise": "price_enterprise_monthly",
}

PLAN_LIMITS = {
    "free": {"clients": 3, "posts": 30, "users": 1},
    "starter": {"clients": 10, "posts": 200, "users": 3},
    "professional": {"clients": 50, "posts": 1000, "users": 15},
    "enterprise": {"clients": -1, "posts": -1, "users": -1},
}

class BillingService:
    def __init__(self, db):
        self.db = db
        settings = get_settings()
        stripe.api_key = settings.stripe_secret_key

    async def create_checkout_session(self, org_id: str, plan: str, success_url: str, cancel_url: str) -> str:
        price_id = PLAN_PRICE_IDS.get(plan)
        if not price_id:
            raise ValueError(f"Unknown plan: {plan}")

        sub = await self._get_subscription(org_id)
        customer_id = sub.stripe_customer_id if sub else None

        if not customer_id:
            org = await self._get_org(org_id)
            customer = stripe.Customer.create(name=org.name, metadata={"org_id": str(org_id)})
            customer_id = customer.id
            await self._save_customer_id(org_id, customer_id)

        session = stripe.checkout.Session.create(
            customer=customer_id,
            payment_method_types=["card"],
            line_items=[{"price": price_id, "quantity": 1}],
            mode="subscription",
            success_url=success_url,
            cancel_url=cancel_url,
            metadata={"org_id": str(org_id), "plan": plan},
        )
        return session.url

    async def create_portal_session(self, org_id: str, return_url: str) -> str:
        sub = await self._get_subscription(org_id)
        if not sub or not sub.stripe_customer_id:
            raise ValueError("No active subscription")

        session = stripe.billing_portal.Session.create(
            customer=sub.stripe_customer_id,
            return_url=return_url,
        )
        return session.url

    async def check_quota(self, org_id: str) -> dict:
        sub = await self._get_subscription(org_id)
        limits = PLAN_LIMITS.get(sub.plan_tier, PLAN_LIMITS["free"])
        posts_remaining = limits["posts"] - sub.posts_used if limits["posts"] > 0 else -1

        return {
            "plan": sub.plan_tier,
            "clients_limit": limits["clients"],
            "posts_limit": limits["posts"],
            "posts_used": sub.posts_used,
            "posts_remaining": posts_remaining,
            "users_limit": limits["users"],
            "can_post": posts_remaining != 0,
        }

    async def increment_usage(self, org_id: str):
        await self.db.execute(
            "UPDATE subscription SET posts_used = posts_used + 1 WHERE org_id = :org_id",
            {"org_id": org_id},
        )
        await self.db.commit()
```

## Webhook Handler

```python
# src/agency/routers/billing.py
from fastapi import APIRouter, Request, HTTPException, status, Depends
import stripe
from agency.config import get_settings
from agency.dependencies import get_db, get_current_user, get_org_id

router = APIRouter(prefix="/billing", tags=["Billing"])

@router.post("/webhook")
async def stripe_webhook(request: Request, db=Depends(get_db)):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")
    settings = get_settings()

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.stripe_webhook_secret
        )
    except stripe.error.SignatureVerificationError:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Invalid signature")

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        org_id = session["metadata"]["org_id"]
        plan = session["metadata"]["plan"]
        subscription_id = session["subscription"]
        await _activate_subscription(db, org_id, plan, subscription_id, session["customer"])

    elif event["type"] == "invoice.paid":
        invoice = event["data"]["object"]
        customer_id = invoice["customer"]
        await _reset_monthly_usage(db, customer_id)

    elif event["type"] == "customer.subscription.deleted":
        subscription = event["data"]["object"]
        customer_id = subscription["customer"]
        await _deactivate_subscription(db, customer_id)

    return {"status": "ok"}

@router.post("/checkout")
async def create_checkout(
    request: Request,
    user=Depends(get_current_user),
    db=Depends(get_db),
    org_id=Depends(get_org_id),
):
    body = await request.json()
    service = BillingService(db)
    url = await service.create_checkout_session(
        org_id=str(org_id),
        plan=body["plan_id"],
        success_url=body.get("success_url", "http://localhost:3000/settings?billing=success"),
        cancel_url=body.get("cancel_url", "http://localhost:3000/settings?billing=cancelled"),
    )
    return {"url": url}

@router.post("/portal")
async def customer_portal(
    user=Depends(get_current_user),
    db=Depends(get_db),
    org_id=Depends(get_org_id),
):
    service = BillingService(db)
    url = await service.create_portal_session(
        org_id=str(org_id),
        return_url="http://localhost:3000/settings",
    )
    return {"url": url}

@router.get("/subscription")
async def get_subscription(
    user=Depends(get_current_user),
    db=Depends(get_db),
    org_id=Depends(get_org_id),
):
    service = BillingService(db)
    return await service.check_quota(str(org_id))
```

## Plan Enforcement

Check quota before creating content or adding clients.

```python
async def enforce_post_quota(db, org_id: str):
    service = BillingService(db)
    quota = await service.check_quota(org_id)

    if not quota["can_post"]:
        raise HTTPException(
            status.HTTP_402_PAYMENT_REQUIRED,
            f"Post quota exceeded. Used {quota['posts_used']}/{quota['posts_limit']}. Please upgrade.",
        )

async def enforce_client_limit(db, org_id: str, current_client_count: int):
    service = BillingService(db)
    quota = await service.check_quota(org_id)
    limit = quota["clients_limit"]

    if limit > 0 and current_client_count >= limit:
        raise HTTPException(
            status.HTTP_402_PAYMENT_REQUIRED,
            f"Client limit reached ({limit}). Please upgrade your plan.",
        )
```

## Frontend Pricing Component

```tsx
// components/billing/pricing-card.tsx
interface PricingCardProps {
  name: string;
  price: string;
  features: string[];
  current: boolean;
  onSelect: () => void;
}

export function PricingCard({ name, price, features, current, onSelect }: PricingCardProps) {
  return (
    <div className={cn(
      "rounded-xl border p-6",
      current ? "border-indigo-500 ring-2 ring-indigo-500" : "border-slate-200"
    )}>
      <h3 className="text-lg font-semibold">{name}</h3>
      <p className="mt-2 text-3xl font-bold">{price}<span className="text-sm text-slate-500">/mo</span></p>
      <ul className="mt-4 space-y-2">
        {features.map((f) => (
          <li key={f} className="flex items-center gap-2 text-sm text-slate-600">
            <Check className="h-4 w-4 text-emerald-500" /> {f}
          </li>
        ))}
      </ul>
      <button
        onClick={onSelect}
        disabled={current}
        className={cn(
          "mt-6 w-full rounded-lg px-4 py-2.5 font-semibold transition-colors",
          current
            ? "bg-slate-100 text-slate-400 cursor-not-allowed"
            : "bg-indigo-600 text-white hover:bg-indigo-500"
        )}
      >
        {current ? "Current Plan" : "Upgrade"}
      </button>
    </div>
  );
}
```

## Key Rules

1. **Stripe amounts are in cents** — multiply USD by 100
2. **Always verify webhook signatures** — reject unverified events
3. **Never expose Stripe secret key** — only publishable key is public
4. **Check quota before every post creation** — enforce at service layer
5. **Check client limit before adding clients** — enforce at service layer
6. **Reset usage counter monthly** — on `invoice.paid` webhook
7. **Stripe Customer Portal** for self-service plan management
8. **Free trial = 14 days, 3 clients, 30 posts** — no credit card required
9. **Usage tracking in both DB and Redis** — DB is source of truth, Redis for fast checks
