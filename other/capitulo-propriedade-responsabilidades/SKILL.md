---
name: capitulo-propriedade-responsabilidades
description: Redigir o Capítulo 8 (Propriedades da Informação e Divulgação da Pesquisa), o Capítulo 9 (Responsabilidades do Pesquisador, da Instituição, do Promotor e do Patrocinador) e o Capítulo 10 (Utilização de Grupos Vulneráveis) de um projeto de pesquisa científica em português brasileiro. Usar quando o usuário solicitar "propriedade intelectual", "direitos autorais", "divulgação dos resultados", "publicação de dados", "responsabilidades do pesquisador", "responsabilidades da instituição", "promotor", "patrocinador", "grupos vulneráveis", "capítulo 8", "capítulo 9", "capítulo 10" ou similares. A skill levanta as informações do estudo via perguntas estruturadas e redige os três capítulos com linguagem acadêmica formal, citações bibliográficas integradas no formato (Autor, ano) e lista de referências Vancouver com DOI e URL ao final, em conformidade com a Resolução CNS 466/12, Lei 9.610/1998, Lei 10.973/2004, LGPD, CIOMS 2016 e Declaração de Helsinki 2013.
version: 1.0.0
argument-hint: [descrição-resumida-do-estudo]

---

# Capítulos 8, 9 e 10. Propriedades, Responsabilidades e Grupos Vulneráveis. Skill de Redação Acadêmica

## Objetivo

Produzir o **Capítulo 8. Propriedades da Informação e Divulgação da Pesquisa**, o **Capítulo 9. Responsabilidades do Pesquisador, da Instituição, do Promotor e do Patrocinador** e o **Capítulo 10. Utilização de Grupos Vulneráveis** de um projeto de pesquisa científica em português brasileiro formal.

O **Capítulo 8** abrange três seções: **8.1 Direitos de propriedade intelectual**, **8.2 Plano de divulgação dos resultados** e **8.3 Publicação de dados**. Fundamenta-se na Lei de Direitos Autorais (Lei nº 9.610/1998), na Lei de Inovação (Lei nº 10.973/2004), na Resolução CNS 466/12, nas Diretrizes do ICMJE e nos Princípios FAIR (Wilkinson et al., 2016).

O **Capítulo 9** abrange quatro seções: **9.1 Responsabilidades do pesquisador**, **9.2 Responsabilidades da instituição**, **9.3 Responsabilidades do promotor** e **9.4 Responsabilidades do patrocinador**. Fundamenta-se na Resolução CNS 466/12 (itens XII.1 e XII.2), na Norma Operacional 001/2013-CONEP, nas Diretrizes do CIOMS 2016 (Diretrizes 22, 25 e 26) e na ICH E6(R2).

O **Capítulo 10** trata da utilização (ou não) de grupos vulneráveis na pesquisa, fundamentando-se na Resolução CNS 466/12 (itens II.9 e III.1), nas Diretrizes do CIOMS 2016 (Diretrizes 15 a 18) e na Declaração de Helsinki (artigos 19 e 20).

O texto deve ser redigido no **futuro do indicativo** ("será realizado", "serão verificados", "manterá") por se tratar de projeto de pesquisa ainda a ser executado. A linguagem é acadêmica formal, sem coloquialismos, com referências bibliográficas integradas ao texto no formato **(Sobrenome, ano)** e lista de referências em ordem alfabética no estilo **Vancouver** (com DOI e URL) ao final.

---

## Regras tipográficas obrigatórias

Aplicar em todo o texto redigido por esta skill, sem exceção:

**Estrangeirismos em itálico:** toda palavra ou expressão em idioma diferente do português brasileiro deve ser grafada em itálico. Exemplos: *data sharing*, *open access*, *preprint*, *FAIR principles*, *spin-off*, *know-how*, *findings*, *et al.*, *apud*.

**Proibição de travessões:** não usar travessões (—) em nenhuma hipótese no texto redigido. Substituir por dois-pontos (:), ponto e vírgula (;), vírgula (,) ou reescrever a frase para eliminar a necessidade do travessão.

---

## Fase 1: Levantamento das informações do estudo

Se o usuário não tiver fornecido as informações abaixo, solicitar **antes de iniciar a redação**. Apresentar as perguntas em um único bloco organizado para que o usuário possa responder de uma só vez:

