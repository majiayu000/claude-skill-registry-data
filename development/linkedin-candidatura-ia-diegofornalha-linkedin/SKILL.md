---
name: linkedin-candidatura-ia
description: Esta skill deve ser usada quando o usuário solicitar candidaturas automáticas em vagas do LinkedIn relacionadas a Inteligência Artificial (IA) no Brasil, priorizando vagas com cadastro simplificado (Easy Apply). A skill filtra vagas por palavras-chave de IA, localização no Brasil, nível de senioridade (se especificado) e tipo de candidatura simplificada.
---

# LinkedIn Candidatura IA

## Visão Geral

Esta skill automatiza o processo de busca e candidatura em vagas de Inteligência Artificial no LinkedIn, focando exclusivamente em vagas com cadastro simplificado (Easy Apply) localizadas no Brasil. A skill utiliza as ferramentas Chrome DevTools para navegar, filtrar e se candidatar em vagas que atendem aos critérios especificados.

## Fluxo de Trabalho Principal

### 1. Preparação e Navegação

Antes de iniciar a busca de vagas:

1. Verificar se o LinkedIn já está aberto usando `mcp__chrome-devtools__list_pages`
2. Se não estiver, navegar para o LinkedIn usando `mcp__chrome-devtools__navigate_page` com URL `https://www.linkedin.com/jobs/`
3. Tirar snapshot da página para verificar se o usuário está logado
4. Se não estiver logado, aguardar login manual do usuário

### 2. Busca e Filtragem de Vagas

Para buscar vagas de IA com os critérios adequados:

1. **Construir query de busca** com base nos critérios:
   - Palavras-chave principais de IA (consultar `references/palavras_chave_ia.md`)
   - Localização: Brasil
   - Nível de senioridade (se especificado pelo usuário)

2. **Aplicar filtros no LinkedIn**:
   - Usar `mcp__chrome-devtools__take_snapshot` para identificar elementos de busca
   - Usar `mcp__chrome-devtools__fill` para preencher campo de busca
   - Usar `mcp__chrome-devtools__click` para aplicar filtro "Easy Apply"
   - Aplicar filtro de localização "Brasil"
   - Se especificado, aplicar filtro de nível de senioridade

3. **Aguardar carregamento** usando `mcp__chrome-devtools__wait_for` para garantir que resultados sejam exibidos

### 3. Identificação de Vagas Elegíveis

Para cada vaga encontrada:

1. Tirar snapshot da lista de vagas
2. Identificar vagas que possuem o badge "Easy Apply"
3. Verificar se a vaga está no Brasil (confirmar localização)
4. Verificar se contém palavras-chave relevantes de IA (consultar `references/palavras_chave_ia.md`)

### 4. Processo de Candidatura

Para cada vaga elegível:

1. **Clicar na vaga** usando o UID do elemento
2. **Tirar snapshot** do painel de detalhes da vaga
3. **Validar elegibilidade**:
   - Confirmar presença do botão "Easy Apply"
   - Verificar se já não foi candidatado anteriormente
   - Verificar descrição da vaga para palavras-chave de IA

4. **Executar candidatura**:
   - Clicar no botão "Easy Apply"
   - Tirar snapshot do formulário de candidatura
   - Se for apenas um clique (formulário já preenchido), submeter
   - Se houver múltiplas etapas, consultar `scripts/preencher_formulario_linkedin.py` para assistência
   - Aguardar confirmação de candidatura

5. **Registrar resultado**:
   - Manter contador de candidaturas realizadas
   - Reportar ao usuário cada candidatura bem-sucedida

6. **Enviar mensagem (opcional)**:
   - Se Sales Navigator estiver disponível, enviar mensagem simples ao recrutador
   - Mensagem padrão: "Olá! Acabei de me candidatar à vaga de [título da vaga] na sua empresa. Fico à disposição para conversarmos."
   - Usar `scripts/enviar_mensagem_recruiter.py` para automação

### 5. Tratamento de Casos Especiais

**Formulários com múltiplas etapas:**
- Usar `scripts/preencher_formulario_linkedin.py` que contém lógica para avançar entre etapas
- Preencher informações básicas automaticamente quando possível
- Para perguntas personalizadas que não podem ser preenchidas automaticamente, pular a vaga

**Perguntas numéricas:**
- IMPORTANTE: Quando o LinkedIn pedir "anos de experiência" ou valores numéricos, fornecer APENAS o número (ex: "2" ou "5")
- NÃO adicionar unidades como "anos", "meses", etc. - o LinkedIn espera valores numéricos puros
- Exemplos corretos: "2", "3.5", "5"
- Exemplos incorretos: "2 anos", "5 anos de experiência"

**Vaga como preferencial:**
- Ao marcar vaga como preferencial, o LinkedIn EXIGE uma mensagem obrigatória
- Usar template padrão: "Olá! Tenho grande interesse nesta vaga de [área]. Possuo experiência em desenvolvimento de soluções de IA e estou ansioso para contribuir com a equipe. Fico à disposição para conversarmos."
- Mensagem deve ter entre 20-400 caracteres

