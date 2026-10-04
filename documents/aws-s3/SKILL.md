---
name: aws-s3
description: Manages file storage with AWS S3 using the JavaScript SDK v3. Use when uploading files, generating presigned URLs, managing buckets, or implementing cloud storage in Node.js applications.
---

# AWS S3 (JavaScript SDK v3)

Object storage with the AWS SDK for JavaScript v3. Upload files, generate presigned URLs, and manage buckets.

## Quick Start

```bash
npm install @aws-sdk/client-s3 @aws-sdk/s3-request-presigner
```

### Configure Client

```javascript
import { S3Client } from '@aws-sdk/client-s3';

const s3Client = new S3Client({
  region: process.env.AWS_REGION || 'us-east-1',
  credentials: {
    accessKeyId: process.env.AWS_ACCESS_KEY_ID,
    secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY,
  },
});
```

## Upload Files

### Basic Upload

```javascript
import { PutObjectCommand } from '@aws-sdk/client-s3';

async function uploadFile(bucket, key, body, contentType) {
  const command = new PutObjectCommand({
    Bucket: bucket,
    Key: key,
    Body: body,
    ContentType: contentType,
  });

  await s3Client.send(command);
  return `https://${bucket}.s3.amazonaws.com/${key}`;
}

// Usage
await uploadFile(
  'my-bucket',
  'uploads/image.jpg',
  fileBuffer,
  'image/jpeg'
);
```

### With Options

```javascript
import { PutObjectCommand } from '@aws-sdk/client-s3';

const command = new PutObjectCommand({
  Bucket: 'my-bucket',
  Key: 'documents/report.pdf',
  Body: fileBuffer,
  ContentType: 'application/pdf',

  // Access control
  ACL: 'private',  // private, public-read, public-read-write

  // Metadata
  Metadata: {
    'uploaded-by': 'user-123',
    'original-name': 'quarterly-report.pdf',
  },

  // Caching
  CacheControl: 'max-age=31536000',

  // Server-side encryption
  ServerSideEncryption: 'AES256',

  // Content disposition
  ContentDisposition: 'attachment; filename="report.pdf"',

  // Tags
  Tagging: 'environment=production&type=report',
});

await s3Client.send(command);
```

### Multipart Upload (Large Files)

```javascript
import { Upload } from '@aws-sdk/lib-storage';

async function uploadLargeFile(bucket, key, body) {
  const upload = new Upload({
    client: s3Client,
    params: {
      Bucket: bucket,
      Key: key,
      Body: body,
    },
    queueSize: 4,  // Concurrent parts
    partSize: 5 * 1024 * 1024,  // 5MB parts
    leavePartsOnError: false,
  });

  upload.on('httpUploadProgress', (progress) => {
    console.log(`Progress: ${progress.loaded}/${progress.total}`);
  });

  await upload.done();
}
```

## Download Files

```javascript
import { GetObjectCommand } from '@aws-sdk/client-s3';

async function downloadFile(bucket, key) {
  const command = new GetObjectCommand({
    Bucket: bucket,
    Key: key,
  });

  const response = await s3Client.send(command);

  // Convert stream to buffer
  const chunks = [];
  for await (const chunk of response.Body) {
    chunks.push(chunk);
  }
  return Buffer.concat(chunks);
}

// Or get as string
async function getFileAsString(bucket, key) {
  const command = new GetObjectCommand({
    Bucket: bucket,
    Key: key,
  });

  const response = await s3Client.send(command);
  return response.Body.transformToString();
}
```

## Presigned URLs

Generate temporary URLs for upload/download without sharing credentials.

### Presigned Download URL

```javascript
import { GetObjectCommand } from '@aws-sdk/client-s3';
import { getSignedUrl } from '@aws-sdk/s3-request-presigner';

async function getDownloadUrl(bucket, key, expiresIn = 3600) {
  const command = new GetObjectCommand({
    Bucket: bucket,
    Key: key,
  });

  const url = await getSignedUrl(s3Client, command, { expiresIn });
  return url;
}

// Usage - valid for 1 hour
const downloadUrl = await getDownloadUrl('my-bucket', 'files/doc.pdf');
```

### Presigned Upload URL

```javascript
import { PutObjectCommand } from '@aws-sdk/client-s3';
import { getSignedUrl } from '@aws-sdk/s3-request-presigner';

async function getUploadUrl(bucket, key, contentType, expiresIn = 3600) {
  const command = new PutObjectCommand({
    Bucket: bucket,
    Key: key,
    ContentType: contentType,
  });

  const url = await getSignedUrl(s3Client, command, { expiresIn });
  return url;
}

// Usage
const uploadUrl = await getUploadUrl(
  'my-bucket',
  'uploads/image.jpg',
  'image/jpeg'
);

// Client can PUT to this URL
await fetch(uploadUrl, {
  method: 'PUT',
  body: file,
  headers: {
    'Content-Type': 'image/jpeg',
  },
});
```

### Presigned POST (Browser Uploads)

```javascript
import { createPresignedPost } from '@aws-sdk/s3-presigned-post';

async function getUploadForm(bucket, key) {
  const { url, fields } = await createPresignedPost(s3Client, {
    Bucket: bucket,
    Key: key,
    Conditions: [
      ['content-length-range', 0, 10 * 1024 * 1024],  // Max 10MB
      ['starts-with', '$Content-Type', 'image/'],
    ],
    Expires: 3600,
  });

  return { url, fields };
}

// Client-side usage
const { url, fields } = await getUploadForm('my-bucket', 'uploads/${filename}');

