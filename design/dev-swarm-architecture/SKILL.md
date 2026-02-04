---
name: dev-swarm-architecture
description: Design system architecture including components, data flow, and deployment boundaries. Use when user asks to design architecture, create architecture diagrams, or start Stage 6 after UX design.
---

# AI Builder - System Architecture

This skill creates/updates the system architecture documentation defining the system structure, major components, data flow, and deployment boundaries without specifying specific frameworks or technologies.

## When to Use This Skill

- User asks to "design architecture" or "create system design"
- User requests to start Stage 6 or the next stage after UX design
- User wants to define system components and their relationships
- User wants to understand data flow and system boundaries
- User needs to plan deployment architecture

## Prerequisites

This skill requires **05-ux** to be completed. The architecture will implement the UX design and functional requirements with a clear system structure.

## Your Roles in This Skill

- **Tech Manager (Architect)**: Lead architecture design with system overview and component definitions. Review PRD and UX design to understand requirements. Create architecture diagrams showing component relationships. Define data structures and data flow patterns. Establish architectural principles and patterns.
- **Backend Architect**: Design backend system components, API structure, and data models. Define service boundaries and responsibilities. Plan database architecture and data flow. Consider scalability and performance requirements.
- **Frontend Architect**: Design frontend architecture and component structure. Define state management approach. Plan client-side data flow and API integration patterns.
- **AI Engineer**: Design AI/ML model architecture and integration patterns. Define prompt engineering strategies and LLM integration. Plan vector database and embeddings architecture. Design model monitoring and evaluation pipelines. Consider AI costs, latency, and fallback strategies. Plan content generation and moderation systems.
- **Content Moderator**: Design content moderation architecture for AI-generated content. Define moderation workflows and automated filtering systems. Plan human-in-the-loop review processes. Design content safety and compliance systems. Consider scalability of moderation infrastructure.
- **DevOps Engineer**: Review architecture for deployment feasibility. Provide input on deployment boundaries and cloud architecture. Consider monitoring, logging, and operational aspects.

## Role Communication

As an expert in your assigned roles, you must announce your actions before performing them using the following format:

As a {Role} [and {Role}, ...], I will {action description}

This communication pattern ensures transparency and allows for human-in-the-loop oversight at key decision points.
## Instructions

Follow these steps in order:

### Step 0: Verify Prerequisites and Gather Context

1. **Check if `05-ux/` folder exists (mandatory):**
   - If NOT found: Inform user they need to create UX design first, then STOP
   - If found: Read all files to understand:
     - User flows and interactions
     - Mockup structure (if UI-based app)
     - Screen navigation patterns

2. **Check if `04-prd/` folder exists (mandatory):**
   - If NOT found: Inform user they need PRD first, then STOP
   - If found: Read to understand:
     - Functional requirements
     - Non-functional requirements (performance, security, scalability)
     - Feature list and priorities

3. **Check if `00-init-ideas/` folder exists (recommended):**
   - If found: Read to understand all files

4. **Check if `03-mvp/` folder exists (recommended):**
   - If found: Read to understand:
     - MVP scope (what to prioritize in architecture)
     - Success metrics (inform performance targets)

5. **Check if this stage should be skipped:**
   - Check if `06-architecture/SKIP.md` exists
   - **If SKIP.md exists:**
     - Read SKIP.md to understand why this stage was skipped
     - Inform the user: "Stage 6 (architecture) is marked as SKIP because [reason from SKIP.md]"
     - Ask the user: "Would you like to proceed to the next stage (tech-specs)?"
     - **If user says yes:**
       - Exit this skill and inform them to run the next stage skill
     - **If user says no:**
       - Ask if they want to proceed with architecture anyway
       - If yes, delete SKIP.md and continue with this skill
       - If no, exit the skill

6. **Check if `06-architecture/` folder exists:**
   - If exists: Read all existing files to understand current architecture state
   - If NOT exists: Will create new structure

7. **If README.md exists:** Check whether it requires diagrams. If it does,
   follow `dev-swarm/docs/mermaid-diagram-guide.md` and use the
   `dev-swarm-mermaid` skill to render outputs.

8. Proceed to Step 1 with gathered context

### Step 1: Refine Design Requirements in README and Get Approval

**CRITICAL: Create/update README.md first based on previous stage results, get user approval, then create other docs.**

