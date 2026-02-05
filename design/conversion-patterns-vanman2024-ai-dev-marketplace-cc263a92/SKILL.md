---
name: conversion-patterns
description: Conversion rate optimization (CRO) patterns for Next.js applications including CTA design, landing page layouts, trust signals, form optimization, pricing tables, and A/B testing. Use when building landing pages, optimizing CTAs, adding social proof, or improving conversion funnels.
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
---

# Conversion Patterns

**Purpose:** Implement proven conversion rate optimization patterns for Next.js applications to maximize signups, sales, and engagement.

**Activation Triggers:**
- Building landing pages
- Optimizing call-to-action buttons
- Adding social proof elements
- Creating pricing tables
- Implementing lead capture forms
- A/B testing setup
- Conversion tracking implementation

**Key Resources:**
- `templates/hero-section.tsx` - High-converting hero patterns
- `templates/cta-components.tsx` - CTA button variants
- `templates/pricing-table.tsx` - Pricing comparison table
- `templates/testimonials.tsx` - Social proof components
- `examples/landing-page-structure.md` - Complete landing page example

## Conversion Psychology

### Core Principles

1. **Clarity Over Cleverness** - Clear value proposition in 5 seconds
2. **Reduce Anxiety** - Trust signals, guarantees, social proof
3. **Create Urgency** - Time-limited offers, scarcity (ethical)
4. **Remove Friction** - Minimal form fields, clear CTAs

### Conversion Hierarchy

```
Attention → Interest → Desire → Action (AIDA)
     ↓          ↓         ↓        ↓
   Hero    Features   Proof     CTA
```

## Hero Section Patterns

### Pattern 1: Benefit-Focused Hero

```typescript
// components/marketing/HeroSection.tsx
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { ArrowRight, Star } from 'lucide-react'

export function HeroSection() {
  return (
    <section className="relative py-20 lg:py-32 overflow-hidden">
      {/* Background gradient */}
      <div className="absolute inset-0 bg-gradient-to-br from-primary/5 via-background to-background" />

      <div className="container mx-auto px-4 relative">
        <div className="max-w-4xl mx-auto text-center">
          {/* Social Proof Badge */}
          <Badge variant="secondary" className="mb-6">
            <Star className="h-3 w-3 mr-1 fill-yellow-500 text-yellow-500" />
            Rated #1 by 50,000+ users
          </Badge>

          {/* Main Headline - Benefit Focused */}
          <h1 className="text-4xl lg:text-6xl font-bold tracking-tight mb-6">
            Build Websites That{' '}
            <span className="text-primary">Convert</span>
          </h1>

          {/* Subheadline - How It Works */}
          <p className="text-xl text-muted-foreground mb-8 max-w-2xl mx-auto">
            AI-powered tools that help you create high-converting landing pages
            in minutes, not days. No coding required.
          </p>

          {/* CTA Buttons */}
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Button size="lg" className="text-lg px-8">
              Start Free Trial
              <ArrowRight className="ml-2 h-5 w-5" />
            </Button>
            <Button size="lg" variant="outline" className="text-lg px-8">
              Watch Demo
            </Button>
          </div>

          {/* Trust Signals */}
          <p className="mt-6 text-sm text-muted-foreground">
            ✓ No credit card required ✓ 14-day free trial ✓ Cancel anytime
          </p>
        </div>
      </div>
    </section>
  )
}
```

### Pattern 2: Problem-Agitation Hero

```typescript
export function ProblemAgitationHero() {
  return (
    <section className="py-20">
      <div className="container mx-auto px-4 text-center">
        {/* Problem Statement */}
        <p className="text-lg text-muted-foreground mb-4">
          Tired of landing pages that don't convert?
        </p>

        {/* Agitation */}
        <h1 className="text-4xl lg:text-6xl font-bold mb-6">
          Stop Losing Customers to{' '}
          <span className="text-destructive line-through">Bad Design</span>
        </h1>

        {/* Solution */}
        <p className="text-xl mb-8 max-w-2xl mx-auto">
          Our AI analyzes 100,000+ high-converting pages to build
          landing pages that actually work.
        </p>

        <Button size="lg">Get Started Free</Button>
      </div>
    </section>
  )
}
```

## CTA Component Patterns

### Primary CTA with Social Proof

