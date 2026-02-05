---
name: headless-api-design
description: Use when designing content delivery APIs for headless CMS architectures. Covers REST and GraphQL API patterns, content preview endpoints, localization strategies, pagination, filtering, caching headers, and API versioning for multi-channel content delivery.
allowed-tools: Read, Glob, Grep, Task, Skill
---

# Headless API Design

Guidance for designing content delivery APIs for headless CMS architectures, enabling multi-channel content distribution.

## When to Use This Skill

- Designing REST or GraphQL APIs for content delivery
- Implementing preview endpoints for draft content
- Adding localization/i18n to content APIs
- Planning pagination and filtering strategies
- Configuring caching headers for content
- Versioning content APIs

## API Architecture Overview

### Headless CMS API Layers

```text
┌─────────────────────────────────────────────────────────────┐
│                    Content Consumers                         │
│  (Blazor, React, Next.js, Mobile Apps, IoT, Digital Signs)  │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    Content Delivery API                      │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │  REST API   │  │ GraphQL API │  │ Preview/Draft API   │  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    Content Services                          │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │   Content   │  │    Media    │  │   Localization      │  │
│  │   Query     │  │   Resolver  │  │   Service           │  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    Content Repository                        │
│              (EF Core + JSON Columns + Cache)               │
└─────────────────────────────────────────────────────────────┘
```

## REST API Design

### Resource Endpoints

```text
GET    /api/content                    # List all content items
GET    /api/content/{id}               # Get content by ID
GET    /api/content/alias/{path}       # Get content by URL path/alias
GET    /api/content/types/{type}       # List content by type

# Type-specific endpoints
GET    /api/articles                   # List articles
GET    /api/articles/{id}              # Get article
GET    /api/pages                      # List pages
GET    /api/pages/{id}                 # Get page

# Nested resources
GET    /api/articles/{id}/comments     # Get article comments
GET    /api/menus/{id}/items           # Get menu items
```

### Query Parameters

```text
# Pagination
?page=1&pageSize=20                    # Offset pagination
?cursor=eyJpZCI6MTIz&limit=20         # Cursor pagination

# Filtering
?filter[status]=published
?filter[contentType]=Article
?filter[author.id]=abc123
?filter[createdUtc][gte]=2025-01-01

# Sorting
?sort=-publishedUtc                    # Descending
?sort=title                            # Ascending
?sort=category.name,-createdUtc        # Multiple fields

# Field selection (sparse fieldsets)
?fields=id,title,slug,publishedUtc
?fields[article]=title,body
?fields[author]=name,avatar

# Include related resources
?include=author,categories
?include=author.profile
```

### Response Structure

```json
{
  "data": {
    "id": "abc123",
    "type": "Article",
    "attributes": {
      "title": "Getting Started with Headless CMS",
      "slug": "getting-started-headless-cms",
      "body": "<p>Content here...</p>",
      "publishedUtc": "2025-01-15T10:30:00Z",
      "status": "Published"
    },
    "parts": {
      "titlePart": {
        "title": "Getting Started with Headless CMS"
      },
      "seoPart": {
        "metaTitle": "Headless CMS Guide",
        "metaDescription": "Learn how to..."
      }
    },
    "relationships": {
      "author": {
        "data": { "id": "author456", "type": "Author" }
      },
      "categories": {
        "data": [
          { "id": "cat1", "type": "Category" }
        ]
      }
    }
  },
  "included": [
    {
      "id": "author456",
      "type": "Author",
      "attributes": {
        "name": "Jane Doe",
        "bio": "Technical writer..."
      }
    }
  ],
  "meta": {
    "version": "1.0",
    "generatedAt": "2025-01-15T14:22:00Z"
  }
}
```

### Collection Response with Pagination

```json
{
  "data": [...],
  "meta": {
    "totalCount": 156,
    "pageSize": 20,
    "currentPage": 1,
    "totalPages": 8
  },
  "links": {
    "self": "/api/articles?page=1&pageSize=20",
    "first": "/api/articles?page=1&pageSize=20",
    "prev": null,
    "next": "/api/articles?page=2&pageSize=20",
    "last": "/api/articles?page=8&pageSize=20"
  }
}
```

## GraphQL API Design

### Schema Definition

