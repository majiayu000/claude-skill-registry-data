---
name: beginner-testing
description: Introduce test-driven development to beginners with simple Flask/Sinatra test examples and TDD concepts
license: Complete terms in LICENSE.txt
---

# Beginner Testing Introduction
**Version:** 0.17.0

## When to Use
- User's Vibe app ready to transition to Structured
- User mentions "testing" or "how to test"
- User has 3-4 features, wants quality assurance

## Prerequisites
- Working Flask/Sinatra app with 3-4 features
- Understanding of routes and functions
- Code works but no tests

## What is Testing?
**Without tests:** Change code → Open browser → Click around → Hope nothing broke
**With tests:** Change code → Run tests → See green/red → Know immediately

## TDD Cycle
```
RED → GREEN → REFACTOR

1. RED: Write test that fails (feature doesn't exist)
2. GREEN: Write just enough code to pass
3. REFACTOR: Clean up while tests still pass
```

## Test Types (Simple)
| Type | Tests | Example |
|------|-------|---------|
| Unit | Individual functions | `add_numbers(2,3)` returns `5` |
| Route | Pages load correctly | `/` returns status 200 |
| Integration | Parts work together | Form adds to database |

**Beginners: Start with route tests!**

## First Test (Flask)
```python
# test_app.py
def test_homepage_loads():
    from app import app
    client = app.test_client()
    response = client.get('/')
    assert response.status_code == 200
```

**Run:** `pip install pytest && pytest`

## First Test (Sinatra)
```ruby
# test_app.rb
require 'minitest/autorun'
require 'rack/test'
require_relative 'app'

class AppTest < Minitest::Test
  include Rack::Test::Methods
  def app; Sinatra::Application; end

  def test_homepage_loads
    get '/'
    assert last_response.ok?
  end
end
```

**Run:** `ruby test_app.rb`

## Common Assertions
**Python:** `assert value == 5`, `assert 'text' in response.data`
**Ruby:** `assert_equal 5, value`, `assert_includes body, 'text'`

## TDD Example: Delete Feature
```python
# 1. RED - Write failing test
def test_delete_note():
    client = app.test_client()
    client.post('/add', data={'note': 'Test'})
    response = client.get('/delete/1')
    assert response.status_code == 302

# 2. GREEN - Make it pass
@app.route('/delete/<int:note_id>')
def delete_note(note_id):
    # implementation
    return redirect('/')

# 3. REFACTOR - Clean up
```

## Test Output
**Pass:** `3 passed in 0.12s`
**Fail:** `FAILED - AssertionError: assert 404 == 200`

## What to Test (Beginners)
- Routes exist (not 404)
- Forms submit successfully
- Data saves/displays correctly

## Common Mistakes
| Mistake | Solution |
|---------|----------|
| Not running tests | Run after every change |
| Tests depend on order | Each test independent |
| One giant test | Small tests, one thing each |

## Benefits
- Clarity: Test defines "working"
- Confidence: Know when things break
- Less fear: Change without worrying

---

**End of Skill**
