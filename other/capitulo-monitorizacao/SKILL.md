---
name: capitulo-monitorizacao
description: Redigir o Capítulo 6 (Monitorização da Pesquisa) de um projeto de pesquisa científica em português brasileiro. Usar quando o usuário solicitar "escrever monitorização", "capítulo de monitoramento", "medidas de proteção", "confidencialidade da pesquisa", "critérios de suspensão", "monitoramento de dados", "proteção de participantes" ou similares. A skill levanta as informações do estudo via perguntas estruturadas e redige as quatro seções obrigatórias do capítulo com linguagem acadêmica formal, citações bibliográficas integradas no formato (Autor, ano) e lista de referências Vancouver com DOI e URL ao final, em conformidade com a legislação brasileira de ética em pesquisa (Resolução CNS 466/12, LGPD) e diretrizes internacionais (ICH E6(R2), CIOMS 2016, Declaração de Helsinki 2013). Após concluir este capítulo, utilizar o skill capitulo-riscos-beneficios para redigir o Capítulo 7.
version: 1.0.0
argument-hint: [descrição-resumida-do-estudo]

---

# Capítulo 6: Monitorização da Pesquisa. Skill de Redação Acadêmica

## Objetivo

Produzir o **Capítulo 6. Monitorização da Pesquisa** de um projeto de pesquisa científica em português brasileiro formal.

O capítulo abrange as quatro seções operacionais: **6.1 Medidas de proteção ou minimização de riscos**, **6.2 Monitorização de dados**, **6.3 Confidencialidade** e **6.4 Critérios para suspensão ou encerramento**. Fundamenta-se na legislação brasileira de ética em pesquisa, nas diretrizes internacionais de boas práticas clínicas e na regulamentação de proteção de dados pessoais.

Ao concluir este capítulo, o aluno deverá utilizar o skill `capitulo-riscos-beneficios` para redigir o Capítulo 7 (Análise dos Riscos e dos Benefícios).

O texto deve ser redigido no **futuro do indicativo** ("será realizado", "serão verificados", "manterá") por se tratar de projeto de pesquisa ainda a ser executado. A linguagem é acadêmica formal, sem coloquialismos, com referências bibliográficas integradas ao texto no formato **(Sobrenome, ano)** e lista de referências em ordem alfabética no estilo **Vancouver** (com DOI e URL) ao final do capítulo.

---

## Regras tipográficas obrigatórias

Aplicar em todo o texto redigido por esta skill, sem exceção:

**Estrangeirismos em itálico:** toda palavra ou expressão em idioma diferente do português brasileiro deve ser grafada em itálico. Exemplos: *data safety monitoring board*, *range checks*, *logic checks*, *double data entry*, *queries*, *equipoise*, *completeness checks*, *data monitoring committee*, *adverse event*, *et al.*, *apud*.

**Proibição de travessões:** não usar travessões (—) em nenhuma hipótese no texto redigido. Substituir por dois-pontos (:), ponto e vírgula (;), vírgula (,) ou reescrever a frase para eliminar a necessidade do travessão.

---

## Fase 1: Levantamento das informações do estudo

Se o usuário não tiver fornecido as informações abaixo, solicitar **antes de iniciar a redação**. Apresentar as perguntas em um único bloco organizado para que o usuário possa responder de uma só vez:

