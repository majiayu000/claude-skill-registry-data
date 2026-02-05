---
name: package-first-development
description: Find existing packages before writing custom code. Uses context7 and websearch to discover battle-tested solutions, maximizes package usage to minimize custom code and complexity. Use when implementing features, adding functionality, or when user requests new capabilities.
version: 1.0.0
---

# Package-First Development

Always search for existing packages before writing custom code. Maximize package usage to minimize complexity.

## Core Philosophy

**Don't build what already exists.**

1. Search for existing packages FIRST
2. Evaluate quality and fit
3. Recommend packages to user
4. User approves selection
5. Only write custom code if no package exists

## Search Process

### Step 1: Use Context7 for Library Documentation

**When user requests a feature, ALWAYS search for packages first:**

```markdown
User wants: "Authentication system with JWT tokens"

Search using Context7:
- Query: "jwt authentication library"
- Find: jsonwebtoken, passport-jwt, jose
- Get documentation for top candidates
```

**Example Context7 queries:**
```
"form validation library react"
"date manipulation library typescript"
"state management library"
"chart visualization library"
"pdf generation library"
```

### Step 2: Use WebSearch for Package Discovery

**Search for battle-tested solutions:**

```markdown
WebSearch queries:
- "best [feature] library for [technology] 2025"
- "[feature] npm package recommendations"
- "how to implement [feature] in [framework]"
- "[feature] library comparison"
```

**Examples:**
```
"best form validation library for React 2025"
"date manipulation npm package recommendations"
"how to implement authentication in Next.js"
"state management library comparison"
```

### Step 3: Evaluate Package Quality

**Check these criteria:**

1. **Popularity**
   - npm downloads per week
   - GitHub stars
   - Used by major projects

2. **Maintenance**
   - Recent updates
   - Active maintainers
   - Issue response time

3. **Quality**
   - Good documentation
   - TypeScript support
   - Test coverage
   - Bundle size

4. **Compatibility**
   - Works with current stack
   - No conflicts with existing packages
   - Active community

**Example evaluation:**

```markdown
## Package Evaluation: React Hook Form

**Popularity:** ✅
- 2M+ weekly downloads
- 37k+ GitHub stars
- Used by Vercel, Stripe, etc.

**Maintenance:** ✅
- Updated 2 weeks ago
- Active maintainers
- Issues resolved quickly

**Quality:** ✅
- Excellent documentation
- Full TypeScript support
- 100% test coverage
- Small bundle size (8.5kb)

**Compatibility:** ✅
- Works with React 18+
- No conflicts with existing packages
- Large community

**Recommendation:** Use React Hook Form for form management
```

## Package Recommendation Format

**Always present options to user, never decide alone:**

```markdown
## Package Recommendations for [Feature]

I found several established packages for [feature]. Here are the top options:

### Option 1: [Package Name] (Recommended)
**Why:** [Main benefits]
**Pros:**
- [Benefit 1]
- [Benefit 2]
- [Benefit 3]

**Cons:**
- [Limitation 1]
- [Limitation 2]

**Usage:**
```bash
npm install [package-name]
```

### Option 2: [Alternative Package]
**Why:** [Alternative benefits]
**Pros:**
- [Benefit 1]
- [Benefit 2]

**Cons:**
- [Limitation 1]
- [Limitation 2]

### Option 3: Custom Implementation
**Only if:**
- No suitable package exists
- Requirements are very specific
- Package overhead too high

**Effort:** [Estimate]
**Risks:** [What could go wrong]

**Which approach would you prefer?**
```

## Common Feature → Package Mappings

### Forms & Validation

**Feature:** Form handling with validation

**Packages:**
- **React Hook Form** - Recommended for React
- **Formik** - Alternative with more features
- **Zod** - Schema validation
- **Yup** - Alternative schema validation

**Usage:**
```typescript
import { useForm } from 'react-hook-form';
import { z } from 'zod';

const schema = z.object({
  email: z.string().email(),
  password: z.string().min(8)
});

function LoginForm() {
  const { register, handleSubmit } = useForm();
  // Form handling with minimal code
}
```

### Date & Time

**Feature:** Date manipulation and formatting

**Packages:**
- **date-fns** - Recommended (modular, tree-shakable)
- **Day.js** - Lightweight alternative
- **Luxon** - For complex timezone needs