1. **Título provisório ou tema** do estudo e **tipo de delineamento** (ensaio clínico randomizado, estudo observacional, qualitativo, misto ou outro)
2. **Nome e tipo da instituição proponente**: nome completo, tipo (universidade pública, universidade privada, hospital universitário, instituto de pesquisa, empresa privada, outro), UF e cidade
3. **Pesquisador principal**: nome completo, titulação mais elevada (graduação, especialização, mestrado, doutorado, pós-doutorado), cargo ou função na instituição e registro no conselho de classe com número (se aplicável: CRM, CREFITO, CFP, CRBM, CRF, CRN, CREA ou outro)
4. **Há um promotor?** (entidade que concebeu ou lidera o estudo de forma independente da instituição proponente, como empresa farmacêutica, organismo internacional ou ONG) — se sim, informar nome completo, tipo e responsabilidades específicas; se não, informar "não há promotor neste estudo"
5. **Há um patrocinador?** (entidade que fornece financiamento ou suporte material ao estudo) — se sim, informar nome completo, natureza do apoio (financeiro, material, equipamentos, bolsas) e valor ou montante aproximado; se não, informar "não há patrocinador neste estudo"
6. **A pesquisa inclui grupos vulneráveis?** (menores de 18 anos, gestantes, pessoas com déficit cognitivo, privados de liberdade, idosos com demência, populações indígenas, pessoas em situação de rua, estudantes ou funcionários sob tutela do pesquisador, pacientes em situação de emergência, doentes terminais ou outros) — se sim, identificar os grupos e justificar a necessidade de inclusão; se não, confirmar que todos os participantes possuem autonomia plena
7. **Plano de divulgação**: periódico(s) pretendido(s) para publicação (se já identificado), forma de disponibilização na internet (sítio do pesquisador, repositório institucional), nome da biblioteca da instituição para entrega das cópias, previsão de apresentação em congressos
8. **Compartilhamento de dados brutos**: pretende disponibilizar os dados brutos em repositório de dados abertos (ex.: OSF, Zenodo, Figshare, repositório institucional)? Se sim, informar o repositório e se haverá período de embargo; se não, justificar brevemente
9. **Há acordos de propriedade intelectual**: há algum acordo de cessão de direitos, exploração de patente ou transferência de tecnologia com a instituição ou com o patrocinador?

Se o usuário já forneceu contexto suficiente no prompt, aproveitar as informações disponíveis e perguntar apenas o que estiver faltando ou ambíguo.

---

## Fase 2: Capítulo 8: Propriedades da Informação e Divulgação da Pesquisa

### Instruções gerais de redação

O Capítulo 8 trata dos direitos sobre os resultados da pesquisa e do plano para sua divulgação e publicação. Redigir as três seções na sequência indicada.

---

### Fase 2.1: Seção 8.1: Direitos de propriedade intelectual

Redigir ao menos **dois parágrafos** cobrindo os seguintes elementos:

**Parágrafo 1: Titularidade dos direitos sobre os resultados:**
Declarar que a propriedade intelectual dos resultados, dados e produtos gerados por esta pesquisa pertence ao pesquisador principal, na qualidade de autor, em conformidade com a Lei nº 9.610/1998 (Lei de Direitos Autorais). Esclarecer que os direitos morais de autoria são inalienáveis e irrenunciáveis (art. 27 da Lei nº 9.610/1998): o pesquisador será sempre identificado como autor nos produtos científicos decorrentes deste estudo. Quando a pesquisa for desenvolvida em instituição de ensino superior ou instituto de pesquisa com o uso de recursos, infraestrutura ou orientação da instituição, mencionar que a titularidade dos direitos patrimoniais poderá ser compartilhada com a instituição nos termos do art. 6º da Lei nº 10.973/2004 (Lei de Inovação) e do regulamento de propriedade intelectual da instituição proponente; caso não haja acordo específico, a titularidade integral pertence ao pesquisador. Se houver patrocinador ou promotor, registrar os termos do acordo de propriedade intelectual firmado entre as partes. Se não houver, declarar explicitamente que não foi firmado qualquer acordo de cessão ou compartilhamento de direitos com patrocinador ou promotor. Citar: (Brasil, 1998; Brasil, 2004; Brasil, 2012).

**Parágrafo 2: Comprometimento com a divulgação imparcial:**
Declarar que a titularidade dos direitos de propriedade intelectual não limitará nem condicionará a publicação dos resultados. Os resultados serão divulgados de forma completa, íntegra e imparcial, independentemente do sentido dos achados (positivos, negativos ou inconclusivos), em conformidade com o artigo 36 da Declaração de Helsinki (2013) e com a Diretriz 24 do CIOMS (2016), que vedam a supressão ou a distorção de resultados desfavoráveis. Se houver patrocinador, registrar que eventuais cláusulas de confidencialidade contratual se limitam ao período de análise dos dados e não se estenderão além do prazo mínimo necessário para proteção de segredo industrial legalmente justificado, sendo vedado o embargo indefinido de resultados. Citar: (World Medical Association, 2013; Council for International Organizations of Medical Sciences, 2016; Brasil, 2012).

