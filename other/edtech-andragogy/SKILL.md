---
name: "edtech-andragogy"
description: "Atua como especialista em Tecnologia Educacional (EdTech) e metodologias de ensino para adultos (Andragogia), dominando design instrucional, gamificação e padrões de interoperabilidade (SCORM, LTI, xAPI)."
---

# 🧠 Tecnologia Educacional e Andragogia (edtech-andragogy)

Esta skill fornece diretrizes metodológicas, padrões de design instrucional e especificações de integração tecnológica voltadas à educação de adultos (Andragogia) e sistemas de tecnologia para educação (EdTech). Deve ser ativada sempre que o agente for solicitado a desenhar trilhas de aprendizagem, conceber fluxos de UX para plataformas e-learning, estruturar programas de treinamento corporativo ou integrar padrões de interoperabilidade técnica.

---

## 🎯 Objetivo da Skill
Capacitar o agente a atuar como um Designer Instrucional Sênior e Engenheiro de EdTech, assegurando que o conteúdo e as ferramentas de software criadas atendam às necessidades cognitivas dos adultos, promovam engajamento contínuo e utilizem protocolos interoperáveis de mercado.

---

## 👨‍💼 Andragogia: Metodologia de Aprendizagem de Adultos

Ao contrário da Pedagogia (focada em crianças), a Andragogia (formulada por Malcolm Knowles) foca nas características do aprendiz adulto. As interfaces, fluxos de plataforma e conteúdos devem seguir seus 6 princípios fundamentais:

| Princípio | Aplicação Prática no Design do LMS / Plataforma |
| :--- | :--- |
| **Necessidade de Saber** (*Need to Know*) | Exibir claramente os benefícios de cada aula e a aplicabilidade prática no trabalho ou carreira antes do início do curso. |
| **Autoconceito** (*Self-Concept*) | Oferecer autonomia. Permitir que o aluno adulto navegue em ritmo próprio, escolha sua ordem de tópicos e decida quando realizar avaliações. |
| **Papel da Experiência** (*Experience*) | Criar fóruns de discussão qualificada, estudos de caso abertos e espaços onde os aprendizes possam compartilhar suas próprias vivências profissionais. |
| **Prontidão para Aprender** (*Readiness*) | Alinhar o conteúdo a desafios cotidianos. O adulto aprende melhor aquilo que precisa para resolver um problema imediato no trabalho. |
| **Orientação para Aprendizagem** (*Orientation*) | Substituir a memorização pura de tópicos teóricos por metodologias ativas com foco em resolução de problemas reais (*Problem-Based Learning*). |
| **Motivação Interna** (*Motivation*) | Focar em conquistas internas (autoestima, satisfação no trabalho, desenvolvimento pessoal) e menos em recompensas puramente externas (grades/notas). |

---

## 📐 Frameworks de Design Instrucional

### 1. Modelo ADDIE (Cascata / Tradicional)
Ideal para projetos educacionais com escopo rígido, regulamentados ou de grande escala.
*   **A**nalysis (Análise): Identificação do público-alvo, objetivos pedagógicos e restrições.
*   **D**esign (Design): Esboço do roteiro, métodos de avaliação, taxonomia e fluxo de telas.
*   **D**evelopment (Desenvolvimento): Criação do conteúdo interativo, mídias e montagem do curso.
*   **I**mplementation (Implementação): Lançamento do treinamento aos alunos na plataforma LMS.
*   **E**valuation (Avaliação): Medição de eficácia (Modelo de Avaliação de Kirkpatrick - Reação, Aprendizado, Comportamento e Resultados).

### 2. Modelo SAM (Ágil / Iterativo)
*Successive Approximation Model*: Ideal para desenvolvimento rápido e flexível, utilizando ciclos curtos de prototipagem e feedback contínuos (*Design Loops*).
*   Priorize a criação de um **Protótipo Mínimo Viável (MVP)** do curso para teste rápido com um pequeno grupo de alunos antes do desenvolvimento total.

---

## 🔌 Padrões de Interoperabilidade EdTech

Para garantir que o conteúdo e as plataformas de terceiros funcionem harmonicamente com qualquer LMS (Moodle, Canvas, Blackboard), utilize os seguintes padrões:

### 1. SCORM (1.2 / 2004)
*   **O que é**: O padrão tradicional de empacotamento de cursos.
*   **Foco**: Monitorar a conclusão do curso e transmitir notas de questionários básicos para o boletim do LMS.
*   **Uso**: Ideal para conteúdos auto-instrucionais legados e pacotes fechados comprados de terceiros.

### 2. LTI (Learning Tools Interoperability - 1.3 / Advantage)
*   **O que é**: Um protocolo de integração baseado em OAuth2 e OpenID Connect para acoplar ferramentas de software externas (ex: laboratórios virtuais de programação, simuladores, ferramentas de videoconferência) diretamente dentro do LMS.
*   **Benefícios**: Permite Single Sign-On (SSO) do aluno do LMS para a ferramenta externa e retorna notas ou progresso gerado fora do LMS de volta ao livro de notas principal de forma segura.

### 3. xAPI (Experience API / Tin Can)
*   **O que é**: O padrão moderno para coleta de experiências e comportamento de aprendizagem.
*   **Diferencial**: Registra eventos em formato de declarações (*Actor-Verb-Object*, ex: "João visualizou o vídeo Y", "Maria concluiu a simulação Z") que ocorrem dentro ou fora do LMS (apps móveis, VR, simulações físicas).
*   **Armazenamento**: As informações são gravadas em um banco de dados de eventos chamado **LRS (Learning Record Store)**.

---

## 🎮 Gamificação e Aprendizado Ativo

*   **Microlearning**: Reduza conteúdos longos em pílulas de conhecimento de 3 a 5 minutos (vídeos curtos, infográficos interativos, quizzes) para respeitar o tempo limitado dos adultos.
*   **Badges Open Badges**: Implemente medalhas e certificados digitais verificáveis baseados na especificação Open Badges para celebrar conquistas de desenvolvimento de competências.
*   **Narrativas (Storytelling)**: Contextualize os cenários com simulações de tomadas de decisão onde o aluno assume um papel simulado enfrentando problemas reais do dia a dia corporativo.

---

## 🔗 Habilidades Relacionadas
*   **Moodle Core**: [program-moodle](../../programs/moodle/SKILL.md) — Customização geral e APIs do Moodle LMS.
*   **Moodle Design & UX**: [program-moodle-design](../../programs/moodle/SKILL.md) — Aplicação visual de metodologias ativas e acessibilidade WCAG.

