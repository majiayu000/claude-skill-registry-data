---
name: ux-heuristics
description: 'Usability heuristics and principles based on Steve Krug''s "Don''t Make Me Think" and Jakob Nielsen''s 10 heuristics. Use when you need to: (1) audit a UI for usability problems, (2) identify why users are confused or frustrated, (3) simplify navigation and information architecture, (4) conduct heuristic evaluations, (5) prioritize UX fixes by severity, (6) review designs before development, (7) improve form usability, (8) validate that interfaces follow established UX principles.'
license: MIT
metadata:
  author: wondelai
  version: "1.1.0"
---

# UX Heuristics Framework

Practical usability principles for evaluating and improving user interfaces. Based on a fundamental truth: users don't read, they scan. They don't make optimal choices, they satisfice. They don't figure out how things work, they muddle through.

## Core Principle

**"Don't Make Me Think"** - Every page should be self-evident. If something requires thinking, it's a usability problem.

**The foundation:** Users have limited patience and cognitive bandwidth. The best interfaces are invisible -- they let users accomplish goals without ever stopping to wonder "What do I click?" or "Where am I?" Every question mark that pops into a user's head adds to cognitive load and increases the chance they'll leave. Design for scanning, satisficing, and muddling through -- because that's what users actually do.

## Scoring

**Goal: 10/10.** When reviewing or creating user interfaces, rate them 0-10 based on adherence to the principles below. A 10/10 means full alignment with all guidelines; lower scores indicate gaps to address. Always provide the current score and specific improvements needed to reach 10/10.

## Krug's Three Laws of Usability

### 1. Don't Make Me Think

**Core concept:** Every question mark that pops into a user's head adds to their cognitive load and distracts from the task.

**Why it works:** Users are on a mission. They don't want to puzzle over labels, wonder what a link does, or decode clever marketing language. The less thinking required, the more likely they complete the task.

**Key insights:**
- Clever names lose to clear names every time
- Marketing-speak creates friction; plain language removes it
- Unfamiliar categories and labels force users to stop and interpret
- Links that could go anywhere create uncertainty
- Buttons with ambiguous labels cause hesitation

**Product applications:**

| Context | Application | Example |
|---------|-------------|---------|
| **Navigation labels** | Use self-evident names | "Get directions" not "Calculate route to destination" |
| **CTAs** | Use action verbs users understand | "Sign in" not "Access your account portal" |
| **E-commerce** | Match user mental models | "Add to cart" not "Proceed to purchase selection" |
| **Form labels** | Describe what's needed plainly | "Email address" not "Electronic correspondence identifier" |
| **Error states** | Tell users what to do next | "Check your email format" not "Validation error" |

**Copy patterns:**
- Self-evident labels: "Sign in", "Search", "Add to cart"
- Action-oriented buttons: verb + noun ("Create account", "Download report")
- Avoid jargon: "Save" not "Persist", "Remove" not "Disassociate"
- If a label needs explanation, simplify the label

**Ethical boundary:** Clarity should serve users, not obscure information. Never use plain language as a veneer to hide unfavorable terms.

See: [references/krug-principles.md](references/krug-principles.md) for full Krug methodology.

### 2. It Doesn't Matter How Many Clicks

**Core concept:** The myth says "users leave after 3 clicks." The reality is users don't mind clicks if each one is painless, obvious, and confidence-building.

**Why it works:** Cognitive effort per click matters more than click count. Three mindless, confident clicks are far better than one click that requires deliberation. Users abandon when they lose confidence, not when they run out of patience for clicking.

