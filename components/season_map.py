import math


# Centre of the circular diagram in the original image.
# The image is 1816 x 1729 pixels.
IMAGE_CENTRE_X = 907
IMAGE_CENTRE_Y = 829

# Approximate radius of the seasonal ring.
IMAGE_RADIUS = 820


# Centre angle of each season.
#
# Because image coordinates increase downwards:
# 270° = top
# 330° = upper-right
# 30°  = lower-right
# 90°  = bottom
# 150° = lower-left
# 210° = upper-left

SEASON_ANGLES = {
    "Birak": 270,
    "Bunuru": 330,
    "Djeran": 30,
    "Makuru": 90,
    "Djilba": 150,
    "Kambarang": 210,
}


def calculate_angle(x, y, centre_x, centre_y):
    """Calculate the angle from the centre to a clicked point."""

    dx = x - centre_x
    dy = y - centre_y

    angle = math.degrees(math.atan2(dy, dx))

    return (angle + 360) % 360


def angular_difference(angle1, angle2):
    """Find the smallest distance between two angles."""

    difference = abs(angle1 - angle2)

    return min(difference, 360 - difference)


def get_season_from_click(
    x,
    y,
    displayed_width,
    displayed_height
):
    """
    Determine which season was clicked on the diagram.

    The image may be displayed smaller than its original size,
    so the original calibration coordinates are scaled first.
    """

    # Convert original-image coordinates to displayed-image coordinates.
    scale_x = displayed_width / 1816
    scale_y = displayed_height / 1729

    centre_x = IMAGE_CENTRE_X * scale_x
    centre_y = IMAGE_CENTRE_Y * scale_y

    radius_x = IMAGE_RADIUS * scale_x
    radius_y = IMAGE_RADIUS * scale_y

    # Work out the distance from the centre.
    dx = x - centre_x
    dy = y - centre_y

    normalised_distance = math.sqrt(
        (dx / radius_x) ** 2 +
        (dy / radius_y) ** 2
    )

    # Ignore the central information circle.
    if normalised_distance < 0.35:
        return None

    # Ignore clicks outside the seasonal artwork.
    if normalised_distance > 1.05:
        return None

    angle = calculate_angle(
        x,
        y,
        centre_x,
        centre_y
    )

    closest_season = None
    smallest_difference = float("inf")

    for season, season_angle in SEASON_ANGLES.items():

        difference = angular_difference(
            angle,
            season_angle
        )

        if difference < smallest_difference:
            smallest_difference = difference
            closest_season = season

    # Each season occupies approximately 60 degrees.
    if smallest_difference <= 30:
        return closest_season

    return None