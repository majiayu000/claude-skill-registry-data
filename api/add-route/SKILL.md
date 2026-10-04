---
name: add-route
description: Add a new Express.js server route to ProAnimate's backend. Covers route file creation, middleware setup, Supabase auth, and mounting in server/index.ts.
argument-hint: <route-name>
---

# Add Server Route to ProAnimate

Create a new Express.js API route in the ProAnimate backend server (port 3001). Frontend requests to `/api/*` are proxied to the server by Vite.

## Steps

1. **Create route file** at `server/routes/<featureName>.ts`

   ```ts
   import { Router } from 'express'
   import type { Request, Response } from 'express'

   const router = Router()

   // GET endpoint
   router.get('/', async (req: Request, res: Response) => {
     try {
       const userId = (req as any).userId  // Set by requireAuth middleware
       // ... business logic
       res.json({ data: [] })
     } catch (error: any) {
       console.error('[MyFeature] Error:', error)
       res.status(500).json({ error: error.message || 'Internal server error' })
     }
   })

   // POST endpoint
   router.post('/', async (req: Request, res: Response) => {
     try {
       const userId = (req as any).userId
       const { param1, param2 } = req.body
       // ... business logic
       res.json({ success: true })
     } catch (error: any) {
       console.error('[MyFeature] Error:', error)
       res.status(500).json({ error: error.message || 'Internal server error' })
     }
   })

   export default router
   ```

2. **Use Supabase for data persistence** (if needed):

   ```ts
   import { getSupabaseAdmin } from '../middleware/supabaseAuth.js'

   router.get('/items', async (req: Request, res: Response) => {
     const userId = (req as any).userId
     const sb = getSupabaseAdmin()

     const { data, error } = await sb
       .from('my_table')
       .select('*')
       .eq('user_id', userId)
       .order('created_at', { ascending: false })

     if (error) {
       res.status(500).json({ error: error.message })
       return
     }
     res.json(data)
   })
   ```

3. **Use Supabase Storage** for file uploads:

   ```ts
   import multer from 'multer'
   const upload = multer({ storage: multer.memoryStorage(), limits: { fileSize: 50_000_000 } })

   router.post('/upload', upload.single('file'), async (req: Request, res: Response) => {
     const userId = (req as any).userId
     const sb = getSupabaseAdmin()
     const file = req.file!

     const path = `${userId}/${Date.now()}-${file.originalname}`
     const { error } = await sb.storage
       .from('my-bucket')
       .upload(path, file.buffer, { contentType: file.mimetype, upsert: true })

     if (error) {
       res.status(500).json({ error: error.message })
       return
     }

     const { data: urlData } = sb.storage.from('my-bucket').getPublicUrl(path)
     res.json({ url: urlData.publicUrl })
   })
   ```

4. **Mount the route** in `server/index.ts`:

   Add the import at the top with other route imports:
   ```ts
   import myFeatureRoutes from './routes/myFeature'
   ```

   Mount with appropriate middleware:
   ```ts
   // Standard authenticated route
   app.use('/api/my-feature', requireAuth, myFeatureRoutes)

   // AI/expensive route with rate limiting (20 req/min per IP)
   app.use('/api/my-feature', requireAuth, aiRateLimiter, myFeatureRoutes)

   // Public route (no auth required)
   app.use('/api/my-feature', myFeatureRoutes)
   ```

5. **Call from frontend** service:

   ```ts
   // In src/services/myFeature.ts
   import { useAuthStore } from '@/stores/useAuthStore'

   export async function fetchMyFeature() {
     const token = useAuthStore.getState().session?.access_token
     const res = await fetch('/api/my-feature', {
       headers: {
         'Content-Type': 'application/json',
         ...(token ? { Authorization: `Bearer ${token}` } : {}),
       },
     })
     if (!res.ok) throw new Error(await res.text())
     return res.json()
   }
   ```

6. **Add environment variables** (if needed):

   Add to `server/.env`:
   ```env
   MY_FEATURE_API_KEY=...
   ```

   Read lazily in the route (env vars are read after `dotenv.config()` in `server/index.ts`):
   ```ts
   const apiKey = process.env.MY_FEATURE_API_KEY
   if (!apiKey) {
     res.status(500).json({ error: 'MY_FEATURE_API_KEY not configured' })
     return
   }
   ```

## Key Files

| Purpose | Path |
|---------|------|
| Route directory | `server/routes/` |
| Server entry point | `server/index.ts` |
| Auth middleware | `server/middleware/supabaseAuth.ts` |
| Server env file | `server/.env` |
| Frontend auth store | `src/stores/useAuthStore.ts` |
| Vite proxy config | `vite.config.ts` (proxies `/api` to `localhost:3001`) |

## Middleware Reference

| Middleware | Purpose |
|-----------|---------|
| `requireAuth` | Verifies Supabase JWT, attaches `req.userId` and `req.userEmail` |
| `aiRateLimiter` | 20 requests per minute per IP (safety net for AI endpoints) |
| `express.json()` | Parses JSON body (100MB limit, already applied globally) |
| `requireApiKey` | For public API v1 routes (API key auth instead of JWT) |

## Common Issues

- **Route returns 401**: Ensure the frontend sends `Authorization: Bearer <token>` header. Token comes from `useAuthStore.getState().session?.access_token`.
- **Route returns 404**: Verify the route is mounted in `server/index.ts` and the path matches. The Vite dev server proxies `/api` to `localhost:3001`.
- **Environment variables undefined**: Env vars are loaded from `server/.env` via dotenv. Make sure the file exists and the key name matches exactly.
- **CORS errors**: The server configures CORS for localhost dev ports (5173, 5174, 5175, 3000). For production, set `ALLOWED_ORIGINS` env var.
- **Large payloads**: `express.json()` is configured with a 100MB limit. For file uploads, use `multer` with `memoryStorage()`.

## Example

Reference: `server/routes/recordings.ts`
- Uses Supabase Storage for video/thumbnail uploads
- JSON metadata index per user
- `multer` for file upload handling
- Full CRUD with `getSupabaseAdmin()`
