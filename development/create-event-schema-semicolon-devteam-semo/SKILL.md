---
name: create-event-schema
description: |
  이벤트 스키마 TypeScript 타입 생성. Use when: 이벤트 봉투 및 Zod 스키마 자동 생성 필요 시
tools: [Write, Edit]
---

# create-event-schema Skill

> **🔔 시스템 메시지**: 이 Skill이 호출되면 EventEnvelope 인터페이스와 Zod 스키마를 생성합니다.

> 이벤트 스키마 TypeScript 타입 생성

## Usage

```
skill:create-event-schema
```

## Input

| 파라미터 | 필수 | 설명 |
|----------|------|------|
| eventType | ✅ | 이벤트 타입 (예: job.failed) |
| service | ✅ | 발신 서비스명 |
| dataFields | ❌ | 페이로드 필드 정의 |

## Output

### types/events/{domain}.event.ts

```typescript
import { z } from 'zod';

// Event Envelope Base
export const EventMetadataSchema = z.object({
  eventId: z.string().uuid(),
  service: z.string(),
  type: z.string(),
  severity: z.enum(['info', 'warning', 'error', 'critical']),
  occurredAt: z.string().datetime()
});

export const EventContextSchema = z.object({
  env: z.enum(['development', 'staging', 'production']),
  tenantId: z.string().optional(),
  traceId: z.string().optional(),
  resource: z.object({
    type: z.string(),
    id: z.string()
  }).optional()
});

export const NotificationPolicySchema = z.object({
  throttle: z.object({
    maxPerHour: z.number(),
    maxPerDay: z.number()
  }).optional(),
  retry: z.object({
    maxAttempts: z.number(),
    backoffMs: z.number()
  }).optional()
});

export const EventNotificationSchema = z.object({
  channels: z.array(z.string()),
  targets: z.array(z.string()),
  template: z.string().optional(),
  policy: NotificationPolicySchema.optional()
});

// Service-Specific Event
export const {EventName}DataSchema = z.object({
  // Define your payload fields here
  {dataFields}
});

export const {EventName}EventSchema = z.object({
  metadata: EventMetadataSchema,
  context: EventContextSchema,
  data: {EventName}DataSchema,
  notification: EventNotificationSchema
});

// Type Exports
export type EventMetadata = z.infer<typeof EventMetadataSchema>;
export type EventContext = z.infer<typeof EventContextSchema>;
export type EventNotification = z.infer<typeof EventNotificationSchema>;
export type {EventName}Data = z.infer<typeof {EventName}DataSchema>;
export type {EventName}Event = z.infer<typeof {EventName}EventSchema>;
```

### utils/event-factory.ts

```typescript
import { v4 as uuidv4 } from 'uuid';
import type { EventMetadata, EventContext, EventNotification } from '../types/events';

interface CreateEventOptions<T> {
  type: string;
  service: string;
  severity: EventMetadata['severity'];
  data: T;
  channels?: string[];
  targets?: string[];
}

export function createEvent<T extends Record<string, unknown>>(
  options: CreateEventOptions<T>
) {
  const { type, service, severity, data, channels = ['slack'], targets = [] } = options;

  return {
    metadata: {
      eventId: uuidv4(),
      service,
      type,
      severity,
      occurredAt: new Date().toISOString()
    },
    context: {
      env: process.env.NODE_ENV as EventContext['env'] ?? 'development'
    },
    data,
    notification: {
      channels,
      targets
    }
  };
}
```

## Example

```typescript
// 사용 예시
import { createEvent } from './utils/event-factory';
import type { JobFailedData } from './types/events/job.event';

const event = createEvent<JobFailedData>({
  type: 'job.failed',
  service: 'scheduler',
  severity: 'error',
  data: {
    jobId: 'job-123',
    jobName: 'daily-report',
    error: 'Connection timeout'
  },
  channels: ['slack'],
  targets: ['#_협업']
});

// ms-notifier로 전송
await fetch('http://ms-notifier/api/events', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify(event)
});
```

## Reference

- [이벤트 봉투 표준](../../semo-core/_shared/microservice-conventions.md)
