---
name: capitulo-metodos
description: Redigir o capítulo de Métodos de um projeto de pesquisa científica em português brasileiro. Usar quando o usuário solicitar "escrever métodos", "capítulo de métodos", "metodologia", "seção de métodos", "redija os métodos", "escreva a metodologia" ou descrever um estudo e pedir para redigir. A skill levanta as informações do estudo via perguntas estruturadas, adapta o texto ao tipo de delineamento (ensaio clínico randomizado, não randomizado, coorte, caso-controle, transversal, qualitativo, misto) e redige cada seção numerada com linguagem acadêmica formal, referências metodológicas publicadas e conformidade com a legislação brasileira de pesquisa com seres humanos (Resolução CNS 466/12, 510/16, Declaração de Helsinki).
version: 1.0.0
argument-hint: [descrição-resumida-do-estudo]

---

# Capítulo de Métodos — Skill de Redação Acadêmica

## Objetivo

Produzir o capítulo de Métodos completo e numerado de um projeto de pesquisa científica em português brasileiro formal, seguindo a estrutura obrigatória definida pelo usuário, fundamentado em guidelines internacionais de relato (CONSORT 2010, STROBE, PRISMA 2020, TREND) e na legislação brasileira de ética em pesquisa com seres humanos.

O texto deve ser redigido no **futuro do indicativo** ("será avaliado", "serão incluídos", "utilizará") por se tratar de um projeto de pesquisa ainda a ser executado. A linguagem é acadêmica formal, sem coloquialismos, com referências bibliográficas integradas ao texto (formato Vancouver ou ABNT, conforme preferência da instituição).

---

## Fase 1 — Levantamento das informações do estudo

Se o usuário não tiver fornecido as informações abaixo, solicitar **antes de iniciar a redação**. Apresentar as perguntas de forma organizada e amigável, em um único bloco, para que o usuário possa responder tudo de uma vez:

1. **Título provisório ou tema** do estudo
2. **Tipo de delineamento** (ensaio clínico randomizado, não randomizado, estudo de coorte, caso-controle, transversal, qualitativo, revisão sistemática, misto — ou outro)
3. **Área de saúde / especialidade** (cardiologia, oncologia, saúde coletiva, fisioterapia, enfermagem, etc.)
4. **Local do estudo**: nome da instituição, tipo de serviço (hospital terciário, UBS, ambulatório especializado, comunidade), cidade e estado
5. **População-alvo**: quem serão os participantes (adultos com diabetes tipo 2, crianças com asma, puérperas, idosos institucionalizados, etc.)
6. **Critérios de inclusão** (quem pode participar — lista de características exigidas)
7. **Critérios de exclusão** (quem não pode participar — contraindicações, limitações)
8. **Intervenção ou exposição** (se houver): descrição da intervenção, dose, frequência, duração, via; e o que o grupo controle receberá (placebo, cuidado padrão, comparador ativo)
9. **Desfecho primário**: a variável principal que será medida (com unidade e instrumento de medição, se conhecido)
10. **Desfechos secundários e dados complementares** (variáveis secundárias e covariáveis)
11. **Método de randomização** (se RCT): simples, em blocos, estratificada, minimização — e ocultação da alocação
12. **Mascaramento** (se aplicável): aberto, simples-cego, duplo-cego, triplo-cego — e quem será mascarado
13. **Tamanho amostral estimado** (se já calculado) e os parâmetros usados (α, poder, DMCR, DP, perda esperada)
14. **Testes estatísticos** pretendidos e software de análise
15. **Cronograma previsto**: datas aproximadas de início e fim da coleta

Se o usuário já forneceu contexto suficiente no prompt, aproveitar as informações disponíveis e perguntar apenas o que estiver faltando ou que for ambíguo.

---

## Fase 2 — Parágrafo inicial de ética (obrigatório, antes das seções numeradas)

Redigir **sempre** como primeiro parágrafo do capítulo, antes da seção "1. Tipo de estudo". Este parágrafo não é numerado.

