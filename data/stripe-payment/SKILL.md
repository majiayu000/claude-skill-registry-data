---
name: stripe-payment
description: |
  Stripe 支付集成统一接口。支持 Checkout Session、订阅管理、Webhook 处理、
  Customer Portal、退款等功能。让 Agent 能快速实现支付功能上线。
version: 1.0.0
author: AgentFlow Team
triggers:
  - stripe
  - payment
  - 支付
  - 決済
  - checkout
  - subscription
  - 订阅
  - サブスクリプション
  - billing
  - invoice
  - refund
  - webhook
requirements:
  - stripe>=7.0.0
tags:
  - payment
  - billing
  - subscription
  - production-ready
examples:
  - "创建 Stripe Checkout Session"
  - "处理 Stripe Webhook"
  - "管理订阅"
  - "生成 Customer Portal 链接"
---

# Stripe Payment Skill

## 概述

完整的 Stripe 支付集成方案，支持一次性支付和订阅模式。

## 支持的功能

| 功能 | 说明 |
|------|------|
| **Checkout Session** | 托管结账页面，支持多种支付方式 |
| **Subscription** | 订阅管理、周期性计费 |
| **Customer Portal** | 客户自助管理订阅 |
| **Webhook** | 安全处理 Stripe 事件 |
| **Refund** | 退款处理 |
| **Invoice** | 发票管理 |

## 快速开始

### 1. 初始化

```python
from agentflow.skills.builtin.stripe_payment import StripePayment, StripeConfig

# 配置
config = StripeConfig(
    secret_key="sk_test_...",       # 或 sk_live_...
    webhook_secret="whsec_...",     # Webhook 签名密钥
    success_url="https://example.com/success",
    cancel_url="https://example.com/cancel",
)

# 初始化
stripe = StripePayment(config)
```

### 2. 创建 Checkout Session（一次性支付）

```python
# 创建结账会话
session = await stripe.create_checkout_session(
    customer_email="customer@example.com",
    line_items=[
        {
            "price_data": {
                "currency": "jpy",
                "product_data": {
                    "name": "Premium Plan",
                    "description": "プレミアムプランへのアップグレード",
                },
                "unit_amount": 9800,  # 9,800円
            },
            "quantity": 1,
        }
    ],
    mode="payment",  # 一次性支付
    metadata={"user_id": "user_123"},
)

# 返回结账 URL
print(session.url)  # 重定向用户到此 URL
```

### 3. 创建订阅 Checkout

```python
# 使用预定义的价格 ID（在 Stripe Dashboard 创建）
session = await stripe.create_checkout_session(
    customer_email="customer@example.com",
    line_items=[
        {"price": "price_xxx", "quantity": 1}  # 价格 ID
    ],
    mode="subscription",  # 订阅模式
    metadata={"user_id": "user_123"},
)
```

### 4. Customer Portal（客户自助管理）

```python
# 创建 Portal 会话
portal_url = await stripe.create_portal_session(
    customer_id="cus_xxx",
    return_url="https://example.com/account",
)

# 重定向用户到 portal_url，用户可以：
# - 查看账单历史
# - 更新支付方式
# - 取消/升级订阅
```

### 5. Webhook 处理

```python
from fastapi import FastAPI, Request, HTTPException

app = FastAPI()

@app.post("/webhooks/stripe")
async def handle_stripe_webhook(request: Request):
    body = await request.body()
    sig = request.headers.get("stripe-signature")
    
    try:
        event = stripe.verify_webhook(body, sig)
    except ValueError:
        raise HTTPException(400, "Invalid payload")
    except stripe.SignatureVerificationError:
        raise HTTPException(400, "Invalid signature")
    
    # 处理事件（带幂等性检查）
    result = await stripe.handle_webhook_event(
        event,
        handlers={
            "checkout.session.completed": handle_checkout_complete,
            "customer.subscription.updated": handle_subscription_update,
            "customer.subscription.deleted": handle_subscription_cancel,
            "invoice.payment_succeeded": handle_payment_success,
            "invoice.payment_failed": handle_payment_failed,
        }
    )
    
    return {"received": True}

async def handle_checkout_complete(event):
    session = event.data.object
    user_id = session.metadata.get("user_id")
    
    # 更新用户订阅状态
    await db.update("users", 
        {"subscription_status": "active"},
        {"id": user_id}
    )

async def handle_subscription_cancel(event):
    subscription = event.data.object
    customer_id = subscription.customer
    
    # 更新用户状态
    user = await db.select("users", {"stripe_customer_id": customer_id})
    if user:
        await db.update("users",
            {"subscription_status": "cancelled"},
            {"id": user[0]["id"]}
        )
```

## 订阅管理

### 获取订阅状态

```python
# 获取客户的所有订阅
subscriptions = await stripe.list_subscriptions(
    customer_id="cus_xxx"
)

for sub in subscriptions:
    print(f"订阅: {sub.id}")
    print(f"状态: {sub.status}")  # active, past_due, canceled, etc.
    print(f"计划: {sub.items.data[0].price.id}")
    print(f"周期结束: {sub.current_period_end}")
```

### 更新订阅

```python
# 升级/降级订阅
updated = await stripe.update_subscription(
    subscription_id="sub_xxx",
    price_id="price_new_plan",
    proration_behavior="create_prorations",  # 按比例计费
)

# 取消订阅（周期结束时）
cancelled = await stripe.cancel_subscription(
    subscription_id="sub_xxx",
    cancel_at_period_end=True,  # 周期结束时取消
)

# 立即取消
cancelled = await stripe.cancel_subscription(
    subscription_id="sub_xxx",
    cancel_at_period_end=False,  # 立即取消
)
```

