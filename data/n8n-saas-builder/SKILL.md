---
name: n8n-saas-builder
description: Builds a complete SaaS frontend wrapper around validated n8n workflows. Use this skill when you want to CREATE A WEBSITE, BUILD A UI, MAKE A SAAS PRODUCT, or WRAP AN N8N WORKFLOW in a user-friendly interface. Generates Next.js/React frontends with Tailwind CSS that connect to n8n webhooks.
---

# n8n SaaS Builder

Transform any validated n8n workflow into a production-ready SaaS product. This skill analyzes your workflow's webhook inputs and automatically generates a beautiful frontend that non-technical users can interact with.

## Capabilities

- Analyze n8n workflow JSON to identify required inputs
- Generate Next.js/React frontend with Tailwind CSS
- Create responsive, modern UI with loading states
- Connect frontend to n8n webhook endpoints
- Add user authentication (optional - using Clerk)
- Deploy to Vercel with one command
- Generate mobile-friendly designs

## How to Use

1. **Validate first** - Run your workflow through n8n-workflow-validator
2. **Provide the clean JSON** - Upload the validated workflow
3. **Specify preferences** - Tell me your design preferences (optional)
4. **Get your app** - I generate the complete frontend code
5. **Deploy** - I can deploy to Vercel for you

## Input Format

- **Validated n8n JSON**: The clean workflow from the validator
- **Design preferences** (optional): Color scheme, style, branding
- **Webhook URL**: Your production n8n webhook URL (or I'll use a placeholder)

## Output Format

- **Complete Next.js project** with all files
- **Tailwind CSS styling** - Modern, responsive design
- **API integration** - Connected to your n8n webhook
- **Deployment instructions** - Ready for Vercel
- **README** - How to customize and run locally

## What Gets Generated

```
my-saas-app/
├── src/
│   ├── app/
│   │   ├── page.tsx          ← Main landing page with form
│   │   ├── layout.tsx        ← App layout and metadata
│   │   └── globals.css       ← Tailwind imports
│   └── components/
│       ├── InputForm.tsx     ← Dynamic form based on webhook inputs
│       ├── ResultCard.tsx    ← Display webhook response
│       └── LoadingSpinner.tsx
├── public/
├── package.json
├── tailwind.config.js
├── next.config.js
└── README.md
```

## Example Usage

"Build a SaaS frontend for my validated n8n workflow"

"Create a website that connects to my n8n webhook - I want it dark mode with purple accents"

"Turn this workflow into a product my clients can use without seeing n8n"

"/build-saas clean_workflow.json"

## Design Options

**Style Presets:**
- `modern` - Clean, minimal, lots of whitespace (default)
- `glassmorphism` - Frosted glass effects, dark mode
- `corporate` - Professional, trustworthy, blue tones
- `playful` - Rounded corners, gradients, friendly

**Color Schemes:**
- Default: Dark mode with purple accents
- Custom: Tell me your brand colors

## Best Practices

1. **Validate first** - Always run n8n-workflow-validator before building UI
2. **Test locally** - Run `npm run dev` to test before deploying
3. **Set your webhook URL** - Replace the placeholder with your real URL
4. **Add authentication** - For paid products, add Clerk or similar
5. **Customize branding** - Update colors/logo to match your brand

## Limitations

- Requires a validated workflow with a webhook trigger
- Complex multi-step workflows may need manual UI adjustments
- Authentication (Clerk) setup requires additional configuration
- File uploads require extra handling (base64 encoding)

## Tech Stack

- **Framework**: Next.js 14 (App Router)
- **Styling**: Tailwind CSS
- **Icons**: Lucide React
- **Deployment**: Vercel-ready
- **Optional Auth**: Clerk
