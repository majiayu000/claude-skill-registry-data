---
name: review-ios-test-results
description: Analyzes iOS test results from xcodebuild test runs. Use immediately after running xcodebuild test, when tests fail, when the user asks to check test results/failures, or when investigating test issues. Automatically locates the latest .xcresult file and presents detailed failure analysis with file locations.
allowed-tools: Bash, Read
---

# Review iOS Test Results

## When to Use

**ALWAYS use this skill when:**
- Just finished running `xcodebuild test` or `swift test`
- Tests failed and need to investigate failures
- User asks about test results, test status, or test failures
- User mentions "テスト結果", "失敗したテスト", "テストエラー"
- Need to analyze .xcresult files

**DO NOT manually parse xcodebuild output** - use this skill instead for structured analysis.

## Quick Start

```bash
# 1. Find latest .xcresult
# Note: <DerivedDataPath> is typically ~/Library/Developer/Xcode/DerivedData/
# but can be changed with xcodebuild's -derivedDataPath option
LATEST_RESULT=$(find <DerivedDataPath>/<ProjectName>-*/Logs/Test -name "*.xcresult" -type d -print0 2>/dev/null | xargs -0 ls -td | head -1)

# 2. Extract summary and detailed results
xcrun xcresulttool get test-results summary --path "${LATEST_RESULT}"
xcrun xcresulttool get test-results tests --path "${LATEST_RESULT}"
```

## Output Requirements

Present results in Japanese with:
1. **統計**: Total, passed, failed, skipped tests
2. **失敗したテスト**: Each failed test with error message and `file:line` reference
3. **次のステップ**: Actionable suggestions based on failure patterns

## Error Handling

- No .xcresult found → Guide user to run tests first
- Multiple failures in same suite → Highlight the pattern
- Assertion failures → Extract and show the assertion condition

## Examples

```
User: "テストを実行したけど失敗した"
→ Invoke this skill immediately

User: "最新のテスト結果を確認して"
→ Invoke this skill immediately

User: "xcodebuild test で何かエラーが出た"
→ Invoke this skill immediately
```
