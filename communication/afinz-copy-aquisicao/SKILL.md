---
name: afinz-copy-aquisicao
description: Redige a copy de comunicações de aquisição de cartão da Afinz (WhatsApp,
  SMS, Push, e-mail) para qualquer combinação de BU (B2C, B2B2C, Plurix), Parceiro,
  Segmento e Oferta — e roteia o resultado pro formato certo do sistema real de destino.
  Para e-mail, produz a copy já no formato de linha de `TB_BRIEFING_CAMPANHA_AQUISICAO`
  (o motor de e-mail dinâmico do SFMC); para WhatsApp/SMS/Push, produz a copy pronta
  pra colar na ferramenta de disparo, já que hoje não existe um motor dinâmico equivalente
  pra esses canais. NÃO é a skill que sobe o CSV no SFMC (isso é `emails-dinamicos-sfmc`)
  nem a que reconcilia template_id×activity_name no módulo Comunicações do GaaS (isso
  é `gaas-governanca-comunicacoes`) — esta skill só escreve o texto persuasivo, com
  o contexto certo montado automaticamente. Use quando o usuário pedir pra escrever,
  redigir, criar copy, criar mensagem de disparo, ou revisar comunicação de aquisição
  — mesmo que ele só diga "escreve um WhatsApp pra Repescagem" sem citar todos os
  detalhes.
metadata:
  version: 1.0.0
  origin: claude-projeto
  agents:
  - claude-code
  - codex
  - cowork
  - chatgpt
  process:
  - Comunicações
  owner: Time GaaS Afinz
  last_validated: null
  packaged_at: '2026-10-30'
  compatibility: Instruções portáveis; execução não validada por ambiente
  license: Distribuição pública autorizada pelo titular; sem concessão adicional de
    licença
---

# ✍️ Afinz Copy Aquisição — Motor de Comunicação Contextual

## O que essa skill é (e o que não é)

Um "compilador de prompt de copywriting": monta o contexto certo (segmento, parceiro, marca, canal, compliance) sozinha, a partir das fontes de verdade do projeto, e só depois escreve. **Não escreve direto em nenhum banco e não sobe nada em SFMC** — quem faz isso são `emails-dinamicos-sfmc` (upload do CSV de briefing) e `gaas-governanca-comunicacoes` (reconciliação template_id×activity_name). Esta skill entrega o *conteúdo*; as outras duas cuidam do *encanamento*. Sempre deixe claro pro usuário qual das duas ele ainda precisa acionar depois.

**Duas famílias de destino — não são a mesma coisa:**

1. **E-mail → motor dinâmico do SFMC.** Existe **um único** e-mail no Content Builder; toda campanha nova é 1 linha na Data Extension `TB_BRIEFING_CAMPANHA_AQUISICAO` (36 colunas fixas), casada por chave composta `NM_PRODUTO_INTERNO`/`TP_CAMPANHA`/`SEQUENCIA` com a audiência. **Não invente as 36 colunas aqui** — leia `.claude/skills/emails-dinamicos-sfmc/SKILL.md` (se disponível no repositório) antes de formatar a saída para e-mail. Regras não-negociáveis vindas de lá: personalização é `%%=v(@FirstName)=%%` (nunca `%%FIRST_NAME%%`), quebra de linha é `<br>` (nunca `\n` cru), e a chave composta tem que bater caractere a caractere com o que já existe no briefing atual — não gere uma linha sem antes perguntar se a combinação já existe.
2. **WhatsApp / SMS / Push → sem motor dinâmico centralizado hoje.** Diferente do e-mail, não existe uma Data Extension de briefing equivalente pra esses canais (confirmado lendo os SKILL.md reais do repositório em 2026-08-12). A copy sai pronta pra colar na ferramenta de disparo (WhatsApp Business Manager, plataforma de SMS, etc.), e o usuário decide onde publicar. Depois de rodar, a peça só entra no catálogo `communication_templates`/`communication_slots` do GaaS via screenshot + `gaas-governanca-comunicacoes` — isso é pós-fato, não faz parte do fluxo desta skill.

**Fontes de verdade — leia antes de escrever, nesta ordem:**

