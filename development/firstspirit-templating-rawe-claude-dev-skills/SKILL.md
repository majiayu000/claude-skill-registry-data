---
name: firstspirit-templating
description: This skill provides comprehensive knowledge for templating in the FirstSpirit CMS, specifically focused on SiteArchitect development. This skill should be used when working with FirstSpirit templates including page templates, section templates, format templates, link templates, input components, template syntax, system objects, rules, and workflows. The skill is organized as structured reference documentation with topics covering architecture, template types, syntax, and development practices.
---

# FirstSpirit Templating

## Overview

This skill provides comprehensive guidance for developing templates in FirstSpirit CMS using SiteArchitect. FirstSpirit uses a unique templating system that separates content, layout, and structure across multiple stores (Template Store, Content Store, Site Store, Media Store). Template development involves creating reusable components using FirstSpirit's template syntax, input components, and configuration options.

## When to Use This Skill

Use this skill when:
- Developing FirstSpirit templates (page, section, format, link templates)
- Working with FirstSpirit template syntax and instructions
- Configuring input components and forms in SiteArchitect
- Creating dynamic forms using rules and validation
- Implementing workflows and approval processes
- Working with FirstSpirit's store architecture
- Using system objects, variables, and functions in templates
- Debugging FirstSpirit templates

## How to Use This Skill

The skill organizes FirstSpirit templating knowledge into topic-specific reference files. When working on a specific aspect of FirstSpirit templating, read the relevant reference file(s) to gain detailed knowledge about that topic.

## Reference Documentation Topics

**IMPORTANT:** Read the reference and do not use your global knowledge about other templating systems, as FirstSpirit has its own unique concepts and syntax.

### 1. Core Architecture

**General Structure** (`references/general-structure.md`)
- FirstSpirit's six-store architecture (Template Store, Content Store, Site Store, Media Store, Global Settings)
- Separation of content and layout principles
- Core concepts: content-first approach, multi-user collaboration, multilingual architecture
- Best practices for organizing each store

**Template Development Basics** (`references/template-development-basics.md`)
- Introduction to template development fundamentals
- Development tools: SiteArchitect, ContentCreator, debugging tools
- Template components overview (Forms, Rules, Snippets, Template Syntax)
- Development workflows and best practices

**Template Structure** (`references/template-structure.md`)
- Template composition and organization
- Seven template types (page, section, format, link, scripts, database schemata, workflows)
- Five-tab structure (Properties, Form, Rules, Snippet, Template Set)
- Template development workflow from planning through deployment

### 2. Template Types

**Page Templates** (`references/page-templates.md`)
- Page template basics and framework structure
- Five-tab structure (Properties, Form, Rules, Snippet, Template Set)
- Input components for page configuration
- Content insertion locations for editors
- Snippet tab for preview content

**Section Templates** (`references/section-templates.md`)
- Section template fundamentals
- Adding content to page framework
- Input components for dynamic content (text, images, tables, datasets)
- Template set architecture with CMS_HEADER and output areas
- Integration with page templates

**Format Templates** (`references/format-templates.md`)
- Text formatting options for editors
- Section vs. individual text formatting
- Default format templates and HTML templates
- Table format templates with display rules and style application

**Link Templates** (`references/link-templates.md`)
- Eight supported link types (internal, image, download, external, email, dataset, remote, image map)
- Five-area configuration structure
- Usage through input components (CMS_INPUT_LINK, CMS_INPUT_DOM, FS_CATALOG)
- Language handling and preview management

**Script Templates** (`references/script-templates.md`)
- BeanShell scripting fundamentals
- Four-tab script configuration system
- Implementing custom functions
- Migration scenarios and external system integration

**Table Templates** (`references/table-templates.md`)
- Database schema templates and abstraction layers
- Table template configuration (six configuration tabs)
- Database integration workflow from schema creation through query configuration
- Inline tables with format and style requirements

**Workflows** (`references/workflows.md`)
- Workflow structure and configuration
- Approval and release processes
- BasicWorkflows module documentation
- Permissions, validation, and error handling

### 3. Template Syntax

**Instructions** (`references/template-syntax-instructions.md`)
- Complete reference for FirstSpirit template instructions
- Core instructions: $CMS_VALUE$, $CMS_SET$, $CMS_IF$, $CMS_FOR$, $CMS_SWITCH$
- Template operations: $CMS_RENDER$, $CMS_INCLUDE$, $CMS_REF$
- Control flow patterns and variable management
- Syntax, parameters, and usage examples for each instruction

