# Report template (max 8 pages without appendix)
Name / Roll no: ______  Repo: https://github.com/sashankdadi/freshcart-pipelines

> Everything below must be in **your own words**. Predictions in B4 and D1 must be written *before* running the code; the viva checks this.

## Part A
**A1.** `git log --oneline` output (paste). Repo tree screenshot.

**A2.** Table (finish the last column in one sentence each, your own words). Facts to build from:
| Command | Where the change happens | What exactly happens? |
|---|---|---|
| `git init` | working folder (creates `.git`) | |
| `git add train.py` | working folder to staging area | |
| `git commit -m "msg"` | staging area to local repository | |
| `git remote add origin URL` | local config only | |
| `git push -u origin main` | local repo to remote | |
| `git pull origin main` | remote to local repo and working folder | |

Question: after `git commit`, can a teammate see your code on GitHub? (Think: which of the four boxes has changed?)

**A3.** Screenshots: green run, red run, fixing commit.

## Part B
**B1.** Screenshot of the B1 check.
**B2.** Trace of ORD-1003 (4 points in the assignment) and ORD-1005 vs ORD-1001 (name the table and the join condition).
**B3.** Reasons before / after, does gold change and why, does quarantine get a second row (point to the SQL).
**B4.** Prediction table (written before running):
| Quantity | Prediction | Actual |
|---|---|---|
| Rows for CUST-02 in dim.customers_scd2 | | |
| Tier used for ORD-1002 | | |
| Loyalty points for ORD-1002 | | |
| Total loyalty points in gold | | |
| Gold rows whose published_at changed | | |
Then 4 to 6 sentences on `row_hash`, `MERGE`, and why bronze grows by 8 rows each run.
**B5.** Check SQL, PROBLEM output, 3 to 4 sentences ELT vs ETL.

## Part C
**C1.** Block graph + `mage run ... --test` output.
**C2.** Table from the notebook + explanation of how a failing `@test` stops `save_results`.
**C3.** metadata.yaml, confusion matrix, metrics table, UI screenshot.
**C4.** Your block, its test, green CI.

## Part D
**D1.** Prediction table (before running):
| # | Routing key | Receiving queues |
|---|---|---|
| 1 | bangalore.koramangala.food | |
| 2 | bangalore.indiranagar.ride | |
| 3 | bangalore.whitefield.ride | |
| 4 | chennai.tnagar.food | |
| 5 | chennai.whitefield.ride | |
| 6 | bangalore.koramangala | |
**D2.** Console output proving a key from D1 reached exactly the queues you predicted.
**D3.** Logs of bad messages discarded; answer both questions (crash before ACK; `requeue=True` on an always-bad message).

## Part E
- Integration diagram (the mermaid in README.md is a starting point; redraw it in your own style).
- Half-page reflection: one thing that broke, how you found the cause, how you fixed it.
