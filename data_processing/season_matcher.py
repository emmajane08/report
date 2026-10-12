"""Match user-selected seasonal signs against the calendar dataset."""

from collections.abc import Iterable, Mapping


def _normalise(value: object) -> str:
    """Normalise text for case-insensitive, whitespace-tolerant matching."""
    return " ".join(str(value).replace("\u00a0", " ").casefold().split())


MATCH_RULES = {
    "fledglings": [{"name_terms": ("fledgling", "fledgings"), "description_terms": ("nest", "parents")}],
    "magpies": [{"name_terms": ("magpie", "koolbardi"), "description_terms": ("swooping", "protecting", "babies", "young")}],
    "black swans": [{"name_terms": ("black swan", "mali"), "description_terms": ("nest", "breed", "moulting")}],
    "bird eggs": [{"name_terms": ("bird eggs", "eggs")}],
    "dugites": [{"name_terms": ("dugite", "dobitj")}],
    "goannas": [{"name_terms": ("goanna", "goana", "yandi")}],
    "frogs": [{"name_terms": ("frog", "kooyal"), "description_terms": ("metamorphosis", "breeding", "winter choruses")}],
    "kangaroos": [{"name_terms": ("kangaroo", "yonga", "yongar")}],
    "quendas": [{"name_terms": ("quenda", "bandicoot")}],
    "mullet": [{"name_terms": ("mullet")}],
    "bream": [{"name_terms": ("bream")}],
    "marron": [{"name_terms": ("marron")}],
    "crabs": [{"name_terms": ("crab", "crabs")}],
    "orchids": [{"name_terms": ("orchid", "orchids")}],
    "banksia": [{"name_terms": ("banksia",)}],
    "paperbark tree": [{"name_terms": ("paperbark tree",)}],
    "moodjar (christmas tree)": [{"name_terms": ("moodjar", "christmas tree")}],
    "grass trees": [{"name_terms": ("grass tree", "grass trees", "balgas")}],
    "southern sea breeze": [{"name_terms": ("sea breeze", "south-west")},],
    "morning easterly winds": [{"name_terms": ("easterly winds", "morning easterly winds")},],
    "decreased rainfall": [{"name_terms": ("rain",), "description_terms": ("decreased rainfall",)}],
    "little to no rainfall": [{"name_terms": ("rain",), "description_terms": ("little to no rainfall",)}],
    "little or no rain": [{"name_terms": ("rain",), "description_terms": ("little to no rainfall",)}],
    "some days are cool and rainy": [{"name_terms": ("rain",), "description_terms": ("some days are cool and rainy",)}],
    "some days are rainy": [{"name_terms": ("rain",), "description_terms": ("some days are cool and rainy",)}],
    "wettest time of the year": [{"name_terms": ("rain",), "description_terms": ("wettest time of the year",)}],
    "wettest time of year": [{"name_terms": ("rain",), "description_terms": ("wettest time of the year",)}],
    "inland water supplies replenished": [{"name_terms": ("rain",), "description_terms": ("replenishes inland water supplies",)}],
    "rain replenishes water supplies": [{"name_terms": ("rain",), "description_terms": ("replenishes inland water supplies",)}],
    "warm temperatures": [{"name_terms": ("warm temperatures", "warm sunny days", "hottest time of the year")}],
    "cool temperatures": [{"name_terms": ("cool temperatures", "nights are cool", "mornings are dewy")}],
    "cold temperatures": [{"name_terms": ("cold temperatures", "coldest time of the year", "cold days and nights")}],
    "transitional temperatures": [{"name_terms": ("transitional temperatures", "warming trend")}],
    "clear skies": [{"name_terms": ("sky", "clear", "sunny"), "description_terms": ("clear", "bright")}],
    "clustered clouds": [{"name_terms": ("cloud", "cloudy", "clustered"), "description_terms": ("cloudy", "overcast")}],
    "afternoon sea breeze (south-west)": [{"name_terms": ("sea breeze", "south-west", "afternoon sea breeze")},],
    "hot easterly winds": [{"name_terms": ("easterly winds", "hot easterly winds")},],
    "light southerly breeze (south east-south west)": [{"name_terms": ("southerly", "breeze")},],
    "frequent storms": [{"name_terms": ("storm", "storms", "thunderstorm"), "description_terms": ("storm", "stormy")}],
    "windy days": [{"name_terms": ("wind", "winds", "gusty")},],
    "days are very dry": [{"name_terms": ("dry", "temperature"), "description_terms": ("dry", "harsh temperatures")}],
    "fire danger is high": [{"name_terms": ("fire", "dry"), "description_terms": ("fire", "dry") }],
    "hottest time of the year": [{"name_terms": ("warm temperatures", "hottest")},],
    "nights are cool": [{"name_terms": ("cool temperatures", "cool nights")},],
    "mornings are dewy": [{"name_terms": ("dew", "dewy")},],
    "coldest time of the year": [{"name_terms": ("cold temperatures", "coldest")},],
    "cold days and nights": [{"name_terms": ("cold temperatures", "cold days and nights")},],
    "warm sunny days": [{"name_terms": ("warm temperatures", "sunny")},],
    "warming trend": [{"name_terms": ("warming", "warm")},],
    "less cold fronts": [{"name_terms": ("cold", "front")},],
    "longer dry periods": [{"name_terms": ("dry", "dry periods")},],
    "mullet": [{"name_terms": ("mullet",)}],
    "bream": [{"name_terms": ("bream",)}],
    "marron": [{"name_terms": ("marron",)}],
    "crabs": [{"name_terms": ("crab", "crabs")}],
    "mussels": [{"name_terms": ("mussel", "mussels")}],
    "abalone": [{"name_terms": ("abalone",)}],
    "herring": [{"name_terms": ("herring",)}],
    "salmon": [{"name_terms": ("salmon",)}],
    "freshwater fish": [{"name_terms": ("fish", "freshwater")},],
    "whales migrating": [{"name_terms": ("whale", "whales", "migrating")}],
    "insects abundants with flowers": [{"name_terms": ("insect", "flower")},],
    "fly ants": [{"name_terms": ("fly ants", "fly ant", "ants")}],
    "yams": [{"name_terms": ("yam", "yams")}],
    "rottnest island daisy": [{"name_terms": ("daisy", "rottnest")},],
    "kangaroo paw": [{"name_terms": ("kangaroo paw", "paw")}],
    "orchids": [{"name_terms": ("orchid", "orchids")}],
    "berries": [{"name_terms": ("berry", "berries")}],
    "lillies": [{"name_terms": ("lily", "lillies")}],
    "djilba flowers": [{"name_terms": ("djilba", "flower")}],
    "purple flags": [{"name_terms": ("purple flag", "flags")}],
    "bluberry lilies": [{"name_terms": ("blueberry lily", "bluberry", "lily")}],
    "summer flame": [{"name_terms": ("summer flame", "flame")}],
    "white flowers": [{"name_terms": ("white flowers", "flower")}],
    "red flowers": [{"name_terms": ("red flowers", "flower")}],
    "samphire": [{"name_terms": ("samphire", "milya")}],
    "zamia": [{"name_terms": ("zamia",)}],
    "rainbow bee-eaters": [{"name_terms": ("rainbow bee-eater", "bee-eater", "bee eater")}],
    "wattle birds swooping": [{"name_terms": ("wattle bird", "wattle birds"), "description_terms": ("swooping", "protecting", "babies", "young")}],
    "willie wagtails swooping": [{"name_terms": ("wagtail", "willie wagtail"), "description_terms": ("swooping", "protecting", "babies", "young")}],
    "magpies swooping": [{"name_terms": ("magpie", "koolbardi"), "description_terms": ("swooping", "protecting", "babies", "young")}],
    "bronzewing pigeons": [{"name_terms": ("bronzewing", "pigeon")}],
    "emus": [{"name_terms": ("emu", "emus")}],
    "ravens": [{"name_terms": ("raven", "ravens")}],
    "crows": [{"name_terms": ("crow", "crows")}],
    "wedge-tailed shearwaters": [{"name_terms": ("shearwater", "wedge-tailed shearwater")}],
    "king skinks": [{"name_terms": ("skink", "king skink")}],
    "snakes": [{"name_terms": ("snake", "snakes", "waugal")}],
    "reptile skins": [{"name_terms": ("skin", "skins", "reptile")}],
    "tadpoles becoming frogs": [{"name_terms": ("tadpole", "frog")}],
    "tortoises": [{"name_terms": ("tortoise", "tortoises")}],
    "moaning frogs": [{"name_terms": ("moaning frog", "moaning frogs")}],
    "turtles": [{"name_terms": ("turtle", "turtles")}],
    "motorbike frogs": [{"name_terms": ("motorbike frog", "motorbike frogs")}],
    "possums": [{"name_terms": ("possum", "possums")}],
    "gilgies": [{"name_terms": ("gilgie", "gilgies")}],
    "seeds": [{"name_terms": ("seed", "seeds", "seed pod", "germinating")}],
    "fruit": [{"name_terms": ("fruit", "fruits", "berries")}],
    "insects": [{"name_terms": ("insect", "bee", "butterfly", "dragonfly", "fly")}],
    "winds west and south": [{"name_terms": ("wind", "winds", "southerly")},],
    "frequent gales": [{"name_terms": ("gale", "wind")},],
    "harsh costal winds": [{"name_terms": ("wind", "harsh", "coastal")},],
    "waterways swelled": [{"name_terms": ("rain", "waterways", "swelled")}],
    "catchments start to fill": [{"name_terms": ("rain", "catchment", "fill")}],
    "second rains": [{"name_terms": ("rain", "second")},],
    "snow on peaks of ranges": [{"name_terms": ("rain", "snow", "range")},],
    "morning easterly winds": [{"name_terms": ("easterly", "wind")},],
    "sea breeze": [{"name_terms": ("sea breeze", "afternoon sea breeze")},],
}

MATCH_RULES_BY_KEY = { _normalise(key): value for key, value in MATCH_RULES.items() }

MATCH_ALIASES = {
    "little or no rain": "little to no rainfall",
    "some days are rainy": "some days are cool and rainy",
    "wettest time of year": "wettest time of the year",
    "rain replenishes water supplies": "inland water supplies replenished",
}


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
    """Score each season by the number of selected signs it contains."""
    selected = list(dict.fromkeys(selected_observations))
    canonical_selected = []
    for item in selected:
        observation = _normalise(item)
        canonical_selected.append(MATCH_ALIASES.get(observation, observation))

    unknown = set(canonical_selected).difference(MATCH_RULES_BY_KEY)
    if unknown:
        raise ValueError(f"No matching rule is defined for: {', '.join(sorted(unknown))}")

    season_rows = {
        season: rows.to_dict("records")
        for season, rows in data.groupby("Season_Name")
    }
    scores = {season: 0 for season in sorted(season_rows)}

    for observation in canonical_selected:
        for season, rows in season_rows.items():
            if any(
                _matches_clause(row, clause)
                for row in rows
                for clause in MATCH_RULES_BY_KEY[observation]
            ):
                scores[season] += 1

    return scores