```typescript
// components/marketing/CTAWithProof.tsx
interface CTAProps {
  text: string
  userCount: number
  avatars: string[]
}

export function CTAWithProof({ text, userCount, avatars }: CTAProps) {
  return (
    <div className="flex flex-col items-center gap-4">
      <Button size="lg" className="text-lg px-8 py-6">
        {text}
        <ArrowRight className="ml-2 h-5 w-5" />
      </Button>

      {/* Social Proof */}
      <div className="flex items-center gap-3">
        <div className="flex -space-x-2">
          {avatars.slice(0, 4).map((src, i) => (
            <Image
              key={i}
              src={src}
              alt=""
              width={32}
              height={32}
              className="rounded-full border-2 border-background"
            />
          ))}
        </div>
        <span className="text-sm text-muted-foreground">
          Join {userCount.toLocaleString()}+ users
        </span>
      </div>
    </div>
  )
}
```

### Sticky Mobile CTA

```typescript
// components/marketing/StickyCTA.tsx
'use client'

import { useState, useEffect } from 'react'
import { Button } from '@/components/ui/button'

export function StickyCTA({ text = 'Get Started' }) {
  const [show, setShow] = useState(false)

  useEffect(() => {
    const handleScroll = () => {
      setShow(window.scrollY > 500)
    }
    window.addEventListener('scroll', handleScroll)
    return () => window.removeEventListener('scroll', handleScroll)
  }, [])

  if (!show) return null

  return (
    <div className="fixed bottom-0 left-0 right-0 p-4 bg-background/80 backdrop-blur-sm border-t md:hidden z-50">
      <Button className="w-full" size="lg">
        {text}
      </Button>
    </div>
  )
}
```

## Pricing Table Patterns

### Three-Tier Pricing

```typescript
// components/marketing/PricingTable.tsx
const plans = [
  {
    name: 'Starter',
    price: { monthly: 29, yearly: 24 },
    description: 'Perfect for individuals',
    features: ['5 projects', '10GB storage', 'Email support'],
    cta: 'Start Free Trial',
    popular: false,
  },
  {
    name: 'Pro',
    price: { monthly: 79, yearly: 66 },
    description: 'For growing teams',
    features: [
      'Unlimited projects',
      '100GB storage',
      'Priority support',
      'Advanced analytics',
      'Custom domains',
    ],
    cta: 'Start Free Trial',
    popular: true,
  },
  {
    name: 'Enterprise',
    price: { monthly: 199, yearly: 166 },
    description: 'For large organizations',
    features: [
      'Everything in Pro',
      'Unlimited storage',
      'Dedicated support',
      'Custom integrations',
      'SLA guarantee',
      'SSO & SAML',
    ],
    cta: 'Contact Sales',
    popular: false,
  },
]

export function PricingTable() {
  const [yearly, setYearly] = useState(false)

  return (
    <section className="py-20">
      <div className="container mx-auto px-4">
        {/* Header */}
        <div className="text-center mb-12">
          <h2 className="text-3xl font-bold mb-4">
            Simple, Transparent Pricing
          </h2>
          <p className="text-muted-foreground mb-6">
            Start free. Upgrade when you need more.
          </p>

          {/* Billing Toggle */}
          <div className="flex items-center justify-center gap-3">
            <span className={cn(!yearly && 'font-medium')}>Monthly</span>
            <Switch checked={yearly} onCheckedChange={setYearly} />
            <span className={cn(yearly && 'font-medium')}>
              Yearly
              <Badge variant="secondary" className="ml-2">Save 20%</Badge>
            </span>
          </div>
        </div>

        {/* Pricing Cards */}
        <div className="grid md:grid-cols-3 gap-8 max-w-5xl mx-auto">
          {plans.map((plan) => (
            <Card
              key={plan.name}
              className={cn(
                'relative',
                plan.popular && 'border-primary shadow-lg scale-105'
              )}
            >
              {plan.popular && (
                <Badge className="absolute -top-3 left-1/2 -translate-x-1/2">
                  Most Popular
                </Badge>
              )}

              <CardHeader>
                <CardTitle>{plan.name}</CardTitle>
                <CardDescription>{plan.description}</CardDescription>
              </CardHeader>

              <CardContent>
                <div className="mb-6">
                  <span className="text-4xl font-bold">
                    ${yearly ? plan.price.yearly : plan.price.monthly}
                  </span>
                  <span className="text-muted-foreground">/month</span>
                  {yearly && (
                    <p className="text-sm text-muted-foreground">
                      billed annually
                    </p>
                  )}
                </div>

                <ul className="space-y-3">
                  {plan.features.map((feature) => (
                    <li key={feature} className="flex items-center gap-2">
                      <Check className="h-4 w-4 text-primary" />
                      <span className="text-sm">{feature}</span>
                    </li>
                  ))}
                </ul>
              </CardContent>

              <CardFooter>
                <Button
                  className="w-full"
                  variant={plan.popular ? 'default' : 'outline'}
                >
                  {plan.cta}
                </Button>
              </CardFooter>
            </Card>
          ))}
        </div>

        {/* Guarantee */}
        <p className="text-center mt-8 text-muted-foreground">
          <Shield className="inline h-4 w-4 mr-1" />
          30-day money-back guarantee. No questions asked.
        </p>
      </div>
    </section>
  )
}
```