### 暂停/恢复订阅

```python
# 暂停
await stripe.pause_subscription("sub_xxx")

# 恢复
await stripe.resume_subscription("sub_xxx")
```

## 退款

```python
# 全额退款
refund = await stripe.create_refund(
    payment_intent_id="pi_xxx",
)

# 部分退款
refund = await stripe.create_refund(
    payment_intent_id="pi_xxx",
    amount=5000,  # 退还 5,000円
)

# 带原因的退款
refund = await stripe.create_refund(
    payment_intent_id="pi_xxx",
    reason="requested_by_customer",  # duplicate, fraudulent, requested_by_customer
)
```

## 发票管理

```python
# 获取发票列表
invoices = await stripe.list_invoices(
    customer_id="cus_xxx",
    status="paid",  # paid, open, void, draft
)

# 获取发票 PDF 链接
for invoice in invoices:
    print(f"发票 PDF: {invoice.invoice_pdf}")

# 创建即时发票
invoice = await stripe.create_invoice(
    customer_id="cus_xxx",
    items=[
        {"price": "price_xxx", "quantity": 1}
    ],
    auto_advance=True,  # 自动发送
)
```

## 价格/产品管理

```python
# 创建产品
product = await stripe.create_product(
    name="Premium Plan",
    description="高级功能访问权限",
    metadata={"tier": "premium"},
)

# 创建价格
price = await stripe.create_price(
    product_id=product.id,
    unit_amount=9800,
    currency="jpy",
    recurring={"interval": "month"},  # 月付
)

# 列出所有活跃价格
prices = await stripe.list_prices(active=True)
```

## 幂等性处理

```python
# Webhook 事件自动去重
result = await stripe.handle_webhook_event(
    event,
    handlers={...},
    idempotency_store=db,  # 使用数据库存储已处理事件
)

# 自定义幂等性检查
@stripe.idempotent("checkout_complete")
async def handle_checkout_complete(event):
    # 即使 Webhook 重试，也只执行一次
    ...
```

## 测试模式

```python
# 测试模式配置
config = StripeConfig(
    secret_key="sk_test_...",
    webhook_secret="whsec_...",
    test_mode=True,
)

# 测试卡号
# 成功: 4242 4242 4242 4242
# 失败: 4000 0000 0000 0002
# 需要验证: 4000 0025 0000 3155

# 测试时钟（订阅测试）
test_clock = await stripe.create_test_clock(
    frozen_time=datetime.now()
)
await stripe.advance_test_clock(
    test_clock.id,
    frozen_time=datetime.now() + timedelta(days=30)
)
```

## Agent 集成示例

```python
from agentflow.skills import SkillEngine

engine = SkillEngine()

@engine.tool("create_payment")
async def create_payment(
    email: str,
    product_name: str,
    amount: int,
    currency: str = "jpy"
) -> dict:
    """创建支付链接"""
    session = await stripe.create_checkout_session(
        customer_email=email,
        line_items=[{
            "price_data": {
                "currency": currency,
                "product_data": {"name": product_name},
                "unit_amount": amount,
            },
            "quantity": 1,
        }],
        mode="payment",
    )
    return {"checkout_url": session.url}

@engine.tool("check_subscription")
async def check_subscription(customer_id: str) -> dict:
    """检查订阅状态"""
    subs = await stripe.list_subscriptions(customer_id)
    if subs:
        return {
            "status": subs[0].status,
            "plan": subs[0].items.data[0].price.id,
            "period_end": subs[0].current_period_end,
        }
    return {"status": "none"}
```

## 最佳实践

### 1. 环境变量

```python
import os

config = StripeConfig(
    secret_key=os.environ["STRIPE_SECRET_KEY"],
    webhook_secret=os.environ["STRIPE_WEBHOOK_SECRET"],
    success_url=os.environ["STRIPE_SUCCESS_URL"],
    cancel_url=os.environ["STRIPE_CANCEL_URL"],
)
```

### 2. 错误处理

```python
from agentflow.skills.builtin.stripe_payment import (
    StripeError,
    PaymentError,
    WebhookError,
    SubscriptionError,
)

try:
    session = await stripe.create_checkout_session(...)
except PaymentError as e:
    logger.error(f"支付失败: {e.message}")
    # 通知用户
except WebhookError as e:
    logger.error(f"Webhook 处理失败: {e}")
```

### 3. 订阅状态同步

```python
# 定期同步订阅状态（备份 Webhook）
async def sync_subscription_status():
    users = await db.select("users", {"stripe_customer_id__not": None})
    
    for user in users:
        subs = await stripe.list_subscriptions(user["stripe_customer_id"])
        status = subs[0].status if subs else "none"
        
        if user["subscription_status"] != status:
            await db.update("users",
                {"subscription_status": status},
                {"id": user["id"]}
            )
            logger.info(f"已同步用户 {user['id']} 的订阅状态: {status}")
```

## 价格配置建议

| 模式 | 场景 | 实现 |
|------|------|------|
| **一次性支付** | 数字产品、服务 | `mode="payment"` |
| **月付订阅** | SaaS、会员 | `mode="subscription"` + 月度价格 |
| **年付优惠** | 长期客户 | 创建年度价格，给予折扣 |
| **使用量计费** | API、存储 | Metered billing |
| **免费试用** | 获客 | `trial_period_days=14` |

