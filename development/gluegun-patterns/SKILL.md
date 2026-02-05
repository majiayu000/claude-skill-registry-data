---
name: gluegun-patterns
description: Gluegun CLI toolkit patterns for TypeScript-powered command-line apps. Use when building CLI tools, creating command structures, implementing template systems, filesystem operations, HTTP utilities, prompts, or plugin architectures with Gluegun.
allowed-tools: Read, Write, Edit, Bash, Glob
---

# Gluegun CLI Toolkit Patterns

Provides comprehensive patterns and templates for building TypeScript-powered CLI applications using the Gluegun toolkit. Gluegun offers parameters, templates, filesystem operations, HTTP utilities, prompts, and extensible plugin architecture.

## Core Capabilities

Gluegun provides these essential toolbox features:

1. **Parameters** - Command-line arguments and options parsing
2. **Template** - EJS-based file generation from templates
3. **Filesystem** - File and directory operations (fs-jetpack)
4. **System** - Execute external commands and scripts
5. **HTTP** - API interactions with axios/apisauce
6. **Prompt** - Interactive user input with enquirer
7. **Print** - Colorful console output with colors/ora
8. **Patching** - Modify existing file contents
9. **Semver** - Version string manipulation
10. **Plugin System** - Extensible command architecture

## Instructions

### Building a Basic CLI

1. **Initialize Gluegun CLI structure:**
   ```typescript
   import { build } from 'gluegun'

   const cli = build()
     .brand('mycli')
     .src(__dirname)
     .plugins('./node_modules', { matching: 'mycli-*', hidden: true })
     .help()
     .version()
     .create()
   ```

2. **Create command structure:**
   - Commands go in `src/commands/` directory
   - Each command exports a `GluegunCommand` object
   - Use templates from `templates/` directory
   - Reference template: `templates/commands/basic-command.ts.ejs`

3. **Implement command with toolbox:**
   ```typescript
   module.exports = {
     name: 'generate',
     run: async (toolbox) => {
       const { template, print, parameters } = toolbox
       const name = parameters.first

       await template.generate({
         template: 'model.ts.ejs',
         target: `src/models/${name}.ts`,
         props: { name }
       })

       print.success(`Generated ${name} model`)
     }
   }
   ```

### Template System

1. **Template file structure:**
   - Store templates in `templates/` directory
   - Use EJS syntax: `<%= variable %>`, `<%- unescaped %>`
   - Reference: `templates/toolbox/template-examples.ejs`

2. **Generate files from templates:**
   ```typescript
   await template.generate({
     template: 'component.tsx.ejs',
     target: `src/components/${name}.tsx`,
     props: { name, style: 'functional' }
   })
   ```

3. **Helper functions:**
   - `props.camelCase` - camelCase conversion
   - `props.pascalCase` - PascalCase conversion
   - `props.kebabCase` - kebab-case conversion
   - Reference: `scripts/template-helpers.ts`

### Filesystem Operations

1. **Common operations (fs-jetpack):**
   ```typescript
   // Read/write files
   const config = await filesystem.read('config.json', 'json')
   await filesystem.write('output.txt', data)

   // Directory operations
   await filesystem.dir('src/components')
   const files = filesystem.find('src', { matching: '*.ts' })

   // Copy/move/remove
   await filesystem.copy('template', 'output')
   await filesystem.move('old.txt', 'new.txt')
   await filesystem.remove('temp')
   ```

2. **Path utilities:**
   ```typescript
   filesystem.path('src', 'commands') // Join paths
   filesystem.cwd() // Current directory
   filesystem.separator // OS-specific separator
   ```

### HTTP Utilities

1. **API interactions:**
   ```typescript
   const api = http.create({
     baseURL: 'https://api.example.com',
     headers: { 'Authorization': 'Bearer token' }
   })

   const response = await api.get('/users')
   const result = await api.post('/users', { name: 'John' })
   ```

2. **Error handling:**
   ```typescript
   if (!response.ok) {
     print.error(response.problem)
     return
   }
   ```

### Interactive Prompts

1. **User input patterns:**
   ```typescript
   // Ask question
   const result = await prompt.ask({
     type: 'input',
     name: 'name',
     message: 'What is your name?'
   })

   // Confirm action
   const proceed = await prompt.confirm('Continue?')

   // Select from list
   const choice = await prompt.ask({
     type: 'select',
     name: 'framework',
     message: 'Choose framework:',
     choices: ['React', 'Vue', 'Angular']
   })
   ```

2. **Multi-select and complex forms:**
   - Reference: `examples/prompts/multi-select.ts`
   - See: `templates/toolbox/prompt-examples.ts.ejs`

### Plugin Architecture

1. **Create extensible plugins:**
   ```typescript
   // Plugin structure
   export default (toolbox) => {
     const { filesystem, template } = toolbox

     // Add custom extension
     toolbox.myFeature = {
       doSomething: () => { /* ... */ }
     }
   }
   ```