**Key insights:**
- Each click should be painless (fast, easy)
- Each click should be obvious (no thinking required)
- Each click should build confidence (users know they're on the right path)
- Three mindless clicks beat one confusing click every time
- Users abandon when confused, not when they've clicked too many times

**Product applications:**

| Context | Application | Example |
|---------|-------------|---------|
| **Information architecture** | Prioritize clarity over depth | Shallow nav with clear labels over deep nav with vague ones |
| **Checkout flows** | Make each step obvious | Clear step indicators with descriptive labels |
| **Settings** | Organize into clear categories | "Account > Security > Change password" (3 confident clicks) |
| **Search results** | Let users drill down confidently | Category filters that narrow results progressively |
| **Onboarding** | Guide with small, clear steps | Wizard with one clear action per step |

**Copy patterns:**
- Progress indicators: "Step 2 of 4: Shipping details"
- Breadcrumbs: "Home > Products > Shoes > Running"
- Confirmations at each step: "Great, your email is verified. Now let's set up your profile."
- Clear link text: "View all running shoes" not "Click here"

**Ethical boundary:** Don't use extra steps to bury cancellation flows or make opting out harder. Every click should move users toward their goal, not away from it.

See: [references/krug-principles.md](references/krug-principles.md) for Krug's click philosophy and scanning behavior.

### 3. Get Rid of Half the Words

**Core concept:** Get rid of half the words on each page, then get rid of half of what's left. Brevity reduces noise, makes useful content more prominent, and shows respect for the user's time.

**Why it works:** Users scan -- they don't read. Every unnecessary word competes with the words that matter. Removing fluff makes important content more discoverable and pages shorter.

**Key insights:**
- Happy-talk ("Welcome to our website!") wastes space
- Instructions nobody reads should be removed
- "Please" and "Kindly" and polite fluff add noise
- Redundant explanations dilute the message
- Shorter pages mean less scrolling and faster scanning

**Product applications:**

| Context | Application | Example |
|---------|-------------|---------|
| **Landing pages** | Cut welcome copy, lead with value | Remove "Welcome to..." paragraphs |
| **Error messages** | State problem and fix, nothing more | "Password too short (min 8 chars)" not a paragraph |
| **Tooltips** | One sentence max | "Last 4 digits of your card" not a full explanation |
| **Empty states** | Action-oriented, minimal | "No results. Try a different search." |
| **Onboarding** | One instruction per screen | "Choose your interests" not a wall of explanatory text |

**Copy patterns:**
- Before: "Please kindly note that you will need to enter your password in order to proceed to the next step."
- After: "Enter your password to continue."
- Before: "We've received your message and will get back to you as soon as possible."
- After: "Message sent. We'll reply within 24 hours."

**Ethical boundary:** Brevity must not mean omitting critical information. Concise disclosures for pricing, terms, and data usage are a user right.

See: [references/krug-principles.md](references/krug-principles.md) for Krug's word-cutting methodology.

### 4. The Trunk Test

**Core concept:** A test for navigation clarity: if users were dropped on any random page (like being locked in a car trunk and released at a random spot), could they instantly answer six key questions?

**Why it works:** Good navigation gives users constant orientation. If users can't identify where they are and what their options are, they feel lost and leave.

**Key insights:**
- Users must know what site they're on (brand/logo visible)
- Users must know what page they're on (clear heading)
- Major sections must be visible (navigation)
- Options at this level must be clear (links/buttons)
- Position in hierarchy must be apparent (breadcrumbs)
- Search must be findable

**Product applications:**

| Context | Application | Example |
|---------|-------------|---------|
| **Global nav** | Persistent site ID and sections | Logo top-left, main nav always visible |
| **Page headers** | Clear, descriptive page titles | "Running Shoes - Men's" not just "Products" |
| **Breadcrumbs** | Show hierarchy on all inner pages | "Home > Products > Shoes > Running" |
| **Mobile nav** | Maintain orientation in hamburger menus | Highlight current section, show breadcrumbs |
| **Search** | Visible search on every page | Search box in header, not buried in footer |

**Copy patterns:**
- Page titles that match the link the user clicked
- "You are here" indicators (highlighted nav items, bold breadcrumb)
- Section headings that orient: "Your Account > Billing" not just "Settings"
- Footer navigation for secondary discovery

**Ethical boundary:** Navigation should honestly represent site structure. Don't use misleading labels to funnel users into marketing pages.

See: [references/krug-principles.md](references/krug-principles.md) for the full Trunk Test methodology.

## Nielsen's 10 Usability Heuristics

### 1. Visibility of System Status

**Core concept:** The system should always keep users informed about what is going on, through appropriate feedback within reasonable time.

**Why it works:** When users don't know the system's state, they assume it's broken. Anxiety and confusion lead to repeated clicks, abandoned tasks, and lost trust. Visible status creates confidence.

**Key insights:**
- Every action needs immediate visual acknowledgment
- Long operations need progress indicators (percentage, spinner, skeleton screen)
- Successful actions need confirmation ("Saved!", checkmark)
- Silent failures are worse than visible errors
- Status should be proportional to importance (subtle for minor, prominent for critical)

**Product applications:**

| Context | Status Feedback | Example |
|---------|----------------|---------|
| **File upload** | Progress bar with percentage | "Uploading... 67%" |
| **Form submit** | Success confirmation | "Your message has been sent" with checkmark |
| **Background sync** | Non-intrusive notification | "Syncing 3 files..." in status bar |
| **Payment processing** | Clear progress with reassurance | "Processing your payment... don't close this page" |
| **Search** | Loading skeleton then results | Skeleton screens that match result layout |

**Copy patterns:**
- "Saving..." / "Saved" (immediate state transitions)
- "Processing your request..." (for operations > 1 second)
- "Upload complete. 3 files added." (specific confirmation)
- "Something went wrong. Please try again." (failure with action)

**Ethical boundary:** Status indicators should be honest. Don't show fake progress bars or artificial loading delays to create a perception of "work being done."

See: [references/nielsen-heuristics.md](references/nielsen-heuristics.md) for detailed examples and severity ratings.

### 2. Match Between System and Real World

**Core concept:** The system should speak the users' language, with words, phrases, and concepts familiar to the user, rather than system-oriented terms.

**Why it works:** Users bring mental models from the real world. When digital interfaces match these models -- using familiar language, logical sequences, and recognizable metaphors -- users feel oriented and confident.

**Key insights:**
- Use "Sign in" not "Authenticate", "Search" not "Query", "Folder" not "Repository"
- Real-world metaphors reduce learning curve (trash bin, shopping cart, bookmark)
- Information should appear in a natural, logical order
- Icons should match real-world objects users already recognize
- One term per concept -- never use different words for the same thing

**Product applications:**

| Context | Real-World Match | Example |
|---------|-----------------|---------|
| **Labels** | User-tested terms over internal names | "Search" not "Query", "Cancel" not "Terminate" |
| **Metaphors** | Digital elements mirror physical | Trash bin, folder, desktop, shopping cart |
| **Sequences** | Follow real-world order | Address form: street, city, state, zip (not zip first) |
| **Icons** | Recognizable real-world objects | Magnifying glass for search, envelope for email |
| **Categories** | Match user mental models | Grocery app: "Fruits & Vegetables" not "Produce SKU Group" |

**Copy patterns:**
- "Go to" not "Navigate to"
- "Start" not "Initiate"
- "End" not "Terminate session"
- "Your files" not "User repository contents"

**Ethical boundary:** Don't use real-world metaphors to deceive -- e.g., a "close" button that actually submits a form, or a "free" label that hides costs.

See: [references/nielsen-heuristics.md](references/nielsen-heuristics.md) for language mapping examples.

### 3. User Control and Freedom

**Core concept:** Users often choose system functions by mistake and need a clearly marked "emergency exit" to leave the unwanted state without having to go through an extended dialogue.

**Why it works:** Users explore by clicking. Without easy escape routes, they become afraid to act. Undo is superior to confirmation dialogs because users click through "Are you sure?" without reading, but undo lets them act confidently knowing they can reverse.

**Key insights:**
- Undo is always better than "Are you sure?" confirmation dialogs
- Every flow needs a visible cancel/exit option
- The back button must never be broken or hijacked
- Forced wizards without skip or back options trap users
- Soft delete with undo beats immediate permanent deletion

**Product applications:**

| Context | Control Mechanism | Example |
|---------|-------------------|---------|
| **Email** | Undo send | Gmail's "Undo" toast after sending |
| **Navigation** | Back button always works | Never hijack browser history |
| **Modals** | Clear close/cancel buttons | "X" button plus "Cancel" text link |
| **Wizards** | Non-linear navigation | Allow jumping to previous steps |
| **Destructive actions** | Soft delete + undo | "Message deleted. Undo" (timed) |

**Copy patterns:**
- "Undo" (single-word, immediate, low-friction)
- "Cancel" (always present alongside primary action)
- "Go back" (clear escape from unwanted state)
- "Exit without saving" (honest about consequences)

**Ethical boundary:** Never make it easy to enter a state (subscription, trial, commitment) but hard to leave. Roach motel patterns -- easy in, hard out -- are a dark pattern.

See: [references/nielsen-heuristics.md](references/nielsen-heuristics.md) for control and freedom patterns.

### 4. Consistency and Standards

**Core concept:** Users should not have to wonder whether different words, situations, or actions mean the same thing. Follow platform conventions.

**Why it works:** Consistency reduces learning. When the same patterns work everywhere, users transfer knowledge between pages and products. Breaking conventions forces re-learning and creates confusion.

**Key insights:**
- Internal consistency: same button style, terms, and behaviors throughout your app
- External consistency: follow platform conventions (logo top-left, search top-right, cart icon)
- Visual consistency: same colors always mean the same things
- Functional consistency: same action always produces the same result
- Linguistic consistency: one term per concept, everywhere

**Product applications:**

| Context | Consistency Standard | Example |
|---------|---------------------|---------|
| **Buttons** | Same style hierarchy everywhere | Primary (filled), secondary (outlined), text link |
| **Layout** | Logo top-left, links to home | Industry convention users expect |
| **Terminology** | One word per concept | Always "Sign in", never mix with "Log in" |
| **Behavior** | Links open consistently | Don't surprise with new tabs |
| **Forms** | Primary action right/bottom | "Submit" on the right, "Cancel" on the left |

**Copy patterns:**
- Pick one term and use it everywhere ("Projects" not sometimes "Projects" and sometimes "Workspaces")
- Follow platform language ("Share" on mobile, "Send link" in email context)
- Button labels should predict outcomes ("Save changes" not just "OK")
- Error formats should be identical throughout the app

**Ethical boundary:** Consistency should not be weaponized. Don't make "Accept" and "Decline" look identical to trick users into accepting terms they didn't read.

See: [references/nielsen-heuristics.md](references/nielsen-heuristics.md) for consistency types and platform conventions.

### 5. Error Prevention

**Core concept:** Even better than good error messages is a careful design which prevents a problem from occurring in the first place.

**Why it works:** The cheapest error to fix is one that never happens. Constraints, suggestions, defaults, and warnings eliminate entire categories of user mistakes before they occur.

**Key insights:**
- Constrained inputs (date pickers, dropdowns) prevent invalid entries
- Autocomplete and suggestions reduce typos and wrong choices
- Sensible defaults pre-fill common values so users don't have to guess
- "Unsaved changes" warnings prevent lost work
- There are two error types: slips (accidental wrong action) and mistakes (wrong intention) -- each needs different prevention

**Product applications:**

| Context | Prevention Strategy | Example |
|---------|-------------------|---------|
| **Date input** | Constrained picker | Calendar widget instead of free text field |
| **Search** | Autocomplete suggestions | Dropdown with matching results as user types |
| **Forms** | Inline validation on blur | "Email must include @" shown before submit |
| **Destructive actions** | Confirmation for irreversible | "Delete permanently? This cannot be undone." |
| **Data entry** | Smart defaults | Pre-fill country based on IP, pre-select common options |

**Copy patterns:**
- Inline validation: "Password must be at least 8 characters" (shown while typing)
- Save warnings: "You have unsaved changes. Leave anyway?"
- Format hints: "MM/DD/YYYY" as placeholder text
- Destructive confirmations: "Delete 3 items permanently? This cannot be undone."

**Ethical boundary:** Error prevention should protect users, not restrict them. Don't use "prevention" as an excuse to block legitimate actions (e.g., preventing unsubscribe by showing warnings).

See: [references/nielsen-heuristics.md](references/nielsen-heuristics.md) for prevention strategies by error type.

### 6. Recognition Rather Than Recall

**Core concept:** Minimize the user's memory load by making objects, actions, and options visible. Don't require users to remember information from one part of the interface to another.

**Why it works:** Human working memory is limited (roughly 7 items). Recognition is dramatically easier than recall. Showing options, recent items, and contextual information eliminates the need for memorization.

**Key insights:**
- Show menus of options instead of requiring typed commands
- Provide dropdowns and autocomplete instead of empty fields requiring memorization
- Display breadcrumbs and recent history so users know where they've been
- Show decoded values (country names, not codes)
- Pre-fill information from previous steps so users don't re-enter data

**Product applications:**

| Context | Recognition Technique | Example |
|---------|----------------------|---------|
| **Navigation** | Breadcrumbs, recent history | "Home > Products > Shoes" trail |
| **Search** | Recent searches, suggestions | "Recent: running shoes, Nike Air Max" |
| **Forms** | Pre-filled fields from prior steps | Email pre-populated from login |
| **Data entry** | Dropdowns with decoded values | Country dropdown, not "Enter 2-letter code" |
| **Settings** | Current values shown | "Notifications: On (email, push)" visible |

**Copy patterns:**
- Placeholder examples: "e.g., john@example.com"
- Contextual reminders: "You selected the Pro plan ($29/mo)"
- Recent items: "Recently viewed: Dashboard, Settings, Reports"
- Inline documentation: tooltips with "?" icons next to non-obvious fields

**Ethical boundary:** Making options visible should not include manipulative defaults. Pre-selected checkboxes for marketing consent or add-ons exploit recognition bias.

See: [references/nielsen-heuristics.md](references/nielsen-heuristics.md) for recognition techniques and examples.

### 7. Flexibility and Efficiency of Use

**Core concept:** Accelerators -- unseen by the novice user -- may often speed up the interaction for the expert user. Allow users to tailor frequent actions.

**Why it works:** Novices and experts have different needs. Progressive disclosure keeps things simple for beginners while accelerators let power users move fast. The best interfaces serve both without compromise.

**Key insights:**
- Keyboard shortcuts (Ctrl+S) speed up expert workflows
- Touch gestures (swipe to archive) reduce tap count
- Recent/favorites provide quick access to common items
- Bulk actions eliminate tedious repetition
- Customization lets users tailor the interface to their workflow
- Progressive disclosure: novices see essentials, experts access full power

**Product applications:**

| Context | Accelerator | Example |
|---------|-------------|---------|
| **Email** | Keyboard shortcuts | "E" to archive, "R" to reply in Gmail |
| **Lists** | Bulk actions | Select all > Move to folder |
| **Dashboards** | Customization | Drag-and-drop widget arrangement |
| **Search** | Saved searches/filters | "My filter: Open bugs assigned to me" |
| **Navigation** | Command palette | Cmd+K to jump anywhere (Slack, VS Code) |

**Copy patterns:**
- Shortcut hints: "Ctrl+S to save" shown in tooltip
- "Customize this view" (for dashboard personalization)
- "Advanced options" (expandable for power users)
- Tutorial skip: "Already know the basics? Skip setup"

**Ethical boundary:** Efficiency features should never be paywalled if they address basic usability. Don't make essential shortcuts "premium" while leaving free users with a deliberately slow experience.

See: [references/nielsen-heuristics.md](references/nielsen-heuristics.md) for accelerator patterns and progressive disclosure.

### 8. Aesthetic and Minimalist Design

**Core concept:** Dialogues should not contain information which is irrelevant or rarely needed. Every extra unit of information competes with the relevant units and diminishes their relative visibility.

**Why it works:** Signal-to-noise ratio determines usability. When everything screams for attention, nothing stands out. Whitespace, hierarchy, and ruthless prioritization make interfaces scannable and fast.

**Key insights:**
- Increase signal, reduce noise -- every element must earn its place
- Visual hierarchy makes important things stand out (size, color, position)
- Whitespace gives elements room to breathe and aids scanning
- Show what matters now, hide what doesn't (progressive disclosure)
- If everything is "important," nothing is important

**Product applications:**

| Context | Minimalist Approach | Example |
|---------|-------------------|---------|
| **Dashboards** | Show key metrics, hide details | 3-5 KPIs visible, "See details" for the rest |
| **Forms** | Remove optional fields | Only ask what's truly required |
| **Landing pages** | One primary CTA | Single "Start free trial" button, not five competing CTAs |
| **Settings** | Group and hide rarely-used options | "Advanced settings" collapsed by default |
| **Content** | Break up walls of text | Short paragraphs, headings, bullet lists |

**Copy patterns:**
- Headlines over paragraphs: lead with the key message
- "Show more" / "See details" for secondary information
- Remove "Welcome to..." happy-talk
- One instruction per screen in onboarding

**Ethical boundary:** Minimalism must not hide critical information. Terms, pricing, data usage, and cancellation options must remain discoverable. Hiding unfavorable content under "Show more" is deceptive.

See: [references/nielsen-heuristics.md](references/nielsen-heuristics.md) for minimalist design principles.

### 9. Help Users Recognize, Diagnose, and Recover from Errors

**Core concept:** Error messages should be expressed in plain language (no codes), precisely indicate the problem, and constructively suggest a solution.

**Why it works:** Errors are inevitable. What matters is whether users can understand what happened and get back on track. Technical jargon, generic messages, and blame create frustration; plain language, specificity, and next steps create recovery.

**Key insights:**
- Every error message needs three parts: what happened, why, and how to fix it
- Plain language always: "Connection failed" not "ECONNREFUSED"
- Be specific: "Password must be at least 8 characters" not "Invalid password"
- Never blame the user: "Card declined" not "You entered wrong information"
- Preserve user input on error -- never clear the form as punishment

**Product applications:**

| Context | Error Recovery | Example |
|---------|---------------|---------|
| **Form validation** | Inline, specific, preserves input | Red outline on field + "Email must include @" |
| **Payment errors** | Clear reason + alternative | "Card declined. Try a different card or contact your bank." |
| **Server errors** | Friendly fallback + retry | "Something went wrong. Try again or contact support." |
| **404 pages** | Helpful direction | "Page not found. Try searching or go to the homepage." |
| **Auth errors** | Specific without security risk | "Incorrect password" (not "Account not found" which leaks info) |

**Copy patterns:**
- "Couldn't save. Check your connection and try again." (what + fix)
- "Email already in use. Sign in instead?" (problem + next step)
- "Password must include a number and be 8+ characters." (specific requirement)
- "We hit a snag. Your work is saved -- try refreshing." (reassurance + action)

**Ethical boundary:** Error states should help users recover, not be used to funnel them into unwanted paths (e.g., "Error: upgrade to Premium to continue").

See: [references/nielsen-heuristics.md](references/nielsen-heuristics.md) for error message guidelines and examples.

### 10. Help and Documentation

**Core concept:** Even though it's better if the system can be used without documentation, it may be necessary to provide help. Such information should be easy to search, focused on the user's task, and concise.

**Why it works:** Users resort to help when they're stuck. If help is hard to find, unsearchable, or written in developer-speak, it fails at the moment it's needed most. Good help is contextual, task-focused, and brief.

**Key insights:**
- Help should be searchable with full-text search
- Task-focused format: "How to..." rather than technical reference
- Contextual help (tooltips, inline hints) keeps users in flow
- Documentation should be scannable: short paragraphs, lists, steps
- Types: inline help (tooltips), contextual ("?" icons), docs (knowledge base), guided tours, live support

**Product applications:**

| Context | Help Type | Example |
|---------|-----------|---------|
| **Complex fields** | Inline tooltips | "?" icon next to "APR" with plain-language definition |
| **New features** | Guided tour | Step-by-step overlay highlighting new UI elements |
| **Settings** | Contextual descriptions | Short explanation under each toggle |
| **Knowledge base** | Searchable docs | Full-text search with task-focused "How to..." articles |
| **Edge cases** | Live support | Chat widget that appears after user shows frustration signals |

**Copy patterns:**
- Tooltip: "Your API key. Find it in Settings > Developer." (concise, actionable)
- Guide step: "Click 'Create project' to get started." (one action per step)
- FAQ: "How do I cancel my subscription?" (user's question, not yours)
- Search placeholder: "Search help articles..." (clear purpose)

**Ethical boundary:** Help should be genuinely helpful. Don't bury cancellation or deletion instructions behind layers of documentation while making upgrade paths prominently documented.

See: [references/nielsen-heuristics.md](references/nielsen-heuristics.md) for help documentation patterns.

## Severity Rating Scale

When auditing interfaces, rate each issue:

| Severity | Rating | Description | Priority |
|----------|--------|-------------|----------|
| **0** | Not a problem | Disagreement, not usability issue | Ignore |
| **1** | Cosmetic | Minor annoyance, low impact | Fix if time |
| **2** | Minor | Causes delay or frustration | Schedule fix |
| **3** | Major | Significant task failure | Fix soon |
| **4** | Catastrophic | Prevents task completion | Fix immediately |

### Rating Factors

Consider all three:

1. **Frequency:** How often does it occur?
2. **Impact:** How severe when it occurs?
3. **Persistence:** One-time or ongoing problem?

## Common Mistakes

| Mistake | Why It Fails | Fix |
|---------|-------------|------|
| **Mystery meat navigation** | Icons without labels force guessing | Add text labels alongside icons |
| **Too many choices** | Decision paralysis slows users | Reduce to 7 plus/minus 2 items |
| **No "you are here" indicator** | Users feel lost in the hierarchy | Highlight current section in nav and breadcrumbs |
| **No inline validation** | Submit, error, scroll cycle frustrates | Validate on blur with specific messages |
| **Unclear required fields** | Users confused about what's mandatory | Mark optional fields, not required (most fields should be required) |
| **Wall of text** | Nobody reads dense paragraphs | Break up with headings, bullets, whitespace |
| **Jargon in labels** | Users don't speak your internal language | User-test all labels, use plain language |
| **No loading indicators** | Users think the system is broken | Show spinner, progress bar, or skeleton screen |
| **Tiny tap targets** | Mobile users misclick constantly | Minimum 44x44 px touch targets |
| **Hover-only information** | Mobile and keyboard users miss it entirely | Don't hide critical info behind hover states |
| **No undo** | Users afraid to take any action | Provide undo for all non-destructive actions |
| **Poor error messages** | "Invalid input" tells users nothing | Explain what's wrong and how to fix it |
| **Low contrast text** | Unreadable for many users | WCAG AA minimum (4.5:1 contrast ratio) |
| **Inconsistent nav location** | Users can't find navigation | Fixed position, same location on every page |
| **Broken back button** | Fundamental browser contract violated | Never hijack or break browser history |

## Quick Diagnostic

Audit any interface:

| Question | If No | Action |
|----------|-------|--------|
| Can I tell what site/page this is immediately? | Users are lost and disoriented | Add clear logo, page title, and breadcrumbs |
| Is the main action obvious? | Users don't know what to do | Create visual hierarchy, single primary CTA |
| Is the navigation clear? | Users can't find their way | Apply the Trunk Test, add "you are here" indicators |
| Can I find the search? | Users with specific goals are blocked | Add visible search box in header |
| Does the system show me what's happening? | Users lose trust and re-click | Add loading states, confirmations, progress indicators |
| Are error messages helpful? | Users get stuck on errors | Rewrite in plain language with specific fix |
| Can users undo or go back? | Users are afraid to act | Add undo, cancel, and back options everywhere |
| Does it work without hover? | Mobile and keyboard users are excluded | Replace hover-only interactions with visible alternatives |
| Are all interactive elements labeled? | Users guess at icon meanings | Add text labels or descriptive tooltips |
| Does anything make me stop and think "huh?" | Cognitive load is too high | Simplify -- if it needs explanation, redesign it |

## Heuristic Conflicts

Heuristics sometimes contradict each other. When they do:
- **Simplicity vs. Flexibility**: Use progressive disclosure
- **Consistency vs. Context**: Consistent patterns, contextual prominence
- **Efficiency vs. Error Prevention**: Prefer undo over confirmation dialogs
- **Discoverability vs. Minimalism**: Primary actions visible, secondary hidden

See: [references/heuristic-conflicts.md](references/heuristic-conflicts.md) for resolution frameworks.

## Dark Patterns Recognition

Dark patterns violate heuristics deliberately to manipulate users:
- Forced continuity (hard to cancel)
- Roach motel (easy in, hard out)
- Confirmshaming (guilt-based options)
- Hidden costs (surprise fees at checkout)

See: [references/dark-patterns.md](references/dark-patterns.md) for complete taxonomy and ethical alternatives.

## When to Use Each Method

| Method | When | Time | Findings |
|--------|------|------|----------|
| Heuristic evaluation | Before user testing | 1-2 hours | Major violations |
| User testing | After heuristic fixes | 2-4 hours | Real behavior |
| A/B testing | When optimizing | Days-weeks | Statistical validation |
| Analytics review | Ongoing | 30 min | Patterns and problems |

## Reference Files

- [krug-principles.md](references/krug-principles.md): Full Krug methodology, scanning behavior, navigation clarity
- [nielsen-heuristics.md](references/nielsen-heuristics.md): Detailed heuristic explanations with examples
- [audit-template.md](references/audit-template.md): Structured heuristic evaluation template
- [dark-patterns.md](references/dark-patterns.md): Categories, examples, ethical alternatives, regulations
- [wcag-checklist.md](references/wcag-checklist.md): Complete WCAG 2.1 AA checklist, testing tools
- [cultural-ux.md](references/cultural-ux.md): RTL, color meanings, form conventions, localization
- [heuristic-conflicts.md](references/heuristic-conflicts.md): When heuristics contradict, resolution frameworks

## Further Reading

This skill is based on usability principles developed by Steve Krug and Jakob Nielsen:

- [*"Don't Make Me Think, Revisited"*](https://www.amazon.com/Dont-Make-Think-Revisited-Usability/dp/0321965515?tag=wondelai00-20) by Steve Krug
- [*"Rocket Surgery Made Easy"*](https://www.amazon.com/Rocket-Surgery-Made-Easy-Yourself/dp/0321657292?tag=wondelai00-20) by Steve Krug (DIY usability testing)
- [*"10 Usability Heuristics for User Interface Design"*](https://www.nngroup.com/articles/ten-usability-heuristics/) by Jakob Nielsen (Nielsen Norman Group)

## About the Author

**Steve Krug** is a usability consultant who has been helping companies make their products more intuitive since the 1990s. His book *"Don't Make Me Think"* (first published in 2000, revised 2014) is the most widely read book on web usability and is considered essential reading for anyone involved in designing interfaces. Known for his accessible, humorous writing style and his advocacy for low-cost usability testing, Krug demonstrated that usability doesn't require a lab or a large budget -- just watching a few real users try to accomplish tasks.

**Jakob Nielsen, PhD** is co-founder of the Nielsen Norman Group (NN/g) and is widely regarded as the "king of usability." His 10 Usability Heuristics for User Interface Design, published in 1994, remain the most-used framework for heuristic evaluation worldwide. Nielsen has been called "the guru of Web page usability" by *The New York Times* and has authored numerous influential books on usability engineering. His research-driven approach to interface design helped establish usability as a recognized discipline in software development.