1. `03_SEGMENTOS_ESTRATEGIAS.md` (projeto AFINZ) — regras de tom por segmento/etapa de funil, com exemplos ✅/❌ prontos para Repescagem, Upgrade, Abandonados e Instabilidade.
2. Skill `growth-brain-intelligence-engine` — dicionário de taxonomia (BU, Parceiro, Canal, Público, Período) e tabela de "Parceiros e perfis típicos". **Não duplique essas tabelas aqui.**
3. Vault Obsidian, se conectado (`Afinz-CRM-Midia-Vault/03-Dimensoes/`) — definições estáveis de Segmentos/Parceiros/BUs/Canais/Ofertas. **Trate os números como possivelmente defasados** (as notas de dimensão têm cadência de reidratação 2x/semana definida mas nem sempre cumprida — confira a data `atualizado:` no frontmatter antes de confiar num número específico; para CAC/conversão atual, prefira consultar o Supabase ao vivo via as queries de `09-Inteligencia-IA/Runbook-Vault-Vivo.md` a citar o snapshot da nota).
4. `references/parceiros.md` (nesta skill) — registro complementar só para parceiros que não estão em nenhuma fonte acima.
5. `references/exemplos_reais.md` (nesta skill) — padrões de copy observados em comunicações reais (CTA duplo, nomenclatura de produto por BU, campos de personalização por canal, hooks de oferta). Consulte antes de escrever pra não reinventar um padrão que já existe e funciona.
6. `references/reguas_taxonomia.md` (nesta skill) — estrutura conhecida de réguas (segmento × canais praticados × nº de disparos) e taxonomia de variantes de público (Institucional/Serasa/Ecred/Negados/Upgrade). **Consulte sempre que o pedido for uma régua** (várias peças ao longo do tempo para um segmento), não uma peça avulsa — ver Passo 3.5.
7. `.claude/skills/gaas-governanca-comunicacoes/references/taxonomia_marcas.md`, se disponível — convenção de prefixo de `template_id` por marca (`b2c_`/`dia_`/`bb_` → família Afinz; `plurix_` → Plurix). Use isso ao sugerir Activity Name/template_id no fim da saída, pra não gerar algo que a governança marcaria como `suspeito`.
8. `GuiaDeMarca_Afinz_Institucional_2024...pdf` — identidade visual e voz institucional por BU.

Se qualquer uma dessas fontes tiver sido atualizada desde a última vez, releia — não confie em memória de conversas anteriores.

---

## Fluxo de trabalho

### Passo 1 — Coletar o briefing mínimo

Pergunte (ou infira do pedido) o que faltar:

| Campo | Obrigatório | Se não informado |
|---|---|---|
| BU | Sim | Perguntar — muda voz, cor institucional e disclaimers |
| Parceiro | Se aplicável | "Proprietária"/Institucional se não houver parceiro externo |
| Segmento | Sim | Não dá pra calibrar tom sem saber a etapa de funil |
| Canal | Sim | Determina qual das duas famílias de destino se aplica (ver acima) |
| Oferta | Recomendado | Checar se é Vibe ou Padrão — Vibe é a oferta dominante hoje e, a partir de 17/08/2026, passa a orientar a comunicação de Aquisição/Rentabilização/Branding por decisão de negócio (ver `Afinz-CRM-Midia-Vault/03-Dimensoes/Vibe.md`, se disponível) |
| Objetivo/CTA | Recomendado | Inferir da etapa de funil (ver tabela abaixo) |

Não trave o fluxo pedindo tudo de uma vez — se o pedido já der pra inferir 80%, preencha o resto com o padrão mais provável e sinalize a suposição no início da resposta.

### Passo 2 — Montar o contexto (a parte "auto-prompt")

1. **Segmento → tom.** Busque o segmento em `03_SEGMENTOS_ESTRATEGIAS.md`. Se tiver bloco "Copy Guidelines" (✅/❌), siga à risca. Se não tiver (CRM, Base_Proprietaria, Leads_Parceiros, Cartonistas), derive da etapa de funil:
   - **Topo** (Base_Proprietaria, CRM): educar, não pressionar, copy institucional.
   - **Meio** (Repescagem, Upgrade, Leads_Parceiros): reativar com prova/urgência moderada.
   - **Fundo** (Abandonados, Instabilidade): urgência real, facilitação máxima, tom direto.

