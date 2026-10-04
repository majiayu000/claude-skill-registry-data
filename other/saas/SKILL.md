---
name: saas
description: Software as a Service architecture
license: MIT
compatibility: opencode
metadata:
  audience: architect, developer
  category: devops
---

## What I do

- Design SaaS architectures and multi-tenancy
- Implement tenant isolation strategies
- Build metering and billing systems
- Configure identity and access for SaaS
- Optimize for multi-tenant costs
- Implement tenant onboarding flows

## When to use me

- When building SaaS products
- When implementing multi-tenancy
- When designing billing systems
- When managing tenant data isolation
- When building SaaS infrastructure
- When planning SaaS scaling

## Key Concepts

### SaaS Architecture Models

| Model | Isolation | Complexity | Cost |
|-------|-----------|------------|------|
| **Shared Everything** | Database | Low | Low |
| **Shared Database** | Schema | Medium | Medium |
| **Shared Application** | Container | Medium | Medium |
| **Isolated** | VPC/Account | High | High |

### Multi-Tenant Database Schema

```sql
-- PostgreSQL multi-tenant schema
CREATE TABLE tenants (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    subdomain VARCHAR(63) UNIQUE NOT NULL,
    plan VARCHAR(50) DEFAULT 'free',
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID REFERENCES tenants(id) ON DELETE CASCADE,
    email VARCHAR(255) NOT NULL,
    name VARCHAR(255),
    role VARCHAR(50) DEFAULT 'member',
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(tenant_id, email)
);

-- Row-level security
ALTER TABLE users ENABLE ROW LEVEL SECURITY;

CREATE POLICY "tenant_isolation" ON users
    FOR ALL
    USING (tenant_id = current_setting('app.tenant_id')::UUID);
```

### Tenant Context

```python
# FastAPI multi-tenancy
from contextvars import ContextVar
from fastapi import Request, Depends

tenant_context: ContextVar[str] = ContextVar('tenant_id', default=None)

def get_tenant_id(request: Request) -> str:
    # Extract from subdomain
    host = request.headers.get('host', '')
    subdomain = host.split('.')[0]
    
    # Or from JWT
    # token = request.headers.get('authorization')
    # tenant_id = decode_jwt(token)['tenant_id']
    
    return tenant_context.set(subdomain)

def get_current_tenant() -> Tenant:
    tenant_id = tenant_context.get()
    return Tenant.objects.get(subdomain=tenant_id)

@app.get("/api/users")
async def list_users(tenant: Tenant = Depends(get_current_tenant)):
    return User.objects.filter(tenant=tenant).all()
```

### SaaS Identity

```typescript
// OAuth2 for SaaS
const oauth2Client = new OAuth2Client(
  process.env.GOOGLE_CLIENT_ID,
  process.env.GOOGLE_CLIENT_SECRET,
  'https://yourapp.com/callback'
);

// Multi-tenant SSO
const samlConfig = {
  entryPoint: 'https://idp.example.com/sso',
  issuer: 'yourapp',
  callbackHandler: async (profile) => {
    const tenant = await findOrCreateTenant(profile.orgId);
    const user = await findOrCreateUser(profile, tenant);
    return { user, tenant };
  }
};

// Role-based access for SaaS
const permissions = {
  admin: ['*'],
  manager: ['read', 'write', 'users:read'],
  member: ['read', 'write:own'],
  viewer: ['read']
};
```

### Usage Tracking

```python
class UsageTracker:
    def track_event(self, tenant_id: str, event_type: str, metadata: dict):
        # Record usage event
        event = UsageEvent(
            tenant_id=tenant_id,
            event_type=event_type,
            metadata=metadata,
            timestamp=datetime.utcnow()
        )
        self.db.save(event)
        
        # Update meter
        meter = self.get_or_create_meter(tenant_id, event_type)
        meter.increment(metadata.get('quantity', 1))
        
    def get_usage(self, tenant_id: str, period: Period) -> UsageReport:
        events = self.db.query(UsageEvent)
            .filter(
                tenant_id=tenant_id,
                timestamp__gte=period.start,
                timestamp__lte=period.end
            )
        
        return self.aggregate_events(events)
```

### Billing Integration

```python
# Stripe SaaS billing
import stripe

stripe.api_key = os.environ['STRIPE_SECRET_KEY']

def create_customer(tenant: Tenant):
    customer = stripe.Customer.create(
        email=tenant.admin_email,
        metadata={'tenant_id': str(tenant.id)}
    )
    tenant.stripe_customer_id = customer.id
    tenant.save()
    
def create_subscription(tenant: Tenant, plan_id: str):
    subscription = stripe.Subscription.create(
        customer=tenant.stripe_customer_id,
        items=[{'price': plan_id}],
        metadata={'tenant_id': str(tenant.id)},
        trial_period_days=14
    )
    
def get_invoices(tenant: Tenant):
    return stripe.Invoice.list(
        customer=tenant.stripe_customer_id,
        limit=12
    )
```

### SaaS Best Practices

- **Tenant Isolation**: Secure data separation
- **Metered Billing**: Track usage accurately
- **Scalable Architecture**: Support growth
- **Self-Service Onboarding**: Reduce friction
- **Feature Flags**: Gradual rollouts per tenant
- **Usage Analytics**: Understand usage patterns
- **SLA Management**: Define and monitor SLAs
