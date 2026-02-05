---
name: implement-page-or-components
description: Implement a new page in the project
license: MIT
compatibility: opencode
---

## What I do

- read and understand the plan in provided file carefully.
- ask unclear questions.
- implement svelte kit page with lastest rune api. For example: `import type { PageProps } from "./$types";` `const { params, data }: PageProps = $props();` `let isInviteDialogOpen = $state(false);`
- import necessary shad cn components from `@repo/ui`. For example `import * as Card from "@repo/ui/card"`. Components are already installed so no need to reinstall and check exist or not.
- use the `@tanstack/svelte-query` latest api to make api calls if necessary.
- use full import of lucide icons import. For example `import UserPlusIcon from "@lucide/svelte/icons/user-plus";`
- use data table with `@tanstack/table-core` if need to implement table. Also check out tables from `apps/website/src/lib/components/tables` for reference.
- use `@tanstack/svelte-form` if need to implement form.
- follow **Refactoring UI** book design guidelines to implement the UI.

## When to use me

Use this when you are going to design and write code to implement page or components.
Ask clarifying questions if the you are unclear about features or necessary actions.