---

### Fase 2.2: Seção 8.2: Plano de divulgação dos resultados

Redigir ao menos **três parágrafos** cobrindo os seguintes elementos:

**Parágrafo 1: Publicação em periódico científico:**
Declarar que os resultados da pesquisa serão publicados na forma de artigo original em periódico científico indexado, preferencialmente de acesso aberto (*open access*), independentemente da confirmação ou não da hipótese investigada. A escolha do periódico obedecerá a critérios de qualidade e visibilidade compatíveis com a área do estudo (indexação em MEDLINE/PubMed, SciELO, LILACS ou base equivalente), à política de acesso aberto e ao escopo temático. Registrar o periódico pretendido, se já identificado pelo pesquisador, ou indicar que a seleção do periódico será definida ao término da pesquisa. A autoria do artigo observará rigorosamente os critérios do International Committee of Medical Journal Editors (ICMJE), que exigem contribuição substancial para a concepção, execução ou análise do estudo, participação na redação ou revisão crítica do manuscrito e aprovação da versão final, sendo vedada a autoria honorária ou a omissão de autores que atendam aos critérios. Citar: (Brasil, 2012; World Medical Association, 2013; International Committee of Medical Journal Editors, 2023).

**Parágrafo 2: Disponibilização na internet e em biblioteca:**
Declarar que as cópias do projeto de pesquisa e dos relatórios parcial e final desta pesquisa serão disponibilizadas eletronicamente por meio do sítio eletrônico do pesquisador principal e/ou do repositório institucional da instituição proponente, e entregues à biblioteca da instituição proponente para integração ao acervo científico institucional, em conformidade com a política de acesso aberto ao conhecimento científico. Indicar a URL do sítio eletrônico ou repositório, se já definida pelo pesquisador, ou indicar que o endereço será informado ao CEP por ocasião da entrega do relatório final. Incluir o nome da biblioteca da instituição proponente, conforme fornecido pelo pesquisador. Citar: (Brasil, 2012; World Medical Association, 2013).

**Parágrafo 3: Comunicação científica oral e relatórios ao CEP:**
Declarar que os resultados da pesquisa serão apresentados em congressos, simpósios e jornadas científicas da área, promovendo a difusão do conhecimento gerado. Indicar a previsão de apresentação em eventos nacionais e internacionais, se já planejada. Registrar que relatórios de progresso serão submetidos ao CEP da instituição proponente nos prazos definidos no parecer de aprovação e que o relatório final será entregue ao CEP após a conclusão da análise dos dados, em conformidade com a Resolução CNS nº 466/2012 e com a Norma Operacional 001/2013-CONEP. Citar: (Brasil, 2012; Brasil, Ministério da Saúde, 2013).

---

### Fase 2.3: Seção 8.3: Publicação de dados

Redigir ao menos **dois parágrafos** cobrindo os seguintes elementos:

**Parágrafo 1: Política de compartilhamento de dados:**
Descrever a política de compartilhamento dos dados brutos desta pesquisa. Se o pesquisador pretender compartilhar os dados em repositório de dados abertos: declarar o repositório pretendido (ex.: OSF, Zenodo, Figshare, repositório institucional), o prazo previsto para disponibilização (ex.: no momento da publicação do artigo ou após período de embargo de [N] meses), o formato de disponibilização (anonimizado, pseudonimizado ou outro) e as condições de acesso (livre, mediante solicitação justificada, restrito a pesquisadores cadastrados). Indicar que os dados serão disponibilizados conforme os Princípios FAIR (do inglês: *Findable, Accessible, Interoperable, Reusable*), que orientam a gestão e o compartilhamento de dados científicos de forma padronizada, citável e reutilizável (Wilkinson et al., 2016). Se o pesquisador não pretender compartilhar os dados brutos: justificar com base na natureza dos dados (dados pessoais sensíveis de saúde, impossibilidade de anonimização irreversível), em compromissos contratuais com o patrocinador (se houver) ou em outra razão pertinente; declarar que os dados permanecerão sob guarda do pesquisador principal pelo prazo mínimo de cinco anos após o encerramento do estudo, conforme exige a Resolução CNS nº 466/2012, item XIII.4. Citar: (Wilkinson et al., 2016; Brasil, 2012; Brasil, 2018).

**Parágrafo 2: Proteção dos dados publicados e uso secundário:**
Declarar que qualquer publicação de dados, seja na forma de tabelas, figuras, bases de dados suplementares ou repositórios públicos, será realizada exclusivamente após anonimização completa e irreversível dos dados dos participantes, garantindo que nenhuma informação individual seja identificável direta ou indiretamente. O uso secundário dos dados por pesquisadores externos àqueles que os coletaram dependerá de aprovação de novo protocolo de pesquisa pelo sistema CEP/CONEP, conforme a Resolução CNS nº 466/2012 e a LGPD (Lei nº 13.709/2018). Citar: (Brasil, 2012; Brasil, 2018; World Medical Association, 2013).

