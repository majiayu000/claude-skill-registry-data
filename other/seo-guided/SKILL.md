---
description: Apply Google's official SEO Starter Guide principles to web development and content generation. Emphasizes descriptive URLs, canonicalization, semantic HTML, proper title/meta tags, and crawlability.
---

# Google SEO Guided Skill

This skill is based directly on the Google Search Central SEO Starter Guide. Use this skill when asked to review, write, or refactor code and content for Search Engine Optimization (SEO).

## Core Principles

1. **Help Google Find Your Content**:
   - Submit a Sitemap (`sitemap.xml`) to help engines find your latest URLs.
   - Provide logical cross-linking (internal links) so crawlers can naturally discover pages.
   
2. **Organize Your Site**:
   - **Descriptive URLs**: Use clear words relevant to the content in URLs. Avoid opaque IDs or long random strings (`/pets/cats` instead of `/123/xYz`).
   - **Group by Directories**: Use directories to logically group topically similar pages, helping Google understand the structure and frequency of updates.
   - **Canonicalization**: Reduce duplicate content by explicitly specifying the canonical URL using `<link rel="canonical" href="..." />`. Ensure every piece of content is primarily accessible via a single URL.

3. **Influence How Your Site Looks in Google Search**:
   - **Title Links (`<title>`)**: Write unique, clear, and concise titles. They should describe the page accurately. Avoid boilerplate or identical titles across multiple pages.
   - **Meta Descriptions**: Provide short, unique (per page) summaries in the `<meta name="description">` tag. This influences the snippet shown in search results.

4. **Make Your Site Interesting and Useful**:
   - Anticipate the terminology users will search for and include those terms naturally in your text.
   - Do not focus on keyword stuffing or the `<meta name="keywords">` tag, as Google ignores it. Focus on readable, helpful content.
   
5. **Optimize Images**:
   - Use high-quality images placed near relevant text context.
   - Always include descriptive `alt` text for images to help search engines understand the image content.

6. **Semantic Output**:
   - Using logical headings (`<h1>`, `<h2>`, etc.) helps structure the document and makes it understandable for both users and bots.
   - Avoid having too many headers if they are not structurally necessary.

## Implementation Guidelines
When reviewing a Next.js (or similar) codebase:
- Check `metadata` (Title, Description, OpenGraph).
- Check dynamic route generation (e.g., `generateMetadata` in Next.js) to ensure strictly unique titles, descriptions, and canonical URLs.
- Look out for generic metadata canonicals that accidentally copy to children pages.
- Verify internal linking structure: ensure HTML Sitemaps, Header/Footer navigation, and Breadcrumbs are properly linked.
- Confirm schema markup/structured data via JSON-LD is properly implemented for rich results (e.g., LocalBusiness, FAQs).