```graphql
type Query {
  # Single item queries
  content(id: ID!): ContentItem
  contentByPath(path: String!): ContentItem

  # Type-specific queries
  article(id: ID!): Article
  articles(
    filter: ArticleFilter
    sort: ArticleSort
    first: Int
    after: String
  ): ArticleConnection!

  page(id: ID!): Page
  pages(parentId: ID): [Page!]!

  menu(id: ID, name: String): Menu
}

interface ContentItem {
  id: ID!
  contentType: String!
  displayText: String
  createdUtc: DateTime!
  modifiedUtc: DateTime!
  publishedUtc: DateTime
  status: ContentStatus!
}

type Article implements ContentItem {
  id: ID!
  contentType: String!
  displayText: String
  createdUtc: DateTime!
  modifiedUtc: DateTime!
  publishedUtc: DateTime
  status: ContentStatus!

  # Parts
  titlePart: TitlePart
  autoroutePart: AutoroutePart
  seoPart: SeoMetaPart

  # Fields
  body: String!
  featuredImage: MediaField
  author: Author
  categories: [Category!]!
  tags: [String!]!
  readTimeMinutes: Int
}

type ArticleConnection {
  edges: [ArticleEdge!]!
  pageInfo: PageInfo!
  totalCount: Int!
}

type ArticleEdge {
  node: Article!
  cursor: String!
}

type PageInfo {
  hasNextPage: Boolean!
  hasPreviousPage: Boolean!
  startCursor: String
  endCursor: String
}

input ArticleFilter {
  status: ContentStatus
  categoryId: ID
  authorId: ID
  tags: [String!]
  publishedAfter: DateTime
  publishedBefore: DateTime
  search: String
}

input ArticleSort {
  field: ArticleSortField!
  direction: SortDirection!
}

enum ArticleSortField {
  TITLE
  PUBLISHED_UTC
  CREATED_UTC
  READ_TIME
}
```

### Content Parts as Types

```graphql
type TitlePart {
  title: String!
  displayTitle: String
}

type AutoroutePart {
  path: String!
  isCustom: Boolean!
}

type SeoMetaPart {
  metaTitle: String
  metaDescription: String
  metaKeywords: String
  noIndex: Boolean!
  noFollow: Boolean!
}

type MediaField {
  paths: [String!]!
  urls: [String!]!
  alt: String
  caption: String
  mediaItems: [MediaItem!]!
}

type MediaItem {
  id: ID!
  url: String!
  mimeType: String!
  width: Int
  height: Int
  alt: String
}
```

## Preview API

### Draft Content Endpoint

```text
# Requires authentication/preview token
GET /api/preview/content/{id}
GET /api/preview/content/{id}?version={versionId}

# Preview token in header
Authorization: Bearer <preview-token>
X-Preview-Mode: true
```

### Preview Implementation

```csharp
[ApiController]
[Route("api/preview")]
public class PreviewController : ControllerBase
{
    private readonly IContentService _contentService;
    private readonly IPreviewTokenService _tokenService;

    [HttpGet("content/{id}")]
    public async Task<ActionResult<ContentItemDto>> GetPreview(
        string id,
        [FromHeader(Name = "X-Preview-Token")] string? previewToken,
        [FromQuery] string? version)
    {
        // Validate preview token
        if (!await _tokenService.ValidateTokenAsync(previewToken))
        {
            return Unauthorized();
        }

        // Get draft or specific version
        var content = version != null
            ? await _contentService.GetVersionAsync(id, version)
            : await _contentService.GetDraftAsync(id);

        if (content == null)
        {
            return NotFound();
        }

        return Ok(content);
    }
}
```

### Preview Token Generation

```csharp
public class PreviewTokenService : IPreviewTokenService
{
    public string GenerateToken(string contentId, TimeSpan validity)
    {
        var payload = new
        {
            ContentId = contentId,
            ExpiresAt = DateTime.UtcNow.Add(validity),
            Nonce = Guid.NewGuid().ToString("N")
        };

        // Sign with HMAC or JWT
        return SignPayload(payload);
    }

    public async Task<bool> ValidateTokenAsync(string? token)
    {
        if (string.IsNullOrEmpty(token))
            return false;

        var payload = VerifyAndDecodeToken(token);
        if (payload == null)
            return false;

        return payload.ExpiresAt > DateTime.UtcNow;
    }
}
```

## Localization Strategy

### URL-Based Localization

```text
# Path prefix (recommended)
GET /api/en/articles
GET /api/fr/articles
GET /api/de-DE/articles

# Query parameter
GET /api/articles?locale=en
GET /api/articles?locale=fr

# Accept-Language header
Accept-Language: en-US, en;q=0.9, fr;q=0.8
```

### Localized Response Structure

```json
{
  "data": {
    "id": "abc123",
    "type": "Article",
    "locale": "en-US",
    "attributes": {
      "title": "Getting Started",
      "body": "English content..."
    },
    "localizations": {
      "available": ["en-US", "fr-FR", "de-DE"],
      "links": {
        "fr-FR": "/api/fr/articles/abc123",
        "de-DE": "/api/de/articles/abc123"
      }
    }
  }
}
```

### Fallback Chain

```csharp
public class LocalizationService
{
    public async Task<ContentItem?> GetLocalizedContentAsync(
        string id,
        string requestedLocale)
    {
        // Define fallback chain
        var fallbackChain = GetFallbackChain(requestedLocale);
        // e.g., ["en-GB", "en", "default"]

        foreach (var locale in fallbackChain)
        {
            var content = await _repository
                .GetByIdAndLocaleAsync(id, locale);

            if (content != null)
            {
                return content;
            }
        }

        return null;
    }

    private List<string> GetFallbackChain(string locale)
    {
        var chain = new List<string> { locale };

        // Add language without region
        if (locale.Contains('-'))
        {
            chain.Add(locale.Split('-')[0]);
        }

        // Add default
        chain.Add("default");

        return chain;
    }
}
```

## Caching Strategy

