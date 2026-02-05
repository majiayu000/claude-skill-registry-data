---
name: "form-workflows"
description: "Master complex multi-step form workflows. Learn wizard forms, conditional logic, cross-step validation, progress tracking, and data persistence. Essential for building registration flows, checkout processes, and surveys."
tags:
  - "forms"
  - "wizard"
  - "multi-step"
  - "conditional-logic"
  - "validation"
  - "survey"
  - "progress-tracking"
  - "state-management"
version: "1.0.0"
level: "advanced"
author: "FixiPlug Team"
references:
  - "formSchemaPlugin"
  - "agentCommands"
  - "stateTrackerPlugin"
  - "fixiAgentPlugin"
---

# Multi-Step Form Workflows Skill

## Overview

Many real-world forms require **multiple steps**, **conditional logic**, and **complex validation**. This skill teaches you how to orchestrate form-schema, agent-commands, and state-tracker plugins to build robust multi-step form experiences.

**Key Principle**: Break complex forms into manageable steps, validate progressively, maintain state across steps.

**What You'll Master**:
1. **Wizard Forms** - Linear multi-step forms with navigation
2. **Conditional Forms** - Dynamic fields based on user input
3. **Cross-Step Validation** - Validate data across multiple steps
4. **Progress Tracking** - Visual progress indicators and step management
5. **Data Persistence** - Save partial progress and resume
6. **Error Recovery** - Handle validation failures gracefully

---

## Pattern 1: Linear Wizard Form (3 Steps)

**Goal**: Registration form split into Personal Info → Account Details → Preferences

### Step-by-Step Workflow

