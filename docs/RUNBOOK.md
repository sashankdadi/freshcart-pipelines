# Runbook: what to do, in what order

## Step 0. Before anything (10 min)
1. **Change your Snowflake password** (you pasted it into a chat) and rotate the CloudAMQP password too (it is hard-coded in your class notebooks).
2. GitHub: create a **public** repo named `freshcart-pipelines` under `sashankdadi`. Do not tick "add README".
3. Create a GitHub **personal access token** (Settings > Developer settings > Tokens, `repo` scope). You will paste it into Colab, never into a file.
4. Colab: open the key icon (Secrets) and add `SNOWFLAKE_PASSWORD` (new password) and `AMQP_URL` if you use CloudAMQP.

## Step 1. Part A1: create the repo and first commits (on your laptop or in Colab)
```bash
unzip freshcart-pipelines.zip && cd freshcart-pipelines
git init -b main
git add .gitignore README.md requirements.txt requirements-extra.txt .env.example pytest.ini
git commit -m "Add repo skeleton, gitignore and requirements"
git remote add origin https://github.com/sashankdadi/freshcart-pipelines.git
git push -u origin main
```
Then commit the rest in separate pieces **as you actually finish each one** (graders check history):
| When | Command | Suggested message |
|---|---|---|
| A3 | `git add iris_project/data_loaders iris_project/transformers/prepare_data.py iris_project/transformers/train_model.py iris_project/data_exporters iris_project/__init__.py iris_project/*/__init__.py tests/test_prepare_data.py .github` | `Add Mage Iris blocks, prepare_data test and CI workflow` |
| A3 red run | edit `test_size=0.3` in prepare_data.py, commit, push, screenshot the red run | `Experiment: change test_size to 0.3 (CI should fail)` |
| A3 fix | revert to `0.2`, commit, push, screenshot the green run | `Fix test_size back to 0.2` |
| B | `git add elt` after B1 to B5 | `ELT: baseline run`, `ELT: unsupported_currency rule`, `ELT: SCD2 event + quality check` |
| C3/C4 | `git add iris_project tests/test_validate_data.py` | `Mage: evaluation branch`, `Mage: validate_data block with test` |
| D | `git add stream tests/test_routing.py` | `Stream: dispatcher and drivers`, `Stream: NACK handling` |
Check with `git log --oneline` (paste into the report). Aim for 8 or more commits.

> Do **not** squash everything into one commit at the end, and do not edit timestamps; the viva checks this.

## Step 2. Part A3: CI (15 min)
1. After the push in the table, open GitHub > Actions: the workflow `CI` should go **green**. Screenshot.
2. Change `test_size=0.2` to `0.3` in `iris_project/transformers/prepare_data.py`, commit, push: **red**. Screenshot. Revert and push: green again.

## Step 3. Part B: ELT on Snowflake (Colab, ~1.5 h)
Open `elt/freshcart_elt.ipynb` in Colab and run **top to bottom**:
1. Sections 1 to 2 (install, connect). Password comes from Colab Secrets or a prompt.
2. The **clean-slate cell** (`RESET_DB = True`) drops only the `FRESHCART` database so that B1 shows one run. Run it once.
3. Setup cell, then **one** `run_pipeline()`.
4. **B1 check cell** (screenshot: 8 / 6 / 2 / 4 / 4 / 7785 / 126, share rejected 25%).
5. Sections 9 and 10 (look in every layer; run again to see idempotency).
6. **B2** (trace queries), then write your trace in prose.
7. **B3**: run the "before" cell, then the patch + re-run cell, then the "after" cell.
8. **B4**: write your predictions into the report table **first**, then run the snapshot, add-event and compare cells.
9. **B5**: sixth check, fail-on-purpose run (screenshot the PROBLEM line), remove, re-run.
10. Save the notebook with outputs (File > Download .ipynb) into `elt/` and commit.

## Step 4. Part C: Mage (Colab, ~1 h)
Open `iris_project/iris_pipeline_colab.ipynb`. It installs Mage in a Python 3.12 venv, clones your repo, adds Mage's scaffold files, runs `pytest`, runs the pipeline (C1), loops over `max_depth` 1 to 5 and builds the C2 table, runs the branch (C3), starts the UI behind a Cloudflare tunnel (screenshot the graph), and commits from Colab. Draw the C1 graph by hand or in any tool.

## Step 5. Part D: RabbitMQ (Colab, ~1 h)
1. **Write your D1 table on paper first.** Question 6 (`bangalore.koramangala`) has only two words: think about how many words each pattern needs.
2. Open `stream/stream_colab.ipynb`. Run D2 (dispatcher + drivers, 2 minutes) and D3 (every 10th message bad). Screenshot the logs.
3. Compare your paper answers with `python stream/routing_check.py`.

## Step 6. Part E: report (about 2 h)
Use `docs/REPORT_TEMPLATE.md`. Export to PDF named `RollNo_Name_Pipelines.pdf` (max 8 pages without the screenshot appendix).

## Step 7. Bonus (optional, +10)
Bottom of the ELT notebook: publish with `stream/bonus_publisher.py`, consume for one minute, run twice, show gold totals unchanged.

## If something breaks
| Symptom | Likely cause / fix |
|---|---|
| `250001 Failed to connect` | Wrong account identifier. Yours is `DOGHCOE-VJ37135` (org-account form). Check the password. |
| `PUT` fails in Colab | Landing folder missing: re-run the `write_landing` cell first. |
| B1 shows bronze = 16 | The notebook ran twice. Set `RESET_DB = True` and start again. |
| Mage `ModuleNotFoundError: mage_ai` in CI | Not needed in CI: the blocks fall back to no-op decorators. Don't add `mage-ai` to `requirements.txt`. |
| Pytest cannot import `iris_project` | Run it from the repo root (`pytest.ini` sets `pythonpath = .`). |
| Driver gets nothing | Start drivers **before** the dispatcher; queues must be bound before messages are published. |
