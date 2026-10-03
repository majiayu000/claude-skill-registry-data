---
memory_layer: durable_knowledge
para_section: pages/skills/file-naming-standards
gigabrain_tags: file-naming, standards, organization, consistency, development-practices, naming, files, documentation
openstinger_context: file-organization-standards, naming-conventions
last_updated: 2026-03-30
related_docs:
  - docs_construct_ai/codebase/coding-standards/
  - docs_construct_ai/codebase/architecture/
related_skills:
  - agent-coding-standards
  - agent-development-standards
  - writing-plans
frequency_percent: 98.0
success_rate_percent: 96.0
---

# File Naming Standards

## Overview

**Core principle:** Follow Construct AI file naming conventions for consistent organization, discoverability, and maintainability across the entire codebase.

**Standards:** Lowercase, underscores, descriptive names, numeric prefixes, consistent extensions.

## When to Use This Skill

**Trigger Conditions:**
- When creating any new file in the Construct AI repository
- Before committing files to ensure naming compliance
- When organizing project structure and directories
- During code reviews to verify naming consistency
- When refactoring or renaming existing files
- When setting up new development environments
- When documenting file organization patterns

**Mandatory Application:**
- Required for all file creation in Construct AI repositories
- Must be verified before any commit or merge
- Required for both new files and file renames
- Must be followed by all team members
- Required for maintaining repository consistency

## Step-by-Step Procedure

### Step 1: Understand Core Naming Principles
**Master the fundamental rules that apply to all files:**

```javascript
// Core naming principles validation
const namingPrinciples = {
  lowercase: true,        // All filenames must be lowercase
  underscores: true,      // Use underscores for word separation
  descriptive: true,      // Names must clearly indicate content
  consistent: true,       // Follow established directory patterns
  sequential: true,       // Use numeric prefixes for ordering
  noEmojis: true         // No emoji characters allowed
};

// File extension standards
const validExtensions = {
  documentation: ['.md'],
  javascript: ['.js', '.mjs', '.cjs'],
  json: ['.json'],
  database: ['.sql'],
  text: ['.txt'],
  images: ['.png', '.jpg', '.jpeg', '.svg', '.webp'],
  configuration: ['.json', '.js', '.yaml', '.yml']
};

// Validate filename against principles
function validateFilename(filename) {
  const errors = [];
  
  // Check lowercase
  if (filename !== filename.toLowerCase()) {
    errors.push('Filename must be all lowercase');
  }
  
  // Check for spaces or hyphens (should use underscores)
  if (filename.includes(' ') || filename.includes('-')) {
    errors.push('Use underscores instead of spaces or hyphens');
  }
  
  // Check for emojis
  const emojiRegex = /[\u{1F600}-\u{1F64F}]|[\u{1F300}-\u{1F5FF}]|[\u{1F680}-\u{1F6FF}]|[\u{1F1E0}-\u{1F1FF}]/u;
  if (emojiRegex.test(filename)) {
    errors.push('No emoji characters allowed in filenames');
  }
  
  return {
    valid: errors.length === 0,
    errors: errors
  };
}
```

**Core Principles:**
- All filenames must be lowercase
- Use underscores for word separation (never spaces or hyphens)
- Names must be descriptive and indicate content clearly
- Follow established patterns within each directory
- Use numeric prefixes for logical ordering
- No emoji characters in any filenames

### Step 2: Apply Directory-Specific Conventions
**Follow the correct naming pattern for each directory type:**

