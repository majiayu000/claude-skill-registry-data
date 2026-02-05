---
name: nestjs-patterns
description: Master NestJS framework with modules, controllers, services, dependency injection, guards, interceptors, and microservices patterns for enterprise applications.
---

# NestJS Patterns

Build enterprise-grade applications with NestJS using modular architecture, dependency injection, and production-ready patterns.

## Core Patterns

### Module Pattern
```typescript
@Module({
  imports: [TypeOrmModule.forFeature([User])],
  controllers: [UserController],
  providers: [UserService],
  exports: [UserService],
})
export class UserModule {}
```

### Controller Pattern
```typescript
@Controller('users')
@UseGuards(JwtAuthGuard)
export class UserController {
  constructor(private readonly userService: UserService) {}

  @Get()
  findAll(): Promise<User[]> {
    return this.userService.findAll();
  }

  @Post()
  create(@Body() createUserDto: CreateUserDto): Promise<User> {
    return this.userService.create(createUserDto);
  }
}
```

### Service Pattern
```typescript
@Injectable()
export class UserService {
  constructor(
    @InjectRepository(User)
    private userRepository: Repository<User>,
  ) {}

  async findAll(): Promise<User[]> {
    return this.userRepository.find();
  }

  async create(createUserDto: CreateUserDto): Promise<User> {
    const user = this.userRepository.create(createUserDto);
    return this.userRepository.save(user);
  }
}
```

## Best Practices

1. Use dependency injection
2. Implement proper error handling
3. Use DTOs for validation
4. Implement guards for authentication
5. Use interceptors for logging
6. Create custom decorators
7. Implement microservices patterns
8. Write comprehensive tests

## Resources
- https://nestjs.com