**Expressions and Data Types** (`references/template-syntax-expressions.md`)
- All FirstSpirit data types: Boolean, String, Number, Date, List, Map, Set
- Expression syntax and operations
- Lambda expressions and data transformations
- Type conversions and methods
- Real-world use cases for data manipulation

**Functions** (`references/template-syntax-functions.md`)
- Template functions: editorId(), if()
- Function syntax and parameters
- ContentCreator content highlighting with editorId()
- Conditional logic with inline if() function
- Combining functions effectively

**System Objects** (`references/template-syntax-system-objects.md`)
- Complete reference for FirstSpirit system objects
- #global (project/page/preview information)
- #field (form component access)
- #for (loop control)
- #style (table styling)
- #content (DOM Editor content)
- #this (context object)
- Practical code examples and common patterns

**Variables** (`references/variables.md`)
- Variable identifier naming rules and conventions
- Variable definition in Form, Header, and Body areas
- Output methods using $CMS_VALUE$ and $CMS_REF$
- Variable scope and lifecycle management
- Metadata variables with inheritance models

### 4. Forms and Components

**Rules and Dynamic Forms** (`references/rules.md`)
- Rules for creating dynamic forms
- Rule structure: execution timing, preconditions, value determination, handling
- Form properties manipulation
- Validation mechanisms with severity levels (SAVE, RELEASE, INFO)
- Practical examples: conditional visibility, dependent dropdowns, date validation
- Best practices for multi-language support and performance

**Metadata** (`references/metadata.md`)
- Creating and configuring metadata templates
- System-assigned and user-defined metadata
- .meta() method for accessing metadata values
- Three inheritance modes (none, inherit, add)
- ELEMENTTYPE and TEMPLATE properties for dynamic forms
- SEO metadata and media-specific metadata examples

**Snippets** (`references/snippets.md`)
- Snippet components: thumbnails, labels, extracts
- Snippet tab configuration
- Implementation patterns using form variables and methods
- Advanced techniques: empty checks, type validation, multilingual support
- Best practices for teaser design and preview content

### 5. Development Tools

**Template Wizard** (`references/template-wizard.md`)
- HTML import capabilities and automated component generation
- Form Builder functionality for reusable form templates
- Workflows for common scenarios
- Best practices for wizard-based template creation
- Limitations requiring manual SiteArchitect intervention

## Official Documentation

All reference files are based on official FirstSpirit documentation from e-Spirit/Crownpeak:
- **Main documentation:** https://docs.e-spirit.com/odfs/
- **Template development:** https://docs.e-spirit.com/odfs/template-develo/
- **Template basics:** https://docs.e-spirit.com/odfs/templates-basic/
- **API documentation:** https://docs.e-spirit.com/odfs/access/

## Typical Development Workflow

1. **Understand the architecture** - Start with `general-structure.md` and `template-development-basics.md`
2. **Choose template type** - Read the appropriate template reference (page, section, format, link)
3. **Learn the syntax** - Review template syntax instructions, expressions, and system objects
4. **Add interactivity** - Use rules and dynamic forms for advanced functionality
5. **Test and debug** - Use Template Inspector and FirstSpirit Debugger
6. **Deploy** - Follow workflow and release processes

## Best Practices

- **Separation of concerns**: Keep content (Content Store), layout (Template Store), and structure (Site Store) separate
- **Reusability**: Design section templates to be reusable across multiple pages
- **Multilingual support**: Always consider language handling in templates
- **Validation**: Use rules for form validation and provide clear error messages
- **Documentation**: Use meaningful variable names and add comments in templates
- **Testing**: Test templates in both SiteArchitect and ContentCreator environments
- **Performance**: Minimize complex calculations in templates; move logic to scripts or modules when appropriate

## Common Use Cases

### Creating a New Page Template
1. Read `page-templates.md` for structure
2. Review `input-components.md` for form elements (note: detailed component reference not included in this skill version)
3. Check `template-syntax-instructions.md` for output syntax
4. Use `snippets.md` for preview configuration

### Building Dynamic Forms
1. Start with `rules.md` for dynamic form behavior
2. Review `variables.md` for state management
3. Check `metadata.md` for metadata integration
4. Reference `template-syntax-system-objects.md` for accessing form data

### Working with Template Output
1. Review `template-syntax-instructions.md` for core instructions
2. Check `template-syntax-system-objects.md` for data access
3. Use `template-syntax-expressions.md` for data transformation
4. Reference `format-templates.md` and `link-templates.md` for content formatting

## Getting Help

When encountering issues:
1. Check the relevant reference file for detailed documentation
2. Review official FirstSpirit documentation links provided in reference files
3. Use the Template Inspector and Debugger tools in SiteArchitect
4. Verify template syntax and system object usage against the syntax references
