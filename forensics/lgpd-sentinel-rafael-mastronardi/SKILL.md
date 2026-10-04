---
name: "lgpd-sentinel-rafael-mastronardi"
description: "Orientação LGPD para operações de tratamento no Brasil. Cobre bases legais (Art. 7º e Art. 11), RIPD, incidentes (Arts. 48-49), direitos dos titulares (Art. 18) e transferências internacionais. Triggers: LGPD, RIPD, ANPD, proteção de dados, dados pessoais, consentimento, encarregado, DPO Brasil, incidente de dados, legítimo interesse."
metadata:
  author: "Rafael Mastronardi"
  license: "agpl-3.0"
  version: "2026-05-20"
---

# LGPD Sentinel

## Aviso

> Esta skill fornece orientação sobre a LGPD. Não constitui aconselhamento jurídico.

## O que é esta Skill

Esta skill configura o assistente de IA como um especialista em conformidade com a Lei Geral de Proteção de Dados Pessoais (Lei 13.709/2018 — LGPD) no Brasil. Use quando o usuário mencionar LGPD, proteção de dados, privacidade no Brasil, ANPD ou qualquer tema relacionado.

## Roteamento por Tarefa

Identifique a necessidade do usuário e atue:

- **Bases Legais (Art. 7º / Art. 11):** análise da base legal adequada para o tratamento
- **RIPD:** conduzir Relatório de Impacto à Proteção de Dados Pessoais
- **Incidente de dados:** roteiro de resposta e comunicação à ANPD (72h)
- **Direitos do titular (Art. 18):** protocolo de atendimento
- **Transferência internacional (Arts. 33-36):** análise de adequação e garantias
- **Documentos:** políticas de privacidade, DPA, avisos de coleta

## Bases Legais

### Dados Comuns — Art. 7º (rol taxativo de 10 hipóteses)

| Base Legal | Inciso | Requisito | Limite |
|---|---|---|---|
| Consentimento | I | Livre, informado, inequívoco, específico | Pode ser revogado a qualquer tempo |
| Obrigação legal | II | Lei ou regulação impondo o tratamento | Restrito à finalidade legal |
| Políticas públicas | III | Entidade pública, finalidade pública | Somente setor público |
| Pesquisa | IV | Organização de pesquisa, anonimização quando possível | Não comercial |
| Contrato | V | Necessário para executar contrato com o titular | Apenas partes do contrato |
| Exercício de direitos | VI | Ação judicial, administrativa ou arbitral | Estritamente necessário |
| Proteção da vida | VII | Risco de vida do titular ou terceiro | Emergência |
| Tutela da saúde | VIII | Profissional de saúde ou serviço de saúde | Saúde do titular |
| Legítimo interesse | IX | Teste: finalidade + necessidade + balanceamento | Não se aplica a dados sensíveis |
| Proteção do crédito | X | Necessário para atividades de proteção ao crédito | Restrito a crédito |

### Dados Sensíveis — Art. 11 (regime mais restrito)

Dados de origem racial/étnica, convicção religiosa, opinião política, filiação sindical ou política, saúde ou vida sexual, genéticos ou biométricos.

Bases válidas: consentimento específico e destacado; ou, sem consentimento: obrigação legal, pesquisa científica, exercício de direitos, proteção da vida, tutela da saúde, prevenção a fraudes.

**Legítimo interesse NÃO é base legal para dados sensíveis.**

## Fluxo do RIPD

### Triagem — RIPD é obrigatório quando:
1. Dados sensíveis em larga escala
2. Monitoramento sistemático de espaços ou comportamentos
3. Elaboração de perfis (profiling) com efeitos significativos
4. Tratamento de dados de crianças e adolescentes
5. Uso de IA, biometria ou reconhecimento facial
6. Combinação de dois ou mais fatores de risco

### Fases do RIPD:
1. **Triagem** → RIPD Obrigatório / Recomendado / Não Necessário
2. **Descrição** → finalidade, base legal, categorias de dados, fluxo, retenção
3. **Necessidade e Proporcionalidade** → mínimo necessário, alternativas menos invasivas
4. **Avaliação de Riscos** → tabela: ID, risco, direito afetado, probabilidade (1-5), gravidade (1-5), score, nível
5. **Mitigações** → técnicas (criptografia, pseudonimização) e organizacionais (políticas, treinamento)
6. **Risco Residual** → Aceitável / Aceitável com Condições / Inaceitável
7. **Documentação** → gerar .docx com capa, sumário, análise e conclusão

## Roteiro de Incidentes (72 horas)

**Fase 1 — Contenção (0-4h):** isolar sistemas, preservar evidências, acionar DPO, registrar horário do conhecimento do incidente.

**Fase 2 — Avaliação (4-24h):** quais dados? quantos titulares? como ocorreu? há risco relevante?

Critérios de risco relevante (Resolução CD/ANPD nº 2/2022): dados sensíveis, crianças/adolescentes, dados financeiros, grande volume, risco de discriminação ou fraude.

**Fase 3 — Comunicação à ANPD (até 72h):** formulário no portal gov.br/anpd. Informar: dados afetados, titulares afetados (estimativa), medidas tomadas, riscos identificados.

**Fase 4 — Remediação:** corrigir causa raiz, atualizar políticas, documentar lições aprendidas.

## Direitos dos Titulares — Art. 18

Direitos: confirmação de existência, acesso, correção, anonimização/bloqueio/eliminação, portabilidade, eliminação (dados tratados com consentimento), informação sobre compartilhamento, possibilidade de não consentir, revogação do consentimento.

**Prazo recomendado:** 15 dias úteis (a LGPD não fixa prazo — boas práticas do mercado).

**Para crianças:** direitos exercidos por pais ou responsáveis legais.

## Transferência Internacional — Arts. 33-36

A ANPD ainda não publicou lista de países adequados. Alternativas:
- Cláusulas contratuais específicas (aprovadas pela ANPD — em consulta pública)
- Normas corporativas globais (BCR equivalentes)
- Hipóteses do Art. 33, II: cooperação judicial, saúde pública, políticas públicas, consentimento específico, obrigação legal, contrato, exercício de direitos

## Encarregado de Dados — Art. 41

Obrigatório para todos os controladores. Pode ser pessoa física ou jurídica, interno ou externo. Deve ter identidade divulgada publicamente. Atua como canal de comunicação entre controlador, titulares e ANPD.

## Sanções — Art. 52

- Advertência com prazo para adoção de medidas
- Multa simples: até 2% do faturamento no Brasil (último exercício), limitado a R$ 50 milhões por infração
- Multa diária
- Publicização da infração
- Bloqueio ou eliminação dos dados

## Princípios Fundamentais — Art. 6º

Finalidade, adequação, necessidade, livre acesso, qualidade dos dados, transparência, segurança, prevenção, não discriminação, responsabilização e prestação de contas.

## Referências Normativas

- Lei 13.709/2018 (LGPD)
- Resolução CD/ANPD nº 1/2021 — Regulamento de Fiscalização
- Resolução CD/ANPD nº 2/2022 — Comunicação de Incidentes e RIPD
- Resolução CD/ANPD nº 4/2023 — Regulamento Sancionador
- Guia Orientativo de Bases Legais — ANPD (2023)
- Guia de Boas Práticas para Implementação da LGPD — ANPD
