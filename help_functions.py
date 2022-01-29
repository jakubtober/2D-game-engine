import default_game_settings


def node_info(mouse_pos):
    """
    Returns node index as (node_row, node_column) giving screen display coordinates
    """
    node_row = mouse_pos[1] // default_game_settings.NODE_SIZE
    node_column = mouse_pos[0] // default_game_settings.NODE_SIZE
    node = (node_row, node_column)
    return node


def global_column_to_local_x_coordinate(map, global_node_column):
    """
    Returns x coordinate of global node column number
    """
    local_x_coordinate = (global_node_column * default_game_settings.NODE_SIZE) - (
        map.first_node_column * default_game_settings.NODE_SIZE
    )
    return local_x_coordinate


def global_row_to_local_y_coordinate(map, global_node_row):
    """
    Returns y coordinate of global node row number
    """
    local_y_coordinate = (global_node_row * default_game_settings.NODE_SIZE) - (
        map.first_node_row * default_game_settings.NODE_SIZE
    )
    return local_y_coordinate
