---
name: backend-technologies
description: Master backend development with Node.js, Python, Java, Go, Rust, API design, databases, and microservices. Use when building APIs, designing systems, or learning backend frameworks.
sasmp_version: "1.3.0"
bonded_agent: 02-typescript-backend
bond_type: PRIMARY_BOND
---

# Backend Technologies Skill

## Quick Start - Express.js API

```typescript
import express, { Request, Response } from 'express';
import { prisma } from './lib/prisma';

const app = express();
app.use(express.json());

// GET all users
app.get('/users', async (req: Request, res: Response) => {
  try {
    const users = await prisma.user.findMany();
    res.json(users);
  } catch (error) {
    res.status(500).json({ error: 'Failed to fetch users' });
  }
});

// POST new user
app.post('/users', async (req: Request, res: Response) => {
  const { email, name } = req.body;
  try {
    const user = await prisma.user.create({
      data: { email, name }
    });
    res.status(201).json(user);
  } catch (error) {
    res.status(400).json({ error: 'Invalid data' });
  }
});

app.listen(3000, () => console.log('Server running on 3000'));
```

## Core Technologies

### Languages
- **Node.js** - JavaScript runtime
- **Python** - Versatile with many frameworks
- **Java** - Enterprise standard
- **Go** - Concurrent systems
- **Rust** - Systems programming

### Web Frameworks
- Express, Fastify, NestJS (Node.js)
- Django, FastAPI, Flask (Python)
- Spring Boot, Quarkus (Java)
- Gin, Fiber (Go)
- Actix, Axum (Rust)

### Databases
- **SQL**: PostgreSQL, MySQL
- **NoSQL**: MongoDB, DynamoDB
- **Cache**: Redis, Memcached
- **Search**: Elasticsearch

### API & Messaging
- REST APIs with best practices
- GraphQL API design
- gRPC for microservices
- WebSockets for real-time
- Kafka, RabbitMQ for messaging

### ORM/Query Tools
- Prisma, Sequelize (Node.js)
- SQLAlchemy, Tortoise (Python)
- Hibernate, Spring Data (Java)
- GORM (Go)

## Best Practices

1. **API Design** - RESTful or GraphQL standards
2. **Database** - Proper indexing and optimization
3. **Security** - Input validation, parameterized queries
4. **Error Handling** - Meaningful error messages
5. **Testing** - Unit and integration tests
6. **Documentation** - OpenAPI/Swagger docs
7. **Logging** - Structured logging
8. **Performance** - Response time optimization

## Resources

- [Express.js Documentation](https://expressjs.com/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Spring Boot Guide](https://spring.io/projects/spring-boot)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [GraphQL Official](https://graphql.org/)
