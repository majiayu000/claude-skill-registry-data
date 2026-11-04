---
name: deep-research
description: "Deep Research Agent for complex, multi-step research requiring web research, planning, and synthesis. Use instead of single web_search for any topic requiring multi-angle investigation. Trigger on: 'what is X', 'research X', 'compare X and Y', before content generation tasks."
---

# Deep Research Agent

> "Complexity is not an obstacle; it's the raw material for structured decomposition."

Kapsamlı, çok kaynaklı araştırma için sistematik metodoloji. Tek web_search yeterli olmadığında kullan.

## Core Principle

**Tek arama = yüzeysel bilgi.** Kaliteli çıktı = kaliteli araştırma. Asla genel bilgiden içerik üretme.

---

## Araştırma Metodolojisi (DeerFlow-inspired)

### Phase 1 — Broad Exploration (Geniş Tarama)

Ana konuyu anlamak için geniş sorgular:
1. **İlk tarama**: Konuyu genel olarak tara
2. **Boyutları belirle**: Hangi alt konular, açılar, perspektifler var?
3. **Harita çiz**: Farklı bakış açıları, paydaşlar, tartışmalı noktalar

```
Örnek: "Oracle agent mimarisi"
İlk sorgular:
- "AI agent orchestration architecture 2025"
- "multi-agent system design patterns"
- "LLM agent memory context management"

Tespit edilen boyutlar:
- Memory sistemleri (short/long term)
- Tool filtering ve güvenlik
- Trace/observability
- Subagent delegation patterns
```

### Phase 2 — Deep Dive (Derinlemesine)

Her önemli boyut için hedefli araştırma:
1. **Spesifik sorgular**: Her alt konu için ayrı keyword
2. **Farklı ifadeler dene**: Aynı konuyu farklı kelimelerle ara
3. **Tam içeriği oku**: web_fetch ile sadece snippet değil, tam sayfa
4. **Referansları takip et**: Kaynakların bahsettiği diğer kaynakları ara

### Phase 3 — Diversity & Validation (Çeşitlilik)

| Bilgi Tipi | Amaç | Sorgu Örnekleri |
|---|---|---|
| **Gerçek & Data** | Somut kanıt | "statistics", "benchmark", "numbers" |
| **Örnekler & Vakalar** | Gerçek uygulama | "case study", "example", "implementation" |
| **Uzman Görüşleri** | Otorite perspektifi | "expert analysis", "opinion", "commentary" |
| **Trendler** | Gelecek yönü | "trend 2025", "forecast", "future" |
| **Karşılaştırma** | Bağlam | "vs", "comparison", "alternatives" |
| **Eleştiriler** | Dengeli bakış | "challenges", "limitations", "criticism" |

### Phase 4 — Reflection Generation (Yansima Uretimi) [v2]

Her onemli kaynak icin distilled insight olustur. Ham icerik yerine yoğunlastirilmis bilgi kaydet.

**Her kaynak icin:**
1. URL + baslik kaydet
2. 2-3 cumlede distilled insight yaz (reflection)
3. `memory_store` ile kaydet: `category="research_reflection"`

**Reflection formati:**
```
- [Kaynak Basligi](URL): [2-3 cumle distilled insight]
```

**Ornekler:**

Iyi:
```
- [LATS: Language Agent Tree Search](https://arxiv.org/abs/2310.04406):
  MCTS + LLM reflection birlestiren agent search. Her basarisiz denemede
  self-reflection uretip sonraki denemeyi yonlendiriyor. ReAct'tan %22
  daha iyi HumanEval'da.
```

Kotu:
```
- [LATS paper](URL): Ilginc bir calisma, agent'lar icin onemli gorusuyor.
```

**Kurallar:**
- Spesifik veri, somut bulgu, uygulanabilir cikti odakli ol
- YASAK: Genel ifadeler ("ilginc", "onemli", "dikkat cekici")
- Her reflection bagimsiz anlasilabilir olmali
- Minimum 5, maksimum 20 reflection (konu genisligine gore)

### Phase 5 — Synthesis from Reflections (Yansimalardan Sentez) [v2]

Icerik uretimini ham kaynak yerine SADECE reflection'lardan yap.

