---
name: content-type-modeling
description: Use when designing content type hierarchies, defining reusable content parts, or structuring field compositions for a headless CMS. Covers the Content Type -> Content Part -> Content Field hierarchy pattern, content type inheritance, composition vs inheritance trade-offs, and schema design for maximum reusability across channels.
allowed-tools: Read, Glob, Grep, Task, Skill, AskUserQuestion
---

# Content Type Modeling

## Interactive Modeling Configuration

Use AskUserQuestion to configure the content type modeling session:

```yaml
# Question 1: Modeling Scope (MCP: CMS content architecture patterns)
question: "What content type modeling do you need?"
header: "Scope"
options:
  - label: "Single Type (Recommended)"
    description: "Design one content type with parts and fields"
  - label: "Type Family"
    description: "Related content types sharing common parts"
  - label: "Full Taxonomy"
    description: "Complete content model with relationships"
  - label: "Migration"
    description: "Migrate from traditional to structured content"

# Question 2: Reusability Strategy (MCP: Orchard Core content patterns)
question: "How should content parts be structured?"
header: "Reuse"
options:
  - label: "Composition (Recommended)"
    description: "Build types from reusable parts - maximum flexibility"
  - label: "Inheritance"
    description: "Base types with specialized extensions"
  - label: "Hybrid"
    description: "Mix of composition and inheritance"
  - label: "Flat"
    description: "Standalone fields on each type - no shared parts"
```

Use these responses to determine modeling scope and composition strategy.

Guidance for designing content type hierarchies, reusable parts, and field compositions for headless CMS architectures.

## When to Use This Skill

- Designing content type schemas for a new CMS
- Defining reusable content parts across multiple types
- Structuring custom field compositions
- Planning content type inheritance strategies
- Migrating from traditional to structured content
- Creating multi-channel content architectures

## The Three-Level Hierarchy

Headless CMS platforms typically use a three-level content hierarchy inspired by patterns from Orchard Core and similar platforms:

```text
Content Type (e.g., "Blog Post", "Product", "Event")
├── Content Parts (reusable groups of fields)
│   ├── TitlePart (title, display title)
│   ├── AutoroutePart (slug, URL pattern)
│   ├── PublishLaterPart (scheduled publishing)
│   └── [Custom Parts]
└── Content Fields (individual data elements)
    ├── TextField (single-line, multi-line)
    ├── HtmlField (rich text)
    ├── MediaField (images, documents)
    ├── ContentPickerField (references)
    └── [Custom Fields]
```

### Content Types

Content Types are the blueprint for content items. They define what parts and fields are available.

```yaml
content_type:
  name: BlogPost
  display_name: Blog Post
  description: A blog article with author and categories
  stereotype: Content  # Content, Widget, MenuItem
  creatable: true
  listable: true
  draftable: true
  versionable: true
  securable: true
```

**Key Decisions:**

| Decision | Options | Recommendation |
| -------- | ------- | -------------- |
| Naming | Singular vs Plural | Singular (BlogPost, not BlogPosts) |
| Stereotypes | Content, Widget, MenuItem | Content for standalone, Widget for embeddable |
| Draftable | true/false | true for editorial content |
| Versionable | true/false | true for audit requirements |

### Content Parts

Content Parts are reusable groups of fields that can be attached to multiple content types. They promote DRY principles.

```yaml
content_part:
  name: SeoMetaPart
  description: SEO metadata for search engines
  fields:
    - name: MetaTitle
      type: TextField
      settings:
        max_length: 60
        hint: "Title shown in search results"
    - name: MetaDescription
      type: TextField
      settings:
        max_length: 160
        editor: TextArea
    - name: MetaKeywords
      type: TextField
      settings:
        editor: TextArea
        hint: "Comma-separated keywords"
    - name: NoIndex
      type: BooleanField
      settings:
        default: false
```

**Common Reusable Parts:**

| Part | Purpose | Attach To |
| ---- | ------- | --------- |
| TitlePart | Title and display title | All content types |
| AutoroutePart | URL slug generation | Pages, articles |
| PublishLaterPart | Scheduled publishing | Editorial content |
| LocalizationPart | Multi-language support | Translatable content |
| SeoMetaPart | Search engine metadata | Public pages |
| CommonPart | Owner, created/modified dates | All content types |
| ContainablePart | Parent container reference | Hierarchical content |

### Content Fields

Content Fields are individual data elements attached to parts or directly to content types.

**Standard Field Types:**

| Field Type | Purpose | Example Use |
| ---------- | ------- | ----------- |
| TextField | Single/multi-line text | Title, description |
| HtmlField | Rich text with formatting | Body content |
| NumericField | Numbers (int, decimal) | Price, quantity |
| BooleanField | True/false toggle | Featured, published |
| DateTimeField | Date and/or time | Event date, deadline |
| MediaField | Images, documents, video | Hero image, attachments |
| ContentPickerField | Reference to other content | Author, related posts |
| TaxonomyField | Category/tag selection | Categories, tags |
| LinkField | URL with optional text | External links |
| UserPickerField | Reference to users | Author, assignee |

## Composition vs Inheritance

### Composition Pattern (Recommended)

Build content types by combining parts. This is the preferred approach for flexibility.

```yaml
# Blog Post = TitlePart + AutoroutePart + BodyPart + SeoMetaPart + Custom Fields
content_type:
  name: BlogPost
  parts:
    - TitlePart
    - AutoroutePart
    - PublishLaterPart
    - SeoMetaPart
  fields:
    - name: FeaturedImage
      type: MediaField
    - name: Author
      type: ContentPickerField
      settings:
        content_types: [Author]
    - name: Categories
      type: TaxonomyField
      settings:
        taxonomy: BlogCategories
```

