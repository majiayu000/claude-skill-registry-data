---
name: build-course
description: Build a complete online course platform with video hosting, progress tracking, quizzes, and payments. Use when Rick says build a course, create a learning platform, or make educational content.
---

# Build Online Course Platform

**IMPORTANT**: Before scaffolding, see @project-scaffolding.md for the complete master project template.
All new projects MUST use the full monorepo structure with all critical config files.

## Stack
- Frontend: Next.js 15 + shadcn/ui + Framer Motion
- Auth: Supabase Auth
- Database: Supabase PostgreSQL
- Video: Mux or Cloudflare Stream
- Payments: Stripe (one-time + subscription)
- Deploy: Cloudflare Pages

## Required Features
1. Course catalog with categories and search
2. Video player with progress tracking
3. Module/lesson structure with sequential unlocking
4. Quiz system with multiple question types
5. Certificate generation on completion
6. Student dashboard with progress overview
7. Admin panel for content management
8. Stripe checkout for course purchases
9. Email notifications (enrollment, progress, completion)
10. Mobile-responsive design

## Database Schema
- users, courses, modules, lessons, enrollments
- progress (user_id, lesson_id, completed_at, watch_time)
- quizzes, quiz_questions, quiz_attempts
- certificates (auto-generated PDF)

## After Building
1. Run pnpm build to verify
2. Deploy to Cloudflare Pages
3. Push to GitHub with branding
