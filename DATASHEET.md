# Datasheet for APPRISE

## Motivation

APPRISE supports research on app-review synthesis, issue-to-review alignment, persona-conditioned generation, and contrastive retrieval or ranking. This GitHub repository is intentionally lightweight: it preserves documentation, scripts, prompts, personas, and small samples while excluding the full dataset files.

## Composition

APPRISE contains:

- 9,435 issues
- 13,579 synthetic reviews
- 73,984 contrastive triplets
- 400 audit samples
- 10 personas
- 4 apps: Brave Browser, Signal Android, AnkiDroid, K-9 Mail

The full dataset is expected to use these files:

- `issues.jsonl`
- `reviews.jsonl`
- `triplets.tsv`
- `audit.csv`

The GitHub companion repository includes only small samples in `data_sample/`.

## Data Sources

The issue records are associated with four open-source applications: Brave Browser, Signal Android, AnkiDroid, and K-9 Mail. Synthetic reviews are generated from issue context with persona-conditioned prompts. Contrastive triplets connect issue records, positive synthetic reviews, and hard-negative examples for retrieval and ranking experiments.

## Generation Process

Synthetic reviews are produced from issue titles, issue bodies, app context, and persona descriptions. The prompt template asks for concise app-store-style review text and instructs the generator not to mention GitHub, issue trackers, pull requests, labels, or maintainers.

## Audit Data

The audit split contains 400 samples for quality inspection. The companion script `scripts/compute_audit_stats.py` can summarize available audit columns such as app, persona, label, verdict, quality, or alignment fields when present.

## Recommended Uses

- Training and evaluating issue-review retrieval models.
- Studying persona-conditioned synthetic app-review generation.
- Auditing alignment between software issues and generated user-facing reviews.
- Evaluating hard-negative mining approaches for contrastive learning.
- Reproducing lightweight validation and sampling workflows.

## Out-of-Scope Uses

APPRISE should not be used to infer real user sentiment, produce production app-store analytics, identify individuals, or represent synthetic reviews as authentic user reviews. Downstream users should clearly label synthetic review text as synthetic.

## Distribution

The full APPRISE dataset will be archived on Zenodo.
Reserved DOI: https://doi.org/10.5281/zenodo.20091031

GitHub repository: https://github.com/SoftALL/APPRISE

The GitHub repository must not contain the full dataset files:

- `issues.jsonl`
- `reviews.jsonl`
- `triplets.tsv`
- `audit.csv`

## Maintenance

Ogtay Hasanov and Saad Ezzini are the maintainers of APPRISE. Validation scripts in `scripts/` provide schema-oriented checks, sample generation helpers, hard-negative mining, and audit summaries. Dataset users should report documentation or script issues through GitHub issues once the repository is published.

## Contact

- g202417720@kfupm.edu.sa
- saad.ezzini@kfupm.edu.sa

## License

The APPRISE companion repository is released under the MIT License. Dataset-specific terms should be checked in the final Zenodo archive record when it is published.

## Provenance

APPRISE includes attribution and provenance notes for BugRMSys-derived research context where applicable. Please preserve those notes in downstream reuse.
