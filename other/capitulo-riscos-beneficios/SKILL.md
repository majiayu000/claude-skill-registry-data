---
name: capitulo-riscos-beneficios
description: Redigir o Capítulo 7 (Análise dos Riscos e dos Benefícios) de um projeto de pesquisa científica em português brasileiro. Usar após concluir o Capítulo 6 com o skill capitulo-monitorizacao. Usar quando o usuário solicitar "análise de riscos", "análise de benefícios", "relação risco-benefício", "matriz de riscos", "capítulo 7" ou similares. A skill solicita ao aluno que reapresente o contexto do Capítulo 6 já redigido antes de iniciar, promovendo releitura e assimilação do conteúdo anterior. Redige as três seções do Capítulo 7 com linguagem acadêmica formal, citações bibliográficas integradas no formato (Autor, ano) e lista de referências Vancouver com DOI e URL ao final, em conformidade com a Resolução CNS 466/12, CIOMS 2016, ISO 31000:2018 e Declaração de Helsinki 2013.
version: 1.0.0
argument-hint: [cole aqui um resumo do Cap. 6 já redigido]

---

# Capítulo 7. Análise dos Riscos e dos Benefícios. Skill de Redação Acadêmica

## Objetivo

Produzir o **Capítulo 7. Análise dos Riscos e dos Benefícios** de um projeto de pesquisa científica em português brasileiro formal, com base no Capítulo 6 (Monitorização da Pesquisa) já concluído pelo aluno.

O capítulo aprofunda a análise ética do estudo mediante três seções: **7.1 Análise dos riscos** (matriz de registro de riscos com detalhamento narrativo dos riscos Moderado, Alto e Crítico), **7.2 Análise dos benefícios diretos e indiretos** e **7.3 Relação risco-benefício**. Fundamenta-se na legislação brasileira de ética em pesquisa (Resolução CNS 466/12), nas Diretrizes Éticas Internacionais do CIOMS (2016), na metodologia de gestão de riscos da ISO 31000:2018 e na Declaração de Helsinki (2013).

O texto deve ser redigido no **futuro do indicativo** ("será realizado", "serão verificados", "manterá") por se tratar de projeto de pesquisa ainda a ser executado. A linguagem é acadêmica formal, sem coloquialismos, com referências bibliográficas integradas ao texto no formato **(Sobrenome, ano)** e lista de referências em ordem alfabética no estilo **Vancouver** (com DOI e URL) ao final do capítulo.

---

## Regras tipográficas obrigatórias

Aplicar em todo o texto redigido por esta skill, sem exceção:

**Estrangeirismos em itálico:** toda palavra ou expressão em idioma diferente do português brasileiro deve ser grafada em itálico. Exemplos: *data safety monitoring board*, *range checks*, *logic checks*, *double data entry*, *queries*, *equipoise*, *completeness checks*, *data monitoring committee*, *adverse event*, *et al.*, *apud*.

**Proibição de travessões:** não usar travessões (—) em nenhuma hipótese no texto redigido. Substituir por dois-pontos (:), ponto e vírgula (;), vírgula (,) ou reescrever a frase para eliminar a necessidade do travessão.

---

## Fase 1: Releitura do Capítulo 6 e levantamento das informações para o Capítulo 7

**Antes de responder, o aluno deve reler o Capítulo 6 (Monitorização da Pesquisa) que redigiu com o skill `capitulo-monitorizacao`.** Esta releitura é indispensável: as informações sobre procedimentos, riscos operacionais e medidas de proteção descritas no Capítulo 6 são a base da análise ética que será desenvolvida neste capítulo.

Apresentar as perguntas abaixo em dois blocos. O aluno pode responder de uma só vez:

---

### Bloco A: Contexto do Capítulo 6 (extraído da releitura)

1. **Título provisório ou tema** do estudo e **tipo de delineamento** (ensaio clínico randomizado, estudo observacional, qualitativo, misto, ou outro)
2. **Lista dos procedimentos** descritos na seção 6.1 (ex.: coleta de sangue, aplicação de questionário, medidas antropométricas, uso de medicamentos, sessões de exercício físico)
3. **Classificação do risco global** já indicada no Capítulo 6: mínimo, menor que o mínimo ou maior que o mínimo (conforme Resolução CNS 466/12, item II.2)
4. **Grupos vulneráveis** incluídos na população (menores de 18 anos, gestantes, pessoas com déficit cognitivo, privados de liberdade, idosos com demência, populações indígenas, pessoas em situação de rua) e as respectivas salvaguardas já descritas no Capítulo 6 — ou "não se aplica"
5. **Profissional responsável pelo acompanhamento em caso de achado anormal** (extraído da seção 6.1 do Capítulo 6): nome completo ou função, registro no conselho de classe com número (ex.: CRM nº 12345/UF, CREFITO nº 67890, CFP nº 12345), forma de agendamento (telefone, e-mail, sistema online ou presencial), dias e horários disponíveis — ou "não se aplica"
6. **Nome e tipo da instituição** proponente

