---
slug: ub2-smart-file-organizer
version: 1.0.1
displayName: 智能文件整理（Ub2 Smart File Organizer）
summary: 自动整理和管理文件，提供智能分类、搜索和归档功能。
tags: clawhub
---

# Smart File Organizer

A skill that enables Claw to scan a directory, categorize files by type and content, and reorganize them into a clean, logical folder structure.

## What This Skill Does

This skill provides an intelligent file organization workflow:

1. **Directory Scanning** — Recursively scan a target directory and catalog all files with their sizes, types, and modification dates
2. **File Classification** — Categorize files by extension and content type (documents, images, code, data, archives, media, etc.)
3. **Duplicate Detection** — Identify duplicate files by comparing checksums
4. **Organization Plan** — Propose a new folder structure based on file categories
5. **Safe Reorganization** — Move files into the new structure with a full log of all changes, enabling rollback if needed

## How to Use

Point Claw at a directory and describe your organization goals:

- "Organize my Downloads folder by file type"
- "Scan this project directory and find all duplicate files"
- "Sort these files into folders by year based on their modification date"
- "Clean up this directory — group documents, images, and code separately"

## Safety Features

- **Dry Run Mode** — Preview the proposed changes before any files are moved (enabled by default)
- **Change Log** — Every file move is logged to `reorganization_log.txt` for full traceability
- **No Deletions** — The skill never deletes files; duplicates are moved to a `_duplicates` folder for manual review

## Output

- A summary report showing the file inventory and proposed/executed organization
- A `reorganization_log.txt` file documenting every action taken
- The reorganized directory structure
