---
name: page-structure-design
description: Use when designing page hierarchies, page templates, layout zones, or sitemap structures. Covers page sets, template inheritance, component zones, and page tree APIs for headless CMS architectures.
allowed-tools: Read, Glob, Grep, Task, Skill
---

# Page Structure Design

Guidance for designing page hierarchies, templates, and modular page composition systems for headless CMS.

## When to Use This Skill

- Designing page tree structures
- Creating page templates with zones
- Implementing page builder functionality
- Planning sitemap generation
- Building modular page composition

## Page Hierarchy Patterns

### Basic Page Tree

```csharp
public class Page
{
    public Guid Id { get; set; }
    public string Title { get; set; } = string.Empty;
    public string Slug { get; set; } = string.Empty;

    // Hierarchy
    public Guid? ParentId { get; set; }
    public Page? Parent { get; set; }
    public List<Page> Children { get; set; } = new();

    // Computed path
    public string Path { get; set; } = string.Empty; // /about/team/leadership
    public int Depth { get; set; }
    public int Order { get; set; }

    // Template and content
    public string Template { get; set; } = string.Empty;
    public PageContent Content { get; set; } = new();
}
```

### Page Sets (Collections)

```csharp
// Page set for grouping related pages
public class PageSet
{
    public Guid Id { get; set; }
    public string Name { get; set; } = string.Empty;
    public string Slug { get; set; } = string.Empty;
    public PageSetType Type { get; set; }

    // Configuration
    public string ItemTemplate { get; set; } = string.Empty;
    public string ListTemplate { get; set; } = string.Empty;
    public int ItemsPerPage { get; set; } = 10;

    // URL pattern
    public string UrlPattern { get; set; } = string.Empty; // /blog/{slug}
}

public enum PageSetType
{
    Blog,       // Chronological posts
    Portfolio,  // Project showcase
    Team,       // Team members
    Products,   // Product catalog
    FAQ,        // Q&A collection
    Custom      // User-defined
}
```

## Template System

### Template Definition

```csharp
public class PageTemplate
{
    public string Name { get; set; } = string.Empty;
    public string DisplayName { get; set; } = string.Empty;
    public string Description { get; set; } = string.Empty;

    // Template hierarchy
    public string? ParentTemplate { get; set; }

    // Available zones for content
    public List<TemplateZone> Zones { get; set; } = new();

    // Required fields
    public List<TemplateField> Fields { get; set; } = new();

    // Applicable page types
    public List<string> ApplicablePageTypes { get; set; } = new();
}

public class TemplateZone
{
    public string Name { get; set; } = string.Empty;
    public string DisplayName { get; set; } = string.Empty;
    public ZoneType Type { get; set; }
    public List<string> AllowedWidgets { get; set; } = new();
    public int? MaxWidgets { get; set; }
}

public enum ZoneType
{
    Single,     // One widget only
    Multiple,   // Multiple widgets stacked
    Grid        // Grid layout
}
```

### Template Inheritance

```text
BaseTemplate
├── Zones: Header, Footer, Sidebar
└── Fields: MetaTitle, MetaDescription

    ├── HomeTemplate (extends Base)
    │   └── Zones: Hero, Features, CTA
    │
    ├── ContentTemplate (extends Base)
    │   └── Zones: MainContent, RelatedContent
    │
    └── LandingTemplate (extends Base)
        └── Zones: Hero, Sections (multiple)
```

## Page Builder Components

### Widget System

```csharp
public abstract class Widget
{
    public Guid Id { get; set; }
    public string Type { get; set; } = string.Empty;
    public int Order { get; set; }
    public Dictionary<string, object?> Settings { get; set; } = new();
}

public class TextWidget : Widget
{
    public string Content { get; set; } = string.Empty;
}

public class ImageWidget : Widget
{
    public Guid MediaItemId { get; set; }
    public string? Alt { get; set; }
    public string? Caption { get; set; }
}

public class CallToActionWidget : Widget
{
    public string Heading { get; set; } = string.Empty;
    public string? Subheading { get; set; }
    public string ButtonText { get; set; } = string.Empty;
    public string ButtonUrl { get; set; } = string.Empty;
    public string? BackgroundImageId { get; set; }
}

public class CardGridWidget : Widget
{
    public List<Card> Cards { get; set; } = new();
    public int Columns { get; set; } = 3;
}
```

### Page Content Structure

