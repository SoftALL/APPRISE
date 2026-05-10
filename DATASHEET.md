# Datasheet for APPRISE

This datasheet documents the APPRISE companion repository and its relationship to the full archived dataset.

## Motivation

APPRISE supports research on app-review synthesis, review-to-issue alignment, persona-conditioned generation, and contrastive retrieval or ranking. The GitHub repository is intentionally lightweight: it preserves documentation, scripts, prompts, persona definitions, and small sample files while excluding the full dataset files.

The full APPRISE dataset is archived on Zenodo:

https://doi.org/10.5281/zenodo.20091031

## Composition

APPRISE contains:

- 9,435 GitHub issues
- 13,579 persona-conditioned synthetic reviews
- 73,984 contrastive triplets
- 400 audit samples
- 10 personas
- 4 Android applications: Brave Browser, Signal Android, AnkiDroid, and K-9 Mail

The full dataset consists of the following main files:

- `issues.jsonl`
- `reviews.jsonl`
- `triplets.tsv`
- `audit.csv`

The GitHub companion repository includes only small sample files under `data_sample/`.

## Data Sources

APPRISE is built from issue records associated with four open-source Android applications: Brave Browser, Signal Android, AnkiDroid, and K-9 Mail.

Brave Browser issue metadata is derived from BugRMSys and is redistributed with attribution. Signal Android, AnkiDroid, and K-9 Mail issue metadata was collected from public GitHub issue trackers.

Synthetic reviews are generated from issue context using persona-conditioned prompts. Contrastive triplets connect synthetic reviews, their positive source issues, and BM25-mined hard-negative issues for retrieval and ranking experiments.

## Generation Process

Synthetic reviews are produced from issue titles, issue bodies, application context, and persona descriptions. The prompt template asks for concise app-store-style review text and instructs the generator not to mention GitHub, issue trackers, pull requests, labels, or maintainers.

The released generation setup uses `Mistral-7B-Instruct-v0.3` through Hugging Face Transformers with 4-bit NF4 quantization.

## Audit Data

The audit split contains 400 samples for quality inspection. Each audited item is scored using a source-alignment rubric that estimates how faithfully a synthetic review preserves the meaning of its source issue.

The companion script `scripts/compute_audit_stats.py` can summarize available audit fields such as application, persona, score, and alignment-related columns.

## Recommended Uses

APPRISE may be used for:

- Training and evaluating review-to-issue retrieval models
- Studying persona-conditioned synthetic app-review generation
- Auditing alignment between software issues and generated user-facing reviews
- Evaluating hard-negative mining approaches for contrastive learning
- Reproducing lightweight validation and sampling workflows
- Studying software-engineering artifact retrieval

## Out-of-Scope Uses

APPRISE should not be used to infer real user sentiment, produce production app-store analytics, identify individuals, or represent synthetic reviews as authentic user reviews.

Downstream users should clearly label APPRISE review text as synthetic.

## Distribution

The full APPRISE dataset is archived on Zenodo:

https://doi.org/10.5281/zenodo.20091031

The companion GitHub repository is available at:

https://github.com/SoftALL/APPRISE

The GitHub repository must not contain the full dataset files:

- `issues.jsonl`
- `reviews.jsonl`
- `triplets.tsv`
- `audit.csv`
- `.zip` archives containing the full dataset

Only small sample files are included under `data_sample/`.

## Hugging Face

The APPRISE contrastive triplets are also made available through the SoftALL Hugging Face organization for convenient model-training access:

https://huggingface.co/datasets/SoftALL/APPRISE-triplets

## Maintenance

Ogtay Hasanov and Saad Ezzini are the maintainers of APPRISE.

Validation scripts in `scripts/` provide schema-oriented checks, sample inspection utilities, hard-negative mining support, and audit summaries. Dataset users should report documentation or script issues through the GitHub issue tracker.

## Contact

- Ogtay Hasanov — g202417720@kfupm.edu.sa
- Saad Ezzini — saad.ezzini@kfupm.edu.sa

## License

APPRISE is released under the MIT License. See [`LICENSE`](LICENSE).

## Provenance

APPRISE includes attribution and provenance notes for BugRMSys-derived Brave Browser issue metadata. Downstream users should preserve these attribution notes when reusing or redistributing APPRISE-derived materials.