---

## Fase 3: Capítulo 9: Responsabilidades do Pesquisador, da Instituição, do Promotor e do Patrocinador

### Instruções gerais de redação

O Capítulo 9 descreve formalmente as responsabilidades de cada ator envolvido na condução ética e técnica da pesquisa. Redigir as quatro seções na sequência indicada. Para promotor e patrocinador ausentes, redigir declaração explícita e fundamentada da ausência, com base legal.

---

### Fase 3.1: Seção 9.1: Responsabilidades do pesquisador

Redigir ao menos **quatro parágrafos**, cobrindo obrigatoriamente os seguintes elementos:

**Parágrafo 1: Comprometimento ético e legal:**
Declarar que o pesquisador principal está ciente dos termos da Resolução CNS nº 466/2012 e os cumprirá integralmente, assumindo a responsabilidade ética e técnica pela condução desta pesquisa. Incluir declaração de que o pesquisador conduzirá o estudo em conformidade com o protocolo aprovado pelo CEP, com as Boas Práticas Clínicas em Pesquisa segundo a ICH E6(R2), com as Diretrizes Éticas Internacionais do CIOMS (2016), com a Declaração de Helsinki (2013) e com a legislação brasileira vigente. Declarar que o pesquisador não iniciará a coleta de dados antes da emissão do parecer de aprovação pelo CEP da instituição proponente e, quando aplicável, pela CONEP, em conformidade com a Norma Operacional 001/2013-CONEP. Citar: (Brasil, 2012; Council for International Organizations of Medical Sciences, 2016; International Council for Harmonisation, 2016; World Medical Association, 2013; Brasil, Ministério da Saúde, 2013).

**Parágrafo 2: Proteção dos participantes e obtenção do consentimento:**
Declarar que o pesquisador principal é responsável pela proteção dos direitos, da segurança e do bem-estar de todos os participantes do estudo, em posição de prioridade sobre os interesses científicos ou comerciais do projeto. A obtenção do consentimento livre e esclarecido será realizada pessoalmente pelo pesquisador principal ou por membro da equipe formalmente designado e treinado para essa função, em linguagem acessível ao participante, com tempo suficiente para reflexão e sem qualquer forma de coerção ou pressão. O pesquisador assegurará que qualquer participante possa retirar o seu consentimento a qualquer momento, sem prejuízo ao atendimento ou à relação com a instituição. Citar: (Brasil, 2012; World Medical Association, 2013).

**Parágrafo 3: Registro, comunicação e transparência:**
Declarar que o pesquisador principal manterá registros completos e atualizados de todas as atividades da pesquisa, incluindo fichas de coleta originais, assinaturas de TCLE, relatórios de eventos adversos, correspondências com o CEP e qualquer desvio de protocolo identificado. Os desvios de protocolo serão comunicados ao CEP por meio do sistema Plataforma Brasil no prazo estabelecido pelo parecer de aprovação. O pesquisador é responsável pela elaboração e pela entrega dos relatórios parciais e final ao CEP nos prazos definidos e pela comunicação imediata de qualquer evento adverso sério inesperado, de achados que coloquem em risco a segurança dos participantes ou de qualquer motivo que justifique a suspensão ou o encerramento prematuro da pesquisa. Citar: (Brasil, 2012; Brasil, Ministério da Saúde, 2013; International Council for Harmonisation, 2016).

**Parágrafo 4: Treinamento e supervisão da equipe:**
Declarar que o pesquisador principal é responsável pelo treinamento, pela supervisão e pela conduta ética de todos os membros da equipe envolvidos na coleta de dados, na análise dos resultados e na disseminação dos achados. Nenhum procedimento será delegado a profissional sem a habilitação técnica e legal exigida. O pesquisador garantirá que todos os membros da equipe tenham lido e compreendido o protocolo aprovado pelo CEP, os Procedimentos Operacionais Padrão (POP) e as normas éticas aplicáveis antes do início da coleta de dados. Citar: (Brasil, 2012; International Council for Harmonisation, 2016; Council for International Organizations of Medical Sciences, 2016).

---

### Fase 3.2: Seção 9.2: Responsabilidades da instituição

Redigir ao menos **três parágrafos**, cobrindo obrigatoriamente os seguintes elementos:

