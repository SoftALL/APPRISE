# APPRISE

APPRISE is a companion repository for the APPRISE dataset and tooling. It contains lightweight code, documentation, prompts, personas, validation scripts, mining scripts, and small sample-file slots intended for GitHub distribution.

The full APPRISE dataset will be archived on Zenodo.
Reserved DOI: https://doi.org/10.5281/zenodo.20091031

## Dataset Summary

- 9,435 issues
- 13,579 synthetic reviews
- 73,984 contrastive triplets
- 400 audit samples
- 10 personas
- 4 apps: Brave Browser, Signal Android, AnkiDroid, K-9 Mail

## Repository Contents

- `DATASHEET.md`: dataset documentation and intended-use notes.
- `personas.json`: the ten persona definitions used for review generation.
- `prompts/generation_prompt_template.txt`: prompt template for synthetic review generation.
- `scripts/validate_dataset.py`: validates APPRISE file structure and basic record consistency.
- `scripts/mine_hard_negatives.py`: mines hard-negative candidates from issue/review text.
- `scripts/compute_audit_stats.py`: summarizes audit labels and per-app/persona distributions.
- `data_sample/`: small sample files for quick inspection.

## Full Dataset Files

Do not commit the full dataset files to this repository:

- `issues.jsonl`
- `reviews.jsonl`
- `triplets.tsv`
- `audit.csv`

These names are explicitly ignored in `.gitignore`.

## Quick Start

```bash
python -m pip install -r requirements.txt
python scripts/validate_dataset.py --data-dir .
python scripts/compute_audit_stats.py --audit audit.csv
python scripts/mine_hard_negatives.py --issues issues.jsonl --reviews reviews.jsonl --output hard_negatives.tsv
```

## Sample Files

The files in `data_sample/` are intended to contain the first 20 rows from the local full dataset files. If the full files are available locally, regenerate the samples from the repository root with:

```bash
python scripts/validate_dataset.py --data-dir . --write-samples data_sample --sample-size 20
```

