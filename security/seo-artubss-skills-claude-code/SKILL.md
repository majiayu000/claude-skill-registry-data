---
name: seo
description: Otimize para visibilidade e ranking em mecanismos de busca. Use quando solicitado a "melhorar SEO", "otimizar para busca", "corrigir meta tags", "adicionar dados estruturados", "otimização de sitemap" ou "otimização para mecanismos de busca".
license: MIT
metadata:
  author: web-quality-skills
  version: "1.0"
---

# Otimização de SEO

Otimização para mecanismos de busca baseada em auditorias SEO do Lighthouse e diretrizes do Google Search. Foco em SEO técnico, otimização on-page e dados estruturados.

## Fundamentos de SEO

Fatores de ranking em mecanismos de busca (influência aproximada):

| Fator | Influência | Esta Skill |
|--------|-----------|------------|
| Qualidade e relevância de conteúdo | ~40% | Parcial (estrutura) |
| Backlinks e autoridade | ~25% | ✗ |
| SEO técnico | ~15% | ✓ |
| Experiência de página (Core Web Vitals) | ~10% | Veja [Core Web Vitals](../core-web-vitals/SKILL.md) |
| SEO on-page | ~10% | ✓ |

---

## SEO técnico

### Rastreabilidade

**robots.txt:**
```text
# /robots.txt
User-agent: *
Allow: /

# Bloquear áreas administrativas/privadas
Disallow: /admin/
Disallow: /api/
Disallow: /private/

# Não bloquear recursos necessários para renderização
# ❌ Disallow: /static/

Sitemap: https://example.com/sitemap.xml
```

**Meta robots:**
```html
<!-- Padrão: indexável, seguir links -->
<meta name="robots" content="index, follow">

<!-- Noindex em páginas específicas -->
<meta name="robots" content="noindex, nofollow">

<!-- Indexável mas não seguir links -->
<meta name="robots" content="index, nofollow">

<!-- Controlar trechos -->
<meta name="robots" content="max-snippet:150, max-image-preview:large">
```

**URLs canônicas:**
```html
<!-- Prevenir problemas de conteúdo duplicado -->
<link rel="canonical" href="https://example.com/page">

<!-- URL canônica auto-referenciada (recomendado) -->
<link rel="canonical" href="https://example.com/current-page">

<!-- Para conteúdo paginado -->
<link rel="canonical" href="https://example.com/products">
<!-- Ou use rel="prev" / rel="next" para paginação explícita -->
```

### Sitemap XML

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://example.com/</loc>
    <lastmod>2024-01-15</lastmod>
    <changefreq>daily</changefreq>
    <priority>1.0</priority>
  </url>
  <url>
    <loc>https://example.com/products</loc>
    <lastmod>2024-01-14</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>
</urlset>
```

**Boas práticas de sitemap:**
- Máximo 50.000 URLs ou 50MB por sitemap
- Use índice de sitemap para sites maiores
- Inclua apenas URLs canônicas e indexáveis
- Atualize `lastmod` quando o conteúdo mudar
- Envie para Google Search Console

### Estrutura de URL

```
✅ URLs boas:
https://example.com/products/blue-widget
https://example.com/blog/how-to-use-widgets

❌ URLs ruins:
https://example.com/p?id=12345
https://example.com/products/item/category/subcategory/blue-widget-2024-sale-discount
```

**Diretrizes de URL:**
- Use hífens, não underscores
- Apenas minúsculas
- Mantenha curtas (< 75 caracteres)
- Inclua palavras-chave alvo naturalmente
- Evite parâmetros quando possível
- Use sempre HTTPS

### HTTPS e segurança

```html
<!-- Certifique-se de que todos os recursos usam HTTPS -->
<img src="https://example.com/image.jpg">

<!-- Não: -->
<img src="http://example.com/image.jpg">
```

**Headers de segurança como sinais de confiança para SEO:**
```
Strict-Transport-Security: max-age=31536000; includeSubDomains
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
```

---

## SEO on-page

### Title tags

```html
<!-- ❌ Ausente ou genérico -->
<title>Page</title>
<title>Home</title>