**Parágrafo 1: Responsabilidade institucional e infraestrutura:**
Declarar que a instituição proponente está ciente dos termos da Resolução CNS nº 466/2012 e assume corresponsabilidade pela execução ética e técnica desta pesquisa. A instituição se compromete a: disponibilizar a infraestrutura física, laboratorial e tecnológica necessária para a realização dos procedimentos previstos no protocolo; garantir as condições de sigilo, segurança e confidencialidade exigidas para o armazenamento e o processamento dos dados dos participantes; e assegurar que os membros da equipe de pesquisa vinculados à instituição disponham de tempo e recursos para cumprir suas obrigações no estudo. Citar: (Brasil, 2012; Council for International Organizations of Medical Sciences, 2016; Brasil, Ministério da Saúde, 2013).

**Parágrafo 2: Responsabilidade ética institucional:**
Declarar que a instituição proponente reconhece a independência do Comitê de Ética em Pesquisa (CEP) e se compromete a não interferir nas suas deliberações. A instituição garantirá que o protocolo desta pesquisa somente será iniciado após a aprovação expressa do CEP e, quando aplicável, da CONEP. A instituição assumirá a responsabilidade de comunicar ao CEP qualquer mudança de infraestrutura, de recursos ou de capacidade institucional que possa afetar a segurança dos participantes ou a continuidade do estudo. Citar: (Brasil, 2012; Brasil, Ministério da Saúde, 2013).

**Parágrafo 3: Guarda dos documentos e acesso pós-estudo:**
Declarar que a instituição proponente assegurará a guarda dos documentos essenciais da pesquisa (fichas de coleta originais, TCLEs assinados, relatórios ao CEP, banco de dados) pelo prazo mínimo de cinco anos após o encerramento ou a interrupção do estudo, conforme a Resolução CNS nº 466/2012, item XIII.4. A instituição garantirá que esses documentos estejam acessíveis para auditoria pelo CEP, pela CONEP ou por organismos reguladores competentes durante todo o período de guarda. Citar: (Brasil, 2012).

---

### Fase 3.3: Seção 9.3: Responsabilidades do promotor

**Instrução condicional:**

**Se não houver promotor:** redigir um único parágrafo declarando explicitamente que, nesta pesquisa, não há um promotor, ou seja, que a pesquisa foi inteiramente concebida e será conduzida pelo pesquisador principal com o suporte exclusivo da instituição proponente, sem a participação de entidade externa que tenha iniciado, organizado ou financiado o estudo na posição de promotor. Justificar que, por essa razão, esta seção não se aplica ao presente protocolo. Citar: (Brasil, 2012; Council for International Organizations of Medical Sciences, 2016).

Exemplo de parágrafo para a situação sem promotor:

> Nesta pesquisa não há um promotor. O estudo foi inteiramente concebido pelo pesquisador principal e será conduzido sob responsabilidade exclusiva do pesquisador e da instituição proponente, sem a participação de entidade externa na posição de organização que toma a iniciativa, administra ou financia o estudo (Brasil, 2012; Council for International Organizations of Medical Sciences, 2016). Por essa razão, esta seção não se aplica ao presente protocolo.

**Se houver promotor:** redigir ao menos dois parágrafos descrevendo a identificação do promotor (nome completo, tipo, endereço), as responsabilidades específicas do promotor em relação ao protocolo (elaboração, financiamento, monitoramento independente, fornecimento de seguro ou indenização, notificação de eventos adversos sérios às autoridades regulatórias), a relação entre o promotor e o pesquisador em termos de independência científica, os mecanismos de monitoramento e auditoria a cargo do promotor e os procedimentos em caso de decisão do promotor de suspender ou encerrar o estudo. Citar: (Brasil, 2012; Council for International Organizations of Medical Sciences, 2016; International Council for Harmonisation, 2016).

---

### Fase 3.4: Seção 9.4: Responsabilidades do patrocinador

**Instrução condicional:**

**Se não houver patrocinador:** redigir um único parágrafo declarando explicitamente que, nesta pesquisa, não há um patrocinador, ou seja, que o estudo não recebe financiamento externo, doação de equipamentos, bolsas ou qualquer outra forma de suporte material de entidade pública ou privada distinta da instituição proponente. Justificar que, por essa razão, esta seção não se aplica ao presente protocolo. Citar: (Brasil, 2012; Council for International Organizations of Medical Sciences, 2016).

Exemplo de parágrafo para a situação sem patrocinador:

> Nesta pesquisa não há um patrocinador. O estudo não conta com financiamento externo, doação de equipamentos, bolsas ou qualquer outra forma de suporte material de entidade pública ou privada distinta da instituição proponente (Brasil, 2012; Council for International Organizations of Medical Sciences, 2016). Por essa razão, esta seção não se aplica ao presente protocolo.

