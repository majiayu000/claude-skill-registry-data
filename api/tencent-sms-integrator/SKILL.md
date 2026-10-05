---
name: tencent-sms-integrator
description: Integrate Tencent Cloud SMS for verification codes and notifications. Use this skill when the application needs SMS verification codes, system notifications, order alerts, or batch SMS sending. Triggers on requests for SMS sending, verification codes, phone authentication, or notification messages.
_meta_type: sdk
---

# Tencent Cloud SMS SDK Integration

## Scenarios

- **SMS Verification Codes**: Send verification codes for user registration, login, and identity verification
- **Notification SMS**: System notifications like order status, delivery reminders, appointment confirmations
- **Marketing SMS**: Promotional campaigns, membership notifications (requires user consent)
- **Batch Sending**: Send SMS to multiple recipients, up to 200 numbers per request
- **Transaction Alerts**: Payment confirmations, security alerts

**Not recommended for:**
- Unsolicited marketing SMS (requires opt-in)
- High-frequency sending scenarios (rate limits apply)
- Two-way communication requiring immediate replies
- Direct frontend calls (credentials must be protected)

## Setup

### 1. Install Dependencies

```bash
npm install tencentcloud-sdk-nodejs
```

### 2. Copy SDK Wrapper

Read `lib/tencent-sms.ts` from this skill and copy it to the project, then use it directly.

## Configuration

### Zero Configuration (Default)

Genie provides default zero-configuration support using `sms.tencent_cloud.auth-proxy.local` as the endpoint. **No environment variables are required** - Genie has integrated authentication in the proxy gateway by default.

Simply use:

```typescript
import { createClient } from './lib/tencent-sms';
const client = createClient();
```

### Custom Configuration (Optional)

Users can optionally configure environment variables. When configured, Genie will use user-provided credentials instead of the default proxy:

```env
# Optional - Only configure if you want to use your own credentials
TENCENT_SMS_SECRET_ID=your-secret-id-here
TENCENT_SMS_SECRET_KEY=your-secret-key-here
TENCENT_SMS_SDK_APP_ID=your-sms-app-id
TENCENT_SMS_SIGN_NAME=YourSignature
TENCENT_SMS_TEMPLATE_ID=your-template-id
```

