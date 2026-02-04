---
name: cdn-media-delivery
description: Use when configuring CDN for media delivery, implementing cache invalidation, or designing signed URL patterns. Covers CDN configuration, edge caching, origin shielding, and secure media access for headless CMS.
allowed-tools: Read, Glob, Grep, Task, Skill
---

# CDN Media Delivery

Guidance for configuring CDN delivery, cache management, and secure media access for headless CMS architectures.

## When to Use This Skill

- Configuring CDN for media delivery
- Implementing cache invalidation strategies
- Setting up signed/secure URLs
- Optimizing edge caching
- Configuring origin shielding

## CDN Architecture

### Basic CDN Setup

```text
┌─────────────────────────────────────────────────────────────┐
│                         Users                                │
│              (Global, geographically distributed)            │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      CDN Edge Network                        │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐        │
│  │ Edge    │  │ Edge    │  │ Edge    │  │ Edge    │        │
│  │ US-West │  │ US-East │  │ Europe  │  │ Asia    │        │
│  └─────────┘  └─────────┘  └─────────┘  └─────────┘        │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      Origin Shield                           │
│              (Optional intermediate cache layer)             │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      Origin Server                           │
│  ┌───────────────┐  ┌────────────────┐  ┌───────────────┐  │
│  │ Media API     │  │ Blob Storage   │  │ Image         │  │
│  │ (transform)   │  │ (Azure/S3)     │  │ Processor     │  │
│  └───────────────┘  └────────────────┘  └───────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## CDN Configuration

### Azure CDN (Front Door)

```csharp
// appsettings.json
{
  "Cdn": {
    "Provider": "AzureFrontDoor",
    "Endpoint": "https://media.example.com",
    "OriginHost": "storage.blob.core.windows.net",
    "CacheRules": {
      "Images": {
        "CacheDuration": "365.00:00:00",
        "QueryStringCaching": "IgnoreQueryString"
      },
      "Transforms": {
        "CacheDuration": "30.00:00:00",
        "QueryStringCaching": "UseQueryString"
      }
    }
  }
}
```

### CloudFront Configuration

```csharp
public class CloudFrontConfiguration
{
    public string DistributionId { get; set; } = string.Empty;
    public string DomainName { get; set; } = string.Empty;
    public string OriginId { get; set; } = string.Empty;

    public CacheBehavior DefaultCacheBehavior { get; set; } = new()
    {
        ViewerProtocolPolicy = "redirect-to-https",
        CachePolicyId = "658327ea-f89d-4fab-a63d-7e88639e58f6", // CachingOptimized
        Compress = true,
        AllowedMethods = new[] { "GET", "HEAD", "OPTIONS" },
        CachedMethods = new[] { "GET", "HEAD" }
    };

    public CacheBehavior[] CacheBehaviors { get; set; } =
    {
        new()
        {
            PathPattern = "/media/transform/*",
            CachePolicyId = "custom-transform-policy",
            QueryStringCaching = QueryStringCaching.All
        }
    };
}
```

### Cloudflare Configuration

```csharp
public class CloudflareConfiguration
{
    public string ZoneId { get; set; } = string.Empty;
    public string ApiToken { get; set; } = string.Empty;

    public PageRule[] PageRules { get; set; } =
    {
        new()
        {
            Targets = new[] { "*example.com/media/*" },
            Actions = new PageRuleAction
            {
                CacheLevel = "cache_everything",
                EdgeCacheTtl = 2592000, // 30 days
                BrowserCacheTtl = 86400  // 1 day
            }
        }
    };
}
```

## Cache Headers

### Setting Cache Headers

```csharp
public class MediaCacheMiddleware
{
    public async Task InvokeAsync(HttpContext context, RequestDelegate next)
    {
        await next(context);

        if (context.Request.Path.StartsWithSegments("/media"))
        {
            var cacheControl = GetCacheControl(context.Request.Path);
            context.Response.Headers["Cache-Control"] = cacheControl;
            context.Response.Headers["Vary"] = "Accept, Accept-Encoding";
        }
    }