**Uso de histórico de pesquisa:**
- LinkedIn mantém histórico de pesquisas recentes
- SEMPRE verificar se há opção de "Pesquisas recentes" no snapshot antes de tentar preencher campo manualmente
- Clicar na pesquisa recente é mais confiável que preencher o campo

**Limites de candidatura:**
- LinkedIn pode limitar número de candidaturas. Se encontrar mensagem de limite, pausar e informar usuário

**Vagas já candidatadas:**
- Verificar presença de texto "Candidatado" ou similar antes de tentar candidatura

**Tratamento de timeouts durante submissão:**
- LinkedIn pode ter delays de 5000ms ao submeter formulários
- Timeouts DURANTE a submissão NÃO indicam falha
- Após timeout, SEMPRE tirar novo snapshot para verificar se a submissão foi bem-sucedida
- Procurar por mensagens como "Candidatou-se em há X segundos" para confirmar sucesso
- Timeouts + sucesso confirmado = candidatura bem-sucedida (não repetir)

**Segurança - Fluxo de submissão:**
- Na tela de revisão (100%): Mostrar resumo ao usuário
- Pedir confirmação: "Deseja enviar esta candidatura?"
- Apenas após aprovação do usuário, clicar no botão de envio
- Se houver timeout durante envio, aguardar novo snapshot para confirmar

## Critérios de Filtro

### Obrigatórios
- ✅ Cadastro simplificado (Easy Apply)
- ✅ Localização: Brasil
- ✅ Palavras-chave relacionadas a IA (consultar `references/palavras_chave_ia.md`)

### Opcionais (aplicar somente se especificado)
- Nível de senioridade (Junior, Pleno, Senior, etc.)
- Modalidade de trabalho (Remoto, Híbrido, Presencial)
- Empresa específica

## Recursos

### scripts/

**`aplicar_candidatura.py`**
Script principal que orquestra o processo completo de candidatura Easy Apply. Baseado em 6+ candidaturas bem-sucedidas, contém:
- Classe `ProcessoCandidaturaLinkedIn` para orquestrar fluxo completo
- Padrão validado: navegação → preenchimento → submissão → confirmação
- Tratamento de timeouts durante submissão (5000ms é normal, não é falha)
- Confirmação de sucesso via mensagem "Candidatou-se em há X segundos"

**`preencher_formulario_linkedin.py`**
Script auxiliar para preencher formulários de candidatura do LinkedIn com múltiplas etapas. Contém lógica para:
- Navegar entre páginas do formulário
- Preencher campos comuns automaticamente
- Identificar quando avançar ou submeter
- Diferenciar campos obrigatórios de opcionais

**`enviar_mensagem_recruiter.py`**
Script para enviar mensagem ao recrutador via Sales Navigator após candidatura. Funcionalidades:
- Identificar recrutador responsável pela vaga
- Enviar mensagem personalizada automática
- Registrar mensagens enviadas para evitar duplicatas

### references/

**`padrao_formulario_pratico.md`** ⭐ **NOVO**
Documentação do padrão real de formulários LinkedIn baseado em experiência prática. Inclui:
- Estrutura padrão: 0% → 67% → 100% de progresso
- Tipos de campos encontrados (dropdowns, numéricos, texto, salário)
- Detalhes críticos: campos numéricos devem ser APENAS números (sem unidades)
- Tratamento de timeouts: quando ocorrem, como verificar sucesso real
- Sinais de quando pular uma vaga
- Exemplos com UIDs reais de candidaturas bem-sucedidas

**`palavras_chave_ia.md`**
Lista abrangente de palavras-chave relacionadas a Inteligência Artificial em português e inglês, incluindo:
- Termos gerais de IA
- Tecnologias específicas (Machine Learning, Deep Learning, NLP, Computer Vision, etc.)
- Frameworks e bibliotecas (TensorFlow, PyTorch, scikit-learn, etc.)
- Cargos relacionados (Cientista de Dados, Engenheiro de ML, etc.)

**`linkedin_selectors.md`**
Referência de seletores CSS e padrões comuns do LinkedIn para:
- Botão Easy Apply
- Campos de busca e filtros
- Elementos de vaga
- Formulários de candidatura

## Exemplos de Uso

**Exemplo 1: Candidatura geral em vagas de IA**
```
Usuário: "Candidate-me a vagas de IA no LinkedIn"
→ Buscar todas as vagas de IA com Easy Apply no Brasil, qualquer nível
```

**Exemplo 2: Candidatura com nível específico**
```
Usuário: "Quero me candidatar apenas em vagas senior de IA"
→ Buscar vagas de IA Senior com Easy Apply no Brasil
```

**Exemplo 3: Candidatura com tecnologia específica**
```
Usuário: "Procure vagas de Machine Learning com PyTorch"
→ Buscar vagas que mencionem "Machine Learning" E "PyTorch" com Easy Apply no Brasil
```

## Notas Importantes

- Esta skill requer que o usuário esteja logado no LinkedIn
- Respeitar limites de taxa do LinkedIn para evitar bloqueios
- Apenas candidatar em vagas que realmente atendem os critérios para manter qualidade do perfil
- Sempre reportar ao usuário quantas candidaturas foram realizadas e quais vagas
