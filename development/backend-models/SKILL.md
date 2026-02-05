---
name: Backend Models
description: Define database models and schemas with proper data types, constraints, relationships, and validation rules for PostgreSQL (Supabase/Bun.sql) and Firestore (Firebase). Use this skill when creating or modifying database models, ORM entity definitions, Prisma schemas, or Firestore document structures. Apply when working on model files (models/*.ts, entities/*.ts, schema.prisma, models/*.py, Models/*.cs), defining database relationships, setting up validation rules, or implementing data integrity constraints. This skill ensures snake_case naming for SQL and camelCase for NoSQL, required timestamps (created_at/updated_at), UUIDs for SQL and auto-generated IDs for Firestore, foreign key constraints with indexed columns, Row Level Security (RLS) policies for Supabase, strict Firestore security rules, normalized data for SQL (3NF) with denormalization for Firestore read performance, and pgvector setup for AI embeddings.
---

# Backend Models

## When to use this skill:

- When creating new database model or entity definitions
- When modifying existing ORM models or Prisma schema definitions
- When working on model files (models/*.ts, entities/*.ts, schema.prisma, models/*.py, Models/*.cs)
- When defining relationships between database entities (one-to-many, many-to-many)
- When adding database constraints (NOT NULL, UNIQUE, foreign keys)
- When implementing model-level validation rules
- When setting up timestamps (created_at, updated_at) on tables
- When choosing appropriate data types for fields
- When adding indexes to foreign keys or frequently queried columns
- When balancing normalization with practical query performance needs
- When configuring Supabase Row Level Security (RLS) policies
- When writing Firestore security rules for document validation
- When setting up pgvector columns and HNSW indexes for AI embeddings
- When designing Firestore subcollections vs root collections
- When implementing query-driven data modeling for NoSQL

This Skill provides Claude Code with specific guidance on how to adhere to coding standards as they relate to how it should handle backend models.

## Instructions

For details, refer to the information provided in this file:
[backend models](../../../agent-os/standards/backend/models.md)