---

### Bloco B: Informações específicas do Capítulo 7

7. **Benefícios diretos esperados para os participantes**: o que cada participante individualmente poderá obter com a sua participação (ex.: acesso gratuito a avaliação de saúde, recebimento de laudo ou relatório individual de resultados, acesso a intervenção terapêutica, benefício educativo, encaminhamento para serviço de referência) — ou informar que **não há benefícios diretos previstos**
8. **Benefícios indiretos científicos esperados**: contribuição do estudo para o conhecimento na área (ex.: publicação em periódico, formação de pesquisadores, produção de tese ou dissertação)
9. **Benefícios indiretos sociais esperados**: impacto para a coletividade (ex.: subsídio a políticas públicas de saúde, melhoria de protocolos clínicos, benefício a grupos futuros de pacientes)

Se o aluno já forneceu contexto suficiente no argumento de entrada do skill, aproveitar as informações disponíveis e perguntar apenas o que estiver faltando ou ambíguo.

---

## Fase 2: Seção 7.1: Análise dos riscos

### Instruções de redação

A seção 7.1 é estruturada em **três elementos sequenciais**. Gerar todos na ordem indicada.

**Abertura direta:** iniciar a seção 7.1 com uma frase que retome brevemente o tipo de estudo, os procedimentos e a população (com base no Bloco A da Fase 1), sem repetir explicações metodológicas nem citar normas introdutórias. Em seguida, apresentar imediatamente a Tabela 1 (Matriz de registro de riscos).

---

#### Elemento 1: Matriz de registro de riscos

Apresentar **todos os riscos identificados** em uma única tabela, ordenada do menor para o maior nível de risco. Cada linha corresponde a um risco específico; a medida de mitigação na coluna correspondente é **específica àquele risco** (nunca genérica). Para riscos com nível **Moderado, Alto ou Crítico**, inserir um número de nota de rodapé (¹ ²...) que remete ao detalhamento do Elemento 2.

```
Instruções de formatação: apresentar como tabela Markdown, exatamente como abaixo. Incluir obrigatoriamente a legenda de interpretação logo abaixo da tabela.
```

**Tabela 1: Matriz de registro de riscos**

| Nº | Risco identificado | Probabilidade | Severidade | **Nível de risco** | Medida de mitigação principal | Responsável |
|---|---|---|---|---|---|---|
| [N] | [Descrição concisa do risco] | [Muito baixa/Baixa/Moderada/Alta] | [Mínima/Leve/Moderada/Grave] | **[Aceitável/Baixo/Moderado¹/Alto²/Crítico³]** | [Medida específica: quem, como, quando] | [Papel na equipe] |

**Riscos-padrão por tipo de procedimento** (pré-populados conforme os procedimentos informados no Bloco A da Fase 1):

Para **procedimentos antropométricos** (peso, estatura, perímetros):

| Nº | Risco identificado | Probabilidade | Severidade | **Nível de risco** | Medida de mitigação principal | Responsável |
|---|---|---|---|---|---|---|
| 1 | Lipotimia/tontura transitória na posição ortostática | Muito baixa | Leve | **Baixo** | Avaliação em sala climatizada; maca disponível; participante nunca permanece sozinho; orientação para comunicar sintomas imediatamente | Avaliador treinado |
| 2 | Desconforto transitório relacionado à exposição corporal durante a mensuração | Baixa | Mínima | **Baixo** | Sala reservada com biombo; avaliador do mesmo sexo quando solicitado; orientação prévia sobre o procedimento; direito de interromper a qualquer momento | Avaliador treinado |
| 3 | Comprometimento da imagem corporal em participantes com insatisfação corporal | Baixa | Leve | **Baixo** | Comunicação não estigmatizante dos resultados; avaliador treinado em abordagem empática; encaminhamento para atendimento psicológico disponível na instituição¹ | Pesquisador / Avaliador |
| 4 | Violação da confidencialidade dos dados durante armazenamento ou transmissão | Baixa | Moderada | **Moderado**² | Pseudonimização por código alfanumérico; banco de dados criptografado; acesso por senha individual; canal seguro de transmissão (ver Cap. 6, seção 6.3) | Pesquisador principal |
| 5 | Perda ou dano irreversível dos dados coletados | Muito baixa | Moderada | **Baixo** | Backups semanais em mídia externa; procedimento de encerramento por perda total (ver Cap. 6, seção 6.4) | Coordenador de pesquisa |