**Se houver patrocinador:** redigir ao menos dois parágrafos descrevendo a identificação do patrocinador (nome completo, tipo, endereço), a natureza e o montante do apoio fornecido (financeiro, material, bolsas, equipamentos), o mecanismo de repasse dos recursos (convênio, contrato, doação, outro), as salvaguardas para garantia da independência científica do pesquisador em relação ao patrocinador (autonomia para publicar resultados independentemente do seu sentido, ausência de conflito de interesse que comprometa a integridade da pesquisa) e a declaração de conflito de interesses, se aplicável. Citar: (Brasil, 2012; Council for International Organizations of Medical Sciences, 2016; World Medical Association, 2013).

---

## Fase 4: Capítulo 10: Utilização de Grupos Vulneráveis

### Instruções de redação

Redigir ao menos **dois parágrafos**, adaptando o conteúdo à situação do estudo: (a) pesquisa conduzida exclusivamente com participantes de autonomia plena, ou (b) pesquisa que inclui um ou mais grupos vulneráveis, com justificativa e salvaguardas.

---

**Instrução condicional A: participantes com autonomia plena (situação mais comum):**

Se o estudo for conduzido exclusivamente com adultos de plena capacidade civil e cognitiva, sem inclusão de grupos reconhecidos como vulneráveis pela Resolução CNS nº 466/2012 e pelo CIOMS 2016, redigir dois parágrafos:

**Parágrafo 1: Declaração de autonomia plena dos participantes:**
Declarar que esta pesquisa será realizada exclusivamente com indivíduos que possuem autonomia plena para decidir, de forma livre, consciente e esclarecida, sobre a sua participação no estudo. Todos os participantes serão maiores de dezoito anos, com plena capacidade civil e cognitiva para compreender as informações apresentadas no Termo de Consentimento Livre e Esclarecido (TCLE) e para exercer seu direito de participar, recusar ou retirar o consentimento sem qualquer forma de coerção ou constrangimento. Citar: (Brasil, 2012).

**Parágrafo 2: Princípio de proteção de grupos vulneráveis:**
Declarar que, em conformidade com a Resolução CNS nº 466/2012 (item III.1) e com as Diretrizes Éticas Internacionais do CIOMS (2016), indivíduos ou grupos em situação de vulnerabilidade não participarão desta pesquisa. O princípio de proteção de grupos vulneráveis orienta que pessoas em situação de diminuição de autonomia não devem ser recrutadas para pesquisas quando as informações desejadas possam ser obtidas por meio de participantes com autonomia plena, salvo quando a investigação ofereça benefícios diretos aos próprios indivíduos vulneráveis ou quando a pesquisa não possa ser conduzida sem a participação desse grupo específico. Como nenhuma dessas condições se aplica ao presente estudo, a seleção dos participantes excluirá deliberadamente indivíduos ou grupos vulneráveis. Citar: (Brasil, 2012; Council for International Organizations of Medical Sciences, 2016; World Medical Association, 2013).

---

**Instrução condicional B: estudo que inclui grupos vulneráveis:**

Se o estudo incluir um ou mais grupos vulneráveis, redigir ao menos três parágrafos:

**Parágrafo 1: Identificação dos grupos vulneráveis e justificativa da inclusão:**
Identificar os grupos vulneráveis incluídos no estudo. Justificar obrigatoriamente a necessidade de inclusão: a pesquisa somente será realizada com participantes vulneráveis quando a informação desejada não puder ser obtida por meio de participantes com plena autonomia, ou quando a investigação puder trazer benefícios diretos e relevantes aos próprios indivíduos ou grupos vulneráveis, em conformidade com a Resolução CNS nº 466/2012 (item III.1) e com a Diretriz 15 do CIOMS (2016). Citar: (Brasil, 2012; Council for International Organizations of Medical Sciences, 2016; World Medical Association, 2013).

**Parágrafo 2: Salvaguardas específicas para cada grupo vulnerável:**
Descrever as salvaguardas adotadas para a proteção de cada grupo vulnerável identificado, conforme aplicável:

- Para **menores de 18 anos**: obtenção de assentimento do menor em linguagem acessível à sua faixa etária, por meio de Termo de Assentimento Livre e Esclarecido (TALE), somado ao consentimento do responsável legal pelo TCLE.
- Para **pessoas com déficit cognitivo ou demência**: avaliação da capacidade de consentimento por profissional habilitado; quando comprometida, obtenção de consentimento substituto do responsável legal; garantia de que a participação corresponde ao melhor interesse do participante.
- Para **gestantes**: garantia de que a participação não expõe o feto a riscos não justificados pelos benefícios esperados; aprovação específica pelo CEP para a inclusão de gestantes.
- Para **privados de liberdade**: garantia incondicional de que a recusa ou retirada do consentimento não implicará qualquer sanção, perda de benefícios ou tratamento diferenciado; participação estritamente voluntária.
- Para **populações indígenas**: consulta e anuência prévia das lideranças comunitárias; tradução do TCLE e dos materiais do estudo para a língua vernácula ou disponibilização de intérprete; respeito às práticas culturais e à organização social da comunidade; submissão à CONEP.

