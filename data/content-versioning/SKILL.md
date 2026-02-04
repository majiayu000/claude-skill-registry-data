---
name: content-versioning
description: Use when implementing draft/publish workflows, version history, content rollback, or audit trails. Covers versioning strategies, snapshot storage, diff generation, and version comparison APIs for headless CMS.
allowed-tools: Read, Glob, Grep, Task, Skill
---

# Content Versioning

Guidance for implementing version control, draft/publish workflows, and audit trails for CMS content.

## When to Use This Skill

- Implementing draft/publish workflows
- Adding version history to content types
- Building content rollback features
- Creating audit trails for compliance
- Comparing content versions

## Versioning Strategies

### Strategy 1: Separate Draft/Published Records

```csharp
public class ContentItem
{
    public Guid Id { get; set; }
    public string ContentType { get; set; } = string.Empty;
    public ContentStatus Status { get; set; }

    // Version tracking
    public int Version { get; set; }
    public Guid? PublishedVersionId { get; set; }
    public Guid? DraftVersionId { get; set; }

    // Timestamps
    public DateTime CreatedUtc { get; set; }
    public DateTime ModifiedUtc { get; set; }
    public DateTime? PublishedUtc { get; set; }
}

public class ContentVersion
{
    public Guid Id { get; set; }
    public Guid ContentItemId { get; set; }
    public int VersionNumber { get; set; }

    // Snapshot of content at this version
    public string DataJson { get; set; } = string.Empty;

    // Metadata
    public string CreatedBy { get; set; } = string.Empty;
    public DateTime CreatedUtc { get; set; }
    public string? ChangeNote { get; set; }
    public bool IsPublished { get; set; }
}

public enum ContentStatus
{
    Draft,
    Published,
    Unpublished,
    Archived
}
```

### Strategy 2: History Table Pattern

```csharp
// Current content (always latest)
public class Article
{
    public Guid Id { get; set; }
    public string Title { get; set; } = string.Empty;
    public string Body { get; set; } = string.Empty;
    public int CurrentVersion { get; set; }
    public ContentStatus Status { get; set; }
}

// Automatic history tracking
public class ArticleHistory
{
    public Guid Id { get; set; }
    public Guid ArticleId { get; set; }
    public int VersionNumber { get; set; }

    // Copy of all fields at this version
    public string Title { get; set; } = string.Empty;
    public string Body { get; set; } = string.Empty;

    // Audit info
    public DateTime ValidFrom { get; set; }
    public DateTime ValidTo { get; set; }
    public string ModifiedBy { get; set; } = string.Empty;
    public ChangeType ChangeType { get; set; }
}

public enum ChangeType
{
    Created,
    Updated,
    Published,
    Unpublished,
    Deleted
}
```

### Strategy 3: Event Sourcing

```csharp
public abstract class ContentEvent
{
    public Guid Id { get; set; }
    public Guid ContentItemId { get; set; }
    public DateTime OccurredUtc { get; set; }
    public string UserId { get; set; } = string.Empty;
    public int SequenceNumber { get; set; }
}

public class ContentCreatedEvent : ContentEvent
{
    public string ContentType { get; set; } = string.Empty;
    public string InitialDataJson { get; set; } = string.Empty;
}

public class ContentUpdatedEvent : ContentEvent
{
    public Dictionary<string, FieldChange> Changes { get; set; } = new();
}

public class ContentPublishedEvent : ContentEvent
{
    public int PublishedVersion { get; set; }
}

public class FieldChange
{
    public object? OldValue { get; set; }
    public object? NewValue { get; set; }
}
```

## Draft/Publish Workflow

### Basic Implementation