Para **procedimentos de coleta de sangue venoso**:

| Nº | Risco identificado | Probabilidade | Severidade | **Nível de risco** | Medida de mitigação principal | Responsável |
|---|---|---|---|---|---|---|
| 1 | Infecção local no sítio de punção | Muito baixa | Moderada | **Baixo** | Materiais descartáveis; antissepsia com álcool isopropílico 70° antes da punção; técnica asséptica rigorosa | Profissional habilitado (enfermeiro/biomédico) |
| 2 | Lipotimia vasovagal durante ou após a punção | Baixa | Leve | **Baixo** | Punção realizada com participante sentado ou deitado; monitoração por 5 minutos pós-procedimento; material de emergência disponível na sala | Profissional habilitado |
| 3 | Dor local e hematoma no sítio de punção | Moderada | Leve | **Moderado**¹ | Escalpe de menor calibre compatível com o volume necessário; pressão local por 3 a 5 minutos; orientação sobre sinais de hematoma e canal de contato para intercorrências | Profissional habilitado |
| 4 | Violação da confidencialidade dos dados | Baixa | Moderada | **Moderado**² | Pseudonimização; banco criptografado; acesso restrito (ver Cap. 6, seção 6.3) | Pesquisador principal |
| 5 | Perda ou dano dos dados | Muito baixa | Moderada | **Baixo** | Backups semanais; procedimento de encerramento (ver Cap. 6, seção 6.4) | Coordenador de pesquisa |

Para **procedimentos de aplicação de questionários sobre temas sensíveis**:

| Nº | Risco identificado | Probabilidade | Severidade | **Nível de risco** | Medida de mitigação principal | Responsável |
|---|---|---|---|---|---|---|
| 1 | Desconforto emocional transitório ao abordar temas sensíveis (saúde mental, violência, sexualidade, uso de substâncias) | Baixa | Leve | **Baixo** | Entrevistador treinado em acolhimento; interrupção imediata ao sinal de angústia; participante pode recusar questões individuais sem encerrar a participação; encaminhamento para serviço de apoio psicológico disponível¹ | Entrevistador treinado |
| 2 | Violação da confidencialidade de dados de saúde sensíveis | Baixa | Moderada | **Moderado**² | Pseudonimização; banco criptografado; acesso por senha individual; nenhum dado identificado armazenado junto às respostas (ver Cap. 6, seção 6.3) | Pesquisador principal |

```
Instrução operacional: se o estudo combinar mais de um tipo de procedimento (ex.: antropometria + questionário), consolidar todos os riscos em uma única tabela numerada sequencialmente, removendo duplicatas (ex.: violação de confidencialidade aparece uma vez, cobrindo todos os procedimentos).
```

**Legenda de interpretação dos níveis de risco** (inserir obrigatoriamente logo abaixo da tabela):
- **Aceitável:** risco desprezível; nenhuma medida adicional requerida além das boas práticas de pesquisa.
- **Baixo:** risco tolerável; controlado com boas práticas padrão de pesquisa (POP, treinamento).
- **Moderado:** requer medidas de mitigação ativas, monitoramento e registro sistemático (ver detalhamento narrativo abaixo).
- **Alto:** requer medidas robustas e documentadas; revisão pelo pesquisador principal antes do início (ver detalhamento narrativo abaixo).
- **Crítico:** pode inviabilizar o estudo na forma proposta; requer reavaliação do protocolo e aprovação expressa do CEP (ver detalhamento narrativo abaixo).

Fonte: International Organization for Standardization (2018); adaptado para pesquisa em saúde segundo Brasil (2012) e Council for International Organizations of Medical Sciences (2016).

Consultar `references/protecao-e-monitoramento.md`, seção 8 (Matriz de risco: metodologia e exemplos), para critérios detalhados de classificação de probabilidade e severidade e exemplos adicionais de matrizes preenchidas.

