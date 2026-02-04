---
name: learning-guide
description: This skill should be used when a user asks to learn a specific skill or knowledge area using the pattern '帮我学习一下xx技能/知识'. The skill provides a comprehensive 9-step learning journey including concept discovery, practical applications, code examples, resource recommendations, community tracking, and related topic suggestions. It covers the complete learning cycle from foundational understanding to advanced community engagement.
---

# Learning Guide

## Overview

This skill provides a comprehensive learning path for any technical or non-technical topic. When triggered by user requests like "帮我学习一下Python" or "帮我学习一下机器学习", it executes a structured 9-step learning journey that covers foundational concepts, practical applications, community resources, and advanced learning pathways.

## When to Use This Skill

Use this skill when a user explicitly asks to learn something using patterns such as:
- "帮我学习一下xx技能/知识"
- "我想学习xx"
- "教我学习xx"
- "介绍一下如何学习xx"

This skill is particularly designed for comprehensive learning requests, not quick reference questions.

## 9-Step Learning Journey

When executing a learning request, follow this structured flow to provide comprehensive coverage of the topic:

### Step 1: Define the Knowledge Domain
Search for and provide a clear, comprehensive definition of the topic. Include key characteristics, core concepts, and fundamental principles.

**Tools to use:**
- WebSearch: Use targeted search queries like "What is [topic]", "[topic] definition", "[topic] explained"

**Expected output:**
- Clear definition in 2-3 paragraphs
- Key characteristics and core concepts
- Historical context or origin if relevant

### Step 2: Analyze Application Domains
Identify where this knowledge is commonly applied, its place in the field hierarchy, and related complementary knowledge.

**Tools to use:**
- WebSearch: "[topic] use cases", "[topic] applications", "when to use [topic]"

**Expected output:**
- Primary application domains (3-5 areas)
- Hierarchy position in the field
- Complementary technologies or knowledge areas that work well together

### Step 3: Practical Usage Examples
Provide concrete examples showing how the knowledge is used in real-world scenarios including code examples, workflows, or case studies.

**Tools to use:**
- WebSearch: "[topic] tutorial", "[topic] examples", "[topic] getting started"

**Expected output:**
- 2-3 practical examples
- Code snippets or workflow diagrams where applicable
- Step-by-step demonstrations for complex concepts

### Step 4: Discover GitHub Repositories
Find and summarize up to 3 popular GitHub repositories related to the topic.

**Tools to use:**
- WebSearch: "[topic] GitHub", "best [topic] repositories", "[topic] GitHub trending"

**Expected output:**
- Repository names with links
- Brief description of each (2-3 sentences)
- Star counts and last update information if available
- Key features and use cases for each repo

### Step 5: Recommend Core Books
Identify and recommend essential books for mastering the topic.

**Tools to use:**
- WebSearch: "best [topic] books", "[topic] reading list", "[topic] must-read books"

**Expected output:**
- 3-5 book recommendations
- Author names and brief descriptions
- Target audience (beginner, intermediate, advanced)
- Why each book is recommended

### Step 6: Identify Field Experts
Find prominent experts in the field and provide their contact information and resources.

**Tools to use:**
- WebSearch: "[topic] experts", "[topic] influencers", "[topic] thought leaders"

**Expected output:**
- 3-5 expert names
- Brief credentials and contributions
- Blog URLs
- Twitter/Social media links
- GitHub profiles if relevant

### Step 7: Track HackerNews Discussions
Search HackerNews for recent discussions about the topic to show current trends and community sentiment.

**Tools to use:**
- WebSearch: "site:news.ycombinator.com [topic]", "[topic] hacker news"

**Expected output:**
- 2-3 recent relevant discussions
- Brief summary of each discussion
- Community sentiment and key insights

### Step 8: Identify Community Resources
Find where to track the latest developments in this knowledge area including specialized news sites, forums, and communities.

**Tools to use:**
- WebSearch: "[topic] community", "[topic] forum", "[topic] news", "[topic] latest developments"

**Expected output:**
- 3-5 community resources
- Brief description of each resource
- Update frequency and content focus

### Step 9: Suggest Related Topics
Recommend closely related knowledge areas for expanded learning.

**Tools to use:**
- WebSearch: "[topic] related technologies", "learning path [topic]", "what to learn after [topic]"

**Expected output:**
- 3-5 related topics
- How each relates to the main topic
- Learning sequence recommendations
- Brief explanation of why they're relevant
