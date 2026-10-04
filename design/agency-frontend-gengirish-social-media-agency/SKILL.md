---
name: agency-frontend
description: Build and maintain the Social Media Agency Next.js frontend with dashboard UI, content calendar, analytics, and responsive design. Use when creating pages, components, layouts, forms, or frontend configuration.
---

# Social Media Agency Next.js Frontend

## Tech Stack

```json
{
  "dependencies": {
    "next": "^14.2",
    "react": "^18.3",
    "react-dom": "^18.3",
    "@radix-ui/react-dialog": "^1.1",
    "@radix-ui/react-dropdown-menu": "^2.1",
    "@radix-ui/react-tabs": "^1.1",
    "@radix-ui/react-select": "^2.1",
    "class-variance-authority": "^0.7",
    "clsx": "^2.1",
    "tailwind-merge": "^2.5",
    "lucide-react": "^0.460",
    "recharts": "^2.13",
    "zustand": "^4.5",
    "@tanstack/react-query": "^5.60",
    "@dnd-kit/core": "^6.1",
    "@dnd-kit/sortable": "^8.0",
    "react-hook-form": "^7.53",
    "@hookform/resolvers": "^3.9",
    "zod": "^3.23",
    "sonner": "^1.7",
    "date-fns": "^3.6"
  }
}
```

## API Client

Typed client wrapping `fetch` with automatic auth headers.

```typescript
// lib/api.ts
const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8001";

class ApiError extends Error {
  constructor(public status: number, message: string) {
    super(message);
  }
}

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const token = typeof window !== "undefined"
    ? localStorage.getItem("token")
    : null;

  const res = await fetch(`${API_BASE}${path}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...options?.headers,
    },
  });

  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    throw new ApiError(res.status, body.detail || "Request failed");
  }
  return res.json();
}

export const api = {
  health: () => request<{ status: string }>("/api/v1/health"),

  // Auth
  login: (email: string, password: string) =>
    request<{ access_token: string; role: string }>("/api/v1/auth/login", {
      method: "POST", body: JSON.stringify({ email, password }),
    }),
  signup: (data: SignupRequest) =>
    request<{ access_token: string }>("/api/v1/auth/signup", {
      method: "POST", body: JSON.stringify(data),
    }),

  // Clients
  getClients: (page = 1) =>
    request<ClientListResponse>(`/api/v1/clients?page=${page}`),
  getClient: (id: string) =>
    request<ClientResponse>(`/api/v1/clients/${id}`),
  createClient: (data: ClientCreateRequest) =>
    request<ClientResponse>("/api/v1/clients", {
      method: "POST", body: JSON.stringify(data),
    }),

  // Campaigns
  getCampaigns: (clientId?: string) =>
    request<CampaignListResponse>(`/api/v1/campaigns${clientId ? `?client_id=${clientId}` : ""}`),
  createCampaign: (data: CampaignCreateRequest) =>
    request<CampaignResponse>("/api/v1/campaigns", {
      method: "POST", body: JSON.stringify(data),
    }),

  // Content
  getContent: (params?: ContentQueryParams) =>
    request<ContentListResponse>(`/api/v1/content?${new URLSearchParams(params as any)}`),
  createContent: (data: ContentCreateRequest) =>
    request<ContentResponse>("/api/v1/content", {
      method: "POST", body: JSON.stringify(data),
    }),
  generateContent: (data: ContentGenerateRequest) =>
    request<ContentGenerateResponse>("/api/v1/content/generate", {
      method: "POST", body: JSON.stringify(data),
    }),

  // Calendar
  getCalendarEvents: (start: string, end: string) =>
    request<CalendarEvent[]>(`/api/v1/calendar?start=${start}&end=${end}`),
  rescheduleContent: (contentId: string, scheduledAt: string) =>
    request<ContentResponse>(`/api/v1/calendar/${contentId}/reschedule`, {
      method: "PATCH", body: JSON.stringify({ scheduled_at: scheduledAt }),
    }),

  // Approvals
  getPendingApprovals: () =>
    request<ApprovalListResponse>("/api/v1/approvals?status=pending"),
  approveContent: (contentId: string) =>
    request<ApprovalResponse>(`/api/v1/approvals/${contentId}/approve`, { method: "POST" }),
  rejectContent: (contentId: string, feedback: string) =>
    request<ApprovalResponse>(`/api/v1/approvals/${contentId}/reject`, {
      method: "POST", body: JSON.stringify({ feedback }),
    }),

  // Analytics
  getDashboardStats: () =>
    request<DashboardStats>("/api/v1/analytics/dashboard"),
  getClientAnalytics: (clientId: string, period: string) =>
    request<AnalyticsResponse>(`/api/v1/analytics/clients/${clientId}?period=${period}`),

  // Assets
  uploadAsset: (formData: FormData) =>
    request<AssetResponse>("/api/v1/assets", {
      method: "POST",
      body: formData,
      headers: {},
    }),

  // Billing
  getSubscription: () =>
    request<Subscription>("/api/v1/billing/subscription"),
  createCheckout: (planId: string) =>
    request<{ url: string }>("/api/v1/billing/checkout", {
      method: "POST", body: JSON.stringify({ plan_id: planId }),
    }),

  // Email
  setupOrgEmail: () =>
    request<{ inbox_id: string; email: string }>("/api/v1/organizations/email/setup", {
      method: "POST",
    }),
  getEmailStatus: () =>
    request<{ configured: boolean; email: string | null }>("/api/v1/organizations/email/status"),
};
```

## Page Template

```tsx
"use client";

