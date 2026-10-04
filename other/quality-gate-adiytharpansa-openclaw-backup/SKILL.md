---
name: quality-gate
description: Final quality check before delivering any output. Use when you need to ensure accuracy, completeness, proper formatting, and high quality before something is sent to the user. This skill validates all outputs against a comprehensive checklist including accuracy, clarity, completeness, security, and professionalism.
---

# Quality Gate

**Quality controller** yang ensure everything perfect sebelum kamu lihat! ✅

## 🎯 Core Function

Skill ini **quality check** semua outputs:

1. **Accuracy Check** - Verify facts & correctness
2. **Completeness Check** - Ensure nothing missing
3. **Format Check** - Proper formatting & style
4. **Language Check** - Correct language usage
5. **Security Check** - No vulnerabilities or issues
6. **Professionalism Check** - Professional & polished

## ✅ Quality Checklist

### 1. Accuracy Check
```
✓ All facts verified
✓ No hallucinations or made-up info
✓ Correct code syntax & logic
✓ Proper function calls & parameters
✓ Valid API endpoints
✓ Current information (not outdated)
```

### 2. Completeness Check
```
✓ All user requirements addressed
✓ No missing sections
✓ Examples provided when needed
✓ Edge cases handled
✓ Error messages included
✓ Follow-up suggestions offered
```

### 3. Format Check
```
✓ Code properly formatted
✓ No markdown errors
✓ Proper indentation
✓ Consistent naming conventions
✓ Readable structure
✓ Professional appearance
```

### 4. Language Check
```
✓ Correct language (Bahasa Indonesia)
✓ No spelling or grammar errors
✓ Appropriate tone
✓ Clear & concise
✓ No unnecessary jargon
✓ Culturally appropriate
```

### 5. Security Check
```
✓ No hardcoded secrets
✓ No exposed credentials
✓ Input validation mentioned
✓ Error handling secure
✓ No injection vulnerabilities
✓ HTTPS recommended when applicable
```

### 6. Professionalism Check
```
✓ Professional tone
✓ No offensive content
✓ Respectful language
✓ Clear value proposition
✓ Actionable recommendations
✓ Well-organized presentation
```

## 🔧 Pre-Flight Check

Before delivering ANY output, run:

```
QUALITY GATE PRE-FLIGHT:
┌─────────────────────────────────────┐
│ ✓ Accuracy      [PASS/FAIL]         │
│ ✓ Completeness  [PASS/FAIL]         │
│ ✓ Format        [PASS/FAIL]         │
│ ✓ Language      [PASS/FAIL]         │
│ ✓ Security      [PASS/FAIL]         │
│ ✓ Professional  [PASS/FAIL]         │
└─────────────────────────────────────┘

ALL PASS → DELIVER
ANY FAIL → FIX & RECHECK
```

## 📝 Output Formats

### For Code:
```
CODE QUALITY CHECKLIST:
✓ Syntax valid
✓ No errors
✓ Best practices followed
✓ Comments where needed
✓ Error handling included
✓ Edge cases covered
✓ Tested/verifiable
```

### For Written Content:
```
CONTENT QUALITY CHECKLIST:
✓ Grammar correct
✓ Spelling correct
✓ Clear & readable
✓ Complete information
✓ No filler content
✓ Professional tone
✓ Proper structure
✓ Actionable conclusion
```

### For Analysis:
```
ANALYSIS QUALITY CHECKLIST:
✓ Data verified
✓ Logic sound
✓ No biases
✓ Multiple perspectives
✓ Clear conclusions
✓ Recommendations practical
✓ Sources cited
✓ Confidence level stated
```

## 🔍 Common Issues Caught

### Code Issues:
```
❌ Syntax errors → Fixed
❌ Missing semicolons → Added
❌ Undefined variables → Declared
❌ Unhandled errors → Added try-catch
❌ Missing imports → Added
❌ Security vulnerabilities → Patched
❌ Performance issues → Optimized
❌ No tests → Added test skeleton
```

### Content Issues:
```
❌ Factual errors → Corrected
❌ Missing information → Added
❌ Unclear explanations → Rewritten
❌ Wrong language → Fixed
❌ Grammar errors → Fixed
❌ Incomplete answer → Completed
❌ Too verbose → Condensed
❌ Too brief → Expanded
```

