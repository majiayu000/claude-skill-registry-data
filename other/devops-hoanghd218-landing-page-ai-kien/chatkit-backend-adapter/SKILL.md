---
name: ChatKit Backend Adapter
description: Modify OpenAI ChatKit starter to use FastAPI backend instead of OpenAI API, including citation support and error handling.
---

# ChatKit Backend Adapter

## Instructions

1. Replace OpenAI ChatKit client with custom backend calls:
   - Modify API calls to fetch from /chat endpoint instead of OpenAI
   - Update authentication and headers
   - Handle response format differences
   - Maintain ChatKit component compatibility

2. Add citation support to UI:
   - Display source information from backend
   - Format citations properly in messages
   - Link citations to original sources
   - Handle citation styling consistently

3. Implement proper error and loading states:
   - Handle backend API errors gracefully
   - Show loading indicators during requests
   - Display error messages to users
   - Implement retry functionality

4. Maintain ChatKit internal states:
   - Preserve existing component architecture
   - Update state management for new backend
   - Handle message history properly
   - Maintain conversation flow

5. Follow Context7 MCP documentation:
   - Do not call OpenAI API for inference
   - Follow deterministic UI patch patterns
   - Include proper error handling
   - Maintain ChatKit component compatibility

## Examples

Input: "Adapt ChatKit to use custom backend"
Output: Patches ChatKit frontend files to replace OpenAI API calls with custom backend endpoints.