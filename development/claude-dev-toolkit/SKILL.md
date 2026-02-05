---
name: claude-dev-toolkit
description: Use this skill when the user wants to create Angular applications, generate Angular components/services/modules, or automate Angular development workflows. Handles scaffolding complete Angular apps with routing and guards, generating individual Angular artifacts, setting up project structure, and initializing git repositories with Angular best practices.
---

# Claude Dev Toolkit - Angular Development

This skill provides automated workflows for Angular development tasks.

## Capabilities

### 1. Angular Application Scaffolding
When the user requests an Angular app, create a well-structured Angular application with:
- Routing configuration
- Authentication guards
- Service structure
- Component architecture
- Core and Shared modules
- Best practices for folder organization

**Command to execute:**
```bash
ng new {app-name} --routing --style=scss
cd {app-name}
ng generate guard auth/guards/auth
ng generate service auth/services/auth
ng generate module core
ng generate module shared
ng generate component core/components/layout
```

Create folder structure:
- `src/app/core/` - Core functionality (singletons, guards, interceptors)
- `src/app/shared/` - Shared components, directives, pipes
- `src/app/features/` - Feature modules
- `src/app/auth/` - Authentication logic

After generation, create a README explaining the structure.

### 2. Angular Component Generation
Generate Angular components with proper structure:
```bash
ng generate component {path}/{component-name}
```

Include component, template, styles, and spec file. Use proper naming conventions.

### 3. Angular Service Generation
Generate Angular services:
```bash
ng generate service {path}/{service-name}
```

Follow singleton pattern for core services, place in appropriate module.

### 4. Angular Module Generation
Generate feature modules with routing:
```bash
ng generate module {module-name} --routing
```

### 5. Git Repository Initialization
Initialize a git repo with Angular-specific best practices:
- Create `.gitignore` for Angular/Node.js projects
- Initialize git
- Create initial commit
- Create a basic README with Angular commands
- Include common Angular build artifacts in .gitignore

### 6. Angular Guards & Interceptors
Generate guards and HTTP interceptors:
```bash
ng generate guard {path}/{guard-name}
ng generate interceptor {path}/{interceptor-name}
```

## Usage Guidelines

1. **Always verify prerequisites** - Check if Angular CLI is installed (`ng version`)
2. **Ask for confirmation** - Before creating files/folders, confirm names and locations
3. **Follow Angular style guide** - Use Angular naming conventions and best practices
4. **Provide next steps** - After generating, tell user how to use/integrate the code
5. **Document everything** - Create README files and code comments

## Example Interactions

User: "Create an Angular app called my-dashboard"
→ Use capability #1, verify ng is installed, create app with routing and guards

User: "Generate a user service"
→ Use capability #3, create service in appropriate location

User: "Add an auth guard"
→ Use capability #6, generate guard with authentication logic template

User: "Create a products feature module"
→ Use capability #4, generate module with routing