## Social Proof Patterns

### Logo Cloud

```typescript
// components/marketing/LogoCloud.tsx
export function LogoCloud() {
  const logos = [
    { name: 'Google', src: '/logos/google.svg' },
    { name: 'Microsoft', src: '/logos/microsoft.svg' },
    { name: 'Amazon', src: '/logos/amazon.svg' },
    { name: 'Meta', src: '/logos/meta.svg' },
    { name: 'Netflix', src: '/logos/netflix.svg' },
  ]

  return (
    <section className="py-12 border-y">
      <div className="container mx-auto px-4">
        <p className="text-center text-sm text-muted-foreground mb-8">
          Trusted by teams at the world's best companies
        </p>
        <div className="flex flex-wrap justify-center items-center gap-x-12 gap-y-6">
          {logos.map((logo) => (
            <Image
              key={logo.name}
              src={logo.src}
              alt={logo.name}
              width={120}
              height={40}
              className="h-8 w-auto opacity-60 hover:opacity-100 transition-opacity"
            />
          ))}
        </div>
      </div>
    </section>
  )
}
```

### Testimonial Cards

```typescript
// components/marketing/Testimonials.tsx
interface Testimonial {
  quote: string
  author: string
  title: string
  company: string
  avatar: string
  rating: number
}

export function TestimonialCard({ testimonial }: { testimonial: Testimonial }) {
  return (
    <Card>
      <CardContent className="pt-6">
        {/* Rating */}
        <div className="flex gap-1 mb-4">
          {[...Array(5)].map((_, i) => (
            <Star
              key={i}
              className={cn(
                'h-4 w-4',
                i < testimonial.rating
                  ? 'fill-yellow-400 text-yellow-400'
                  : 'text-muted'
              )}
            />
          ))}
        </div>

        {/* Quote */}
        <p className="text-muted-foreground mb-4">
          "{testimonial.quote}"
        </p>

        {/* Author */}
        <div className="flex items-center gap-3">
          <Image
            src={testimonial.avatar}
            alt={testimonial.author}
            width={40}
            height={40}
            className="rounded-full"
          />
          <div>
            <p className="font-medium">{testimonial.author}</p>
            <p className="text-sm text-muted-foreground">
              {testimonial.title}, {testimonial.company}
            </p>
          </div>
        </div>
      </CardContent>
    </Card>
  )
}
```

## Form Optimization

### Multi-Step Lead Form

