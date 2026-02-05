---
name: generate-questions
description: Generate high-quality bilingual programming quiz questions for Codle. Use this skill when creating new quiz questions that test deep understanding rather than rote memorization.
---

# Generate Programming Quiz Questions

Generate high-quality, bilingual (English/Chinese) programming quiz questions that test deep understanding rather than rote memorization.

## Quality Standards

### Core Philosophy: No Rote Learning, Deep Understanding Only
- **AVOID**: Pure definition questions (e.g., "What does CPU stand for?")
- **PREFER**: Principle/scenario questions (e.g., "Why should CSS animations use transform instead of width?")
- Questions should reveal underlying mechanisms, common pitfalls, or real-world production issues

### Question Categories to Cover
- JavaScript quirks and internals (type coercion, event loop, closures, `this` binding)
- CSS layout and performance (BFC, reflow/repaint, animation optimization)
- Browser APIs and Web Platform (DOM, Storage, Workers)
- Network and HTTP (caching, CORS, protocols)
- System Architecture (memory, CPU cache, concurrency)
- React/Vue/Framework internals
- Performance optimization patterns
- Security (XSS, CSRF, CSP)
- Algorithm fundamentals (from Nowcoder TOP101)

## External Reference: Nowcoder (牛客网) TOP101

When generating algorithm-related questions, reference the **Nowcoder Interview TOP101** question bank for inspiration and coverage.

### How to Access Nowcoder TOP101
1. **Web URL**: https://www.nowcoder.com/exam/oj?tab=算法篇&topicId=295
2. **Mobile URL**: https://m.nowcoder.com/mianshi/top
3. Use `WebFetch` tool to fetch specific problem details when needed

### TOP101 Categories (11 categories, 101 problems)
| Category | Count | Key Topics |
|----------|-------|------------|
| 链表 (Linked List) | 16 | 反转链表、K组翻转、合并有序链表、环形链表 |
| 二分查找/排序 (Binary Search) | 6 | 二分查找、二维数组查找、寻找峰值 |
| 二叉树 (Binary Tree) | 19 | 遍历、层序遍历、序列化、最近公共祖先 |
| 堆/栈/队列 (Heap/Stack/Queue) | 8 | 两栈实现队列、滑动窗口最大值、数据流中位数 |
| 哈希 (Hash) | 5 | 两数之和、三数之和 |
| 递归/回溯 (Recursion/Backtrack) | 7 | 岛屿数量、N皇后、括号生成 |
| 动态规划 (Dynamic Programming) | 21 | 斐波那契、正则匹配、买卖股票、背包问题 |
| 字符串 (String) | 4 | 字符串变形、大数加法 |
| 双指针 (Two Pointers) | 8 | 合并区间、接雨水 |
| 贪心算法 (Greedy) | 4 | 分糖果、跳跃游戏 |
| 模拟 (Simulation) | 3 | 螺旋矩阵、旋转数组 |

### Nowcoder "八股文" Categories (26 topics)
For non-algorithm interview questions:
- 网络模型、HTTP/HTTPS、TCP/UDP
- 操作系统、数据库基础、SQL、数据库锁/日志
- Java基础、Java多线程、JVM
- Redis、分布式、系统设计
- C++基础、C++高级、C++STL
- 前端开发、Vue、Spring、Mybatis
- 测试理论、测试用例设计、测试开发

### Fetching Specific Problems
To get detailed problem info, use WebFetch:
```
WebFetch URL: https://www.nowcoder.com/practice/[problem-id]
Example: https://www.nowcoder.com/practice/75e878df47f24fdc9dc3e400ec6058ca (反转链表)
```

### Difficulty Levels
- **Easy**: Basic concepts with common gotchas
- **Medium**: Requires understanding of underlying principles
- **Hard**: Edge cases, performance implications, or cross-cutting concerns

## Required Output Format

Generate questions as valid JSON array entries matching this schema:

```json
{
  "id": "category-topic-number",
  "category": {
    "en": "Category Name",
    "cn": "分类名称"
  },
  "difficulty": "Easy|Medium|Hard",
  "question": {
    "en": "Question text in English?",
    "cn": "中文题目描述？"
  },
  "options": {
    "en": ["Option A", "Option B", "Option C", "Option D"],
    "cn": ["选项 A", "选项 B", "选项 C", "选项 D"]
  },
  "answer": 0,
  "explanation": {
    "en": "Detailed explanation with why, production tips, and light humor.",
    "cn": "深入浅出的原理解析，包含原因、生产建议和适当幽默。"
  }
}
```

## Explanation Guidelines

Each explanation should include:
1. **WHY**: Why the correct answer is correct and why others are wrong
2. **PRO-TIP**: Real-world best practices or production advice
3. **HUMOR**: Light touch of humor to make learning enjoyable (optional but encouraged)

## Workflow

1. Read the current questions from `src/data/questions.json` to understand existing style and avoid duplicates
2. Generate new questions following the format above
3. Ensure bilingual consistency (术语翻译准确，如 Closure = 闭包)
4. Add the new questions to the JSON file
5. Test with `npm run dev` and use `?dev=1` to preview

## Example High-Quality Question

```json
{
  "id": "js-promise-1",
  "category": { "en": "JavaScript", "cn": "JavaScript" },
  "difficulty": "Hard",
  "question": {
    "en": "What is the output order of: `console.log(1); Promise.resolve().then(() => console.log(2)); console.log(3);`?",
    "cn": "`console.log(1); Promise.resolve().then(() => console.log(2)); console.log(3);` 的输出顺序是？"
  },
  "options": {
    "en": ["1, 2, 3", "1, 3, 2", "2, 1, 3", "3, 2, 1"],
    "cn": ["1, 2, 3", "1, 3, 2", "2, 1, 3", "3, 2, 1"]
  },
  "answer": 1,
  "explanation": {
    "en": "Microtask magic! Synchronous code runs first (1, 3), then the microtask queue is flushed (2). Promise.then() callbacks are microtasks, not macrotasks like setTimeout. Understanding this order is crucial for debugging async code - and for not pulling your hair out during interviews.",
    "cn": "微任务魔法！同步代码先执行（1, 3），然后清空微任务队列（2）。Promise.then() 回调是微任务，不像 setTimeout 那样是宏任务。理解这个顺序对调试异步代码至关重要——也能让你在面试中少掉几根头发。"
  }
}
```
