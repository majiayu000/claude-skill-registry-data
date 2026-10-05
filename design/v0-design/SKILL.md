---
name: v0-design
description: Pull V0-generated React components for building. V0 output is production-quality React/Tailwind/Shadcn code. Use when Pixel provides a V0 chatId or demo URL as the design reference.
---

# V0 Design References

## How to Use V0 Output

When Pixel provides V0 references for a build:

### Get files from a V0 chat
```bash
MCPORTER_CALL_TIMEOUT=60000 mcporter call v0.getChat chatId="CHAT_ID" --output json
```

### What V0 gives you
- `.tsx` files with React components using Shadcn UI
- Tailwind CSS classes (not raw CSS)
- Lucide icon imports
- TypeScript types
- `globals.css` with CSS custom properties

### How to use in your build
1. V0 output is 70-80% production-ready
2. Copy component structure and styling
3. Add: data fetching, state management, routing, auth guards
4. Replace hardcoded data with props/API calls
5. Add missing edge states if V0 didn't include them
6. Run through Forge review before deploy

### V0 Demo URLs
Pixel provides live preview URLs — open them to see exactly what the design looks like before building.
