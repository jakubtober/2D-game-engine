import default_game_settings


def tile_row_and_column(screen_coordinates: tuple) -> tuple:
    """
    Returns tile index as (tile_row, tile_column) giving screen display coordinates
    """
    tile_row = screen_coordinates[1] // default_game_settings.NODE_SIZE
    tile_column = screen_coordinates[0] // default_game_settings.NODE_SIZE
    tile = (tile_row, tile_column)
    return tile


def global_column_to_local_x_coordinate(map, global_node_column):
    """
    Returns x coordinate of global node column number
    """
    local_x_coordinate = (global_node_column * default_game_settings.NODE_SIZE) - (
        map.column_index_of_first_visible_tile * default_game_settings.NODE_SIZE
    )
    return local_x_coordinate


def global_row_to_local_y_coordinate(map, global_node_row):
    """
    Returns y coordinate of global node row number
    """
    local_y_coordinate = (global_node_row * default_game_settings.NODE_SIZE) - (
        map.row_index_of_first_visible_tile * default_game_settings.NODE_SIZE
    )
    return local_y_coordinate
