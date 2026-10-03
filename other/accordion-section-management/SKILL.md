---
memory_layer: durable_knowledge
para_section: pages/skills/accordion-section-management
gigabrain_tags: ui-frontend, navigation, accordion, implementation, construct-ai
openstinger_context: ui-development, navigation-systems, component-integration
last_updated: 2026-03-30
related_docs:
  - docs_construct_ai/codebase/procedures/ui-frontend/0000_ACCORDION_SECTION_PROCEDURE.md
  - docs_construct_ai/Archive/0975_ACCORDION_MASTER_GUIDE.md
  - docs_construct_ai/Archive/0003_UI_ACCORDION_STANDARDS.md
related_skills:
  - state-based-button-display
  - dropdown-implementation
  - correspondence-reply-modal
frequency_percent: 75.0
success_rate_percent: 92.0
---

# Accordion Section Management

## Overview
Comprehensive skill for managing Construct AI's accordion navigation system, ensuring consistent implementation across server templates, client fallbacks, and emergency configurations. This skill transforms complex accordion management procedures into structured, actionable steps for reliable UI navigation implementation.

## When to Use This Skill
- Adding new navigation sections to the accordion system
- Modifying existing accordion sections (links, permissions, display order)
- Implementing discipline-specific navigation patterns
- Troubleshooting accordion display or routing issues
- Ensuring consistency across development, production, and fallback environments

## Step-by-Step Procedure

### Step 1: Planning and Requirements Analysis
**Duration:** 15-30 minutes
Analyze the accordion change requirements and validate against existing system constraints.

- [ ] **Determine section requirements**: Identify section type (1-tier, 2-tier, or 3-tier), title, display order, and sector restrictions
- [ ] **Check existing sections**: Verify section ID uniqueness and appropriate display order positioning
- [ ] **Validate permissions**: Confirm organization and sector restrictions are properly defined
- [ ] **Document requirements**: Record all links, URLs, subsections, and permission settings

### Step 2: Page Component Preparation
**Duration:** 20-45 minutes
Ensure the target page component exists and is properly configured for routing.

- [ ] **Create page directory structure**: Set up `/client/src/pages/{page-name}/` with required files
- [ ] **Implement index.js**: Create mandatory export file with proper component reference
- [ ] **Update App.js routing**: Add import statement and Route definition for the new page
- [ ] **Verify component structure**: Ensure main component file and optional styles exist
- [ ] **Test route accessibility**: Confirm page loads without "Page Not Found" errors

### Step 3: Server Template Configuration
**Duration:** 15-25 minutes
Update the authoritative server-side accordion configuration.

- [ ] **Locate MASTER_TEMPLATE**: Access `server/src/routes/accordion-sections-routes.js`
- [ ] **Add section structure**: Implement proper JSON structure with id, title, display_order, sector, links, and subsections
- [ ] **Apply naming conventions**: Use correct ID format (`accordion-button-{5-digit-number}`) and display orders
- [ ] **Configure permissions**: Set sector and organization restrictions appropriately
- [ ] **Validate structure**: Ensure "My Tasks Dashboard" appears first for discipline sections

### Step 4: Client Fallback Implementation
**Duration:** 15-25 minutes
Mirror server configuration in the client-side fallback system.

- [ ] **Access sectionMappings**: Open `client/src/common/js/config/00200-ui-display-mappings.js`
- [ ] **Create mapping entry**: Add section configuration with title, optionId, links, and subsections
- [ ] **Ensure consistency**: Verify exact match with server template structure
- [ ] **Apply organization settings**: Configure allowedOrganizations array correctly
- [ ] **Test fallback functionality**: Confirm client fallback works when server unavailable

### Step 5: Emergency Fallback Configuration
**Duration:** 10-15 minutes
Implement minimal critical sections for emergency scenarios.

- [ ] **Access emergencyFallback**: Locate configuration in accordion component
- [ ] **Add essential sections**: Include only critical navigation elements
- [ ] **Minimize complexity**: Remove non-essential subsections and advanced features
- [ ] **Ensure basic functionality**: Verify core navigation works without full system

### Step 6: Testing and Validation
**Duration:** 20-40 minutes
Comprehensive testing across all environments and scenarios.

- [ ] **Functional testing**: Verify accordion loads, expands, collapses, and navigates correctly
- [ ] **Cross-environment validation**: Test development (client fallback), production (server template), and offline (emergency fallback)
- [ ] **Permission verification**: Confirm role-based access and organization filtering work
- [ ] **Mobile responsiveness**: Test accordion behavior on different screen sizes
- [ ] **Error handling**: Verify graceful failure modes and user feedback

### Step 7: Documentation and Maintenance
**Duration:** 10-20 minutes
Update references and prepare for ongoing maintenance.

- [ ] **Update cross-references**: Modify any hardcoded section references in documentation
- [ ] **Version control**: Commit changes with descriptive commit messages
- [ ] **Update change logs**: Document accordion modifications for future reference
- [ ] **Notify stakeholders**: Inform relevant teams about navigation changes

## Success Criteria
- [ ] **Accordion loads consistently** across all environments (development, production, emergency)
- [ ] **All navigation links work** and route to correct destinations without "Page Not Found" errors
- [ ] **Permissions apply correctly** with proper role-based access and organization filtering
- [ ] **No breaking changes** to existing accordion functionality or user workflows
- [ ] **Documentation updated** with new section details and cross-references
- [ ] **Mobile responsive** behavior confirmed on target devices

## Common Pitfalls
1. **Missing index.js file** - Routes show "Page Not Found" without proper component export
2. **Inconsistent configurations** - Server, client, and emergency fallbacks must match exactly
3. **Permission conflicts** - Organization restrictions must align across all configuration layers
4. **Display order conflicts** - Unique display_order values required to prevent navigation issues
5. **URL format errors** - Must use `/route-name` format, never `/#/` hash routing
6. **Missing page components** - Ensure target pages exist before adding accordion entries

## Cross-References

### Source Documentation
- **Primary Procedure**: `docs_construct_ai/codebase/procedures/ui-frontend/0000_ACCORDION_SECTION_PROCEDURE.md`
- **Master Guide**: `docs_construct_ai/Archive/0975_ACCORDION_MASTER_GUIDE.md`
- **UI Standards**: `docs_construct_ai/Archive/0003_UI_ACCORDION_STANDARDS.md`

### Related Skills
- **state-based-button-display**: For button state management within accordion sections
- **dropdown-implementation**: For dropdown menus within accordion navigation
- **correspondence-reply-modal**: For modal implementations triggered from accordion

### Agent Support
- **DevForge**: Code implementation and component development
- **PromptForge**: UI/UX optimization and user experience enhancement
- **QualityForge**: Testing and validation of accordion functionality

## Performance Metrics
- **Average Implementation Time:** 2-3 hours for complete accordion section addition
- **Success Rate:** 92% - Most failures due to missing page components or routing issues
- **Frequency:** 75% of UI development tasks involve accordion navigation management
- **Maintenance Overhead:** <30 minutes/month for typical accordion updates
