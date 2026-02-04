---
name: Book Ingestion
description: Generate the complete RAG ingestion script to crawl textbook from sitemap.xml, chunk content, embed using Gemini, and push to Qdrant following MCP documentation.
---

# Book Ingestion

## Instructions

1. Generate the complete RAG ingestion script at `scripts/ingest-book.py` that:
   - Fetches sitemap.xml from the Docusaurus textbook URL
   - Parses XML to extract all content page URLs
   - Crawls each page and extracts main content (strips nav/footer/sidebar)
   - Chunks content by sections, code blocks, paragraphs with 500-1000 token sizes
   - Extracts metadata (url, module, chapter, title, chunk_index)
   - Generates embeddings using Gemini via LangChain
   - Uploads vectors to Qdrant collection "book_chunks"

2. Sitemap crawling implementation:
   - Fetch sitemap.xml using requests
   - Parse XML with BeautifulSoup or xml.etree
   - Filter URLs to content pages only (exclude /tags/, /search/, etc.)
   - Implement rate limiting (1-2 requests/second)
   - Handle HTTP errors gracefully

3. HTML content extraction:
   - Use BeautifulSoup to parse HTML
   - Extract main article content (typically `<article>` or `<main>` tag)
   - Remove navigation, footer, sidebar, and script elements
   - Convert HTML to clean text while preserving code blocks
   - Extract page title from `<h1>` or `<title>` tag

4. Follow chunking best practices:
   - Preserve semantic boundaries (headings, paragraphs)
   - Maintain document hierarchy in metadata
   - Handle code blocks separately from text
   - Include overlap between chunks (50-100 tokens)
   - Target chunk size: 500-1000 tokens

5. Metadata schema for each chunk:
   ```python
   {
       "url": "https://nadeemsangrasi.github.io/humanoid-and-robotic-book/module-1-ros2/03-ros2-communication-patterns/",
       "module": "module-1-ros2",
       "chapter": "03-ros2-communication-patterns",
       "title": "ROS2 Communication Patterns",
       "chunk_index": 0,
       "content_type": "text" | "code",
       "heading": "Topic Subscriptions"
   }
   ```

6. Implement Gemini embedding integration:
   - Use LangChain GoogleGenerativeAIEmbeddings
   - Model: "models/embedding-001" or "models/text-embedding-004"
   - Handle API authentication via GOOGLE_API_KEY env var
   - Implement batch processing (max 100 texts per batch)
   - Include retry logic with exponential backoff

7. Configure Qdrant upload:
   - Connect to Qdrant Cloud (QDRANT_URL, QDRANT_API_KEY env vars)
   - Create collection "book_chunks" with vector size 768
   - Batch upload with proper metadata payload
   - Use deterministic IDs based on URL + chunk_index for idempotency
   - Include progress tracking with tqdm

8. Environment variables required:
   ```
   GOOGLE_API_KEY=your-gemini-api-key
   QDRANT_URL=https://your-cluster.qdrant.io
   QDRANT_API_KEY=your-qdrant-api-key
   SITEMAP_URL=https://nadeemsangrasi.github.io/humanoid-and-robotic-book/sitemap.xml
   ```

9. Follow Context7 MCP conventions:
   - Use Gemini embeddings only (no OpenAI)
   - Follow Qdrant best practices for batch uploads
   - Output deterministic Python code
   - Include proper error handling and logging

## Examples

Input: "Create book ingestion pipeline for textbook"
Output: Creates ingest-book.py that:
1. Fetches sitemap.xml from SITEMAP_URL
2. Crawls all 23 textbook pages
3. Extracts and chunks content
4. Embeds with Gemini
5. Uploads to Qdrant with full metadata

Input: "Re-index the textbook"
Output: Runs ingest-book.py which idempotently updates Qdrant collection
