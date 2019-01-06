def node_info(mouse_pos):
    """
    Returns node index as (node_row, node_column) giving screen display coordinates
    """
    node_row = mouse_pos[1] // 80
    node_column = mouse_pos[0] // 80
    node = (node_row, node_column)
    return node

def global_column_to_local_x_coordinate(map, global_node_column):
    """
    Returns x coordinate of global node column number
    """
    local_x_coordinate = (global_node_column * 80) - (map.first_node_column * 80)
    return local_x_coordinate

def global_row_to_local_y_coordinate(map, global_node_row):
    """
    Returns y coordinate of global node row number
    """
    local_y_coordinate = (global_node_row * 80) - (map.first_node_row * 80)
    return local_y_coordinate
