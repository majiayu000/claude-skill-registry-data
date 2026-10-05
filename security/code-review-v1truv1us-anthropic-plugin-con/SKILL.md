---
name: code-review
description: Automated code review assistance with AI-powered analysis, security scanning, performance analysis, and best practices enforcement.
license: MIT
---

# Automated Code Review Assistant

## Overview

Comprehensive code review system providing AI-powered analysis, automated security scanning, performance analysis, and best practices enforcement to improve code quality and development efficiency.

## Quick Start

### Installation
```bash
npm install -g @code-review/cli
# or
npx @code-review/cli init
```

### Initial Code Review
```bash
# Review current changes
code-review review

# Review specific branch
code-review review --branch=feature/user-auth

# Review with custom rules
code-review review --rules=security,performance,maintainability
```

## Review Configuration

### Setup Review Rules
```bash
# Initialize review configuration
code-review init --template=javascript

# Add custom rules
code-review rules add --name=no-console-log --pattern=console\.log --severity=warning

# Configure review thresholds
code-review config set --complexity.max=10 --coverage.min=80
```

**Review Configuration File**
```javascript
// .code-review/config.js
module.exports = {
  languages: ['javascript', 'typescript', 'python', 'java'],
  
  rules: {
    security: {
      enabled: true,
      rules: [
        'sql-injection',
        'xss-vulnerability',
        'hardcoded-secrets',
        'insecure-random',
        'path-traversal'
      ],
      severity: 'error'
    },
    
    performance: {
      enabled: true,
      rules: [
        'inefficient-loops',
        'memory-leaks',
        'unnecessary-computation',
        'blocking-operations'
      ],
      severity: 'warning'
    },
    
    maintainability: {
      enabled: true,
      rules: [
        'complex-function',
        'long-method',
        'duplicate-code',
        'magic-numbers',
        'deep-nesting'
      ],
      severity: 'info'
    },
    
    style: {
      enabled: true,
      rules: [
        'consistent-naming',
        'proper-formatting',
        'missing-comments',
        'unused-variables'
      ],
      severity: 'warning'
    }
  },
  
  thresholds: {
    complexity: {
      maximum: 10,
      veryHigh: 20
    },
    coverage: {
      minimum: 80,
      target: 90
    },
    duplication: {
      maximum: 5, // percentage
      tokens: 50
    },
    fileLength: {
      maximum: 500,
      veryHigh: 1000
    }
  },
  
  ai: {
    enabled: true,
    model: 'gpt-4',
    temperature: 0.3,
    maxTokens: 2000,
    focus: ['security', 'performance', 'maintainability']
  }
};
```

## Automated Analysis

### Security Analysis
```bash
# Run security-focused review
code-review security --scan-all

# Check for specific vulnerabilities
code-review security --check=sql-injection,xss,hardcoded-secrets

# Generate security report
code-review security --report --format=html
```

**Security Rules Configuration**
```javascript
// .code-review/security.js
module.exports = {
  rules: {
    'sql-injection': {
      pattern: [
        /query\s*\(\s*['"`][^'"`]*\+.*['"`]/,
        /execute\s*\(\s*['"`][^'"`]*\+.*['"`]/
      ],
      message: 'Potential SQL injection vulnerability. Use parameterized queries.',
      severity: 'error',
      suggestion: 'Use prepared statements or ORM methods'
    },
    
    'xss-vulnerability': {
      pattern: [
        /innerHTML\s*=\s*.*[^)]/,
        /document\.write\s*\([^)]*\+/
      ],
      message: 'Potential XSS vulnerability. Sanitize user input.',
      severity: 'error',
      suggestion: 'Use textContent or sanitize HTML with DOMPurify'
    },
    
    'hardcoded-secrets': {
      pattern: [
        /password\s*=\s*['"`][^'"`]{8,}['"`]/,
        /api[_-]?key\s*=\s*['"`][^'"`]{16,}['"`]/,
        /secret\s*=\s*['"`][^'"`]{16,}['"`]/
      ],
      message: 'Hardcoded secret detected. Use environment variables.',
      severity: 'error',
      suggestion: 'Move secrets to environment variables or secret manager'
    },
    
    'insecure-random': {
      pattern: /Math\.random\(\)/,
      message: 'Insecure random number generation. Use crypto.randomBytes().',
      severity: 'warning',
      suggestion: 'Use crypto.randomBytes() for security-sensitive operations'
    }
  },
  
  customRules: [
    {
      name: 'no-debug-in-production',
      pattern: /console\.(log|debug|warn)/,
      exclude: ['test/', 'spec/', 'dev/'],
      message: 'Debug statements should not be in production code.',
      severity: 'warning'
    }
  ]
};
```

### Performance Analysis
```bash
# Analyze performance issues
code-review performance --analyze-all

