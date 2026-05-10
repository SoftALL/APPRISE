# APPRISE

APPRISE is a lightweight GitHub companion repository for the APPRISE dataset. It contains code, documentation, prompts, personas, validation scripts, mining scripts, and small sample files so researchers can inspect and reuse the project without committing the full dataset payload to GitHub.

The full APPRISE dataset will be archived on Zenodo.
Reserved DOI: https://doi.org/10.5281/zenodo.20091031

Repository: https://github.com/SoftALL/APPRISE

## Dataset Summary

- 9,435 issues
- 13,579 synthetic reviews
- 73,984 contrastive triplets
- 400 audit samples
- 10 personas
- 4 apps: Brave Browser, Signal Android, AnkiDroid, K-9 Mail

## What Is Included Here

- `DATASHEET.md`: dataset documentation, intended uses, limitations, and maintenance notes.
- `personas.json`: persona definitions used for synthetic review generation.
- `prompts/generation_prompt_template.txt`: prompt template for generating persona-conditioned synthetic reviews.
- `scripts/validate_dataset.py`: validates expected dataset files and can generate small local samples.
- `scripts/mine_hard_negatives.py`: mines lexical hard-negative candidates for contrastive experiments.
- `scripts/compute_audit_stats.py`: summarizes audit labels and distributional fields.
- `data_sample/`: small sample files for repository inspection.

## Full Dataset Files Are Excluded

The full dataset files must not be committed to GitHub:

- `issues.jsonl`
- `reviews.jsonl`
- `triplets.tsv`
- `audit.csv`

These filenames are listed in `.gitignore`. Keep the full files local or obtain them from the archived dataset once Zenodo publication is finalized.

## Installation

```bash
python -m pip install -r requirements.txt
```

## Validation

From the repository root, validate local full dataset files with:

```bash
python scripts/validate_dataset.py --data-dir .
```

To regenerate the sample files from local full files, write the first 20 rows with:

```bash
python scripts/validate_dataset.py --data-dir . --write-samples data_sample --sample-size 20
```

## Audit Statistics

```bash
python scripts/compute_audit_stats.py --audit audit.csv
```

## Hard-Negative Mining

```bash
python scripts/mine_hard_negatives.py --issues issues.jsonl --reviews reviews.jsonl --output hard_negatives.tsv
```

## Citation

If you use APPRISE, cite the archived dataset once available on Zenodo and include the reserved DOI:

```text
https://doi.org/10.5281/zenodo.20091031
```

See `CITATION.cff` for repository citation metadata.

## Provenance

APPRISE includes attribution and provenance notes for BugRMSys-derived research context where applicable. Please preserve those notes in downstream reuse.

## License

This companion repository is released under the MIT License. Dataset-specific terms should be checked in the final Zenodo archive record when it is published.

## Contact

- Ogtay Hasanov, King Fahd University of Petroleum and Minerals, g202417720@kfupm.edu.sa
- Saad Ezzini, King Fahd University of Petroleum and Minerals, saad.ezzini@kfupm.edu.sa