## 🛠️ Commands

### `/quality-check`
Run quality check on current output:
```
QUALITY GATE CHECK

Output: [current output]

Checking...
✓ Accuracy: PASS
✓ Completeness: PASS
✓ Format: PASS
✓ Language: PASS
✓ Security: PASS
✓ Professionalism: PASS

All checks passed! Ready to deliver.
```

### `/quality-check <output>`
Check specific output:
```
QUALITY GATE CHECK

[output provided]

Status: ⚠️ Issues Found

Issues:
1. Missing: [issue 1]
2. Correction: [issue 2]

Fixes applied: [list]
Re-check: PASS
```

### `/quality-mode <level>`
Set quality level:
```
SET QUALITY MODE:

Standard → Basic checks only
High → Full checklist
Maximum → Extra thorough checks
```

### `/quality-report`
Show quality report:
```
QUALITY REPORT

Checks performed today: [X]
Passed: [Y]
Issues found & fixed: [Z]

Quality Score: [XX%]
Common issues: [list]
```

### `/quality-prefer`
Set quality preferences:
```
QUALITY PREFERENCES:

Code: [level]
Content: [level]
Analysis: [level]
Format: [your preference]
Language: [your preference]

Updated. All outputs will follow these preferences.
```

## 🎯 Example Workflow

### Scenario 1: Code Generation
```
USER: "Create a login function"

GENERATION:
[Code generated]

QUALITY GATE CHECK:
✓ Syntax: Valid ✓
✓ Security: Passwords hashed ✓
✓ Error handling: Included ✓
✓ Comments: Added ✓
✓ Testing: Test skeleton included ✓

RESULT: ✅ Production-ready code delivered
```

### Scenario 2: Content Creation
```
USER: "Write a blog post about AI"

GENERATION:
[Blog post created]

QUALITY GATE CHECK:
✓ Accuracy: All facts verified ✓
✓ Language: Bahasa Indonesia correct ✓
✓ Structure: Clear headings ✓
✓ Completeness: All points covered ✓
✓ Tone: Professional ✓
✓ Grammar: No errors ✓

RESULT: ✅ High-quality blog post delivered
```

### Scenario 3: Complex Analysis
```
USER: "Analyze this project codebase"

GENERATION:
[Analysis created]

QUALITY GATE CHECK:
✓ Facts: All verified ✓
✓ Analysis: No bias ✓
✓ Recommendations: Actionable ✓
✓ Sources: Cited ✓
✓ Confidence: Level stated ✓
✓ Completeness: All aspects covered ✓

RESULT: ✅ Comprehensive analysis delivered
```

## 📊 Quality Metrics

```
QUALITY METRICS (Today):

Total outputs: [X]
Passed first check: [XX%]
Issues found: [Y]
Issues fixed: [Y]
Quality score: [ZZ%]

Common improvements:
- Added error handling: [N]
- Fixed grammar: [N]
- Added examples: [N]
- Enhanced security: [N]
- Improved formatting: [N]
```

## 🔄 Continuous Improvement

### Learning from Checks:
```
Pattern: Often miss error handling
Action: Add error handling reminder

Pattern: Sometimes skip security check
Action: Strengthen security validation

Pattern: Formatting issues in code blocks
Action: Pre-format code before delivering
```

### Quality Evolution:
```
Week 1: Quality score 85%
Week 2: Quality score 92%
Week 3: Quality score 95%
Week 4: Quality score 98%

Trend: ↗️ Improving
```

## 💡 Best Practices

### DO:
- ✅ Run quality check on EVERY output
- ✅ Be thorough in checks
- ✅ Fix issues before delivering
- ✅ Document quality decisions
- ✅ Learn from common issues

### DON'T:
- ❌ Skip quality checks
- ❌ Be too lenient
- ❌ Assume first attempt is perfect
- ❌ Ignore user preferences
- ❌ Compromise on security

---

**Goal:** Never deliver anything less than PERFECT! ✨

**Status:** Quality Gate ACTIVE  
**Quality Standard:** MAXIMUM  
**Commitment:** Flawless delivery
