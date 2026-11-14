#!/usr/bin/env bash
# Run once from the repo root after creating the empty GitHub repo.
set -e
git init -b main
git add .gitignore README.md requirements.txt requirements-extra.txt .env.example pytest.ini
git commit -m "Add repo skeleton, gitignore and requirements"
git remote add origin https://github.com/sashankdadi/freshcart-pipelines.git
git push -u origin main
echo "Now commit the other parts one at a time as you finish them (see docs/RUNBOOK.md)."
