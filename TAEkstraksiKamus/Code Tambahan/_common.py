"""
_common.py
-----------
Shared utilities for the batch fix scripts.

Both fix_morphology_split_batch.py and fix_billex_headword_batch.py rely on:
  - the LookupIsFromIndonesia.csv table to decide which column holds the
    Indonesian side of each dictionary;
  - a consistent way to parse the dictionary ID out of a CSV filename like
    "4_Morphology.csv" or "18_Billex.csv".

These are kept here so both scripts stay thin and aligned with the rest of
the pipeline (notebooks 14, PostProcessing pyspellchecker, etc. all resolve
direction the same way).
"""

from __future__ import annotations

import os
import re
from pathlib import Path
from typing import Optional

import pandas as pd


LOOKUP_PATH = Path(
    "../Ekstraksi/12. Parallel Corpus - Spelling Checker/LookupIsFromIndonesia.csv"
)


# Order matters for the POS regex: multi-char tags must be tried before
# their single-char prefixes (vt before v, adv before a, pron before p).
POS_TAGS = ["adv", "pron", "num", "vt", "vi", "v", "a", "n", "p"]
POS_ALT = "|".join(POS_TAGS)
POS_SPLIT_RE = re.compile(rf"(?:^|\s)({POS_ALT})(?:\s|$)")


def parse_dict_id(filename: str) -> Optional[str]:
    """
    Extract the numeric dictionary ID from a filename such as
      '4_Morphology.csv' -> '4'
      '18_Billex.csv'    -> '18'
    Returns None if the ID cannot be parsed.
    """
    base = os.path.basename(str(filename))
    # Accept either '4_' or '4.' as separator; take the leading integer.
    m = re.match(r"^(\d+)[_.]", base)
    return m.group(1) if m else None


def load_direction_lookup(
    lookup_path: Path = LOOKUP_PATH,
) -> dict[str, int]:
    """
    Parse LookupIsFromIndonesia.csv into {dict_id: is_from_indonesia}.
    is_from_indonesia = 1 means the source language is Indonesian and the
    target is a regional language. 0 means the reverse.
    """
    if not lookup_path.exists():
        raise FileNotFoundError(
            f"LookupIsFromIndonesia.csv not found at {lookup_path}. "
            f"Run this script from the 'resourceGen/' or similar directory, "
            f"or update LOOKUP_PATH."
        )
    df = pd.read_csv(lookup_path)
    mapping: dict[str, int] = {}
    for _, row in df.iterrows():
        raw = str(row["kamus"])
        m = re.search(r"\d+", raw)
        if not m:
            continue
        mapping[m.group()] = int(row["is_from_indonesia"])
    return mapping


def direction_for(dict_id: str, mapping: dict[str, int]) -> Optional[int]:
    """
    Return 1 if dictionary is Indonesian->Regional, 0 if Regional->Indonesian,
    or None if the ID is not in the lookup (caller decides what to do).
    """
    return mapping.get(dict_id)


def roles_for_billex(direction: int) -> tuple[str, str]:
    """
    Billex columns are fixed: kata_asal = source, kata_tujuan = target.
    But WHICH side is Indonesian depends on direction.

    Returns (indonesian_column, regional_column).
    """
    if direction == 1:
        # Indonesian -> Regional: kata_asal is Indonesian
        return "kata_asal", "kata_tujuan"
    else:
        # Regional -> Indonesian: kata_tujuan is Indonesian
        return "kata_tujuan", "kata_asal"


def roles_for_morphology(direction: int) -> tuple[str, str]:
    """
    Morphology `form` column conventionally stores
      [source_form] [POS] [target_form]
    so returning (source_role, target_role) as 'ind'/'reg' strings lets the
    caller know which half of the split is Indonesian.
    """
    if direction == 1:
        return "ind", "reg"
    else:
        return "reg", "ind"
