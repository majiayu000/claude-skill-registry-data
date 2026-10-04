---
name: bootstrap
description: Skill de inicialização da squad. Faz a varredura do projeto e popula a memória técnica e de negócios em `memorys/`. ATENÇÃO - SÓ DEVE ser executada se houver solicitação explícita do usuário ("instalar a squad", "fazer setup inicial", "bootstrap do projeto") ou após o instalador raiz (`agent.md`) já ter feito a configuração de ferramenta.
---

> **Nota de Design:** Esta é a única skill sem agente dono por definição. Ela existe para popular a memória inicial — pré-requisito para que os agentes operem com contexto. É invocada diretamente pelo usuário, pelo workflow `bootstrap.md` ou pelo instalador raiz `agent.md` após configurar a ferramenta de gerenciamento.
>
> **Escopo desta skill:** APENAS varredura do projeto e preenchimento de `memorys/`. A configuração da ferramenta (Claude Code, Cursor, Antigravity, Gemini-CLI, etc.) é responsabilidade do `agent.md` na raiz, não desta skill.

## Gatilhos (Execution Triggers)

- Comando explícito do usuário: "Setup project context", "Instale a squad neste projeto", "Execute o bootstrap".
- Etapa final do instalador raiz `agent.md` após a configuração de symlinks/cópias para a ferramenta escolhida.

## Papel dos Arquivos de Memória (Fronteiras Rígidas)

Antes de preencher os arquivos em `memorys/`, respeite as fronteiras de responsabilidade. Cada aprendizado vai exatamente em um arquivo:

1. **`memorys/business.md` — O Quê e Para Quem (Requisitos Funcionais)**:
   - Regras de negócio, terminologia do produto, modelos de domínio, fluxos de permissão do usuário, lógica de negócio.

2. **`memorys/architecture.md` — Como o sistema opera (Requisitos Não Funcionais)**:
   - Decisões de infra/arquitetura, conexão entre serviços, escalabilidade, escolhas tecnológicas (frameworks, banco, CI/CD). "Quais tecnologias sustentam o software e como os dados fluem macroarquiteturalmente".
   - Inclui a seção *Modelo de Ameaças* (alimentada pelo Security Specialist) e a seção *Segurança e Compliance* (provedor de identidade, criptografia, requisitos regulatórios).

3. **`memorys/guidelines.md` — Como codificar localmente (Sintaxe e Restrições)**:
   - Padrões táticos de desenvolvimento, convenções de equipe, linting, antipadrões e aprendizados de bugs já resolvidos (incluindo vulnerabilidades de segurança remediadas).
   - Inclui a seção *Personalidade e Tom de Voz* da squad.

## Workflow

### 1. Discovery Estrutural
Analisa o código-fonte e configurações do projeto, identificando manifestos primários (`package.json`, `pyproject.toml`, `.csproj`, `go.mod`, `pom.xml`, `Gemfile`, `Cargo.toml`, etc.) e lendo amostras representativas para extrair inteligência sobre stack, padrões e restrições.

### 2. Definição de Personalidade (Humor da Squad)
Disparar o seguinte prompt ao usuário:
> "Setup de contexto concluído. Por padrão a squad opera em modo **Neutro**. Deseja definir um humor específico (Sarcástico, Cordial, Amigável, Técnico-Rígido, Hostil, Motivacional, ou outro)?"

Após a resposta, registrar em `memorys/guidelines.md` na seção `# 🎭 Personalidade e Tom de Voz`. Todas as interações futuras entre agentes e com o usuário devem refletir esse humor, sem comprometer a eficiência técnica.

### 3. Memory Init (Mapeamento de Contexto Inicial)
- **`memorys/business.md`**: extrair regras de negócio primárias e requisitos funcionais detectados na varredura.
- **`memorys/architecture.md`**: mapear requisitos não funcionais, design do sistema, infraestrutura, arquitetura macro de componentes. Incluir uma linha sobre o provedor de identidade/auth detectado (se houver) na seção *Segurança e Compliance*.
- **`memorys/guidelines.md`**: listar tipagens, restrições técnicas, boas práticas e padrões de desenvolvimento detectados. Adicionar a regra de tom/humor escolhida.

### 4. Skill Specialization (Calibração da Stack)
Adaptar os comandos das skills sensíveis à stack para o ecossistema detectado:
- `.claude/skills/delivery/SKILL.md`: comandos de build, lint, test, version bump (`npm`, `yarn`, `pnpm`, `pip`, `poetry`, `go`, `mvn`, `cargo`, `dotnet`, etc.).
- `.claude/skills/security-audit/SKILL.md`: auditor de dependências (`npm audit`, `pip-audit`, `cargo audit`, `bundle audit`, etc.).
- `.claude/skills/infrastructure/SKILL.md`: idem para `audit` e gestão de pacotes.

> ATENÇÃO: a calibração ocorre por **registro nas memórias** ou por preferências locais — **não reescreva** os arquivos de skill (eles são agnósticos). Os comandos específicos da stack ficam em `memorys/architecture.md`, e os agentes consultam de lá.

### 5. Feedback Final
Após popular `memorys/`, resumir ao usuário:
- Stacks detectadas (linguagem, framework, banco, CI/CD).
- Personalidade adotada pela squad.
- Caminho onde a squad foi configurada (e qual ferramenta detectada/escolhida).
- Próximo passo sugerido (ex: "Pronto. Para abrir uma feature, use o workflow `nova-feature` ou simplesmente descreva a demanda — o Product Owner assume o controle.").