**Conteúdo obrigatório:**
- O estudo somente terá início após aprovação pelo **Comitê de Ética em Pesquisa (CEP)** da instituição proponente, via **Plataforma Brasil**
- Conformidade com a **Resolução nº 466, de 12 de dezembro de 2012, do Conselho Nacional de Saúde (CNS/MS)** — norma central que regulamenta pesquisa com seres humanos no Brasil
- Para pesquisas em ciências humanas, sociais ou humanas aplicadas: citar também a **Resolução CNS nº 510, de 7 de abril de 2016**
- Observância aos princípios éticos da **Declaração de Helsinki** (World Medical Association, 2013)
- Para ensaios clínicos: mencionar o **registro prospectivo** em base de dados de ensaios clínicos (**ReBEC** — Registro Brasileiro de Ensaios Clínicos, ou **ClinicalTrials.gov**)
- Todos os participantes receberão informações completas sobre o estudo e assinarão o **Termo de Consentimento Livre e Esclarecido (TCLE)**

**Modelo de referência para redação:**

"O presente estudo será submetido ao Comitê de Ética em Pesquisa (CEP) [nome da instituição] por meio do sistema Plataforma Brasil (CONEP/CNS/MS) e somente terá início após a emissão do parecer favorável. A pesquisa será conduzida em estrita observância à Resolução nº 466, de 12 de dezembro de 2012, do Conselho Nacional de Saúde (CNS/MS), que estabelece as diretrizes e normas regulamentadoras de pesquisas envolvendo seres humanos no Brasil, e aos princípios éticos enunciados na Declaração de Helsinki (World Medical Association, 2013). [Para ensaios clínicos: O estudo será registrado prospectivamente no Registro Brasileiro de Ensaios Clínicos (ReBEC), conforme recomendação da Organização Mundial da Saúde (OMS) e exigência de periódicos científicos indexados.] Todos os participantes ou seus responsáveis legais receberão esclarecimentos detalhados sobre os objetivos, procedimentos, riscos e benefícios da pesquisa, sendo a participação condicionada à assinatura do Termo de Consentimento Livre e Esclarecido (TCLE)."

Adaptar o modelo ao tipo de estudo, instituição e população específicas. Consultar `references/etica-e-regulamentacao.md` para detalhes sobre CONEP, LGPD e populações vulneráveis.

---

## Fase 3 — Seção 1: Tipo de estudo

Classificar o delineamento em **todas** as seguintes dimensões:
- **Quanto ao objetivo:** exploratório, descritivo ou analítico/explicativo
- **Quanto à abordagem:** quantitativo, qualitativo ou misto
- **Quanto ao procedimento:** experimental (intervencionista) ou observacional
- **Quanto à temporalidade:** transversal (cross-sectional), prospectivo, retrospectivo ou longitudinal

Para **ensaios clínicos randomizados**: especificar número de grupos, tipo de controle (placebo, comparador ativo, sem tratamento), paralelismo ou crossover, e fase do ensaio (I, II, III, IV), se pertinente.

Ao final da seção, indicar o **guideline de relato** que orientará a apresentação dos resultados:
- **CONSORT 2010** (Consolidated Standards of Reporting Trials) — para RCTs
- **STROBE** (Strengthening the Reporting of Observational Studies in Epidemiology) — para coorte, caso-controle, transversal
- **PRISMA 2020** (Preferred Reporting Items for Systematic reviews and Meta-Analyses) — para revisões sistemáticas
- **TREND** (Transparent Reporting of Evaluations with Nonrandomized Designs) — para intervenções não randomizadas
- **COREQ** ou **SRQR** — para estudos qualitativos

Referências: Hulley SB et al. *Delineando a Pesquisa Clínica*, 4ª ed., 2015; Fontelles MJ et al., Rev Assoc Med Bras 2009; Moher D et al. (CONSORT 2010), BMJ 2010; von Elm E et al. (STROBE), Lancet 2007; Page MJ et al. (PRISMA 2020), BMJ 2021.

