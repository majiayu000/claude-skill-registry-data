---
name: mega-plano
description: Use no fim de uma análise (ou quando pedirem plano de ação em PDF). Reclassifica tudo por prioridade e gera o plano estratégico em PDF, um arquivo para colar em qualquer IA e um checklist.
---

# Mega Plano

## Para que serve

A análise mostra o que está errado. O Mega Plano transforma isso num **produto que se aplica**:
- reorganiza tudo em ações;
- dá nota de prioridade para cada uma;
- entrega o texto pronto de cada ação;
- gera um PDF bonito e um arquivo que a pessoa cola em qualquer IA para aplicar ou corrigir o plano.

Ele não repete a análise. Ele **reclassifica**: cada achado vira ação com dono, semana, métrica e entregável, e a ordem sai da nota, não da ordem em que as coisas foram ditas.

## O que entra

Tudo o que já foi produzido. Na sequência Ultra:
- `01-scan/`
- `02-pessoas.md`
- `03-fundadores.md`
- `04-plano-estrategico.md`

Fora da sequência, qualquer análise ou plano que exista na conversa ou em arquivo.

## Passo 1: escrever o `plano.json`

Siga o formato de `exemplo/plano.json`, nesta pasta. Regras:

- **projeto:**
  - obrigatórios: `nome`, `veredito`, `estrategia_unica`;
  - opcionais: `url`, `publico`, `meta_90_dias`, `resumo`.
- **acoes:** de 8 a 25. Cada uma com:
  - `titulo`: verbo + objeto, curto;
  - `etapa`: tecnico, oferta, site, aquisicao, vendas, identidade, instagram, conteudo, produto ou outro;
  - `semana`;
  - `dono`;
  - `impacto` (1–10): quanto move a meta;
  - `facilidade` (1–10): 10 = faz em uma hora;
  - `evidencia`: TESTADO, EVIDENCIA ou HIPOTESE, a mesma marcação da `pare-de-pensar-como-ia`;
  - `porque`: com a prova;
  - `passos`: lista;
  - `entregavel`: **o texto pronto**, como copy, e-mail, script ou instrução exata. Nunca "melhorar X";
  - `metrica` e `meta`;
  - `prompt_ia` é opcional: se ficar vazio, o script gera.
- **ofertas, ativos, paleta, conteudo, metricas, suposicoes, fontes:** copie do plano estratégico. Na paleta, marque a cor de destaque com `"destaque": true`. Ela vira a cor de acento do PDF.

Dê notas honestas. Ação com impacto alto e evidência HIPOTESE fica abaixo de uma com evidência TESTADO, e isso é proposital.

## Passo 2: gerar

No Windows, troque `python3` por `py`.

```bash
python3 <pasta-desta-skill>/scripts/gerar.py plano.json --validar          # confere antes
python3 <pasta-desta-skill>/scripts/gerar.py plano.json --saida plano-final
```

Se a validação apontar erro, corrija o JSON e rode de novo. A mensagem diz o campo exato.

**A reclassificação:**
- **ICE** = impacto × confiança × facilidade ÷ 10.
- **Confiança** vem da evidência: TESTADO 9, EVIDENCIA 7, HIPOTESE 4.
- **Quadrantes:**
  - FAÇA AGORA: impacto ≥ 6 e facilidade ≥ 6;
  - PROJETO: impacto ≥ 6 e facilidade < 6;
  - RÁPIDO: impacto < 6 e facilidade ≥ 6;
  - REPENSAR: o resto.
- As ações são ordenadas por quadrante e depois por ICE.

**O que sai:**
- `plano-de-acao.pdf`:
  - capa com veredito e estratégia;
  - como usar;
  - matriz de prioridade;
  - roteiro semana a semana;
  - cada ação com passos, entregável pronto e métrica;
  - ofertas, ativos para copiar, paleta com amostras, conteúdo, métricas, suposições;
  - checklist e fontes.
- `plano-para-ia.md`: instruções para a IA + o plano inteiro + o JSON. A pessoa cola em qualquer IA e diz "aplique A01" ou "corrija o plano: [dado novo]".
- `plano.json`: versão normalizada com as notas. Edite e gere de novo: as prioridades se recalculam.
- `checklist.csv`: para Trello, Notion, Sheets ou ClickUp.
- Sem `reportlab` instalado, sai `plano-de-acao.html`: é só abrir e usar Imprimir → Salvar como PDF. Para PDF direto: `pip install reportlab`.

## Passo 3: conferir antes de entregar

1. Abra o PDF ou renderize as primeiras páginas. Veja se a capa, a matriz e uma ação estão legíveis.
2. As 3 primeiras ações (o "Top 3" que o script imprime) fazem sentido como primeiro passo? Se não, as notas estão erradas. Ajuste e gere de novo.
3. Algum `entregavel` ficou genérico? Reescreva com o detalhe do negócio.

## Entrega

Entregue o PDF, o `plano-para-ia.md` e o `checklist.csv`. Diga numa linha qual é a primeira ação e por quê.

## Modo agentes

Depois de uma análise com agentes, o `plano.json` sai pronto do motor. Ele junta as ações de todos os conselhos, ordenadas por ICE e sem repetidas, a oferta campeã e as entregas de cada etapa:

```bash
python3 ~/.ultra-skills/ultra.py plano PASTA-DA-ANALISE --pdf
```

Confira o `06-plano/plano.json` antes de entregar: entregáveis vazios, ação sem métrica, hipótese no topo da ordem. Se mexer no arquivo, rode o `gerar.py` de novo.