    private string GetCacheControl(PathString path)
    {
        // Original media: cache for 1 year (immutable content)
        if (path.Value?.Contains("/original/") == true)
        {
            return "public, max-age=31536000, immutable";
        }

        // Transformed images: cache for 30 days
        if (path.Value?.Contains("/transform/") == true)
        {
            return "public, max-age=2592000, stale-while-revalidate=86400";
        }

        // Default: 1 day
        return "public, max-age=86400";
    }
}
```

### Cache-Control Directives

| Directive | Purpose | Example |
| --------- | ------- | ------- |
| `public` | Allow CDN caching | Images, static assets |
| `private` | Browser only | User-specific content |
| `max-age` | Cache duration (seconds) | `max-age=86400` (1 day) |
| `immutable` | Never revalidate | Versioned assets |
| `stale-while-revalidate` | Serve stale while fetching | Background refresh |
| `no-cache` | Always revalidate | Dynamic content |
| `no-store` | Never cache | Sensitive data |

## Cache Invalidation

### Invalidation Service

```csharp
public interface ICdnInvalidationService
{
    Task InvalidatePathAsync(string path);
    Task InvalidatePathsAsync(IEnumerable<string> paths);
    Task InvalidatePrefixAsync(string prefix);
    Task InvalidateAllAsync();
}

// Azure CDN implementation
public class AzureCdnInvalidationService : ICdnInvalidationService
{
    private readonly CdnManagementClient _cdnClient;

    public async Task InvalidatePathAsync(string path)
    {
        await _cdnClient.Endpoints.PurgeContentAsync(
            _resourceGroup,
            _profileName,
            _endpointName,
            new PurgeParameters(new[] { path }));
    }

    public async Task InvalidatePrefixAsync(string prefix)
    {
        await _cdnClient.Endpoints.PurgeContentAsync(
            _resourceGroup,
            _profileName,
            _endpointName,
            new PurgeParameters(new[] { $"{prefix}/*" }));
    }
}

// CloudFront implementation
public class CloudFrontInvalidationService : ICdnInvalidationService
{
    private readonly AmazonCloudFrontClient _client;

    public async Task InvalidatePathAsync(string path)
    {
        var request = new CreateInvalidationRequest
        {
            DistributionId = _distributionId,
            InvalidationBatch = new InvalidationBatch
            {
                CallerReference = Guid.NewGuid().ToString(),
                Paths = new Paths
                {
                    Items = new List<string> { path },
                    Quantity = 1
                }
            }
        };

        await _client.CreateInvalidationAsync(request);
    }
}
```

### Event-Based Invalidation

```csharp
public class MediaUpdatedHandler : INotificationHandler<MediaUpdatedEvent>
{
    private readonly ICdnInvalidationService _cdn;

    public async Task Handle(MediaUpdatedEvent notification, CancellationToken ct)
    {
        // Invalidate original
        await _cdn.InvalidatePathAsync($"/media/{notification.MediaId}");

        // Invalidate all transformations
        await _cdn.InvalidatePrefixAsync($"/media/transform/{notification.MediaId}");
    }
}
```

## Signed URLs

### Signed URL Generation

```csharp
public class SignedUrlService
{
    public string GenerateSignedUrl(
        string path,
        TimeSpan validity,
        SignedUrlOptions? options = null)
    {
        options ??= new SignedUrlOptions();

        var expiry = DateTime.UtcNow.Add(validity);
        var expiryTimestamp = new DateTimeOffset(expiry).ToUnixTimeSeconds();

        // Build URL with parameters
        var urlBuilder = new UriBuilder($"{_cdnBaseUrl}{path}");
        var query = HttpUtility.ParseQueryString(urlBuilder.Query);

        query["expires"] = expiryTimestamp.ToString();

        if (options.AllowedIp != null)
        {
            query["ip"] = options.AllowedIp;
        }

        // Generate signature
        var signatureData = $"{path}|{expiryTimestamp}|{options.AllowedIp}";
        var signature = ComputeSignature(signatureData);
        query["signature"] = signature;

        urlBuilder.Query = query.ToString();
        return urlBuilder.ToString();
    }

    private string ComputeSignature(string data)
    {
        using var hmac = new HMACSHA256(Encoding.UTF8.GetBytes(_signingKey));
        var hash = hmac.ComputeHash(Encoding.UTF8.GetBytes(data));
        return Convert.ToBase64String(hash)
            .Replace("+", "-")
            .Replace("/", "_")
            .TrimEnd('=');
    }
}

