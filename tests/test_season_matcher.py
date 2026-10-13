import unittest

import pandas as pd

from data_processing.data_loader import load_data
from data_processing.season_matcher import calculate_season_scores


class SeasonMatcherTests(unittest.TestCase):
    def test_rain_observation_only_matches_its_dataset_season(self):
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

        scores = calculate_season_scores(data, ["Little or no rain"])

        self.assertEqual(scores, {"Birak": 0, "Bunuru": 1})

    def test_one_observation_counts_only_once_per_season(self):
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

        scores = calculate_season_scores(data, ["Warm temperatures"])

        self.assertEqual(scores["Birak"], 1)

    def test_lowercase_user_selection_matches_rule(self):
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

        scores = calculate_season_scores(data, ["magpies", "fledglings"])

        self.assertEqual(scores["Birak"], 1)
        self.assertEqual(scores["Bunuru"], 1)

    def test_unknown_observation_is_rejected(self):
        data = pd.DataFrame(
            [{"Season_Name": "Birak", "Indicator_Name": "Rain", "Description": "Dry"}]
        )

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