1. **Analyze information from previous stages:**
   - Read `05-ux/` to understand user flows and UI structure
   - Read `04-prd/` to understand functional and non-functional requirements
   - Read `03-mvp/` (if exists) to understand what to prioritize
   - Consider cost-budget constraints for this stage

2. **Create or update 06-architecture/README.md with refined requirements:**
   - List deliverables explicitly in README (typical: system-overview.md, architecture-diagram.md, data-flow.md, deployment-boundaries.md)
   - **Stage overview and objectives** (based on previous stage context)
   - **Owners:** Tech Manager (lead), Backend Architect, Frontend Architect, AI Engineer, Content Moderator, DevOps Engineer
   - **Diagrams (if required by project init):**
     - Reference `dev-swarm/docs/mermaid-diagram-guide.md`
     - Include `diagram/` deliverables when needed
   - **What architecture will include:**
     - System components and their responsibilities
     - Architecture diagrams (high-level + detail)
     - Data flow for critical user journeys
     - Deployment boundaries and scaling strategy
   - **Methodology:**
     - How components will be defined (from PRD requirements)
     - Diagram approach (Mermaid for all diagrams)
   - **Deliverables planned:**
     - List of files that will be created (system-overview.md, architecture-diagram.md, etc.)
   - **Budget allocation for this stage** (from cost-budget.md)
   - **Status:** In Progress (update to "Completed" after implementation)

3. **Present README to user:**
   - Show the architecture approach and what will be designed
   - Show what documentation files will be created
   - Explain how it aligns with previous stages
   - Ask: "Does this architecture plan look good? Should I proceed with designing system architecture?"

4. **Wait for user approval:**
   - **If user says yes:** Proceed to Step 2
   - **If user says no:**
     - Ask what needs to be changed
     - Update README based on feedback
     - Ask for approval again

### Step 2: Create/Update Architecture Structure

**Only after user approves the README:**

1. **Create files as specified in the approved README.md:**

   **IMPORTANT:** The file structure below is a SAMPLE only. The actual files you create must follow what was approved in the README.md in Step 1.

   **Typical structure (example):**
   ```
   06-architecture/
   ├── README.md (already created and approved in Step 1)
   ├── system-overview.md (if specified in README)
   ├── architecture-diagram.md (if specified in README)
   ├── data-flow.md (if specified in README)
   └── deployment-boundaries.md (if specified in README)
   ```

   **Create only the files listed in the README's "Deliverables planned" section.**

### Step 3: Create/Update Architecture Documentation

**IMPORTANT: Only create architecture documentation after README is approved in Step 1.**

**NOTE:** The content structure below provides GUIDELINES for typical architecture documentation. Adapt based on the approved README and project needs.

**If files don't exist:** Create new comprehensive architecture documents.

**06-architecture/README.md:**
- Stage overview and objectives
- Specify the owners: Tech Manager (lead), Backend Architect, Frontend Architect, DevOps Engineer
- Summary of architectural approach and principles
- Links to all architecture documentation files
- Key architectural decisions and rationale

**system-overview.md:**

Define the major system components and their responsibilities:

1. **Architectural Principles:**
   - List the guiding principles for this architecture
   - Examples:
     - Separation of concerns
     - Scalability and horizontal scaling
     - Security by design
     - Fail-fast and graceful degradation
     - Stateless services where possible
     - API-first approach
     - Mobile-first or responsive design

2. **System Components:**

   **Format for each component:**
   ```
   ### Component: [Component Name]

   **Type:** Frontend / Backend / Database / External Service / Infrastructure

   **Responsibility:**
   - What this component does
   - What problems it solves
   - What it is NOT responsible for

   **Key Capabilities:**
   - Capability 1
   - Capability 2
   - Capability 3

   **Interfaces:**
   - Inputs: What data/requests it receives
   - Outputs: What data/responses it produces
   - APIs: What APIs it exposes (if any)

   **Dependencies:**
   - What other components does this depend on?
   - What external services does this use?

   **Data Storage:**
   - What data does this component store?
   - Where is it stored?

   **Scalability:**
   - Can this scale horizontally or vertically?
   - What are the scaling constraints?
   ```