Consultar `references/tipos-de-estudo.md` para checklists completos de cada guideline e tabela de correspondência delineamento × guideline.

---

## Fase 4 — Seção 2: Local

Redigir parágrafo descrevendo:
- Nome e tipo da instituição (hospital universitário, hospital público, UBS, ambulatório de especialidade, comunidade, domicílio)
- Nível de atenção (primário, secundário, terciário)
- Cidade e estado
- Capacidade instalada e perfil da clientela atendida (relevante para justificar a adequação da instituição ao estudo)
- Vínculo do pesquisador principal com a instituição
- **Período de coleta de dados**: mês/ano de início previsto até mês/ano de término estimado

---

## Fase 5 — Seção 3: Amostra

### 3.1 Critérios de inclusão

Apresentar em lista com marcadores. Cada critério deve ser:
- **Objetivo e verificável** (mensurável, não subjetivo)
- **Diretamente relacionado** à pergunta de pesquisa (framework PICO)

Incluir tipicamente: faixa etária, sexo/gênero (quando relevante), diagnóstico/condição (com código CID-10, DSM-5 ou critérios diagnósticos validados), capacidade de fornecer consentimento, demais condições clínicas ou laboratoriais necessárias.

Evitar critérios vagos como "bom estado geral" ou "compreensão satisfatória" — especificar como isso será avaliado.

### 3.2 Critérios de exclusão

Apresentar em lista com marcadores. **Não repetir a negação dos critérios de inclusão** (erro metodológico comum).

Os critérios de exclusão devem refletir circunstâncias que, mesmo na presença dos critérios de inclusão, **impedem a participação segura ou comprometem a validade dos dados**:
- Contraindicações clínicas à intervenção
- Uso de medicamentos com potencial interferência no desfecho
- Gestação ou lactação (se clinicamente relevante)
- Participação concomitante em outro ensaio clínico
- Impossibilidade de seguimento pelo período do estudo (mudança de cidade, transferência)
- Recusa em assinar o TCLE

### 3.3 Amostragem

Descrever:
1. **Método de seleção dos participantes**:
   - *Probabilístico*: aleatória simples (sorteio), sistemática (a cada k elementos), estratificada (por variável de estratificação) ou por conglomerados
   - *Não probabilístico*: conveniência (pacientes disponíveis no período), intencional/proposital, bola de neve (redes de indicação, para populações de difícil acesso)
2. **Fluxo de recrutamento**: onde e como os participantes serão identificados e abordados
3. **Tamanho amostral calculado**: citar o n total e o n por grupo (se aplicável), remetendo o detalhamento do cálculo à **seção 6.1**
4. **Para RCTs**: descrever o fluxo CONSORT esperado (elegíveis avaliados → excluídos → randomizados → alocados → seguidos → analisados), que será apresentado graficamente nos resultados

### 3.4 Consentimento livre e esclarecido

Descrever o processo de obtenção do TCLE, conforme a **Resolução CNS 466/12, Capítulo IV**:
- **Quem apresentará** o TCLE: pesquisador responsável ou equipe treinada (nunca profissional em posição de autoridade sobre o participante, para evitar coerção)
- **Como será apresentado**: leitura conjunta, linguagem acessível, possibilidade de perguntas, tempo adequado para reflexão antes da assinatura
- **Voluntariedade**: enfatizar que a recusa ou retirada não acarretará prejuízo ao atendimento ou à relação com a instituição
- **Confidencialidade**: os dados serão identificados por código, armazenados em local seguro, acessíveis apenas à equipe de pesquisa; mencionar **LGPD (Lei nº 13.709/2018)** se dados forem armazenados digitalmente
- **Para menores de 18 anos**: assentimento do menor (adequado à faixa etária) + consentimento do responsável legal
- **Para populações vulneráveis** (pessoas com déficit cognitivo, idosos com demência, presos, gestantes): descrever salvaguardas adicionais conforme Resolução CNS 466/12, item II.6