```javascript
class WizardFormController {
  constructor() {
    this.currentStep = 1;
    this.totalSteps = 3;
    this.formData = {};
    this.stepSchemas = {};
  }

  async initialize() {
    // Set initial state
    await fixiplug.dispatch('api:setState', {
      state: 'wizard-step-1',
      data: {
        step: 1,
        totalSteps: this.totalSteps,
        completed: []
      }
    });

    // Load first step
    await this.loadStep(1);
  }

  async loadStep(stepNumber) {
    this.currentStep = stepNumber;

    // Inject step form
    await fixiplug.dispatch('api:injectFxHtml', {
      html: `
        <div id="wizard-container">
          <div class="progress">
            Step ${stepNumber} of ${this.totalSteps}
            <div class="progress-bar" style="width: ${(stepNumber / this.totalSteps) * 100}%"></div>
          </div>

          <div id="step-content"
               fx-action="/registration/step-${stepNumber}/"
               fx-trigger="load">
          </div>

          <div class="wizard-nav">
            <button id="prev-btn" ${stepNumber === 1 ? 'disabled' : ''}>Previous</button>
            <button id="next-btn">${stepNumber === this.totalSteps ? 'Submit' : 'Next'}</button>
          </div>
        </div>
      `,
      selector: '#app',
      position: 'innerHTML'
    });

    // Wait for form to load
    await new Promise(resolve => setTimeout(resolve, 500));

    // Extract schema for this step
    this.stepSchemas[stepNumber] = await fixiplug.dispatch('api:getFormSchema', {
      form: `step-${stepNumber}-form`
    });

    console.log(`Step ${stepNumber} schema:`, this.stepSchemas[stepNumber].schema);

    // Set up navigation
    this.setupNavigation();

    // Update state
    await fixiplug.dispatch('api:setState', {
      state: `wizard-step-${stepNumber}`,
      data: {
        step: stepNumber,
        schema: this.stepSchemas[stepNumber].schema
      }
    });
  }

  setupNavigation() {
    const nextBtn = document.getElementById('next-btn');
    const prevBtn = document.getElementById('prev-btn');

    nextBtn.addEventListener('click', async () => {
      await this.handleNext();
    });

    prevBtn.addEventListener('click', async () => {
      await this.handlePrevious();
    });
  }

  async handleNext() {
    // 1. Collect data from current step
    const formElement = document.querySelector(`form[name="step-${this.currentStep}-form"]`);
    const stepData = this.collectFormData(formElement);

    // 2. Validate current step
    const validation = await fixiplug.dispatch('api:validateFormData', {
      form: `step-${this.currentStep}-form`,
      data: stepData
    });

    if (!validation.valid) {
      console.error('Step validation failed:', validation.errors);

      // Show errors
      this.showValidationErrors(validation.errors);

      await fixiplug.dispatch('api:setState', {
        state: 'validation-error',
        data: {
          step: this.currentStep,
          errors: validation.errors
        }
      });

      return;
    }

    // 3. Save step data
    this.formData[`step${this.currentStep}`] = stepData;

    await fixiplug.dispatch('api:setState', {
      state: 'step-completed',
      data: {
        step: this.currentStep,
        data: this.formData
      }
    });

    // 4. Move to next step or submit
    if (this.currentStep < this.totalSteps) {
      await this.loadStep(this.currentStep + 1);
    } else {
      await this.submitAllSteps();
    }
  }

  async handlePrevious() {
    if (this.currentStep > 1) {
      await this.loadStep(this.currentStep - 1);
    }
  }

  collectFormData(formElement) {
    const formData = new FormData(formElement);
    const data = {};

    for (const [key, value] of formData.entries()) {
      data[key] = value;
    }

    return data;
  }

  showValidationErrors(errors) {
    for (const [field, message] of Object.entries(errors)) {
      const input = document.querySelector(`[name="${field}"]`);

      if (input) {
        const errorDiv = document.createElement('div');
        errorDiv.className = 'field-error';
        errorDiv.textContent = message;

        // Remove existing error
        const existingError = input.parentElement.querySelector('.field-error');
        if (existingError) {
          existingError.remove();
        }

        input.parentElement.appendChild(errorDiv);
        input.classList.add('error');
      }
    }
  }

  async submitAllSteps() {
    // Combine all step data
    const completeData = Object.assign({}, ...Object.values(this.formData));

    console.log('Submitting complete form:', completeData);

    await fixiplug.dispatch('api:setState', {
      state: 'submitting',
      data: { formData: completeData }
    });

    try {
      // Submit to server
      const response = await fetch('/api/registration/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(completeData)
      });

      if (!response.ok) {
        throw new Error('Submission failed');
      }

      const result = await response.json();

      // Success
      await fixiplug.dispatch('api:setState', {
        state: 'registration-complete',
        data: { userId: result.id }
      });

      console.log('Registration complete:', result);

      // Show success message
      await fixiplug.dispatch('api:injectFxHtml', {
        html: '<div class="success">Registration complete! Redirecting...</div>',
        selector: '#app',
        position: 'innerHTML'
      });

    } catch (error) {
      console.error('Submission error:', error);

      await fixiplug.dispatch('api:setState', {
        state: 'submission-error',
        data: { error: error.message }
      });

      alert('Submission failed: ' + error.message);
    }
  }
}

// Usage
const wizard = new WizardFormController();
await wizard.initialize();
```

---

## Pattern 2: Conditional Forms (Dynamic Fields)

**Goal**: Show/hide fields based on user selections

### Dynamic Field Management

