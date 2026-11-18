# 16S rRNA Taxonomic Classifier

A student project that compares a query 16S rRNA DNA sequence against a labelled reference dataset and reports the closest local-alignment match with its taxonomy.

## What it does

1. Accepts a DNA sequence containing A, C, G, T and optionally N.
2. Locally aligns it against each reference sequence using Biopython.
3. Selects the reference with the highest alignment score.
4. Displays the reference organism, taxonomic ranks and sequence identity.

**Important limitations:** This is a reference-matching prototype, not a trained machine-learning model. The reported identity is not a probability or a guarantee of species-level identification. Closely related species can share very similar 16S sequences. Results depend on the quality and coverage of the reference dataset. Evaluate the classifier on held-out labelled sequences before making accuracy claims.

## Dataset format

The app expects a CSV with these columns:

- `Sequence`
- `Organism`
- `Kingdom`
- `Phylum`
- `Class`
- `Order`
- `Family`
- `Genus`
- `Species`

Your downloaded NCBI FASTA file alone does not contain all these taxonomy columns in the CSV. Use the taxonomy-enriched CSV produced by your data-preparation step (for example, `taxonomy_test.csv`) and check that it has all required columns before uploading it.

The reference dataset is not included in this GitHub repository. Add it through the app at runtime. Do not commit a large dataset unless you have checked its size and applicable database terms.

## Run locally

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd 16s-taxonomic-classifier
pip install -r requirements.txt
streamlit run app.py
```

Open the local URL printed by Streamlit, upload your reference CSV, paste a query sequence, and click **Classify sequence**.

## Run in Google Colab

Install dependencies:

```python
!pip install biopython pandas streamlit
```

For the web app, it is easiest to run this project locally or deploy it using Streamlit Community Cloud after pushing the files to GitHub.

## Project structure

```text
16s-taxonomic-classifier/
├── app.py
├── classifier.py
├── requirements.txt
├── README.md
├── .gitignore
└── tests/
    └── test_classifier.py
```

## Current project status

This repository contains the classifier and web interface code. It does not include the full reference database, and the code must be tested with a taxonomy-enriched dataset before reporting performance. The current implementation reports the closest match; it does not calculate validated accuracy metrics.
