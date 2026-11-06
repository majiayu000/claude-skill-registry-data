---
name: science-fulltext-hunting
description: Use when you have a DOI/PMID/arXiv id and need the actual PDF or JATS full text, when a download returns HTML instead of a PDF, or when building the methods section and you need page-level quotes; covers the nine-stage fallback chain, how to verify a real PDF, and what provenance to record.
---

# 全文获取：九级回退与验真

## 铁律：200 不等于拿到了全文

实测中大量站点回 **200 + `text/html`**：Cookie 门、登录页、"请启用 cookie"跳转页。
**每一级都必须验**：`content-type` 含 `pdf` **且** 文件头是 `%PDF-`；JATS 则验根元素 `<article`。

判失败的特征：
- 内容是 HTML 且含 `cookies_not_supported` / `sign in` / `access denied` / `captcha`
- 重定向后的 `finalUrl` 落在 `/login`、`/sorry/`、`?error=`
- 长度 < 20KB 的"PDF"（多为占位页）

## 九级顺序（不跳级，除非上层明确 no-oa）

1. `OpenAlex best_oa_location.pdf_url` —— **经常是空的**，别停在这一级
2. `OpenAlex locations[].pdf_url` —— 遍历全部 location，取第一个非空
3. `Unpaywall /v2/{doi}?email=` —— 需真实邮箱（占位会被 422 拒）
4. `Europe PMC fullTextUrlList` —— 挑 `documentStyle=pdf` 且 `availability` 含 open
5. `Europe PMC /{PMCID}/fullTextXML` —— **优先 JATS**：有章节标签，做证据链比 PDF 好切
6. `PMC efetch db=pmc&id={pmcid}&retmode=xml` —— 无需 key
7. 直链模板（这四个实测无门）：
   - arXiv `https://arxiv.org/pdf/{id}`（支持 Range）
   - PLOS `journals.plos.org/plosone/article/file?id={doi}&type=printable`
   - Frontiers `frontiersin.org/articles/{doi}/pdf`
   - bioRxiv `biorxiv.org/content/{doi}v1.full.pdf`（medRxiv 同路径会 403）
8. 出版商 Cookie 两步：先 GET 落地页收 Cookie，再带 `Referer` + Cookie 请求 PDF
   - Springer `link.springer.com/content/pdf/{doi}.pdf`
   - Nature `nature.com/articles/{suffix}.pdf`
9. CF 站点（Wiley `pdfdirect/`、SAGE `doi/pdf/`、T&F `doi/pdf/`、MDPI）—— 需 TLS 指纹伪装；本机默认判 `blocked`

Sci-Hub（`.st`/`.ru`）返回的是 **ALTCHA PoW 挑战页**，默认关闭；开了也要接受它可能变算法。

## 拿到之后

1. **抽结构**：PDF 用 pymupdf 逐页取文本并记 `page_from/page_to`；JATS 按 `<sec sec-type>` 切。
2. **留 page 偏移**：证据链要能回答"这句话在第几页第几段"，所以抽文本时同时存字符偏移到页码的映射。
3. **算哈希**：文件 sha256 + 来源 URL + 时间，写进 `resolve_attempt`。同一篇下次先查哈希，别重下。
4. **抽参考文献 DOI**：从 JATS `<ref-list>` 或 PDF 末尾正则抓 DOI，供滚雪球（前向/后向各一轮）。

## 失败时怎么汇报

不要只说"下载失败"。按级写清楚：

```
doi:10.1002/anie.201900123
L1 openalex best_oa   : empty
L2 openalex locations : 3 条，无 pdf_url
L3 unpaywall          : skipped（未配置邮箱）
L4 europepmc          : 非 OA
L7 直链               : -
L8 wiley pdfdirect    : 403 text/html（CF）
结论：需要代理或机构权限，已记 blocked，未污染其他级的 provenance
```

这份记录进 `docs/` 或项目日志，下次别人接手不用再试一遍。