```javascript
// Directory-specific naming patterns
const directoryPatterns = {
  // Documentation files
  'docs/': '{category}/{prefix}_{descriptive_name}.md',
  'docs/standards/': '0000_{UPPER_CASE_DESCRIPTION}.md',
  'docs/procedures/': '0000_{UPPER_CASE_PROCEDURE_NAME}.md',
  'docs/pages-agents/': '{page_id}_AGENT_{agent_name}_{purpose}.md',
  'docs/error-tracking/': '{page_id}_{agent_id}_{error_type}.md',
  
  // Source code files
  'client/src/': '{camelCase}.js',
  'server/src/': '{camelCase}.js',
  'client/src/components/': '{PascalCase}.js',
  'server/src/routes/': '{camelCase}Routes.js',
  
  // Database files
  'server/sql/': '{operation}_{table}_{description}.sql',
  
  // Configuration files (root)
  './': '.env{environment}',
  
  // Test files
  'tests/': '{describe}_{it}.test.js',
  'tests/': 'test_{functionality}.js'
};

// Apply correct pattern for directory
function getCorrectFilename(directory, purpose, context = {}) {
  const pattern = directoryPatterns[directory];
  if (!pattern) {
    throw new Error(`No naming pattern defined for directory: ${directory}`);
  }
  
  // Apply pattern with context
  return pattern
    .replace('{category}', context.category || 'general')
    .replace('{prefix}', context.prefix || '0000')
    .replace('{descriptive_name}', purpose.toLowerCase().replace(/\s+/g, '_'))
    .replace('{UPPER_CASE_DESCRIPTION}', purpose.toUpperCase().replace(/\s+/g, '_'))
    .replace('{UPPER_CASE_PROCEDURE_NAME}', purpose.toUpperCase().replace(/\s+/g, '_'))
    .replace('{page_id}', context.pageId || '0000')
    .replace('{agent_name}', context.agentName || 'unknown')
    .replace('{purpose}', context.purpose || 'procedure')
    .replace('{agent_id}', context.agentId || 'unknown')
    .replace('{error_type}', context.errorType || 'errors')
    .replace('{camelCase}', toCamelCase(purpose))
    .replace('{PascalCase}', toPascalCase(purpose))
    .replace('{operation}', context.operation || 'create')
    .replace('{table}', context.table || 'table')
    .replace('{description}', purpose.toLowerCase().replace(/\s+/g, '_'))
    .replace('{environment}', context.environment || '')
    .replace('{describe}', context.describe || 'describe')
    .replace('{it}', context.it || 'it')
    .replace('{functionality}', purpose.toLowerCase().replace(/\s+/g, '_'));
}

// Helper functions for case conversion
function toCamelCase(str) {
  return str
    .toLowerCase()
    .replace(/[^a-zA-Z0-9]+(.)/g, (match, chr) => chr.toUpperCase());
}

function toPascalCase(str) {
  const camel = toCamelCase(str);
  return camel.charAt(0).toUpperCase() + camel.slice(1);
}
```

**Directory Patterns:**
- Documentation: `{prefix}_{descriptive_name}.md`
- JavaScript: `{camelCase}.js`
- React components: `{PascalCase}.js`
- Database: `{operation}_{table}_{description}.sql`
- Tests: Descriptive names with test indicators

### Step 3: Implement Numeric Prefixing System
**Apply the standardized numeric prefix system for ordering:**

```javascript
// Numeric prefix ranges and their purposes
const prefixRanges = {
  '0000-0999': 'Master guides and foundational documents',
  '1000-1999': 'Agent-specific documentation',
  '2000-2999': 'Workflow and process documentation',
  '3000-3999': 'Technical implementation guides',
  '4000-4999': 'Reserved for future use',
  '5000-5999': 'Database and migration documentation',
  '6000-6999': 'Testing and quality assurance',
  '7000-7999': 'Deployment and operations',
  '8000-8999': 'Feature-specific documentation',
  '9000-9999': 'Legacy and archived documentation'
};

// Determine appropriate prefix for content type
function getAppropriatePrefix(contentType, category) {
  const prefixMap = {
    'master_guide': '0000',
    'standards': '0000',
    'procedures': '0000',
    'agent_docs': '1000',
    'workflow_docs': '2000',
    'implementation': '3000',
    'database': '5000',
    'testing': '6000',
    'deployment': '7000',
    'features': '8000',
    'legacy': '9000'
  };
  
  const basePrefix = prefixMap[contentType] || '0000';
  
  // Add sequential numbering within category
  const sequentialNumber = getNextSequentialNumber(category, basePrefix);
  
  return basePrefix.slice(0, -sequentialNumber.toString().length) + sequentialNumber;
}

// Get next sequential number for category
function getNextSequentialNumber(category, basePrefix) {
  // This would check existing files in category to determine next number
  // For now, return a default
  return 1;
}

// Validate prefix is within correct range
function validatePrefixRange(prefix, contentType) {
  const rangeMap = {
    'master_guide': '0000-0999',
    'standards': '0000-0999',
    'procedures': '0000-0999',
    'agent_docs': '1000-1999',
    'workflow_docs': '2000-2999',
    'implementation': '3000-3999',
    'database': '5000-5999',
    'testing': '6000-6999',
    'deployment': '7000-7999',
    'features': '8000-8999',
    'legacy': '9000-9999'
  };
  
  const expectedRange = rangeMap[contentType];
  if (!expectedRange) return true; // No specific range defined
  
  const [min, max] = expectedRange.split('-').map(n => parseInt(n));
  const prefixNum = parseInt(prefix);
  
  return prefixNum >= min && prefixNum <= max;
}
```