3. **Component Categories:**

   **Frontend Components:**
   - Web Application (if applicable)
   - Mobile Application (if applicable)
   - Desktop Application (if applicable)
   - Admin Dashboard (if needed)

   **Backend Components:**
   - API Gateway / Backend for Frontend (BFF)
   - Core Application Services
   - Authentication Service
   - Business Logic Services
   - Background Job Processors
   - Notification Service
   - File Storage Service

   **Data Components:**
   - Primary Database
   - Cache Layer
   - Search Index (if needed)
   - Object Storage (for files/media)
   - Message Queue (if needed)

   **External Services:**
   - Third-party APIs (payment, email, SMS, etc.)
   - Authentication providers (OAuth, SSO)
   - CDN services
   - Monitoring and logging services

4. **Component Interaction Patterns:**
   - Request-Response (synchronous)
   - Event-Driven (asynchronous)
   - Pub-Sub messaging
   - Polling vs. webhooks
   - WebSocket connections (if real-time features)

**architecture-diagram.md:**

Create visual diagrams showing system architecture:

1. **High-Level Architecture Diagram:**

   Use Mermaid to create a diagram showing all major components:

   ```mermaid
   graph TB
       subgraph "Client Layer"
           WebApp[Web Application]
           MobileApp[Mobile Application]
       end

       subgraph "API Layer"
           APIGateway[API Gateway]
           Auth[Auth Service]
       end

       subgraph "Application Layer"
           CoreAPI[Core API Service]
           BgJobs[Background Jobs]
           Notifications[Notification Service]
       end

       subgraph "Data Layer"
           DB[(Primary Database)]
           Cache[(Cache)]
           Storage[(Object Storage)]
       end

       subgraph "External Services"
           Email[Email Service]
           Payment[Payment Service]
       end

       WebApp --> APIGateway
       MobileApp --> APIGateway
       APIGateway --> Auth
       APIGateway --> CoreAPI
       CoreAPI --> DB
       CoreAPI --> Cache
       CoreAPI --> BgJobs
       BgJobs --> Notifications
       Notifications --> Email
       CoreAPI --> Payment
       CoreAPI --> Storage
   ```

2. **Component Detail Diagrams:**

   Create additional diagrams for complex subsystems:
   - Authentication flow diagram
   - Payment processing flow
   - File upload/download flow
   - Real-time messaging flow (if applicable)

3. **Database Schema Diagram (High-Level):**

   Show major entities and relationships:
   ```mermaid
   erDiagram
       User ||--o{ Post : creates
       User ||--o{ Comment : writes
       Post ||--o{ Comment : has
       User {
           uuid id
           string email
           string name
       }
       Post {
           uuid id
           uuid user_id
           string title
           text content
       }
       Comment {
           uuid id
           uuid user_id
           uuid post_id
           text content
       }
   ```

**data-flow.md:**

Document how data flows through the system:

1. **Request Flow (Frontend to Backend):**

   For each major user flow from UX design:

   **Format:**
   ```
   ### Flow: [User Flow Name]

   **Trigger:** User action that initiates the flow (from 05-ux/user-flows.md)

   **Step-by-Step Data Flow:**

   1. **User Action:** User clicks/submits/interacts
      - Component: [Frontend Component]
      - Data: [What data is involved]

   2. **API Request:**
      - Component: Frontend → API Gateway
      - Method: GET/POST/PUT/DELETE
      - Endpoint: /api/resource
      - Request Data: { ... }
      - Headers: [Authentication, Content-Type, etc.]

   3. **Authentication/Authorization:**
      - Component: API Gateway → Auth Service
      - Validation: [What is checked]
      - Result: [Pass/Fail action]

   4. **Business Logic Processing:**
      - Component: Core API Service
      - Processing: [What happens to the data]
      - Validation: [Business rules applied]
      - Transformations: [Data transformations]

   5. **Database Operations:**
      - Component: Core API → Database
      - Operation: SELECT/INSERT/UPDATE/DELETE
      - Tables: [Which tables affected]
      - Transactions: [If transaction needed]

   6. **External Service Calls (if any):**
      - Component: Core API → External Service
      - Service: [Which external service]
      - Purpose: [Why calling it]
      - Fallback: [What if service fails]

   7. **Response Construction:**
      - Component: Core API
      - Data: [Response data structure]
      - Status: [HTTP status code]

   8. **Response to Frontend:**
      - Component: API Gateway → Frontend
      - Data: { ... }
      - Frontend Action: [How UI updates]

   **Error Handling:**
   - What happens if step X fails?
   - Rollback strategy
   - Error messages to user

   **Caching Strategy:**
   - What data is cached?
   - Where is it cached?
   - Cache invalidation rules

   **Performance Considerations:**
   - Expected latency
   - Database query optimization
   - N+1 query prevention
   ```

