---
name: ui
description: "Skill for the Ui area of Securacy. 106 symbols across 31 files."
---

# Ui

106 symbols | 31 files | Cohesion: 96%

## When to Use

- Working with code in `securacyfrontend/`
- Understanding how useIsMobile, cn, Navbar work
- Modifying ui-related functionality

## Key Files

| File | Symbols |
|------|---------|
| `securacyfrontend/components/ui/sidebar.tsx` | SidebarProvider, SidebarInset, SidebarInput, SidebarHeader, SidebarFooter (+19) |
| `securacyfrontend/components/ui/field.tsx` | FieldSet, FieldLegend, FieldGroup, Field, FieldContent (+5) |
| `securacyfrontend/components/ui/dropdown-menu.tsx` | DropdownMenuContent, DropdownMenuItem, DropdownMenuCheckboxItem, DropdownMenuRadioItem, DropdownMenuLabel (+4) |
| `securacyfrontend/components/ui/table.tsx` | Table, TableHeader, TableBody, TableFooter, TableRow (+3) |
| `securacyfrontend/components/ui/card.tsx` | Card, CardHeader, CardTitle, CardDescription, CardAction (+2) |
| `securacyfrontend/components/ui/sheet.tsx` | SheetOverlay, SheetContent, SheetHeader, SheetFooter, SheetTitle (+1) |
| `securacyfrontend/components/ui/dialog.tsx` | DialogOverlay, DialogContent, DialogHeader, DialogFooter, DialogTitle (+1) |
| `securacyfrontend/components/ui/tabs.tsx` | Tabs, TabsList, TabsTrigger, TabsContent |
| `securacyfrontend/components/ui/avatar.tsx` | Avatar, AvatarImage, AvatarFallback |
| `securacyfrontend/components/ui/alert.tsx` | Alert, AlertTitle, AlertDescription |

## Entry Points

Start here when exploring this area:

- **`useIsMobile`** (Function) — `securacyfrontend/hooks/use-mobile.ts:4`
- **`cn`** (Function) — `securacyfrontend/lib/utils.ts:3`
- **`Navbar`** (Function) — `securacyfrontend/app/home/_components/Navbar.tsx:17`
- **`SettingsNav`** (Function) — `securacyfrontend/app/home/settings/_components/settings-nav.tsx:16`
- **`ExpandableChatCard`** (Function) — `securacyfrontend/app/home/(bots)/_components/ExpandableChatCard.tsx:25`

## Key Symbols

| Symbol | Type | File | Line |
|--------|------|------|------|
| `useIsMobile` | Function | `securacyfrontend/hooks/use-mobile.ts` | 4 |
| `cn` | Function | `securacyfrontend/lib/utils.ts` | 3 |
| `Navbar` | Function | `securacyfrontend/app/home/_components/Navbar.tsx` | 17 |
| `SettingsNav` | Function | `securacyfrontend/app/home/settings/_components/settings-nav.tsx` | 16 |
| `ExpandableChatCard` | Function | `securacyfrontend/app/home/(bots)/_components/ExpandableChatCard.tsx` | 25 |
| `EditableAnalysisCard` | Function | `securacyfrontend/app/home/(bots)/_components/EditableAnalysisCard.tsx` | 104 |
| `handleChange` | Function | `securacyfrontend/app/home/(bots)/_components/EditableAnalysisCard.tsx` | 123 |
| `ChatNav` | Function | `securacyfrontend/app/home/(bots)/_components/ChatNav.tsx` | 8 |
| `TooltipContent` | Function | `securacyfrontend/components/ui/tooltip.tsx` | 36 |
| `Textarea` | Function | `securacyfrontend/components/ui/textarea.tsx` | 4 |
| `Tabs` | Function | `securacyfrontend/components/ui/tabs.tsx` | 7 |
| `TabsList` | Function | `securacyfrontend/components/ui/tabs.tsx` | 20 |
| `TabsTrigger` | Function | `securacyfrontend/components/ui/tabs.tsx` | 36 |
| `TabsContent` | Function | `securacyfrontend/components/ui/tabs.tsx` | 52 |
| `Table` | Function | `securacyfrontend/components/ui/table.tsx` | 6 |
| `TableHeader` | Function | `securacyfrontend/components/ui/table.tsx` | 21 |
| `TableBody` | Function | `securacyfrontend/components/ui/table.tsx` | 31 |
| `TableFooter` | Function | `securacyfrontend/components/ui/table.tsx` | 41 |
| `TableRow` | Function | `securacyfrontend/components/ui/table.tsx` | 54 |
| `TableHead` | Function | `securacyfrontend/components/ui/table.tsx` | 67 |

## How to Explore

1. `gitnexus_context({name: "useIsMobile"})` — see callers and callees
2. `gitnexus_query({query: "ui"})` — find related execution flows
3. Read key files listed above for implementation details