**Benefits:**

- Parts are reusable across types
- Changes to parts affect all attached types
- Clear separation of concerns
- Easier to add/remove capabilities

### Inheritance Pattern

Use sparingly for true "is-a" relationships.

```yaml
# Base type
content_type:
  name: Article
  abstract: true  # Cannot create instances directly
  parts:
    - TitlePart
    - AutoroutePart
    - BodyPart

# Derived types
content_type:
  name: NewsArticle
  extends: Article
  fields:
    - name: BreakingNews
      type: BooleanField

content_type:
  name: OpinionPiece
  extends: Article
  fields:
    - name: OpinionAuthor
      type: ContentPickerField
```

**When to Use Inheritance:**

- Clear "is-a" relationship
- Shared behavior across subtypes
- Polymorphic queries needed
- Limited hierarchy depth (2-3 levels max)

## Field Design Best Practices

### Naming Conventions

```text
DO:
- PascalCase for type/part/field names: BlogPost, FeaturedImage
- Descriptive names that indicate purpose: PublishDate (not Date1)
- Consistent suffixes: *Date, *Image, *List

DON'T:
- Abbreviations: PubDt, FeatImg
- Generic names: Data, Value, Field1
- Inconsistent casing: blogPost, featured_image
```

### Field Validation

```yaml
field:
  name: Email
  type: TextField
  validation:
    required: true
    pattern: "^[^@]+@[^@]+\\.[^@]+$"
    max_length: 255
    unique: true  # Within content type
  settings:
    placeholder: "user@example.com"
    hint: "Enter a valid email address"
```

### Required vs Optional Fields

```text
Required fields:
- Essential for content to be meaningful
- Used in URLs or identification
- Needed for API consumers

Optional fields:
- Enhancements or metadata
- May not apply to all instances
- Progressive disclosure in editor
```

## Content Type Categories

### System Content Types

Built-in types that power CMS functionality:

| Type | Purpose |
| ---- | ------- |
| Menu | Navigation structure |
| MenuItem | Individual menu link |
| Taxonomy | Category/tag vocabulary |
| TaxonomyTerm | Individual term |
| MediaAsset | Images, documents |
| User | User profiles |

### Common Content Types

Frequently needed across CMS projects:

```yaml
# Page - generic content page
content_type:
  name: Page
  parts: [TitlePart, AutoroutePart, BodyPart, SeoMetaPart]
  fields:
    - name: FeaturedImage
      type: MediaField
      optional: true

# Article - blog post, news article
content_type:
  name: Article
  parts: [TitlePart, AutoroutePart, BodyPart, SeoMetaPart, PublishLaterPart]
  fields:
    - name: Author
      type: ContentPickerField
    - name: FeaturedImage
      type: MediaField
    - name: Categories
      type: TaxonomyField
    - name: Tags
      type: TaxonomyField
    - name: ReadTime
      type: NumericField
      computed: true

# Event - calendar event
content_type:
  name: Event
  parts: [TitlePart, AutoroutePart, BodyPart]
  fields:
    - name: StartDate
      type: DateTimeField
      required: true
    - name: EndDate
      type: DateTimeField
    - name: Location
      type: TextField
    - name: VirtualLink
      type: LinkField
    - name: RegistrationUrl
      type: LinkField
```

## API Considerations

### Content Type to API Shape

Content types should map cleanly to API responses:

```json
{
  "id": "abc123",
  "contentType": "BlogPost",
  "displayText": "My Blog Post Title",
  "createdUtc": "2025-01-15T10:30:00Z",
  "modifiedUtc": "2025-01-15T14:22:00Z",
  "publishedUtc": "2025-01-15T14:22:00Z",
  "owner": "user123",
  "parts": {
    "TitlePart": {
      "title": "My Blog Post Title"
    },
    "AutoroutePart": {
      "path": "/blog/my-blog-post-title"
    }
  },
  "fields": {
    "FeaturedImage": {
      "paths": ["/media/hero.jpg"],
      "alt": "Hero image"
    },
    "Author": {
      "contentItemIds": ["author456"]
    },
    "Categories": {
      "termIds": ["cat1", "cat2"]
    }
  }
}
```

### GraphQL Schema Generation

Content types typically map to GraphQL types:

```graphql
type BlogPost implements ContentItem {
  contentItemId: ID!
  contentType: String!
  displayText: String
  createdUtc: DateTime
  publishedUtc: DateTime

  # Parts
  titlePart: TitlePart
  autoroutePart: AutoroutePart

  # Fields
  featuredImage: MediaField
  author: ContentPickerField
  categories: TaxonomyField
}
```

## Migration Strategy

### From Traditional to Structured

```text
1. Audit existing content
   - Document current structure
   - Identify repeated patterns
   - Note relationships

2. Design target schema
   - Group fields into parts
   - Define content types
   - Plan taxonomies

3. Create mapping
   - Old field -> New field
   - Data transformations needed
   - Default values for new fields

4. Migrate incrementally
   - Start with simpler types
   - Validate after each batch
   - Keep old system running in parallel
```

## Content Type Checklist

Before finalizing a content type:

- [ ] Clear, descriptive name
- [ ] Appropriate parts attached
- [ ] All necessary fields defined
- [ ] Validation rules specified
- [ ] Required vs optional clearly marked
- [ ] API shape considered
- [ ] Localization requirements addressed
- [ ] Search indexing configured
- [ ] Preview/display template planned
- [ ] Editor experience optimized

## Related Skills

- `dynamic-schema-design` - EF Core JSON columns for custom fields
- `content-relationships` - References between content items
- `content-versioning` - Draft/publish and version history
- `taxonomy-architecture` - Categories and tags
- `headless-api-design` - Content delivery APIs
