---
name: technical-seo-expert
description: >
  Web sitelerini teknik SEO standartlarına uygun hale getirir. Schema Markup (JSON-LD) uygulamaları, Core Web Vitals optimizasyonu, meta etiket yönetimi ve teknik SEO dosyalarının (sitemap, robots.txt) oluşturulmasını sağlar. Kullanıcı "SEO uyumlu güncelleme", "schema markup ekle", "teknik SEO" veya "siteyi optimize et" dediğinde bu yeteneği kullanın.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
---

# Technical SEO & Schema Markup Skill

Bu yetenek, web sitelerinin arama motorları tarafından daha iyi taranmasını ve anlaşılmasını sağlamak için yazılımsal iyileştirmeler yapmaya odaklanır.

## Temel Yetkinlikler

1.  **Schema Markup (Yapılandırılmış Veri)**:
    *   JSON-LD formatında veri yapıları oluşturma.
    *   Organization, Product, Article, FAQ, Breadcrumb ve LocalBusiness şemalarını uygulama.
    *   Mevcut HTML yapısına şema verilerini entegre etme.

2.  **Teknik SEO Optimizasyonu**:
    *   Semantic HTML (Anlamsal HTML) yapısının kurulması (H1-H6 hiyerarşisi, main, section, article kullanımı).
    *   Meta etiketleri (Title, Description, Open Graph, Twitter Cards) yönetimi.
    *   Canonical etiketlerinin yerleştirilmesi.
    *   Görsel optimizasyonu (Alt text, lazy loading, modern formatlar).

3.  **Performans ve Core Web Vitals**:
    *   LCP (Largest Contentful Paint) iyileştirmeleri için görsel ve script yükleme stratejileri.
    *   CLS (Cumulative Layout Shift) engellemek için boyut tanımlamaları.
    *   Scriptlerin `async` veya `defer` ile yönetilmesi.

4.  **Altyapı Dosyaları**:
    *   Dinamik veya statik `sitemap.xml` oluşturma.
    *   Doğru yapılandırılmış `robots.txt` hazırlama.

## Uygulama Rehberi

### Schema Markup Ekleme (JSON-LD)
Her zaman `<script type="application/ld+json">` bloğunu tercih edin.

**Örnek FAQ Yapısı:**
```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [{
    "@type": "Question",
    "name": "Soru metni buraya?",
    "acceptedAnswer": {
      "@type": "Answer",
      "text": "Cevap metni buraya."
    }
  }]
}
</script>
```

### Next.js / React SEO Uygulaması
Modern frameworklerde SEO yönetimi için özel bileşenleri veya API'leri kullanın.

**Next.js Metadata Örneği:**
```typescript
export const metadata = {
  title: 'Sayfa Başlığı',
  description: 'SEO uyumlu açıklama metni',
  alternates: {
    canonical: 'https://example.com/sayfa',
  },
};
```

## Dikkat Edilmesi Gerekenler
- Tek bir sayfada birden fazla H1 başlığı olmamasına dikkat edin.
- Görsellerin `alt` etiketlerinin boş kalmadığından emin olun.
- Mevcut kodda değişiklik yaparken SEO değerlerini (mevcut meta tagler gibi) koruyun, sadece iyileştirme yapın.
- Sayfa hızını etkilemeyecek şekilde script yerleşimi yapın.