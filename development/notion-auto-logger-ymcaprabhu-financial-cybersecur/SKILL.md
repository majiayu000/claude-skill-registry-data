---
name: notion-auto-logger
description: Automatically logs every user prompt and AI output to datewise Notion pages. Use this skill to create a comprehensive archive of all AI interactions, track research progress, maintain conversation history, and build a searchable knowledge base. The skill creates one JSON file per day with all interactions and can export them to Notion in a structured format.
---

# Notion Auto Logger

## Overview

This skill enables automatic logging of every prompt and output interaction to create a comprehensive, searchable archive of AI conversations. It generates daily JSON files with structured data and can export formatted content to Notion pages for long-term storage and reference.

## Quick Start

To start logging immediately:

1. **Automatic Logging**: The skill automatically detects and logs every interaction
2. **Daily Files**: Creates one JSON file per day in `~/notion_logs/`
3. **Notion Export**: Export daily logs to Notion pages with one command

## Core Capabilities

### 1. Automatic Interaction Logging
- **Real-time capture**: Logs every prompt and output as they occur
- **Structured data**: Captures timestamps, categories, session IDs, and model info
- **Smart categorization**: Automatically classifies interactions (research, coding, analysis, etc.)
- **Content management**: Handles long content with intelligent truncation

### 2. Daily Organization
- **Datewise files**: Creates `prompts_outputs_YYYY-MM-DD.json` for each day
- **Metadata tracking**: Records total interactions, categories, and statistics
- **Incremental updates**: Appends new interactions to existing daily files

### 3. Notion Integration
- **Export to Notion**: Converts daily logs to Notion-compatible format
- **Structured content**: Generates properly formatted headings, lists, and paragraphs
- **Batch processing**: Export entire days or specific date ranges

### 4. Analysis & Statistics
- **Daily summaries**: Track interaction counts, categories, and content metrics
- **Category breakdown**: Monitor types of interactions (research vs coding vs general)
- **Content metrics**: Track character counts and interaction patterns

## Usage Workflow

### Step 1: Enable Automatic Logging
The skill automatically begins logging when loaded. Use configuration file to customize:
- Enable/disable specific features
- Set content truncation limits
- Define categories and keywords
- Configure export preferences

### Step 2: Monitor Daily Activity
Daily logs are automatically created in `~/notion_logs/` with structure:
```json
{
  "date": "2025-10-27",
  "created_at": "2025-10-27T12:00:00Z",
  "total_interactions": 15,
  "interactions": [
    {
      "timestamp": "2025-10-27T12:30:00Z",
      "session_id": "session_123",
      "model": "claude",
      "category": "research",
      "prompt": "Analyze quantum computing trends...",
      "output": "Based on current research...",
      "prompt_length": 45,
      "output_length": 1250
    }
  ]
}
```

### Step 3: Export to Notion
When ready to archive in Notion:
1. Run export command for specific date
2. Copy generated content to Notion page
3. Maintain searchable archive in your workspace

## Configuration

### Basic Settings (`notion_config.json`)
- **Auto-logging**: Enable/disable automatic capture
- **Content limits**: Set maximum character limits for storage
- **Categories**: Define custom categories with keywords and icons
- **Export preferences**: Choose markdown or plain text formats

### Advanced Options
- **Session tracking**: Group related interactions
- **Model identification**: Track which AI model was used
- **Backup strategies**: Multiple storage locations
- **Privacy controls**: Sensitive content filtering

## Resources

### scripts/
**notion_auto_logger.py** - Core logging functionality with automatic categorization, daily file management, and JSON storage. Handles real-time prompt/output capture with metadata tracking.

**notion_integration.py** - Notion-specific export functionality that converts daily JSON logs into Notion-compatible block format for seamless integration with your workspace.

### Configuration Files
**notion_config.json** - Complete configuration with categories, automation settings, content limits, and export preferences. Customizable categories include research, coding, analysis, cybersecurity, and general interactions.

### Usage Commands
```bash
# Log an interaction manually
python scripts/notion_auto_logger.py log "your prompt" "ai response"

# Get daily statistics
python scripts/notion_auto_logger.py stats

# Export to Notion format
python scripts/notion_auto_logger.py export

# Generate Notion blocks
python scripts/notion_integration.py
```

## Automation Integration

This skill can be integrated with automated workflows:
- **Real-time logging**: Automatically captures every conversation
- **Scheduled exports**: Daily/weekly Notion page creation
- **Statistical analysis**: Track interaction patterns over time
- **Content backup**: Secure storage of important conversations