```csharp
public class ContentPublishingService
{
    public async Task<ContentItem> CreateDraftAsync(
        string contentType,
        object data,
        string userId)
    {
        var item = new ContentItem
        {
            Id = Guid.NewGuid(),
            ContentType = contentType,
            Status = ContentStatus.Draft,
            Version = 1,
            CreatedUtc = DateTime.UtcNow,
            ModifiedUtc = DateTime.UtcNow
        };

        var version = new ContentVersion
        {
            Id = Guid.NewGuid(),
            ContentItemId = item.Id,
            VersionNumber = 1,
            DataJson = JsonSerializer.Serialize(data),
            CreatedBy = userId,
            CreatedUtc = DateTime.UtcNow,
            IsPublished = false
        };

        item.DraftVersionId = version.Id;

        await _repository.AddAsync(item);
        await _versionRepository.AddAsync(version);

        return item;
    }

    public async Task PublishAsync(Guid contentItemId, string userId)
    {
        var item = await _repository.GetAsync(contentItemId);
        if (item == null || item.DraftVersionId == null)
            throw new InvalidOperationException("No draft to publish");

        var draft = await _versionRepository.GetAsync(item.DraftVersionId.Value);

        // Create published version from draft
        var published = new ContentVersion
        {
            Id = Guid.NewGuid(),
            ContentItemId = item.Id,
            VersionNumber = item.Version + 1,
            DataJson = draft!.DataJson,
            CreatedBy = userId,
            CreatedUtc = DateTime.UtcNow,
            IsPublished = true
        };

        await _versionRepository.AddAsync(published);

        // Update content item
        item.Version = published.VersionNumber;
        item.PublishedVersionId = published.Id;
        item.Status = ContentStatus.Published;
        item.PublishedUtc = DateTime.UtcNow;
        item.ModifiedUtc = DateTime.UtcNow;

        await _repository.UpdateAsync(item);

        // Raise event
        await _mediator.Publish(new ContentPublishedEvent(item.Id));
    }

    public async Task UnpublishAsync(Guid contentItemId, string userId)
    {
        var item = await _repository.GetAsync(contentItemId);
        if (item == null)
            throw new InvalidOperationException("Content not found");

        item.Status = ContentStatus.Unpublished;
        item.PublishedVersionId = null;
        item.ModifiedUtc = DateTime.UtcNow;

        await _repository.UpdateAsync(item);
        await _mediator.Publish(new ContentUnpublishedEvent(item.Id));
    }
}
```

### Simultaneous Draft and Published

```csharp
public class ContentQueryService
{
    public async Task<ContentVersion?> GetPublishedAsync(Guid contentItemId)
    {
        var item = await _repository.GetAsync(contentItemId);
        if (item?.PublishedVersionId == null)
            return null;

        return await _versionRepository.GetAsync(item.PublishedVersionId.Value);
    }

    public async Task<ContentVersion?> GetDraftAsync(Guid contentItemId)
    {
        var item = await _repository.GetAsync(contentItemId);
        if (item?.DraftVersionId == null)
            return null;

        return await _versionRepository.GetAsync(item.DraftVersionId.Value);
    }

    public async Task<ContentVersion?> GetLatestAsync(
        Guid contentItemId,
        bool preferDraft = false)
    {
        var item = await _repository.GetAsync(contentItemId);
        if (item == null) return null;

        if (preferDraft && item.DraftVersionId != null)
            return await _versionRepository.GetAsync(item.DraftVersionId.Value);

        if (item.PublishedVersionId != null)
            return await _versionRepository.GetAsync(item.PublishedVersionId.Value);

        return null;
    }
}
```

## Version History

### Retrieving History

```csharp
public async Task<List<ContentVersionSummary>> GetVersionHistoryAsync(
    Guid contentItemId,
    int page = 1,
    int pageSize = 20)
{
    return await _context.ContentVersions
        .Where(v => v.ContentItemId == contentItemId)
        .OrderByDescending(v => v.VersionNumber)
        .Skip((page - 1) * pageSize)
        .Take(pageSize)
        .Select(v => new ContentVersionSummary
        {
            Id = v.Id,
            VersionNumber = v.VersionNumber,
            CreatedBy = v.CreatedBy,
            CreatedUtc = v.CreatedUtc,
            ChangeNote = v.ChangeNote,
            IsPublished = v.IsPublished
        })
        .ToListAsync();
}
```

### Rollback

```csharp
public async Task RollbackToVersionAsync(
    Guid contentItemId,
    int targetVersion,
    string userId)
{
    var item = await _repository.GetAsync(contentItemId);
    var targetVersionRecord = await _versionRepository
        .GetByVersionNumberAsync(contentItemId, targetVersion);

    if (item == null || targetVersionRecord == null)
        throw new InvalidOperationException("Invalid rollback target");

    // Create new version from old data
    var rollbackVersion = new ContentVersion
    {
        Id = Guid.NewGuid(),
        ContentItemId = item.Id,
        VersionNumber = item.Version + 1,
        DataJson = targetVersionRecord.DataJson,
        CreatedBy = userId,
        CreatedUtc = DateTime.UtcNow,
        ChangeNote = $"Rolled back to version {targetVersion}",
        IsPublished = false
    };

    await _versionRepository.AddAsync(rollbackVersion);

    item.Version = rollbackVersion.VersionNumber;
    item.DraftVersionId = rollbackVersion.Id;
    item.ModifiedUtc = DateTime.UtcNow;

    await _repository.UpdateAsync(item);
}
```

## Version Comparison

### Generating Diffs

