---
name: wp-structured-data
description: "Use when emitting JSON-LD structured data (schema.org) from a WordPress theme or plugin — FAQPage, HowTo, ItemList, Recipe, Event, Product, Review — especially when the data lives in post meta / custom fields the SEO plugin can't see, OR when you must avoid duplicating the schema an SEO plugin (Rank Math, Yoast SEO, SEOPress) already outputs. Covers building the @graph in PHP, escaping with wp_json_encode, printing on wp_head, validating, and coexisting with SEO-plugin graphs. Triggers: \"add FAQ schema\", \"FAQPage JSON-LD\", \"add structured data\", \"schema.org markup WordPress\", \"rich results\", \"HowTo schema\", \"ItemList schema\", \"my FAQ rich result isn't showing\", \"duplicate Article schema\", \"Rank Math already outputs schema\", \"Yoast schema graph\", \"json-ld in head or footer\", \"wp_json_encode schema\", \"schema for custom fields\", \"breadcrumb schema duplicate\", \"validate structured data\". Not for: configuring an SEO plugin's built-in schema UI (use the plugin's own settings); meta tags / OpenGraph (that's SEO-plugin territory); on-page heading/markup SEO."
---

# WordPress Structured Data (JSON-LD)

> **Model note:** Building a single schema type is mechanical (`haiku`). Reach for `sonnet`/`opus` only when reconciling a complex graph against an existing SEO-plugin graph.

Emit schema.org JSON-LD from theme/plugin code for content an SEO plugin can't generate on its own — without duplicating what the SEO plugin already ships.

## When to use

- Content lives in **post meta / custom fields** (e.g. an FAQ repeater) and is *stripped from the rendered content*, so Rank Math/Yoast can't detect it.
- You render a **custom section** (table of contents, related items, steps) that warrants `ItemList` / `HowTo`.
- You need a schema type the SEO plugin doesn't offer on that template.

## Rule 0 — never duplicate the SEO plugin's graph

Most sites already run Rank Math, Yoast, or SEOPress. They emit a `@graph` with `WebSite`, `WebPage`, `Organization`, `Person`, `BreadcrumbList`, and an article type (`Article`/`BlogPosting`/`Product`). **Never** re-emit those — duplicate/competing nodes confuse parsers and can suppress rich results.

**Always** check first what is already on the page:

```bash
# View source, then list the @type values in every ld+json block
curl -s "<url>" | grep -A99 'application/ld+json'
```

Or in the browser console:

```js
[...document.querySelectorAll('script[type="application/ld+json"]')]
  .flatMap(s => { const j = JSON.parse(s.textContent); return (j['@graph']||[j]).map(n => n['@type']); });
```

Only add types the existing graph is **missing** (commonly `FAQPage`, `HowTo`, `Recipe`, custom `ItemList`).

## Pattern — build in PHP, print on `wp_head`

```php
add_action( 'wp_head', function () {
    if ( ! is_singular( 'post' ) ) {
        return;
    }

    $faqs = get_post_meta( get_the_ID(), 'my_faqs', true ); // stripped from content
    if ( empty( $faqs ) || ! is_array( $faqs ) ) {
        return;
    }

    $questions = array();
    foreach ( $faqs as $faq ) {
        if ( empty( $faq['question'] ) ) {
            continue;
        }
        $questions[] = array(
            '@type'          => 'Question',
            'name'           => wp_strip_all_tags( $faq['question'] ),
            'acceptedAnswer' => array(
                '@type' => 'Answer',
                'text'  => wp_kses_post( wpautop( $faq['answer'] ?? '' ) ),
            ),
        );
    }

    if ( ! $questions ) {
        return;
    }

    $schema = array(
        '@context'   => 'https://schema.org',
        '@type'      => 'FAQPage',
        'mainEntity' => $questions,
    );

    echo '<script type="application/ld+json">' . wp_json_encode( $schema ) . '</script>' . "\n";
} );
```

### Key points

- **Build a PHP array, then `wp_json_encode()`** — never hand-concatenate JSON. `wp_json_encode()` escapes for the `<script>` context; output is safe to print as-is. (PHPCS's `EscapeOutput` sniff doesn't recognise it as an escaper; suppress it via a centralized `phpcs.xml.dist` exclude scoped to the file rather than scattering inline ignores.)
- **`@type` text:** `wp_strip_all_tags()` for short names/titles; `wp_kses_post()` for answer/description bodies that may carry HTML.
- **head vs footer is irrelevant to Google** — it parses JSON-LD anywhere. Use `wp_head` to sit alongside the SEO plugin's graph (convention), or `wp_footer` if you need late data; both work.
- **Gate to the right context** (`is_singular()`, post type, a feature toggle) so schema only appears where the content does.
- **Mirror visible content.** Schema must reflect what users actually see on the page (Google's structured-data policy). Don't emit FAQ schema for FAQs you don't render.

## Common types worth emitting from code

| Type | Use for | Usually missing from SEO plugins? |
|------|---------|-----------------------------------|
| `FAQPage` | Q&A stored in meta / repeater | Yes, when stripped from content |
| `HowTo` | Step-by-step tutorial sections | Often |
| `ItemList` | TOC, related items, rankings | Yes |
| `Recipe` | Recipe meta fields | Yes (unless a recipe plugin) |
| `Article`/`BlogPosting` | The post itself | **No — SEO plugin owns this** |
| `BreadcrumbList` | Breadcrumb trail | **No — SEO plugin owns this** |

## Validate

- Google **Rich Results Test** (search.google.com/test/rich-results) — confirms eligibility per type.
- Schema.org **validator** (validator.schema.org) — structural correctness.
- Confirm there's exactly **one** node per type across all blocks (no duplicate `Article`/`FAQPage`).

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Re-emitting `Article`/`BreadcrumbList`/`Organization` the SEO plugin already outputs | **Never** duplicate — inspect existing `ld+json` first; add only missing types |
| Hand-building the JSON string | **Always** build a PHP array + `wp_json_encode()` |
| FAQ schema present but FAQs not visible on the page | Mirror visible content — only emit schema for rendered content |
| Assuming head vs footer affects indexing | It doesn't; place by convention (`wp_head`) |
| Inline `// phpcs:ignore` for the `wp_json_encode` echo | Centralize the `EscapeOutput` exclude in `phpcs.xml.dist`, scoped to the file |
| Emitting schema on every template | Gate with `is_singular()` / post type / feature toggle |