2. **Data Flow Categories:**
   - **Read Flows**: Fetching and displaying data
   - **Write Flows**: Creating and updating data
   - **Delete Flows**: Removing data
   - **File Upload Flows**: Handling file uploads
   - **Background Processing Flows**: Async jobs and batch operations
   - **Real-time Flows**: WebSocket or server-sent events (if applicable)

3. **Data Transformation Pipeline:**
   - Input validation and sanitization
   - Data normalization
   - Business logic application
   - Response formatting
   - Error formatting

**deployment-boundaries.md:**

Define what runs where and security/trust boundaries:

1. **Deployment Environments:**

   **Development Environment:**
   - Where: Local machine / Dev cloud
   - Purpose: Development and testing
   - Data: Fake/seed data
   - Access: Developers only

   **Staging Environment:**
   - Where: Cloud (same region as production)
   - Purpose: Pre-production testing and QA
   - Data: Production-like data (anonymized)
   - Access: Internal team + selected beta testers

   **Production Environment:**
   - Where: Cloud (specify regions if multi-region)
   - Purpose: Live user-facing environment
   - Data: Real user data
   - Access: Public users (authenticated)

2. **What Runs Where:**

   **Client-Side (User's Device):**
   - Web application (browser)
   - Mobile application (iOS/Android)
   - Desktop application (if applicable)
   - Client-side validation
   - UI rendering and interaction

   **Edge/CDN:**
   - Static assets (HTML, CSS, JS, images)
   - Cached API responses (if applicable)
   - DDoS protection
   - SSL/TLS termination

   **Cloud - Application Layer:**
   - API Gateway
   - Application servers
   - Authentication services
   - Background job workers
   - Notification services

   **Cloud - Data Layer:**
   - Primary database
   - Cache servers (Redis/Memcached)
   - Search indexes (if applicable)
   - Object storage (S3/CloudStorage)
   - Message queues (if applicable)

   **Third-Party Services:**
   - Email delivery (SendGrid, AWS SES, etc.)
   - Payment processing (Stripe, PayPal, etc.)
   - SMS delivery (Twilio, etc.)
   - Analytics (Google Analytics, Mixpanel, etc.)
   - Error tracking (Sentry, etc.)
   - Monitoring (Datadog, New Relic, etc.)

3. **Trust Boundaries:**

   **Boundary 1: User Device ↔ Cloud:**
   - Trust Level: Untrusted to Trusted
   - Security:
     - HTTPS/TLS encryption
     - Authentication required
     - Input validation and sanitization
     - CSRF protection
     - Rate limiting
   - Data Flow: User actions → API requests

   **Boundary 2: Public API ↔ Internal Services:**
   - Trust Level: Partially Trusted to Trusted
   - Security:
     - API authentication (JWT, OAuth)
     - Authorization checks
     - Service-to-service authentication
     - Network segmentation (VPC, private subnets)
   - Data Flow: API Gateway → Internal services

   **Boundary 3: Application ↔ Database:**
   - Trust Level: Trusted to Highly Trusted
   - Security:
     - Database credentials in secrets manager
     - Encrypted connections (SSL/TLS)
     - Principle of least privilege
     - Network isolation
   - Data Flow: Application services → Database

   **Boundary 4: Application ↔ External Services:**
   - Trust Level: Trusted to Untrusted
   - Security:
     - API keys in secrets manager
     - HTTPS only
     - Timeout and retry logic
     - Fallback mechanisms
     - Circuit breaker pattern
   - Data Flow: Application → Third-party APIs

4. **Scaling Assumptions:**

   **Vertical Scaling (Scale Up):**
   - Which components scale vertically?
   - Maximum instance size limits
   - When to switch to horizontal scaling

   **Horizontal Scaling (Scale Out):**
   - Which components scale horizontally?
   - Load balancing strategy
   - Stateless service requirements
   - Session management approach

   **Auto-Scaling Triggers:**
   - CPU utilization thresholds
   - Memory utilization thresholds
   - Request rate thresholds
   - Queue depth thresholds

   **Database Scaling:**
   - Read replicas for read-heavy workloads
   - Sharding strategy (if applicable)
   - Caching to reduce database load
   - Connection pooling

   **CDN and Caching:**
   - Static asset caching
   - API response caching
   - Cache invalidation strategy
   - Edge caching locations

5. **High Availability & Fault Tolerance:**
   - Multi-AZ deployment (if cloud)
   - Database failover strategy
   - Service redundancy
   - Load balancer health checks
   - Circuit breaker for external services
   - Graceful degradation strategies

6. **Geographic Distribution (if applicable):**
   - Multi-region deployment
   - Data residency requirements
   - Latency optimization
   - CDN edge locations

### Step 4: Ensure Alignment

Make sure architecture aligns with:
- Non-functional requirements from 04-prd/non-functional-requirements.md
- Functional requirements from 04-prd/functional-requirements.md
- User flows from 05-ux/user-flows.md
- MVP scope from 03-mvp/ (architecture should support MVP first, then scale)

Verify that:
- All functional requirements can be implemented in this architecture
- Performance targets are achievable
- Security requirements are addressed
- Scalability needs are met
- Deployment is feasible

### Step 5: Final User Review

1. **Inform user that architecture is complete**
2. **Update README.md:**
   - Change **Status** from "In Progress" to "Completed"
   - Add a **Summary** section with key insights (2-3 paragraphs)
   - Add a **Created Files** section listing all created files

3. **Present completed work to user:**
   - Walk through the architecture diagrams
   - Explain major components and their responsibilities
   - Show data flow for critical user journeys
   - Explain deployment boundaries and security

4. **Highlight key insights:**
   - Number of major components
   - Key architectural patterns used
   - Scalability approach
   - Security boundaries
   - Cloud vs. local deployment split

5. **Ask questions:**
   - Does the architecture make sense?
   - Are there any components missing?
   - Any concerns about scalability or security?
   - Ready to proceed to next stage (tech specs)?

6. Make adjustments based on user feedback if needed

### Step 6: Commit to Git (if user confirms)

1. **If user confirms architecture is complete:**
   - Ask if they want to commit to git
2. **If user wants to commit:**
   - Stage all changes in `06-architecture/`
   - Commit with message: "Design system architecture and deployment (Stage 6)"

## Expected Project Structure

```
project-root/
├── 00-init-ideas/
│   └── [existing files]
├── 01-market-research/ (optional)
│   └── [existing files if present]
├── 02-personas/
│   └── [existing files]
├── 03-mvp/
│   └── [existing files]
├── 04-prd/
│   └── [existing files]
├── 05-ux/
│   └── [existing files]
└── 06-architecture/
    ├── README.md (with owners and summary)
    ├── system-overview.md (components + responsibilities)
    ├── architecture-diagram.md (Mermaid diagrams)
    ├── data-flow.md (request/data flow details)
    └── deployment-boundaries.md (what runs where, trust boundaries, scaling)
```

## Key Architecture Principles

1. **Structure, Not Frameworks**: Define system shape without specifying technologies
2. **Component Clarity**: Each component has clear, single responsibility
3. **Separation of Concerns**: Frontend, backend, data, external services clearly separated
4. **Scalability by Design**: Consider scaling from the start
5. **Security Boundaries**: Clear trust boundaries and security controls
6. **Fail Gracefully**: Plan for failures and degradation
7. **Data Flow Transparency**: Clear understanding of how data moves
8. **Deployment Feasibility**: Can actually be deployed and operated

## Architecture Best Practices

1. **Start Simple**: MVP architecture should be simple, add complexity later
2. **Use Diagrams**: Mermaid diagrams make architecture visual and clear
3. **Document Decisions**: Explain why you chose this architecture
4. **Consider Trade-offs**: No architecture is perfect, document trade-offs
5. **Plan for Change**: Make architecture flexible for future needs
6. **Security First**: Build security into architecture, not bolt on later
7. **Performance Aware**: Consider performance implications of design decisions
8. **Operational Thinking**: Consider monitoring, logging, debugging

## Deliverables

By the end of this stage, you should have:
- Complete system overview with component definitions (5-15 major components)
- Architecture diagrams using Mermaid (high-level + detail diagrams)
- Detailed data flow documentation for critical user journeys
- Deployment boundaries and security trust zones defined
- Scaling strategy and assumptions documented
- Foundation for tech stack selection (next stage)
- Clear understanding of how system will be structured
