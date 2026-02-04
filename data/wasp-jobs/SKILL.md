---
name: wasp-jobs
description: Background jobs with PgBoss for Wasp applications. Use when implementing async tasks, scheduled jobs, email queues, or background processing. Requires PostgreSQL database.
triggers:
  [
    "background job",
    "scheduled task",
    "cron",
    "job",
    "email queue",
    "async task",
    "PgBoss",
  ]
version: 1.0
last_updated: 2025-10-18
allowed_tools: [Edit, Bash, Read]
---

# Wasp Background Jobs Skill

## Quick Reference

**When to use this skill:**

- Sending emails asynchronously
- Processing data in background
- Scheduled/recurring tasks
- Long-running operations
- Queue-based processing

## Critical Requirements

**MUST use PostgreSQL** - PgBoss requires PostgreSQL (SQLite not supported)

```prisma
// schema.prisma
datasource db {
  provider = "postgresql"  // ✅ Required for jobs
  url      = env("DATABASE_URL")
}
```

## Complete Job Setup Workflow

### 1. Define Job in main.wasp

```wasp
job emailSender {
  executor: PgBoss,  // Requires PostgreSQL
  perform: {
    fn: import { sendEmail } from "@src/jobs/emailSender.js"
  },
  entities: [User, EmailQueue]  // Entities needed in job
}
```

**Job options:**

```wasp
job myJob {
  executor: PgBoss,
  perform: {
    fn: import { myJobFunction } from "@src/jobs/myJob.js"
  },
  entities: [User, Task],
  schedule: {
    cron: "0 0 * * *",  // Daily at midnight
    args: {=json { "foo": "bar" } json=}  // Optional default args
  }
}
```

### 2. Implement Job Function

**File:** `src/jobs/emailSender.js`

```typescript
import type { EmailSender } from "wasp/server/jobs";

type EmailArgs = {
  to: string;
  subject: string;
  body: string;
};

export const sendEmail: EmailSender<EmailArgs> = async (args, context) => {
  // Access entities via context
  const user = await context.entities.User.findUnique({
    where: { email: args.to },
  });

  if (!user) {
    console.error("User not found:", args.to);
    return { success: false, error: "User not found" };
  }

  try {
    // Send email logic here
    console.log(`Sending email to ${args.to}`);
    console.log(`Subject: ${args.subject}`);
    console.log(`Body: ${args.body}`);

    // Actual email sending would go here
    // await emailService.send(args)

    return { success: true };
  } catch (error) {
    console.error("Email send failed:", error);
    throw error; // PgBoss will retry
  }
};
```

### 3. Trigger Job Programmatically

**From an action:**

```typescript
import { emailSender } from "wasp/server/jobs";
import type { SendWelcomeEmail } from "wasp/server/operations";

export const sendWelcomeEmail: SendWelcomeEmail = async (args, context) => {
  if (!context.user) throw new HttpError(401);

  // Trigger job
  await emailSender.submit({
    to: context.user.email,
    subject: "Welcome!",
    body: "Thanks for signing up!",
  });

  return { message: "Email queued" };
};
```

**With delay:**

```typescript
// Send email in 1 hour
await emailSender.submit(
  { to: "user@example.com", subject: "Reminder", body: "Don't forget!" },
  { startAfter: new Date(Date.now() + 3600000) }, // 1 hour delay
);
```

**With retry configuration:**

```typescript
await emailSender.submit(emailArgs, {
  retryLimit: 5, // Retry up to 5 times
  retryDelay: 60, // 60 seconds between retries
  retryBackoff: true, // Exponential backoff
});
```

## Scheduling Patterns

### Cron-Based Scheduling

```wasp
job dailyReport {
  executor: PgBoss,
  perform: {
    fn: import { generateDailyReport } from "@src/jobs/reports.js"
  },
  schedule: {
    cron: "0 9 * * 1-5",  // 9 AM on weekdays
    args: {=json { "reportType": "daily" } json=}
  }
}
```

**Common cron patterns:**

- `"0 * * * *"` - Every hour
- `"0 0 * * *"` - Daily at midnight
- `"0 9 * * 1-5"` - 9 AM on weekdays
- `"0 0 1 * *"` - First day of month
- `"*/15 * * * *"` - Every 15 minutes

### Programmatic Scheduling

```typescript
import { myJob } from "wasp/server/jobs";

// Schedule one-time job
await myJob.submit(args, {
  startAfter: new Date("2025-12-01T10:00:00Z"),
});

// Schedule recurring job (every 6 hours)
await myJob.submit(args, {
  retryLimit: 3,
  retryDelay: 3600, // 1 hour retry delay
  expireInHours: 24, // Job expires after 24 hours
});
```

## Job Patterns

### Email Queue Pattern

