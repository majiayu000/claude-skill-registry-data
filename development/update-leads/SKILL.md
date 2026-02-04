---
name: update-leads
description: Updates the list of job leads and prioritizes actions. Use for weekly lead review.
---

# Update Job Leads

<workflow>

## Step 1: Collect & Extract

1. Check sources (LinkedIn, Company sites, Referrals).
2. Extract: Role, Company, Location, Salary, Deadline.

## Step 2: Evaluate & Prioritize

1. Score fit (1-10) against `CANDIDATE-PROFILE.md`.
2. Assign Priority:
   - **High:** Direct fit, high value.
   - **Medium:** Good fit.
   - **Low:** Backup.

## Step 3: Update File

1. Load `/03-Job-Market-Research/Active-Leads/Current-Leads.md`.
2. Add new leads using the template in `references/templates.md`.
3. Archive stale leads.

## Step 4: Action Planning

1. Create a weekly plan (Research -> Apply -> Follow-up).
2. Set goals for application volume.

## Step 5: Integration

1. Create dossiers for High Priority leads.
2. Sync deadlines to calendar.

</workflow>
