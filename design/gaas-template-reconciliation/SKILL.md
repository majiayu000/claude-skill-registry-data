---
name: gaas-template-reconciliation
description: Reconciliar governança XLSX de links/templates Afinz, imagens, pacotes
  SFMC, catálogo e activities por conteúdo, público, posição e data; preparar propostas
  auditáveis e uma fila compacta de aprovação. Usar ao analisar template_id versus
  comunicação e uso histórico, ou especificar inteligência da aba Comunicações. Não
  executa mudanças no SFMC nem aplica vínculos por iniciativa própria.
metadata:
  version: 1.0.1
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

# Reconciliação de templates GaaS

## Resultado esperado
Produzir propostas explicáveis de peça + versão + uso + execução, aproveitando todas as fontes disponíveis sem transformar evidência ausente em confirmação. A unidade de aprovação é um conjunto explícito de registros, dentro de jornada, ramo, canal e período comprovados.

Leia [contrato da governança](references/governance-contract.md) para interpretar XLSX, IDs e URLs; [evidências visuais](references/visual-evidence.md) quando houver prints; [motor e aprovação](references/reconciliation-design.md) para ranking de candidatos, repetição, ordem ou mudanças na interface. Essas referências distinguem fatos observados de propostas futuras.

Antes de fechar a interpretação, leia [fundamentos do Vault](references/vault-foundations.md): reúne a evolução das regras, conflitos históricos, acervos existentes e separação entre toque, canal, cadência e data. Consulte as notas vivas quando uma conclusão depender de vigência ou estado de implementação.

Para revisar momento, subgrupo, período ou cobertura de ID no pack, leia [contrato atualizado de momentos e subgrupos](references/moments-subgroups-pack-inventory.md). Ele registra a definição mais recente do operador e os conflitos com as notas históricas.

## Fontes
- Workbook fornecido: declaração de governança, não prova de envio. Preserve nome da aba, célula, fórmula, cache e SHA-256.
- Pacote SFMC: configuração exportada da jornada/versão, conteúdo e ramo. Não certifica a versão enviada numa data passada.
- activities: execução registrada e suas dimensões; confrontar divergências com o ramo e o Activity Name.
- Catálogo: identidade e arquivo registrado; não comprova que esse conteúdo foi usado em todos os vínculos históricos.
- Imagem: evidência de texto/criativo visível. Nome, limite, relógio do celular e link curto não comprovam identidade de pessoa, data do disparo ou parâmetros ocultos.
- Acervos do Vault: incluir dataset_vibe_completo.json, estrutura_bau_regua.json e dataset_completo.json, com proveniência e sem assumir certificação. Nome Salesforce não é necessariamente template_id.
- Decisões anteriores: reutilizáveis somente no mesmo escopo e com fingerprint vigente.

## Executar
1. Extrair XLSX em modo de leitura:
   `python scripts/inspect_governance.py "<arquivo.xlsx>" --out "<pasta>" --images`.
   O script usa apenas a biblioteca padrão, não altera o XLSX nem recalcula fórmulas. Interprete cache ausente como desconhecido.
2. Identificar abas operacionais pela estrutura, incluindo estado hidden e blocos auxiliares. Não promover cópia oculta nem linhas repetidas de preenchimento a cadastro ativo.
3. Ler as imagens extraídas com sua âncora. Se necessário, transcrever ou usar OCR disponível, marcando termos ilegíveis. Não persistir nomes e valores personalizados como parâmetros genéricos.
4. Extrair os packs com o parser do GaaS ou a skill sfmc-jornadas-pacote. Consultar toda a base relevante paginada, com contagem verificada; não usar a lista limitada da UI como universo completo.
5. Separar quatro entidades: template governado, versão de conteúdo, uso configurado em ramo/posição e execução histórica com activities.id + data.
6. Resolver dimensões com evidência por campo; sinalizar divergências. ID exato identifica um cadastro, mas não elimina conflito de canal, público, versão ou vigência.
7. Comparar candidatos, texto já observado e textos historicamente vinculados. Preparar fila com proposta, provas, restrições, alternativa e ação.
8. Entregar resumo simples e artefato de decisões para revisão. Especificar UI compacta conforme referência quando solicitado.

## Invariantes do domínio
- template_id/af_sub3 conserva a caixa. Campos de classificação podem ter aliases canônicos, a chave não.
- APP não equivale a BU/parceiro. DIA pode usar app Afinz; Serasa é audiência/parceiro de B2C.
- No contexto carrinho: car21 qualifica carrinho/público 21D; carsab qualifica sábado; inst = institucional; srsa é o código Serasa observado. srasa/sersa/serasa/ecred são candidatos a aliases de comparação contextual, não renomeações automáticas.
- `inst` também significa Instabilidade no ID_Dicionario: resolver por família/campo, nunca por substituição global.
- Segmento da coluna/af_sub1 vale como declaração. Exemplo DIA: ID contém bsp, mas K2 declara CRM e J2 contém crm; preservar CRM e expor o alias legado.
- Momento usa contrato por régua: DispDn é disparo; Negados pode usar Dn como disparo; calendários de topo/e-mail/CRM usam S=semana e D=dia conforme definição atual do operador. Dia relativo, semana, toque, subgrupo 21D e data de calendário permanecem separados. Não extrair ordinal de recência nem de YYYYMMDD.
- A BAU conta toques por canal; preservar ordinal global e ordinal no canal separadamente. O par Oferta + Promocional participa da intenção e da comparação.
- Upgrade menor pode reutilizar a linha de Repescagem por decisão operacional, sem trocar silenciosamente o segmento do disparo.
- Reuso de template/texto não é automaticamente erro. Diferença de assunto, público, parâmetro, ramo ou oferta pode ser intencional.
- Conteúdo/template inferidos por IA ou imagem não autorizam reassociação histórica. Aplicação depende de aprovação explícita; vínculo preenchido não é sobrescrito.
- Análise autônoma pode extrair, classificar, reunir candidatos, identificar reuso e simular. Não muda IDs, URLs, templates correntes ou activities; a skill não amplia a autorização do usuário.
- Fonte de conhecimento vivo permanece no Vault/OneDrive. Snapshot da referência deve ser confrontado com os arquivos e banco atuais; não gravar memória permanente sem pedido.

## Entrega mínima
Contexto identificado; template real observado; candidato contextual e razões; versão/conteúdo; repetição com escopo e data; ordem com grau de determinação; IDs de execução elegíveis; conflitos; ação e prévia compacta. Mostrar ausência de cobertura, sem afirmar “nunca utilizado”.