```javascript
class ConditionalFormController {
  constructor(formName) {
    this.formName = formName;
    this.conditions = new Map();
    this.schema = null;
  }

  async initialize() {
    // Get initial schema
    const schemaResult = await fixiplug.dispatch('api:getFormSchema', {
      form: this.formName
    });

    this.schema = schemaResult.schema;

    // Set up conditional logic
    this.setupConditions();

    // Listen for changes
    this.watchFormChanges();
  }

  setupConditions() {
    // Example: Show "Company Name" if user type is "Business"
    this.conditions.set('userType', {
      field: 'userType',
      values: {
        'business': ['companyName', 'taxId'],
        'individual': ['dateOfBirth', 'ssn']
      }
    });

    // Example: Show shipping address if different from billing
    this.conditions.set('differentShipping', {
      field: 'differentShippingAddress',
      values: {
        'true': ['shippingAddress', 'shippingCity', 'shippingZip'],
        'false': []
      }
    });
  }

  watchFormChanges() {
    const formElement = document.querySelector(`form[name="${this.formName}"]`);

    // Watch all condition trigger fields
    for (const [_, condition] of this.conditions) {
      const triggerField = formElement.querySelector(`[name="${condition.field}"]`);

      if (triggerField) {
        triggerField.addEventListener('change', async (e) => {
          await this.handleCondition(condition, e.target.value);
        });

        // Apply initial state
        this.handleCondition(condition, triggerField.value);
      }
    }
  }

  async handleCondition(condition, value) {
    const fieldsToShow = condition.values[value] || [];

    // Show/hide fields
    for (const fieldName of Object.keys(condition.values).flatMap(k => condition.values[k])) {
      const field = document.querySelector(`[name="${fieldName}"]`);
      const container = field?.closest('.form-field');

      if (container) {
        if (fieldsToShow.includes(fieldName)) {
          container.style.display = 'block';
          field.removeAttribute('disabled');
        } else {
          container.style.display = 'none';
          field.setAttribute('disabled', 'disabled');
          field.value = ''; // Clear hidden field
        }
      }
    }

    // Update state
    await fixiplug.dispatch('api:setState', {
      state: 'conditional-fields-updated',
      data: {
        trigger: condition.field,
        value,
        visibleFields: fieldsToShow
      }
    });

    // Re-extract schema (fields have changed)
    const updatedSchema = await fixiplug.dispatch('api:getFormSchema', {
      form: this.formName
    });

    this.schema = updatedSchema.schema;

    console.log('Schema updated:', this.schema);
  }

  async validateWithConditions() {
    // Only validate visible fields
    const formElement = document.querySelector(`form[name="${this.formName}"]`);
    const visibleFields = Array.from(formElement.querySelectorAll('[name]:not([disabled])'))
      .map(input => input.name);

    const formData = this.collectFormData(formElement);

    // Filter data to only include visible fields
    const dataToValidate = {};
    for (const field of visibleFields) {
      if (formData[field] !== undefined) {
        dataToValidate[field] = formData[field];
      }
    }

    const validation = await fixiplug.dispatch('api:validateFormData', {
      form: this.formName,
      data: dataToValidate
    });

    return validation;
  }

  collectFormData(formElement) {
    const formData = new FormData(formElement);
    const data = {};

    for (const [key, value] of formData.entries()) {
      data[key] = value;
    }

    return data;
  }
}

// Usage
const conditionalForm = new ConditionalFormController('registration-form');
await conditionalForm.initialize();

// Later: validate
const validation = await conditionalForm.validateWithConditions();
if (validation.valid) {
  console.log('Form is valid');
}
```

---

## Pattern 3: Cross-Step Validation

**Goal**: Validate data consistency across multiple form steps

### Cross-Step Validator