**Prefixing System:**
- 0000-0999: Master guides and foundational documents
- 1000-1999: Agent-specific documentation
- 2000-2999: Workflow and process documentation
- 3000-3999: Technical implementation guides
- 5000-5999: Database and migration documentation
- 6000-6999: Testing and quality assurance
- 7000-7999: Deployment and operations
- 8000-8999: Feature-specific documentation
- 9000-9999: Legacy and archived documentation

### Step 4: Validate File Extensions
**Ensure correct file extensions are used:**

```javascript
// File extension validation
const extensionRules = {
  // Documentation
  '.md': { type: 'documentation', required: true },
  '.MD': { type: 'documentation', required: false, error: 'Use lowercase .md' },
  
  // JavaScript
  '.js': { type: 'javascript', required: true },
  '.mjs': { type: 'javascript_module', required: false },
  '.cjs': { type: 'javascript_commonjs', required: false },
  
  // Data formats
  '.json': { type: 'json', required: true },
  '.sql': { type: 'database', required: true },
  '.txt': { type: 'text', required: true },
  
  // Images
  '.png': { type: 'image', required: true },
  '.jpg': { type: 'image', required: true },
  '.jpeg': { type: 'image', required: true },
  '.svg': { type: 'image', required: true },
  '.webp': { type: 'image', required: true },
  
  // Configuration
  '.yaml': { type: 'configuration', required: false },
  '.yml': { type: 'configuration', required: false },
  
  // Invalid extensions
  '.MD': { type: 'invalid', error: 'Use lowercase .md extension' },
  '.JS': { type: 'invalid', error: 'Use lowercase .js extension' },
  '.JSON': { type: 'invalid', error: 'Use lowercase .json extension' }
};

// Validate file extension
function validateFileExtension(filename) {
  const extension = filename.substring(filename.lastIndexOf('.'));
  const rule = extensionRules[extension];
  
  if (!rule) {
    return {
      valid: false,
      error: `Unknown file extension: ${extension}`
    };
  }
  
  if (rule.type === 'invalid') {
    return {
      valid: false,
      error: rule.error
    };
  }
  
  return {
    valid: true,
    type: rule.type,
    required: rule.required
  };
}

// Get recommended extension for file type
function getRecommendedExtension(fileType, context = {}) {
  const recommendations = {
    documentation: '.md',
    javascript: '.js',
    javascript_module: context.esm ? '.mjs' : '.js',
    json: '.json',
    database: '.sql',
    text: '.txt',
    image_png: '.png',
    image_svg: '.svg',
    configuration: '.json'
  };
  
  return recommendations[fileType] || '.txt';
}
```

**Extension Standards:**
- Documentation: `.md` (lowercase)
- JavaScript: `.js`, `.mjs`, `.cjs`
- Data: `.json`, `.sql`, `.txt`
- Images: `.png`, `.jpg`, `.svg`, `.webp`
- All extensions must be lowercase

### Step 5: Generate Correct Filenames
**Create properly named files for any given purpose:**