Citar: (Brasil, 2012; Council for International Organizations of Medical Sciences, 2016; World Medical Association, 2013).

**Parágrafo 3: Benefícios esperados para o grupo vulnerável:**
Descrever os benefícios diretos esperados para os participantes pertencentes ao grupo vulnerável, ou, quando não houver benefícios diretos, demonstrar que os benefícios científicos ou sociais justificam eticamente a exposição ao risco mínimo e a potencial perda de privacidade. Reafirmar que as salvaguardas descritas são suficientes para garantir que o consentimento será válido e livre de coerção e que a inclusão do grupo vulnerável é eticamente justificada. Citar: (Brasil, 2012; Council for International Organizations of Medical Sciences, 2016; World Medical Association, 2013).

---

## Fase 5: Lista de referências (ao final do conjunto dos três capítulos)

Ao concluir a redação dos três capítulos, gerar automaticamente a **lista de referências** unificada. A lista deve obedecer às seguintes regras:

- **Formato**: Vancouver (sobrenome, iniciais do nome. Título. Periódico ou Editora. Ano; volume(número):páginas. doi: [DOI]. Disponível em: [URL])
- **Ordem**: alfabética pelo primeiro elemento de entrada (sobrenome do primeiro autor ou nome do órgão institucional)
- **Completude**: incluir DOI quando disponível; incluir URL de acesso quando disponível; para legislação brasileira, indicar o Diário Oficial da União
- **Cobertura**: incluir todas as fontes citadas no texto no formato (Autor, ano)

### Lista de referências nucleares a incluir (adaptar e acrescentar conforme as seções redigidas):

Brasil. Conselho Nacional de Saúde. Resolução nº 466, de 12 de dezembro de 2012. Aprova as diretrizes e normas regulamentadoras de pesquisas envolvendo seres humanos. Diário Oficial da União, Brasília, DF, 13 jun. 2013; Seção 1:59. Disponível em: https://conselho.saude.gov.br/resolucoes/2012/Reso466.pdf

Brasil. Lei nº 9.610, de 19 de fevereiro de 1998. Altera, atualiza e consolida a legislação sobre direitos autorais e dá outras providências. Diário Oficial da União, Brasília, DF, 20 fev. 1998. Disponível em: https://www.planalto.gov.br/ccivil_03/leis/l9610.htm

Brasil. Lei nº 10.973, de 2 de dezembro de 2004. Dispõe sobre incentivos à inovação e à pesquisa científica e tecnológica no ambiente produtivo e dá outras providências. Diário Oficial da União, Brasília, DF, 3 dez. 2004. Disponível em: https://www.planalto.gov.br/ccivil_03/_ato2004-2006/2004/lei/l10.973.htm

Brasil. Lei nº 13.709, de 14 de agosto de 2018. Lei Geral de Proteção de Dados Pessoais (LGPD). Diário Oficial da União, Brasília, DF, 15 ago. 2018. Disponível em: https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm

Brasil. Ministério da Saúde. Conselho Nacional de Saúde. Norma Operacional nº 001/2013 — CONEP. Dispõe sobre a organização e funcionamento do sistema CEP/CONEP. Brasília: Ministério da Saúde; 2013. Disponível em: https://conselho.saude.gov.br/web_comissoes/conep/aquivos/normativa/normaoperacional001_2013_conep.pdf

Council for International Organizations of Medical Sciences (CIOMS). International Ethical Guidelines for Health-related Research Involving Humans. 4th ed. Geneva: CIOMS; 2016. doi:10.56759/rgxl7429. Disponível em: https://cioms.ch/publications/product/international-ethical-guidelines-for-health-related-research-involving-humans/

International Committee of Medical Journal Editors (ICMJE). Recommendations for the Conduct, Reporting, Editing, and Publication of Scholarly Work in Medical Journals. Philadelphia: ICMJE; 2023. Disponível em: https://www.icmje.org/icmje-recommendations.pdf

International Council for Harmonisation (ICH). ICH E6(R2): Guideline for Good Clinical Practice. Geneva: ICH; 2016. Disponível em: https://www.ich.org/page/efficacy-guidelines

Wilkinson MD, Dumontier M, Aalbersberg IJ, Appleton G, Axton M, Baak A, et al. The FAIR Guiding Principles for scientific data management and stewardship. Sci Data. 2016;3:160018. doi:10.1038/sdata.2016.18. Disponível em: https://www.nature.com/articles/sdata201618

