---
name: scaffold-component
description: Generate a new React component following project conventions. Use when creating new components or UI features.
argument-hint: <ComponentName>
---

Create a new React component named `$ARGUMENTS` following project conventions:

1. **Create the component file** at `client/src/components/$ARGUMENTS.tsx`

2. **Follow this structure:**
   ```typescript
   import React from 'react';
   // Icons (if needed)
   // Types (if needed)

   interface Props {
     // Define props here
   }

   export function $ARGUMENTS({ ...props }: Props) {
     // State hooks

     // Handler functions

     return (
       <section className="bg-white rounded border border-slate-200 p-4">
         <h3 className="font-bold text-brand-navy mb-4">Title</h3>
         {/* Content */}
       </section>
     );
   }
   ```

3. **Conventions:**
   - Use function components (not arrow functions for exports)
   - Interface for Props comes first
   - Imports order: React, Icons, Types, local imports
   - Use Tailwind CSS classes
   - Use `brand-navy` for headings

4. **After creation:**
   - Add export to `client/src/components/index.ts` if it exists
   - Run build to verify no type errors
