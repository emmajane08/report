from components.season_map import (
    calculate_angle,
    get_season_from_click
)


def test_top_of_circle_is_birak():

    season = get_season_from_click(
        450,
        100,
        900,
        600
    )

    assert season == "Birak"


def test_upper_left_is_kambarang():

    season = get_season_from_click(
        200,
        250,
        900,
        600
    )

    assert season == "Kambarang"


def test_upper_right_is_bunuru():

    season = get_season_from_click(
        700,
        250,
        900,
        600
    )

    assert season == "Bunuru"


def test_lower_right_is_djeran():

    season = get_season_from_click(
        700,
        500,
        900,
        600
    )

    assert season == "Djeran"


def test_lower_left_is_djilba():

    season = get_season_from_click(
        200,
        500,
        900,
        600
    )

    assert season == "Djilba"


def test_centre_is_not_a_season():

    season = get_season_from_click(
        450,
        300,
        900,
        600
    )

    assert season is None