```javascript
// Complete filename generation system
function generateCorrectFilename(directory, purpose, context = {}) {
  // Step 1: Determine content type and category
  const contentType = determineContentType(directory, purpose);
  const category = determineCategory(directory, context);
  
  // Step 2: Get appropriate prefix
  const prefix = getAppropriatePrefix(contentType, category);
  
  // Step 3: Generate base name
  const baseName = generateBaseName(purpose, contentType, context);
  
  // Step 4: Get correct extension
  const extension = getRecommendedExtension(contentType, context);
  
  // Step 5: Combine all parts
  const fullName = `${prefix}_${baseName}${extension}`;
  
  // Step 6: Final validation
  const validation = validateCompleteFilename(fullName, directory);
  
  return {
    filename: fullName,
    valid: validation.valid,
    errors: validation.errors,
    suggestions: validation.suggestions
  };
}

// Determine content type from directory and purpose
function determineContentType(directory, purpose) {
  if (directory.includes('docs/standards')) return 'standards';
  if (directory.includes('docs/procedures')) return 'procedures';
  if (directory.includes('docs/pages-agents')) return 'agent_docs';
  if (directory.includes('server/sql')) return 'database';
  if (directory.includes('tests')) return 'testing';
  if (purpose.toLowerCase().includes('test')) return 'testing';
  if (purpose.toLowerCase().includes('migration')) return 'database';
  return 'documentation';
}

// Generate descriptive base name
function generateBaseName(purpose, contentType, context) {
  let baseName = purpose
    .toLowerCase()
    .replace(/[^a-z0-9\s]/g, '') // Remove special characters
    .replace(/\s+/g, '_') // Replace spaces with underscores
    .replace(/_+/g, '_') // Remove multiple underscores
    .replace(/^_|_$/g, ''); // Remove leading/trailing underscores
  
  // Add context-specific elements
  if (contentType === 'agent_docs' && context.agentName) {
    baseName = `agent_${context.agentName}_${baseName}`;
  }
  
  if (contentType === 'database' && context.table) {
    baseName = `${context.operation}_${context.table}_${baseName}`;
  }
  
  return baseName;
}

// Validate complete filename
function validateCompleteFilename(filename, directory) {
  const errors = [];
  const suggestions = [];
  
  // Check overall filename validation
  const nameValidation = validateFilename(filename);
  if (!nameValidation.valid) {
    errors.push(...nameValidation.errors);
  }
  
  // Check extension validation
  const extensionValidation = validateFileExtension(filename);
  if (!extensionValidation.valid) {
    errors.push(extensionValidation.error);
  }
  
  // Check directory-specific rules
  const directoryValidation = validateDirectoryRules(filename, directory);
  if (!directoryValidation.valid) {
    errors.push(...directoryValidation.errors);
    suggestions.push(...directoryValidation.suggestions);
  }
  
  return {
    valid: errors.length === 0,
    errors: errors,
    suggestions: suggestions
  };
}
```

**Filename Generation:**
- Determine content type from directory and purpose
- Apply appropriate numeric prefix
- Generate descriptive base name
- Add correct file extension
- Validate against all standards

### Step 6: Handle File Renames and Moves
**Properly rename existing files to follow standards:**

