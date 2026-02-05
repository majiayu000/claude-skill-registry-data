---
name: image-management
description: Centralized polymorphic image management with CheckboxList picker, WebP auto-conversion, order management (order=0 for cover), soft deletes. USE WHEN adding images/gallery to models, implementing image upload, working with ImagesRelationManager, or fixing image errors.
---
---
## When to Use

- Adding image gallery to models
- Implementing single featured image
- Setting up logo/favicon
- Fixing image upload issues
- Working with ImagesRelationManager
- Image picker implementation


---
## System Overview

**Centralized Polymorphic:**
- Single `images` table for ALL entities
- Polymorphic relationships
- Order management (0 = cover)
- Auto WebP conversion (85%)
- Soft deletes with cleanup
- CheckboxList picker (native Filament)


---
---
## ImagesRelationManager

**Auto-generated features:**
- Upload with drag-drop
- Reorder with drag-drop
- Set cover (order=0)
- Edit alt text/title
- Delete with confirmation
- WebP auto-conversion

**Generate:**
```bash
php artisan make:filament-relation-manager ProductResource images file_path
```


---
## ImageObserver

**Auto-features:**
- Alt text from model name
- Order auto-increment
- Cover auto-set
- Soft delete cleanup

```php
class ImageObserver
{
    public function creating(Image $image): void
    {
        if (empty($image->alt_text) && $image->model) {
            $image->alt_text = $image->model->name ?? 'Image';
        }
        
        if ($image->order === null) {
            $max = Image::where('model_type', $image->model_type)
                ->where('model_id', $image->model_id)
                ->max('order');
            $image->order = ($max ?? -1) + 1;
        }
    }
}
```


---
## WebP Conversion

**Automatic on upload:**
- Original preserved
- WebP created (85% quality)
- Stored in `storage/app/public/images/`
- Auto-served via intervention

**Manual conversion:**
```php
$webpPath = Image::convertToWebP($originalPath);
```


---
## Common Issues

### Issue: Unique constraint violation on order

**Solution:**
```php
// ImageObserver handles auto-increment
// Don't manually set order=0 for all images
```

### Issue: Images not showing

**Check:**
1. Storage link: `php artisan storage:link`
2. Disk config: `config/filesystems.php`
3. Image path: `Storage::url($image->file_path)`

### Issue: Multiple covers (order=0)

**Solution:**
```php
// When setting new cover
Image::where('model_type', $type)
    ->where('model_id', $id)
    ->where('order', 0)
    ->update(['order' => 999]);  // Reset old cover

$newCover->update(['order' => 0]);
```


## Complete Guide

For detailed implementation, advanced patterns, and troubleshooting:

`read .claude/skills/filament/image-management/CLAUDE.md`

**Related:**
- Filament standards: `read .claude/skills/filament/filament-rules/SKILL.md`
- Resource generator: `read .claude/skills/filament/filament-resource-generator/SKILL.md`


---

## References

**Quick Patterns:** `read .claude/skills/filament/image-management/references/quick-patterns.md`