```csharp
public class PageContent
{
    // Zone-based content storage
    public Dictionary<string, List<Widget>> Zones { get; set; } = new();

    // Page-level fields
    public string? HeroTitle { get; set; }
    public string? HeroSubtitle { get; set; }
    public Guid? HeroImageId { get; set; }

    // SEO
    public string? MetaTitle { get; set; }
    public string? MetaDescription { get; set; }
    public bool NoIndex { get; set; }
}
```

## Sitemap Generation

### Sitemap Data Model

```csharp
public class SitemapEntry
{
    public string Url { get; set; } = string.Empty;
    public DateTime LastModified { get; set; }
    public ChangeFrequency ChangeFrequency { get; set; }
    public decimal Priority { get; set; }
    public List<SitemapAlternate>? Alternates { get; set; }
}

public class SitemapAlternate
{
    public string Hreflang { get; set; } = string.Empty;
    public string Url { get; set; } = string.Empty;
}

public enum ChangeFrequency
{
    Always,
    Hourly,
    Daily,
    Weekly,
    Monthly,
    Yearly,
    Never
}
```

### Sitemap Generation Service

```csharp
public class SitemapService
{
    public async Task<List<SitemapEntry>> GenerateSitemapAsync()
    {
        var entries = new List<SitemapEntry>();

        // Add pages
        var pages = await _pageRepository.GetPublishedPagesAsync();
        foreach (var page in pages)
        {
            entries.Add(new SitemapEntry
            {
                Url = $"{_baseUrl}{page.Path}",
                LastModified = page.ModifiedUtc,
                ChangeFrequency = GetChangeFrequency(page),
                Priority = CalculatePriority(page)
            });
        }

        // Add page set items (blog posts, products, etc.)
        var pageSets = await _pageSetRepository.GetAllAsync();
        foreach (var pageSet in pageSets)
        {
            var items = await _pageSetRepository.GetItemsAsync(pageSet.Id);
            foreach (var item in items)
            {
                var url = GenerateUrl(pageSet.UrlPattern, item);
                entries.Add(new SitemapEntry
                {
                    Url = url,
                    LastModified = item.ModifiedUtc,
                    ChangeFrequency = ChangeFrequency.Weekly,
                    Priority = 0.6m
                });
            }
        }

        return entries;
    }

    private decimal CalculatePriority(Page page)
    {
        // Home page highest priority
        if (page.Depth == 0) return 1.0m;

        // Decrease by depth
        return Math.Max(0.5m, 1.0m - (page.Depth * 0.1m));
    }
}
```

## Page Tree API

### REST Endpoints

```text
GET    /api/pages                    # Root pages
GET    /api/pages/{id}               # Single page
GET    /api/pages/{id}/children      # Child pages
GET    /api/pages/path/{*path}       # Page by URL path
GET    /api/pages/tree               # Full page tree
GET    /api/sitemap.xml              # XML sitemap
GET    /api/sitemap.json             # JSON sitemap
```

### Page Tree Response

```json
{
  "data": {
    "id": "page-123",
    "title": "About Us",
    "slug": "about",
    "path": "/about",
    "template": "ContentTemplate",
    "depth": 1,
    "order": 2,
    "children": [
      {
        "id": "page-456",
        "title": "Our Team",
        "slug": "team",
        "path": "/about/team",
        "template": "TeamTemplate",
        "children": []
      },
      {
        "id": "page-789",
        "title": "Careers",
        "slug": "careers",
        "path": "/about/careers",
        "template": "ContentTemplate",
        "children": []
      }
    ]
  },
  "breadcrumbs": [
    { "title": "Home", "path": "/" },
    { "title": "About Us", "path": "/about" }
  ]
}
```

## Best Practices

### Page Structure

| Pattern | When to Use |
| ------- | ----------- |
| Flat structure | Simple sites, few pages |
| 2-level hierarchy | Most corporate sites |
| Deep hierarchy | Documentation, large catalogs |
| Page sets | Blog, portfolio, team pages |

### Template Design

```text
DO:
- Keep zones semantic (Header, MainContent, Sidebar)
- Allow flexible widget placement
- Inherit common zones from base template
- Provide sensible defaults

DON'T:
- Create overly specific templates
- Hard-code layout in templates
- Mix content and presentation concerns
- Create deep template inheritance chains
```

## Related Skills

- `navigation-architecture` - Menu and breadcrumb design
- `url-routing-patterns` - URL structure and routing
- `content-type-modeling` - Page as content type