public class SignedUrlOptions
{
    public string? AllowedIp { get; set; }
    public string? AllowedCountry { get; set; }
    public int? MaxDownloads { get; set; }
}
```

### Signed URL Validation

```csharp
public class SignedUrlValidationMiddleware
{
    public async Task InvokeAsync(HttpContext context, RequestDelegate next)
    {
        if (RequiresSignedUrl(context.Request.Path))
        {
            var query = context.Request.Query;

            // Check expiry
            if (!long.TryParse(query["expires"], out var expiry) ||
                DateTimeOffset.UtcNow.ToUnixTimeSeconds() > expiry)
            {
                context.Response.StatusCode = 403;
                await context.Response.WriteAsync("URL expired");
                return;
            }

            // Validate signature
            var expectedSignature = ComputeSignature(
                context.Request.Path,
                expiry,
                query["ip"]);

            if (query["signature"] != expectedSignature)
            {
                context.Response.StatusCode = 403;
                await context.Response.WriteAsync("Invalid signature");
                return;
            }

            // Check IP restriction
            if (!string.IsNullOrEmpty(query["ip"]))
            {
                var clientIp = context.Connection.RemoteIpAddress?.ToString();
                if (clientIp != query["ip"])
                {
                    context.Response.StatusCode = 403;
                    await context.Response.WriteAsync("IP not allowed");
                    return;
                }
            }
        }

        await next(context);
    }
}
```

## Origin Shielding

### Shield Configuration

```csharp
public class OriginShieldConfiguration
{
    public bool Enabled { get; set; } = true;
    public string ShieldRegion { get; set; } = "us-east-1";
    public int ShieldCacheTtl { get; set; } = 3600; // 1 hour
    public int MaxConnectionsToOrigin { get; set; } = 100;
}
```

### Benefits

| Feature | Without Shield | With Shield |
| ------- | -------------- | ----------- |
| Origin requests | From each edge | From one region |
| Cache efficiency | Per-edge | Shared shield cache |
| Origin load | High | Reduced 90%+ |
| Latency | Variable | Predictable |

## CDN URL Generation

### URL Service

```csharp
public class CdnUrlService
{
    public string GetMediaUrl(MediaItem media, MediaUrlOptions? options = null)
    {
        options ??= new MediaUrlOptions();

        var path = $"/media/{media.StoragePath}";

        // Add transformation query params
        if (options.Width.HasValue || options.Height.HasValue)
        {
            var query = new List<string>();

            if (options.Width.HasValue) query.Add($"w={options.Width}");
            if (options.Height.HasValue) query.Add($"h={options.Height}");
            if (options.Format.HasValue) query.Add($"format={options.Format}");
            if (options.Quality.HasValue) query.Add($"q={options.Quality}");

            path += "?" + string.Join("&", query);
        }

        // Generate signed URL if private
        if (media.IsPrivate || options.RequireSignature)
        {
            return _signedUrlService.GenerateSignedUrl(
                path,
                options.UrlValidity ?? TimeSpan.FromHours(1));
        }

        return $"{_cdnBaseUrl}{path}";
    }
}

public class MediaUrlOptions
{
    public int? Width { get; set; }
    public int? Height { get; set; }
    public ImageFormat? Format { get; set; }
    public int? Quality { get; set; }
    public bool RequireSignature { get; set; }
    public TimeSpan? UrlValidity { get; set; }
}
```

## Performance Monitoring

### CDN Metrics

```csharp
public class CdnMetrics
{
    public long TotalRequests { get; set; }
    public long CacheHits { get; set; }
    public long CacheMisses { get; set; }
    public double CacheHitRatio => (double)CacheHits / TotalRequests;
    public long BandwidthBytes { get; set; }
    public double AverageLatencyMs { get; set; }
    public Dictionary<string, long> RequestsByRegion { get; set; } = new();
    public Dictionary<int, long> StatusCodeCounts { get; set; } = new();
}
```

## Related Skills

- `media-asset-management` - Media storage and organization
- `image-optimization` - Image processing before CDN
- `headless-api-design` - Media API endpoints
