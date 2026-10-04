---
name: ats-resume-optimization
description: "Especialista em Engenharia e Otimização de Currículos para Sistemas ATS (Applicant Tracking Systems). Domina parsing unicolunar, densidade semântica de keywords, acrônimos, métricas de impacto pela fórmula XYZ e auditoria de compatibilidade com descrições de vagas."
---

# ATS Resume Optimization & Keyword Engineering

Esta skill estabelece a metodologia técnica e analítica para arquitetura, revisão e otimização de currículos orientados a sistemas **ATS (Applicant Tracking Systems)** como Greenhouse, Lever, Workday, Taleo, iCIMS e Ashby.

---

## 🧭 1. Princípios de Parsing Algorítmico de Currículos
O ATS converte o arquivo em texto bruto através de OCR/Parser semântico antes de calcular a pontuação de aderência (*Match Score*). Para evitar perda de dados e corrupção estrutural:

1. **Layout Estritamente Unicolunar**:
   - Nunca use tabelas, grades multi-colunas, caixas de texto flutuantes ou barras laterais.
   - Textos inseridos em caixas de texto são frequentemente ignorados pelo parser.
2. **Cabeçalhos Universais e Padronizados**:
   - Use termos exatos: `Resumo Profissional` (ou `Professional Summary`), `Experiência Profissional` (`Work Experience`), `Formação Acadêmica` (`Education`), `Habilidades Técnicas` (`Technical Skills`).
   - Evite termos criativos como "O que me move" ou "Minha trajetória".
3. **Formatação de Dados de Contato**:
   - Coloque nome, email, telefone, LinkedIn e cidade/país no corpo principal superior do documento (nunca em rodapés ou cabeçalhos do Word/PDF).
4. **Formato de Datas Uniforme**:
   - Use formato consistente em todas as posições: `MM/AAAA - MM/AAAA` (ex.: `03/2022 - Atual`).

---

## 🎯 2. Engenharia de Palavras-Chave e Scoring
Os algoritmos de ATS ranqueiam candidatos comparando a densidade, frequência e contexto semântico das palavras-chave da vaga com o currículo:

- **Mapeamento de Hard Skills e Ferramentas**:
  - Extrair as tecnologias, metodologias e certificações exigidas no descritivo da vaga.
  - Assegurar a presença tanto do termo por extenso quanto de seu acrônimo:
    - Exemplo: `Search Engine Optimization (SEO)`, `Amazon Web Services (AWS)`, `Continuous Integration / Continuous Delivery (CI/CD)`.
- **Contextualização Obrigatória**:
  - Não crie listas estéreis de palavras-chave no final do documento (penalizadas por parsers modernos). Integre os termos nas descrições de realizações.

---

## 📊 3. Fórmula de Impacto de Linhas de Experiência (Google XYZ Formula)
Toda linha de conquista deve seguir a fórmula de alto impacto:
$$\text{Alcancei [X]}, \text{ medido por [Y]}, \text{ através de [Z]}$$

- **Fraco**: "Responsável por desenvolver a API de pagamentos."
- **Forte (XYZ)**: "Reduzi a latência de processamento de pagamentos em 35% (de 1.2s para 780ms) para 200 mil transações diárias através da refatoração de endpoints e implementação de cache distribuído em Redis."

---

## ✅ 4. Checklist Pré-Submissão (Auditoria ATS)
- [ ] Layout de coluna única sem tabelas, caixas de texto ou imagens.
- [ ] Nome e contatos no corpo do documento (não em header/footer).
- [ ] Mínimo de 75% a 85% de correspondência semântica de palavras-chave essenciais.
- [ ] Conquistas metrificadas com porcentagens, valores financeiros, latência ou volume.
- [ ] Arquivo salvo em `.docx` ou `.pdf` com camada de texto selecionável (não rasterizado).
