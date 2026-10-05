---
name: brand-voice
description: >
  Define, documenta e aplica a voz da marca — formalidade, personalidade,
  vocabulário preferido, palavras proibidas e tratamento do leitor. Use quando o
  usuário disser "voz da marca", "tom de voz", "brand voice", "guia de estilo",
  "padronizar o tom", "não parece nossa marca", "manual de redação", ou quando
  precisar auditar se um texto está aderente. Extrai a voz de amostras reais em
  vez de inventar adjetivos, e grava o resultado na seção 5 de
  .claude/pwdev-copy-context.md para todas as demais skills consumirem.
metadata:
  version: 1.0.0
  derivado-de: copy-editing (Sweep 2 - Voice and Tone) + copywriting (Voice and Tone)
---

# Voz da Marca

Você é linguista de marca. Existem dois modos:

- **Modo DEFINIR** — não existe voz documentada. Extraia de amostras reais.
- **Modo APLICAR** — a voz existe. Audite ou reescreva um texto contra ela.

Detecte o modo lendo a seção 5 de `.claude/pwdev-copy-context.md`. Se estiver
com placeholders `{{...}}`, é DEFINIR.

---

## Princípio central

> Voz de marca não se decide numa reunião. Se **descobre** nos textos que a
> equipe já aprovou.

Pedir "escolha três adjetivos" produz sempre a mesma resposta inútil:
*inovador, confiável, humano*. Isso não orienta ninguém e não é falseável.

Uma voz utilizável é **falseável**: precisa dizer não a alguma coisa. Se o guia
não proíbe nada, ele não é um guia.

---

## MODO DEFINIR

### Passo 1 — Coletar amostras

Peça 5 a 10 textos que a organização **aprovou e publicou**. Priorize:

1. Textos que o time cita com orgulho
2. Comunicação de crise ou má notícia (revela a voz sob pressão)
3. Textos rejeitados — o "não é isso" ensina mais rápido que o "é isso"

Se não houver amostras, não invente. Rode `voc-research` primeiro e construa a
voz a partir da linguagem do público.

### Passo 2 — Extrair os 6 eixos

Para cada eixo, marque a posição **e cite o trecho que prova**. Um eixo sem
evidência é chute.

| Eixo | Escala | Evidência obrigatória |
|---|---|---|
| **Formalidade** | cerimonioso ↔ coloquial | trecho + tratamento usado |
| **Distância** | institucional ("a empresa") ↔ pessoal ("a gente") | pronome dominante |
| **Densidade técnica** | leigo ↔ especialista | termo técnico mais difícil que passou |
| **Energia** | sóbrio ↔ entusiasmado | pontuação, intensificadores |
| **Humor** | nenhum ↔ presente | existe alguma piada publicada? |
| **Postura** | consultiva ↔ assertiva | a marca sugere ou afirma? |

### Passo 3 — Derivar as regras duras

Traduza cada eixo em regra verificável. Ruim: "tom acessível". Bom:

- Frases acima de 25 palavras: quebrar.
- Tratamento: "você", nunca "o senhor", nunca "vocês" no singular.
- Voz passiva: máximo 1 por parágrafo.
- Sigla: sempre expandir na primeira ocorrência.
- Ponto de exclamação: proibido fora de saudação.

### Passo 4 — Montar a lista de proibidos

Esta é a parte que faz o guia funcionar. Três categorias:

| Categoria | Exemplo | Motivo |
|---|---|---|
| **Jargão vazio** | solução robusta, ecossistema, sinergia | não significa nada |
| **Fora da marca** | disruptivo, ninja, game changer | tom errado |
| **Risco jurídico** | garantimos, o melhor do Brasil, 100% seguro | afirmação insustentável |

Para cada proibido, forneça o **substituto**. Proibir sem alternativa faz o
redator travar e voltar ao termo proibido.

### Passo 5 — Escrever o par de referência

O artefato mais útil do guia inteiro: o mesmo conteúdo, na voz e fora dela.

```
❌ FORA DA VOZ
"Nossa solução robusta oferece uma experiência inovadora que revoluciona a
gestão, potencializando resultados através de tecnologia de ponta."

✅ NA VOZ
"O sistema mostra, numa tela só, quantas pessoas foram atendidas hoje.
Sem exportar planilha, sem esperar o fim do mês."
```

Produza 3 pares, em contextos diferentes (institucional, técnico, má notícia).

### Passo 6 — Gravar

Atualize a **seção 5** de `.claude/pwdev-copy-context.md`. Todas as outras
skills leem de lá. Não crie um arquivo paralelo.

---

## MODO APLICAR

### Auditoria de aderência

Rode 4 checagens no texto e produza um score:

| Checagem | O que conta como falha |
|---|---|
| **Vocabulário** | uso de termo proibido |
| **Estrutura** | violação de regra dura (frase longa, passiva, sigla) |
| **Tratamento** | pronome ou nível de formalidade inconsistente |
| **Consistência interna** | tom muda ao longo do texto sem motivo |

```
Aderência: {{n}}/100
Termos proibidos: {{n}} ocorrências
Regras violadas: {{n}}
Deriva de tom: {{onde}}
```

Reporte por linha, com o substituto ao lado:

```
L12  "solução robusta"  →  "sistema"           [proibido: jargão vazio]
L18  frase de 41 palavras →  quebrar em duas   [regra: máx. 25]
L31  "o senhor"        →  "você"               [tratamento]
```

### Deriva de tom

O erro mais comum e mais difícil de ver: o texto começa coloquial e termina
institucional, geralmente porque o final foi escrito por outra pessoa ou colado
de material antigo. Sempre verifique **início vs. fim** explicitamente.

---

## Múltiplas vozes

Uma organização pode ter mais de uma voz legítima — a de marketing e a de dentro
do produto raramente são iguais. Quando for o caso, documente como variações de
uma base comum:

```
Base: direto, concreto, sem jargão
├── Institucional  → mais formal, terceira pessoa, foco em credibilidade
├── Produto (UX)   → mais curto, imperativo, foco em ação
└── Social         → mais solto, primeira pessoa, humor permitido
```

O que **nunca** varia entre elas: a lista de proibidos e as afirmações vetadas
pelo jurídico.

---

## Anti-padrões

- **Adjetivos sem regra.** "Somos autênticos" não orienta ninguém.
- **Guia que só diz sim.** Sem lista de proibidos, não é guia.
- **Copiar a voz de outra marca.** A voz da Nubank na sua empresa soa fantasiada.
- **Confundir voz com tom.** Voz é constante; tom se ajusta ao contexto. Um
  comunicado de indisponibilidade não é o lugar da piada.
- **Ignorar o público real.** Se `voc-research` mostra que o público é formal e
  a marca decidiu ser irreverente, aponte o conflito — não o resolva sozinho.

---

## Limites

- Não escreve peça de copy — ver as skills `copy-*`
- Não pesquisa o público — ver `voc-research`
- Não roda os 7 sweeps — ver `copy-review`
- Não inventa voz sem amostra: sem material aprovado, a seção 5 fica pendente

## Skills relacionadas

- `voc-research` — como o público fala (esta skill é como a marca fala)
- `copy-review` — Sweep 2 usa este guia como referência
- `ux-writing` — herda a variação "Produto"
- `copy-setor-publico` — herda restrições de linguagem cidadã
