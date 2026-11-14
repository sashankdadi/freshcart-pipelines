# freshcart-pipelines

Data Engineering assignment *From Git to Gold*: Git + CI, a FreshCart ELT pipeline on Snowflake, a Mage ML pipeline, and a RabbitMQ food-order stream.

```
freshcart-pipelines/
├── README.md
├── .gitignore                  # .env, *.pkl, *.csv, mage.log, __pycache__/ ...
├── requirements.txt            # what CI installs
├── elt/freshcart_elt.ipynb     # Part B (+ bonus)
├── iris_project/               # Part C (Mage project + iris_pipeline_colab.ipynb)
├── stream/                     # Part D (dispatcher.py, driver.py, stream_colab.ipynb, bonus_publisher.py)
├── tests/                      # pytest tests run by CI
├── docs/                       # RUNBOOK.md, REPORT_TEMPLATE.md
└── .github/workflows/ci.yml
```

## How the pieces fit together

```mermaid
flowchart LR
  A[Working folder] -->|git add / commit| B[Local Git]
  B -->|git push| C[GitHub remote]
  C -->|on every push| D[CI: pytest on prepare_data, validate_data, routing]
  subgraph ELT [Snowflake ELT]
    E[Sample APIs] --> F[raw files] --> G[bronze] --> H[silver + quarantine] --> I[gold.fct_orders]
  end
  subgraph ML [Mage ML pipeline]
    J[load_iris] --> K[validate_data] --> L[prepare_data] --> M[train_model + test gate]
    M --> N[save_results]
    M --> O[evaluate_model]
  end
  subgraph STREAM [RabbitMQ]
    P[dispatcher] -->|topic exchange| Q[driver queues]
    P -.bonus: order events.-> R[consumer: 1-minute batch]
  end
  C -. holds the code for .-> ELT
  C -. holds the code for .-> ML
  C -. holds the code for .-> STREAM
  R -->|write_landing + load_file| G
  I -. data for .-> ML
```

## Secrets
No passwords in Git. Snowflake credentials come from environment variables / Colab Secrets (`.env.example` lists the names); the broker URL comes from `AMQP_URL`.

See `docs/RUNBOOK.md` for the step-by-step order.