```typescript
// Queue email for sending
export const queueEmail = async (args, context) => {
  if (!context.user) throw new HttpError(401);

  // Create email queue record
  const emailRecord = await context.entities.EmailQueue.create({
    data: {
      to: args.to,
      subject: args.subject,
      body: args.body,
      status: "PENDING",
    },
  });

  // Trigger job
  await emailSender.submit({
    emailId: emailRecord.id,
  });

  return emailRecord;
};

// Job processes queued email
export const emailSender = async (args, context) => {
  const email = await context.entities.EmailQueue.findUnique({
    where: { id: args.emailId },
  });

  if (!email) return { success: false };

  try {
    // Send email
    await sendEmailViaService(email);

    // Update status
    await context.entities.EmailQueue.update({
      where: { id: args.emailId },
      data: { status: "SENT", sentAt: new Date() },
    });

    return { success: true };
  } catch (error) {
    // Update status to failed
    await context.entities.EmailQueue.update({
      where: { id: args.emailId },
      data: { status: "FAILED", error: error.message },
    });
    throw error;
  }
};
```

### Batch Processing Pattern

```typescript
job processBatchUsers {
  executor: PgBoss,
  perform: {
    fn: import { processBatch } from "@src/jobs/batchProcessor.js"
  },
  entities: [User],
  schedule: {
    cron: "0 2 * * *"  // 2 AM daily
  }
}

export const processBatch = async (args, context) => {
  const batchSize = 100
  let offset = 0
  let processedCount = 0

  while (true) {
    const users = await context.entities.User.findMany({
      skip: offset,
      take: batchSize,
      where: { needsProcessing: true }
    })

    if (users.length === 0) break

    for (const user of users) {
      await processUser(user, context)
      processedCount++
    }

    offset += batchSize

    // Log progress
    console.log(`Processed ${processedCount} users`)
  }

  return { processedCount }
}
```

## Error Handling

### Job-Level Error Handling

```typescript
export const myJob = async (args, context) => {
  try {
    // Job logic
    await doWork(args, context);
    return { success: true };
  } catch (error) {
    console.error("Job failed:", error);

    // Log to database
    await context.entities.JobLog.create({
      data: {
        jobName: "myJob",
        args: JSON.stringify(args),
        error: error.message,
        stack: error.stack,
      },
    });

    // Rethrow to trigger PgBoss retry
    throw error;
  }
};
```

### Dead Letter Queue

```typescript
// Handle jobs that failed all retries
export const processDeadLetterQueue = async (args, context) => {
  // Find failed jobs
  const failedJobs = await context.entities.JobLog.findMany({
    where: {
      status: "FAILED",
      retries: { gte: 5 },
    },
  });

  // Alert admin or take remedial action
  for (const job of failedJobs) {
    await notifyAdmin({
      subject: "Job permanently failed",
      job: job.jobName,
      args: job.args,
      error: job.error,
    });
  }
};
```

## PostgreSQL Setup

### Local Development

```bash
# macOS
brew install postgresql
brew services start postgresql
createdb myapp_dev

# Linux
sudo apt-get install postgresql
sudo systemctl start postgresql
sudo -u postgres createdb myapp_dev
```

### .env.server

```bash
DATABASE_URL="postgresql://username:password@localhost:5432/myapp_dev"
```

### schema.prisma

```prisma
datasource db {
  provider = "postgresql"  // Required for PgBoss
  url      = env("DATABASE_URL")
}
```

## Common Job Errors

### Error: PgBoss requires PostgreSQL

**Cause:** Using SQLite as database provider

**Fix:**

```prisma
// Change in schema.prisma
datasource db {
  provider = "postgresql"  // Not "sqlite"
  url      = env("DATABASE_URL")
}
```

### Error: Job not defined

**Cause:** Forgot to restart wasp after adding job to main.wasp

**Fix:**

```bash
# Ctrl+C to stop, then safe-start (multi-worktree safe)
../scripts/safe-start.sh
```

### Error: Cannot submit job

**Cause:** Job not imported correctly

**Fix:**

```typescript
// ✅ CORRECT
import { myJob } from "wasp/server/jobs";

// ❌ WRONG
import { myJob } from "@wasp/jobs";
```

## Best Practices

✅ DO:

- Use jobs for long-running operations
- Handle errors and log failures
- Set appropriate retry limits
- Use PostgreSQL (required)
- Test jobs locally before scheduling
- Monitor job execution
- Implement dead letter queue

❌ NEVER:

- Use jobs for real-time operations
- Forget error handling
- Use SQLite (PgBoss requires PostgreSQL)
- Set infinite retries
- Skip job logging

## Quick Setup Checklist

- [ ] Switch to PostgreSQL (if using SQLite)
- [ ] Define job in main.wasp
- [ ] Implement job function
- [ ] Restart `../scripts/safe-start.sh` (multi-worktree safe)
- [ ] Test job submission
- [ ] Add error handling
- [ ] Set up monitoring/logging

## Critical Rules

**Database:** MUST use PostgreSQL (PgBoss requirement)
**Restart:** ALWAYS restart wasp after adding jobs to main.wasp
**Error handling:** ALWAYS handle errors in job functions
**Monitoring:** LOG job execution and failures

## References

- Wasp jobs docs: https://wasp.sh/docs/language/features#jobs
- PgBoss docs: https://github.com/timgit/pg-boss
