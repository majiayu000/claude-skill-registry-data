---
name: emails-dinamicos-sfmc
description: Monta, valida e sobe linhas de CSV para o motor de e-mail dinâmico do
  Content Builder no SFMC (Salesforce Marketing Cloud) — o par de Data Extensions
  TB_CAMPANHA_AQUISICAO (audiência) + TB_BRIEFING_CAMPANHA_AQUISICAO (conteúdo), casadas
  por AMPscript via chave composta PRODUTO/TP_CAMPANHA/SEQUENCIA. Use quando o usuário
  pedir para criar/testar uma campanha de e-mail dinâmico, gerar linha de briefing
  a partir de um xlsx de analista de mkt, diagnosticar erro de importação de Data
  Extension ("Data inválida", "arquivo inválido", "briefing não encontrado"), ou perguntar
  como funciona o motor de e-mails dinâmicos. NÃO é sobre o módulo interno "Comunicações"
  do GaaS (template_id/af_sub3, communication_templates) — isso é escopo de `gaas-governanca-comunicacoes`.
metadata:
  version: 1.0.0
  origin: claude-projeto
  agents:
  - claude-code
  - codex
  - cowork
  - chatgpt
  process:
  - SFMC
  owner: Time GaaS Afinz
  last_validated: null
  packaged_at: '2026-10-30'
  compatibility: Instruções portáveis; execução não validada por ambiente
  license: Distribuição pública autorizada pelo titular; sem concessão adicional de
    licença
---

# Emails Dinâmicos SFMC (Content Builder + AMPscript)

Motor único de e-mail no Content Builder do SFMC que resolve seu conteúdo via
`LookupOrderedRows` numa Data Extension de briefing, em vez de existir um e-mail por
campanha. Toda campanha nova = 1 linha em cada uma de duas planilhas, não um e-mail novo.
Detalhes de arquitetura e o caso de validação real (Plurix, 2026-08-10) estão em
`Afinz-CRM-Midia-Vault/04-Operacao/Emails-Dinamicos-SFMC.md` — leia essa nota primeiro se
precisar do contexto completo; este SKILL.md é o guia operacional de "como montar/subir".

## As 3 peças

1. **`TB_CAMPANHA_AQUISICAO`** (audiência, quem recebe) — `CPF, PRI_NOME, EMAIL, CELULAR,
   LOCAL, LIMITE, PRODUTO, TP_CAMPANHA, SEQUENCIA, CAMPANHA`. No contrato documental
   corrigido em 19/08/2026, **CPF é chave primária e há uma linha por pessoa**;
   `SEQUENCIA` avança in-place por `Update Contact`. Não carregar duplicatas por toque.
   Confira a configuração da DE e a leitura da sequência atual antes de operar: o
   Journey Builder pode preservar os dados de entrada. Ver `Emails-Dinamicos-Plurix.md` §12.
2. **`TB_BRIEFING_CAMPANHA_AQUISICAO`** (conteúdo, o que é enviado) — 36 colunas fixas (ver
   lista completa abaixo). Cada linha é um e-mail inteiro.
3. **E-mail dinâmico** no Content Builder (ex.:
   `afz_car_vis_aqs_email_anc_joraquisicaotestedinamicoseq1_diario`) — o motor, não mexe
   nele para criar campanha nova.

## A chave composta — regra inegociável

`PRODUTO` (audiência) = `NM_PRODUTO_INTERNO` (briefing) · `TP_CAMPANHA` = `TP_CAMPANHA` ·
`SEQUENCIA` = `SEQUENCIA`. Idêntico caractere a caractere (maiúscula/acento) nos dois
arquivos, senão o AMPscript dá `RaiseError("Dados de briefing da campanha não
encontrados.")`. Mais: `DT_INICIO`/`DT_FIM` do briefing precisam cobrir a data de hoje,
senão `RaiseError("Campanha fora do prazo de vigência.")`.

Antes de gravar uma linha nova, **cheque se essa combinação já existe** no briefing atual
— duas linhas com a mesma chave é ambíguo (`LookupOrderedRows` desempata por `DT_INICIO
DESC`, não confie nisso de propósito).