---

#### Elemento 2: Detalhamento narrativo dos riscos Moderado, Alto e Crítico

Para **cada risco com nível Moderado, Alto ou Crítico** identificado na Tabela 1, redigir um parágrafo de detalhamento referenciado pelo número de nota de rodapé correspondente. Riscos com nível Baixo ou Aceitável **não recebem parágrafo**: a tabela é suficiente.

Cada parágrafo de detalhamento deve conter:
- **Identificação:** "Nota [N]: [Nome do risco]"
- **Circunstâncias de materialização:** quando, em quem e sob quais condições o risco tem maior probabilidade de ocorrer
- **Detalhamento completo da mitigação:** quem implementa, como, em que momento, com quais recursos e com qual frequência de verificação
- **Informações do profissional de acompanhamento (quando aplicável):** sempre que a mitigação previr encaminhamento ou acompanhamento do participante por profissional de saúde em razão de achado anormal, incluir obrigatoriamente: nome completo do profissional (ou função, se ainda não definido), registro no conselho de classe com número (ex.: CRM nº 12345/UF, CREFITO nº 67890, CFP nº 12345), forma de agendamento (telefone, e-mail, sistema online ou presencial), dias e horários disponíveis para atendimento, e qualquer outra informação necessária para que o participante acesse o serviço de forma autônoma.
- **Monitoramento:** como será verificado se a medida de mitigação está sendo efetivamente cumprida durante a coleta
- **Referência bibliográfica** que embasa a avaliação ou a medida adotada

Exemplo de estrutura para "Violação da confidencialidade dos dados" (nível Moderado):

> *Nota 2: Violação da confidencialidade dos dados.* O risco de acesso não autorizado às informações dos participantes é classificado como **Moderado** em razão da severidade moderada do dano potencial (exposição de dados sensíveis de saúde), embora sua probabilidade seja baixa dado o conjunto de controles técnicos adotados. Este risco é mais provável durante a transmissão de dados entre membros da equipe ou em caso de acesso não autorizado ao dispositivo de armazenamento. A mitigação será assegurada por: (a) pseudonimização completa, com todos os registros identificados exclusivamente por código alfanumérico e lista de correspondência mantida separada pelo pesquisador principal; (b) criptografia do arquivo do banco de dados; (c) senhas individuais e intransferíveis trocadas a cada noventa dias; (d) proibição de transmissão de dados por canais não seguros. A efetividade dessas medidas será verificada nas auditorias quinzenais do banco de dados descritas na seção 6.2. Citar: (Brasil, 2018; Society for Clinical Data Management, 2013; International Council for Harmonisation, 2016).

---

#### Elemento 3: Parágrafo de conclusão da seção 7.1

Redigir um parágrafo final sintetizando o perfil geral de risco do estudo a partir da matriz. Indicar: quantos riscos foram identificados; a distribuição por nível (ex.: "N riscos Aceitável ou Baixo; N riscos Moderado; nenhum risco Alto ou Crítico"); a classificação global na escala CNS 466/12 (reafirmar). Concluir que todas as medidas de mitigação previstas são suficientes para reduzir o risco residual a um nível aceitável e que a análise da relação risco-benefício é apresentada na seção 7.3. Citar: (Brasil, 2012; Council for International Organizations of Medical Sciences, 2016; International Organization for Standardization, 2018).

---

## Fase 3: Seção 7.2: Análise dos benefícios diretos e indiretos

### Instruções de redação

Redigir ao menos **três parágrafos**, separando com clareza os benefícios diretos dos indiretos:

**Parágrafo 1: Benefícios diretos:**
Os benefícios diretos são aqueles que o **participante individualmente** pode obter em razão de sua participação no estudo. Descrever com especificidade cada benefício direto identificado:

