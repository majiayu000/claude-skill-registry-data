---
name: Backend API
description: Design and implement NestJS REST API endpoints following the project's layered architecture (Controllers, Use Cases, Repositories). Use this skill when creating or modifying controller files (*.controller.ts), defining API routes, implementing HTTP handlers, setting up Swagger documentation, configuring route guards and decorators, working with request/response DTOs, or structuring API endpoints. This includes files in features/{feature}/controller/, auth/controller/, and any file with @Controller() decorator. Apply when working with API_ENDPOINTS constants, @Get/@Post/@Put/@Patch/@Delete decorators, @ApiTags/@ApiProperty swagger decorators, @Public/@MemberRoles custom decorators, HttpCode/HttpStatus configurations, or Query/Param/Body parameter decorators.
---

## When to use this skill

- When creating new API endpoints or controllers (\*.controller.ts files)
- When modifying existing HTTP route handlers in NestJS controllers
- When adding or updating Swagger/OpenAPI documentation decorators
- When implementing route-level authentication and authorization (guards, @Public, @MemberRoles)
- When defining request DTOs for query params, route params, or request bodies
- When defining response DTOs and handling HTTP status codes
- When working with files in `features/{feature}/controller/` or `auth/controller/` directories
- When using API_ENDPOINTS constants from @imkdw-dev/consts
- When structuring controller constructor dependency injection

# Backend API

This Skill provides Claude Code with specific guidance on how to adhere to coding standards as they relate to how it should handle backend API.

## Instructions

For details, refer to the information provided in this file:
[backend API](../../../agent-os/standards/backend/api.md)

## Project-Specific Patterns

### Controller Structure

```typescript
@ApiTags('Feature Name')
@Controller()
@MemberRoles(MEMBER_ROLE.ADMIN) // Default role guard
export class FeatureController {
  constructor(
    private readonly createUseCase: CreateUseCase,
    private readonly updateUseCase: UpdateUseCase,
    private readonly getQuery: GetQuery
  ) {}
}
```

### Route Handler Pattern

```typescript
@Swagger.getItems('Description')
@Public()  // For public endpoints
@Get(API_ENDPOINTS.GET_ITEMS)
async getItems(@Query() query: RequestDto): Promise<ResponseDto> {
  return this.query.execute(query);
}

@Swagger.createItem('Description')
@Post(API_ENDPOINTS.CREATE_ITEM)
async createItem(@Body() dto: CreateDto) {
  const result = await this.useCase.execute(dto);
  return ResponseDto.from(result);
}

@Swagger.updateItem('Description')
@HttpCode(HttpStatus.NO_CONTENT)
@Put(API_ENDPOINTS.UPDATE_ITEM)
async updateItem(@Param('id') id: string, @Body() dto: UpdateDto): Promise<void> {
  await this.useCase.execute(id, dto);
}
```

### Key Conventions

- Use `HttpStatus.NO_CONTENT` for update/delete operations returning void
- Separate read operations (Query classes) from write operations (UseCase classes)
- Import API endpoints from `@imkdw-dev/consts` package
- Use feature-specific Swagger decorators from `swagger/{feature}.swagger.ts`
