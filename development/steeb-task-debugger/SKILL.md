---
name: steeb-task-debugger
description: Debug and fix task-related issues in STEEB app. This skill should be used when encountering task creation, completion, deletion, or state management problems in the STEEB task management system.
---

# STEEB Task Debugger

This skill helps debug and resolve issues with task management in the STEEB application.

## When to Use This Skill

Use this skill when encountering:
- Tasks not completing correctly
- Task state inconsistencies between components
- Firestore synchronization errors
- Tasks disappearing or duplicating
- UI not reflecting task changes
- Performance issues with task operations

## Debugging Workflow

### Step 1: Identify the Issue Type

First, determine the type of task issue:

**Task Creation Issues:**
- Check if `addTask` function is being called correctly
- Verify task data structure matches expected `Task` interface
- Check for duplicate task IDs or missing required fields

**Task Completion/Toggle Issues:**
- Verify `toggleTask` is called with correct task ID
- Check if optimistic updates are working
- Verify Firestore synchronization (if enabled)

**Task Deletion Issues:**
- Confirm task exists before deletion attempt
- Check if `deleteTask` function removes from local state
- Verify UI re-renders after deletion

**State Management Issues:**
- Check if tasks are properly synchronized between components
- Verify Zustand store updates trigger re-renders
- Check for stale state or race conditions

### Step 2: Run Diagnostic Commands

Execute these commands to diagnose the problem:

```bash
# Check current task state in console
console.log('Current tasks:', useTaskStore.getState().tasks);

# Check specific task properties
const task = useTaskStore.getState().tasks.find(t => t.id === 'task-id');
console.log('Task details:', task);

# Check store state
console.log('Store state:', useTaskStore.getState());
```

### Step 3: Verify Store Functions

Test the core task management functions:

```javascript
// Test task creation
const testTask = {
  title: 'Debug test task',
  completed: false,
  status: 'pending',
  createdAt: new Date().toISOString()
};
await useTaskStore.getState().addTask(testTask);

// Test task toggle
const taskId = 'existing-task-id';
await useTaskStore.getState().toggleTask(taskId);

// Test task deletion
await useTaskStore.getState().deleteTask(taskId);
```

### Step 4: Check Component Integration

Verify components are using the store correctly:

**SteebChatAI Component:**
- Ensure `toggleTask` and `deleteTask` are properly imported
- Check if button onClick handlers prevent multiple clicks
- Verify error handling in async operations

**Dashboard Component:**
- Ensure tasks are filtered correctly (pending vs completed)
- Check if `useTaskStore` updates trigger re-renders
- Verify statistics calculations are accurate

### Step 5: Common Solutions

**Multiple Click Issues:**
```javascript
// Add this pattern to prevent multiple clicks
const [isProcessing, setIsProcessing] = useState(false);

const handleTaskAction = async (taskId) => {
  if (isProcessing) return;

  setIsProcessing(true);
  try {
    await toggleTask(taskId);
  } catch (error) {
    console.error('Task action failed:', error);
  } finally {
    setIsProcessing(false);
  }
};
```

**State Not Updating:**
```javascript
// Force re-render after store update
setForceUpdate(prev => prev + 1);
// Or use proper React state management
const { tasks, toggleTask } = useTaskStore();
```

**Firebase Errors:**
```javascript
// Handle Firestore errors gracefully
try {
  await FirestoreTaskService.updateTask(id, updates);
} catch (error) {
  console.warn('Firestore sync failed, local changes kept:', error);
  // Continue with local state only
}
```

### Step 6: Performance Optimization

For large task lists:
- Implement virtual scrolling
- Add pagination or lazy loading
- Use React.memo for task components
- Debounce search/filter operations

## Scripts

The following scripts are available for automated debugging:

### Quick Task Validation
```bash
# Run quick task validation
python .claude/skills/steeb-task-debugger/scripts/quick_validate.py
```

### Task State Analyzer
```bash
# Analyze task state consistency
python .claude/skills/steeb-task-debugger/scripts/analyze_task_state.py
```

## References

- Task interface definition in `src/types/index.ts`
- Task store implementation in `src/store/useTaskStore.ts`
- Firestore service in `src/services/firestoreTaskService.ts`
- Task components in `src/components/Task*.tsx`

## Assets

- Debug checklist template for common issues
- Task state flow diagram
- Performance profiling guidelines