# APPRISE

APPRISE is a lightweight GitHub companion repository for the APPRISE dataset. It contains code, documentation, prompts, persona definitions, validation scripts, mining scripts, and small sample files so researchers can inspect and reuse the project without committing the full dataset payload to GitHub.

The full APPRISE dataset is archived on Zenodo:

https://doi.org/10.5281/zenodo.20091031

Repository:

https://github.com/SoftALL/APPRISE

Hugging Face triplets dataset:

https://huggingface.co/datasets/SoftALL/APPRISE-triplets

## Dataset Summary

APPRISE contains:

- 9,435 GitHub issues
- 13,579 persona-conditioned synthetic reviews
- 73,984 contrastive triplets
- 400 audit samples
- 10 personas
- 4 Android applications: Brave Browser, Signal Android, AnkiDroid, and K-9 Mail

## What Is Included Here

This companion repository includes:

- `DATASHEET.md`: dataset documentation, intended uses, limitations, and maintenance notes
- `personas.json`: persona definitions used for synthetic review generation
- `prompts/generation_prompt_template.txt`: prompt template for generating persona-conditioned synthetic reviews
- `scripts/validate_dataset.py`: validation script for checking APPRISE dataset consistency
- `scripts/mine_hard_negatives.py`: script for mining lexical hard-negative candidates
- `scripts/compute_audit_stats.py`: script for summarizing audit scores and distributional fields
- `data_sample/`: small sample files for repository inspection
- `CITATION.cff`: citation metadata
- `LICENSE`: MIT License

## Full Dataset Files Are Excluded

The full dataset files must not be committed to GitHub:

- `issues.jsonl`
- `reviews.jsonl`
- `triplets.tsv`
- `audit.csv`
- `.zip` archives containing the full dataset

These filenames are listed in `.gitignore`. Keep the full files local or obtain them from the archived Zenodo dataset.

## Installation

```bash
python -m pip install -r requirements.txt
```

## Validation

After downloading the full APPRISE dataset from Zenodo, run validation by pointing the script to the folder containing the full files:

```bash
python scripts/validate_dataset.py --data-dir path/to/apprise/data
```

To regenerate small sample files from local full dataset files:

```bash
python scripts/validate_dataset.py --data-dir path/to/apprise/data --write-samples data_sample --sample-size 20
```

## Audit Statistics

```bash
python scripts/compute_audit_stats.py --audit path/to/apprise/data/audit.csv
```

## Hard-Negative Mining

```bash
python scripts/mine_hard_negatives.py \
  --issues path/to/apprise/data/issues.jsonl \
  --reviews path/to/apprise/data/reviews.jsonl \
  --output hard_negatives.tsv
```

## Citation

If you use APPRISE, cite the archived dataset and companion repository.

Zenodo DOI:

https://doi.org/10.5281/zenodo.20091031

See [`CITATION.cff`](CITATION.cff) for machine-readable citation metadata.

## Provenance

APPRISE includes attribution and provenance notes for BugRMSys-derived Brave Browser issue metadata. Please preserve those notes in downstream reuse.

## License

APPRISE is released under the MIT License. See [`LICENSE`](LICENSE).

## Contact

- Ogtay Hasanov, King Fahd University of Petroleum and Minerals  
  Email: g202417720@kfupm.edu.sa

- Saad Ezzini, King Fahd University of Petroleum and Minerals  
  Email: saad.ezzini@kfupm.edu.sa