1. **Título provisório ou tema** do estudo
2. **Tipo de delineamento** (ensaio clínico randomizado, estudo observacional, qualitativo, misto: ou outro)
3. **Procedimentos aos quais os participantes serão submetidos**: listar todos (ex.: coleta de sangue, aplicação de questionário, medidas antropométricas, intervenção cirúrgica, uso de medicamentos, sessões de exercício físico)
4. **Classificação do risco previsto**: mínimo, menor que o mínimo, maior que o mínimo (conforme Resolução CNS 466/12, item II.2): ou descrever os riscos para que a skill classifique
5. **A população inclui grupos vulneráveis?** (menores de 18 anos, gestantes, pessoas com déficit cognitivo, privados de liberdade, idosos com demência, populações indígenas, pessoas em situação de rua)
6. **Número de avaliadores/coletadores de dados** que integrarão a equipe
7. **Software/plataforma de banco de dados** que será utilizado (Microsoft Excel, REDCap, EpiInfo, SPSS, outro)
8. **Sistema de segurança digital previsto**: proteção por senha, criptografia, armazenamento em nuvem com autenticação de dois fatores, servidor institucional, outro
9. **Meta de recrutamento semanal** de participantes (número mínimo por semana) e **duração total do recrutamento** (em semanas ou meses)
10. **Está previsto um Comitê de Monitoramento de Dados (DSMB/DSMC)?** (tipicamente indicado para ensaios clínicos de fase III, estudos com desfechos de mortalidade ou eventos adversos graves)
11. **Nome e tipo da instituição** proponente (para adequar o texto de notificação ao CEP)
12. **Profissional responsável pelo acompanhamento em caso de achado anormal**: informar para cada profissional previsto: nome completo (ou função, se ainda não definido), registro no conselho de classe com número (ex.: CRM nº 12345/UF, CREFITO nº 67890, CFP nº 12345, CRF nº 67890), forma de agendamento (telefone, e-mail, sistema online ou presencial), dias e horários disponíveis para atendimento, e qualquer outra informação necessária para que o participante acesse o serviço de forma autônoma. Informar "não se aplica" se o estudo não prevê nenhum tipo de encaminhamento.

Se o usuário já forneceu contexto suficiente no prompt, aproveitar as informações disponíveis e perguntar apenas o que estiver faltando ou ambíguo.

---

## Fase 2: Seção 6.1: Medidas para a proteção ou minimização de quaisquer riscos

### Instruções de redação

Redigir ao menos **cinco parágrafos** cobrindo obrigatoriamente todos os seguintes elementos:

**Parágrafo 1: Descrição dos procedimentos e das medidas operacionais de proteção:**
Descrever cada procedimento ao qual os participantes serão submetidos, com especificidade técnica suficiente para permitir avaliação pelo CEP: instrumento utilizado, sequência de execução, profissional responsável pela realização e duração estimada de cada etapa. Registrar que a **análise detalhada dos riscos identificados**, suas probabilidades, severidades e respectivas medidas de mitigação, bem como a análise dos benefícios e da relação risco-benefício, são apresentadas no **Capítulo 7. Análise dos Riscos e dos Benefícios** deste protocolo, conforme estrutura recomendada pela Resolução CNS nº 466/2012 e pelo CIOMS 2016. As medidas descritas nesta seção (6.1) são de natureza **operacional**, complementares à análise de risco e voltadas para a condução segura da coleta de dados. Citar: (Brasil, 2012; Council for International Organizations of Medical Sciences, 2016).

**Parágrafo 2: Protocolo de treinamento e simulação da equipe:**
Descrever que todos os procedimentos serão minuciosamente detalhados em Procedimento Operacional Padrão (POP), apresentados em sessões de treinamento teórico e prático à equipe de pesquisa, e simulados com observadores treinados antes da primeira coleta de dados com participantes reais. Mencionar que somente após a validação da execução do POP por avaliador sênior, o procedimento será autorizado para aplicação em participantes. Para procedimentos clínicos ou laboratoriais, indicar que apenas profissionais com habilitação legal e certificação técnica específica realizarão os procedimentos. Citar: (International Council for Harmonisation, 2016; Council for International Organizations of Medical Sciences, 2016).

