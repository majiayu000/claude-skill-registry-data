---
name: frontend-trading-ui
description: Frontend Trading UI Engineer — Institutional capability and runbook for frontend-trading-ui.
---

# SKILL: Frontend Trading UI Engineer
## Domain: imCharts, imJournal, imCopying — Module-Specific Patterns

**Activation triggers:** trading interface, chart panel, watchlist, journal entry,
copy trading UI, provider card, trade history table, PnL display, broker account
connection panel.

---

## Module Architecture

```
app/src/modules/expert/
  ├── imCharts/
  │   ├── components/
  │   │   ├── WatchlistPanel.tsx     ← symbol list, drag-reorder
  │   │   ├── ChartContainer.tsx     ← TradingView wrapper
  │   │   ├── OrderPanel.tsx         ← buy/sell form
  │   │   └── PositionsTable.tsx     ← live open positions
  │   ├── hooks/
  │   │   ├── useWatchlist.ts        ← React Query + WebSocket sync
  │   │   └── usePositions.ts        ← live position updates
  │   └── store/
  │       └── chartsStore.ts         ← Zustand: selected symbol, layout
  │
  ├── imJournal/
  │   ├── components/
  │   │   ├── TradeTable.tsx         ← virtual-scrolled trade list
  │   │   ├── JournalEntryModal.tsx  ← annotate trade
  │   │   ├── StatsDashboard.tsx     ← win rate, profit factor, Sharpe
  │   │   └── CalendarHeatmap.tsx    ← daily PnL heat map
  │   ├── hooks/
  │   │   └── useJournal.ts          ← React Query: /api/v1/journal/*
  │   └── store/
  │       └── journalStore.ts        ← Zustand: filters, date range
  │
  └── imCopying/
      ├── components/
      │   ├── ProviderCard.tsx        ← provider stats, subscribe CTA
      │   ├── SubscriptionPanel.tsx  ← active subscriptions, controls
      │   └── SignalFeed.tsx          ← live signal stream
      ├── hooks/
      │   └── useCopyTrading.ts      ← React Query + WebSocket
      └── store/
          └── copyingStore.ts        ← Zustand: selected provider
```

---

## Live Data Pattern (WebSocket + React Query Hybrid)

```typescript
// hooks/usePositions.ts — live positions via WS, fallback to query
import { useQuery, useQueryClient } from '@tanstack/react-query';
import { useEffect } from 'react';
import { useExpertWS } from '@/shared/ws/expertSocket';

export function usePositions(accountId: string) {
  const queryClient = useQueryClient();

  // Initial data from REST
  const query = useQuery({
    queryKey: ['positions', accountId],
    queryFn: () => expertApi.get(`/brokers/accounts/${accountId}/positions`).then(r => r.data),
    staleTime: 5_000,
  });

  // Live updates via WebSocket
  const { subscribe } = useExpertWS();
  useEffect(() => {
    return subscribe(`positions.${accountId}`, (payload) => {
      queryClient.setQueryData(['positions', accountId], payload);
    });
  }, [accountId, queryClient, subscribe]);

  return query;
}
```

---

## Trade Table — Virtual Scroll Pattern

```typescript
// components/TradeTable.tsx — handles 10k+ rows without lag
import { useVirtualizer } from '@tanstack/react-virtual';
import { useRef } from 'react';

export function TradeTable({ trades }: { trades: Trade[] }) {
  const parentRef = useRef<HTMLDivElement>(null);

  const virtualizer = useVirtualizer({
    count: trades.length,
    getScrollElement: () => parentRef.current,
    estimateSize: () => 48,   // row height in px
    overscan: 10,
  });

  return (
    <div ref={parentRef} className="h-[600px] overflow-auto">
      <div style={{ height: virtualizer.getTotalSize() }} className="relative">
        {virtualizer.getVirtualItems().map((virtualRow) => (
          <div
            key={virtualRow.index}
            style={{ position: 'absolute', top: virtualRow.start, height: 48, width: '100%' }}
            className="flex items-center border-b border-navy-800 px-4"
          >
            <TradeRow trade={trades[virtualRow.index]} />
          </div>
        ))}
      </div>
    </div>
  );
}
```

---

## Broker Account Connection Panel

```typescript
// Connects to Expert Backend POST /api/v1/brokers/accounts
// Shows connection status with proper color semantics

type ConnectionStatus = 'connected' | 'disconnected' | 'connecting' | 'error';

const statusConfig: Record<ConnectionStatus, { label: string; color: string; dot: string }> = {
  connected:    { label: 'Live',         color: 'text-cyan-400',   dot: 'bg-cyan-400' },
  disconnected: { label: 'Disconnected', color: 'text-gray-400',   dot: 'bg-gray-600' },
  connecting:   { label: 'Connecting…',  color: 'text-yellow-400', dot: 'bg-yellow-400 animate-pulse' },
  error:        { label: 'Error',        color: 'text-red-400',    dot: 'bg-red-500' },
};

function AccountStatusBadge({ status }: { status: ConnectionStatus }) {
  const cfg = statusConfig[status];
  return (
    <span className={`flex items-center gap-1.5 text-xs font-medium ${cfg.color}`}>
      <span className={`w-1.5 h-1.5 rounded-full ${cfg.dot}`} />
      {cfg.label}
    </span>
  );
}
```