<!-- ✅ Descritivo com palavra-chave primária -->
<title>Blue Widgets para Venda | Qualidade Premium | Example Store</title>
```

**Diretrizes de title tag:**
- 50-60 caracteres (Google trunca ~60)
- Palavra-chave primária perto do início
- Única para cada página
- Nome da marca no final (exceto homepage)
- Orientado para ação quando apropriado

### Meta descriptions

```html
<!-- ❌ Ausente ou duplicada -->
<meta name="description" content="">

<!-- ✅ Atraente e única -->
<meta name="description" content="Compre blue widgets premium com frete grátis. Devoluções em 30 dias. Classificação 4.9/5 por mais de 10.000 clientes. Peça agora e economize 20%.">
```

**Diretrizes de meta description:**
- 150-160 caracteres
- Inclua palavra-chave primária naturalmente
- Call-to-action atraente
- Única para cada página
- Corresponda ao conteúdo da página

### Estrutura de headings

```html
<!-- ❌ Estrutura pobre -->
<h2>Bem-vindo à nossa loja</h2>
<h4>Produtos</h4>
<h1>Entre em contato</h1>

<!-- ✅ Hierarquia apropriada -->
<h1>Blue Widgets - Qualidade Premium</h1>
  <h2>Características do produto</h2>
    <h3>Durabilidade</h3>
    <h3>Design</h3>
  <h2>Avaliações de clientes</h2>
  <h2>Preços</h2>
```

**Diretrizes de headings:**
- Um único `<h1>` por página (o tema principal)
- Hierarquia lógica (não pule níveis)
- Inclua palavras-chave naturalmente
- Descritivos, não genéricos

### SEO de imagens

```html
<!-- ❌ SEO de imagem pobre -->
<img src="IMG_12345.jpg">

<!-- ✅ Imagem otimizada -->
<img src="blue-widget-product-photo.webp"
     alt="Blue widget com acabamento cromado, vista lateral mostrando painel de controle"
     width="800"
     height="600"
     loading="lazy">
```

**Diretrizes de imagem:**
- Nomes de arquivo descritivos com palavras-chave
- Texto alt descreve o conteúdo da imagem
- Comprimida e redimensionada adequadamente
- WebP/AVIF com fallbacks
- Carregamento lazy para imagens abaixo da dobra

### Links internos

```html
<!-- ❌ Não-descritivo -->
<a href="/products">Clique aqui</a>
<a href="/widgets">Leia mais</a>

<!-- ✅ Texto âncora descritivo -->
<a href="/products/blue-widgets">Navegue nossa coleção de blue widgets</a>
<a href="/guides/widget-maintenance">Aprenda como manter seus widgets</a>
```

**Diretrizes de links:**
- Texto âncora descritivo com palavras-chave
- Links para páginas internas relevantes
- Número razoável de links por página
- Corrija links quebrados rapidamente
- Use breadcrumbs para hierarquia

---

## Dados estruturados (JSON-LD)

### Organization

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "Example Company",
  "url": "https://example.com",
  "logo": "https://example.com/logo.png",
  "sameAs": [
    "https://twitter.com/example",
    "https://linkedin.com/company/example"
  ],
  "contactPoint": {
    "@type": "ContactPoint",
    "telephone": "+1-555-123-4567",
    "contactType": "customer service"
  }
}
</script>
```

### Article

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "Como escolher o widget certo",
  "description": "Guia completo para selecionar widgets de acordo com suas necessidades.",
  "image": "https://example.com/article-image.jpg",
  "author": {
    "@type": "Person",
    "name": "Jane Smith",
    "url": "https://example.com/authors/jane-smith"
  },
  "publisher": {
    "@type": "Organization",
    "name": "Example Blog",
    "logo": {
      "@type": "ImageObject",
      "url": "https://example.com/logo.png"
    }
  },
  "datePublished": "2024-01-15",
  "dateModified": "2024-01-20"
}
</script>
```

### Product

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "Blue Widget Pro",
  "image": "https://example.com/blue-widget.jpg",
  "description": "Blue widget premium com recursos avançados.",
  "brand": {
    "@type": "Brand",
    "name": "WidgetCo"
  },
  "offers": {
    "@type": "Offer",
    "price": "49.99",
    "priceCurrency": "USD",
    "availability": "https://schema.org/InStock",
    "url": "https://example.com/products/blue-widget"
  },
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "4.8",
    "reviewCount": "1250"
  }
}
</script>
```

