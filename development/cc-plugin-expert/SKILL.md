---
name: cc-plugin-expert
description: 'Comprehensive Claude Code plugin development expert providing guidance for creation, maintenance, installation, configuration, and troubleshooting of plugins and skills'
category: development
tags:
  [
    'claude-code',
    'plugin-development',
    'skill-creation',
    'maintenance',
    'troubleshooting',
    'best-practices',
  ]
triggers:
  - type: keyword
    pattern: 'create plugin'
    priority: 3
  - type: keyword
    pattern: 'plugin development'
    priority: 3
  - type: keyword
    pattern: 'claude code plugin'
    priority: 3
  - type: keyword
    pattern: 'skill creation'
    priority: 3
  - type: keyword
    pattern: 'plugin troubleshooting'
    priority: 2
  - type: keyword
    pattern: 'plugin installation'
    priority: 2
  - type: keyword
    pattern: 'plugin configuration'
    priority: 2
  - type: keyword
    pattern: 'plugin maintenance'
    priority: 2
  - type: pattern
    pattern: 'how to (create|build|develop) (a )?claude code plugin'
    priority: 3
  - type: pattern
    pattern: '(fix|troubleshoot|debug) (my )?claude code plugin'
    priority: 2
  - type: pattern
    pattern: '(install|configure|setup) (a )?claude code plugin'
    priority: 2
  - type: context
    pattern: 'plugin-development'
    priority: 2
  - type: context
    pattern: 'claude-code-ecosystem'
    priority: 1
---

# Claude Code Plugin Expert

This skill provides comprehensive expertise for Claude Code plugin development, including creation, installation, configuration, maintenance, and troubleshooting. It serves as the definitive resource for developers working with Claude Code plugins and skills.

## When to Use This Skill

Use this skill when you need to:

- **Create new plugins** from scratch or templates
- **Develop custom skills** for specific workflows
- **Install and configure** plugins in various environments
- **Troubleshoot plugin issues** and errors
- **Maintain and update** existing plugins
- **Optimize plugin performance** and security
- **Understand best practices** for plugin development
- **Debug plugin execution** problems
- **Configure plugin permissions** and security
- **Manage plugin dependencies** and versions

## Core Capabilities

### 1. Plugin Development Guidance

- Complete plugin architecture understanding
- Step-by-step plugin creation workflows
- Code structure and organization patterns
- TypeScript/JavaScript best practices
- Plugin manifest configuration
- Command and skill implementation

### 2. Installation and Configuration

- Multiple installation methods (marketplace, local, git)
- Environment-specific configuration
- Permission management and security
- Dependency resolution and versioning
- Marketplace configuration
- Enterprise deployment strategies

### 3. Troubleshooting and Debugging

- Common plugin issues and solutions
- Performance optimization techniques
- Error handling and logging strategies
- Debugging tools and methodologies
- Plugin isolation and testing
- Health monitoring and analytics

### 4. Best Practices and Standards

- Code quality standards and patterns
- Security considerations and validation
- Performance optimization strategies
- Testing methodologies and frameworks
- Documentation standards
- Community guidelines and contribution

## Development Framework

### Phase 1: Requirements Analysis

- Understand plugin purpose and scope
- Identify target users and use cases
- Determine required permissions and dependencies
- Plan plugin architecture and components
- Define success criteria and metrics

### Phase 2: Design and Planning

- Create plugin structure and manifest
- Design command and skill interfaces
- Plan configuration and settings
- Consider security and performance requirements
- Document technical specifications

### Phase 3: Implementation

- Set up development environment
- Create plugin directory structure
- Implement core plugin functionality
- Add commands and skills
- Include error handling and logging

### Phase 4: Testing and Validation

- Unit testing of components
- Integration testing with Claude Code
- Performance testing and optimization
- Security testing and validation
- User acceptance testing

### Phase 5: Deployment and Maintenance

- Package plugin for distribution
- Install and configure in target environments
- Monitor performance and usage
- Update and maintain over time
- Handle user feedback and issues

## Plugin Architecture Understanding

### Core Components

- **Plugin Manifest**: Metadata and configuration
- **Commands**: Slash commands for user interaction
- **Skills**: AI-triggered capabilities
- **MCP Servers**: External tool integrations
- **Event Hooks**: Automated response handlers
- **Custom Agents**: Specialized AI agents

### Directory Structure

```
my-plugin/
├── .claude-plugin/
│   ├── plugin.json          # Plugin metadata
│   └── marketplace.json     # Distribution config
├── commands/                # Custom slash commands
│   ├── command1.md
│   └── command2.md
├── skills/                  # Agent skills
│   └── my-skill/
│       └── SKILL.md
├── agents/                  # Custom agents
│   └── custom-agent.json
├── hooks/                   # Event handlers
│   └── hooks.json
├── mcp/                     # MCP server configs
│   └── server.json
├── scripts/                 # Helper scripts
├── templates/               # Code templates
└── README.md               # Plugin documentation
```

## Installation Methods

### 1. Interactive Marketplace Installation

```bash
claude
/plugin
```

