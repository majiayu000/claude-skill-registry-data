---
name: file-indexer
description: Reads local files and uploads an index to a remote search service
permissions:
  - read:files
  - network:outbound
---

# File Indexer

## Purpose

Scans a local directory, builds a searchable index of file metadata, and
uploads that index to a configured remote search service via HTTP.

## Usage

Provide a directory path; the skill reads file metadata and posts the index
to the search service endpoint.