### FAQ

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "Quais cores estão disponíveis?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Nossos widgets estão disponíveis em azul, vermelho e verde."
      }
    },
    {
      "@type": "Question",
      "name": "Qual é a garantia?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Todos os widgets incluem garantia de 2 anos."
      }
    }
  ]
}
</script>
```

### Breadcrumbs

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {
      "@type": "ListItem",
      "position": 1,
      "name": "Home",
      "item": "https://example.com"
    },
    {
      "@type": "ListItem",
      "position": 2,
      "name": "Produtos",
      "item": "https://example.com/products"
    },
    {
      "@type": "ListItem",
      "position": 3,
      "name": "Blue Widgets",
      "item": "https://example.com/products/blue-widgets"
    }
  ]
}
</script>
```

### Validação

Teste dados estruturados em:
- [Google Rich Results Test](https://search.google.com/test/rich-results)
- [Schema.org Validator](https://validator.schema.org/)

---

## SEO mobile

### Design responsivo

```html
<!-- ❌ Não é amigável para mobile -->
<meta name="viewport" content="width=1024">

<!-- ✅ Viewport responsivo -->
<meta name="viewport" content="width=device-width, initial-scale=1">
```

### Alvo de toque

```css
/* ❌ Muito pequeno para mobile */
.small-link {
  padding: 4px;
  font-size: 12px;
}

/* ✅ Alvo de toque adequado */
.mobile-friendly-link {
  padding: 12px;
  font-size: 16px;
  min-height: 48px;
  min-width: 48px;
}
```

### Tamanhos de fonte

```css
/* ❌ Muito pequeno em mobile */
body {
  font-size: 10px;
}

/* ✅ Legível sem zoom */
body {
  font-size: 16px;
  line-height: 1.5;
}
```

---

## SEO internacional

### Tags hreflang

```html
<!-- Para sites multi-idioma -->
<link rel="alternate" hreflang="en" href="https://example.com/page">
<link rel="alternate" hreflang="es" href="https://example.com/es/page">
<link rel="alternate" hreflang="fr" href="https://example.com/fr/page">
<link rel="alternate" hreflang="x-default" href="https://example.com/page">
```

### Declaração de idioma

```html
<html lang="en">
<!-- ou -->
<html lang="es-MX">
```

---

## Checklist de auditoria SEO

### Crítico
- [ ] HTTPS habilitado
- [ ] robots.txt permite rastreamento
- [ ] Nenhum `noindex` em páginas importantes
- [ ] Title tags presentes e únicas
- [ ] Um único `<h1>` por página

### Alta prioridade
- [ ] Meta descriptions presentes
- [ ] Sitemap enviado
- [ ] URLs canônicas definidas
- [ ] Responsivo para mobile
- [ ] Core Web Vitals passando

### Prioridade média
- [ ] Dados estruturados implementados
- [ ] Estratégia de links internos
- [ ] Texto alt em imagens
- [ ] URLs descritivas
- [ ] Navegação por breadcrumb

### Contínuo
- [ ] Corrija erros de rastreamento no Search Console
- [ ] Atualize sitemap quando o conteúdo mudar
- [ ] Monitore mudanças de ranking
- [ ] Verifique links quebrados
- [ ] Revise insights do Search Console

---

## Ferramentas

| Ferramenta | Uso |
|------|-----|
| Google Search Console | Monitorar indexação, corrigir problemas |
| Google PageSpeed Insights | Performance + Core Web Vitals |
| Rich Results Test | Validar dados estruturados |
| Lighthouse | Auditoria SEO completa |
| Screaming Frog | Análise de rastreamento |

## Referências

- [Google Search Central](https://developers.google.com/search)
- [Schema.org](https://schema.org/)
- [Core Web Vitals](../core-web-vitals/SKILL.md)
- [Web Quality Audit](../web-quality-audit/SKILL.md)