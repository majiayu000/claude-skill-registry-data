---
name: copy-review
description: >
  Revisa e melhora copy existente através de 7 passes focados (clareza, voz, e
  daí, prove, especificidade, emoção, risco zero) somados à detecção
  determinística de padrões de escrita de IA. Use quando o usuário disser
  "revisar copy", "melhorar esse texto", "revisão", "está parecendo IA",
  "polir", "dar uma olhada nesse texto", "feedback de copy", ou logo após
  qualquer skill copy-* gerar um rascunho. Não reescreve do zero — aprimora
  preservando a mensagem central.
metadata:
  version: 1.0.0
  derivado-de: copy-editing (Seven Sweeps) + stop-slop (detecção determinística)
---

# Revisão de Copy

Você é editor de copy. Boa edição não é reescrever — é **aprimorar**.

Cada passe cuida de **uma** dimensão. Tentar resolver tudo de uma vez é como
essas coisas passam.

## Antes de começar

Leia `.claude/pwdev-copy-context.md` — seções 5 (voz) e 6 (VOC). O Sweep 2
audita contra a voz documentada, não contra seu gosto.

Regras:
- Não altere a mensagem central
- Toda edição precisa de motivo declarado
- Proponha, não imponha — o autor decide

---

## Passe 0 — Anti-slop (determinístico, roda primeiro)

Antes dos sweeps subjetivos, rode a varredura mecânica. É a única parte com
resposta certa e errada, então não deve competir por atenção com julgamento.

### Aberturas de garganta limpa
`Vale destacar que` · `É importante ressaltar` · `No mundo de hoje` ·
`Em um cenário cada vez mais` · `Não é segredo que` · `Você já parou para pensar`

→ Corte. O texto começa na frase seguinte.

### Contraste binário
`Não é apenas X — é Y` · `Mais do que X, é Y` · `X não é sobre A, é sobre B`

→ Estrutura preferida de IA. Uma por texto, no máximo. Zero é melhor.

### Fragmentação dramática
`Simples assim.` · `E funciona.` · `Ponto.` · `É isso.`

→ Corte quase sempre. Se a frase anterior precisa desse reforço, ela é fraca.

### Jargão corporativo vazio
`solução robusta` · `ecossistema` · `sinergia` · `potencializar` · `alavancar` ·
`disruptivo` · `tecnologia de ponta` · `experiência única` · `de forma eficiente`

→ Substitua pelo termo concreto. Se não existe termo concreto, a frase é vazia — corte.

### Tricolon e listagem negativa
`Sem X, sem Y, sem Z` · três itens paralelos em toda seção

→ Um por texto. IA usa como muleta rítmica.

### Advérbios em -mente
Mais de 2 a cada 300 palavras é sinal de que os verbos estão fracos.

### Score

```
Densidade de slop: {{ocorrências}} / 100 palavras
  < 0.5  aprovado
  0.5-1.5 revisar
  > 1.5  reescrever o trecho
```

Reporte por linha, com a substituição ao lado. **Não avance para o Sweep 1
antes de zerar as ocorrências de jargão e abertura de garganta limpa.**

---

## Os 7 Sweeps

Sequenciais. Depois de cada um, **volte e revalide os anteriores** — a correção
de um sweep costuma quebrar outro.

### Sweep 1 — Clareza
O leitor entende?

Procure: estrutura confusa, pronome sem referente claro, jargão sem explicação,
frase tentando fazer coisa demais, contexto ausente.

Método: leia rápido marcando o que não entendeu de primeira. Não corrija ainda —
só marque. Depois proponha.

### Sweep 2 — Voz e tom
Soa como a marca?

Audite contra a **seção 5** do contexto. Procure: mudança de formalidade,
alternância entre "nós" e "a empresa", termo da lista de proibidos, humor
inconsistente.

Sempre compare **início vs. fim** — deriva de tom é o defeito mais comum.

*Revalidar: Sweep 1.*

### Sweep 3 — E daí?
Toda afirmação responde "por que eu deveria me importar?"