```typescript
// components/marketing/MultiStepForm.tsx
'use client'

import { useState } from 'react'

export function MultiStepForm() {
  const [step, setStep] = useState(1)
  const totalSteps = 3

  return (
    <Card className="max-w-md mx-auto">
      <CardHeader>
        <CardTitle>Get Started</CardTitle>

        {/* Progress Bar */}
        <div className="flex gap-2 mt-4">
          {[...Array(totalSteps)].map((_, i) => (
            <div
              key={i}
              className={cn(
                'h-1 flex-1 rounded',
                i < step ? 'bg-primary' : 'bg-muted'
              )}
            />
          ))}
        </div>
        <p className="text-sm text-muted-foreground">
          Step {step} of {totalSteps}
        </p>
      </CardHeader>

      <CardContent>
        {step === 1 && (
          <div className="space-y-4">
            <div>
              <Label htmlFor="email">Work Email</Label>
              <Input
                id="email"
                type="email"
                placeholder="you@company.com"
                autoFocus
              />
            </div>
            <Button onClick={() => setStep(2)} className="w-full">
              Continue
            </Button>
          </div>
        )}

        {step === 2 && (
          <div className="space-y-4">
            <div>
              <Label htmlFor="name">Full Name</Label>
              <Input id="name" placeholder="John Doe" />
            </div>
            <div>
              <Label htmlFor="company">Company</Label>
              <Input id="company" placeholder="Acme Inc" />
            </div>
            <Button onClick={() => setStep(3)} className="w-full">
              Continue
            </Button>
          </div>
        )}

        {step === 3 && (
          <div className="space-y-4">
            <div>
              <Label htmlFor="size">Team Size</Label>
              <Select>
                <SelectTrigger>
                  <SelectValue placeholder="Select team size" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="1-10">1-10</SelectItem>
                  <SelectItem value="11-50">11-50</SelectItem>
                  <SelectItem value="51-200">51-200</SelectItem>
                  <SelectItem value="200+">200+</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <Button className="w-full">
              Create Account
            </Button>
          </div>
        )}
      </CardContent>

      <CardFooter className="flex-col gap-2">
        <p className="text-xs text-muted-foreground text-center">
          By continuing, you agree to our Terms and Privacy Policy
        </p>
        <div className="flex items-center gap-2 text-sm text-muted-foreground">
          <Lock className="h-3 w-3" />
          <span>Your data is secure</span>
        </div>
      </CardFooter>
    </Card>
  )
}
```

## Urgency Patterns

### Countdown Timer

```typescript
// components/marketing/CountdownTimer.tsx
'use client'

import { useState, useEffect } from 'react'

interface CountdownProps {
  endDate: Date
  label?: string
}

export function CountdownTimer({ endDate, label = 'Offer ends in' }: CountdownProps) {
  const [timeLeft, setTimeLeft] = useState(calculateTimeLeft())

  function calculateTimeLeft() {
    const difference = +endDate - +new Date()
    if (difference <= 0) return null

    return {
      days: Math.floor(difference / (1000 * 60 * 60 * 24)),
      hours: Math.floor((difference / (1000 * 60 * 60)) % 24),
      minutes: Math.floor((difference / 1000 / 60) % 60),
      seconds: Math.floor((difference / 1000) % 60),
    }
  }

  useEffect(() => {
    const timer = setInterval(() => {
      setTimeLeft(calculateTimeLeft())
    }, 1000)
    return () => clearInterval(timer)
  }, [endDate])

  if (!timeLeft) return null

  return (
    <div className="text-center">
      <p className="text-sm text-muted-foreground mb-2">{label}</p>
      <div className="flex justify-center gap-4">
        {Object.entries(timeLeft).map(([unit, value]) => (
          <div key={unit} className="text-center">
            <div className="text-2xl font-bold tabular-nums">
              {String(value).padStart(2, '0')}
            </div>
            <div className="text-xs text-muted-foreground uppercase">
              {unit}
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
```

## A/B Testing

### Simple A/B Hook

```typescript
// hooks/useABTest.ts
'use client'

import { useEffect, useState } from 'react'

export function useABTest(testName: string): 'A' | 'B' {
  const [variant, setVariant] = useState<'A' | 'B'>('A')

  useEffect(() => {
    // Check localStorage for existing assignment
    const stored = localStorage.getItem(`ab_${testName}`)
    if (stored === 'A' || stored === 'B') {
      setVariant(stored)
      return
    }

    // Assign randomly
    const assigned = Math.random() < 0.5 ? 'A' : 'B'
    localStorage.setItem(`ab_${testName}`, assigned)
    setVariant(assigned)

    // Track assignment (GA4, etc.)
    if (typeof window.gtag !== 'undefined') {
      window.gtag('event', 'experiment_assignment', {
        experiment_name: testName,
        variant: assigned,
      })
    }
  }, [testName])

  return variant
}

// Usage
function CTASection() {
  const variant = useABTest('cta_text_2024')

  return (
    <Button>
      {variant === 'A' ? 'Start Free Trial' : 'Get Started Now'}
    </Button>
  )
}
```

## Conversion Checklist

```bash
# Run conversion audit
./scripts/conversion-audit.sh

# Checks:
# ✓ Primary CTA above fold
# ✓ CTA text is action-oriented
# ✓ Trust signals present (logos, testimonials)
# ✓ Social proof with numbers
# ✓ Form has minimal fields
# ✓ Mobile CTA visible
# ✓ Pricing has "Most Popular"
# ✓ Money-back guarantee visible
# ✓ FAQ addresses objections
```
