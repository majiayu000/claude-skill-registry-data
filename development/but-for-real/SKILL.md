---
name: but-for-real
description: "Force a skeptical second pass on your own work. Because 'it should work' has never once been true."
metadata:
  author: Shpigford
  version: "1.0"
---

Hey. Are you sure about that?

No really — are you *sure*? Because you just mass-produced a bunch of changes with the confidence of someone who's never been wrong, and statistically, you've been wrong plenty. So let's do this properly.

Go run `git diff` and actually read what you wrote. Not skim it. *Read* it. Then:

1. **Did you even do what was asked?** Not what you *decided* was asked. Go re-read the original request. If you added bonus features nobody wanted, rip them out. You're not being generous, you're being noisy.

2. **Pretend someone else wrote this.** Would you approve this PR? Or would you leave one of those comments? Look for:
   - Logic that's wrong but *looks* right (your specialty)
   - Edge cases you glossed over because handling them was boring
   - Imports you added and never used
   - That one variable you definitely named wrong
   - Copy-paste remnants from the thing you copied this from

3. **What did you forget?** Something. You always forget something.
   - Tests? Did you update them or just hope they still pass?
   - Other files that reference the thing you just changed?
   - That TODO you left "to come back to" (you weren't coming back)

4. **Run it.** Actually execute the code. Run the tests. Build the project. "I'm confident this works" is not a test suite. Your confidence is not a unit test.

5. **Fix what you find.** Don't just sheepishly list the issues — fix them. Then review the fixes. Yes, review the review. It's reviews all the way down.

If you actually went through all of that and found nothing: fine, say so. But we both know you found something.
