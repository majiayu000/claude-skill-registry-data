---
name: livewire-principles
description: Principles for writing simple, maintainable Laravel/Livewire code. Use when writing Livewire components, tests, or Blade views. Focuses on avoiding over-engineering.
---

# Laravel/Livewire Principles

> The right mindset prevents over-engineering before it starts.

These principles guide you toward simple, maintainable code. They're not rules to follow blindly - they're questions to ask yourself as you write.

---

## 1. Trust the Framework

Laravel validation works. Livewire form binding works. Eloquent relationships work. Don't rebuild what's already there.

**Ask yourself:** "Does the framework already handle this?"

If Livewire tracks when a form field changes, you don't need to track it too. If Laravel validation rejects invalid input, you don't need to check it again. If an enum cast throws on invalid values, you don't need a guard clause.

```php
// The framework handles this - you don't need to
public function save(): void
{
    $this->validate(); // Laravel validates
    $this->form->save(); // Done
}
```

---

## 2. Test Behavior, Not Implementation

Test what users see and what data changes. If a test would break when you refactor (without changing behavior), it's testing implementation details.

**Ask yourself:** "Would this test break if I refactored without changing behavior?"

Good tests survive refactoring. They verify outcomes: "A role was created in the database." They don't verify mechanics: "A modal closed and a property was reset."

```php
// Test behavior: what changed in the world?
it('creates a new role', function () {
    Livewire::test(RolesList::class)
        ->set('roleName', 'Editor')
        ->call('saveRole');

    expect(Role::where('name', 'Editor')->exists())->toBeTrue();
});

// Not implementation: what happened inside the component?
// (Don't test that $isModalOpen became false)
```

---

## 3. Let Errors Surface

Don't hide problems with defensive guards and silent returns. On a trusted network with error monitoring, exceptions are helpful - they tell you something's wrong.

**Ask yourself:** "Am I hiding a problem or solving it?"

If invalid data reaches your code through normal use, fix the source. If it can only arrive through deliberate manipulation, let it fail loudly - that's useful information.

```php
// Let it fail - this tells you something's wrong
public function updateLevel(int $skillId, SkillLevel $level): void
{
    $this->user->skills()->updateExistingPivot($skillId, [
        'level' => $level->value,
    ]);
}

// Don't silently swallow problems
// if (! $this->user) { return; } // Where did the user go?!
```

---

## 4. Simple Over Clever

The right amount of code is the minimum that works. If you're adding complexity "just in case" or "for future flexibility" - stop.

**Ask yourself:** "Am I adding this 'just in case'?"

Three similar lines are better than a premature abstraction. A button that's always visible is simpler than one that tracks whether it "should" be visible. Code you don't write has no bugs.

```php
// Simple: always show the button, let validation handle invalid states
<flux:button type="submit">Save</flux:button>

// Over-engineered: track whether the form "deserves" a save button
// @if($isFormModified && $hasRequiredFields && !$isSaving)
```

---

## 5. The Happy Path is Enough (Usually)

Test that things work when used correctly. Edge cases requiring malicious intent don't need testing on internal staff apps.

**Ask yourself:** "Who would actually do this?"

Trusted staff won't open devtools to inject invalid form values. They won't craft malicious URLs to bypass validation. Test for realistic use, not theoretical attacks.

**Caveat:** Student-facing features need more care. There's always one who'll try it on. For features accessible to undergraduates, add appropriate validation and authorization.

```php
// For staff apps: test the workflow works
it('assigns a role to a user', function () { ... });

// For student-facing: also test they can't access others' data
it('prevents students accessing other students records', function () { ... });
```

---

## Questions Before You Code

Pause and ask:

1. **Does the framework already handle this?**
   If yes, don't rebuild it.

2. **Am I testing what users see, or component internals?**
   Test outcomes, not mechanics.

3. **Would this test break if I refactored without changing behavior?**
   If yes, it's testing implementation.

4. **Am I adding this "just in case"?**
   If yes, probably don't.

5. **Who would actually do this?**
   Trusted staff? Happy path is enough. Students? Be more careful.

---

## Detailed Examples

For more thorough side-by-side comparisons, see:

- **[Component Examples](component-examples.md)** - Form delegation, validation, modal patterns, Blade templates
- **[Test Examples](test-examples.md)** - Behavior vs implementation tests, the refactoring test, staff vs student apps

---

## What's Already Handled

Some things are already enforced or documented elsewhere:

- **Validation hooks** block: `DB::` queries, `@php` in Blade, Mockery mocks, `assertDatabase`, `select()` calls
- **CLAUDE.md** documents: code style, Livewire conventions, testing practices, Eloquent patterns
- **Flux skill** covers: UI component patterns, button variants, modal triggers

This skill focuses on the mindset. The details are elsewhere.

---

## The Underlying Philosophy

> "Simplicity is the ultimate sophistication."

Write code that could be read aloud to a business stakeholder. If you find yourself explaining why you needed a `FormModificationTracker` service, something went wrong earlier.

The goal isn't to follow rules. It's to write code so obvious that rules aren't needed.
