---
name: php-laravel
description: "Laravel 11 architecture, Eloquent query optimization, Form Requests, Queues, and Service Container bindings."
---

# Laravel Architecture Protocol

Build modern PHP web applications with Laravel.

---

## 1. Eloquent Eager Loading

1. Always eager load relationships using `with(['relation'])`.
2. Enable `Model::preventLazyLoading(!app()->isProduction())` to catch N+1 queries during development.

---

## 2. Validation & Form Requests

Validate all HTTP inputs in dedicated `FormRequest` classes, never inside controller closures.
