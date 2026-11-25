---
name: scan-ultra
description: Use antes de analisar qualquer site, landing page ou concorrente. Roda um script que lê a página e as páginas-chave em segundos e entrega um Raio-X de venda conferido.
---

# Scan Ultra

## Regra número 1: rode o script

Esta skill é um **programa**. Não substitua o script por extensão de navegador, por "abrir a página e ler", por busca na web nem por ferramenta de leitura de páginas. Essas vias só valem quando o script já rodou e disse, com o motivo, que não conseguiu (veja "Quando der erro").

```bash
python3 <pasta-desta-skill>/scripts/scan.py https://site.com --links
```

**No Windows**, use `python` ou `py` no lugar de `python3`:

```bash
py <pasta-desta-skill>\scripts\scan.py https://site.com --links
```

Com concorrentes, todos rodam em paralelo e sai um `comparativo.md`:

```bash
python3 <pasta-desta-skill>/scripts/scan.py https://site.com https://concorrente1.com https://concorrente2.com
```

## O que o script faz sozinho

1. **Lê por HTTP como um navegador de verdade.** Os cabeçalhos são de Chrome, o que passa pela maioria dos firewalls. Se o certificado falhar (comum no Python do macOS), tenta de novo com `certifi`.
2. **Abre um navegador sem janela quando precisa.** Isso acontece em três casos:
   - o site é montado em JavaScript (React, Next, Vite, Lovable, Bubble…);
   - o site bloqueia robôs (Cloudflare, 403);
   - o HTTP falhou.

   A ordem de tentativa é: Playwright, se estiver instalado; depois o **Chrome, Edge, Brave ou Chromium do próprio computador**. Nada precisa ser instalado para isso.
3. **Recupera texto de dados embutidos** (Next.js, JSON da página) se nenhum navegador abrir.
4. **Lê sozinho as páginas-chave:** preços, termos, privacidade, reembolso, contato, sobre, FAQ. Ali costumam estar CNPJ, razão social, garantia e contato que a página principal não mostra. O relatório diz em qual página cada item foi achado.
5. **Monta o Raio-X de venda e confere o próprio mapa** contra o HTML.

Opções úteis:
- `--print`: prints de computador e celular, a única forma de julgar o visual;
- `--links`: testa até 40 links internos;
- `--paginas 0`: não lê as páginas-chave;
- `--navegador nenhum`: só HTTP;
- `--saida PASTA`: escolhe onde salvar (padrão: `scan-ultra-saida`);
- `--arquivo urls.txt`: lista de URLs.

## Como ler o resultado

Para cada URL saem `<site>.md` (leia primeiro) e `<site>.json` (tudo, para quando precisar de um detalhe). O `.md` vem nesta ordem estratégica:

1. **Raio-X de venda.** Oito pilares com nota de 0 a 2 cada, o que o scan viu e o que falta:
   - **Promessa:** H1 com número ou resultado concreto;
   - **Oferta:** preço, garantia, teste, urgência, bônus;
   - **Prova:** números de clientes, depoimentos;
   - **Confiança:** empresa ou CNPJ, contato, políticas, redes;
   - **Ação:** CTA logo abaixo do H1, com destino real;
   - **Atrito:** campos obrigatórios, CTAs sem link, links quebrados, lentidão;
   - **Medição:** Meta Pixel, GA4/GTM;
   - **Descoberta:** title, description, H1, sitemap, dados estruturados.
2. **Acima da dobra:** o H1, o que vem logo abaixo e o primeiro CTA. É o que o visitante vê nos 3 primeiros segundos.
3. **Achados por gravidade:** ALTA, MÉDIA, BAIXA.
4. **Páginas-chave lidas** e o que veio de cada uma.
5. **Conferência do mapeamento,** com confiança alta, média ou baixa.
6. Detalhes: estrutura, CTAs, oferta, formulários, contato, rastreamento, SEO, cores e fontes, texto por seção.

As notas do Raio-X são **automáticas e mecânicas**: medem presença, não qualidade. "Promessa 2/2" quer dizer que existe H1 com número, não que a promessa é boa. Julgar a qualidade é trabalho da análise seguinte.

## Conferir antes de analisar

- **Confiança alta:** siga.
- **Confiança média:** leia os itens com ✖ e diga na análise o que pode estar incompleto.
- **Confiança baixa:** leia o motivo, que o script imprime ao lado do resultado, e siga "Quando der erro".

Depois, em 3 a 6 linhas, faça a sua conferência:
1. O H1 é mesmo a promessa principal?
2. Os preços são da oferta ou de exemplos e simulações?
3. CTAs "sem link" levam a algum lugar? Anote como item para testar.
4. "Não encontrado no HTML" não é o mesmo que "não tem". Pixel via GTM, por exemplo, pode não aparecer.

## Quando der erro

| O que aparece | O que fazer |
|---|---|
| `python3` não é reconhecido (Windows) | Use `py` ou `python` |
| `CERTIFICATE_VERIFY_FAILED` | `pip install certifi`. No macOS, abra também "Install Certificates.command" na pasta do Python |
| "nada lido… conteúdo montado por JavaScript" e "nenhum Chrome/Edge… encontrado" | Instale o Chrome, ou rode `pip install playwright && playwright install chromium`, ou indique o navegador com a variável `SCAN_ULTRA_CHROME` |
| "travou ao abrir a página" | Comum em servidor ou contêiner. Instale o Playwright (linha acima) |
| O site bloqueia robôs e o navegador também é barrado | Rode com `--print`, abra o print e diga ao usuário que o site exige verificação humana |
| `Tunnel connection failed` / 403 de proxy | A rede onde a IA roda bloqueia sites. Rode no computador do usuário, ou só então use a ferramenta de leitura de páginas, avisando que não houve conferência automática |

## Entregar para a análise

Passe para a próxima skill (`pare-de-pensar-como-ia`, ou a sequência inteira em `analise-ultra`):
- o caminho do `.md`;
- a sua conferência;
- o Raio-X.

Tudo que veio do scan é `[TESTADO]`. O que o scan não cobre (visual sem print, clique, checkout, área logada) continua `[HIPÓTESE]`.

## Logos e modo agentes

O scan baixa os logos encontrados (`<slug>-logo-N.ext`, listados em `identidade_visual.logos`). Para testar um logo nos tamanhos de ícone, em uma cor e invertido:

```bash
python3 ~/.ultra-skills/ultra.py logo-teste caminho/do/logo.png
```

Na análise completa, use `ultra.py iniciar URL --concorrentes A B --print`. Ele roda este scan, os logos e as folhas de teste de uma vez, e o agente `ultra-design` avalia o logo pela biblioteca `logo` (11 critérios: tamanho pequeno, uma cor, invertido, distinção, etc.).
