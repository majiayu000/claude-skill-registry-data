---
name: code-review
description: Realize análises de código seguindo as práticas de engenharia da Sentry. Use ao revisar pull requests, examinar alterações de código ou fornecer feedback sobre qualidade de código. Abrange segurança, performance, testes e revisão de design.
---

# Revisão de Código Sentry

Siga estas diretrizes ao revisar código de projetos Sentry.

## Checklist de Revisão

### Identificando Problemas

Procure por estes problemas nas alterações de código:

- **Erros em runtime**: Exceções potenciais, problemas de null pointer, acesso fora dos limites
- **Performance**: Operações O(n²) ilimitadas, consultas N+1, alocações desnecessárias
- **Efeitos colaterais**: Mudanças comportamentais não intencionais afetando outros componentes
- **Compatibilidade com versões anteriores**: Alterações de API que quebram compatibilidade sem caminho de migração
- **Consultas ORM**: Django ORM complexo com performance inesperada de consultas
- **Vulnerabilidades de segurança**: Injeção, XSS, lacunas no controle de acesso, exposição de secrets

### Avaliação de Design

- As interações entre componentes fazem sentido lógico?
- A alteração está alinhada com a arquitetura atual do projeto?
- Há conflitos com requisitos ou objetivos atuais?

### Cobertura de Testes

Todo PR deve ter cobertura de testes apropriada:

- Testes funcionais para lógica de negócio
- Testes de integração para interações entre componentes
- Testes end-to-end para caminhos críticos do usuário

Verifique se os testes cobrem requisitos reais e casos extremos. Evite ramificações ou loops excessivos no código de teste.

### Impacto a Longo Prazo

Sinalize para revisão de engenheiro sênior quando as alterações envolverem:

- Modificações de schema de banco de dados
- Alterações de contrato de API
- Adoção de novo framework ou biblioteca
- Caminhos de código críticos para performance
- Funcionalidade sensível a segurança

## Diretrizes de Feedback

### Tom

- Seja educado e empático
- Forneça sugestões acionáveis, não críticas vagas
- Formule como perguntas quando incerto: "Você considerou...?"

### Aprovação

- Aprove quando apenas problemas menores permanecerem
- Não bloqueie PRs por preferências estilísticas
- Lembre-se: o objetivo é reduzir riscos, não obter código perfeito

## Padrões Comuns para Sinalizar

### Python/Django

```python
# Bad: N+1 query
for user in users:
    print(user.profile.name)  # Separate query per user

# Good: Prefetch related
users = User.objects.prefetch_related('profile')
```

### TypeScript/React

```typescript
// Bad: Missing dependency in useEffect
useEffect(() => {
  fetchData(userId);
}, []);  // userId not in deps

// Good: Include all dependencies
useEffect(() => {
  fetchData(userId);
}, [userId]);
```

### Segurança

```python
# Bad: SQL injection risk
cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")

# Good: Parameterized query
cursor.execute("SELECT * FROM users WHERE id = %s", [user_id])
```

## Referências

- [Diretrizes de Revisão de Código Sentry](https://develop.sentry.dev/engineering-practices/code-review/)