```javascript
// File rename handling
function planFileRename(currentPath, newPurpose = null, newDirectory = null) {
  const currentFile = path.basename(currentPath);
  const currentDir = path.dirname(currentPath);
  
  const targetDir = newDirectory || currentDir;
  const purpose = newPurpose || inferPurposeFromFilename(currentFile);
  
  // Generate correct filename
  const result = generateCorrectFilename(targetDir, purpose, {});
  
  if (!result.valid) {
    throw new Error(`Cannot generate valid filename: ${result.errors.join(', ')}`);
  }
  
  const newPath = path.join(targetDir, result.filename);
  
  return {
    currentPath: currentPath,
    newPath: newPath,
    renameNeeded: currentPath !== newPath,
    validation: result
  };
}

// Find all references to renamed file
function findFileReferences(filePath, projectRoot) {
  const references = [];
  const filename = path.basename(filePath);
  
  // Search for imports, requires, links, etc.
  const searchPatterns = [
    `import.*${filename}`,
    `require.*${filename}`,
    `from.*${filename}`,
    `\\[.*${filename}.*\\]`, // Markdown links
    `href.*${filename}`,
    `src.*${filename}`
  ];
  
  // This would implement actual file searching
  // For now, return placeholder
  return references;
}

// Execute safe file rename
async function executeSafeRename(renamePlan) {
  const { currentPath, newPath } = renamePlan;
  
  // Step 1: Find all references
  const references = findFileReferences(currentPath, process.cwd());
  
  // Step 2: Create backup
  const backupPath = `${currentPath}.backup`;
  await fs.copyFile(currentPath, backupPath);
  
  // Step 3: Rename file
  await fs.rename(currentPath, newPath);
  
  // Step 4: Update all references
  for (const ref of references) {
    await updateFileReference(ref, currentPath, newPath);
  }
  
  // Step 5: Verify rename success
  const newExists = await fs.access(newPath).then(() => true).catch(() => false);
  const oldExists = await fs.access(currentPath).then(() => true).catch(() => false);
  
  if (newExists && !oldExists) {
    // Clean up backup
    await fs.unlink(backupPath);
    return { success: true, referencesUpdated: references.length };
  } else {
    // Restore from backup
    await fs.rename(backupPath, currentPath);
    throw new Error('File rename failed, restored from backup');
  }
}
```

**File Rename Process:**
- Generate correct new filename
- Find all references to current file
- Create backup before rename
- Update all references after rename
- Verify rename success and clean up

### Step 7: Implement Validation Automation
**Set up automated checking for naming compliance:**

```javascript
// Automated validation system
class FileNamingValidator {
  constructor(projectRoot) {
    this.projectRoot = projectRoot;
    this.violations = [];
    this.validFiles = [];
  }
  
  async validateProject() {
    const allFiles = await this.getAllProjectFiles();
    
    for (const file of allFiles) {
      const relativePath = path.relative(this.projectRoot, file);
      const validation = await this.validateFile(relativePath);
      
      if (validation.valid) {
        this.validFiles.push(relativePath);
      } else {
        this.violations.push({
          file: relativePath,
          errors: validation.errors,
          suggestions: validation.suggestions
        });
      }
    }
    
    return {
      totalFiles: allFiles.length,
      validFiles: this.validFiles.length,
      violations: this.violations.length,
      violationDetails: this.violations
    };
  }
  
  async validateFile(relativePath) {
    const directory = path.dirname(relativePath);
    const filename = path.basename(relativePath);
    
    // Skip validation for certain directories
    if (this.shouldSkipDirectory(directory)) {
      return { valid: true, errors: [], suggestions: [] };
    }
    
    const errors = [];
    const suggestions = [];
    
    // Check filename validation
    const nameValidation = validateFilename(filename);
    if (!nameValidation.valid) {
      errors.push(...nameValidation.errors);
    }
    
    // Check extension validation
    const extValidation = validateFileExtension(filename);
    if (!extValidation.valid) {
      errors.push(extValidation.error);
    }
    
    // Check directory-specific rules
    const dirValidation = validateDirectoryRules(filename, directory);
    if (!dirValidation.valid) {
      errors.push(...dirValidation.errors);
      suggestions.push(...dirValidation.suggestions);
    }
    
    // Generate suggestions for fixes
    if (errors.length > 0) {
      const suggestion = generateCorrectFilename(directory, 
        inferPurposeFromFilename(filename));
      if (suggestion.valid) {
        suggestions.push(`Rename to: ${suggestion.filename}`);
      }
    }
    
    return {
      valid: errors.length === 0,
      errors: errors,
      suggestions: suggestions
    };
  }
  
  shouldSkipDirectory(directory) {
    const skipDirs = [
      'node_modules',
      '.git',
      'dist',
      'build',
      'coverage',
      '.next',
      '.nuxt'
    ];
    
    return skipDirs.some(skipDir => directory.includes(skipDir));
  }
  
  async getAllProjectFiles() {
    const files = [];
    
    async function scanDir(dir) {
      const entries = await fs.readdir(dir, { withFileTypes: true });
      
      for (const entry of entries) {
        const fullPath = path.join(dir, entry.name);
        
        if (entry.isDirectory()) {
          await scanDir(fullPath);
        } else if (entry.isFile()) {
          files.push(fullPath);
        }
      }
    }
    
    await scanDir(this.projectRoot);
    return files;
  }
}

// Usage
const validator = new FileNamingValidator('/path/to/project');
const results = await validator.validateProject();

console.log(`Validated ${results.totalFiles} files:`);
console.log(`✅ ${results.validFiles} valid files`);
console.log(`❌ ${results.violations} violations found`);

if (results.violations > 0) {
  console.log('\nViolations:');
  results.violationDetails.forEach(v => {
    console.log(`  ${v.file}:`);
    v.errors.forEach(error => console.log(`    ❌ ${error}`));
    v.suggestions.forEach(suggestion => console.log(`    💡 ${suggestion}`));
  });
}
```