```csharp
public class VersionComparisonService
{
    public VersionDiff Compare(ContentVersion older, ContentVersion newer)
    {
        var oldData = JsonSerializer.Deserialize<Dictionary<string, JsonElement>>(
            older.DataJson);
        var newData = JsonSerializer.Deserialize<Dictionary<string, JsonElement>>(
            newer.DataJson);

        var diff = new VersionDiff
        {
            OlderVersion = older.VersionNumber,
            NewerVersion = newer.VersionNumber
        };

        // Find added fields
        foreach (var key in newData!.Keys.Except(oldData!.Keys))
        {
            diff.Changes.Add(new FieldDiff
            {
                FieldName = key,
                ChangeType = DiffChangeType.Added,
                NewValue = newData[key].ToString()
            });
        }

        // Find removed fields
        foreach (var key in oldData.Keys.Except(newData.Keys))
        {
            diff.Changes.Add(new FieldDiff
            {
                FieldName = key,
                ChangeType = DiffChangeType.Removed,
                OldValue = oldData[key].ToString()
            });
        }

        // Find modified fields
        foreach (var key in oldData.Keys.Intersect(newData.Keys))
        {
            var oldJson = oldData[key].ToString();
            var newJson = newData[key].ToString();

            if (oldJson != newJson)
            {
                diff.Changes.Add(new FieldDiff
                {
                    FieldName = key,
                    ChangeType = DiffChangeType.Modified,
                    OldValue = oldJson,
                    NewValue = newJson
                });
            }
        }

        return diff;
    }
}

public class VersionDiff
{
    public int OlderVersion { get; set; }
    public int NewerVersion { get; set; }
    public List<FieldDiff> Changes { get; set; } = new();
}

public class FieldDiff
{
    public string FieldName { get; set; } = string.Empty;
    public DiffChangeType ChangeType { get; set; }
    public string? OldValue { get; set; }
    public string? NewValue { get; set; }
}

public enum DiffChangeType
{
    Added,
    Removed,
    Modified
}
```

## Audit Trail

### Audit Log Entry

```csharp
public class ContentAuditEntry
{
    public Guid Id { get; set; }
    public Guid ContentItemId { get; set; }
    public string ContentType { get; set; } = string.Empty;
    public string Action { get; set; } = string.Empty; // Created, Updated, Published, etc.
    public string UserId { get; set; } = string.Empty;
    public string UserName { get; set; } = string.Empty;
    public DateTime OccurredUtc { get; set; }
    public string? IpAddress { get; set; }
    public string? UserAgent { get; set; }
    public string? ChangeSummary { get; set; }
    public string? DataBefore { get; set; }
    public string? DataAfter { get; set; }
}
```

### Automatic Audit Logging

```csharp
public class AuditInterceptor : SaveChangesInterceptor
{
    private readonly ICurrentUserService _currentUser;
    private readonly IHttpContextAccessor _httpContext;

    public override async ValueTask<InterceptionResult<int>> SavingChangesAsync(
        DbContextEventData eventData,
        InterceptionResult<int> result,
        CancellationToken cancellationToken = default)
    {
        var context = eventData.Context;
        if (context == null) return result;

        var entries = context.ChangeTracker.Entries<ContentItem>()
            .Where(e => e.State is EntityState.Added
                     or EntityState.Modified
                     or EntityState.Deleted);

        foreach (var entry in entries)
        {
            var audit = new ContentAuditEntry
            {
                Id = Guid.NewGuid(),
                ContentItemId = entry.Entity.Id,
                ContentType = entry.Entity.ContentType,
                Action = entry.State.ToString(),
                UserId = _currentUser.UserId,
                UserName = _currentUser.UserName,
                OccurredUtc = DateTime.UtcNow,
                IpAddress = _httpContext.HttpContext?.Connection.RemoteIpAddress?.ToString()
            };

            if (entry.State == EntityState.Modified)
            {
                audit.DataBefore = JsonSerializer.Serialize(
                    entry.OriginalValues.ToObject());
                audit.DataAfter = JsonSerializer.Serialize(
                    entry.CurrentValues.ToObject());
            }

            context.Set<ContentAuditEntry>().Add(audit);
        }

        return result;
    }
}
```

## API Design

### Version Endpoints

```text
GET    /api/content/{id}/versions              # List version history
GET    /api/content/{id}/versions/{version}    # Get specific version
GET    /api/content/{id}/versions/compare?v1=1&v2=2  # Compare versions
POST   /api/content/{id}/versions/{version}/restore  # Rollback
GET    /api/content/{id}/audit                 # Audit trail
```

## Related Skills

- `content-type-modeling` - Versionable content types
- `content-workflow` - Editorial approval workflows
- `headless-api-design` - Version API endpoints
