---
name: common-beginner-coding-errors
description: Diagnose and solve common beginner programming mistakes in Flask or Sinatra development with detailed explanations
license: Complete terms in LICENSE.txt
---

# Common Beginner Coding Errors
**Version:** 0.17.0

## When to Use
- Beginner reports error message
- Code isn't working as expected
- User asks "Why isn't this working?"

## Error Diagnosis Process
1. Get complete error (exact message, file/line, what they tried)
2. Identify category (keyword-based)
3. Guide to solution with explanation
4. Teach prevention

## Errors by Category

### 1. File Management

**Changes Don't Appear:**
| Cause | Solution |
|-------|----------|
| File not saved | Check for dot/asterisk, press Ctrl+S |
| Server not restarted (Sinatra) | Ctrl+C, then `ruby app.rb` |
| Browser cache | Hard refresh: Ctrl+Shift+R |

**Template Not Found:**
- Flask: Templates must be in `templates/` folder (exact name)
- Sinatra: Templates must be in `views/` folder (exact name)

### 2. Python Errors

**IndentationError:**
- Python uses spaces for grouping (not `{ }`)
- Use 4 spaces per level, don't mix tabs/spaces
- Check all lines in block have same indent

**ModuleNotFoundError: No module named 'flask':**
| Check | Solution |
|-------|----------|
| No `(venv)` in prompt | Activate: `venv\Scripts\activate` (Win) or `source venv/bin/activate` |
| Flask not installed | `pip install flask` |
| Wrong Python | Check `which python` points to venv |

### 3. Ruby/Sinatra Errors

**uninitialized constant Sinatra:**
1. Check: `bundle list | grep sinatra`
2. Verify Gemfile has `gem 'sinatra'`
3. Run: `bundle install`
4. Use: `bundle exec ruby app.rb`

### 4. Route/URL Errors

**404 Not Found:**
| Cause | Solution |
|-------|----------|
| Typo in URL | Check spelling (case-sensitive) |
| Route not defined | Add route to code |
| Wrong HTTP method | Match GET/POST in route definition |

### 5. Server Errors

**Address Already in Use:**
1. Find other terminal with server running, Ctrl+C
2. Or kill process: `lsof -i :5000` then `kill <PID>`
3. Or use different port: `port=5001`

### 6. Function Errors

**Nothing Returned from Route:**
Routes must return something (HTML, template, redirect, JSON).
- Flask: `return render_template('index.html', ...)`
- Sinatra: `erb :index`

## Debugging Mindset
1. Read error message (file, line number)
2. Form hypothesis
3. Make one small change
4. Test
5. Learn from it

---

**End of Skill**
