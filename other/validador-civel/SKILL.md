---
name: validador-civel
description: "Gate anti-alucinacao do plugin civel: valida vigencia e existencia de dispositivo, sumula, tese, tema e enunciado ANTES de qualquer citacao entrar em peca. Cruza com context/ (CPC/CC + reformas + jurisprudencia) e, na duvida, exige checagem ao vivo (fetch real) ou bloqueia. Integra o guard global anti-alucinacao-juridica. Use antes de citar qualquer fundamento, ou quando o operador disser valida essa jurisprudencia, esse artigo existe, essa sumula esta vigente, esse tema/acordao existe, confere essa ementa, antes de citar, esse dispositivo ainda esta em vigor, checa esse fundamento."
---

# VALIDADOR-CIVEL — Gate anti-alucinacao (dispositivos + jurisprudencia)

> Camada 1 (Fundacao). Trava de seguranca. Nenhuma citacao — legal ou jurisprudencial — entra em peca sem passar por aqui. Distinto da `suprema-corte-civel` (gate final da peca inteira): este valida cada CITACAO.

## Anexos obrigatorios (context/)
- `context/cpc-13105-15.md` e `context/cc-10406-02.md` — conferir existencia/redacao de artigo (grep do artigo + ler faixa; nao ler inteiro).
- `context/cpc-cc-alteracoes-recentes.md` — conferir vigencia/reforma (Lei 14.879/2024 foro art. 63; Lei 14.939/2024 feriado local art. 1.003; EC 136/2025 = precatorios, nao CPC; PL 4/2025 NAO e lei).
- `context/jurisprudencia-civel.md` — corpus com selos ✅/🟡/❌.
- `context/metodologia-civel.md` — quando chamada pelo `civel-master`.

## Objetivo
Impedir que qualquer dispositivo, sumula, tese, tema, enunciado ou acordao **inexistente, revogado, alterado ou nao verificado** entre numa peca. Veredito binario por citacao: **VALIDADO** ou **BLOQUEADO**.

## Quando ativar
- Antes de inserir qualquer citacao numa peca/recurso/parecer.
- O operador pede para conferir um artigo, sumula, tema, acordao ou ementa.
- Outra skill propos um fundamento e precisa do sinal verde antes de redigir.

## Metodologia
1. **Dispositivo de lei (CPC/CC):**
   - grep do artigo no anexo (`^Art\. 300\.` no CPC; `^Art\. 206` no CC) e ler a faixa — o numero/redacao **existe**?
   - cruzar com `cpc-cc-alteracoes-recentes.md` — esta **vigente** e nao foi alterado? (foro 63, feriado 1.003). EC 136/2025 NAO mexe no CPC. **PL 4/2025 nunca como lei.**
2. **Jurisprudencia (sumula/tema/tese/enunciado/acordao):**
   - achar no corpus `jurisprudencia-civel.md`. **✅** → VALIDADO; **🟡** → so VALIDADO apos conferir inteiro teor ao vivo; **❌/nao consta** → busca ao vivo obrigatoria.
   - **busca ao vivo:** `WebSearch`/`WebFetch` nativos (Firecrawl/Perplexity fallback) na fonte oficial (STJ/STF/CJF/tribunal). So VALIDADO se a pagina **abrir** e o trecho/tese **constar** la, com link.
3. **Veredito por citacao:** VALIDADO (com fonte) ou BLOQUEADO (motivo: inexistente / revogado / alterado / nao verificavel / divergencia nao resolvida). Na duvida → BLOQUEADO.
4. **Acionar o guard global** `anti-alucinacao-juridica` em paralelo (camada autossuficiente, independente do cwd).

## Entrega obrigatoria final
- Lista de citacoes com veredito (VALIDADO/BLOQUEADO) + fonte/ponteiro + motivo do bloqueio. Versao corrigida das citacoes que passam; as bloqueadas saem da peca. Se houver reforma incidente, apontar a redacao vigente correta.

## Guard
Default no incerto e **BLOQUEAR**. Nada inventado, nada revogado, nada 🟡 sem conferencia, nada ❌. Sem fonte real aberta, nao valida. Trabalha junto com `jurisprudencia-civel`, com o guard global `anti-alucinacao-juridica` e entrega para a `suprema-corte-civel` (R2 fundamentacao vigente · R3 jurisprudencia real).