```javascript
class CrossStepValidator {
  constructor() {
    this.stepData = {};
    this.crossStepRules = [];
  }

  addStepData(stepNumber, data) {
    this.stepData[stepNumber] = data;
  }

  addCrossStepRule(rule) {
    // Rule format:
    // {
    //   name: 'password-match',
    //   validate: (allData) => boolean,
    //   message: 'Error message',
    //   affectedSteps: [1, 2]
    // }
    this.crossStepRules.push(rule);
  }

  async validateAllSteps() {
    const errors = {};

    // Run all cross-step validation rules
    for (const rule of this.crossStepRules) {
      const isValid = await rule.validate(this.stepData);

      if (!isValid) {
        errors[rule.name] = {
          message: rule.message,
          affectedSteps: rule.affectedSteps
        };
      }
    }

    const isValid = Object.keys(errors).length === 0;

    await fixiplug.dispatch('api:setState', {
      state: isValid ? 'cross-validation-passed' : 'cross-validation-failed',
      data: {
        errors: isValid ? undefined : errors
      }
    });

    return {
      valid: isValid,
      errors: isValid ? undefined : errors
    };
  }
}

// Usage Example: Registration with Password Confirmation

const validator = new CrossStepValidator();

// Add rule: Password must match across steps
validator.addCrossStepRule({
  name: 'password-match',
  validate: (stepData) => {
    const password = stepData[2]?.password;
    const confirmPassword = stepData[2]?.confirmPassword;

    return password === confirmPassword;
  },
  message: 'Passwords do not match',
  affectedSteps: [2]
});

// Add rule: Email must be unique (async check)
validator.addCrossStepRule({
  name: 'email-unique',
  validate: async (stepData) => {
    const email = stepData[1]?.email;

    const response = await fetch(`/api/check-email?email=${email}`);
    const result = await response.json();

    return result.available;
  },
  message: 'Email is already registered',
  affectedSteps: [1]
});

// Add rule: Age must be 18+ if account type is business
validator.addCrossStepRule({
  name: 'business-age-requirement',
  validate: (stepData) => {
    const accountType = stepData[1]?.accountType;
    const birthDate = stepData[2]?.dateOfBirth;

    if (accountType !== 'business') {
      return true; // Rule doesn't apply
    }

    const age = new Date().getFullYear() - new Date(birthDate).getFullYear();
    return age >= 18;
  },
  message: 'Must be 18+ for business accounts',
  affectedSteps: [1, 2]
});

// Collect data from step 1
validator.addStepData(1, {
  email: 'user@example.com',
  accountType: 'business'
});

// Collect data from step 2
validator.addStepData(2, {
  password: 'SecurePass123!',
  confirmPassword: 'SecurePass123!',
  dateOfBirth: '1990-01-01'
});

// Validate all steps
const validation = await validator.validateAllSteps();

if (!validation.valid) {
  console.error('Cross-step validation failed:', validation.errors);

  // Show errors to user
  for (const [ruleName, error] of Object.entries(validation.errors)) {
    alert(`Error in step(s) ${error.affectedSteps.join(', ')}: ${error.message}`);
  }
}
```

---

## Pattern 4: Progress Tracking & Resumption

**Goal**: Save partial progress and allow users to resume later

### Progress Persistence

```javascript
class FormProgressManager {
  constructor(formId) {
    this.formId = formId;
    this.storageKey = `form_progress_${formId}`;
  }

  async saveProgress(stepNumber, stepData) {
    const progress = this.loadProgress() || {
      formId: this.formId,
      startedAt: new Date().toISOString(),
      steps: {}
    };

    progress.steps[stepNumber] = {
      data: stepData,
      completedAt: new Date().toISOString()
    };

    progress.lastUpdated = new Date().toISOString();
    progress.currentStep = stepNumber;

    // Save to localStorage
    localStorage.setItem(this.storageKey, JSON.stringify(progress));

    // Update state
    await fixiplug.dispatch('api:setState', {
      state: 'progress-saved',
      data: {
        formId: this.formId,
        step: stepNumber,
        progress: progress
      }
    });

    console.log('Progress saved:', progress);
  }

  loadProgress() {
    const stored = localStorage.getItem(this.storageKey);

    if (!stored) {
      return null;
    }

    try {
      return JSON.parse(stored);
    } catch (error) {
      console.error('Failed to parse stored progress:', error);
      return null;
    }
  }

  hasProgress() {
    return !!this.loadProgress();
  }

  async restoreProgress() {
    const progress = this.loadProgress();

    if (!progress) {
      console.log('No saved progress found');
      return null;
    }

    await fixiplug.dispatch('api:setState', {
      state: 'progress-restored',
      data: progress
    });

    console.log('Progress restored:', progress);

    return progress;
  }

  clearProgress() {
    localStorage.removeItem(this.storageKey);

    fixiplug.dispatch('api:setState', {
      state: 'progress-cleared',
      data: { formId: this.formId }
    });

    console.log('Progress cleared');
  }

  async promptResume() {
    if (!this.hasProgress()) {
      return false;
    }

    const progress = this.loadProgress();
    const lastUpdated = new Date(progress.lastUpdated);
    const hoursSince = (Date.now() - lastUpdated.getTime()) / (1000 * 60 * 60);

    const message = `You have saved progress from ${Math.round(hoursSince)} hours ago (Step ${progress.currentStep}). Resume?`;

    return confirm(message);
  }
}

// Usage in Wizard

class WizardWithProgress extends WizardFormController {
  constructor() {
    super();
    this.progressManager = new FormProgressManager('registration-wizard');
  }

  async initialize() {
    // Check for saved progress
    if (await this.progressManager.promptResume()) {
      // Restore progress
      const progress = await this.progressManager.restoreProgress();

      // Restore form data
      this.formData = progress.steps;

      // Resume at last step
      await this.loadStep(progress.currentStep);

      console.log('Resumed from saved progress');
    } else {
      // Start fresh
      this.progressManager.clearProgress();
      await super.initialize();
    }
  }

  async handleNext() {
    // Save progress before moving to next step
    const formElement = document.querySelector(`form[name="step-${this.currentStep}-form"]`);
    const stepData = this.collectFormData(formElement);

    await this.progressManager.saveProgress(this.currentStep, stepData);

    // Continue with normal flow
    await super.handleNext();
  }

  async submitAllSteps() {
    // Submit form
    await super.submitAllSteps();

    // Clear progress on successful submission
    this.progressManager.clearProgress();
  }
}

// Usage
const wizard = new WizardWithProgress();
await wizard.initialize();
```

