---
name: supabase-storage
description: Apply when handling file uploads, downloads, and storage management in Supabase.
version: 1.0.0
tokens: ~550
confidence: high
sources:
  - https://supabase.com/docs/guides/storage
  - https://supabase.com/docs/reference/javascript/storage-from-upload
last_validated: 2025-01-10
next_review: 2025-01-24
tags: [supabase, storage, files, uploads]
---

## When to Use

Apply when handling file uploads, downloads, and storage management in Supabase.

## Patterns

### Pattern 1: Upload File
```typescript
// Source: https://supabase.com/docs/reference/javascript/storage-from-upload
async function uploadFile(file: File, userId: string) {
  const fileExt = file.name.split('.').pop();
  const fileName = `${userId}/${Date.now()}.${fileExt}`;

  const { data, error } = await supabase.storage
    .from('avatars') // bucket name
    .upload(fileName, file, {
      cacheControl: '3600',
      upsert: false, // false = error if exists, true = overwrite
    });

  if (error) throw error;
  return data.path;
}
```

### Pattern 2: Get Public URL
```typescript
// Source: https://supabase.com/docs/reference/javascript/storage-from-getpublicurl
// For public buckets
const { data } = supabase.storage
  .from('avatars')
  .getPublicUrl('user123/avatar.png');

const publicUrl = data.publicUrl;

// With transformations
const { data } = supabase.storage
  .from('avatars')
  .getPublicUrl('user123/avatar.png', {
    transform: { width: 200, height: 200, resize: 'cover' },
  });
```

### Pattern 3: Signed URL (Private Buckets)
```typescript
// Source: https://supabase.com/docs/reference/javascript/storage-from-createsignedurl
const { data, error } = await supabase.storage
  .from('private-docs')
  .createSignedUrl('user123/document.pdf', 3600); // 1 hour expiry

if (data) {
  window.open(data.signedUrl, '_blank');
}
```

### Pattern 4: Delete File
```typescript
// Source: https://supabase.com/docs/reference/javascript/storage-from-remove
const { error } = await supabase.storage
  .from('avatars')
  .remove(['user123/old-avatar.png']);

// Delete multiple
const { error } = await supabase.storage
  .from('avatars')
  .remove(['file1.png', 'file2.png', 'file3.png']);
```

### Pattern 5: React Upload Component
```typescript
// Source: https://supabase.com/docs/guides/storage
function AvatarUpload({ userId, onUpload }: Props) {
  const [uploading, setUploading] = useState(false);

  const handleUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setUploading(true);
    try {
      const path = await uploadFile(file, userId);
      onUpload(path);
    } catch (error) {
      alert('Upload failed');
    } finally {
      setUploading(false);
    }
  };

  return (
    <input
      type="file"
      accept="image/*"
      onChange={handleUpload}
      disabled={uploading}
    />
  );
}
```

## Anti-Patterns

- **No file validation** - Check size/type before upload
- **Predictable paths** - Use UUIDs or timestamps in paths
- **No error handling** - Handle upload failures gracefully
- **Missing RLS on bucket** - Configure storage policies

## Verification Checklist

- [ ] File size limit enforced client-side
- [ ] File type validation (accept attribute + server)
- [ ] Unique file paths (prevent overwrites)
- [ ] Storage policies configured for bucket
- [ ] Loading state during upload
