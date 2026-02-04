---
name: tech-stack-constraints
description: Validate code and configurations against the allowed technology stack per constitution. Use when writing platform code, selecting libraries, or checking framework compliance.
allowed-tools: Read, Grep
---

# Tech Stack Constraints

## Instructions

When validating technology choices:

1. Check the proposed technology against the allowed list
2. If not allowed, suggest the approved alternative
3. Reference the constitution section for authority
4. Provide migration guidance if needed

## Allowed Technologies

### Backend
- **Framework**: FastAPI (Python 3.11+)
- **Vector Database**: Qdrant
- **Authentication**: BetterAuth
- **API Format**: REST with JSON

### Frontend
- **Static Site**: Docusaurus 3.x
- **UI Framework**: React 18+
- **Language**: TypeScript
- **Chatbot**: CopilotKit/ChatKit

### Robotics
- **Middleware**: ROS 2 Humble
- **Simulation**: Gazebo, Isaac Sim
- **Robot Description**: URDF, XACRO
- **Languages**: Python, C++ (for ROS nodes)

### Infrastructure
- **Hosting**: GitHub Pages (static), Cloud Run (API)
- **CI/CD**: GitHub Actions
- **Container**: Docker (optional)

## Validation Rules

1. **No alternative web frameworks** - Django, Flask, Express are NOT allowed
2. **No alternative databases** - PostgreSQL, MongoDB are NOT allowed for vector search
3. **No alternative auth** - Passport, Auth0 are NOT allowed
4. **Secrets via .env** - Never hardcode API keys or tokens

## Reference

See [allowed-tech.md](allowed-tech.md) for the complete list.