Consultar `references/etica-e-regulamentacao.md` para modelos de TCLE e situações especiais.

---

## Fase 6 — Seção 4: Procedimentos

### 4.1 Grupos estudados

Descrever cada grupo de forma completa e simétrica (o leitor deve conseguir replicar o estudo):
- **Grupo intervenção**: nome da intervenção, dose, frequência de aplicação, duração total, via de administração, operador (quem aplica), local de administração
- **Grupo controle**: descrição detalhada (placebo — forma, aparência idêntica, ou cuidado padrão, ou comparador ativo)
- **Cronograma de avaliações**: visita basal (baseline/T0), avaliações intermediárias (T1, T2...) e avaliação final/desfecho — com intervalo exato de tempo
- **Para estudos observacionais**: descrever os grupos de exposição ou o critério diagnóstico que define casos e controles; período de seguimento (para coortes)

Consultar `references/tipos-de-estudo.md` para especificidades de cada delineamento.

### 4.2 Randomização

**Se o delineamento for um RCT ou ensaio com componente de randomização:**

Descrever os três componentes obrigatórios do CONSORT 2010:

1. **Geração da sequência aleatória** (item 8a do CONSORT):
   - Método computadorizado: software R (`blockrand`, `randomizeR`), SAS PROC PLAN, plataforma online (Sealed Envelope, ALEA) — especificar qual
   - Tipo: simples, em blocos permutados (tamanho do bloco: fixo ou variável — preferir variável para dificultar predição), estratificada por variáveis prognósticas relevantes (centro, sexo, gravidade), minimização
   - Razão de alocação: 1:1 (padrão), 2:1 ou outra — justificar se diferente de 1:1

2. **Ocultação da alocação** (item 9 do CONSORT — *allocation concealment*):
   - Envelopes opacos, selados e numerados sequencialmente (preparados por pessoa não envolvida na alocação)
   - Sistema centralizado de randomização por telefone/internet (IVRS/IWRS) — padrão-ouro
   - Farmácia central com embalagens codificadas
   - Descrever exatamente *quem* custódia a lista de randomização (bioestatístico independente, serviço externo) e como ela fica protegida até o final do estudo

3. **Implementação** (item 10 do CONSORT):
   - Quem gerou a sequência
   - Quem fez o recrutamento/elegibilidade
   - Quem atribuiu os participantes aos grupos
   - (Esses três papéis devem ser exercidos por pessoas diferentes, quando possível)

Referências: Schulz KF, Grimes DA. Generation of allocation sequences in randomised trials: chance, not choice. *Lancet* 2002;359:515-9; Moher D et al. CONSORT 2010. *BMJ* 2010;340:c332.

**Se o estudo NÃO incluir randomização:**
Explicar o delineamento adotado e as estratégias metodológicas para controle de confundimento: pareamento (individual ou por frequência), restrição de critérios, estratificação na análise, modelagem multivariada (regressão logística, propensity score matching).

### 4.3 Mascaramento

**Se aplicável:**

Especificar:
- **Tipo**: aberto (open-label, sem mascaramento), simples-cego (participante), duplo-cego (participante + equipe ou avaliador), triplo-cego (participante + equipe + analista estatístico)
- **Quem é mascarado**: participantes, equipe de tratamento, avaliadores de desfechos, analista estatístico
- **Método operacional**: aparência, forma e sabor idênticos do placebo ao produto ativo; embalagem com código alfanumérico; avaliação de desfechos por profissional que não participou da administração da intervenção; lista de codes mantida pelo farmacêutico responsável
- **Procedimento de quebra de cegamento** (*unblinding*): em caso de emergência clínica — quem aciona, como, quais dados são documentados

Referência: Schulz KF, Grimes DA. Blinding in randomised trials: hiding who got what. *Lancet* 2002;359:696-700; CONSORT 2010, item 11.

**Se não aplicável:**
Justificar a impossibilidade (intervenção não mascarável, como exercício físico ou cirurgia) e descrever as medidas adotadas para minimizar o viés de aferição: avaliador de desfechos cego para a alocação, utilização de desfechos objetivos (laboratoriais, por imagem), comitê de adjudicação de desfechos independente.

