---
name: ruby-on-rails
description: "Ruby on Rails 7, Active Record query tuning, Turbo/Stimulus, and background processing with Sidekiq."
---

# Ruby on Rails Protocol

Write idiomatic, scalable Rails applications.

---

## 1. Active Record Optimization

1. Use `includes`, `preload`, or `eager_load` to eliminate N+1 database queries.
2. Avoid loading full models for simple counts or existence checks (`exists?`, `pluck`).

---

## 2. Background Jobs

Offload emails, image processing, and external API requests to background jobs (Sidekiq) with exponential retries.