**Automated Validation:**
- Scan entire project for naming violations
- Generate detailed error reports
- Provide specific fix suggestions
- Skip irrelevant directories (node_modules, .git, etc.)
- Support bulk validation and reporting

## Success Criteria

- [ ] All new files follow lowercase convention
- [ ] Underscores used for word separation
- [ ] Descriptive names that indicate content clearly
- [ ] Appropriate numeric prefixes applied
- [ ] Correct file extensions used (lowercase)
- [ ] Directory-specific naming patterns followed
- [ ] Existing files renamed to comply with standards
- [ ] All file references updated after renames
- [ ] Automated validation passes for entire project

## Common Pitfalls

1. **Mixed Case Filenames** - Always use lowercase for all files
2. **Spaces or Hyphens** - Use underscores instead of spaces or hyphens
3. **Non-Descriptive Names** - Choose names that clearly indicate content
4. **Wrong Numeric Prefixes** - Use appropriate prefix ranges for content types
5. **Uppercase Extensions** - All extensions must be lowercase (.md, .js, .json)
6. **Inconsistent Directory Patterns** - Follow established patterns for each directory type
7. **Missing File Renames** - Update existing non-compliant files
8. **Broken References** - Update all imports and links when renaming files

## Examples

### Correct Filenames

**Documentation:**
- `docs/standards/0000_AGENT_CODING_STANDARDS.md`
- `docs/procedures/0000_PROMPT_MANAGEMENT_PROCEDURE.md`
- `docs/pages-agents/1300_00435_AGENT_CORRESPONDENCE_PROCEDURE.md`

**Source Code:**
- `client/src/common/js/services/promptKeyValidator.js`
- `server/src/routes/promptsRoutes.js`
- `client/src/components/CorrespondenceReplyModal.js`

**Database:**
- `server/sql/create_prompts_table.sql`
- `server/sql/add_prompt_versions_table.sql`

**Tests:**
- `tests/prompt_key_validator.test.js`
- `tests/correspondence_reply_modal.test.js`

### Incorrect Filenames (with corrections)

**❌ `docs/Agent Coding Standards.md`**
**✅ `docs/standards/0000_AGENT_CODING_STANDARDS.md`**
*Issues: Mixed case, spaces, no prefix, wrong directory*

**❌ `client/src/PromptKeyValidator.js`**
**✅ `client/src/common/js/services/promptKeyValidator.js`**
*Issues: Wrong case, missing directory structure*

**❌ `server/sql/Create-Prompts-Table.sql`**
**✅ `server/sql/create_prompts_table.sql`**
*Issues: Mixed case, hyphens, uppercase extension*

## Cross-References

### Related Procedures
- [Agent Coding Standards](skills/agent-coding-standards/SKILL.md) - Language-specific coding standards
- [Agent Development Standards](skills/agent-development-standards/SKILL.md) - Development workflow standards

### Related Skills
- `agent-coding-standards` - JavaScript/Python coding standards
- `agent-development-standards` - Agent framework standards
- `writing-plans` - Planning file organization

### Related Agents
- `DevForge_AI_Team` - Development workflow assistance
- `QualityForge_AI_Team` - Code quality and standards verification