---

## Fase 7 — Seção 5: Variáveis

Para cada variável (primária, secundárias e complementares), descrever os seguintes atributos em texto corrido ou tabela:

| Atributo | O que descrever |
|---|---|
| **Definição conceitual** | O que a variável representa clinicamente / teoricamente |
| **Definição operacional** | Como será medida na prática (procedimento exato) |
| **Instrumento de medição** | Questionário (citar validação para pt-BR), equipamento (marca/modelo/versão), exame laboratorial (método), imagem (equipamento/protocolo) |
| **Escala de medida** | Nominal, ordinal, intervalar ou razão (contínua) |
| **Ponto/momento de aferição** | Baseline (T0), após intervenção (T1), follow-up (T2, T3...) — com intervalo exato |
| **Responsável pela aferição** | Pesquisador cego à alocação, avaliador externo, autorrelato do participante |

### 5.1 Variável primária (desfecho primário)

É o desfecho que fundamenta o cálculo do tamanho amostral (seção 6.1) e o objetivo principal do estudo. Deve ser **um único desfecho primário** bem definido.

Descrever todos os atributos listados acima. Citar a validação do instrumento para a população brasileira, quando existente. Se o instrumento for original (desenvolvido pela equipe), descrever o processo de validação ou citar que será validado antes da coleta.

### 5.2 Variáveis secundárias (desfechos secundários)

Listar todos os desfechos secundários com a mesma estrutura da seção 5.1. Para clareza, apresentar em formato de lista numerada ou tabela. Justificar brevemente a relevância clínica de cada variável com base em literatura prévia.

Alertar no texto que as análises secundárias serão exploratórias e interpretadas com cautela, dado o maior risco de erro tipo I por múltiplas comparações (mencionar correção de Bonferroni ou FDR se for o caso).

### 5.3 Dados complementares (covariáveis e variáveis de controle)

Listar as variáveis sociodemográficas e clínicas coletadas para caracterização da amostra e controle de confundimento:

**Variáveis sociodemográficas** (seguir padrão IBGE):
- Idade (anos completos)
- Sexo (masculino/feminino — variável biológica) e gênero (se pertinente — conforme autodeclaração)
- Cor/raça (branca, preta, parda, amarela, indígena — IBGE)
- Escolaridade (anos de estudo completos ou categorias do IBGE)
- Renda familiar (salários mínimos mensais)
- Situação conjugal, profissão, município de residência — conforme relevância

**Variáveis clínicas de base:**
- Comorbidades relevantes (com CID-10)
- Medicamentos em uso (especificar aqueles com potencial interação)
- Tempo de diagnóstico da condição-índice
- Exames laboratoriais basais pertinentes

**Variáveis de processo** (para ensaios clínicos):
- Aderência à intervenção (método de verificação: diário, contagem de comprimidos, marcador biológico)
- Cointervenções (tratamentos não protocolados recebidos durante o estudo)
- Eventos adversos — como serão registrados e classificados (Common Terminology Criteria for Adverse Events — CTCAE, se aplicável)

---

## Fase 8 — Seção 6: Análise Estatística

### 6.1 Cálculo do tamanho da amostra

Descrever **todos** os parâmetros utilizados no cálculo. Um texto completo deve conter:

