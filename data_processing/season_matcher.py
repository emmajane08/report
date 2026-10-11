"""Match user-selected seasonal signs against the calendar dataset."""

from collections.abc import Iterable, Mapping


# Each option is a list of alternatives. A clause matches when all its
# populated criteria match; any clause can make the option match a row.
MATCH_RULES = {
    "Little or no rain": [
        {"name_terms": ("rain",), "description_terms": ("little to no rainfall",)},
    ],
    "Decreased rainfall": [
        {"name_terms": ("rain",), "description_terms": ("decreased rainfall",)},
    ],
    "Some days are rainy": [
        {"name_terms": ("rain",), "description_terms": ("some days are cool and rainy",)},
    ],
    "Wettest time of year": [
        {"name_terms": ("rain",), "description_terms": ("wettest time of the year",)},
    ],
    "Rain replenishes water supplies": [
        {"name_terms": ("rain",), "description_terms": ("replenishes inland water supplies",)},
    ],
    "Rain is decreasing": [
        {"name_terms": ("rain",), "description_terms": ("rain decreasing",)},
    ],
    "Warm temperatures": [
        {"name_terms": ("warm temperatures",)},
    ],
    "Cool temperatures": [
        {"name_terms": ("cool temperatures",)},
    ],
    "Cold temperatures": [
        {
            "name_terms": ("temperature", "cool temperatures"),
            "description_terms": ("coldest time of the year", "cold days and nights"),
        },
    ],
    "Transitional temperatures": [
        {
            "name_terms": ("temperature",),
            "description_terms": (
                "transitional time of the year",
                "intermediate season",
                "transformational time of year",
            ),
        },
    ],
    "Moodjar (Christmas tree)": [
        {"name_terms": ("moodjar (christmas tree)",)},
    ],
    "Paperbark tree": [
        {"name_terms": ("paperbark tree",)},
    ],
    "Banksia": [
        {"name_terms": ("banksia",)},
    ],
    "Acacias": [
        {"name_terms": ("acacia",)},
    ],
    "Grass trees": [
        {"name_terms": ("grass trees",)},
    ],
    "Flowers": [
        {"name_terms": ("flower", "blossom")},
    ],
    "Orchids": [
        {"name_terms": ("orchid",)},
    ],
    "Frogs": [
        {"name_terms": ("frog",)},
    ],
    "Reptiles": [
        {"name_terms": ("reptile", "snake", "goanna", "goana", "dugite")},
    ],
    "Kangaroos": [
        {"name_terms": ("kangaroo", "yonga", "yongar")},
    ],
    "Young animals": [
        {"name_terms": ("young", "fledgling", "baby birds", "maturing", "adolescent animals")},
    ],
    "Birds breeding": [
        {
            "name_terms": ("black swan", "mali"),
            "description_terms": ("nest", "breed", "moulting"),
        },
        {
            "name_terms": ("magpie", "koolbardi", "wagtail", "wattle bird"),
            "description_terms": ("swooping", "nest-bound", "protecting", "babies", "young"),
        },
        {"name_terms": ("bird eggs",)},
        {
            "name_terms": ("fledgings",),
            "description_terms": ("nest", "parents"),
        },
    ],
}


def _normalise(value: object) -> str:
    """Normalise text for case-insensitive, whitespace-tolerant matching."""
    return " ".join(str(value).replace("\u00a0", " ").casefold().split())


def _matches_clause(row: Mapping[str, object], clause: Mapping[str, tuple[str, ...]]) -> bool:
    indicator_name = _normalise(row["Indicator_Name"])
    description = _normalise(row["Description"])

    name_terms = clause.get("name_terms", ())
    description_terms = clause.get("description_terms", ())

    return (
        (not name_terms or any(_normalise(term) in indicator_name for term in name_terms))
        and (
            not description_terms
            or any(_normalise(term) in description for term in description_terms)
        )
    )


def calculate_season_scores(data, selected_observations: Iterable[str]) -> dict[str, int]:
    """Score each season by the number of selected signs it contains.

    Each selected sign contributes at most one point to a season, even if
    several dataset rows support that sign.
    """
    selected = list(dict.fromkeys(selected_observations))
    unknown = set(selected).difference(MATCH_RULES)
    if unknown:
        raise ValueError(f"No matching rule is defined for: {', '.join(sorted(unknown))}")

    scores = {
        season: 0
        for season in sorted(data["Season_Name"].dropna().unique())
    }

    for observation in selected:
        clauses = MATCH_RULES[observation]
        for season, season_rows in data.groupby("Season_Name"):
            if any(
                any(_matches_clause(row, clause) for clause in clauses)
                for row in season_rows.to_dict("records")
            ):
                scores[season] += 1

    return scores
