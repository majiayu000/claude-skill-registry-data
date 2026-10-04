---
name: arch-bce-pattern
description: "Especialista no padrão arquitetural Boundary-Control-Entity (BCE / ECB de Ivar Jacobson). Define a separação limpa entre interfaces externas (Boundary), lógica de negócio (Control) e entidades de domínio (Entity), com estratégias de migração incremental de código legado."
---

# Boundary-Control-Entity (BCE) Architecture Pattern

Esta skill define as diretrizes de engenharia e estratégias de modelagem para o padrão **Boundary-Control-Entity (BCE / ECB)**, formulado por Ivar Jacobson para desenvolvimento orientado a casos de uso e componentes de negócio desacoplados.

---

## 🏛️ 1. As Três Camadas Canônicas do BCE

```
[ Cliente Externo / UI ]
          │
          ▼
┌──────────────────┐
│     BOUNDARY     │  <-- Entrada, APIs REST/gRPC, Web, Mensageria, Tradução DTO
└─────────┬────────┘
          │
          ▼
┌──────────────────┐
│     CONTROL      │  <-- Coordenação do Caso de Uso, Regras de Negócio, Transações
└─────────┬────────┘
          │
          ▼
┌──────────────────┐
│      ENTITY      │  <-- Modelo de Domínio, Invariantes, Estado e Persistência
└──────────────────┘
```

### A. Boundary (Fronteira)
- Isola o componente do mundo externo (protocolos de rede, formato JSON, controladores HTTP, filas de mensageria).
- Responsabilidade: validação de entrada estrutural, roteamento de requisição e conversão de DTOs para modelos de domínio.
- **Regra**: Boundaries conversam apenas com Controls ou com Entities através de DTOs. Nunca chamam Entities diretamente para operações de mutação.

### B. Control (Controle / Caso de Uso)
- Orquestra os casos de uso do negócio e a sequência de operações.
- Responsabilidade: regras de fluxo, gerenciamento de transações, políticas de negócio e disparo de eventos de domínio.
- **Regra**: Controls não sabem de detalhes de transporte (sem anotações HTTP ou servlets); dependem apenas de interfaces e Entities.

### C. Entity (Entidade de Negócio)
- Encapsula o estado, a identidade e os invariantes de negócio fundamentais.
- Responsabilidade: cálculo interno de regras atômicas, persistência e consistência de dados.

---

## 🔄 2. Procedimento de Migração Incremental (Migrate-to-BCE)
Para refatorar um projeto legado para a arquitetura BCE sem quebras em produção:
1. **Identificar Componentes de Negócio (Business Components)**: Agrupar classes por capacidade de domínio em vez de apenas camadas técnicas.
2. **Extrair Boundaries**: Isolar classes `@RestController` ou `@Path` movendo-as para o pacote `boundary`.
3. **Desacoplar a Lógica de Serviço em Controls**: Mover o fluxo de orquestração de `@Service` monolíticos para classes de controle atômicas e focadas em cada caso de uso.
4. **Isolar Entities**: Manter entidades de persistência no pacote `entity`, protegendo seus invariantes.
