---
name: run-eval
description: Run the LangSmith evaluation suite and display pass/fail results
disable-model-invocation: true
---

# /run-eval

## Steps

1. **Ensure Docker is running**
   ```bash
   docker compose ps
   ```
   If PostgreSQL is not up:
   ```bash
   docker compose up -d
   ```

2. **Run the evaluation suite**
   ```bash
   uv run dotenv -f .env run -- python scripts/run_eval.py
   ```
   Note the experiment name printed (e.g. `medox-<hash>`).

3. **Fetch and display results**
   Write the following script to `/tmp/check_eval.py` then run it:

   ```python
   from langsmith import Client

   client = Client()
   runs = list(client.list_runs(project_name='<experiment_name>', is_root=True))
   print(f'Eval cases: {len(runs)}')
   print()

   passed, failed = 0, 0
   for run in runs:
       fb = list(client.list_feedback(run_ids=[str(run.id)]))
       score = fb[0].score if fb else None
       comment = fb[0].comment if fb else ''
       prompt = (run.inputs or {}).get('prompt', '').strip()[:75]
       status = 'PASS' if score == 1 else 'FAIL'
       if score == 1:
           passed += 1
       else:
           failed += 1
       print(f'[{status}] {prompt}')
       if comment and comment != 'OK':
           print(f'       -> {comment}')

   print()
   print(f'Result: {passed} passed, {failed} failed out of {len(runs)}')
   ```

   Replace `<experiment_name>` with the value printed in step 2, then:
   ```bash
   uv run dotenv -f .env run -- python3 /tmp/check_eval.py
   ```

4. **Investigate failures**
   For any `[FAIL]`, read the comment and:
   - Check the relevant node/tool in `src/medox/agent/`
   - Check the evaluator logic in `scripts/run_eval.py`
   - Use `/add-eval-case` to add a regression case if a new edge case was found

5. **Report summary**
   Print the final `Result: N passed, M failed out of X` line to the user.