### Cache Headers

```csharp
[HttpGet("{id}")]
public async Task<ActionResult<ContentItemDto>> Get(string id)
{
    var content = await _contentService.GetAsync(id);
    if (content == null)
    {
        return NotFound();
    }

    // Set cache headers
    Response.Headers["Cache-Control"] = "public, max-age=300"; // 5 minutes
    Response.Headers["ETag"] = $"\"{content.Version}\"";
    Response.Headers["Last-Modified"] = content.ModifiedUtc
        .ToString("R"); // RFC 1123 format

    return Ok(content);
}
```

### Conditional GET

```csharp
[HttpGet("{id}")]
public async Task<ActionResult<ContentItemDto>> Get(
    string id,
    [FromHeader(Name = "If-None-Match")] string? ifNoneMatch,
    [FromHeader(Name = "If-Modified-Since")] string? ifModifiedSince)
{
    var content = await _contentService.GetAsync(id);
    if (content == null)
    {
        return NotFound();
    }

    var etag = $"\"{content.Version}\"";

    // Check ETag
    if (ifNoneMatch == etag)
    {
        return StatusCode(304); // Not Modified
    }

    // Check Last-Modified
    if (DateTime.TryParse(ifModifiedSince, out var modifiedSince))
    {
        if (content.ModifiedUtc <= modifiedSince)
        {
            return StatusCode(304); // Not Modified
        }
    }

    Response.Headers["ETag"] = etag;
    return Ok(content);
}
```

### Cache Invalidation

```csharp
public class ContentPublishHandler : INotificationHandler<ContentPublishedEvent>
{
    private readonly ICacheInvalidationService _cache;

    public async Task Handle(ContentPublishedEvent notification,
        CancellationToken cancellationToken)
    {
        // Invalidate specific content
        await _cache.InvalidateAsync($"content:{notification.ContentId}");

        // Invalidate collection caches
        await _cache.InvalidateByTagAsync($"type:{notification.ContentType}");

        // Invalidate CDN cache
        await _cache.PurgeCdnAsync($"/api/content/{notification.ContentId}");
    }
}
```

## API Versioning

### URL Path Versioning

```text
GET /api/v1/content/{id}
GET /api/v2/content/{id}
```

### Header Versioning

```text
GET /api/content/{id}
Api-Version: 2.0
```

### Implementation

```csharp
// Program.cs
builder.Services.AddApiVersioning(options =>
{
    options.DefaultApiVersion = new ApiVersion(1, 0);
    options.AssumeDefaultVersionWhenUnspecified = true;
    options.ReportApiVersions = true;
    options.ApiVersionReader = ApiVersionReader.Combine(
        new UrlSegmentApiVersionReader(),
        new HeaderApiVersionReader("Api-Version")
    );
});

// Controller
[ApiController]
[ApiVersion("1.0")]
[ApiVersion("2.0")]
[Route("api/v{version:apiVersion}/content")]
public class ContentController : ControllerBase
{
    [HttpGet("{id}")]
    [MapToApiVersion("1.0")]
    public async Task<ActionResult<ContentItemDtoV1>> GetV1(string id)
    {
        // V1 response shape
    }

    [HttpGet("{id}")]
    [MapToApiVersion("2.0")]
    public async Task<ActionResult<ContentItemDtoV2>> GetV2(string id)
    {
        // V2 response shape with breaking changes
    }
}
```

## Security Considerations

### API Key Authentication

```csharp
public class ApiKeyAuthenticationHandler : AuthenticationHandler<ApiKeyAuthenticationOptions>
{
    protected override async Task<AuthenticateResult> HandleAuthenticateAsync()
    {
        if (!Request.Headers.TryGetValue("X-Api-Key", out var apiKey))
        {
            return AuthenticateResult.NoResult();
        }

        var client = await _clientService.ValidateApiKeyAsync(apiKey!);
        if (client == null)
        {
            return AuthenticateResult.Fail("Invalid API key");
        }

        var claims = new[]
        {
            new Claim(ClaimTypes.NameIdentifier, client.Id),
            new Claim("client_name", client.Name),
            new Claim("scope", string.Join(" ", client.Scopes))
        };

        var identity = new ClaimsIdentity(claims, Scheme.Name);
        var principal = new ClaimsPrincipal(identity);
        var ticket = new AuthenticationTicket(principal, Scheme.Name);

        return AuthenticateResult.Success(ticket);
    }
}
```

### Rate Limiting

```csharp
builder.Services.AddRateLimiter(options =>
{
    options.AddPolicy("content-api", context =>
        RateLimitPartition.GetFixedWindowLimiter(
            partitionKey: context.Request.Headers["X-Api-Key"].ToString(),
            factory: _ => new FixedWindowRateLimiterOptions
            {
                PermitLimit = 1000,
                Window = TimeSpan.FromHours(1),
                QueueLimit = 0
            }));
});
```

## Related Skills

- `content-type-modeling` - Content structure for API responses
- `dynamic-schema-design` - JSON column storage for flexible APIs
- `content-versioning` - Version history API endpoints
- `cdn-media-delivery` - CDN integration for media APIs
