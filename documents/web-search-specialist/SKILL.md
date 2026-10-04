---
name: web-search-specialist
description: "Especialista em Pesquisa Avançada na Web e Motores de Busca (Google, DuckDuckGo, Bing, SearXNG, Yahoo, Mojeek). Domina operadores booleanos, Google Dorks, filtros estruturais (site, filetype, intitle, inurl), busca temporal, estratégias de desambiguação e verificação de fatos/fontes primárias."
---

# Web Search Specialist & Search Engine Intelligence

Esta skill estabelece a metodologia avançada de investigação, busca de informações e engenharia de queries em motores de busca na internet (**Google, DuckDuckGo, Bing, SearXNG, Yahoo, Mojeek e Kagi**).

---

## 🎯 1. Princípios Fundamentais de Busca na Web

1. **Economia de Ruído e Alta Precisão**:
   - Evitar consultas puramente conversacionais quando o objetivo for localizar documentos técnicos, tabelas, dados brutos ou páginas específicas.
   - Utilizar palavras-chave discriminantes em vez de stopwords ou frases prolixas.
2. **Triangulação de Fontes**:
   - Nunca confiar em um único resultado isolado para afirmações factuais críticas ou estatísticas.
   - Cruzar fontes primárias (sites oficiais, órgãos governamentais, relatórios originais) com fontes secundárias confiáveis.
3. **Estratégia de Busca Progressiva (Scoping & Funneling)**:
   - **Etapa 1 (Ampliação)**: Consulta exploratória ampla para identificar terminologia correta e sinônimos da indústria.
   - **Etapa 2 (Focalização)**: Aplicação de aspas e operadores de exclusão/inclusão para eliminar ruídos óbvios.
   - **Etapa 3 (Extração Pontual)**: Uso de operadores estruturais (`site:`, `filetype:`, `intitle:`, `inurl:`) para localizar documentos fonte ou portais canônicos.

---

## 🔍 2. Catálogo Canônico de Operadores de Busca (Search Operators & Dorks)

### A. Operadores Booleanos e Modificadores Básicos

| Operador | Sintaxe | Função e Efeito | Exemplo Prático |
| :--- | :--- | :--- | :--- |
| **Aspas Duplas** | `"termo exato"` | Força correspondência literal exata e ordem exata das palavras. | `"Inbound Marketing"` |
| **Sinal Menos** | `-termo` | Exclui páginas que contenham a palavra ou domínio especificado (sem espaço após o hífen). | `marketing digital -curso -gratis` |
| **OR / Pipe** | `A OR B` ou `A | B` | Retorna resultados que contenham o termo A ou o termo B. | `"kubernetes" OR "k8s"` |
| **Curinga / Wildcard** | `*` | Atua como marcador para uma ou mais palavras desconhecidas na frase. | `"o segredo de * negócios"` |
| **Intervalo Numérico** | `num1..num2` | Busca números, datas ou valores monetários dentro de um intervalo contínuo. | `relatorio seguranca 2023..2025` |

---

### B. Operadores Estruturais e de Metadados

| Operador | Sintaxe | Descrição | Exemplo de Aplicação |
| :--- | :--- | :--- | :--- |
| **`site:`** | `site:dominio.com` | Restringe a pesquisa exclusivamente ao domínio ou TLD especificado (ex: `.gov.br`, `.edu`). | `vulnerabilidades site:gov.br` |
| **`filetype:` / `ext:`** | `filetype:pdf` | Restringe a busca a extensões de arquivos específicas (`pdf`, `xlsx`, `csv`, `docx`, `pptx`, `json`). | `"panorama de dados" filetype:pdf` |
| **`intitle:`** | `intitle:"termo"` | Exige que o termo apareça no título (`<title>`) da página HTML. | `intitle:"relatório anual" mercado` |
| **`allintitle:`** | `allintitle: termo1 termo2`| Exige que todas as palavras listadas estejam presentes no título. | `allintitle: benchmark ia produtividade` |
| **`inurl:`** | `inurl:termo` | Exige que o termo esteja presente no caminho da URL. | `inurl:blog "segurança ofensiva"` |
| **`allinurl:`** | `allinurl: termo1 termo2` | Exige que todas as palavras façam parte da URL. | `allinurl: docs api authentication` |
| **`intext:` / `allintext:`** | `intext:"termo"` | Garante que o termo esteja no corpo do texto (ignorando títulos e URLs). | `intext:"CVE-2024-"` |
| **`related:`** | `related:site.com` | Encontra websites similares ou relacionados tematicamente ao domínio informado. | `related:github.com` |
| **`cache:`** | `cache:site.com` | Exibe a versão salva em cache pelo motor de busca para o endereço. | `cache:exemplo.com/artigo` |

