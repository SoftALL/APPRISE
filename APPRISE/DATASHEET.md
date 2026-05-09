# Datasheet for APPRISE

## Motivation

APPRISE supports research on app-review synthesis, issue-to-review alignment, persona-conditioned generation, and contrastive retrieval or ranking. The companion repository intentionally excludes the full dataset payload while preserving documentation, scripts, prompts, personas, and small samples.

## Composition

APPRISE contains:

- 9,435 issues
- 13,579 synthetic reviews
- 73,984 contrastive triplets
- 400 audit samples
- 10 personas
- 4 apps: Brave Browser, Signal Android, AnkiDroid, K-9 Mail

The expected full dataset files are:

- `issues.jsonl`
- `reviews.jsonl`
- `triplets.tsv`
- `audit.csv`

## Collection and Generation Process

Issues are associated with four open-source apps. Synthetic reviews are generated from issue context using persona-conditioned prompts. Contrastive triplets pair issues, positive synthetic reviews, and hard negatives for retrieval and ranking experiments. Audit samples support manual or semi-automated quality checks.

## Recommended Uses

- Training and evaluating issue-review retrieval models.
- Studying persona-conditioned synthetic app-review generation.
- Auditing alignment between software issues and generated user-facing reviews.
- Evaluating hard-negative mining approaches for contrastive learning.

## Out-of-Scope Uses

APPRISE should not be used to infer real user sentiment, produce production app-store analytics, or identify individuals. Synthetic reviews should be clearly labeled as synthetic in downstream work.

## Distribution

The GitHub repository contains lightweight companion materials only. The full APPRISE dataset will be archived separately on Zenodo.

Reserved DOI: https://doi.org/10.5281/zenodo.20091031

## Maintenance

Validation scripts in `scripts/` provide schema-oriented checks and sample generation helpers. Dataset users should report inconsistencies through GitHub issues once the repository is published.

