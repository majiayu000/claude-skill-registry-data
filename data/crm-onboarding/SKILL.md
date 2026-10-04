---
name: crm-onboarding
description: >
  Build a lead capture + email nurture CRM pipeline — public onboarding form,
  CRM state machine (NEW→QUALIFIED→PROPOSAL→WON/LOST), 5-email drip sequence via Resend,
  Slack webhook handoff on qualification, and kanban dashboard. Triggers when user asks
  to build a CRM, lead capture, onboarding flow, lead nurture, or lead pipeline.
---

# CRM Onboarding Agent

## Schema

```typescript
// prisma/schema.prisma
model Lead {
  id          String     @id @default(cuid())
  name        String
  email       String     @unique
  company     String?
  useCase     String?
  budget      String?    // 'under_1k' | '1k_5k' | '5k_plus'
  source      String?
  status      LeadStatus @default(NEW)
  stageDays   Int        @default(0)
  lastEmailAt DateTime?
  nextEmailAt DateTime?
  qualifiedAt DateTime?
  proposalAt DateTime?
  wonAt       DateTime?
  lostAt      DateTime?
  notes       String?
  emails      EmailEvent[]
  createdAt   DateTime  @default(now())
  updatedAt   DateTime  @updatedAt
}

enum LeadStatus { NEW CONTACTED QUALIFIED PROPOSAL NEGOTIATION WON LOST }

model EmailEvent {
  id       String  @id @default(cuid())
  leadId   String
  lead     Lead    @relation(fields: [leadId], references: [id])
  event    String
  sentAt   DateTime @default(now())
  openedAt DateTime?
  clickedAt DateTime?
  bounced  Boolean @default(false)
}
```

## State Machine

```typescript
// lib/crm-state-machine.ts
type Transition = {
  from: LeadStatus[];
  to: LeadStatus;
  trigger: 'manual' | 'auto' | 'email_open' | 'link_click';
  reason?: string;
};

const TRANSITIONS: Transition[] = [
  { from: ['NEW'], to: 'CONTACTED', trigger: 'manual' },
  { from: ['CONTACTED'], to: 'QUALIFIED', trigger: 'manual', reason: 'Budget and timeline confirmed' },
  { from: ['QUALIFIED'], to: 'PROPOSAL', trigger: 'manual' },
  { from: ['PROPOSAL'], to: 'NEGOTIATION', trigger: 'manual' },
  { from: ['PROPOSAL', 'NEGOTIATION'], to: 'WON', trigger: 'manual' },
  { from: ['NEW', 'CONTACTED', 'QUALIFIED', 'PROPOSAL', 'NEGOTIATION'], to: 'LOST', trigger: 'manual' },
];

export function canTransition(from: LeadStatus, to: LeadStatus): boolean {
  return TRANSITIONS.some(t => t.from.includes(from) && t.to === to);
}

export async function transitionLead(leadId: string, to: LeadStatus, reason?: string) {
  const lead = await prisma.lead.findUnique({ where: { id: leadId } });
  if (!canTransition(lead.status, to)) throw new Error(`Cannot transition ${lead.status} → ${to}`);

  return prisma.lead.update({
    where: { id: leadId },
    data: {
      status: to,
      stageDays: 0,
      ...(to === 'QUALIFIED' ? { qualifiedAt: new Date() } : {}),
      ...(to === 'PROPOSAL' ? { proposalAt: new Date() } : {}),
      ...(to === 'WON' ? { wonAt: new Date() } : {}),
      ...(to === 'LOST' ? { lostAt: new Date() } : {}),
      notes: reason ? `${lead.notes}\n${new Date().toISOString()}: ${reason}` : lead.notes,
    }
  });
}
```

## Resend 5-Email Drip

```typescript
// lib/resend-sequence.ts
const DRIP_SEQUENCE = [
  {
    day: 0,
    event: 'welcome',
    subject: 'Welcome! Let me introduce myself',
    template: 'emails/welcome.tsx',
    condition: () => true,
  },
  {
    day: 2,
    event: 'value_prop',
    subject: 'How [company] solves [useCase] in days, not months',
    template: 'emails/value-prop.tsx',
    condition: (lead) => lead.status === 'CONTACTED',
  },
  {
    day: 5,
    event: 'case_study',
    subject: '[Similar Company] cut costs by 40% — here\'s how',
    template: 'emails/case-study.tsx',
    condition: (lead) => ['CONTACTED', 'QUALIFIED'].includes(lead.status),
  },
  {
    day: 10,
    event: 'demo_cta',
    subject: '15-min demo — see it live this week',
    template: 'emails/demo-cta.tsx',
    condition: (lead) => ['QUALIFIED', 'PROPOSAL'].includes(lead.status),
  },
  {
    day: 14,
    event: 'urgency',
    subject: 'Last chance — slots filling up for [month]',
    template: 'emails/urgency-final.tsx',
    condition: (lead) => lead.status !== 'WON' && lead.status !== 'LOST',
  },
];

// Cron job (every hour):
// 1. Find leads where nextEmailAt <= now AND status != WON && != LOST
// 2. Send email via Resend
// 3. Update lastEmailAt, set nextEmailAt to day+N
// 4. Track opens/clicks via Resend webhook
```

## Slack Handoff

```typescript
// lib/slack-handoff.ts
export async function notifyQualifiedLead(lead: Lead) {
  const blocks = [
    { type: 'header', text: { type: 'plain_text', text: 'New Qualified Lead' }},
    { type: 'section', fields: [
      { type: 'mrkdwn', text: `*Name:*\n${lead.name}` },
      { type: 'mrkdwn', text: `*Email:*\n${lead.email}` },
      { type: 'mrkdwn', text: `*Company:*\n${lead.company ?? 'N/A'}` },
      { type: 'mrkdwn', text: `*Use case:*\n${lead.useCase ?? 'N/A'}` },
      { type: 'mrkdwn', text: `*Budget:*\n${lead.budget ?? 'N/A'}` },
    ]},
    { type: 'actions', elements: [
      { type: 'button', text: { type: 'plain_text', text: 'View CRM' }, url: `https://crm.example.com/leads/${lead.id}` }
    ]},
  ];

  await fetch(process.env.SLACK_WEBHOOK_URL!, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ blocks }),
  });
}
```

## Kanban Dashboard

```tsx
// pages/admin/crm/index.tsx
const STAGES: LeadStatus[] = ['NEW', 'CONTACTED', 'QUALIFIED', 'PROPOSAL', 'NEGOTIATION'];

export function CRMKanban() {
  const { data: leadsByStatus } = trpc.lead.byStatus.useQuery();

  return (
    <div className="flex gap-4 overflow-x-auto p-4">
      {STAGES.map(stage => (
        <div key={stage} className="min-w-64 flex-1">
          <div className="bg-gray-100 rounded-t p-3 font-bold text-sm">{stage}</div>
          <div className="space-y-2 p-2 min-h-96">
            {leadsByStatus[stage]?.map(lead => (
              <LeadCard key={lead.id} lead={lead} />
            ))}
          </div>
        </div>
      ))}
    </div>
  );
}
```
