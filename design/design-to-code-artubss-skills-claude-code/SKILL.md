---
name: design-to-code
description: Conversão pixel-perfeita de Figma para React usando coderio. Gera código pronto para produção (TypeScript, Vite, TailwindCSS V4) com alta fidelidade visual. Inclui tratamento robusto de erros, recuperação de checkpoints e execução simplificada via script auxiliar.
---

# Design to Code

Restauração de UI com alta fidelidade de designs Figma para componentes React + TypeScript prontos para produção.
Esta SKILL utiliza um **script auxiliar robusto** para minimizar erros manuais e garantir resultados pixel-perfeitos.

## Pré-requisitos

1.  **Token da API Figma**: Obtenha em Figma → Settings → Personal Access Tokens
2.  **Node.js**: Versão 18+
3.  **coderio**: Instalado na pasta `scripts/` (tratado na fase Setup)

## Visão Geral do Workflow

```
Fase 0: SETUP    → Criar script auxiliar e ambiente de execução
Fase 1: PROTOCOL → Gerar protocolo de design (Estrutura e Props)
Fase 2: CODE     → Gerar componentes e assets
```

---

# Fase 0: Setup

## Passo 0.1: Inicializar Script Auxiliar

**Ação do Usuário**: Execute estes comandos para criar o helper de execução e isolar suas dependências.

```bash
mkdir -p scripts

# 1. Copiar arquivos de script
# Nota: Certifique-se de que você tem o diretório 'skills/design-to-code/scripts' disponível
cp skills/design-to-code/scripts/package.json scripts/package.json
cp skills/design-to-code/scripts/coderio-skill.mjs scripts/coderio-skill.mjs

# 2. Instalar coderio no diretório scripts (ajuste a versão se necessário)
cd scripts && pnpm install && cd ..
```

## Passo 0.2: Estruturar Projeto (Opcional)

Se está iniciando um novo projeto:

1.  Execute: `node scripts/coderio-skill.mjs scaffold-prompt "MyApp"`
2.  **Tarefa de IA**: Siga as instruções de saída do comando para criar os arquivos.

---

# Fase 1: Geração do Protocolo

## Passo 1.1: Buscar Dados

```bash
# Substitua pela sua URL e Token
node scripts/coderio-skill.mjs fetch-figma "https://figma.com/file/..." "figd_..."
```

**Verificação**: `process/thumbnail.png` deve existir.

## Passo 1.2: Gerar Estrutura

1.  **Gerar Prompt**:

    ```bash
    node scripts/coderio-skill.mjs structure-prompt > scripts/structure-prompt.md
    ```

2.  **Tarefa de IA (Estrutura)**:
    - **ANEXAR**: `process/thumbnail.png` (OBRIGATÓRIO)
    - **LER**: `scripts/structure-prompt.md`
    - **INSTRUÇÃO**: "Gere a JSON de estrutura de componentes com base no prompt e na miniatura anexada. Concentre-se no agrupamento visual. **Use o conteúdo de texto para nomear componentes com precisão (por exemplo, 'SafeProducts', não 'FAQ').**"
    - **SALVAR**: Cole o resultado em JSON em `scripts/structure-output.json`.

3.  **Processar Resultado**:
    ```bash
    node scripts/coderio-skill.mjs save-structure
    ```

## Passo 1.3: Extrair Props (Iterativo)

1.  **Listar Componentes**:

    ```bash
    node scripts/coderio-skill.mjs list-components
    ```

2.  **Para CADA componente na lista**:

    a. **Gerar Prompt**:

    ```bash
    node scripts/coderio-skill.mjs props-prompt "ComponentName" > scripts/current-props-prompt.md
    ```

    b. **Tarefa de IA (Props)**:
    - **ANEXAR**: `process/thumbnail.png` (OBRIGATÓRIO)
    - **LER**: `scripts/current-props-prompt.md`
    - **INSTRUÇÃO**: "Extraia props e dados de estado. Seja pixel-perfeito com texto e caminhos de imagem."
    - **SALVAR**: Cole o resultado em JSON em `scripts/ComponentName-props.json`.

    c. **Salvar e Validar**:

    ```bash
    node scripts/coderio-skill.mjs save-props "ComponentName"
    # Se falhar, refaça o passo 'b' com maior atenção à miniatura
    ```

---

# Fase 2: Geração de Código

## Passo 2.1: Planejar Tarefas

```bash
node scripts/coderio-skill.mjs list-gen-tasks
```

Isso gera uma lista de tarefas com índices (0, 1, 2...).

## Passo 2.2: Gerar Componentes (Iterativo)

**Para CADA índice de tarefa (começando do 0)**:

1.  **Gerar Prompt**:

    ```bash
    node scripts/coderio-skill.mjs code-prompt 0 > scripts/code-prompt.md
    # Substitua '0' pelo índice da tarefa atual
    ```

2.  **Tarefa de IA (Código)**:
    - **ANEXAR**: `process/thumbnail.png` (OBRIGATÓRIO)
    - **LER**: `scripts/code-prompt.md`
    - **INSTRUÇÃO**: "Gere o código do componente React. Corresponda à miniatura EXATAMENTE. **Use conteúdo de texto RIGOROSO dos dados de entrada, não alucine.**"
    - **SALVAR**: Cole o bloco de código em `scripts/code-output.txt`.

3.  **Salvar Código**:
    ```bash
    node scripts/coderio-skill.mjs save-code 0
    # Substitua '0' pelo índice da tarefa atual
    ```

## Passo 2.3: Integração Final

Injete o componente raiz em `App.tsx`. Use o caminho encontrado na última tarefa da Fase 2.1.

---

# Solução de Problemas

- **"Props validation failed"**: A IA gerou props vazios. Verifique se `process/thumbnail.png` foi anexado e está visível à IA. Repita a etapa de geração de props.
- **"Module not found"**: Certifique-se de que `node scripts/coderio-skill.mjs save-code` foi executado para o componente filho antes do componente pai. A Fase 2 deve ser feita em ordem (0, 1, 2...).
- **"Visuals don't match"**: Você anexou a miniatura? A IA depende dela para nuances de espaçamento e layout não presentes nos dados brutos.