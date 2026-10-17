---
name: swiftui-design-skill
description: Anti-AI-slop SwiftUI interface design with 6 Iron Rules, design direction consulting, brand asset integration, and 5-dimension review system
triggers:
  - "design a SwiftUI interface"
  - "create an iOS screen design"
  - "review this SwiftUI design"
  - "suggest design directions"
  - "integrate brand assets into SwiftUI"
  - "check for AI slop patterns"
  - "generate design system tokens"
  - "improve SwiftUI visual hierarchy"
---

# SwiftUI Design Skill

> Skill by [ara.so](https://ara.so) — Design Skills collection.

Transforms single prompts into shippable SwiftUI interfaces that don't look AI-generated. Enforces 6 Iron Rules against AI slop, provides design direction consulting across 5 major design schools, integrates real brand assets, and validates output through a 5-dimension review system.

## Installation

```bash
npx skills add wholiver/swiftui-design-skill -g -y
```

## Core Capabilities

### 1. Anti-AI Slop 6 Iron Rules

Every design must pass these checks before delivery:

**Rule 1: Start from Context**
- ❌ Never invent from scratch
- ✅ Always ask: "Do you have a design system, UI kit, or brand guidelines?"

**Rule 2: Junior Designer Mode**
- ❌ Never wait for perfect solutions
- ✅ Ship gray placeholders over bad AI-generated assets

**Rule 3: Give Variants, Not Finals**
- ❌ Never present one "final answer"
- ✅ Always provide 2-3 differentiated design directions

**Rule 4: Placeholder > Bad Implementation**
```swift
// ❌ BAD: AI-generated clipart
Image("ai-generated-icon")

// ✅ GOOD: Clean placeholder
ZStack {
    RoundedRectangle(cornerRadius: 8)
        .fill(Color.gray.opacity(0.1))
        .frame(width: 80, height: 80)
    Text("Logo")
        .font(.caption)
        .foregroundColor(.secondary)
}
```

**Rule 5: System-First, Don't Fill**
```swift
// ❌ BAD: Filling every pixel
VStack(spacing: 12) {
    HeaderSection()
    SubHeaderSection()
    QuoteOfTheDay()  // Why?
    TrendingHashtags()  // Why?
    SuggestedUsers()  // Why?
}

// ✅ GOOD: Every element justified
VStack(spacing: 24) {
    HeaderSection()  // Navigation
    ContentSection()  // Primary task
}
```

**Rule 6: Ban AI Slop Patterns**

| AI Slop Pattern | ❌ Forbidden | ✅ Alternative |
|-----------------|-------------|----------------|
| Colors | Purple-blue gradients | Single warm accent (amber, coral, sage) |
| Icons | Emoji or rounded blobs | SF Symbols only |
| Typography | Sans-serif everywhere | Serif headlines, legible body |
| Layout | Cards with left accent border | Full-bleed sections or clean cards |
| Shadows | Heavy drop shadows | Subtle elevation (0.05 opacity max) |

### 2. Design Direction Advisor

When requirements are vague, recommend 3 directions from 5 schools:

```swift
// Example: Editorial Direction (NYT-style)
struct ArticleView: View {
    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 32) {
                // Generous top margin
                Spacer().frame(height: 40)
                
                // Serif headline
                Text("The Long-Form Headline That Spans Multiple Lines")
                    .font(.system(size: 34, weight: .bold, design: .serif))
                    .lineSpacing(4)
                    .padding(.horizontal, 24)
                
                // Byline with generous spacing
                Text("By Author Name · 12 min read")
                    .font(.system(size: 14))
                    .foregroundColor(.secondary)
                    .padding(.horizontal, 24)
                    .padding(.bottom, 24)
                
                // Full-bleed image
                Image(systemName: "photo")
                    .resizable()
                    .aspectRatio(16/9, contentMode: .fill)
                    .frame(maxWidth: .infinity)
                
                // Body text with optimal line length
                Text(bodyContent)
                    .font(.system(size: 17, design: .serif))
                    .lineSpacing(6)
                    .padding(.horizontal, 24)
                    .frame(maxWidth: 680)  // Optimal reading width
            }
        }
    }
}
```

**5 Design Schools:**

| School | Use When | Signature Elements |
|--------|----------|-------------------|
| **Informational** | Data-heavy, professional tools | Dense charts, monospace numbers, high contrast |
| **Editorial** | Content-first, reading-focused | Serif type, generous whitespace, full-bleed images |
| **Expressive** | Brand-forward, memorable | Bold color, asymmetric layout, motion |
| **Functional** | Productivity, power users | Dense UI, keyboard shortcuts, monospace accents |
| **Warm Minimal** | Consumer-friendly, approachable | Soft neutrals, rounded corners, subtle texture |

### 3. Brand Asset Integration Protocol

Mandatory 5-step process:

```markdown
## Step 1: Ask
"Do you have brand guidelines, a style guide, or existing design assets?"

## Step 2: Search
Use web_search to find:
- [Brand Name] brand guidelines
- [Brand Name] press kit
- [Brand Name] design system

## Step 3: Download
Use computer tool to download:
- Logo files (SVG/PNG)
- Brand fonts (if available)
- Official documentation

## Step 4: Verify
Cross-check extracted colors against official sources:
- Compare hex values
- Verify color names
- Check contrast ratios

## Step 5: Document
Generate `brand-spec.md` with minimum:
- 5 real brand colors with hex values
- 10 design tokens (spacing, radius, etc.)
- 2 font families
- 8pt spacing grid
```

**Example brand-spec.md:**

```markdown
# Brand Specification: Acme Corp

## Colors
- Primary: #2563EB (Blue 600)
- Secondary: #059669 (Emerald 600)
- Accent: #F59E0B (Amber 500)
- Surface: #FFFFFF
- Background: #F9FAFB (Gray 50)

## Typography
- Headline: Inter Bold, 28-34pt
- Body: Inter Regular, 16-17pt
- Caption: Inter Medium, 12-14pt

## Spacing Scale (8pt grid)
- xs: 8pt
- sm: 16pt
- md: 24pt
- lg: 32pt
- xl: 48pt

## Corner Radius
- sm: 8pt
- md: 12pt
- lg: 16pt
```

### 4. Layout Pattern Library

9 production-ready patterns:

**Pattern 1: Asymmetric Split**
```swift
struct AsymmetricSplitView: View {
    var body: some View {
        GeometryReader { geo in
            HStack(spacing: 0) {
                // Left: 38% width, content
                VStack(alignment: .leading, spacing: 24) {
                    Text("Content")
                        .font(.system(size: 28, weight: .bold))
                }
                .frame(width: geo.size.width * 0.38)
                .padding(32)
                
                // Right: 62% width, visual
                Rectangle()
                    .fill(Color.gray.opacity(0.1))
                    .frame(width: geo.size.width * 0.62)
            }
        }
    }
}
```

**Pattern 2: Editorial Long-Form**
```swift
struct EditorialView: View {
    var body: some View {
        ScrollView {
            VStack(spacing: 0) {
                // Hero
                VStack(alignment: .leading, spacing: 24) {
                    Text("Headline")
                        .font(.system(size: 34, weight: .bold, design: .serif))
                    Text("Subheading")
                        .font(.system(size: 17, design: .serif))
                        .foregroundColor(.secondary)
                }
                .padding(.horizontal, 24)
                .padding(.vertical, 40)
                .frame(maxWidth: 680, alignment: .leading)
                
                // Body
                Text("Content...")
                    .font(.system(size: 17, design: .serif))
                    .lineSpacing(6)
                    .padding(.horizontal, 24)
                    .frame(maxWidth: 680)
            }
        }
    }
}
```

**Pattern 3: Dashboard Grid**
```swift
struct DashboardView: View {
    let columns = [
        GridItem(.flexible(), spacing: 16),
        GridItem(.flexible(), spacing: 16)
    ]
    
    var body: some View {
        ScrollView {
            LazyVGrid(columns: columns, spacing: 16) {
                ForEach(0..<6) { i in
                    MetricCard(title: "Metric \(i)", value: "1,234")
                }
            }
            .padding(16)
        }
    }
}

struct MetricCard: View {
    let title: String
    let value: String
    
    var body: some View {
        VStack(alignment: .leading, spacing: 8) {
            Text(title)
                .font(.system(size: 14, weight: .medium))
                .foregroundColor(.secondary)
            Text(value)
                .font(.system(size: 32, weight: .bold))
        }
        .frame(maxWidth: .infinity, alignment: .leading)
        .padding(20)
        .background(Color.gray.opacity(0.05))
        .cornerRadius(12)
    }
}
```

### 5. Five-Dimension Review System

Before delivery, score each dimension 1-10:

```swift
struct DesignReview {
    let philosophyConsistency: Int  // Does it embody chosen school?
    let visualHierarchy: Int        // Is priority clear?
    let detailExecution: Int        // Spacing/type/color precise?
    let functionality: Int          // Does layout serve goals?
    let originality: Int            // At least 1 signature detail?
    
    var passesThreshold: Bool {
        philosophyConsistency >= 7 &&
        visualHierarchy >= 7 &&
        detailExecution >= 7 &&
        functionality >= 7 &&
        originality >= 7
    }
}
```

**Review Output Format:**
```markdown
## 5-Dimension Review

🎯 Philosophy Consistency: 8/10
✅ Keep: Editorial serif headlines
⚠️ Fix: Add more generous whitespace

📐 Visual Hierarchy: 7/10
✅ Keep: Clear headline > body distinction
🔧 Fix: Increase byline contrast

🔧 Detail Execution: 9/10
✅ Keep: 8pt grid adherence
✨ Quick Win: Increase line spacing by 2pt

⚡ Functionality: 8/10
✅ Keep: Optimal reading width (680pt)
⚠️ Fix: Add scroll indicator

✨ Originality: 7/10
✅ Keep: Asymmetric image placement
🔧 Fix: Add signature color accent
```

## Essential Swift Extensions

**Color System:**
```swift
extension Color {
    static let brandPrimary = Color(hex: "2563EB")
    static let brandSecondary = Color(hex: "059669")
    
    init(hex: String) {
        let hex = hex.trimmingCharacters(in: CharacterSet.alphanumerics.inverted)
        var int: UInt64 = 0
        Scanner(string: hex).scanHexInt64(&int)
        let r, g, b: UInt64
        switch hex.count {
        case 6:
            (r, g, b) = ((int >> 16) & 0xFF, (int >> 8) & 0xFF, int & 0xFF)
        default:
            (r, g, b) = (0, 0, 0)
        }
        self.init(.sRGB, red: Double(r) / 255, green: Double(g) / 255, blue: Double(b) / 255)
    }
}
```

**Typography Scale:**
```swift
extension Font {
    static let displayLarge = Font.system(size: 34, weight: .bold, design: .serif)
    static let headlineLarge = Font.system(size: 28, weight: .bold)
    static let headlineMedium = Font.system(size: 22, weight: .semibold)
    static let bodyLarge = Font.system(size: 17, design: .serif)
    static let bodyMedium = Font.system(size: 15)
    static let caption = Font.system(size: 12, weight: .medium)
}
```

**Spacing System:**
```swift
extension CGFloat {
    static let spacingXS: CGFloat = 8
    static let spacingSM: CGFloat = 16
    static let spacingMD: CGFloat = 24
    static let spacingLG: CGFloat = 32
    static let spacingXL: CGFloat = 48
}
```

**Animation Presets:**
```swift
extension Animation {
    static let softSpring = Animation.spring(response: 0.4, dampingFraction: 0.7)
    static let quickEase = Animation.easeOut(duration: 0.2)
    static let gentleFade = Animation.easeInOut(duration: 0.3)
}
```

## Common Workflows

### Workflow 1: New Interface from Scratch

```
User: "Design a workout tracking screen"

Agent Actions:
1. Ask: "Do you have brand guidelines?"
2. Recommend 3 directions:
   - Functional: Dense metrics, monospace numbers
   - Warm Minimal: Soft colors, encouraging tone
   - Informational: Chart-heavy, progress-focused
3. User chooses Functional
4. Generate code with:
   - 8pt grid spacing
   - Monospace numbers
   - High contrast
   - Dense information layout
5. Run 5-dimension review
6. Deliver with review scores
```

### Workflow 2: Brand Asset Integration

```
User: "Design for Stripe"

Agent Actions:
1. web_search("Stripe brand guidelines")
2. Download assets from stripe.com/newsroom/brand-assets
3. Extract:
   - Primary: #635BFF (Stripe purple)
   - Accent: #00D4FF (Stripe cyan)
   - Fonts: Inter, SF Mono
4. Generate brand-spec.md
5. Create interface using verified colors
6. Run anti-slop check (no purple gradients!)
```

### Workflow 3: Design Review

```
User: "Review this design" [shares code]

Agent Actions:
1. Check 6 Iron Rules:
   - ✅ Uses SF Symbols
   - ❌ Purple-blue gradient detected → Fix
   - ✅ Spacing follows 8pt grid
2. Run 5-dimension scoring
3. Provide item-by-item fixes:
   - Keep: Typography hierarchy
   - Fix: Replace gradient with solid brand color
   - Quick Win: Increase title size by 4pt
4. Generate fixed code
```

## Configuration

Create `.swiftui-design-config.md` in project root:

```markdown
# Design Configuration

## Brand Colors
- Primary: #2563EB
- Secondary: #059669

## Design School
Preferred: Editorial

## Typography
- Headlines: Serif
- Body: Sans-serif

## Spacing Grid
8pt base

## Anti-Slop Overrides
Allow: None (enforce all 6 rules)
```

## Troubleshooting

**Issue: AI keeps generating purple gradients**
```swift
// Add to project rules:
// FORBIDDEN: Any gradient containing purple (#800080 to #9B59B6 range)
// REQUIRED: Single-color backgrounds only

// ✅ Correct approach:
.background(Color.brandPrimary)
```

**Issue: Typography feels generic**
```swift
// Add serif hierarchy:
Text("Headline")
    .font(.system(size: 28, weight: .bold, design: .serif))
    
Text("Body")
    .font(.system(size: 17, design: .default))
    .lineSpacing(6)
```

**Issue: Layout feels cramped**
```swift
// Enforce minimum spacing:
VStack(spacing: .spacingLG) {  // 32pt minimum
    HeaderSection()
    ContentSection()
}
.padding(.horizontal, .spacingMD)  // 24pt minimum
```

**Issue: Design review scores below 7**
- **Philosophy < 7:** Choose a different design school
- **Hierarchy < 7:** Increase size contrast by 4-6pt
- **Detail < 7:** Audit spacing against 8pt grid
- **Functionality < 7:** Remove non-essential elements
- **Originality < 7:** Add one signature detail (asymmetry, color accent, unique spacing)

## Reference Files

- `references/anti-ai-slop.md` — Detailed slop pattern database
- `references/layout-patterns.md` — 9 copy-paste patterns
- `references/typography-color.md` — Complete type scale + color system
- `references/design-review.md` — Review process details
- `references/swift-extensions.md` — Production-ready extensions
- `templates/brand-spec.md` — Brand documentation template

## Quality Checklist

Before delivery, verify:

- [ ] All 6 Iron Rules passed
- [ ] 5-dimension scores ≥ 7/10
- [ ] Code compiles in Xcode
- [ ] SF Symbols only (no emoji/custom icons)
- [ ] 8pt spacing grid followed
- [ ] No purple-blue gradients
- [ ] Typography hierarchy clear (6pt+ size difference)
- [ ] Real brand colors used (if brand context exists)
- [ ] At least 1 signature detail present

---

**Philosophy:** Ship imperfect but honest designs over polished AI slop. Junior designer mode enabled — gray placeholders beat bad implementations.