## Workflow — montar uma campanha nova a partir de um xlsx de analista

1. **Ler o xlsx por nome de coluna, nunca por posição.** Analistas de mkt reordenam/removem
   colunas entre campanhas (já aconteceu: a aba de um parceiro veio sem a coluna "Título
   Copy 1 - Azul", desalinhando tudo se copiado por índice).
2. **Resolver todo placeholder antes de gerar o CSV**: `"PEGAR NA BASE"` em produto,
   `"CRIAR"` em código de campanha — não travam o CSV tecnicamente, mas quebram o lookup
   silenciosamente. Perguntar ao operador o valor real se não for óbvio pelo contexto
   (ex.: produto já cadastrado na audiência).
3. **Corrigir sintaxe de personalização.** Único formato válido dentro dos campos de
   texto: `%%=v(@FirstName)=%%` (resolvido por `TreatAsContent()`). `%%FIRST_NAME%%` ou
   `%%first_name%%` são de outro mecanismo (Triggered Send/Journey merge field) e **não
   funcionam aqui** — vazam texto literal pro cliente. Isso já apareceu na planilha-modelo
   da analista, não só em campanhas pontuais — sempre conferir, mesmo em copy que parece
   "copiada de campanha que já funcionou".
4. **Nunca deixar quebra de linha crua (`\n`) num campo.** Trocar por `<br>` (o CSS de
   `Copy1Preto`/`Copy2Preto` já tem `white-space: pre-line`, então `<br>` renderiza igual
   ao `\n` pretendido — mas sem quebrar a contagem de linhas físicas do CSV no importador).
5. **Campo sem slot no template = decisão explícita, não perda silenciosa.** O template só
   tem 1 imagem de topo (`HEADER`). Se a analista mandar "Logo" + "Header" separados, avisar
   e perguntar: usar só um, ou abrir o AMPscript pra adicionar um segundo slot (ver seção
   "Adicionar campo/slot novo" abaixo)?
6. **Gerar o CSV** com delimitador `,` (vírgula — não `;`), sem BOM, CRLF e
   `QUOTE_MINIMAL`. Este é o contrato confirmado por comparação com um arquivo baixado
   da própria DE do SFMC em 03/09/2026. Campos que contêm vírgula precisam permanecer
   entre aspas duplas.
7. **Formatar as datas de importação como `MM/DD/AAAA HH:mm:ss`**. A DE exporta datas
   localizadas em DD/MM, mas o wizard desta BU valida a entrada como English (United States).
   Ex.: 31 de agosto de 2026 = `08/31/2026 00:00:00`.
8. **Entregar 1 arquivo só com a(s) linha(s) nova(s)** quando o operador só quer
   `Adicionar e Atualizar` (não mexe no resto da DE); só gerar o arquivo completo
   (linhas antigas + novas) se for `Overwrite` explícito e confirmado.

## As 36 colunas do briefing (ordem oficial)

```
DT_INICIO, DT_FIM, UTM_CAMPANHA, TP_CAMPANHA, SEQUENCIA, ASSUNTO, PRE_CABECALHO, HEADER,
CARTAO_NM_COMERCIAL, NM_PRODUTO_INTERNO, TITULO_COPY_1_AZUL, COR_COPY_1,
TAMANHO_DA_FONTE_TITULO_COPY_1, TITULO_CTA_1, LINK_CTA_1, COPY_1_PRETO, COR_COPY_PRETO_1,
TAMANHO_DA_FONTE_TITULO_COPY_PRETO_1, TITULO_COPY_2, COR_TITULO_COPY_2,
TAMANHO_DA_FONTE_TITULO_COPY_2, COPY_2_PRETO, COR_COPY_2, TAMANHO_DA_FONTE_COPY_2,
TITULO_CTA_2, LINK_CTA_2, BANNER_1_CORPO, LINK_BANNER_1_CORPO, BANNER_2_CORPO,
LINK_BANNER_2_CORPO, BANNER_3_CORPO, LINK_BANNER_3_CORPO, NOTA_LEGAL, COR_NOTA_LEGAL,
TAMANHO_DA_FONTE_NOTA_LEGAL, RODAPE
```
Não existe "Copy 3" nem "Logo" separado neste template — se a planilha da analista tiver
essas colunas, é gap de template (ver item 5 do workflow) ou sobra da planilha-modelo dela
que não se aplica aqui.

## Pitfalls confirmados (cada um já causou um import falho real)

1. **Formato de data.** O arquivo baixado da DE usa **DD/MM/AAAA**, mas o wizard desta BU
   interpreta a importação como **MM/DD/AAAA**. Exportar do GaaS em MM/DD. Evidência:
   56 linhas com `17/08/2026` geraram exatamente 56 erros "Data inválida" em 03/09/2026.
2. **Checkbox "Respeitar as aspas duplas como qualificadores de texto"** some a cada nova
   importação (não é lembrada). Sem ela marcada, qualquer vírgula dentro de um campo quebra
   a contagem de colunas — geralmente derruba **todas** as linhas do arquivo de uma vez.
3. **Quebra de linha crua dentro de campo quoted** é CSV válido (RFC4180) mas o importador
   do SFMC conta linha física — vira "arquivo inválido". Ver item 4 do workflow.
4. **Placeholder não resolvido** (`PEGAR NA BASE`, `CRIAR`) sobe sem erro técnico e quebra
   o lookup depois, silenciosamente.
5. **A Jornada tem filtro de entrada próprio, independente da chave do briefing.** CSVs
   100% corretos não disparam nada se nenhuma jornada ativa filtrar aquele
   `TP_CAMPANHA`/`SEQUENCIA`. Sempre perguntar/confirmar isso antes de considerar uma
   campanha "pronta pra produção" (não bloqueia o **teste** via Test Send, só o disparo
   automático real).

## Como testar

- **Rápido, sem depender de jornada:** Content Builder → e-mail → "Visualizar e testar" →
  Test Send, escolhendo o `CPF` na DE de audiência. Valida renderização e personalização.
- **Fluxo completo (jornada real):** confirmar/criar jornada com filtro de entrada batendo
  `TP_CAMPANHA` + `SEQUENCIA` da campanha (pitfall #5).

## Adicionar campo/slot novo ao template (ex.: um 2º slot de imagem)

1. Content Builder → e-mail → **Visualização de código**.
2. Adicionar `SET @NovoCampo = Field(@Row, "NOME_COLUNA")` junto dos outros `SET` na seção
   "Atribuição dos demais Campos do Briefing".
3. Adicionar o bloco HTML condicional `%%[ IF NOT EMPTY(@NovoCampo) THEN ]%% ... %%[ ENDIF ]%%`
   no ponto certo do layout.
4. Contact Builder → `TB_BRIEFING_CAMPANHA_AQUISICAO` → Propriedades → Adicionar campo
   (Texto, ~500 caracteres, **anulável = Sim** — senão trava toda linha antiga sem esse
   campo).
5. CSVs futuros passam a ter essa coluna a mais.
6. Testar antes numa cópia/versão de teste do e-mail, nunca direto no de produção.

## O que NÃO fazer

- Não assumir que "está tudo igual à campanha anterior" sem checar a chave composta contra
  o briefing atual — duplicidade de chave é silenciosa até o operador notar o e-mail errado
  chegando.
- Não inventar valor pra um placeholder sem contexto suficiente — perguntar.
- Não prometer que o CSV está "pronto pra disparar" sem checar o pitfall #5 (jornada).
- Não editar o CSV de trabalho em Excel com locale pt-BR sem depois conferir/reverter o
  delimitador (`;`→`,`), CRLF, aspas qualificadoras e o formato de data.

## Referências

- `Afinz-CRM-Midia-Vault/04-Operacao/Emails-Dinamicos-SFMC.md` — nota de arquitetura e
  contexto de negócio (ler para entender o "porquê"; este arquivo é o "como fazer").
- `Afinz-CRM-Midia-Vault/04-Operacao/SFMC-Salesforce-Marketing-Cloud.md` — fronteira
  GaaS↔SFMC em geral.
- `.claude/skills/gaas-governanca-comunicacoes/` — sistema **diferente**: governança de
  `template_id`/`af_sub3` do módulo Comunicações do GaaS. Não confundir com este.
