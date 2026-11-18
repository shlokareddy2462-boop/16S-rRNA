import re
import pandas as pd
from Bio.Align import PairwiseAligner

REQUIRED_COLUMNS = [
    "Sequence", "Organism", "Kingdom", "Phylum", "Class",
    "Order", "Family", "Genus", "Species"
]

def clean_sequence(sequence: str) -> str:
    """Uppercase and validate a DNA sequence."""
    seq = re.sub(r"\s+", "", str(sequence)).upper()
    if not seq:
        raise ValueError("Please enter a DNA sequence.")
    invalid = set(seq) - set("ACGTN")
    if invalid:
        raise ValueError("Sequence contains invalid characters: " + ", ".join(sorted(invalid)))
    if len(seq) < 50:
        raise ValueError("Please enter a sequence of at least 50 bases.")
    return seq

def make_aligner():
    aligner = PairwiseAligner()
    aligner.mode = "local"
    aligner.match_score = 2
    aligner.mismatch_score = -1
    aligner.open_gap_score = -5
    aligner.extend_gap_score = -0.5
    return aligner

def classify_sequence(query: str, reference_df: pd.DataFrame) -> dict:
    """Return the closest local-alignment match from a labelled reference CSV."""
    query = clean_sequence(query)
    missing = [c for c in REQUIRED_COLUMNS if c not in reference_df.columns]
    if missing:
        raise ValueError("Reference CSV is missing columns: " + ", ".join(missing))

    refs = reference_df.dropna(subset=["Sequence"]).copy()
    if refs.empty:
        raise ValueError("The reference dataset has no sequences.")

    aligner = make_aligner()
    best_result = None
    best_score = float("-inf")

    for _, row in refs.iterrows():
        ref_seq = re.sub(r"\s+", "", str(row["Sequence"])).upper()
        if not ref_seq or set(ref_seq) - set("ACGTN"):
            continue
        alignment = aligner.align(query, ref_seq)[0]
        counts = alignment.counts()
        denominator = counts.identities + counts.mismatches + counts.gaps
        identity = (counts.identities / denominator * 100) if denominator else 0.0

        # Rank primarily by local alignment score; report identity over aligned columns.
        if alignment.score > best_score:
            best_score = alignment.score
            best_result = row.to_dict()
            best_result["identity_percent"] = identity
            best_result["alignment_score"] = float(alignment.score)

    if best_result is None:
        raise ValueError("No valid reference sequences were found.")
    return best_result
