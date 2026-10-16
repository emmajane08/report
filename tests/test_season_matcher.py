# Import unittest to define and run automated regression tests.
import unittest

# Import pandas to construct small test datasets as DataFrames.
import pandas as pd

from data_processing.data_loader import load_data

# Import the scoring function that these tests exercise.
from data_processing.season_matcher import calculate_season_scores


# Group related tests for the seasonal observation-matching function.
class SeasonMatcherTests(unittest.TestCase):
    # Verify a rainfall observation scores only the season whose text matches it.
    def test_rain_observation_only_matches_its_dataset_season(self):
        # Build a minimal dataset with different rainfall descriptions per season.
        data = pd.DataFrame(
            [
                {
                    "Season_Name": "Bunuru",
                    "Indicator_Name": "Rain",
                    "Description": "Little to no rainfall",
                },
                {
                    "Season_Name": "Birak",
                    "Indicator_Name": "Rain",
                    "Description": "Decreased rainfall",
                },
            ]
        )

        # Score the selected phrase against those dataset rows.
        scores = calculate_season_scores(data, ["Little or no rain"])

        # Confirm only Bunuru receives a matching-sign point.
        self.assertEqual(scores, {"Birak": 0, "Bunuru": 1})

    # Ensure duplicate matching rows do not score one observation more than once.
    def test_one_observation_counts_only_once_per_season(self):
        # Create two matching warm-temperature records in the same season.
        data = pd.DataFrame(
            [
                {
                    "Season_Name": "Birak",
                    "Indicator_Name": "Warm Temperatures",
                    "Description": "Warm weather starts to take hold",
                },
                {
                    "Season_Name": "Birak",
                    "Indicator_Name": "Warm Temperatures",
                    "Description": "Another warm period",
                },
            ]
        )

        # Score the single selected observation.
        scores = calculate_season_scores(data, ["Warm temperatures"])

        # Verify Birak receives exactly one point, not one per matching row.
        self.assertEqual(scores["Birak"], 1)

    # Check that case differences in user choices do not prevent matching.
    def test_lowercase_user_selection_matches_rule(self):
        # Build rows whose indicator names match two chosen observations.
        data = pd.DataFrame(
            [
                {
                    "Season_Name": "Birak",
                    "Indicator_Name": "Magpies",
                    "Description": "young ventures out, learning independence",
                },
                {
                    "Season_Name": "Bunuru",
                    "Indicator_Name": "Fledglings",
                    "Description": "venturing out of nests",
                },
            ]
        )

        # Score lowercase selections against the mixed-case dataset values.
        scores = calculate_season_scores(data, ["magpies", "fledglings"])

        # Confirm one sign matches in each corresponding season.
        self.assertEqual(scores["Birak"], 1)
        self.assertEqual(scores["Bunuru"], 1)

    # Ensure the matcher reports a clear error for an unmapped selection.
    def test_unknown_observation_is_rejected(self):
        # Supply one dataset row; the selected observation has no matching rule.
        data = pd.DataFrame(
            [{"Season_Name": "Birak", "Indicator_Name": "Rain", "Description": "Dry"}]
        )

        # Verify the scorer raises ValueError with its missing-rule explanation.
        with self.assertRaisesRegex(ValueError, "No matching rule"):
            calculate_season_scores(data, ["Unmapped option"])

    def test_multiple_valid_observations_produce_combined_scores(self):
        data = pd.DataFrame(
            [
                {
                    "Season_Name": "Birak",
                    "Indicator_Name": "Warm Temperatures",
                    "Description": "Warm weather starts to take hold",
                },
                {
                    "Season_Name": "Bunuru",
                    "Indicator_Name": "Magpies",
                    "Description": "Young magpies leave their nests",
                },
            ]
        )

        scores = calculate_season_scores(data, ["warm temperatures", "magpies"])

        self.assertEqual(scores, {"Birak": 1, "Bunuru": 1})

    def test_repeated_selections_do_not_double_count(self):
        data = pd.DataFrame(
            [
                {
                    "Season_Name": "Birak",
                    "Indicator_Name": "Warm Temperatures",
                    "Description": "Warm weather starts to take hold",
                }
            ]
        )

        scores = calculate_season_scores(
            data, ["warm temperatures", "warm temperatures"]
        )

        self.assertEqual(scores, {"Birak": 1})

    def test_extra_whitespace_and_mixed_case_are_normalised(self):
        data = pd.DataFrame(
            [
                {
                    "Season_Name": "Birak",
                    "Indicator_Name": "Warm Temperatures",
                    "Description": "Warm weather starts to take hold",
                }
            ]
        )

        scores = calculate_season_scores(data, ["  WARM   TEMPERATURES  "])

        self.assertEqual(scores, {"Birak": 1})

    def test_data_loads_with_clean_columns_and_text_values(self):
        data = load_data()

        self.assertFalse(data.empty)
        self.assertTrue(all(column == column.strip() for column in data.columns))

        text_columns = data.select_dtypes(include="object")
        self.assertFalse(text_columns.isna().any().any())
        self.assertTrue(
            all(
                value == value.strip()
                for column in text_columns
                for value in column
            )
        )
