---
name: tencent-face-compare-integrator
description: Integrate Tencent Cloud Face Compare for identity verification and face similarity detection. Use this skill when the application needs face check-in, access control, ID verification, or photo matching. Triggers on requests for face comparison, identity verification, face sign-in, or similarity detection.
_meta_type: sdk
---

# Tencent Cloud Face Compare SDK Integration

## Scenarios

- **Face Sign-in/Check-in**: Match user photo against stored reference for attendance
- **Identity Verification**: Compare ID photo with live capture for KYC
- **Access Control Systems**: Compare visitor face with pre-registered photos
- **Photo Matching**: Verify if two photos belong to the same person
- **User Authentication**: Add face verification as a security layer

**Not recommended for:**
- Face enrollment/registration (use dedicated face database APIs)
- Multi-face detection in group photos
- Real-time video stream analysis
- Liveness detection (use dedicated liveness API)

## Setup

### 1. Install Dependencies

```bash
npm install tencentcloud-sdk-nodejs-iai
```

### 2. Copy SDK Wrapper

Read `lib/tencent-face-compare.ts` from this skill and copy it to the project, then use it directly.

## Configuration

### Zero Configuration (Default)

Genie provides default zero-configuration support using `iai.tencent_cloud.auth-proxy.local` as the endpoint. **No environment variables are required** - Genie has integrated authentication in the proxy gateway by default.

Simply use:

```typescript
import { createFaceCompareClient } from './lib/tencent-face-compare';
const client = createFaceCompareClient();
```

### Custom Configuration (Optional)

Users can optionally configure environment variables. When configured, Genie will use user-provided credentials instead of the default proxy:

```env
# Optional - Only configure if you want to use your own credentials
TENCENT_FACE_COMPARE_SECRET_ID=your-secret-id
TENCENT_FACE_COMPARE_SECRET_KEY=your-secret-key
TENCENT_FACE_COMPARE_REGION=ap-guangzhou
```

**Obtaining Credentials** (if needed):
1. Visit [Tencent Cloud Console - Access Keys](https://console.cloud.tencent.com/cam/capi)
2. Create or use existing SecretId/SecretKey pair
3. Enable IAI (Face Recognition) service in console

## Quick Start

### Basic Usage

```typescript
import { createFaceCompareClient, compareFaces } from './lib/tencent-face-compare';

const client = createFaceCompareClient();

// Compare two face images
const result = await compareFaces(client, {
  imageA: base64ImageA,  // Reference photo (stored)
  imageB: base64ImageB   // Live captured photo
});

if (result.isSamePerson) {
  console.log('Identity verified, score:', result.score);
}
```

### Face Comparison with Quality Control

```typescript
const result = await compareFaces(client, {
  imageA: base64ImageA,
  imageB: base64ImageB,
  qualityControl: 2  // Medium quality requirement
});

// Response
// {
//   score: 95.5,           // Similarity score 0-100
//   isSamePerson: true,    // true if score >= 70
//   isHighConfidence: true, // true if score >= 80
//   requestId: 'xxx'
// }
```

### Using Image URLs

```typescript
import { compareFacesWithUrl } from './lib/tencent-face-compare';

const result = await compareFacesWithUrl(client, {
  urlA: 'https://example.com/reference.jpg',
  urlB: 'https://example.com/captured.jpg'
});
```

## Response Structure

```typescript
{
  score: number;           // Similarity score 0-100
  isSamePerson: boolean;   // true if score >= 70 (1/1000 false positive rate)
  isHighConfidence: boolean; // true if score >= 80 (1/10000 false positive rate)
  requestId: string;       // Request ID for debugging
}
```

## Similarity Thresholds

| Score | Meaning |
|-------|---------|
| >= 70 | Same person (1/1000 false positive rate) |
| >= 80 | High confidence (1/10000 false positive rate) |

## Quality Control Levels

| Level | Description |
|-------|-------------|
| 0 | No quality check (default) |
| 1 | Low: Reject very blurry or occluded faces |
| 2 | Medium: Reject overexposed/underexposed |
| 3 | High: Minor issues rejected |
| 4 | Very high: Best quality required |

## Image Requirements

| Constraint | Requirement |
|------------|-------------|
| Max size | 5MB (base64 encoded) |
| JPG long edge | Max 4000px |
| Other formats | Max 2000px long edge |
| Min short edge | 64px |
| Supported formats | PNG, JPG, JPEG, BMP |
| Not supported | GIF |

## Architecture Integration

### Service Layer Pattern (Recommended)

```typescript
// src/services/face-verify.service.ts
import { createFaceCompareClient, compareFaces } from '../lib/tencent-face-compare';

export class FaceVerifyService {
  private client = createFaceCompareClient();

  async verifyIdentity(
    referenceImage: string,  // Stored user photo
    capturedImage: string    // Live captured photo
  ): Promise<{ verified: boolean; confidence: number }> {
    const result = await compareFaces(this.client, {
      imageA: referenceImage,
      imageB: capturedImage,
      qualityControl: 2  // Medium quality requirement
    });

    return {
      verified: result.isSamePerson,
      confidence: result.score
    };
  }
}
```

### Express Route Example

```typescript
// src/routes/checkin.ts
import { Router } from 'express';
import { FaceVerifyService } from '../services/face-verify.service';

const router = Router();
const faceService = new FaceVerifyService();

router.post('/face-checkin', async (req, res) => {
  const { userId, capturedImage } = req.body;
  
  const user = await getUserById(userId);
  if (!user?.referencePhoto) {
    return res.status(400).json({ error: 'No reference photo found' });
  }

  const result = await faceService.verifyIdentity(
    user.referencePhoto,
    capturedImage
  );

  if (result.verified) {
    await recordCheckin(userId);
    return res.json({ success: true, confidence: result.confidence });
  }

  return res.status(401).json({ 
    success: false, 
    message: 'Face verification failed' 
  });
});
```

## Security Best Practices

1. **Never expose credentials in frontend**: Always call face comparison API from backend
2. **Store reference photos securely**: Use encryption for stored face images
3. **Implement rate limiting**: Prevent brute-force attacks
4. **Log verification attempts**: Create audit trail for security review
5. **Use environment variables**: Never commit credentials to source control

## Troubleshooting

**FailedOperation.FaceQualityNotQualified**
- Face image quality too low
- Solution: Use `qualityControl: 1` or ask user to retake photo

**InvalidParameterValue.NoFaceInPhoto**
- No face detected in image
- Solution: Ensure face is clearly visible and centered

**FailedOperation.ImageSizeExceed**
- Image exceeds 5MB limit
- Solution: Compress image before sending

**ResourceUnavailable.InArrears**
- Account balance insufficient
- Solution: Top up Tencent Cloud account

## Resources

- **SDK Wrapper Source**: `lib/tencent-face-compare.ts`
- **Official Documentation**: https://cloud.tencent.com/document/product/867/44987
- **API Console**: https://console.cloud.tencent.com/aiface
