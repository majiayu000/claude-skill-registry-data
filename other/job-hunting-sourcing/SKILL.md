---
name: job-hunting-sourcing
description: "Especialista em Mineração Ativa e Busca Estratégica de Vagas de Emprego. Domina Google Dorks para portais de ATS diretos (Greenhouse, Lever, Workday, Ashby), operadores booleanos de localização e senioridade, e técnicas de abordagem direta a hiring managers."
---

# Job Hunting & Sourcing Intelligence (Boolean & ATS Dorks)

Esta skill estabelece técnicas avançadas de inteligência e mineração ativa de vagas na internet, permitindo localizar oportunidades diretamente nas plataformas de ATS corporativas antes de sua republicação em agregadores.

---

## 🔍 1. Google Dorks para Plataformas ATS Diretas

Muitas empresas publicam vagas em seus próprios portais de ATS antes de alimentarem plataformas pagas. Utilize as sintaxes booleanas abaixo:

| Plataforma ATS | Operador de Busca | Exemplo de Query |
| :--- | :--- | :--- |
| **Greenhouse** | `site:boards.greenhouse.io` | `site:boards.greenhouse.io ("software engineer" OR "backend") "remote" "brazil"` |
| **Lever** | `site:jobs.lever.co` | `site:jobs.lever.co ("java" OR "spring") "remoto" -estágio` |
| **Workday** | `site:myworkdayjobs.com` | `site:myworkdayjobs.com "cloud architect" ("aws" OR "gcp") "latam"` |
| **Ashby** | `site:jobs.ashbyhq.com` | `site:jobs.ashbyhq.com "tech lead" "remote"` |

### A. Busca Agrupada Multi-Plataforma
```text
(site:boards.greenhouse.io OR site:jobs.lever.co OR site:jobs.ashbyhq.com OR site:myworkdayjobs.com) ("software engineer" OR "developer") ("remote" OR "remoto") after:2026-08-01
```

### B. Filtros de Exclusão e Nível de Senioridade
- Para vagas plenas/sêniores sem liderança executiva:
  `site:boards.greenhouse.io "backend developer" -senior -principal -director -intern`

---

## 📨 2. Estratégia de Abordagem Direta (Cold Outreach)
Para vagas concorridas, complementar a candidatura formal no ATS com contato direcionado com o Hiring Manager ou Recrutador técnico:

1. **Localização do Decisor**: Identificar no LinkedIn quem lidera a equipe da vaga (ex.: Engineering Manager, Head of Tech).
2. **Mensagem Curta e Objetiva (Max 75 palavras)**:
   - Apresentar como sua experiência específica resolve um gargalo imediato da equipe.
   - Referenciar a candidatura realizada no portal.
   - Fornecer links rápidos para o currículo e portfólio GitHub.
