---
name: user-profile-management
description: Manage user signup/signin and collect software/hardware background to enable personalized content in the Physical AI & Humanoid Robotics textbook.
---

# User Profile Management

## Instructions

1. During signup, ask the user about:
   - Software experience (languages, frameworks, AI experience)
   - Hardware experience (robots, sensors, controllers)
   - Learning preferences (visual, text, examples, etc.)
2. Validate user input for completeness and correctness.
3. Store user data securely in the database via DatabaseAgent.
4. Make the user profile available to other agents (DocAgent, ContentAgent) for personalization and content recommendations.
5. Support updates to the profile if the user modifies their background later.

## Example

Input (from signup form):
```json
{
  "user_id": "user123",
  "software": ["Python", "ROS", "FastAPI"],
  "hardware": ["Humanoid robot kits", "Arduino", "Sensors"],
  "learning_style": "visual"
}