2. **Parceiro → contexto de co-branding.** Verifique o parceiro na tabela da skill `growth-brain-intelligence-engine` primeiro. Se não estiver lá, cheque `references/parceiros.md`. Se não existir em lugar nenhum, siga o [Passo 4](#passo-4--parceiro-novo-registrar-antes-de-escrever).

3. **BU → identidade.** B2C = azul, tom direto ao consumidor. B2B2C = verde, comunicação via parceiro comercial (credenciais do parceiro aparecem primeiro). Plurix = roxo, "Cartão [Loja] + Afinz" como posicionamento (nunca só "Afinz").

4. **Canal → destino e formato.** Ver [Duas famílias de destino](#o-que-essa-skill-é-e-o-que-não-é) e [Limites por Canal](#limites-por-canal-diretrizes-práticas).

5. **Compliance → checklist.** Ver [Checklist de Compliance](#checklist-de-compliance) antes de finalizar.

### Passo 3 — Escrever

Gere **2 a 3 variações** quando o usuário não pedir uma quantidade específica. Cada variação varia o gancho (benefício vs. urgência vs. prova social/limite), não é paráfrase.

Use variáveis dinâmicas do Framework quando fizer sentido: `%%NOME%%`, `%%LIMITE_CRD%%`, `%%DIAS_ABANDONADO%%`, `%%LINK_CONTINUAR%%` para WhatsApp/SMS/Push (ver `03_SEGMENTOS_ESTRATEGIAS.md` seção 4.1). **Para e-mail, a sintaxe é outra** — `%%=v(@FirstName)=%%` — não misture as duas.

### Passo 3.5 — Quando o pedido é uma RÉGUA, não uma peça avulsa

Se o usuário pedir várias peças ao longo do tempo pra um segmento ("me dá uma régua de X", "monta os disparos de Y"), não trate como N pedidos avulsos independentes. Antes de escrever:

1. Consulte `references/reguas_taxonomia.md` — se o segmento estiver lá, você já sabe quantos disparos, quais canais são praticados e se existem sub-jornadas (ex.: Carrinho Abandonado não é uma régua só — são 3, com propósitos diferentes). Ofereça essa estrutura conhecida em vez de perguntar do zero.
2. Pergunte/confirme: quais canais desta régua o usuário quer cobrir agora (sugerindo os já praticados), e quais variantes de público entram (Institucional/Serasa/Ecred/etc., se o segmento tiver essa divisão).
3. Para cada combinação canal × disparo × variante, gere copy coerente com a progressão esperada (ex.: disparo 1 mais neutro → disparo final com urgência/fechamento, se o padrão real observado em `references/exemplos_reais.md` sustentar isso — não invente uma progressão sem lastro).
4. Feche sinalizando quais combinações têm exemplo real por trás (mais confiança) e quais foram geradas sem precedente direto no dataset (menos confiança) — não apresente as duas com o mesmo nível de certeza.
5. Se o segmento pedido não estiver em `references/reguas_taxonomia.md`, diga isso explicitamente e pergunte a estrutura em vez de estimar quantos disparos/canais ele deveria ter.

### Passo 4 — Parceiro novo: registrar antes de escrever

Se o usuário citar um parceiro que não está em nenhuma fonte do Passo 2.2, **não invente o tom**. Pergunte:

1. BU de atuação (B2C, B2B2C ou Plurix)
2. Tipo (base própria / bureau de crédito / rede varejista / outro)
3. Restrição de marca (ex: sempre citar nome da loja antes de "Afinz")
4. Segmento(s) típico(s)

Depois, **acrescente uma linha em `references/parceiros.md`** (edite, não recrie do zero) e avise o usuário.

---

## Limites por Canal (diretrizes práticas)

| Canal | Referência prática | Observação |
|---|---|---|
| **SMS** | ~160 caracteres por segmento (GSM-7) | Emoji/acento reduz para ~70/segmento |
| **WhatsApp** | Corpo curto, 2–4 linhas | Mensagens de template (Marketing/Utility) têm aprovação prévia — não assumir liberdade total de texto |
| **E-mail** | Assunto ≤ 45–60 caracteres | Pré-header ~35–90 caracteres. Corpo entra nos campos `TITULO_COPY_1_AZUL`/`COPY_1_PRETO`/`TITULO_COPY_2`/`COPY_2_PRETO` da DE de briefing — ver `emails-dinamicos-sfmc` |
| **Push** | Título ≤ 50 caracteres, corpo ≤ 150 caracteres | Varia por iOS/Android — tratar como teto |

Confirme limites exatos com o provedor real em uso — estes são ponto de partida.

---

## Checklist de Compliance

**Isto não é aconselhamento jurídico.** Antes de considerar a copy pronta pra sair:

- [ ] Se menciona taxa, parcelamento ou "sem juros", verificar se precisa de CET junto
- [ ] Se o segmento é Repescagem/Negados, **nunca** expor histórico de rejeição
- [ ] Se o segmento é Upgrade (já aprovado), não usar "sujeito a análise"
- [ ] Confirmar com jurídico/compliance da Afinz antes do disparo em produção

---

## Formato de Saída

### Para WhatsApp / SMS / Push

```
BRIEFING ASSUMIDO
BU: [...] | Parceiro: [...] | Segmento: [...] | Etapa: [Topo/Meio/Fundo] | Canal: [...] | Oferta: [...]
(sinalizar campos inferidos, não informados pelo usuário)

VARIAÇÃO 1 — [gancho]
[texto, com %%VARIAVEL%% quando aplicável]

VARIAÇÃO 2 — [gancho diferente]
[...]

RATIONALE
[por que esse tom/gancho — ligar a CAC/conversão/temperatura do segmento]

CHECKLIST DE COMPLIANCE
[itens relevantes]

NOME SUGERIDO DE ACTIVITY (taxonomia)
{empresa}_{area}_{parceiro}_{tipo_comunicação}_{canal}_{publico}_{descricao}_{periodo}
(dicionário de siglas da skill growth-brain-intelligence-engine; conferir prefixo × marca em taxonomia_marcas.md antes de fechar)

PRÓXIMO PASSO
Esta copy ainda não está em nenhum sistema. Publicar direto na ferramenta do canal;
depois do disparo, vira candidata a entrar no catálogo via gaas-governanca-comunicacoes.
```

### Para E-mail (SFMC)

```
BRIEFING ASSUMIDO
[igual acima]

LINHA PROPOSTA PARA TB_BRIEFING_CAMPANHA_AQUISICAO
NM_PRODUTO_INTERNO: [...] | TP_CAMPANHA: [...] | SEQUENCIA: [...]
(⚠️ conferir com o usuário se essa combinação de chave já existe no briefing atual antes de considerar pronta)

ASSUNTO: [...]
PRE_CABECALHO: [...]
TITULO_COPY_1_AZUL / COPY_1_PRETO: [...]
TITULO_CTA_1 / LINK_CTA_1: [...]
TITULO_COPY_2 / COPY_2_PRETO: [...] (se aplicável)
TITULO_CTA_2 / LINK_CTA_2: [...] (se aplicável)
NOTA_LEGAL: [...]

RATIONALE
[...]

CHECKLIST DE COMPLIANCE
[...]

PRÓXIMO PASSO
Esta linha ainda não foi validada contra as 36 colunas oficiais nem subida. Passar para a
skill emails-dinamicos-sfmc (ou o operador humano) pra montar o CSV completo, checar
duplicidade de chave e formato de data antes do import no SFMC.
```

---

## Regras Inegociáveis

❌ Nunca escreva copy para um segmento sem checar se `03_SEGMENTOS_ESTRATEGIAS.md` já tem regra ✅/❌ documentada.
❌ Nunca invente perfil de parceiro novo sem perguntar — siga o Passo 4.
❌ Nunca prometa taxa/condição sem sinalizar a exigência de CET.
❌ Nunca duplique as 36 colunas do briefing SFMC, o dicionário de taxonomia da growth-brain, ou as tabelas de dimensão do vault — referencie as fontes.
❌ Nunca apresente a copy de e-mail como "pronta pra subir" sem passar pelo checklist de `emails-dinamicos-sfmc` (chave duplicada, sintaxe de personalização, formato de data).
❌ Nunca confunda esta skill com `gaas-governanca-comunicacoes` (essa reconcilia template_id×activity_name já existentes; não escreve copy nova).

✅ Sempre gere 2-3 variações com ganchos diferentes.
✅ Sempre sinalize campos assumidos/inferidos no início da resposta.
✅ Sempre feche com o checklist de compliance e o "próximo passo" (qual skill/humano assume depois desta).
