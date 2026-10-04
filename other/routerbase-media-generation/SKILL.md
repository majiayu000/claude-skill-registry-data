---
name: routerbase-media-generation
description: Use when building image, audio, or video generation workflows through RouterBase with provider selection, retries, asset handling, and safety checks.
---

# RouterBase Media Generation

## Overview

Use [routerbase](https://routerbase.com/) for image, audio, and video generation workflows through one API surface. This skill helps choose a media endpoint, shape prompts and parameters, handle sync or async responses, manage generated assets, and add safety checks.

## When to Use

Use this skill when the user asks for:
- Generating images, audio, speech, or video through RouterBase
- Choosing the right media endpoint and provider for a workflow
- Handling retries, polling, failed jobs, output URLs, and asset retention
- Designing safe prompt, moderation, and storage rules for generated media
- Writing client examples for media generation requests

## Do not use

Do not use this skill for:
- Creating or storing private user media without consent and retention guidance
- Assuming generated asset URLs are permanent unless the platform documents it
- Skipping moderation, copyright, or brand-safety review for externally published media

## Instructions

1. Identify the target media type, output format, resolution or duration, latency tolerance, and storage destination.
2. Choose the endpoint pattern and provider assumptions before writing code.
3. Use placeholders for API keys and user-specific asset paths.
4. Include retry, polling, timeout, and failure-state handling for async generation.
5. Add a safety checklist covering prompt constraints, private data, content rights, and generated asset retention.