---

## Pattern 5: Survey with Skip Logic

**Goal**: Survey form where questions depend on previous answers

### Survey Controller

```javascript
class SurveyController {
  constructor(surveyConfig) {
    this.config = surveyConfig;
    this.answers = {};
    this.currentQuestion = 0;
  }

  async initialize() {
    await this.showQuestion(0);
  }

  async showQuestion(index) {
    const question = this.config.questions[index];

    if (!question) {
      // No more questions - submit survey
      await this.submitSurvey();
      return;
    }

    this.currentQuestion = index;

    // Check if question should be skipped
    if (question.showIf && !this.evaluateCondition(question.showIf)) {
      console.log(`Skipping question ${index} (condition not met)`);
      await this.showQuestion(index + 1);
      return;
    }

    // Inject question HTML
    await fixiplug.dispatch('api:injectFxHtml', {
      html: `
        <div class="survey-question">
          <div class="question-progress">${index + 1} of ${this.config.questions.length}</div>
          <h3>${question.text}</h3>
          <form id="question-form">
            ${this.renderQuestionInput(question)}
            <button type="submit">Next</button>
          </form>
        </div>
      `,
      selector: '#survey-container',
      position: 'innerHTML'
    });

    // Handle form submission
    document.getElementById('question-form').addEventListener('submit', async (e) => {
      e.preventDefault();
      await this.handleAnswer(question);
    });

    // Update state
    await fixiplug.dispatch('api:setState', {
      state: 'survey-question',
      data: {
        questionIndex: index,
        question: question.text
      }
    });
  }

  renderQuestionInput(question) {
    switch (question.type) {
      case 'text':
        return `<input type="text" name="answer" required />`;

      case 'number':
        return `<input type="number" name="answer" required />`;

      case 'choice':
        return question.options.map(opt =>
          `<label><input type="radio" name="answer" value="${opt.value}" required /> ${opt.label}</label>`
        ).join('<br />');

      case 'multiple':
        return question.options.map(opt =>
          `<label><input type="checkbox" name="answer" value="${opt.value}" /> ${opt.label}</label>`
        ).join('<br />');

      default:
        return `<input type="text" name="answer" />`;
    }
  }

  async handleAnswer(question) {
    // Collect answer
    const formElement = document.getElementById('question-form');
    const formData = new FormData(formElement);

    let answer;
    if (question.type === 'multiple') {
      answer = formData.getAll('answer');
    } else {
      answer = formData.get('answer');
    }

    // Save answer
    this.answers[question.id] = answer;

    console.log(`Answer to "${question.text}": ${answer}`);

    // Move to next question
    await this.showQuestion(this.currentQuestion + 1);
  }

  evaluateCondition(condition) {
    // Condition format: { questionId: 'q1', value: 'yes' }
    const answer = this.answers[condition.questionId];

    if (condition.operator === 'equals') {
      return answer === condition.value;
    }

    if (condition.operator === 'contains') {
      return Array.isArray(answer) && answer.includes(condition.value);
    }

    if (condition.operator === 'greaterThan') {
      return Number(answer) > Number(condition.value);
    }

    return false;
  }

  async submitSurvey() {
    console.log('Survey complete:', this.answers);

    await fixiplug.dispatch('api:setState', {
      state: 'survey-complete',
      data: { answers: this.answers }
    });

    // Submit to server
    await fetch('/api/survey/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        surveyId: this.config.id,
        answers: this.answers
      })
    });

    // Show thank you message
    await fixiplug.dispatch('api:injectFxHtml', {
      html: '<div class="survey-complete"><h2>Thank you for completing the survey!</h2></div>',
      selector: '#survey-container',
      position: 'innerHTML'
    });
  }
}

// Survey Configuration

const surveyConfig = {
  id: 'customer-satisfaction',
  questions: [
    {
      id: 'q1',
      text: 'How satisfied are you with our product?',
      type: 'choice',
      options: [
        { value: 'very-satisfied', label: 'Very Satisfied' },
        { value: 'satisfied', label: 'Satisfied' },
        { value: 'neutral', label: 'Neutral' },
        { value: 'dissatisfied', label: 'Dissatisfied' }
      ]
    },
    {
      id: 'q2',
      text: 'What specifically did you dislike?',
      type: 'text',
      showIf: { questionId: 'q1', operator: 'equals', value: 'dissatisfied' }
    },
    {
      id: 'q3',
      text: 'Would you recommend us to a friend?',
      type: 'choice',
      options: [
        { value: 'yes', label: 'Yes' },
        { value: 'no', label: 'No' }
      ]
    },
    {
      id: 'q4',
      text: 'What features would you like to see?',
      type: 'text',
      showIf: { questionId: 'q3', operator: 'equals', value: 'yes' }
    }
  ]
};

// Usage
const survey = new SurveyController(surveyConfig);
await survey.initialize();
```