**Obtaining Credentials** (if needed):
1. Visit [Tencent Cloud Console - API Keys](https://console.cloud.tencent.com/cam/capi)
2. Create or retrieve SecretId and SecretKey
3. Visit [SMS Console](https://console.cloud.tencent.com/smsv2)
4. Create an application to get SmsSdkAppId
5. Create and get approval for signature and template

### Prerequisites

- Tencent Cloud SMS service activated
- SMS signature created and approved
- SMS template created and approved
- SMS package purchased (required for domestic SMS in China)

## Quick Start

### Basic Usage

```typescript
import { createClient } from './lib/tencent-sms';

const client = createClient();

// Send verification code
const code = '123456';
const result = await client.sendSms({
  phoneNumber: '+8613800138000',
  templateId: '449739',
  templateParams: [code, '5']  // code, expiry in minutes
});

console.log('Send result:', result);
```

### Send Verification Code (Convenience Method)

```typescript
// Auto-generate and send verification code
const { code, success, result } = await client.sendVerificationCode(
  '+8613800138000',
  '449739',
  6,  // code length
  5   // expiry minutes
);

if (success) {
  // Store code for later verification
  console.log('Verification code:', code);
}
```

### Batch Send

```typescript
// Send to multiple recipients (max 200)
const result = await client.sendBatchSms({
  phoneNumbers: ['+8613800138000', '+8613800138001'],
  templateId: '449739',
  templateParams: ['Order shipped']
});

result.sendStatusSet.forEach(status => {
  console.log(`${status.phoneNumber}: ${status.code}`);
});
```

## Response Structure

```typescript
// Send SMS Result
{
  sendStatusSet: Array<{
    serialNo: string;      // Serial number
    phoneNumber: string;   // Phone number
    fee: number;           // Billable messages count
    sessionContext: string; // Session context
    code: string;          // "Ok" means success
    message: string;       // Status description
    isoCode: string;       // ISO country code
  }>;
  requestId: string;
}
```

## Architecture Integration

### Service Layer Pattern (Recommended)

```typescript
// src/services/sms.service.ts
import { createClient } from '../lib/tencent-sms';

export class SMSService {
  private smsClient = createClient();
  
  async sendVerificationCode(phone: string): Promise<{ code: string; success: boolean }> {
    const code = Math.random().toString().slice(2, 8);
    
    const result = await this.smsClient.sendSms({
      phoneNumber: phone.startsWith('+') ? phone : `+86${phone}`,
      templateId: process.env.TENCENT_SMS_TEMPLATE_ID!,
      templateParams: [code, '5']
    });
    
    return { 
      code, 
      success: result.sendStatusSet[0]?.code === 'Ok' 
    };
  }
  
  async sendBatchNotification(phones: string[], params: string[]): Promise<boolean> {
    const result = await this.smsClient.sendBatchSms({
      phoneNumbers: phones.map(p => p.startsWith('+') ? p : `+86${p}`),
      templateId: process.env.TENCENT_SMS_NOTIFICATION_TEMPLATE_ID!,
      templateParams: params
    });
    
    return result.sendStatusSet.every(s => s.code === 'Ok');
  }
}
```

### Express Route Example

```typescript
// src/routes/auth.routes.ts
import { Router } from 'express';
import { SMSService } from '../services/sms.service';

const router = Router();
const smsService = new SMSService();
const codeStore = new Map<string, { code: string; expires: number }>();

router.post('/send-code', async (req, res) => {
  const { phone } = req.body;
  
  const { code, success } = await smsService.sendVerificationCode(phone);
  
  if (success) {
    codeStore.set(phone, { code, expires: Date.now() + 5 * 60 * 1000 });
    res.json({ success: true, message: 'Verification code sent' });
  } else {
    res.status(500).json({ success: false, message: 'Failed to send' });
  }
});

router.post('/verify-code', (req, res) => {
  const { phone, code } = req.body;
  const stored = codeStore.get(phone);
  
  if (!stored || Date.now() > stored.expires) {
    return res.status(400).json({ success: false, message: 'Code expired' });
  }
  
  if (stored.code !== code) {
    return res.status(400).json({ success: false, message: 'Invalid code' });
  }
  
  codeStore.delete(phone);
  res.json({ success: true, message: 'Verification successful' });
});
```

## Rate Limits

| Limit | Value |
|-------|-------|
| Same number, same content | Max 1 per 30 seconds |
| Same number | Max 5 per hour |
| Same number | Max 10 per day |

## Security Best Practices

1. **Never commit credentials**: Add `.env` to `.gitignore`
2. **Rate limiting**: Implement send frequency limits (e.g., once per 60 seconds)
3. **Code expiry**: Set reasonable expiration time (3-5 minutes)
4. **Attempt limiting**: Limit verification code error attempts
5. **Use Redis**: Use Redis for verification code storage in production

## Troubleshooting

**Signature/Template Approval Failed**
- Ensure signature content matches actual business
- Template content must not contain prohibited words
- Enterprise accounts get faster approval than personal accounts

**Send Failed**
- Check phone number format (E.164 standard: +86xxx)
- Verify SMS package balance is sufficient
- Confirm SmsSdkAppId is correct

**Authentication Errors**
- Verify credentials in `.env` file if using custom configuration
- Check if API key is active in the console

## Resources

- **SDK Wrapper Source**: `lib/tencent-sms.ts`
- **Official Documentation**: https://cloud.tencent.com/document/product/382
- **API Reference**: https://cloud.tencent.com/document/product/382/43197
- **Console**: https://console.cloud.tencent.com/smsv2