1. **Desfecho primário** que embasou o cálculo
2. **Tipo de hipótese testada**: superioridade, não-inferioridade ou equivalência
3. **Diferença mínima clinicamente relevante (DMCR)** entre grupos — valor numérico + justificativa clínica + fonte bibliográfica
4. **Desvio-padrão esperado** (para desfechos contínuos) ou **proporção esperada de eventos** (para desfechos dicotômicos) — citar fonte (estudo piloto próprio, literatura, dados históricos da instituição)
5. **Nível de significância (α)**: 0,05 (bilateral, padrão) — explicitar se unilateral e justificar
6. **Poder estatístico (1−β)**: 0,80 (80%) ou 0,90 (90%) — justificar a escolha
7. **Razão de alocação** entre grupos (se diferente de 1:1)
8. **N calculado** por grupo e **N total** antes do ajuste por perdas
9. **Taxa de perda/abandono esperada**: acrescentar 15–25% ao n calculado (justificar com base na literatura ou experiência local)
10. **N total final** (após ajuste por perdas)
11. **Software ou fórmula utilizada**: G*Power 3.1 (Faul F et al., 2009), PASS (NCSS, LLC), OpenEpi, pacote `pwr` do R — citar versão e referência do software

Referências metodológicas a citar: Cohen J. *Statistical Power Analysis for the Behavioral Sciences*, 2ª ed., 1988; Lwanga SK, Lemeshow S. *Sample size determination in health studies*. WHO, 1991; Faul F et al. G*Power 3. *Behav Res Methods* 2009;41(4):1149-60.

Consultar `references/analise-estatistica.md` para fórmulas por tipo de estudo e desfecho.

### 6.2 Análise estatística

**Estratégia geral de análise:**
- Para RCTs: análise **por intenção de tratar (intention-to-treat, ITT)** como análise primária — todos os participantes randomizados são incluídos nos grupos aos quais foram alocados, independentemente da adesão. Análise **por protocolo (per-protocol)** como análise de sensibilidade (apenas participantes que completaram o protocolo conforme previsto)
- Para estudos observacionais: análise completa dos casos disponíveis (complete case analysis) como análise principal, com análise de sensibilidade por imputação múltipla se a proporção de dados ausentes for > 5%

**Estatística descritiva:**
- Variáveis contínuas com **distribuição normal**: média ± desvio-padrão (DP)
- Variáveis contínuas com **distribuição não normal**: mediana [intervalo interquartil — IQR: percentil 25–75]
- Variáveis categóricas: frequências absolutas (n) e relativas (%)
- Avaliação da normalidade: **teste de Shapiro-Wilk** para amostras pequenas (n ≤ 50) e **Kolmogorov-Smirnov** para amostras maiores, complementado por análise visual de histogramas e gráficos Q-Q

**Comparação entre grupos (selecionar conforme o tipo de variável e distribuição):**

| Situação | Teste paramétrico | Teste não paramétrico |
|---|---|---|
| 2 grupos independentes — variável contínua | Teste t de Student independente | Mann-Whitney U |
| ≥ 3 grupos independentes — variável contínua | ANOVA de uma via + post-hoc Tukey/Bonferroni | Kruskal-Wallis + post-hoc de Dunn |
| 2 grupos pareados — variável contínua | Teste t de Student pareado | Wilcoxon pareado |
| Variável categórica — amostras independentes | Qui-quadrado de Pearson | Exato de Fisher (n esperado < 5) |
| Medidas repetidas ao longo do tempo | ANOVA de medidas repetidas | Friedman |
| Dados longitudinais com perdas diferenciais | Modelo linear misto (*mixed models*) | — |

**Análise de correlação:**
- Pearson (variáveis contínuas, distribuição normal)
- Spearman (variáveis ordinais ou contínuas sem normalidade)

**Análise multivariada** (especificar conforme o desfecho):
- Regressão linear múltipla — desfecho contínuo
- Regressão logística binária — desfecho dicotômico (OR com IC 95%)
- Regressão de Cox — desfecho de sobrevivência/tempo até evento (HR com IC 95%)
- Regressão de Poisson robusta — desfecho dicotômico com alta prevalência (> 10%), para estimar RP em vez de OR

Variáveis incluídas no modelo multivariado: aquelas com p < 0,20 na análise bivariada ou com relevância clínica estabelecida na literatura (a despeito do p).

**Parâmetros de significância:**
- Nível de significância: **α = 0,05** (bilateral)
- Intervalos de confiança: **95% (IC 95%)**