---

## PnL Statistics Dashboard

```typescript
// StatsDashboard.tsx — key trading metrics
interface TradingStats {
  winRate: number;          // 0–1
  profitFactor: number;     // >1 is profitable
  sharpeRatio: number;      // risk-adjusted return
  maxDrawdown: number;      // negative, e.g. -0.15 = 15% drawdown
  totalPnl: number;
  totalTrades: number;
  avgWin: number;
  avgLoss: number;
}

function StatCard({ label, value, format }: { label: string; value: number; format: 'pct' | 'usd' | 'ratio' | 'count' }) {
  const formatted = {
    pct:   `${(value * 100).toFixed(1)}%`,
    usd:   `$${value.toLocaleString(undefined, { minimumFractionDigits: 2 })}`,
    ratio: value.toFixed(2),
    count: value.toLocaleString(),
  }[format];

  const isPositive = value > 0;
  const colorClass = format === 'usd' || format === 'pct'
    ? (isPositive ? 'text-green-400' : value < 0 ? 'text-red-400' : 'text-gray-300')
    : 'text-cyan-300';

  return (
    <div className="bg-navy-900/50 rounded-xl border border-navy-800 p-4">
      <p className="text-xs text-gray-500 uppercase tracking-wider mb-1">{label}</p>
      <p className={`text-2xl font-bold font-mono ${colorClass}`}>{formatted}</p>
    </div>
  );
}
```

---

## Provider Card (imCopying)

```typescript
// ProviderCard.tsx — display copy trading provider stats
function ProviderCard({ provider, onSubscribe }: ProviderCardProps) {
  return (
    <div className="bg-navy-900/50 border border-navy-800 rounded-2xl p-5 hover:border-cyan-500/30 transition-all duration-200">
      {/* Header */}
      <div className="flex items-start justify-between mb-4">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-full bg-gradient-to-br from-cyan-500 to-blue-600 flex items-center justify-center text-white font-bold">
            {provider.username[0].toUpperCase()}
          </div>
          <div>
            <p className="text-white font-semibold">{provider.username}</p>
            <p className="text-xs text-gray-500">{provider.broker} · {provider.account_type}</p>
          </div>
        </div>
        <span className={`text-xs px-2 py-0.5 rounded-full ${provider.is_verified ? 'bg-cyan-500/10 text-cyan-400 border border-cyan-500/20' : 'bg-gray-700/50 text-gray-500'}`}>
          {provider.is_verified ? 'Verified' : 'Unverified'}
        </span>
      </div>

      {/* Stats grid */}
      <div className="grid grid-cols-3 gap-3 mb-4">
        <div className="text-center">
          <p className="text-xs text-gray-500">Win Rate</p>
          <p className="text-lg font-bold text-white">{(provider.win_rate * 100).toFixed(0)}%</p>
        </div>
        <div className="text-center">
          <p className="text-xs text-gray-500">Total Return</p>
          <p className={`text-lg font-bold ${provider.total_return >= 0 ? 'text-green-400' : 'text-red-400'}`}>
            {provider.total_return >= 0 ? '+' : ''}{(provider.total_return * 100).toFixed(1)}%
          </p>
        </div>
        <div className="text-center">
          <p className="text-xs text-gray-500">Drawdown</p>
          <p className="text-lg font-bold text-red-400">{(provider.max_drawdown * 100).toFixed(1)}%</p>
        </div>
      </div>

      <button
        onClick={() => onSubscribe(provider.id)}
        className="w-full py-2 rounded-xl bg-cyan-500/10 hover:bg-cyan-500/20 border border-cyan-500/30 text-cyan-400 text-sm font-medium transition-all duration-200"
      >
        Subscribe
      </button>
    </div>
  );
}
```

---

## Anti-Patterns

```
✗ Polling REST every 1s for live prices — use WebSocket subscription
✗ Rendering 1000+ trades without virtualization (DOM crash)
✗ Storing position data in component state (use React Query + WS)
✗ Mixing journal and chart state in one Zustand slice
✗ Broker account credentials in Redux/Zustand (never in frontend state)
✗ PnL colors inconsistent with design system (always use pnlColor utility)
✗ Fixed height containers on journal table (use flex-1 + overflow-auto)
✗ Provider rating without verified badge (trust signals matter)
```
