---
name: framework-spring-boot
description: "Fornece padrões de engenharia e arquitetura para aplicações corporativas com Spring Boot 3.x+, cobrindo Spring MVC REST, injeção de dependências por construtor, DTOs imutáveis (Records), Virtual Threads (Loom), validação, Spring Data JPA e testes com Testcontainers."
---

# Spring Boot Server Engineering & Best Practices

Esta skill estabelece os padrões e regras de engenharia de software para aplicações corporativas e microsserviços desenvolvidos com **Spring Boot 3.x+** e Java moderno (Java 17/21/25).

---

## 🧭 1. Princípios Arquiteturais e de Projeto
1. **Separação Limpa de Camadas**:
   - Manter anotações do framework nos pontos de entrada (REST Controllers), configuração e adaptadores de infraestrutura.
   - Evitar acoplamento de classes de domínio com anotações de serialização ou persistência sempre que possível.
2. **Injeção de Dependências Idiomática**:
   - Usar estritamente injeção via construtor com campos `final`. Evitar `@Autowired` direto em campos (dificulta testes e acopla a classe ao container de DI).
   - Injetar interfaces ou beans especializados em vez de classes de implementação diretas.
3. **Imutabilidade e DTOs Modernos**:
   - Usar Java `record` para todos os Data Transfer Objects (Requests e Responses), garantindo imutabilidade e validação estruturada com Jakarta Bean Validation (`@Valid`, `@NotNull`, `@NotBlank`, etc.).

---

## ⚡ 2. Performance, Concorrência e Virtual Threads
- **Virtual Threads (Project Loom)**: Em Spring Boot 3.2+, habilitar `spring.threads.virtual.enabled=true` para o servidor Tomcat embutido e tarefas assíncronas bloqueadas em I/O.
- **Evitar Pinning**: Em rotas que utilizam Virtual Threads, auditar o uso de `synchronized` substituindo por `ReentrantLock` em blocos com chamadas de rede ou banco de dados.
- **Spring Data JPA**: Evitar consultas N+1 utilizando `JOIN FETCH`, `@EntityGraph` ou projeções DTO dedicadas.

---

## 🧪 3. Estratégia de Testes
- **Testes Unitários Rápidos**: Testar serviços e regras de negócio sem carregar o contexto do Spring (`MockitoExtension`, instanciando a classe diretamente).
- **Testes Focados de Camada**: Usar `@WebMvcTest` para validar endpoints REST, filtros de segurança e serialização Jackson sem inicializar o banco de dados.
- **Testes de Integração com Testcontainers**: Usar `@SpringBootTest` com Testcontainers para instâncias reais de PostgreSQL, MySQL ou Redis.