**Dados ausentes (*missing data*):**
- Classificação prévia da natureza das perdas: MCAR (*Missing Completely at Random*), MAR (*Missing at Random*), MNAR (*Missing Not at Random*)
- Estratégia: complete case analysis para < 5% de dados ausentes; imputação múltipla (*multiple imputation by chained equations*, pacote `mice` do R) para ≥ 5%, com sensibilidade reportada

**Software de análise estatística:**
Informar o software, versão e fabricante. Exemplo: "As análises serão realizadas com o programa Statistical Package for the Social Sciences (SPSS Statistics, versão XX.X, IBM Corp., Armonk, NY, EUA) / R (versão X.X.X, R Core Team, 2024), adotando-se nível de significância de 5% para todos os testes."

Consultar `references/analise-estatistica.md` para fórmulas, tabela de escolha de testes e interpretação dos tamanhos de efeito.

### 6.3 Apresentação dos resultados

Descrever como os resultados serão estruturados no artigo ou relatório:

- Seguir as recomendações do **guideline de relato** indicado na seção 1 (CONSORT, STROBE, PRISMA, TREND)
- **Para RCTs**: apresentar o **diagrama de fluxo CONSORT** (participantes avaliados para elegibilidade → excluídos com motivos → randomizados → alocados por grupo → perdas com motivos → analisados)
- **Tabela 1 — Características basais dos grupos**: variáveis sociodemográficas e clínicas apresentadas por grupo; para RCTs, sem p-valor (diferenças basais após randomização são fruto do acaso); para estudos observacionais, com p-valor e tamanho de efeito
- **Resultados primários e secundários**: apresentar com estatística descritiva (média ± DP ou mediana [IQR]), estimativa do efeito (diferença de médias, OR, RR, HR), IC 95% e p-valor
- **Relevância clínica**: além da significância estatística, apresentar o **tamanho de efeito** (d de Cohen, r de Pearson, NNT — número necessário para tratar, ou NNH — número necessário para causar dano), para interpretar a magnitude clínica dos achados
- **Figuras recomendadas**: diagrama de fluxo, gráficos de caixa (boxplots) para variáveis contínuas, curvas de Kaplan-Meier para análises de sobrevivência, forest plots para subgrupos ou meta-análise

---

## Padrões de qualidade — checklist de revisão antes de entregar o texto

Antes de apresentar o capítulo ao usuário, verificar se **todos** os itens abaixo estão presentes e completos:

- [ ] Parágrafo de ética presente antes da seção 1 (mencionando CEP, Resolução 466/12, Helsinki, TCLE)
- [ ] Para RCT: menção ao registro em ReBEC ou ClinicalTrials.gov
- [ ] Todas as 6 seções numeradas presentes, com **todas as subseções** (3.1 a 3.4, 4.1 a 4.3, 5.1 a 5.3, 6.1 a 6.3)
- [ ] Nenhuma seção genérica ou com marcador de posição ("[inserir aqui]", "a definir", etc.)
- [ ] Tipo de estudo classificado em todas as dimensões (objetivo, abordagem, procedimento, temporalidade)
- [ ] Guideline de relato identificado e citado
- [ ] Critérios de inclusão e exclusão sem sobreposição lógica e sem critérios vagos
- [ ] Para RCT: randomização descrita com (a) método de geração, (b) ocultação da alocação, (c) implementação
- [ ] Para RCT: mascaramento descrito com tipo, quem é mascarado e método operacional
- [ ] Variável primária com definição operacional + instrumento validado + momento de aferição + responsável
- [ ] Cálculo amostral com TODOS os parâmetros (α, poder, DMCR, DP/proporção, fonte, taxa de perda, n final, software)
- [ ] Testes estatísticos escolhidos e justificados conforme tipo de variável e distribuição esperada
- [ ] Software de análise estatística especificado com versão
- [ ] Referências metodológicas integradas ao texto (formato Vancouver: sobrenome et al., periódico, ano)
- [ ] Texto integralmente em **português brasileiro formal**, no **futuro do indicativo**
- [ ] Ausência de primeira pessoa do singular ("Eu realizarei" → "será realizado")
- [ ] Coerência interna: o n da seção 3.3 coincide com o n da seção 6.1; os grupos da seção 4.1 correspondem às variáveis da seção 5