### 2. Direct Command Installation

```bash
# Install from marketplace
claude marketplace install plugin-name@marketplace-name

# Install from local directory
claude marketplace install ./my-plugin

# Install from Git repository
claude marketplace install https://github.com/user/plugin-repo.git

# Install specific version
claude marketplace install plugin-name@1.2.3
```

### 3. Configuration File Installation

```json
{
  "plugins": ["my-awesome-plugin@latest", "code-formatter@2.1.0", "database-tools@github:user/repo"]
}
```

## Configuration Management

### Settings File Structure

```json
{
  "version": "1.0.0",
  "plugins": {
    "sources": [
      {
        "type": "marketplace",
        "name": "official",
        "url": "https://github.com/claude-official/marketplace",
        "enabled": true
      }
    ],
    "installed": [
      {
        "name": "code-formatter",
        "version": "2.1.0",
        "source": "official",
        "installedAt": "2024-01-15T10:30:00Z",
        "enabled": true,
        "autoUpdate": true
      }
    ]
  },
  "permissions": {
    "allowedDomains": ["github.com", "api.github.com"],
    "allowedCommands": ["git", "npm", "node"],
    "filesystemAccess": ["read", "write"],
    "networkAccess": true
  }
}
```

## Common Issues and Solutions

### Plugin Not Found

- Verify marketplace configuration
- Check plugin name spelling
- Confirm plugin exists in marketplace
- Test network connectivity

### Permission Denied

- Check file system permissions
- Verify plugin permissions
- Review security settings
- Use alternative installation directory

### Version Conflicts

- Check dependency tree
- Use specific version constraints
- Resolve conflicts automatically
- Force reinstall if needed

### Performance Issues

- Implement lazy loading
- Add caching strategies
- Monitor resource usage
- Optimize code execution

## Development Best Practices

### Code Quality

- Use TypeScript with strict configuration
- Implement comprehensive error handling
- Follow consistent naming conventions
- Add proper documentation and comments
- Use ESLint and Prettier for code formatting

### Security

- Validate all input parameters
- Implement proper permission management
- Use secure plugin execution patterns
- Scan dependencies for vulnerabilities
- Follow principle of least privilege

### Performance

- Use lazy loading for resources
- Implement caching strategies
- Monitor memory usage
- Optimize database queries
- Use asynchronous operations

### Testing

- Write comprehensive unit tests
- Implement integration testing
- Test error scenarios
- Monitor plugin performance
- Test security boundaries

## Debugging Tools and Techniques

### Debug Logging

```typescript
// Enable debug logging
export CLAUDE_DEBUG=true
claude --verbose

// Check plugin status
claude plugin list
claude plugin status plugin-name
```

### Performance Monitoring

```typescript
class PerformanceMonitor {
  async measure<T>(
    operation: () => Promise<T>,
    operationName: string
  ): Promise<{ result: T; metrics: PerformanceMetrics }> {
    // Implementation for performance measurement
  }
}
```

### Error Analysis

- Review error logs and stack traces
- Check plugin initialization sequence
- Validate configuration files
- Test with minimal dependencies
- Use isolated test environments

## Security Considerations

### Input Validation

- Sanitize all user inputs
- Validate parameter types and ranges
- Prevent injection attacks
- Use whitelist validation

### Permission Management

- Request minimum required permissions
- Implement permission checks
- Use secure file access patterns
- Validate network requests

### Dependency Security

- Scan dependencies for vulnerabilities
- Keep dependencies updated
- Use trusted sources
- Review license compatibility

## Advanced Features

### Plugin Communication

- Event-driven architecture
- Inter-plugin messaging
- Shared resource management
- Dependency injection

### Enterprise Features

- Centralized configuration management
- Team-based plugin distribution
- Security policy enforcement
- Usage analytics and reporting

### Performance Optimization

- Lazy loading strategies
- Memory management
- Caching implementations
- Resource pooling

## Community Resources

### Documentation

- Official Claude Code documentation
- Plugin development guides
- API reference documentation
- Best practice guides

### Support Channels

- GitHub discussions and issues
- Community forums
- Stack Overflow
- Discord/Slack communities

### Contributing

- Fork and clone repositories
- Create feature branches
- Submit pull requests
- Participate in code reviews

## Quality Assurance Checklist

### Before Release

- [ ] Code follows all style guidelines
- [ ] All tests pass successfully
- [ ] Documentation is complete and accurate
- [ ] Security review passed
- [ ] Performance benchmarks met
- [ ] Plugin tested in multiple environments
- [ ] Error handling comprehensive
- [ ] Dependencies validated

### After Installation

- [ ] Plugin loads without errors
- [ ] Commands function correctly
- [ ] Skills trigger appropriately
- [ ] Configuration works as expected
- [ ] Permissions are properly enforced
- [ ] Performance is acceptable
- [ ] Logs are informative
- [ ] User documentation is helpful

---

_This skill serves as the comprehensive resource for Claude Code plugin development, providing guidance from initial concept through deployment and maintenance. For specific implementation details, refer to the reference materials in the references/ directory._