**Parágrafo 3: Canal de comunicação permanente com o participante:**
Descrever que, durante toda a coleta de dados, o participante será ativamente encorajado a formular perguntas e esclarecer dúvidas sobre qualquer etapa do procedimento a que está sendo submetido, antes, durante e após sua realização. Indicar que será disponibilizado ao participante um meio de contato direto com o pesquisador responsável (número de telefone institucional, endereço de e-mail ou outro canal definido pelo pesquisador) para que quaisquer dúvidas, desconfortos ou eventos adversos pós-coleta possam ser comunicados e devidamente acolhidos. Mencionar que o participante poderá retirar o consentimento e abandonar a pesquisa a qualquer momento, sem qualquer prejuízo ao seu atendimento ou relação com a instituição. Citar: (Brasil, 2012; World Medical Association, 2013).

**Parágrafo 4: Protocolo de identificação, registro e notificação de eventos adversos:**
Descrever os procedimentos para identificação, grau de severidade (conforme critérios do National Cancer Institute Common Terminology Criteria for Adverse Events: CTCAE v5.0, para estudos com intervenções clínicas), registro sistemático em formulário padronizado, conduta imediata adotada e notificação ao CEP. Diferenciar: **evento adverso** (qualquer ocorrência médica desfavorável, não necessariamente causalmente relacionada ao procedimento); **evento adverso sério** (aquele que resulta em morte, hospitalização, incapacidade, anomalia congênita ou que exija intervenção médica imediata). Para ensaios clínicos: descrever o prazo de notificação expedita ao CEP/CONEP (geralmente 15 dias para eventos adversos sérios inesperados). Citar: (International Council for Harmonisation, 2016; National Cancer Institute, 2017; Brasil, 2012).

**Parágrafo 5: Medidas adicionais para populações vulneráveis (quando aplicável):**
Se a população incluir grupos vulneráveis, descrever as salvaguardas adicionais adotadas para proteção de cada grupo: para menores de 18 anos, obtenção de assentimento do menor adequado à sua faixa etária (termo de assentimento) somado ao consentimento do responsável legal; para pessoas com déficit cognitivo ou demência, avaliação da capacidade de consentimento por profissional habilitado e obtenção de consentimento substituto do responsável legal; para pessoas privadas de liberdade, garantia de que a recusa não implicará qualquer sanção ou perda de benefícios; para populações indígenas, consulta às lideranças comunitárias e tradução do TCLE para a língua vernácula, quando necessário. Citar: (Brasil, 2012; Council for International Organizations of Medical Sciences, 2016).

Consultar `references/protecao-e-monitoramento.md` para a tabela de classificação de riscos, graus CTCAE e modelos de frases por tipo de estudo.

---

## Fase 3: Seção 6.2: Medidas de monitorização da coleta de dados

### Instruções de redação

Redigir ao menos **quatro parágrafos** cobrindo obrigatoriamente todos os seguintes elementos:

**Parágrafo 1: Design das fichas de coleta e dupla entrada de dados:**
Descrever que os dados serão coletados em fichas de coleta padronizadas (instrumento de papel ou formulário eletrônico), desenvolvidas especificamente para este estudo e testadas em estudo piloto. Descrever o processo de dupla entrada de dados (*double data entry*): dois digitadores independentes inserirão todos os dados no banco eletrônico; as discrepâncias identificadas pela comparação automática entre as duas entradas serão investigadas e resolvidas por reunião de consenso entre os pesquisadores responsáveis, com consulta às fichas originais de coleta. Especificar o software utilizado para o banco de dados e a versão. Citar: (Society for Clinical Data Management, 2013; International Council for Harmonisation, 2016).

**Parágrafo 2: Verificações automáticas de consistência e qualidade:**
Descrever as verificações de consistência interna aplicadas ao banco de dados, incluindo: *range checks* (valores fora da faixa biologicamente plausível serão sinalizados automaticamente para verificação); *logic checks* (verificação de consistência lógica entre variáveis relacionadas, como data de nascimento e idade calculada, diagnóstico e exames laboratoriais correspondentes); *completeness checks* (identificação de campos obrigatórios não preenchidos). Indicar a frequência com que os dados serão verificados (ex.: ao final de cada jornada de coleta, semanalmente, mensalmente) e o responsável pela auditoria de qualidade dos dados. Citar: (Society for Clinical Data Management, 2013; International Council for Harmonisation, 2016).

