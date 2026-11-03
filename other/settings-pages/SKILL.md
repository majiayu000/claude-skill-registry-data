---
name: settings-pages
description: Use when building settings — account, profile, team/members, workspace, and a danger zone. Covers sectioned layouts, sidebar/tab navigation, autosave vs explicit save, and safe destructive actions.
---

# Settings Pages

## Overview

Settings sprawl fast. Tame them with a consistent structure: a section navigation (sidebar on desktop, tabs/select on mobile), grouped cards per topic, and a clear save model. Isolate irreversible actions in a visually distinct **danger zone** so users never delete by reflex.

## When to use

- Building account/profile/team/workspace/billing settings.
- A settings page has become one giant unstructured form.
- Adding destructive actions (delete account, remove member).

## Structure: section nav + content

```tsx
<div className="mx-auto grid max-w-5xl gap-8 md:grid-cols-[200px_1fr]">
  <nav aria-label="Settings" className="flex gap-1 md:flex-col">
    {sections.map((s) => (
      <a key={s.href} href={s.href} aria-current={s.active ? "page" : undefined}
        className={cn("rounded-md px-3 py-2 text-sm", s.active ? "bg-muted font-medium" : "text-muted-foreground hover:bg-muted/50")}>
        {s.label}
      </a>
    ))}
  </nav>

  <div className="space-y-6">
    <SettingsSection title="Profile" description="How you appear across the workspace.">
      <ProfileForm />
    </SettingsSection>
    <SettingsSection title="Notifications" description="Choose what we email you about.">
      <NotificationPrefs />
    </SettingsSection>
  </div>
</div>
```

A reusable section card keeps spacing/typography consistent:

```tsx
function SettingsSection({ title, description, children }: SettingsSectionProps) {
  return (
    <Card>
      <CardHeader><CardTitle>{title}</CardTitle><CardDescription>{description}</CardDescription></CardHeader>
      <CardContent>{children}</CardContent>
    </Card>
  );
}
```

## Save model: pick one and be consistent

- **Explicit save** (form + Save button) for grouped changes — show a sticky "You have unsaved changes" bar when `isDirty`, disable Save while submitting, toast on success.
- **Autosave** for single toggles/switches — optimistic update, revert + toast on failure. Don't mix a "Save" button with auto-saving toggles on the same screen.

## Team / members table

List members with role selects and a remove action (use `data-tables` patterns). Guard the last owner: you can't remove or demote the only admin.

## Danger zone

```tsx
<Card className="border-destructive/50">
  <CardHeader>
    <CardTitle className="text-destructive">Danger zone</CardTitle>
    <CardDescription>Irreversible and destructive actions.</CardDescription>
  </CardHeader>
  <CardContent className="flex items-center justify-between">
    <div>
      <p className="font-medium">Delete workspace</p>
      <p className="text-sm text-muted-foreground">Permanently removes all data.</p>
    </div>
    <DeleteWorkspaceDialog /> {/* AlertDialog + type-to-confirm */}
  </CardContent>
</Card>
```

Require typing the workspace name to enable the delete button (see `modals-and-dialogs`).

## Pitfalls

- **One giant form** for everything — group into sections/cards.
- **Mixing autosave toggles with an explicit Save button** — confusing; pick one model per screen.
- **No unsaved-changes warning** — users navigate away and lose edits.
- **Destructive actions next to normal ones** — isolate in a danger zone with confirm.
- **Letting the last admin be removed** — lock yourself out of the org.
- **No mobile treatment** for the section nav — collapse to tabs or a select.

## Hand-off

Configuration screens built from `forms-and-validation`, `data-tables` (members), and `modals-and-dialogs` (destructive confirms); link to `billing-and-pricing` for plan management.