```
sessions_spawn(
  task="Asagidaki arastirma reflection'larindan kapsamli sentez yaz:\n\n[TUM REFLECTION'LAR]\n\nKurallar:\n- Sadece reflection'lardaki bilgiyi kullan\n- Kaynak URL'lerini icerige dahil et\n- Celiskili bulgulari belirt\n- Bilgi boslugu varsa isaretleKonular arasi baglanti kur",
  model="sonnet-4-6"
)
```

**Token tasarrufu:**
- ~50K ham veri → ~3K reflection = ~%94 azalma
- Writer subagent'a sadece reflection'lar gider (tam content DEGIL)
- Context penceresi korunur, sentez kalitesi artar (gurultu azalir)

**Reflection yetersizse:**
- Phase 4'teki minimum 5 kurali kontrole et
- Eksik boyut varsa Phase 2-3'e don, ek arastirma yap
- Yeni reflection'lar ekle, sonra Phase 5'i tekrarla

### Phase 6 — Synthesis Check (Sentez Kontrolu)

Icerik uretimine gecmeden once:
- [ ] En az 3-5 farkli acidan aradim mi?
- [ ] Onemli kaynaklari tam okudum mu?
- [ ] Somut veri, ornek, uzman gorusu var mi?
- [ ] Hem olumlu hem elestirel perspektif var mi?
- [ ] Bilgi guncel mi?
- [ ] Reflection'lar spesifik ve uygulanabilir mi? [v2]
- [ ] Writer subagent'a sadece reflection'lar mi gitti? [v2]

**Herhangi biri HAYIR ise → arastirmaya devam et.**

---

## Etkili Sorgu Stratejisi

```bash
# Bağlam ile spesifik ol
❌ "AI trends"
✅ "enterprise AI agent architecture 2025"

# Otoriter kaynak ipuçları ekle
"[konu] research paper"
"[konu] benchmark comparison"
"[konu] industry analysis"

# İçerik tipi belirt
"[konu] case study"
"[konu] statistics"
"[konu] expert interview"

# Temporal qualifier
"[konu] 2025"
"[konu] latest"
"[konu] recent"
```

## web_fetch Ne Zaman Kullan

- Arama sonucu yüksek relevance gösteriyor
- Snippet yeterli değil, tam içerik gerekiyor
- Data, case study, uzman analizi var
- Tam bağlamı anlamak gerekiyor

---

## Kalite Çubuğu

Araştırma yeterli sayılır, şunları yanıtlayabiliyorsam:
- Temel gerçekler ve veriler neler?
- 2-3 somut gerçek dünya örneği?
- Uzmanlar ne diyor?
- Mevcut trendler ve gelecek yönü?
- Zorluklar ve limitasyonlar?
- Bu konu şu an neden önemli?

## Kaçınılacaklar

- ❌ 1-2 aramada durma
- ❌ Snippet'e güvenip tam kaynak okumama
- ❌ Konunun sadece bir boyutunu arama
- ❌ Çelişkili görüşleri görmezden gelme
- ❌ Güncel olmayan bilgiyi kullanma
- ❌ Araştırma tamamlanmadan içerik üretme

---

## Multi-Step Research Planning

Karmaşık sorular için plan önce:
1. **Hedefi parçala**: Ana soruyu alt sorulara böl
2. **Sıralı/paralel execution**: Bağımlılıkları belirle
3. **Context yönet**: Bulguları düzenli kaydet
4. **Sentez**: Tüm bulguları birleştir → tutarlı rapor

### Subagent Delegation (Büyük Araştırmalar)
Uzun araştırmalarda sessions_spawn ile Gemini Pro subagent kullan:
- 2M context → tüm repo/döküman okuyabilir
- $0 maliyet (OAuth)
- Oracle token'ı korunur

```
sessions_spawn(
  task="[araştırma görevi]",
  model="gemini31-pro",
  runtime="subagent"
)
```

---

## Çıktı Formatı

Araştırma tamamlandığında:
1. Konunun çok açılı kapsamlı analizi
2. Spesifik gerçekler, veriler, istatistikler
3. Gerçek dünya örnekleri ve vakalar
4. Uzman perspektifleri ve otoriter kaynaklar
5. Güncel trendler ve bağlam
6. **Kaynak listesi** (`[başlık](URL)` formatında)

**Ancak bundan sonra içerik üret.**