**Parágrafo 3: Auditoria periódica e gestão de inconsistências:**
Descrever que será realizada auditoria interna periódica do banco de dados pelo coordenador de pesquisa, com frequência definida (ex.: quinzenal ou mensal), verificando: completude dos registros, conformidade com os critérios de inclusão e exclusão, coerência entre as fichas de coleta originais e os dados digitados, e ausência de desvios de protocolo. Descrever como as *queries* (dúvidas ou inconsistências identificadas) serão formalizadas, encaminhadas ao coletador responsável e resolvidas dentro do prazo estipulado. Citar: (Society for Clinical Data Management, 2013).

**Parágrafo 4: Comitê de Monitoramento de Dados / DSMB (quando indicado):**
Para ensaios clínicos com desfechos de mortalidade, morbidade grave ou potencial de dano significativo: descrever a constituição de um **Comitê de Monitoramento de Dados** (*Data Safety Monitoring Board*: DSMB) independente, composto por profissionais com expertise clínica e estatística não vinculados à equipe de pesquisa. Especificar: composição prevista (ex.: um clínico especialista na área, um bioestatístico independente, um especialista em ética em pesquisa); mandato do comitê (revisão periódica de dados de segurança e eficácia intermediária); frequência das reuniões (ex.: a cada 25%, 50% e 75% do recrutamento); regras de parada interina pré-especificadas (ex.: fronteira de O'Brien-Fleming para eficácia, limiar pré-definido para danos); processo de relatório e recomendação ao patrocinador e ao CEP. Se o DSMB não for aplicável ao estudo, justificar brevemente (ex.: estudo de risco mínimo, delineamento transversal sem intervenção). Citar: (DeMets et al., 2006; Ellenberg et al., 2019; International Council for Harmonisation, 2016).

Consultar `references/protecao-e-monitoramento.md` para modelos de DSMB, regras de parada e checklist de qualidade de dados.

---

## Fase 4: Seção 6.3: Medidas de proteção à confidencialidade

### Instruções de redação

Redigir ao menos **cinco parágrafos** cobrindo obrigatoriamente todos os seguintes elementos:

**Parágrafo 1: Pseudonimização e controle de identificação:**
Descrever que a identidade dos participantes será protegida por meio de pseudonimização: a cada participante será atribuído um código alfanumérico único, gerado sequencialmente ou aleatoriamente, que será utilizado em todas as fichas de coleta, formulários e no banco de dados eletrônico. A lista de correspondência entre o código e a identidade real do participante (nome completo, CPF ou outro identificador) será mantida em documento separado do banco de dados principal, armazenada em local de acesso estritamente controlado pelo pesquisador principal. O acesso à lista de correspondência será permitido apenas em situações excepcionais (emergência clínica, solicitação judicial, auditoria pelo CEP) e devidamente registrado em livro de log. Citar: (Brasil, 2012; Brasil, 2018; World Medical Association, 2013).

**Parágrafo 2: Armazenamento físico dos documentos:**
Descrever que todos os documentos físicos (fichas de coleta impressas, TCLEs assinados, formulários de avaliação) serão armazenados em arquivo físico trancado, em sala de acesso restrito na instituição proponente, com acesso permitido exclusivamente ao pesquisador principal e aos membros da equipe formalmente autorizados e relacionados no protocolo do estudo submetido ao CEP. Os documentos serão mantidos pelo prazo mínimo de **cinco anos após o encerramento ou interrupção da pesquisa**, conforme exigido pela Resolução CNS nº 466/2012, item XIII.4. Transcorrido esse prazo, os documentos serão destruídos de forma segura (trituração ou incineração), garantindo a impossibilidade de recuperação das informações. Citar: (Brasil, 2012).

**Parágrafo 3: Armazenamento digital e segurança de dados eletrônicos:**
Descrever as medidas de segurança digital adotadas para o banco de dados eletrônico: proteção por senha individual intransferível para cada membro autorizado da equipe; criptografia dos arquivos do banco de dados (especificar algoritmo ou software, se conhecido); armazenamento em servidor institucional com política de segurança formalizada ou em plataforma de nuvem com autenticação de dois fatores e conformidade com a LGPD; realização de cópias de segurança (backups) periódicas, armazenadas em mídias distintas e locais fisicamente separados, com frequência mínima semanal. Descrever que a transferência de dados entre membros da equipe será realizada exclusivamente por meio de canais seguros (e-mail institucional criptografado, plataforma de compartilhamento seguro), sendo vedado o uso de dispositivos pessoais não autorizados. Citar: (Brasil, 2018; Society for Clinical Data Management, 2013; International Council for Harmonisation, 2016).

**Parágrafo 4: Conformidade com a LGPD e direitos do titular:**
Descrever a conformidade do estudo com a **Lei Geral de Proteção de Dados Pessoais (LGPD: Lei nº 13.709/2018)**, especialmente em relação ao tratamento de dados pessoais sensíveis (dados relativos à saúde). Indicar: a **base legal** para o tratamento dos dados (consentimento do titular, conforme art. 7º, I, e art. 11, I, da LGPD, formalizado por meio do TCLE; ou finalidade de pesquisa científica, conforme art. 7º, IV, e art. 11, II, "c", com aprovação do CEP); a identificação do **controlador** dos dados (instituição proponente ou pesquisador responsável) e do **operador** (quando houver empresa ou serviço terceirizado no tratamento); os **direitos assegurados ao titular** (acesso, correção, exclusão, portabilidade e revogação do consentimento, conforme art. 18 da LGPD), com indicação do canal pelo qual o participante poderá exercê-los. Citar: (Brasil, 2018; Brasil, 2012).

**Parágrafo 5: Disseminação dos resultados e proteção na publicação:**
Descrever que os resultados da pesquisa serão divulgados exclusivamente de forma agregada, sem qualquer informação que permita a identificação individual dos participantes. A publicação dos dados brutos (se prevista em repositório de dados abertos) será realizada apenas após anonimização completa e irreversível, e somente mediante aprovação do CEP para esse fim específico. Análises secundárias dos dados por pesquisadores não integrantes da equipe original dependerão de novo protocolo de pesquisa submetido ao CEP. Tanto participantes quanto instituições participantes serão protegidos de qualquer exposição não autorizada em publicações, relatórios técnicos, apresentações em congressos e materiais de divulgação científica. Citar: (Brasil, 2012; World Medical Association, 2013; Brasil, 2018).

Consultar `references/protecao-e-monitoramento.md` para requisitos detalhados da LGPD aplicados à pesquisa em saúde e modelos de frases.

---

## Fase 5: Seção 6.4: Critérios para suspender ou encerrar a pesquisa

### Instruções de redação

Redigir ao menos **quatro parágrafos** cobrindo obrigatoriamente todos os seguintes elementos, diferenciando com clareza **suspensão temporária** de **encerramento definitivo**:

**Parágrafo 1: Critérios de suspensão temporária:**
Descrever os critérios pré-estabelecidos que levarão à suspensão temporária da coleta de dados, com indicação de limites numéricos específicos quando aplicável:

- **Taxa de recrutamento insuficiente**: a pesquisa será temporariamente suspensa caso a taxa de recrutamento de participantes seja inferior à meta mínima pré-definida (ex.: menos de [N] participantes por semana) por [X] semanas consecutivas, indicando inviabilidade do protocolo nas condições vigentes. O pesquisador principal avaliará as causas da baixa adesão e poderá propor emendas ao protocolo, submetidas ao CEP para aprovação antes da retomada.
- **Taxa de eventos adversos acima do limiar**: qualquer evento adverso sério inesperado, ou taxa de eventos adversos que ultrapasse o limiar pré-especificado no protocolo (ex.: mais de [X]% de eventos de grau ≥ 3 pelo CTCAE v5.0 relacionados ao procedimento do estudo), determinará a suspensão imediata da coleta até avaliação pelo pesquisador principal, revisão pela equipe e, se indicado, pelo DSMB.
- **Falha sistemática de protocolo**: identificação de desvio sistemático do protocolo por um ou mais membros da equipe coletora que comprometa a qualidade ou a segurança dos dados coletados.
- **Nova evidência científica relevante**: surgimento de evidência publicada que coloque em dúvida a *equipoise* do estudo ou que indique risco desproporcional ao benefício para os participantes.

Citar: (Brasil, 2012; International Council for Harmonisation, 2016; DeMets et al., 2006).

**Parágrafo 2: Critérios de encerramento definitivo:**
Descrever os critérios que determinarão o encerramento definitivo e irreversível da pesquisa:

- **Perda integral dos dados**: o encerramento será determinado caso o arquivo eletrônico do banco de dados principal, protegido por senha e armazenado em diretório seguro, e **todos** os arquivos de cópia de segurança sejam danificados ou perdidos de forma irrecuperável, tornando impossível a recuperação das informações coletadas e inviabilizando a análise dos dados.
- **Decisão do CEP ou CONEP**: determinação expressa do Comitê de Ética em Pesquisa da instituição proponente ou da Comissão Nacional de Ética em Pesquisa (CONEP), em decorrência de irregularidades éticas, violação de direitos dos participantes ou por quaisquer outros motivos de interesse público.
- **Recomendação do DSMB (quando aplicável)**: recomendação formal do Comitê de Monitoramento de Dados (DSMB) pelo encerramento da pesquisa, em razão de risco desproporcional ao benefício, ineficácia inequívoca da intervenção ou benefício clínico tão evidente que torne antiético manter participantes no grupo controle.
- **Decisão regulatória (para ensaios clínicos)**: determinação da Agência Nacional de Vigilância Sanitária (ANVISA), do patrocinador ou de organismo regulador internacional competente, em caso de ensaios clínicos de fase I a III.
- **Inviabilidade institucional**: encerramento ou inabilitação da instituição proponente, perda de financiamento sem possibilidade de substituição, ou incapacidade da equipe de continuar o estudo sem substituição aprovada pelo CEP.

Citar: (Brasil, 2012; International Council for Harmonisation, 2016; Ellenberg et al., 2019; Moher et al., 2010).

**Parágrafo 3: Procedimento de notificação ao CEP:**
Descrever o procedimento formal de notificação ao Comitê de Ética em Pesquisa da instituição proponente em caso de suspensão ou encerramento: a notificação será submetida por meio do sistema **Plataforma Brasil** (CONEP/CNS/MS), no prazo máximo estabelecido pelo CEP (geralmente até 30 dias corridos após a decisão de suspender ou encerrar, ou imediatamente em casos de eventos adversos sérios inesperados), acompanhada de relatório circunstanciado contendo: descrição detalhada do motivo da suspensão ou encerramento, estágio do estudo no momento da decisão, número de participantes recrutados e status de cada um, medidas adotadas para proteger os participantes já incluídos e plano de gestão dos dados já coletados. Citar: (Brasil, 2012; Brasil, Ministério da Saúde, 2013).

**Parágrafo 4: Medidas de proteção dos participantes após suspensão ou encerramento:**
Descrever as providências que serão adotadas para proteção dos participantes já incluídos no estudo em caso de suspensão ou encerramento: comunicação individual a cada participante sobre a interrupção da pesquisa, orientações sobre a continuidade do cuidado clínico e indicação de serviço de referência para acompanhamento, quando aplicável; manutenção do sigilo e da confidencialidade dos dados já coletados pelo prazo legal mínimo de cinco anos; possibilidade de acesso dos participantes aos resultados individuais de avaliações realizadas, quando clinicamente relevante e solicitado pelo participante. Citar: (Brasil, 2012; World Medical Association, 2013).

Consultar `references/protecao-e-monitoramento.md` para modelos de frases por tipo de estudo e critérios numéricos de referência para suspensão.

---

## Fase 6: Lista de referências (ao final do capítulo)

Ao concluir a redação das quatro seções, gerar automaticamente a **lista de referências** do capítulo. A lista deve obedecer às seguintes regras:

- **Formato**: Vancouver (sobrenome, iniciais do nome. Título. Periódico ou Editora. Ano; volume(número):páginas. doi: [DOI]. Disponível em: [URL])
- **Ordem**: alfabética pelo primeiro elemento de entrada (sobrenome do primeiro autor ou nome do órgão institucional)
- **Completude**: incluir DOI quando disponível; incluir URL de acesso quando disponível; para legislação brasileira, indicar o Diário Oficial da União
- **Cobertura**: incluir todas as fontes citadas no texto no formato (Autor, ano)

### Lista de referências nucleares a incluir (adaptar e acrescentar conforme as seções redigidas):

Brasil. Conselho Nacional de Saúde. Resolução nº 466, de 12 de dezembro de 2012. Aprova as diretrizes e normas regulamentadoras de pesquisas envolvendo seres humanos. Diário Oficial da União, Brasília, DF, 13 jun. 2013; Seção 1:59. Disponível em: https://conselho.saude.gov.br/resolucoes/2012/Reso466.pdf

Brasil. Ministério da Saúde. Conselho Nacional de Saúde. Norma Operacional nº 001/2013 — CONEP. Dispõe sobre a organização e funcionamento do sistema CEP/CONEP. Brasília: Ministério da Saúde; 2013. Disponível em: https://conselho.saude.gov.br/web_comissoes/conep/aquivos/normativa/normaoperacional001_2013_conep.pdf

Brasil. Lei nº 13.709, de 14 de agosto de 2018. Lei Geral de Proteção de Dados Pessoais (LGPD). Diário Oficial da União, Brasília, DF, 15 ago. 2018. Disponível em: https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm

Council for International Organizations of Medical Sciences (CIOMS). International Ethical Guidelines for Health-related Research Involving Humans. 4th ed. Geneva: CIOMS; 2016. doi:10.56759/rgxl7429. Disponível em: https://cioms.ch/publications/product/international-ethical-guidelines-for-health-related-research-involving-humans/

International Council for Harmonisation (ICH). ICH E6(R2): Guideline for Good Clinical Practice. Geneva: ICH; 2016. Disponível em: https://www.ich.org/page/efficacy-guidelines

National Cancer Institute. Common Terminology Criteria for Adverse Events (CTCAE), Version 5.0. Bethesda (MD): US Department of Health and Human Services; 2017. Disponível em: https://ctep.cancer.gov/protocoldevelopment/electronic_applications/docs/CTCAE_v5_Quick_Reference_5x7.pdf

Society for Clinical Data Management (SCDM). Good Clinical Data Management Practices (GCDMP). Version 4.0. Milwaukee: SCDM; 2013. Disponível em: https://scdm.org/gcdmp/

World Medical Association. Declaration of Helsinki: Ethical Principles for Medical Research Involving Human Subjects. Fortaleza: WMA; 2013. Disponível em: https://www.wma.net/policies-post/wma-declaration-of-helsinki-ethical-principles-for-medical-research-involving-human-subjects/

---

## Fase 7: Entregáveis

Após apresentar o texto completo do Capítulo 6, inclua a seguinte mensagem ao final da resposta:

> "Capítulo 6 gerado. Use os botões abaixo para baixar o resultado nos formatos .md, .docx e .pdf."

O sistema gera os arquivos automaticamente — **não inclua scripts, código ou blocos de dependências na resposta.**

Para redigir o Capítulo 7 (Análise dos Riscos e dos Benefícios), utilize o skill `capitulo-riscos-beneficios`.

---

## Padrões de qualidade: checklist de revisão antes de entregar o texto

Antes de apresentar o capítulo ao usuário, verificar se **todos** os itens abaixo estão presentes e completos:

- [ ] As quatro seções numeradas (6.1, 6.2, 6.3, 6.4) estão presentes e com títulos explícitos
- [ ] Seção 6.1: procedimentos descritos com especificidade suficiente; risco classificado (mínimo / menor que o mínimo / maior que o mínimo); protocolo de treinamento mencionado; canal de comunicação com o participante descrito; direito de retirada explicitado
- [ ] Seção 6.1: para populações vulneráveis: salvaguardas específicas descritas
- [ ] Seção 6.1: protocolo de eventos adversos com definição, grau (CTCAE) e notificação ao CEP
- [ ] Seção 6.2: dupla entrada de dados descrita com processo de resolução de discordâncias; software especificado
- [ ] Seção 6.2: verificações automáticas de consistência (*range checks*, *logic checks*) descritas; frequência da auditoria indicada
- [ ] Seção 6.2: DSMB descrito (composição, frequência, regras de parada) ou ausência justificada
- [ ] Seção 6.3: pseudonimização descrita (código alfanumérico; lista de correspondência separada)
- [ ] Seção 6.3: armazenamento físico descrito (arquivo trancado, acesso restrito, prazo mínimo de 5 anos)
- [ ] Seção 6.3: armazenamento digital descrito (senha, criptografia, backup periódico)
- [ ] Seção 6.3: conformidade com a LGPD mencionada (base legal, controlador, direitos do titular)
- [ ] Seção 6.3: proteção na publicação descrita (resultados agregados, sem identificação)
- [ ] Seção 6.4: critérios de suspensão temporária com limites numéricos específicos (meta de recrutamento, limiar de eventos adversos)
- [ ] Seção 6.4: critérios de encerramento definitivo (perda de dados, decisão do CEP/CONEP, DSMB, regulatório, institucional)
- [ ] Seção 6.4: procedimento de notificação ao CEP via Plataforma Brasil descrito
- [ ] Seção 6.4: medidas de proteção dos participantes após encerramento descritas
- [ ] Citações integradas ao texto no formato **(Autor, ano)** em todas as afirmações que requerem fundamentação
- [ ] Lista de referências ao final do capítulo em ordem **alfabética**, estilo **Vancouver**, com **DOI** e **URL** quando disponíveis
- [ ] Nenhuma seção genérica ou com marcador de posição ("[inserir aqui]", "a definir", etc.); limites numéricos preenchidos ou indicados claramente ao usuário se faltarem informações
- [ ] Texto integralmente em **português brasileiro formal**, no **futuro do indicativo**
- [ ] Ausência de primeira pessoa do singular ("Eu realizarei" deve ser "será realizado")
- [ ] Todas as palavras e expressões em outros idiomas grafadas em **itálico**
- [ ] Ausência de travessões (—) em todo o texto redigido
- [ ] **Geração de arquivos** (Fase 7): pandoc verificado; arquivo `.md` salvo; `.docx` gerado; `.pdf` gerado; caminhos completos confirmados ao usuário; aluno orientado a usar `capitulo-riscos-beneficios` para o Capítulo 7

---

## Referências de suporte

O arquivo de referência desta skill (carregado sob demanda com a ferramenta Read) contém:

- `references/protecao-e-monitoramento.md`: classificação de risco CNS 466/12 com exemplos práticos; tabela de graus CTCAE v5.0; checklist de qualidade de dados; componentes do DSMB e modelos de regras de parada (O'Brien-Fleming, Pocock); requisitos LGPD aplicados à pesquisa em saúde; modelos de frases para cada subseção (6.1 a 6.4) em diferentes cenários de estudo (ensaio clínico, observacional, qualitativo); lista de referências Vancouver completa com DOI e URL


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
