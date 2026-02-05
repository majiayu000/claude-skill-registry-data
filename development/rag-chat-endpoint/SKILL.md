---
name: RAG Chat Endpoint
description: Implement the /chat endpoint that performs agent-based RAG reasoning with proper input validation and response formatting.
---

# RAG Chat Endpoint

## Instructions

1. Create the chat endpoint in app/routers/chat.py:
   - Define POST /chat endpoint using FastAPI
   - Accept request body with schema: { message: string, selection?: string }
   - Implement proper input validation using Pydantic models
   - Include rate limiting and error handling

2. Integrate with the RAG agent system:
   - Call the reasoning agent via Agent SDK
   - Pass user message and any selection context
   - Handle tool calls from the agent (retrieval tools)
   - Process final response and citations

3. Ensure proper response formatting:
   - Return structured response with answer and sources
   - Include proper error responses with appropriate HTTP status codes
   - Add streaming support if needed for better UX

4. Follow Context7 MCP standards:
   - Enforce strict input/output schemas
   - Only use retrieved context (no hallucinations)
   - Follow proper error handling patterns
   - Include logging for debugging

5. Add proper authentication and authorization if required:
   - Check for valid API keys or session tokens
   - Implement rate limiting to prevent abuse

## Examples

Input: "Create RAG chat endpoint"
Output: Creates chat.py router with:
```python
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.services.agent.client import call_gemini_agent
from app.services.tools.retrieval_tools import retrieval_tools

router = APIRouter(prefix="/chat", tags=["chat"])

class ChatRequest(BaseModel):
    message: str
    selection: Optional[str] = None

class ChatResponse(BaseModel):
    answer: str
    sources: list

@router.post("/", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    try:
        # Prepare messages for the agent
        messages = [
            {"role": "system", "content": "You are a helpful assistant for Physical AI & Humanoid Robotics textbook."},
            {"role": "user", "content": request.message}
        ]

        if request.selection:
            messages.append({"role": "user", "content": f"Context: {request.selection}"})

        # Call the agent with retrieval tools
        response = call_gemini_agent(messages, tools=retrieval_tools)

        return ChatResponse(
            answer=response.choices[0].message.content,
            sources=[]  # Populate with actual sources from tool calls
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```