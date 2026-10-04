---
name: exportacao-multiplos-formatos
description: Pipeline de exportação de manuscritos para DOCX, PDF, ePub, Markdown e TXT com preservação de formatação e metadados. Ativar ao implementar funcionalidades de exportação de textos (UC-008, UC-064, UC-089, UC-197) ou importação de formatos externos (UC-194, UC-195, UC-196).
---

# exportacao-multiplos-formatos

## Descrição
A skill `exportacao-multiplos-formatos` especifica o pipeline de conversão de documentos entre o formato interno JSON ProseMirror e os formatos externos usados por escritores e editoras (DOCX, PDF, ePub, Markdown, TXT). Ela define os conversores recomendados, o fluxo de processamento assíncrono em background para exportações grandes, a estrutura de metadados incluídos em cada formato e os casos especiais de formatação literária (notas de rodapé, numeração de capítulos).

## Quando usar
Gatilhos concretos e observáveis:
- Implementação das ações de exportação no menu do editor (UC-008, UC-064, UC-197).
- Importação de manuscritos externos (Scrivener/DOCX/ePub) para o editor (UC-194, UC-195, UC-196).
- Geração do PDF ilustrado do universo (wiki + fichas + grafo) em UC-089.

Quando NÃO usar:
- Para exportação de dados de usuário por conformidade LGPD (usar `conformidade-com-lgpd-e-gdpr-por-design`).
- Para portabilidade do grafo GUF em formato JSON-LD (coberto pela mesma skill LGPD).

## Pré-requisitos
- **DOCX:** `docx` (Node.js) ou `python-docx` (Python).
- **PDF:** `puppeteer` (headless Chrome) ou `@react-pdf/renderer`.
- **ePub:** `epub-gen` (Node.js).
- **Markdown:** conversão nativa do JSON ProseMirror para Markdown via `prosemirror-markdown`.
- **Importação DOCX:** `mammoth.js` para extração de texto e estilos básicos do .docx.
- Fila de processamento assíncrono (ver skill `queue-de-tarefas-assincrona-com-bull`) para exportações de documentos longos.

## Processo (passo a passo executável)
1. **Exportação (fluxo geral):**
   - Usuário clica "Exportar como [formato]" no menu do editor.
   - Para documentos menores que `SYNC_EXPORT_MAX_WORDS` palavras: processar sincronamente e retornar o arquivo para download direto.
   - Para documentos maiores: enfileirar job de exportação na fila Bull, retornar `202 Accepted` com `job_id`, notificar o usuário via WebSocket quando o arquivo estiver pronto.

2. **Exportação para DOCX:**
   - Percorrer a árvore de nós do JSON ProseMirror e mapear para objetos `docx`:
     - `paragraph` → `Paragraph`; `heading` → `Heading` com nível; `bold/italic` → `TextRun` com estilos.
     - Notas de rodapé → `FootnoteReference` + `Footnote` do pacote `docx`.
   - Incluir metadados no `Properties`: título, autor, data de exportação.

3. **Exportação para PDF (via Puppeteer):**
   - Renderizar o documento como HTML estilizado em uma página Express interna.
   - Usar Puppeteer para capturar a página e gerar o PDF com `page.pdf({ format: 'A4', printBackground: true })`.
   - Incluir cabeçalho com título do manuscrito e rodapé com número de página.

4. **Exportação para ePub:**
   - Dividir o documento por nós `heading` de nível 1 (capítulos) para gerar a estrutura de navegação do ePub.
   - Incluir metadados Dublin Core: título, autor, idioma, ISBN (se cadastrado na ficha do projeto).

5. **Importação de DOCX:**
   - Usar `mammoth.js` para extrair o HTML simplificado do arquivo .docx.
   - Converter o HTML extraído para JSON ProseMirror via `DOMParser` + serializer customizado.
   - Criar um novo documento no projeto com o conteúdo importado e marcar como `is_imported = true`.

## Parâmetros e configuração
| Parâmetro | Descrição | Padrão |
|---|---|---|
| `SYNC_EXPORT_MAX_WORDS` | Máximo de palavras para exportação síncrona | `50000` |
| `PDF_PAGE_FORMAT` | Formato de página do PDF exportado | `A4` |
| `PDF_MARGIN_MM` | Margens do PDF em milímetros | `{ top: 25, bottom: 25, left: 30, right: 30 }` |
| `EPUB_SPLIT_BY` | Nível de heading usado para dividir capítulos no ePub | `1` |

## Armadilhas e como evitá-las
- **Armadilha:** Gerar PDFs de romances longos (300+ páginas) de forma síncrona na requisição HTTP, causando timeout de 30+ segundos e experiência péssima para o usuário.
  **Mitigação:** Usar a fila Bull para processar exportações de documentos acima de `SYNC_EXPORT_MAX_WORDS` palavras em background. O usuário recebe feedback visual "Exportação em andamento..." e uma notificação push quando o arquivo estiver disponível para download.

## Critérios de validação (Definition of Done)
- [ ] Um romance de 80.000 palavras é exportado para DOCX com formatação preservada (negrito, itálico, capítulos) em menos de 30 segundos via processamento em fila.
- [ ] A importação de um arquivo .docx de 50 páginas gera um documento JSON ProseMirror válido sem perder o texto.

## Exemplos
**Exportação DOCX (documento pequeno):**
`GET /api/documents/42/export?format=docx` → retorna imediatamente `Content-Disposition: attachment; filename="Kael-e-as-Sombras.docx"`.

**Exportação PDF (documento grande):**
`POST /api/documents/42/export` `{ format: 'pdf' }` → `{ status: 202, job_id: "job-abc123" }` → WebSocket: `{ event: 'export_ready', download_url: '/downloads/job-abc123.pdf', expires_in: '24h' }`.
