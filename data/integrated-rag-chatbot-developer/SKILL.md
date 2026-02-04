---
name: "integrated-rag-chatbot-developer"
description: "Design, generate, and fully deploy a stylish, production-ready Retrieval-Augmented Generation (RAG) chatbot embedded directly into any website/project. Uses OpenAI ChatKit widget + Cohere embeddings + Qdrant Cloud + Neon Serverless Postgres + FastAPI backend. Supports selected-text questioning and full conversation history."
version: "1.0.0"
---

# Integrated RAG Chatbot Developer Skill

## When to Use This Skill

- User wants to "add an AI chatbot to my website"
- User asks to "build a RAG chatbot", "embed a smart assistant", or "make the site answer questions about its own content"
- User needs a chatbot that can answer based on **selected text** on the page
- User wants a complete, deployable solution with backend, vector DB, history, and beautiful UI

## How This Skill Works

1. Generate full project structure with FastAPI backend
2. Create secure `.env` files with all required keys
3. Set up Qdrant Cloud collection + Cohere embeddings pipeline
4. Implement Neon Postgres for conversation history & metadata
5. Generate OpenAI ChatKit widget with custom styling and selected-text trigger
6. Add ingestion script to index all site content (Markdown, HTML, PDFs)
7. Enable "Ask about selected text" feature via context injection
8. Provide one-click deployment instructions (Vercel / Render / Railway)

## Full Deliverables Generated

- Complete project folder structure
- `backend/` – FastAPI server with RAG routes
- `ingest.py` – Script to load and chunk your website/content
- `chatkit-widget/` – Custom styled OpenAI ChatKit embed code
- `.env.example` and deployment-ready `.env`
- Stylish floating widget with dark/light mode, typing indicators, copy buttons

## Output Format

```text
Project: RAG-Chatbot-YourSiteName
├── backend/
│   ├── main.py              ← FastAPI server
│   ├── rag.py                ← Cohere + Qdrant retrieval
│   ├── database.py           ← Neon Postgres history
│   └── models.py
├── ingest.py                 ← Run once to index your site
├── chatkit-widget/
│   └── widget.html           ← Copy-paste into <head>
├── .env                      ← Auto-generated with your keys
└── README.md                 ← Full deployment guide
```

### Example Output (Delivered Instantly)

**Input**:  
"Build a RAG chatbot for my personal portfolio at https://john.dev that uses my blog posts and projects page. Make it beautiful, support selected text, and store chat history."

**What You Get Immediately**:

1. `.env` (ready for your keys)
```env
# === YOUR SECRETS (User fills these) ===
OPENAI_API_KEY=sk-...
COHERE_API_KEY=...
QDRANT_URL=https://your-cluster.qdrant.cloud:6333
QDRANT_API_KEY=...
NEON_DATABASE_URL=postgresql://user:pass@ep-...pooler.neon.tech/db?sslmode=require

# === AUTO-FILLED BY SKILL ===
CHATKIT_BOT_ID=bot_1234567890
PROJECT_NAME=john.dev Assistant
```

2. Beautiful ChatKit Widget (paste into your site)
```html
<script src="https://chatkit.openai.com/widget.js"></script>
<div id="chatkit-widget"></div>
<script>
  ChatKit.init({
    botId: "YOUR_BOT_ID",
    title: "Ask me anything about this site",
    subtitle: "I can read selected text!",
    primaryColor: "#6366f1",
    position: "bottom-right",
    welcomeMessage: "Hi! Highlight any text and ask me about it.",
    selectedTextSupport: true,
    apiBase: "https://your-backend.onrender.com"
  });
</script>
```

3. FastAPI Backend Snippet (main.py)
```python
from fastapi import FastAPI, Request
from rag import retrieve_context, generate_response
from database import save_conversation, get_history

app = FastAPI()

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    user_message = data["message"]
    selected_text = data.get("selectedText", "")
    history = get_history(data["sessionId"])

    context = retrieve_context(user_message + selected_text)
    response = generate_response(user_message, context, history)
    
    save_conversation(data["sessionId"], user_message, response)
    return {"response": response}
```

4. One-Command Ingestion
```bash
python ingest.py --url https://john.dev --recursive
→ Successfully indexed 42 pages into Qdrant with Cohere embeddings
```

5. Live Features Included
- Answers only from your site content (no hallucinations)
- Highlight any text → "Ask about this" button appears
- Full conversation history per user (Neon Postgres)
- Mobile-responsive, animated, professional design
- GDPR-safe session handling

**Final Message from Skill**:
> Your RAG chatbot is 100% ready!  
> Deploy backend → Run ingestion → Paste widget → Done!  
> Users can now talk to your website like it’s alive.
