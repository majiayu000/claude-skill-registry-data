---
name: Supabase Frontend Integration
description: Connect React frontend pages to Supabase database with TypeScript, React Query, and proper error handling. Use when integrating Supabase with website pages, setting up database queries, or replacing mock data with real data from events, bookings, menu_items, or profiles tables.
---

# Supabase Frontend Integration

## Quick start

Connect a page to Supabase in three steps:

1. **Create hook**: Write React Query hook for data fetching
2. **Update component**: Replace mock data with hook
3. **Add states**: Handle loading, error, and empty states

## File structure

```
src/
├── lib/
│   ├── supabase.ts           # Client config (already exists)
│   └── formatters.ts          # Date/time helpers
├── hooks/
│   ├── useEvents.ts           # Events queries
│   ├── useBookings.ts         # Booking mutations
│   └── useMenu.ts             # Menu queries
└── pages/
    ├── Index.tsx              # Home page
    ├── Schedule.tsx           # Events list
    ├── Menu.tsx               # Menu items
    └── Reserve.tsx            # Create bookings
```

## Database tables reference

See [TABLES.md](TABLES.md) for complete schema with field names and types.

## Common patterns

### Pattern 1: Fetch list of items

**Use for**: Events page, menu page, customer list

See [FETCH_LIST.md](FETCH_LIST.md) for complete examples.

### Pattern 2: Create new record

**Use for**: Reserve page, contact form

See [CREATE_RECORD.md](CREATE_RECORD.md) for mutation patterns.

### Pattern 3: Update existing record

**Use for**: Edit profile, update booking

See [UPDATE_RECORD.md](UPDATE_RECORD.md) for update examples.

## Error handling checklist

When adding Supabase queries:

```
- [ ] Loading state shows spinner
- [ ] Error state shows message with retry
- [ ] Empty state shows friendly message
- [ ] Success state displays data correctly
- [ ] RLS policies allow query (check Supabase dashboard)
```

## Validation workflow

For critical operations (bookings, payments):

1. Create data in hook
2. Validate response has no errors
3. Update UI optimistically
4. Revert on failure

See [VALIDATION.md](VALIDATION.md) for implementation details.

## Environment setup

Required environment variables in `.env.local`:

```
VITE_SUPABASE_URL=https://project-id.supabase.co
VITE_SUPABASE_ANON_KEY=eyJhbGc...
```

For Vercel deployment, add same variables in project settings.

## Real-time updates

For dashboard pages needing live data:

See [REALTIME.md](REALTIME.md) for subscription patterns.

## Troubleshooting

**401 Unauthorized**: Add RLS policy in Supabase Dashboard
**No data returned**: Check table has published records with correct status
**Type errors**: Regenerate types with `npx supabase gen types typescript`
**Slow queries**: Add index on filtered/sorted columns

See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for complete solutions.
