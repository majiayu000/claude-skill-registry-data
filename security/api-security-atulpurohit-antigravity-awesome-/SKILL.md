---
name: api-security
description: "Harden APIs against OWASP API Top 10 vulnerabilities."
category: security
tags: [api,security,oauth,jwt,input-validation,owasp]
complexity: advanced
risk: high
compatibility: [claude-code, antigravity, gemini-cli, cursor, copilot, codex-cli, autohand, kiro]
source: antigravity-official
version: "1.0.0"
date_added: "2026-07-10"
last_updated: "2026-07-10"
---

# API Security Expert

## Purpose
Protect APIs from authentication bypasses, excessive data exposure, and injection attacks.

## Security Controls

### Object Level Authorization
```javascript
// Always verify resource ownership
router.get('/orders/:id', auth, async (req, res) => {
  const order = await Order.findOne({ _id: req.params.id, userId: req.user.id });
  if (!order) return res.status(404).json({ error: 'Not found' });
  res.json(orderSerializer.toJson(order));
});
```

### Input Validation (Zod)
```typescript
const createOrderSchema = z.object({
  items: z.array(z.object({
    productId: z.string().uuid(),
    quantity: z.int().min(1).max(100),
  })).min(1).max(50),
  shippingAddressId: z.string().uuid(),
});

router.post('/orders', auth, validate(createOrderSchema), createOrder);
```

### Rate Limiting per Route
```javascript
const strictLimit = rateLimit({ windowMs: 15 * 60 * 1000, max: 5 });
const standardLimit = rateLimit({ windowMs: 15 * 60 * 1000, max: 100 });

router.post('/auth/login', strictLimit, login);
router.post('/auth/password-reset', strictLimit, passwordReset);
router.get('/products', standardLimit, getProducts);
```

## Outputs
1. OWASP API Top 10 assessment
2. Input validation middleware
3. Authorization checks on all endpoints
4. Rate limiting configuration
5. Security audit checklist