2. **Load plugins:**
   ```typescript
   cli.plugins('./node_modules', { matching: 'mycli-*' })
   cli.plugins('./plugins', { matching: '*.js' })
   ```

3. **Plugin examples:**
   - Reference: `examples/plugin-system/custom-plugin.ts`
   - See: `templates/plugins/plugin-template.ts.ejs`

### Print Utilities

1. **Colorful output:**
   ```typescript
   print.info('Information message')
   print.success('Success message')
   print.warning('Warning message')
   print.error('Error message')
   print.highlight('Highlighted text')
   print.muted('Muted text')
   ```

2. **Spinners and progress:**
   ```typescript
   const spinner = print.spin('Loading...')
   await doWork()
   spinner.succeed('Done!')

   // Or fail
   spinner.fail('Something went wrong')
   ```

3. **Tables and formatting:**
   ```typescript
   print.table([
     ['Name', 'Age'],
     ['John', '30'],
     ['Jane', '25']
   ])
   ```

### System Commands

1. **Execute external commands:**
   ```typescript
   const output = await system.run('npm install')
   const result = await system.exec('git status')

   // Spawn with options
   await system.spawn('npm run build', { stdio: 'inherit' })
   ```

2. **Check command availability:**
   ```typescript
   const hasGit = await system.which('git')
   ```

### File Patching

1. **Modify existing files:**
   ```typescript
   // Add line after pattern
   await patching.update('package.json', (content) => {
     const pkg = JSON.parse(content)
     pkg.scripts.build = 'tsc'
     return JSON.stringify(pkg, null, 2)
   })

   // Insert import statement
   await patching.insert('src/index.ts', 'import { Router } from "express"')
   ```

## Validation Scripts

Use these scripts to validate Gluegun CLI implementations:

- `scripts/validate-cli-structure.sh` - Check directory structure
- `scripts/validate-commands.sh` - Verify command format
- `scripts/validate-templates.sh` - Check template syntax
- `scripts/test-cli-build.sh` - Run full CLI build test

## Templates

### Command Templates
- `templates/commands/basic-command.ts.ejs` - Simple command
- `templates/commands/generator-command.ts.ejs` - File generator
- `templates/commands/api-command.ts.ejs` - HTTP interaction

### Extension Templates
- `templates/extensions/custom-toolbox.ts.ejs` - Toolbox extension
- `templates/extensions/helper-functions.ts.ejs` - Utility functions

### Plugin Templates
- `templates/plugins/plugin-template.ts.ejs` - Plugin structure
- `templates/plugins/plugin-with-commands.ts.ejs` - Plugin with commands

### Toolbox Templates
- `templates/toolbox/template-examples.ejs` - Template patterns
- `templates/toolbox/prompt-examples.ts.ejs` - Prompt patterns
- `templates/toolbox/filesystem-examples.ts.ejs` - Filesystem patterns

## Examples

### Basic CLI Example
See `examples/basic-cli/` for complete working CLI:
- Simple command structure
- Template generation
- User prompts
- File operations

### Plugin System Example
See `examples/plugin-system/` for extensible architecture:
- Plugin loading
- Custom toolbox extensions
- Command composition

### Template Generator Example
See `examples/template-generator/` for advanced patterns:
- Multi-file generation
- Conditional templates
- Helper functions

## Best Practices

1. **Command Organization**
   - One command per file
   - Group related commands in subdirectories
   - Use clear, descriptive command names

2. **Template Design**
   - Keep templates simple and focused
   - Use helper functions for complex logic
   - Document template variables

3. **Error Handling**
   - Check HTTP response status
   - Validate user input from prompts
   - Provide helpful error messages

4. **Plugin Architecture**
   - Make plugins optional
   - Document plugin interfaces
   - Version plugin APIs

5. **Testing**
   - Test commands in isolation
   - Mock filesystem operations
   - Validate template output

## Security Considerations

- Never hardcode API keys in templates
- Use environment variables for secrets
- Validate all user input from prompts
- Sanitize file paths from parameters
- Check filesystem permissions before operations

## Requirements

- Node.js 14+ or TypeScript 4+
- Gluegun package: `npm install gluegun`
- EJS for templates (included)
- fs-jetpack for filesystem (included)
- enquirer for prompts (included)

## Related Documentation

- Gluegun Official Docs: https://infinitered.github.io/gluegun/
- GitHub Repository: https://github.com/infinitered/gluegun
- EJS Templates: https://ejs.co/
- fs-jetpack: https://github.com/szwacz/fs-jetpack

---

**Purpose**: Enable rapid CLI development with Gluegun patterns and best practices
**Load when**: Building CLI tools, command structures, template systems, or plugin architectures