---

### C. Filtros Temporais e Operadores Cronológicos (Google)

- `after:YYYY-MM-DD`: Retorna páginas publicadas ou indexadas após a data especificada.
- `before:YYYY-MM-DD`: Retorna páginas publicadas ou indexadas antes da data informada.
- **Exemplo Combinado**: `incidente seguranca after:2024-01-01 before:2024-12-31`

---

### D. Operadores e Recursos Específicos por Motor de Busca

#### 1. Microsoft Bing
- **`contains:tipo`**: Localiza páginas que contêm links para formatos específicos (`contains:pdf`, `contains:mp4`).
- **`loc:codigo`**: Restringe resultados a países específicos (`loc:br`, `loc:us`).
- **`prefer:termo`**: Aplica peso de relevância superior para determinados termos sem torná-los estritamente obrigatórios.
- **`feed:termo`**: Encontra feeds RSS ou Atom sobre o assunto.

#### 2. DuckDuckGo
- **`!bangs`**: Permite redirecionamento imediato para buscas internas em milhares de serviços (`!g` para Google, `!w` para Wikipedia, `!gh` para GitHub, `!so` para StackOverflow, `!arxiv` para arXiv).
- **Aspas e Menos**: Tratamento estrito de correspondência sem personalização algorítmica ou bolha de filtro (*anti-tracking*).

#### 3. SearXNG & Motores Privados (Mojeek, Startpage)
- Agregação imparcial e busca independente de perfilamento de usuário.
- Sintaxe booleana estrita recomendada (`AND`, `OR`, `NOT`).

---

## 🛠️ 3. Técnicas Heurísticas de Alto Desempenho

### 1. Busca Direta de Documentos Primários e Relatórios
Para obter pesquisas e números concretos sem intermediários:
```text
"termo de pesquisa" (relatório OR survey OR benchmark OR estudo) filetype:pdf site:gov.br OR site:org
```

### 2. Investigação OSINT e Descoberta de Assets Públicos (Google Dorking Ético)
- **Localização de documentações técnicas públicas ou Swagger**:
  ```text
  intitle:"swagger ui" inurl:"/api/v1" "especificação"
  ```
- **Localização de logs ou dumps de diagnóstico**:
  ```text
  filetype:log "exception" intext:"stack trace"
  ```

### 3. Desambiguação Semântica
Se o termo possuir polissemia (ex.: *Java* linguagem vs. *Java* ilha geográfica):
```text
"Java" -programação -software -código -jdk -oracle
```

### 4. Extração de Citações e Origem de Notícias
```text
"frase exata de uma declaração" after:2024-01-01 site:reuters.com OR site:bloomberg.com
```

---

## 📋 4. Protocolo de Resposta do Pesquisador Web

Ao apresentar resultados de pesquisa para o usuário ou outros agentes:
1. **Síntese Executiva**: Resumo direto das respostas encontradas.
2. **Fontes Auditáveis**: Lista com links diretos ou referências de domínios consultados.
3. **Strings de Busca Empregadas**: Exibição explícita dos operadores utilizados para possibilitar reprodutibilidade.
4. **Nível de Confiança e Divergências**: Indicação de consenso ou discrepâncias identificadas entre as fontes.