**Usage:**
```typescript
import { format, addDays } from 'date-fns';

const tomorrow = addDays(new Date(), 1);
const formatted = format(tomorrow, 'yyyy-MM-dd');
```

### Authentication

**Feature:** User authentication and session management

**Packages:**
- **NextAuth.js** - Recommended for Next.js
- **Passport** - Node.js authentication
- **Auth0** - Managed authentication service
- **Clerk** - Complete user management

**Usage:**
```typescript
import NextAuth from 'next-auth';
import Providers from 'next-auth/providers';

// Complete auth in minimal code
export default NextAuth({
  providers: [
    Providers.Google({
      clientId: process.env.GOOGLE_ID,
      clientSecret: process.env.GOOGLE_SECRET
    })
  ]
});
```

### State Management

**Feature:** Global state management

**Packages:**
- **Zustand** - Recommended (simple, small)
- **Jotai** - Atomic state management
- **Redux Toolkit** - For complex needs
- **React Query** - For server state

**Usage:**
```typescript
import create from 'zustand';

const useStore = create((set) => ({
  count: 0,
  increment: () => set((state) => ({ count: state.count + 1 }))
}));
```

### HTTP Requests

**Feature:** Making API calls

**Packages:**
- **axios** - Recommended (feature-rich)
- **ky** - Modern fetch wrapper
- **React Query** - With built-in caching
- **SWR** - React hooks for data fetching

**Usage:**
```typescript
import axios from 'axios';

const { data } = await axios.get('/api/users');
```

### Data Visualization

**Feature:** Charts and graphs

**Packages:**
- **Recharts** - React charts (recommended)
- **Chart.js** - Canvas-based charts
- **Victory** - React Native compatible
- **visx** - Low-level visualization

**Usage:**
```typescript
import { LineChart, Line } from 'recharts';

<LineChart data={data}>
  <Line dataKey="value" />
</LineChart>
```

### PDF Generation

**Feature:** Create PDF documents

**Packages:**
- **jsPDF** - Client-side PDF generation
- **PDFKit** - Node.js PDF generation
- **React-PDF** - React components to PDF
- **Puppeteer** - HTML to PDF

**Usage:**
```typescript
import jsPDF from 'jspdf';

const doc = new jsPDF();
doc.text('Hello world', 10, 10);
doc.save('document.pdf');
```

### File Upload

**Feature:** File upload with progress

**Packages:**
- **react-dropzone** - Drag & drop (recommended)
- **Uppy** - Complete upload solution
- **Filepond** - Elegant file upload
- **Resumable.js** - Resumable uploads

**Usage:**
```typescript
import { useDropzone } from 'react-dropzone';

function FileUpload() {
  const { getRootProps, getInputProps } = useDropzone({
    onDrop: files => handleUpload(files)
  });

  return <div {...getRootProps()}>Drop files here</div>;
}
```

### Email Sending

**Feature:** Send emails

**Packages:**
- **Nodemailer** - Node.js email (recommended)
- **SendGrid** - Email service
- **Resend** - Modern email API
- **Postmark** - Transactional email

**Usage:**
```typescript
import nodemailer from 'nodemailer';

const transporter = nodemailer.createTransport({
  service: 'gmail',
  auth: { user: 'email', pass: 'password' }
});

await transporter.sendMail({
  to: 'user@example.com',
  subject: 'Hello',
  html: '<p>Hello world</p>'
});
```

### CSS & Styling

**Feature:** Component styling

**Packages:**
- **Tailwind CSS** - Utility-first (recommended)
- **styled-components** - CSS-in-JS
- **emotion** - Performant CSS-in-JS
- **CSS Modules** - Built into Next.js

**Usage:**
```tsx
// Tailwind
<div className="px-4 py-2 bg-blue-500 text-white rounded">
  Button
</div>
```

### Testing

**Feature:** Unit and integration testing

**Packages:**
- **Vitest** - Fast unit testing (recommended)
- **Jest** - Popular testing framework
- **React Testing Library** - React component testing
- **Playwright** - E2E testing

**Usage:**
```typescript
import { test, expect } from 'vitest';

test('adds numbers', () => {
  expect(1 + 1).toBe(2);
});
```

## Conflict Detection

**Check if new package conflicts with existing instructions:**

**Steps:**
1. Review current CLAUDE.md
2. Check existing skills
3. Identify potential conflicts
4. Remove conflicts if found