World Medical Association. Declaration of Helsinki: Ethical Principles for Medical Research Involving Human Subjects. Fortaleza: WMA; 2013. Disponível em: https://www.wma.net/policies-post/wma-declaration-of-helsinki-ethical-principles-for-medical-research-involving-human-subjects/

---

## Fase 6: Entregáveis

Após apresentar o texto completo dos Capítulos 8, 9 e 10, inclua a seguinte mensagem ao final da resposta:

> "Capítulos 8, 9 e 10 gerados. Use os botões abaixo para baixar o resultado nos formatos .md, .docx e .pdf."

O sistema gera os arquivos automaticamente — **não inclua scripts, código ou blocos de dependências na resposta.**

---

## Padrões de qualidade: checklist de revisão antes de entregar o texto

Antes de apresentar os capítulos ao usuário, verificar se **todos** os itens abaixo estão presentes e completos:

**Capítulo 8:**
- [ ] Seção 8.1: titularidade dos direitos intelectuais declarada com base na Lei 9.610/1998
- [ ] Seção 8.1: acordos com instituição ou patrocinador descritos, ou ausência declarada explicitamente
- [ ] Seção 8.1: comprometimento com divulgação imparcial dos resultados (positivos e negativos)
- [ ] Seção 8.2: publicação em periódico indexado declarada, independentemente do sentido dos achados
- [ ] Seção 8.2: critérios de autoria ICMJE mencionados
- [ ] Seção 8.2: disponibilização na internet e entrega à biblioteca da instituição descritas
- [ ] Seção 8.2: relatórios ao CEP mencionados
- [ ] Seção 8.3: política de *data sharing* descrita (com repositório e condições, ou justificativa de não compartilhamento)
- [ ] Seção 8.3: Princípios FAIR mencionados quando há compartilhamento de dados
- [ ] Seção 8.3: proteção dos participantes na publicação de dados e uso secundário declarados

**Capítulo 9:**
- [ ] Seção 9.1: comprometimento com CNS 466/12, ICH E6(R2), CIOMS 2016 e Declaração de Helsinki declarado
- [ ] Seção 9.1: não início antes da aprovação do CEP declarado
- [ ] Seção 9.1: proteção dos participantes como prioridade declarada
- [ ] Seção 9.1: obtenção do consentimento descrita
- [ ] Seção 9.1: registro e comunicação de desvios ao CEP descrito
- [ ] Seção 9.1: treinamento e supervisão da equipe descrito
- [ ] Seção 9.2: corresponsabilidade da instituição declarada
- [ ] Seção 9.2: infraestrutura e independência do CEP mencionadas
- [ ] Seção 9.2: guarda dos documentos pelo prazo mínimo de 5 anos declarada
- [ ] Seção 9.3: se não há promotor: declaração explícita e fundamentada; se há: responsabilidades descritas
- [ ] Seção 9.4: se não há patrocinador: declaração explícita e fundamentada; se há: responsabilidades e independência científica descritas

**Capítulo 10:**
- [ ] Declaração explícita sobre a ausência ou presença de grupos vulneráveis
- [ ] Se ausência: princípio de proteção de grupos vulneráveis mencionado com base legal (CNS 466/12, item III.1; CIOMS 2016)
- [ ] Se presença: identificação dos grupos e justificativa da necessidade de inclusão
- [ ] Se presença: salvaguardas específicas descritas para cada grupo vulnerável identificado
- [ ] Se presença: benefícios esperados para os grupos vulneráveis descritos ou justificativa ética de inclusão sem benefício direto

**Requisitos gerais (todos os capítulos):**
- [ ] Citações integradas ao texto no formato **(Autor, ano)** em todas as afirmações que requerem fundamentação
- [ ] Lista de referências ao final em ordem **alfabética**, estilo **Vancouver**, com **DOI** e **URL** quando disponíveis
- [ ] Nenhuma seção genérica ou com marcador de posição ("[inserir aqui]", "a definir", etc.)
- [ ] Texto integralmente em **português brasileiro formal**, no **futuro do indicativo**
- [ ] Ausência de primeira pessoa do singular ("Eu realizarei" deve ser "será realizado")
- [ ] Todas as palavras e expressões em outros idiomas grafadas em **itálico**
- [ ] Ausência de travessões (—) em todo o texto redigido
- [ ] PDFs gerados com cabeçalho do capítulo correspondente e numeração de páginas; caminhos completos confirmados ao usuário

**Próxima etapa:** solicite a skill `/capitulo-anexos` para redigir o Capítulo 11 — Anexos.


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
