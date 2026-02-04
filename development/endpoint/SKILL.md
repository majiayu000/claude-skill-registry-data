---
name: endpoint
description: Create Express.js API endpoints following the MVC pattern. Use when the user wants to create new REST API routes, controllers, or services for the backend.
---

# Endpoint Generator

This skill helps you create new API endpoints following the Express.js MVC pattern used in this codebase.

## Instructions

When the user invokes this skill, guide them through creating a new endpoint:

1. **Ask for endpoint details:**
   - Feature name (e.g., "notifications", "settings", "reports")
   - Route path (e.g., "/api/notifications")
   - HTTP methods needed (GET, POST, PUT, DELETE, PATCH)
   - Authentication requirements (none, authenticate, requireAdmin)
   - Brief description of what each endpoint does

2. **Create the route file:**
   - Location: `/home/user/math/backend/src/routes/[featureName]Routes.ts`
   - Import necessary dependencies (Router, middleware, controllers)
   - Define routes with appropriate HTTP methods
   - Apply middleware (authenticate, requireAdmin, etc.)
   - Export the router

3. **Create the controller file:**
   - Location: `/home/user/math/backend/src/controllers/[featureName]Controller.ts`
   - Import Request, Response types from Express
   - Create controller functions for each endpoint
   - Include proper error handling with try-catch
   - Validate request inputs
   - Return appropriate HTTP status codes
   - Export all controller functions

4. **Optionally create a service file if needed:**
   - Location: `/home/user/math/backend/src/services/[featureName]Service.ts`
   - Contains business logic and external integrations
   - Separates data processing from HTTP handling
   - Export service functions

5. **Show registration instructions:**
   - Provide the exact line to add to `/home/user/math/backend/src/index.ts`
   - Show where to add the import statement
   - Show where to register the route with `app.use()`

## Patterns to Follow

### Route File Pattern

```typescript
import { Router } from 'express';
import { authenticate, requireAdmin } from '../middleware/auth';
import {
  controllerFunction1,
  controllerFunction2,
} from '../controllers/[featureName]Controller';

const router = Router();

/**
 * @route   GET /api/[feature]/[path]
 * @desc    Description of what this endpoint does
 * @access  Public/Private/Admin
 */
router.get('/[path]', authenticate, controllerFunction1);

/**
 * @route   POST /api/[feature]/[path]
 * @desc    Description of what this endpoint does
 * @access  Public/Private/Admin
 */
router.post('/[path]', authenticate, requireAdmin, controllerFunction2);

export default router;
```

### Controller File Pattern

```typescript
import { Request, Response } from 'express';
import { serviceFunction } from '../services/[featureName]Service';

/**
 * Controller for [description]
 */
export const controllerFunction1 = async (req: Request, res: Response) => {
  try {
    // Extract parameters
    const { param1, param2 } = req.body;
    const userId = req.user?.userId;

    // Validate inputs
    if (!param1) {
      return res.status(400).json({
        success: false,
        error: 'param1 is required',
      });
    }

    // Call service layer
    const result = await serviceFunction(param1, param2, userId);

    // Return success response
    return res.status(200).json({
      success: true,
      data: result,
    });
  } catch (error: any) {
    console.error('Error in controllerFunction1:', error);
    return res.status(500).json({
      success: false,
      error: error.message || 'Internal server error',
    });
  }
};
```

### Service File Pattern (Optional)

```typescript
/**
 * Service function for [description]
 */
export async function serviceFunction(
  param1: string,
  param2?: string,
  userId?: string
): Promise<any> {
  // Business logic here
  // Database queries
  // External API calls
  // Data processing

  return result;
}
```

### Middleware Options

- `authenticate` - Requires valid JWT token, attaches `req.user`
- `requireAdmin` - Requires admin role (must use after authenticate)
- No middleware - Public endpoint

### Error Handling Standards

- **400** - Bad Request (validation errors)
- **401** - Unauthorized (authentication required)
- **403** - Forbidden (insufficient permissions)
- **404** - Not Found
- **500** - Internal Server Error

### Response Format Standards

**Success responses:**
```typescript
{
  success: true,
  data: result
}
```

**Error responses:**
```typescript
{
  success: false,
  error: 'Error message'
}
```

## Registration Instructions Template

After creating the files, provide these instructions:

1. **Add import to `/home/user/math/backend/src/index.ts`:**
   ```typescript
   import [featureName]Routes from './routes/[featureName]Routes';
   ```

2. **Register route (add after existing routes):**
   ```typescript
   app.use('/api/[feature]', [featureName]Routes);
   ```

## Tips

- Use descriptive function and variable names
- Add JSDoc comments for documentation
- Keep controllers thin - move complex logic to services
- Always validate user inputs
- Use appropriate HTTP status codes
- Log errors with descriptive messages
- Consider adding TypeScript interfaces for request/response types
- Test with different authentication scenarios

## Examples

### Example 1: Simple GET endpoint

**User request:** "Create an endpoint to get user profile"

**Steps:**
1. Create `profileRoutes.ts` with GET /api/profile route
2. Create `profileController.ts` with getProfile function
3. Add authentication middleware
4. Register route in index.ts

### Example 2: Full CRUD resource

**User request:** "Create endpoints for managing user notifications"

**Steps:**
1. Create `notificationRoutes.ts` with routes:
   - GET /api/notifications - Get user's notifications
   - POST /api/notifications - Create new notification
   - PATCH /api/notifications/:id/read - Mark as read
   - DELETE /api/notifications/:id - Delete notification
2. Create `notificationController.ts` with all controller functions
3. Create `notificationService.ts` for database operations
4. Add authentication middleware to all routes
5. Register routes in index.ts