import { useEffect, useState } from "react";
import { toast } from "sonner";
import { api } from "@/lib/api";

export default function FeaturePage() {
  const [data, setData] = useState<DataType[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.getData()
      .then(setData)
      .catch((err) => toast.error(err.message))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <PageSkeleton />;

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-slate-900">Feature</h1>
      </div>
      {/* Content */}
    </div>
  );
}
```

## Dashboard Layout

```tsx
// app/(dashboard)/layout.tsx
"use client";
import { useState } from "react";
import { Sidebar } from "@/components/layout/sidebar";
import { Topbar } from "@/components/layout/topbar";
import { MobileNav } from "@/components/layout/mobile-nav";

export default function DashboardLayout({ children }: { children: React.ReactNode }) {
  const [sidebarOpen, setSidebarOpen] = useState(false);

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-indigo-50/30">
      <Sidebar className="hidden lg:fixed lg:inset-y-0 lg:flex lg:w-64" />
      <MobileNav open={sidebarOpen} onClose={() => setSidebarOpen(false)} />
      <div className="lg:pl-64">
        <Topbar onMenuClick={() => setSidebarOpen(true)} />
        <main className="p-4 sm:p-6 lg:p-8">{children}</main>
      </div>
    </div>
  );
}
```

## KPI Card

```tsx
// components/analytics/kpi-card.tsx
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { TrendingUp, TrendingDown } from "lucide-react";

interface KPICardProps {
  label: string;
  value: string;
  changePct: number;
  icon: React.ReactNode;
  loading?: boolean;
}

export function KPICard({ label, value, changePct, icon, loading }: KPICardProps) {
  if (loading) {
    return (
      <Card>
        <CardContent className="p-6">
          <div className="h-4 w-24 animate-pulse rounded bg-slate-200" />
          <div className="mt-3 h-8 w-32 animate-pulse rounded bg-slate-200" />
        </CardContent>
      </Card>
    );
  }

  const isPositive = changePct >= 0;

  return (
    <Card>
      <CardHeader className="flex flex-row items-center justify-between pb-2">
        <CardTitle className="text-sm font-medium text-muted-foreground">{label}</CardTitle>
        {icon}
      </CardHeader>
      <CardContent>
        <div className="text-2xl font-bold">{value}</div>
        <div className={`mt-1 flex items-center gap-1 text-sm ${
          isPositive ? "text-emerald-600" : "text-red-600"
        }`}>
          {isPositive ? <TrendingUp className="h-4 w-4" /> : <TrendingDown className="h-4 w-4" />}
          {isPositive ? "+" : ""}{changePct.toFixed(1)}%
        </div>
      </CardContent>
    </Card>
  );
}
```

## Content Editor with AI

```tsx
// components/content/content-editor.tsx
"use client";

import { useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { toast } from "sonner";
import { Sparkles } from "lucide-react";
import { api } from "@/lib/api";

const schema = z.object({
  body: z.string().min(1, "Content body is required"),
  platform: z.string().min(1, "Select a platform"),
  hashtags: z.string().optional(),
  scheduled_at: z.string().optional(),
});

type FormData = z.infer<typeof schema>;

export function ContentEditor({ clientId, onSuccess }: { clientId: string; onSuccess: () => void }) {
  const [generating, setGenerating] = useState(false);
  const {
    register,
    handleSubmit,
    setValue,
    watch,
    formState: { errors, isSubmitting },
  } = useForm<FormData>({ resolver: zodResolver(schema) });

  async function handleGenerate() {
    setGenerating(true);
    try {
      const result = await api.generateContent({
        client_id: clientId,
        platform: watch("platform"),
        topic: watch("body") || "general engagement post",
        tone: "professional",
        content_type: "post",
      });
      setValue("body", result.body);
      if (result.hashtags) setValue("hashtags", result.hashtags.join(" "));
      toast.success("Content generated!");
    } catch (err: any) {
      toast.error(err.message);
    } finally {
      setGenerating(false);
    }
  }

  async function onSubmit(data: FormData) {
    try {
      await api.createContent({
        client_id: clientId,
        platform: data.platform,
        body: data.body,
        hashtags: data.hashtags?.split(/\s+/).filter(Boolean) || [],
        scheduled_at: data.scheduled_at || undefined,
      });
      toast.success("Content created!");
      onSuccess();
    } catch (err: any) {
      toast.error(err.message);
    }
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
      <div>
        <label className="block text-sm font-medium text-slate-700 mb-1">Platform</label>
        <select
          {...register("platform")}
          className="w-full rounded-lg border border-slate-300 px-4 py-2.5 text-slate-900 focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 outline-none"
        >
          <option value="">Select platform...</option>
          <option value="instagram">Instagram</option>
          <option value="facebook">Facebook</option>
          <option value="twitter">Twitter / X</option>
          <option value="linkedin">LinkedIn</option>
          <option value="tiktok">TikTok</option>
        </select>
        {errors.platform && <p className="mt-1 text-xs text-red-500">{errors.platform.message}</p>}
      </div>

      <div>
        <div className="flex items-center justify-between mb-1">
          <label className="block text-sm font-medium text-slate-700">Content</label>
          <button
            type="button"
            onClick={handleGenerate}
            disabled={generating}
            className="flex items-center gap-1 text-xs text-indigo-600 hover:text-indigo-500"
          >
            <Sparkles className="h-3 w-3" />
            {generating ? "Generating..." : "AI Generate"}
          </button>
        </div>
        <textarea
          {...register("body")}
          rows={5}
          className="w-full rounded-lg border border-slate-300 px-4 py-2.5 text-slate-900 placeholder-slate-400 focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 outline-none resize-none"
          placeholder="Write your post content or use AI to generate..."
        />
        {errors.body && <p className="mt-1 text-xs text-red-500">{errors.body.message}</p>}
      </div>

      <div>
        <label className="block text-sm font-medium text-slate-700 mb-1">Hashtags</label>
        <input
          {...register("hashtags")}
          className="w-full rounded-lg border border-slate-300 px-4 py-2.5 text-slate-900 placeholder-slate-400 focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 outline-none"
          placeholder="#socialmedia #marketing #growth"
        />
      </div>

      <button
        type="submit"
        disabled={isSubmitting}
        className="w-full rounded-lg bg-indigo-600 px-6 py-2.5 font-semibold text-white hover:bg-indigo-500 disabled:opacity-50 transition-colors"
      >
        {isSubmitting ? "Creating..." : "Create Content"}
      </button>
    </form>
  );
}
```

## Calendar View (Drag & Drop)

```tsx
// components/calendar/content-calendar.tsx
"use client";

import { DndContext, DragEndEvent } from "@dnd-kit/core";
import { toast } from "sonner";
import { api } from "@/lib/api";

interface CalendarEvent {
  id: string;
  title: string;
  platform: string;
  scheduledAt: string;
  status: string;
  clientName: string;
}

export function ContentCalendar({ events }: { events: CalendarEvent[] }) {
  async function handleDragEnd(event: DragEndEvent) {
    const { active, over } = event;
    if (!over || active.id === over.id) return;

    try {
      await api.rescheduleContent(active.id as string, over.id as string);
      toast.success("Content rescheduled");
    } catch (err: any) {
      toast.error(err.message);
    }
  }

  return (
    <DndContext onDragEnd={handleDragEnd}>
      <div className="grid grid-cols-7 gap-px bg-slate-200 rounded-xl overflow-hidden">
        {/* Calendar grid with draggable content cards */}
      </div>
    </DndContext>
  );
}
```

## Loading Skeleton

```tsx
function PageSkeleton() {
  return (
    <div className="space-y-4">
      <div className="h-8 w-48 animate-pulse rounded-lg bg-slate-200" />
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        {[...Array(4)].map((_, i) => (
          <div key={i} className="h-28 animate-pulse rounded-xl bg-slate-200" />
        ))}
      </div>
      <div className="h-64 animate-pulse rounded-xl bg-slate-200" />
    </div>
  );
}
```

## Error Boundary

```tsx
// app/(dashboard)/error.tsx
"use client";
export default function DashboardError({ error, reset }: { error: Error; reset: () => void }) {
  return (
    <div className="flex min-h-[400px] flex-col items-center justify-center gap-4">
      <h2 className="text-xl font-semibold text-slate-900">Something went wrong</h2>
      <p className="text-slate-500">{error.message}</p>
      <button onClick={reset} className="rounded-lg bg-indigo-600 px-4 py-2 text-white hover:bg-indigo-500">
        Try again
      </button>
    </div>
  );
}
```

## Platform Color Coding

```typescript
// lib/platform-colors.ts
export const PLATFORM_COLORS: Record<string, { bg: string; text: string; border: string }> = {
  instagram: { bg: "bg-pink-50", text: "text-pink-700", border: "border-pink-200" },
  facebook: { bg: "bg-blue-50", text: "text-blue-700", border: "border-blue-200" },
  twitter: { bg: "bg-sky-50", text: "text-sky-700", border: "border-sky-200" },
  linkedin: { bg: "bg-indigo-50", text: "text-indigo-700", border: "border-indigo-200" },
  tiktok: { bg: "bg-slate-50", text: "text-slate-700", border: "border-slate-200" },
};
```

## Key Rules

1. **Never hardcode backend URLs** — use `NEXT_PUBLIC_API_URL`
2. **Always use the `api` client** — never raw `fetch` in components
3. **Always provide loading skeletons** — never blank screens
4. **Always define TypeScript interfaces** for API responses
5. **Dashboard uses light theme** — slate/indigo palette
6. **Toast notifications via sonner** — never `alert()`
7. **Icons from `lucide-react` only**
8. **Mobile-first** — design for 375px, scale up with `sm:`, `md:`, `lg:`
9. **Sidebar collapses** on screens < 1024px
10. **Drag-and-drop** via `@dnd-kit` for calendar and content ordering
11. **Color-code content by platform** — use the `PLATFORM_COLORS` map