- **Se houver benefícios diretos:** descrever cada um: acesso gratuito a avaliação profissional de saúde (antropométrica, clínica, laboratorial, psicológica); recebimento de laudo ou relatório individual com os resultados das avaliações realizadas; acesso a intervenção terapêutica, educativa ou preventiva não disponível pela via assistencial habitual; encaminhamento qualificado para serviço de referência especializado; orientações individualizadas de saúde decorrentes dos resultados obtidos. **Sempre que o benefício direto envolver encaminhamento ou acompanhamento por profissional de saúde**, incluir obrigatoriamente no texto: nome completo do profissional (ou função, se ainda não definido), registro no conselho de classe com número (ex.: CRM nº 12345/UF, CREFITO nº 67890, CFP nº 12345), forma de agendamento (telefone, e-mail, sistema online ou presencial), dias e horários disponíveis para atendimento, e qualquer outra informação necessária para que o participante acesse o serviço de forma autônoma. Citar: (Brasil, 2012; World Medical Association, 2013).
- **Se não houver benefícios diretos:** registrar explicitamente que a pesquisa não prevê benefícios diretos individuais aos participantes, e justificar a aceitabilidade ética dessa ausência com base no risco mínimo dos procedimentos, no valor científico e social do estudo, e no caráter voluntário e revogável da participação. Citar: (Brasil, 2012; Council for International Organizations of Medical Sciences, 2016).

**Parágrafo 2: Benefícios indiretos científicos:**
Os benefícios indiretos científicos referem-se à contribuição do estudo para a produção e disseminação de conhecimento na área. Descrever: o avanço esperado no entendimento do fenômeno estudado; a publicação dos resultados em periódicos científicos de acesso aberto (para maximizar o alcance); a contribuição para o campo de pesquisa nacional e internacional; a formação de pesquisadores e a capacitação de estudantes de pós-graduação envolvidos no projeto; a produção de dissertações, teses e relatórios técnicos. Citar: (Brasil, 2012; World Medical Association, 2013).

**Parágrafo 3: Benefícios indiretos sociais e para grupos futuros:**
Os benefícios indiretos sociais são aqueles que recairão sobre a coletividade (grupos de pacientes, gestores de saúde, formuladores de políticas públicas) a partir dos achados desta pesquisa. Descrever: o potencial do estudo para subsidiar diretrizes clínicas, protocolos assistenciais ou políticas públicas de saúde na área investigada; a contribuição para a melhoria da qualidade da atenção à saúde de grupos futuros de pessoas com a mesma condição; o impacto esperado sobre indicadores epidemiológicos ou de saúde pública; a possibilidade de redução de custos para o sistema de saúde mediante intervenções baseadas em evidências geradas por este estudo. Citar: (Brasil, 2012; Council for International Organizations of Medical Sciences, 2016; World Medical Association, 2013).

---

## Fase 4: Seção 7.3: Relação risco-benefício

### Instruções de redação

Redigir ao menos **dois parágrafos** sintetizando a análise ética e concluindo pela aceitabilidade ou não do estudo:

**Parágrafo 1: Síntese comparativa:**
Retomar, de forma concisa, os riscos identificados na seção 7.1 (com suas classificações globais e as medidas de mitigação previstas) e os benefícios descritos na seção 7.2 (diretos e indiretos). Argumentar que os riscos são justificados pelos benefícios esperados: quando o risco é mínimo ou menor que o mínimo e os benefícios científicos e/ou sociais são relevantes, a relação risco-benefício é favorável e eticamente aceitável. Quando o risco é maior que o mínimo, demonstrar que os benefícios diretos ao participante ou o valor científico excepcional do estudo justificam a exposição, e que as medidas de mitigação reduzem o risco residual a níveis aceitáveis. Citar: (Brasil, 2012; Council for International Organizations of Medical Sciences, 2016; World Medical Association, 2013).

**Parágrafo 2: Declaração de aceitabilidade ética e papel do CEP:**
Concluir com declaração de que, com base na análise apresentada, a relação risco-benefício do presente estudo é considerada **favorável** (ou, em casos de risco maior que o mínimo: favorável mediante as medidas de mitigação descritas), sendo a pesquisa eticamente justificável. Registrar que a avaliação independente dessa relação pelo **Comitê de Ética em Pesquisa (CEP)** da instituição proponente, por meio do sistema Plataforma Brasil, constitui salvaguarda adicional e condição indispensável para o início do estudo. Nos casos em que o risco for maior que o mínimo, registrar também a submissão ao escrutínio da **CONEP**, quando aplicável. Citar: (Brasil, 2012; Brasil, Ministério da Saúde, 2013; World Medical Association, 2013).

---

## Fase 5: Lista de referências (ao final do capítulo)

Ao concluir a redação das três seções, gerar automaticamente a **lista de referências** do capítulo. A lista deve obedecer às seguintes regras:

- **Formato:** Vancouver (sobrenome, iniciais do nome. Título. Periódico ou Editora. Ano; volume(número):páginas. doi: [DOI]. Disponível em: [URL])
- **Ordem:** alfabética pelo primeiro elemento de entrada (sobrenome do primeiro autor ou nome do órgão institucional)
- **Completude:** incluir DOI quando disponível; incluir URL de acesso quando disponível; para legislação brasileira, indicar o Diário Oficial da União
- **Cobertura:** incluir todas as fontes citadas no texto no formato (Autor, ano)

### Lista de referências nucleares a incluir (adaptar e acrescentar conforme as seções redigidas):

Brasil. Conselho Nacional de Saúde. Resolução nº 466, de 12 de dezembro de 2012. Aprova as diretrizes e normas regulamentadoras de pesquisas envolvendo seres humanos. Diário Oficial da União, Brasília, DF, 13 jun. 2013; Seção 1:59. Disponível em: https://conselho.saude.gov.br/resolucoes/2012/Reso466.pdf

Brasil. Lei nº 13.709, de 14 de agosto de 2018. Lei Geral de Proteção de Dados Pessoais (LGPD). Diário Oficial da União, Brasília, DF, 15 ago. 2018. Disponível em: https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm

Brasil. Ministério da Saúde. Conselho Nacional de Saúde. Norma Operacional nº 001/2013 — CONEP. Dispõe sobre a organização e funcionamento do sistema CEP/CONEP. Brasília: Ministério da Saúde; 2013. Disponível em: https://conselho.saude.gov.br/web_comissoes/conep/aquivos/normativa/normaoperacional001_2013_conep.pdf

Council for International Organizations of Medical Sciences (CIOMS). International Ethical Guidelines for Health-related Research Involving Humans. 4th ed. Geneva: CIOMS; 2016. doi:10.56759/rgxl7429. Disponível em: https://cioms.ch/publications/product/international-ethical-guidelines-for-health-related-research-involving-humans/

DeMets DL, Furberg CD, Friedman LM. Data Monitoring in Clinical Trials: A Case Studies Approach. New York: Springer; 2006. doi:10.1007/978-0-387-27771-8

Ellenberg SS, Fleming TR, DeMets DL. Data Monitoring Committees in Clinical Trials: A Practical Perspective. 2nd ed. Chichester: Wiley; 2019. doi:10.1002/9781119512592

International Council for Harmonisation (ICH). ICH E6(R2): Guideline for Good Clinical Practice. Geneva: ICH; 2016. Disponível em: https://www.ich.org/page/efficacy-guidelines

International Organization for Standardization. ISO 31000:2018 — Risk management: guidelines. Geneva: ISO; 2018. Disponível em: https://www.iso.org/standard/65694.html

Moher D, Hopewell S, Schulz KF, Montori V, Gøtzsche PC, Devereaux PJ, et al. CONSORT 2010 explanation and elaboration: updated guidelines for reporting parallel group randomised trials. BMJ. 2010;340:c869. doi:10.1136/bmj.c869. Disponível em: https://www.bmj.com/content/340/bmj.c869

National Cancer Institute. Common Terminology Criteria for Adverse Events (CTCAE), Version 5.0. Bethesda (MD): US Department of Health and Human Services; 2017. Disponível em: https://ctep.cancer.gov/protocoldevelopment/electronic_applications/docs/CTCAE_v5_Quick_Reference_5x7.pdf

Society for Clinical Data Management (SCDM). Good Clinical Data Management Practices (GCDMP). Version 4.0. Milwaukee: SCDM; 2013. Disponível em: https://scdm.org/gcdmp/

World Medical Association. Declaration of Helsinki: Ethical Principles for Medical Research Involving Human Subjects. Fortaleza: WMA; 2013. Disponível em: https://www.wma.net/policies-post/wma-declaration-of-helsinki-ethical-principles-for-medical-research-involving-human-subjects/

---

## Fase 6: Entregáveis

Após apresentar o texto completo do Capítulo 7, inclua a seguinte mensagem ao final da resposta:

> "Capítulo 7 gerado. Use os botões abaixo para baixar o resultado nos formatos .md, .docx e .pdf."

O sistema gera os arquivos automaticamente — **não inclua scripts, código ou blocos de dependências na resposta.**

---

## Padrões de qualidade: checklist de revisão antes de entregar o texto

Antes de apresentar o capítulo ao usuário, verificar se **todos** os itens abaixo estão presentes e completos:

