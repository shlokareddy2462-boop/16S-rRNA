import io
import pandas as pd
import streamlit as st
from classifier import classify_sequence, REQUIRED_COLUMNS

st.set_page_config(page_title="16S rRNA Taxonomic Classifier", page_icon="🧬")
st.title("16S rRNA Taxonomic Classifier")
st.write("Upload a labelled 16S reference CSV and enter a query DNA sequence.")

reference_file = st.file_uploader("Reference dataset (CSV)", type=["csv"])
sequence = st.text_area("Query 16S rRNA sequence", height=160, placeholder="Paste DNA sequence here (A, C, G, T, N)...")

if reference_file is not None:
    try:
        reference_df = pd.read_csv(reference_file)
        missing = [c for c in REQUIRED_COLUMNS if c not in reference_df.columns]
        if missing:
            st.error("The CSV is missing required columns: " + ", ".join(missing))
        else:
            st.success(f"Loaded {len(reference_df):,} reference records.")
            if st.button("Classify sequence"):
                try:
                    result = classify_sequence(sequence, reference_df)
                    st.subheader("Closest reference match")
                    st.metric("Sequence identity", f"{result['identity_percent']:.2f}%")
                    st.write(f"**Reference organism:** {result.get('Organism', '')}")
                    taxonomy = ["Kingdom", "Phylum", "Class", "Order", "Family", "Genus", "Species"]
                    st.table(pd.DataFrame({"Taxonomic rank": taxonomy,
                                           "Prediction": [result.get(c, "") for c in taxonomy]}))
                    st.caption("This is the closest match in the uploaded reference set, not a guaranteed species identification. Similarity is not a calibrated probability.")
                except ValueError as exc:
                    st.error(str(exc))
    except Exception as exc:
        st.error(f"Could not read the CSV: {exc}")
else:
    st.info("Upload taxonomy_test.csv or your completed reference dataset to begin.")