---

## Best Practices

### ✅ DO

1. **Extract schema for each step**
```javascript
const schema = await fixiplug.dispatch('api:getFormSchema', { form: 'step-1-form' });
```

2. **Validate progressively (each step)**
```javascript
const validation = await fixiplug.dispatch('api:validateFormData', { form, data });
if (!validation.valid) { return; }
```

3. **Track progress with state management**
```javascript
await fixiplug.dispatch('api:setState', { state: 'wizard-step-2', data: {...} });
```

4. **Save partial progress**
```javascript
localStorage.setItem('form_progress', JSON.stringify(formData));
```

5. **Provide clear progress indicators**
```javascript
<div class="progress-bar" style="width: ${(step / total) * 100}%"></div>
```

### ❌ DON'T

1. **Don't skip per-step validation**
```javascript
// Bad: Only validate on final submit
// Good: Validate each step before proceeding
```

2. **Don't lose user data on errors**
```javascript
// Bad: Clear form on validation error
// Good: Keep data, show errors, allow fixing
```

3. **Don't block navigation without saving**
```javascript
// Bad: User can't go back without losing data
// Good: Save data before navigating
```

4. **Don't forget conditional field validation**
```javascript
// Only validate fields that are currently visible/enabled
```

---

## Summary

This skill teaches you to:

1. **Build wizard forms** with multi-step navigation
2. **Handle conditional logic** with dynamic fields
3. **Validate across steps** with cross-step rules
4. **Track progress** and enable resumption
5. **Build surveys** with skip logic
6. **Coordinate plugins** (form-schema + agent-commands + state-tracker)

**Remember**: Break complex forms into steps, validate progressively, maintain state, save progress, and provide clear navigation.