- [ ] Fase 1 concluída: aluno forneceu contexto do Cap. 6 (procedimentos, classificação de risco, grupos vulneráveis, profissional de acompanhamento) e informações dos benefícios
- [ ] Seção 7.1: abre com frase de contextualização direta (tipo de estudo, procedimentos, população) sem parágrafo introdutório explicativo sobre normas
- [ ] Seção 7.1: Tabela 1 (Matriz de registro de riscos) presente imediatamente após a frase de abertura
- [ ] Seção 7.1: legenda de interpretação dos níveis de risco inserida logo abaixo da Tabela 1
- [ ] Seção 7.1: cada risco apresentado com Descrição, Probabilidade, Severidade, Nível de risco, Medida de mitigação específica e Responsável
- [ ] Seção 7.1: nenhuma medida de mitigação genérica; cada mitigação vinculada diretamente ao risco correspondente
- [ ] Seção 7.1: detalhamento narrativo (Elemento 2) presente para todos os riscos Moderado, Alto ou Crítico
- [ ] Seção 7.1: quando o detalhamento narrativo previr encaminhamento por profissional de saúde, informações completas incluídas (nome/função, conselho de classe com número, agendamento, dias e horários)
- [ ] Seção 7.1: parágrafo de conclusão (Elemento 3) com distribuição dos níveis de risco e classificação global CNS 466/12
- [ ] Seção 7.2: benefícios diretos descritos com especificidade (ou ausência declarada e justificada eticamente)
- [ ] Seção 7.2: quando benefício direto envolver encaminhamento, informações completas do profissional incluídas (nome/função, conselho de classe com número, agendamento, dias e horários)
- [ ] Seção 7.2: benefícios indiretos científicos descritos (publicação, formação, produção de conhecimento)
- [ ] Seção 7.2: benefícios indiretos sociais descritos (políticas públicas, grupos futuros, sistema de saúde)
- [ ] Seção 7.3: síntese comparativa riscos x benefícios com argumentação ética coerente
- [ ] Seção 7.3: declaração de aceitabilidade ética e papel do CEP mencionado
- [ ] Citações integradas ao texto no formato **(Autor, ano)** em todas as afirmações que requerem fundamentação
- [ ] Lista de referências ao final do capítulo em ordem **alfabética**, estilo **Vancouver**, com **DOI** e **URL** quando disponíveis
- [ ] Nenhuma seção genérica ou com marcador de posição ("[inserir aqui]", "a definir", etc.)
- [ ] Texto integralmente em **português brasileiro formal**, no **futuro do indicativo**
- [ ] Ausência de primeira pessoa do singular ("Eu realizarei" deve ser "será realizado")
- [ ] Todas as palavras e expressões em outros idiomas grafadas em **itálico**
- [ ] Ausência de travessões (—) em todo o texto redigido
- [ ] PDF gerado com cabeçalho "Capítulo 7. Análise dos Riscos e dos Benefícios" e numeração de páginas; caminhos completos confirmados ao usuário

**Próxima etapa:** solicite a skill `/capitulo-propriedade-responsabilidades` para redigir os Capítulos 8, 9 e 10 — Propriedade intelectual, Responsabilidades e Grupos vulneráveis.

---

## Referências de suporte

O arquivo de referência desta skill (carregado sob demanda com a ferramenta Read) contém:

- `references/protecao-e-monitoramento.md`: classificação de risco CNS 466/12 com exemplos práticos; tabela de graus CTCAE v5.0; checklist de qualidade de dados; componentes do DSMB e modelos de regras de parada (O'Brien-Fleming, Pocock); requisitos LGPD aplicados à pesquisa em saúde; modelos de frases em diferentes cenários de estudo (ensaio clínico, observacional, qualitativo); lista de referências Vancouver completa com DOI e URL


---

## SINALIZAÇÃO DE CONCLUSÃO

Quando todos os entregáveis desta etapa estiverem gerados e a etapa estiver
completa — e somente então —, adicione a seguinte linha como **última linha** da resposta:

=== ETAPA CONCLUÍDA ===

**Regras:**
- Emita o marcador **apenas uma vez**, na última resposta da etapa.
- **Não emita** em respostas intermediárias, enquanto aguardar dados do usuário,
  ou antes de todos os documentos/seções solicitados estarem prontos.
- Se o usuário pedir ajustes após a sinalização, **não** emita o marcador novamente
  nas respostas de ajuste.
