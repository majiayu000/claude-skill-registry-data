---
name: admin-shell-foundation
description: >
  The shared admin shell scaffold used by all domain skills. Provides the base
  AdminShell layout, DataTable, StatusBadge, ConfirmDialog, sidebar navigation,
  and header with user menu. All domain skills (hotel-pms, reservation-booking,
  restaurant-pos, crm-onboarding) consume this as a shared foundation.
  Triggers when building any admin dashboard — the layout wrapper that goes
  around every admin page.
---

# Admin Shell Foundation

## What's Included

```
admin-shell-foundation/
├── AdminShell.tsx           ← Base layout wrapper (sidebar + header)
├── DataTable.tsx            ← Sortable, filterable CRUD table
├── StatusBadge.tsx          ← active/inactive/pending/confirmed states
├── ConfirmDialog.tsx        ← Destructive action confirmation modal
└── references/
    ├── sidebar-nav-pattern.md
    └── data-table-pattern.md
```

## AdminShell Layout

```tsx
// components/AdminShell.tsx
export function AdminShell({ children, nav }: {
  children: React.ReactNode;
  nav: NavItem[];
}) {
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const { session } = useSession();

  return (
    <div className="flex h-screen bg-gray-50">
      {/* Sidebar */}
      <aside className={`${sidebarOpen ? 'w-64' : 'w-16'} bg-slate-800 transition-width`}>
        <div className="p-4 font-bold text-white">Admin</div>
        <nav className="flex-1">
          {nav.map(item => (
            <NavLink key={item.href} to={item.href}
              className="flex items-center gap-3 px-4 py-3 text-gray-300 hover:bg-slate-700">
              <item.icon className="w-5 h-5" />
              {sidebarOpen && <span>{item.label}</span>}
            </NavLink>
          ))}
        </nav>
      </aside>

      {/* Main content */}
      <div className="flex-1 flex flex-col">
        <header className="h-16 bg-white border-b flex items-center justify-between px-6">
          <button onClick={() => setSidebarOpen(!sidebarOpen)} className="p-2 hover:bg-gray-100 rounded">
            <Menu className="w-5 h-5" />
          </button>
          <div className="flex items-center gap-4">
            <span className="text-sm text-gray-600">{session?.user?.name}</span>
            <UserMenu />
          </div>
        </header>
        <main className="flex-1 overflow-auto p-6">
          {children}
        </main>
      </div>
    </div>
  );
}

export const adminNav: NavItem[] = [
  { href: '/admin', label: 'Dashboard', icon: LayoutDashboard },
  { href: '/admin/bookings', label: 'Bookings', icon: Calendar },
  { href: '/admin/guests', label: 'Guests', icon: Users },
  { href: '/admin/packages', label: 'Packages', icon: Package },
  { href: '/admin/reports', label: 'Reports', icon: BarChart3 },
];
```

## DataTable Component

```tsx
// components/DataTable.tsx
interface Column<T> {
  key: keyof T | string;
  label: string;
  sortable?: boolean;
  render?: (value: T[keyof T], row: T) => React.ReactNode;
}

interface DataTableProps<T> {
  data: T[];
  columns: Column<T>[];
  onRowClick?: (row: T) => void;
  emptyMessage?: string;
}

export function DataTable<T extends { id: string }>({ data, columns, onRowClick }: DataTableProps<T>) {
  const [sortKey, setSortKey] = useState<string | null>(null);
  const [sortDir, setSortDir] = useState<'asc' | 'desc'>('asc');
  const [filter, setFilter] = useState('');

  const filtered = data.filter(row =>
    Object.values(row).some(v => String(v).toLowerCase().includes(filter.toLowerCase()))
  );

  const sorted = [...filtered].sort((a, b) => {
    if (!sortKey) return 0;
    const cmp = String(a[sortKey as keyof T]).localeCompare(String(b[sortKey as keyof T]));
    return sortDir === 'asc' ? cmp : -cmp;
  });

  return (
    <div className="space-y-4">
      <input placeholder="Filter..." value={filter} onChange={e => setFilter(e.target.value)}
        className="border rounded px-3 py-2 w-64" />
      <table className="w-full border-collapse">
        <thead>
          <tr className="border-b bg-gray-50">
            {columns.map(col => (
              <th key={String(col.key)} className="px-4 py-3 text-left text-sm font-medium text-gray-600"
                onClick={() => col.sortable && setSortKey(String(col.key))}>
                {col.label} {col.sortable && (sortKey === String(col.key) ? (sortDir === 'asc' ? '↑' : '↓') : '↕')}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {sorted.map(row => (
            <tr key={row.id} className="border-b hover:bg-gray-50 cursor-pointer"
              onClick={() => onRowClick?.(row)}>
              {columns.map(col => (
                <td key={String(col.key)} className="px-4 py-3">
                  {col.render ? col.render(row[col.key as keyof T], row) : String(row[col.key as keyof T])}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
```

## StatusBadge

```tsx
// components/StatusBadge.tsx
type Status = 'active' | 'inactive' | 'pending' | 'confirmed' | 'cancelled' | 'checked_in' | 'no_show';

export function StatusBadge({ status }: { status: Status }) {
  const styles: Record<Status, string> = {
    active: 'bg-green-100 text-green-700',
    inactive: 'bg-gray-100 text-gray-600',
    pending: 'bg-yellow-100 text-yellow-700',
    confirmed: 'bg-blue-100 text-blue-700',
    cancelled: 'bg-red-100 text-red-700',
    checked_in: 'bg-green-100 text-green-800',
    no_show: 'bg-red-100 text-red-800',
  };

  return (
    <span className={`inline-flex px-2 py-1 text-xs font-medium rounded-full ${styles[status]}`}>
      {status.replace('_', ' ')}
    </span>
  );
}
```

## ConfirmDialog

```tsx
// components/ConfirmDialog.tsx
interface ConfirmDialogProps {
  open: boolean;
  title: string;
  message: string;
  confirmLabel?: string;
  onConfirm: () => void;
  onCancel: () => void;
  variant?: 'danger' | 'warning' | 'default';
}

export function ConfirmDialog({ open, title, message, confirmLabel = 'Confirm', onConfirm, onCancel, variant = 'danger' }: ConfirmDialogProps) {
  if (!open) return null;
  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg shadow-xl max-w-md w-full p-6">
        <h3 className="text-lg font-semibold">{title}</h3>
        <p className="mt-2 text-gray-600">{message}</p>
        <div className="mt-4 flex justify-end gap-3">
          <button onClick={onCancel} className="px-4 py-2 text-gray-600 hover:bg-gray-100 rounded">Cancel</button>
          <button onClick={onConfirm}
            className={`px-4 py-2 rounded text-white ${variant === 'danger' ? 'bg-red-600 hover:bg-red-700' : 'bg-blue-600 hover:bg-blue-700'}`}>
            {confirmLabel}
          </button>
        </div>
      </div>
    </div>
  );
}
```