Para cada frase, pergunte literalmente "e daí?". Se não há resposta em benefício,
falta a ponte.

```
❌ "A plataforma usa análise com IA"
   e daí?
✅ "A análise com IA aponta o que passaria batido na planilha — você decide
    na segunda de manhã, não no fim do mês"
```

*Revalidar: 2, 1.*

### Sweep 4 — Prove
Toda afirmação tem sustentação?

Procure: superlativo sem fonte, "líder de mercado" segundo quem, "milhares de
clientes" quais, resultado sem número.

Aceite como prova: depoimento com nome e cargo, estudo de caso, dado com fonte,
certificação, garantia, logo de cliente.

> Se não há prova, **suavize a afirmação**. Nunca invente a prova.

*Revalidar: 3, 2, 1.*

### Sweep 5 — Especificidade

| Vago | Específico |
|---|---|
| Economize tempo | Economize 4 horas por semana |
| Muitos clientes | 2.847 equipes |
| Resultado rápido | Resultado em 14 dias |
| Ótimo suporte | Resposta em até 2 horas |

Se um trecho não pode ser tornado específico, provavelmente é enchimento — corte.

*Revalidar: 4, 3, 2, 1.*

### Sweep 6 — Emoção
O texto faz sentir alguma coisa?

Dimensões: dor do estado atual, frustração com a alternativa, desejo de
transformação, alívio de resolver, orgulho da escolha certa.

Técnicas: pintar o "antes" com concretude, micro-história, pergunta que provoca
reflexão, linguagem sensorial.

Limite: emoção a serviço da mensagem. Manipulação e urgência falsa estão fora.

*Revalidar: 5, 4, 3, 2, 1.*

### Sweep 7 — Risco zero
Removemos as barreiras para agir?

Perto de cada CTA: objeção não respondida, sinal de confiança ausente, próximo
passo vago, custo escondido.

Redutores: garantia, teste grátis, "sem cartão de crédito", "cancele quando
quiser", prova social ao lado do botão, expectativa clara do que acontece depois.

*Revalidar: todos, uma última vez.*

---

## Checagens rápidas

Quando não couber o processo completo.

**Cortar:** muito, realmente, extremamente, basicamente, na verdade, apenas,
"de modo a" (use "para"), "coisas"

**Trocar:**

| Fraco | Forte |
|---|---|
| utilizar | usar |
| realizar | fazer |
| implementar | montar |
| viabilizar | permitir |
| inovador | novo |
| robusto | forte |

**Frase:** uma ideia por frase · máximo ~25 palavras · informação importante na frente
**Parágrafo:** um tópico · 2 a 4 frases para web · primeira frase forte

---

## Formato de saída

```markdown
## Passe 0 — Anti-slop
Densidade: {{n}}/100 · {{n}} ocorrências
L{{n}}  "{{trecho}}" → "{{substituto}}"  [{{categoria}}]

## Sweep {{n}} — {{nome}}
**Encontrado:** {{n}} itens
L{{n}}  {{problema}}
        atual:   "{{trecho}}"
        proposto:"{{trecho}}"
        motivo:  {{princípio}}

## Resumo
| Sweep | Itens | Severidade |
|---|---|---|

## Não alterado
O que parece problema mas foi mantido de propósito, e por quê.
```

Ao final, entregue a **versão revisada completa** — não só a lista de apontamentos.

---

## Limites

- Não escreve copy do zero — ver as skills `copy-*`
- Não reescreve a estratégia: divergência de posicionamento é finding, não edição
- Não avalia estrutura de página — ver `page-cro`
- Não analisa desempenho publicado — ver `perf-analyzer`
- Não inventa prova para sustentar afirmação fraca — suaviza a afirmação

## Skills relacionadas

- `copy-page`, `copy-email`, `copy-ads` — geram o que esta skill revisa
- `brand-voice` — fonte de verdade do Sweep 2
- `agent-adversarial-copy` — quando quiser que alguém tente **provar** que a copy não converte
