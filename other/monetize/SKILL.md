---
name: monetize
description: Add Stripe + MyFreeScoreNow monetization to any project
---

# Monetization Integration Protocol

## Stripe Setup:
- Create products: Free, Pro ($29/mo), Enterprise ($99/mo)
- Implement checkout.session.completed webhook
- Implement subscription lifecycle webhooks
- Add customer portal for self-service

## MyFreeScoreNow Affiliate:
- Default PID: 49914 ($11/mo commission)
- Enrollment URL: https://myfreescorenow.com/enroll/?AID=RickJeffersonSolutions&PID={pid}
- Implement tracking pixel for conversions

## Revenue Dashboard:
- MRR, churn rate, LTV, CAC metrics
- Stripe + MFSN combined revenue view

## UTM parameter tracking on all marketing URLs