const formData = new FormData();
Object.entries(fields).forEach(([key, value]) => {
  formData.append(key, value);
});
formData.append('file', file);

await fetch(url, {
  method: 'POST',
  body: formData,
});
```

## List Objects

```javascript
import { ListObjectsV2Command } from '@aws-sdk/client-s3';

async function listFiles(bucket, prefix = '') {
  const command = new ListObjectsV2Command({
    Bucket: bucket,
    Prefix: prefix,
    MaxKeys: 100,
  });

  const response = await s3Client.send(command);

  return response.Contents?.map((item) => ({
    key: item.Key,
    size: item.Size,
    lastModified: item.LastModified,
  })) || [];
}

// Paginate through all files
async function* listAllFiles(bucket, prefix = '') {
  let continuationToken;

  do {
    const command = new ListObjectsV2Command({
      Bucket: bucket,
      Prefix: prefix,
      ContinuationToken: continuationToken,
    });

    const response = await s3Client.send(command);

    for (const item of response.Contents || []) {
      yield item;
    }

    continuationToken = response.NextContinuationToken;
  } while (continuationToken);
}

// Usage
for await (const file of listAllFiles('my-bucket', 'uploads/')) {
  console.log(file.Key);
}
```

## Delete Files

```javascript
import { DeleteObjectCommand, DeleteObjectsCommand } from '@aws-sdk/client-s3';

// Delete single file
async function deleteFile(bucket, key) {
  const command = new DeleteObjectCommand({
    Bucket: bucket,
    Key: key,
  });

  await s3Client.send(command);
}

// Delete multiple files
async function deleteFiles(bucket, keys) {
  const command = new DeleteObjectsCommand({
    Bucket: bucket,
    Delete: {
      Objects: keys.map((Key) => ({ Key })),
    },
  });

  const response = await s3Client.send(command);
  return response.Deleted;
}

// Usage
await deleteFiles('my-bucket', [
  'uploads/old1.jpg',
  'uploads/old2.jpg',
]);
```

## Copy & Move Files

```javascript
import { CopyObjectCommand, DeleteObjectCommand } from '@aws-sdk/client-s3';

async function copyFile(bucket, sourceKey, destinationKey) {
  const command = new CopyObjectCommand({
    Bucket: bucket,
    CopySource: `${bucket}/${sourceKey}`,
    Key: destinationKey,
  });

  await s3Client.send(command);
}

async function moveFile(bucket, sourceKey, destinationKey) {
  await copyFile(bucket, sourceKey, destinationKey);
  await deleteFile(bucket, sourceKey);
}
```

## Check If File Exists

```javascript
import { HeadObjectCommand } from '@aws-sdk/client-s3';

async function fileExists(bucket, key) {
  try {
    const command = new HeadObjectCommand({
      Bucket: bucket,
      Key: key,
    });

    await s3Client.send(command);
    return true;
  } catch (error) {
    if (error.name === 'NotFound') {
      return false;
    }
    throw error;
  }
}
```

## Next.js API Routes

```typescript
// app/api/upload/route.ts
import { NextRequest, NextResponse } from 'next/server';
import { PutObjectCommand } from '@aws-sdk/client-s3';
import { getSignedUrl } from '@aws-sdk/s3-request-presigner';
import { s3Client } from '@/lib/s3';

export async function POST(request: NextRequest) {
  const { filename, contentType } = await request.json();

  const key = `uploads/${Date.now()}-${filename}`;

  const command = new PutObjectCommand({
    Bucket: process.env.S3_BUCKET!,
    Key: key,
    ContentType: contentType,
  });

  const uploadUrl = await getSignedUrl(s3Client, command, { expiresIn: 3600 });

  return NextResponse.json({
    uploadUrl,
    key,
    publicUrl: `https://${process.env.S3_BUCKET}.s3.amazonaws.com/${key}`,
  });
}
```

```tsx
// Client component
async function handleUpload(file: File) {
  // Get presigned URL
  const response = await fetch('/api/upload', {
    method: 'POST',
    body: JSON.stringify({
      filename: file.name,
      contentType: file.type,
    }),
  });

  const { uploadUrl, publicUrl } = await response.json();

  // Upload directly to S3
  await fetch(uploadUrl, {
    method: 'PUT',
    body: file,
    headers: {
      'Content-Type': file.type,
    },
  });

  return publicUrl;
}
```

## CORS Configuration

Set in AWS Console or via SDK:

```json
[
  {
    "AllowedHeaders": ["*"],
    "AllowedMethods": ["GET", "PUT", "POST", "DELETE"],
    "AllowedOrigins": ["https://yourdomain.com"],
    "ExposeHeaders": ["ETag"]
  }
]
```

## With CloudFront

Use CloudFront for CDN delivery:

```javascript
const cloudFrontUrl = `https://d1234.cloudfront.net/${key}`;
```

## R2 Compatibility (Cloudflare)

S3 SDK works with Cloudflare R2:

```javascript
const s3Client = new S3Client({
  region: 'auto',
  endpoint: `https://${accountId}.r2.cloudflarestorage.com`,
  credentials: {
    accessKeyId: R2_ACCESS_KEY_ID,
    secretAccessKey: R2_SECRET_ACCESS_KEY,
  },
});
```

## Best Practices

1. **Use presigned URLs** for client uploads (don't expose credentials)
2. **Set appropriate CORS** for browser uploads
3. **Use multipart upload** for files > 100MB
4. **Enable versioning** for important buckets
5. **Set lifecycle rules** to clean up old files
6. **Use CloudFront** for public files (faster, cheaper)
7. **Encrypt sensitive data** with SSE
