def node_info(mouse_pos):
    node_row = mouse_pos[1] // 80
    node_column = mouse_pos[0] // 80
    node = (node_row, node_column)
    return node