**Example:**

```markdown
User wants to add: ESLint with specific rules

Current CLAUDE.md says: "No semicolons in code"
New package ESLint config: "Requires semicolons"

**CONFLICT DETECTED**

Options:
1. Update CLAUDE.md to allow semicolons
2. Configure ESLint to match current style (no semicolons)
3. Discuss with user which standard to follow

Which approach would you prefer?
```

## When Custom Code Is Necessary

**Only write custom code if:**

1. **No package exists**
   - Searched thoroughly
   - No suitable solution found

2. **Requirements are very specific**
   - Existing packages don't fit
   - Customization needed is extensive

3. **Package overhead too high**
   - Package is too heavy for simple need
   - Bundle size concerns
   - Performance critical

4. **Security concerns**
   - Package has vulnerabilities
   - Not actively maintained
   - Trustworthiness issues

**Even then, consider:**
- Fork and modify existing package
- Contribute to existing package
- Use package as reference for implementation

## Decision Process Flowchart

```
User requests feature
       ↓
Search for packages (Context7 + WebSearch)
       ↓
Found packages? → NO → Discuss custom implementation
       ↓ YES          with user approval
Evaluate quality
       ↓
Good packages exist? → NO → Custom implementation
       ↓ YES
Present 2-3 options to user
       ↓
User selects package
       ↓
Check for conflicts with existing setup
       ↓
Conflicts? → YES → Resolve or update instructions
       ↓ NO
Implement with selected package
```

## Example Search Sessions

### Example 1: Image Cropping

```markdown
User: "I need to add image cropping functionality"

Search:
- Context7: "image crop library react"
- WebSearch: "best image cropping library for React 2025"

Found:
1. react-image-crop
2. react-easy-crop
3. cropperjs

Evaluation:
**react-easy-crop** - Recommended
- 1.5k+ stars
- Active maintenance
- TypeScript support
- Mobile-friendly gestures
- Small bundle size

Recommendation:
```bash
npm install react-easy-crop
```

Benefits:
✅ Battle-tested (used in production by many)
✅ Easy API
✅ Mobile support
✅ No custom code needed

vs Custom Implementation:
❌ Would take 2-3 days
❌ Need to handle touch gestures
❌ Mobile compatibility issues
❌ Ongoing maintenance

**Should we use react-easy-crop?**
```

### Example 2: Markdown Editor

```markdown
User: "Add markdown editing capability"

Search:
- Context7: "markdown editor react"
- WebSearch: "markdown editor component React 2025"

Found:
1. react-markdown-editor-lite
2. @uiw/react-md-editor
3. react-mde

Evaluation:
**@uiw/react-md-editor** - Recommended
- Simple API
- Preview built-in
- Code syntax highlighting
- Minimal configuration

Alternative: **react-mde**
- More customizable
- More complex API
- Larger bundle

Recommendation:
For simple markdown editing:
```bash
npm install @uiw/react-md-editor
```

For advanced customization:
```bash
npm install react-mde
```

**Which fits your needs better?**
```

## Benefits of Package-First Approach

### Reduces Custom Code
- ✅ Less code to write
- ✅ Less code to maintain
- ✅ Fewer bugs
- ✅ Faster development

### Battle-Tested Solutions
- ✅ Used by thousands
- ✅ Edge cases handled
- ✅ Community support
- ✅ Regular updates

### Focus on Business Logic
- ✅ Spend time on unique features
- ✅ Not reinventing the wheel
- ✅ Faster time to market

### Easier Onboarding
- ✅ Standard tools
- ✅ Known patterns
- ✅ Available documentation

## Summary: Search First, Build Last

**Golden Rules:**

1. **Always Search First**
   - Use Context7 for docs
   - Use WebSearch for packages
   - Find battle-tested solutions

2. **Evaluate Thoroughly**
   - Check popularity
   - Verify maintenance
   - Assess quality
   - Test compatibility

3. **Recommend, Don't Decide**
   - Present 2-3 options
   - Explain pros/cons
   - User makes final choice

4. **Minimize Custom Code**
   - Maximize package usage
   - Reduce complexity
   - Focus on business logic

5. **Check for Conflicts**
   - Review existing instructions
   - Resolve conflicts
   - Update documentation

**Remember:** The best code is code you don't have to write. Use packages to build on the shoulders of giants.
