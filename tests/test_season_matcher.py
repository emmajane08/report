import unittest

import pandas as pd

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