---

## Referências de suporte

Os arquivos de referência desta skill (carregados sob demanda com a ferramenta Read) contêm:

- `references/etica-e-regulamentacao.md` — Resolução 466/12, 510/16, Norma Operacional 001/2013, Declaração de Helsinki, LGPD, CONEP, Plataforma Brasil, ReBEC, modelos de TCLE
- `references/tipos-de-estudo.md` — pirâmide de evidências, checklists CONSORT/STROBE/PRISMA/TREND/COREQ, vantagens e limitações por delineamento, tabela delineamento × guideline × registro obrigatório
- `references/analise-estatistica.md` — fórmulas de cálculo amostral, tabela de escolha de testes estatísticos, interpretação de tamanhos de efeito, abordagem de dados ausentes, imputação múltipla, comandos R e SPSS

---

## Geração de Arquivos (automática, após o checklist)

Imediatamente após a entrega do capítulo completo e do checklist de qualidade, gerar os
três arquivos sem aguardar novo comando do pesquisador. [O sistema gerará o arquivo para download]
nome base: `capitulo-02-metodos_[AAAAMMDD]`

**Dependências — verificar e instalar antes de gerar:**
```
python-docx   → pip install python-docx
docx2pdf      → pip install docx2pdf
```
Fallback para PDF: `reportlab` → pip install reportlab

**Ordem de geração:**
1. Salvar o texto completo do capítulo em `capitulo-02-metodos_[AAAAMMDD].md`
2. Gerar `capitulo-02-metodos_[AAAAMMDD].docx` com python-docx:
   - Fonte Calibri 11pt corpo; título "Capítulo 2. Métodos" Calibri bold 14pt azul `#1F497D`
   - Subtítulos das seções (2.1 a 2.6) Calibri bold 12pt azul `#1F497D`
   - Margens 2,5 cm superior/inferior e 3 cm esquerda/direita; espaçamento 1,5 entre linhas
   - Cabeçalho: título do projeto + "Capítulo 2. Métodos"; rodapé: numeração centralizada
3. Converter `[nome-base].docx` → `[nome-base].pdf` com docx2pdf; se falhar, usar reportlab
4. Remover o script Python temporário
5. Confirmar ao pesquisador os três caminhos completos dos arquivos gerados

---

## ◈ PRÓXIMO PASSO

Após confirmar os arquivos gerados, apresentar o bloco abaixo ao pesquisador:

```
=========================================================
BLOCO DE CONTEXTO PORTÁTIL — Capítulo 2. Métodos
=========================================================
Título              : [título do projeto]
Delineamento        : [tipo de estudo]
Local               : [instituição, cidade, estado]
População           : [descrição da população-alvo]
Critérios inclusão  : [síntese]
Critérios exclusão  : [síntese]
Intervenção/Exposição: [descrição ou "não se aplica"]
Desfecho primário   : [variável principal]
Tamanho amostral    : [n calculado ou estimado]
Análise estatística : [testes previstos]
Período coleta      : [início previsto — término previsto]
Métodos gerado em   : [data]
=========================================================
```

Orientar: "Salve o bloco acima. Ele será solicitado no início da próxima etapa e
garante que as Etapas, o Cronograma, os Materiais e o Orçamento sejam elaborados
com total coerência com o que foi definido nos Métodos."

> "Com o Capítulo 2 aprovado, as próximas seções a serem redigidas são as Etapas da
> pesquisa (3.1), o Cronograma de execução (3.2), os Materiais necessários (Capítulo 4)
> e o Orçamento detalhado (Capítulo 5).
>
> **Próxima etapa:** solicite a skill `/etapas-e-cronograma` e cole o Bloco de Contexto
> Portátil gerado ao final desta etapa no início da sua mensagem."


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