# Check specific performance patterns
code-review performance --check=loops,memory,async

# Generate performance report
code-review performance --report --include-suggestions
```

**Performance Rules Configuration**
```javascript
// .code-review/performance.js
module.exports = {
  rules: {
    'inefficient-loops': {
      patterns: [
        {
          pattern: /for\s*\(\s*let\s+\w+\s*=\s*0\s*;\s*\w+\s*<\s*.*\.length\s*;\s*\w+\+\+\s*\)\s*{[\s\S]*?\.push\(/,
          message: 'Inefficient array growth in loop. Pre-allocate array size.',
          suggestion: 'Pre-allocate array or use array methods like map()'
        },
        {
          pattern: /while\s*\([^)]*\.length\s*>\s*\d+\)/,
          message: 'Repeated length calculation in loop condition.',
          suggestion: 'Cache array length before loop'
        }
      ],
      severity: 'warning'
    },
    
    'memory-leaks': {
      patterns: [
        {
          pattern: /setInterval\s*\([^,]+,\s*\d+\)/,
          message: 'setInterval without cleanup. Potential memory leak.',
          suggestion: 'Store interval ID and clear on component unmount'
        },
        {
          pattern: /addEventListener\s*\([^)]+\)/,
          message: 'Event listener without removal. Potential memory leak.',
          suggestion: 'Remove event listeners when no longer needed'
        }
      ],
      severity: 'warning'
    },
    
    'blocking-operations': {
      patterns: [
        {
          pattern: /fs\.readFileSync\s*\(/,
          message: 'Synchronous file I/O blocks event loop.',
          suggestion: 'Use fs.readFile() with callback or promises'
        },
        {
          pattern: /require\s*\(\s*['"`][^'"`]*\.json['"`]\s*\)/,
          message: 'Synchronous JSON parsing in require().',
          suggestion: 'Use fs.readFile() with JSON.parse() for large files'
        }
      ],
      severity: 'warning'
    }
  },
  
  metrics: {
    complexity: {
      enabled: true,
      threshold: 10
    },
    maintainability: {
      enabled: true,
      threshold: 70
    },
    technicalDebt: {
      enabled: true,
      threshold: 5 // hours
    }
  }
};
```

### Code Quality Analysis
```bash
# Analyze code quality
code-review quality --comprehensive

# Check maintainability
code-review quality --maintainability --threshold=70

# Generate quality dashboard
code-review quality --dashboard --output=./quality-report
```

**Quality Metrics Configuration**
```javascript
// .code-review/quality.js
module.exports = {
  metrics: {
    complexity: {
      enabled: true,
      algorithm: 'cyclomatic',
      threshold: {
        good: 5,
        moderate: 10,
        high: 20
      }
    },
    
    maintainability: {
      enabled: true,
      factors: [
        'complexity',
        'size',
        'duplication',
        'testing'
      ],
      threshold: {
        excellent: 85,
        good: 70,
        moderate: 50
      }
    },
    
    duplication: {
      enabled: true,
      minTokens: 50,
      ignoreAnnotations: true,
      threshold: 5 // percentage
    },
    
    testing: {
      enabled: true,
      coverage: {
        minimum: 80,
        target: 90
      },
      testTypes: ['unit', 'integration', 'e2e']
    }
  },
  
  smells: [
    {
      name: 'long-method',
      threshold: 50, // lines
      severity: 'warning'
    },
    {
      name: 'large-class',
      threshold: 300, // lines
      severity: 'warning'
    },
    {
      name: 'too-many-parameters',
      threshold: 5,
      severity: 'info'
    },
    {
      name: 'deep-nesting',
      threshold: 4,
      severity: 'warning'
    }
  ]
};
```

## AI-Powered Review

### Intelligent Code Analysis
```bash
# Run AI review
code-review ai --focus=security,performance

# Get AI suggestions
code-review ai suggest --file=src/auth.js

# AI code explanation
code-review ai explain --file=src/complex-algorithm.js --line=45
```

**AI Review Configuration**
```javascript
// .code-review/ai.js
module.exports = {
  provider: 'openai', // or 'anthropic', 'local'
  
  model: {
    name: 'gpt-4',
    temperature: 0.3,
    maxTokens: 2000,
    timeout: 30000
  },
  
  prompts: {
    codeReview: `
You are an expert code reviewer. Analyze the following code for:
1. Security vulnerabilities
2. Performance issues
3. Code quality and maintainability
4. Best practices adherence

Provide specific, actionable feedback with line numbers when applicable.

Code:
{code}
    `,
    
    securityReview: `
Focus specifically on security issues in this code:
- Input validation
- Authentication/authorization
- Data exposure
- Injection vulnerabilities
- Cryptographic issues

Code:
{code}
    `,
    
    performanceReview: `
Analyze this code for performance issues:
- Algorithmic complexity
- Memory usage
- I/O operations
- Caching opportunities
- Bottlenecks

Code:
{code}
    `
  },
  
  focus: {
    security: {
      enabled: true,
      weight: 0.4
    },
    performance: {
      enabled: true,
      weight: 0.3
    },
    maintainability: {
      enabled: true,
      weight: 0.2
    },
    style: {
      enabled: true,
      weight: 0.1
    }
  },
  
  output: {
    format: 'structured', // or 'plain', 'markdown'
    includeSuggestions: true,
    includeExamples: true,
    maxSuggestions: 10
  }
};
```

### AI Suggestions
```javascript
const { AIReviewer } = require('@code-review/ai');

const aiReviewer = new AIReviewer({
  model: 'gpt-4',
  focus: ['security', 'performance']
});

// Get AI suggestions for specific code
const suggestions = await aiReviewer.suggest({
  code: `
function authenticateUser(username, password) {
  const query = \`SELECT * FROM users WHERE username = '\${username}' AND password = '\${password}'\`;
  return db.query(query);
}
  `,
  context: {
    file: 'src/auth.js',
    language: 'javascript',
    framework: 'express'
  }
});

console.log(suggestions);
/*
Output:
[
  {
    type: 'security',
    severity: 'error',
    line: 2,
    message: 'SQL injection vulnerability',
    suggestion: 'Use parameterized queries',
    example: `
const query = 'SELECT * FROM users WHERE username = ? AND password = ?';
return db.query(query, [username, password]);
    `
  }
]
*/
```

## Integration with Development Workflow

### Git Integration
```bash
# Install git hooks
code-review git install-hooks

# Pre-commit review
code-review git pre-commit

# Pre-push review
code-review git pre-push

# Review specific commit
code-review git review --commit=abc123
```

**Git Hooks Configuration**
```javascript
// .code-review/git-hooks.js
module.exports = {
  hooks: {
    'pre-commit': {
      enabled: true,
      commands: [
        'code-review security --staged',
        'code-review quality --staged',
        'code-review test --staged'
      ],
      failOnError: true
    },
    
    'pre-push': {
      enabled: true,
      commands: [
        'code-review review --branch=HEAD',
        'code-review performance --full-scan'
      ],
      failOnError: false
    },
    
    'commit-msg': {
      enabled: true,
      pattern: /^(feat|fix|docs|style|refactor|test|chore)(\(.+\))?: .{1,50}$/,
      message: 'Commit message must follow conventional commit format'
    }
  },
  
  ignore: {
    files: [
      '*.min.js',
      'dist/**',
      'node_modules/**',
      '*.test.js',
      '*.spec.js'
    ],
    patterns: [
      'debugger;',
      'console.log('
    ]
  }
};
```

### CI/CD Integration
```yaml
# .github/workflows/code-review.yml
name: Code Review

on: [pull_request]

jobs:
  code-review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Setup Code Review
        run: |
          npm install -g @code-review/cli
          code-review init --ci
      
      - name: Security Review
        run: |
          code-review security --format=github --output=security-review.json
      
      - name: Performance Review
        run: |
          code-review performance --format=github --output=performance-review.json
      
      - name: AI Review
        run: |
          code-review ai --focus=security,performance --format=github --output=ai-review.json
      
      - name: Comment PR
        uses: actions/github-script@v6
        with:
          script: |
            const fs = require('fs');
            
            const securityReview = JSON.parse(fs.readFileSync('security-review.json'));
            const performanceReview = JSON.parse(fs.readFileSync('performance-review.json'));
            const aiReview = JSON.parse(fs.readFileSync('ai-review.json'));
            
            const comment = `
## 🤖 Automated Code Review
            
### 🔒 Security Issues
${securityReview.issues.map(issue => `- **${issue.severity}**: ${issue.message} (Line ${issue.line})`).join('\n')}
            
### ⚡ Performance Issues
${performanceReview.issues.map(issue => `- **${issue.severity}**: ${issue.message} (Line ${issue.line})`).join('\n')}
            
### 🧠 AI Suggestions
${aiReview.suggestions.map(suggestion => `- **${suggestion.type}**: ${suggestion.message}`).join('\n')}
            `;
            
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: comment
            });
```

### IDE Integration
```bash
# VS Code extension
code --install-extension code-review.vscode

# JetBrains plugin
# Install from marketplace: Code Review Assistant

# Vim/Neovim plugin
git clone https://github.com/code-review/vim-plugin ~/.vim/pack/code-review/start/
```

**VS Code Extension Configuration**
```json
{
  "code-review.autoReview": true,
  "code-review.focus": ["security", "performance"],
  "code-review.severity": ["error", "warning"],
  "code-review.realTime": true,
  "code-review.showSuggestions": true,
  "code-review.aiEnabled": true,
  "code-review.customRules": "./.code-review/custom-rules.js"
}
```

## Reporting & Analytics

### Review Reports
```bash
# Generate comprehensive report
code-review report --comprehensive --format=html

# Weekly review summary
code-review report --period=week --format=markdown

# Team performance report
code-review report --team --metrics=quality,velocity
```

**Report Configuration**
```javascript
// .code-review/reports.js
module.exports = {
  templates: {
    comprehensive: {
      sections: [
        'executive-summary',
        'security-analysis',
        'performance-analysis',
        'quality-metrics',
        'trends',
        'recommendations'
      ],
      format: 'html',
      includeCharts: true
    },
    
    weekly: {
      sections: [
        'summary',
        'key-metrics',
        'issues-found',
        'improvements'
      ],
      format: 'markdown',
      includeCharts: false
    }
  },
  
  metrics: {
    security: {
      vulnerabilities: ['critical', 'high', 'medium', 'low'],
      trends: true,
      byFile: true
    },
    
    performance: {
      issues: ['critical', 'warning'],
      improvements: true,
      byComplexity: true
    },
    
    quality: {
      maintainability: true,
      technicalDebt: true,
      coverage: true
    },
    
    team: {
      reviewVelocity: true,
      issueResolution: true,
      codeQuality: true
    }
  },
  
  charts: {
    types: ['line', 'bar', 'pie', 'heatmap'],
    interactive: true,
    exportable: true
  }
};
```

### Analytics Dashboard
```javascript
const { ReviewAnalytics } = require('@code-review/analytics');

const analytics = new ReviewAnalytics({
  dataSource: './code-review-data.json',
  timeRange: '30d'
});

// Generate quality trends
const qualityTrends = await analytics.getQualityTrends();
console.log(`
Quality Trends (Last 30 Days):
- Maintainability: ${qualityTrends.maintainability.trend}%
- Security Score: ${qualityTrends.security.trend}%
- Performance Score: ${qualityTrends.performance.trend}%
`);

// Team performance
const teamPerformance = await analytics.getTeamPerformance();
console.log(`
Team Performance:
- Average Review Time: ${teamPerformance.avgReviewTime} minutes
- Issues Found per Review: ${teamPerformance.avgIssuesFound}
- Resolution Rate: ${teamPerformance.resolutionRate}%
`);
```

## Custom Rules & Extensions

### Custom Rule Development
```javascript
// .code-review/custom-rules.js
const { Rule } = require('@code-review/rules');

class NoHardcodedUrlsRule extends Rule {
  constructor() {
    super({
      name: 'no-hardcoded-urls',
      description: 'Detect hardcoded URLs in code',
      severity: 'warning'
    });
  }

  check(file, content) {
    const issues = [];
    const lines = content.split('\n');
    
    lines.forEach((line, index) => {
      const urlPattern = /https?:\/\/[^\s"'`]+/g;
      const matches = line.match(urlPattern);
      
      if (matches) {
        matches.forEach(url => {
          if (!this.isAllowedUrl(url)) {
            issues.push({
              line: index + 1,
              column: line.indexOf(url) + 1,
              message: `Hardcoded URL detected: ${url}`,
              suggestion: 'Move URL to environment variables or config file'
            });
          }
        });
      }
    });
    
    return issues;
  }
  
  isAllowedUrl(url) {
    const allowed = [
      'localhost',
      '127.0.0.1',
      'example.com'
    ];
    
    return allowed.some(domain => url.includes(domain));
  }
}

module.exports = NoHardcodedUrlsRule;
```

### Rule Testing
```javascript
// test/custom-rules.test.js
const { NoHardcodedUrlsRule } = require('../.code-review/custom-rules');

describe('NoHardcodedUrlsRule', () => {
  let rule;
  
  beforeEach(() => {
    rule = new NoHardcodedUrlsRule();
  });

  test('should detect hardcoded URLs', () => {
    const content = `
      const apiUrl = 'https://api.example.com/users';
      fetch(apiUrl);
    `;
    
    const issues = rule.check('test.js', content);
    expect(issues).toHaveLength(1);
    expect(issues[0].message).toContain('Hardcoded URL detected');
  });

  test('should ignore localhost URLs', () => {
    const content = `
      const localUrl = 'http://localhost:3000/api';
      fetch(localUrl);
    `;
    
    const issues = rule.check('test.js', content);
    expect(issues).toHaveLength(0);
  });
});
```

## API Reference

### Core Classes

**CodeReviewer**
```javascript
const { CodeReviewer } = require('@code-review/core');

const reviewer = new CodeReviewer({
  rules: ['security', 'performance', 'quality'],
  ai: { enabled: true, model: 'gpt-4' }
});

const results = await reviewer.review('./src');
```

**RuleEngine**
```javascript
const { RuleEngine } = require('@code-review/rules');

const engine = new RuleEngine();
engine.addRule(new NoHardcodedUrlsRule());
const issues = engine.checkFile('test.js', content);
```

**AIReviewer**
```javascript
const { AIReviewer } = require('@code-review/ai');

const aiReviewer = new AIReviewer({
  model: 'gpt-4',
  focus: ['security', 'performance']
});

const suggestions = await aiReviewer.analyze(code);
```

## Contributing

1. Fork repository
2. Create feature branch
3. Add comprehensive tests
4. Follow code review guidelines
5. Submit pull request

## License

MIT License - see LICENSE file for details.