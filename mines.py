import typing
import doctest

def dump(game):
    """
    Prints a human-readable version of a game (provided as a dictionary)
    """
    for key, val in sorted(game.items()):
        if isinstance(val, list) and val and isinstance(val[0], list):
            print(f"{key}:")
            for inner in val:
                print(f"    {inner}")
        else:
            print(f"{key}:", val)


# 2-D IMPLEMENTATION

def new_game_2d(num_rows, num_cols, bombs):
    """
    Start a new game.

    Return a game state dictionary, with the 'dimensions', 'state', 'board' and
    'hidden' fields adequately initialized.

    Parameters:
       num_rows (int): Number of rows
       num_cols (int): Number of columns
       bombs (list): List of bombs, given in (row, column) pairs, which are
                     tuples

    Returns:
       A game state dictionary

    >>> dump(new_game_2d(2, 4, [(0, 0), (1, 0), (1, 1)]))
    board:
        ['.', 3, 1, 0]
        ['.', '.', 1, 0]
    dimensions: (2, 4)
    hidden:
        [True, True, True, True]
        [True, True, True, True]
    squares_left: 5
    state: ongoing
    """

    return new_game_nd((num_rows, num_cols), bombs)


def dig_2d(game, row, col):
    """
    Reveal the cell at (row, col), and, in some cases, recursively reveal its
    neighboring squares.

    Update game['hidden'] to reveal (row, col).  Then, if (row, col) has no
    adjacent bombs (including diagonally), then recursively reveal (dig up) its
    eight neighbors.  Return an integer indicating how many new squares were
    revealed in total, including neighbors, and neighbors of neighbors, and so
    on.

    The state of the game should be changed to 'defeat' when at least one bomb
    is revealed on the board after digging (i.e. game['hidden'][bomb_location]
    == False), 'victory' when all safe squares (squares that do not contain a
    bomb) and no bombs are revealed, and 'ongoing' otherwise.

    Parameters:
       game (dict): Game state
       row (int): Where to start digging (row)
       col (int): Where to start digging (col)

    Returns:
       int: the number of new squares revealed

    >>> game = {'dimensions': (2, 4),
    ...         'board': [['.', 3, 1, 0],
    ...                   ['.', '.', 1, 0]],
    ...         'hidden': [[True, False, True, True],
    ...                  [True, True, True, True]],
    ...         'state': 'ongoing',
    ...         'squares_left': 4}
    >>> dig_2d(game, 0, 3)
    4
    >>> dump(game)
    board:
        ['.', 3, 1, 0]
        ['.', '.', 1, 0]
    dimensions: (2, 4)
    hidden:
        [True, False, False, False]
        [True, True, False, False]
    squares_left: 0
    state: victory

    >>> game = {'dimensions': [2, 4],
    ...         'board': [['.', 3, 1, 0],
    ...                   ['.', '.', 1, 0]],
    ...         'hidden': [[True, False, True, True],
    ...                  [True, True, True, True]],
    ...         'state': 'ongoing',
    ...         'squares_left': 4}
    >>> dig_2d(game, 0, 0)
    1
    >>> dump(game)
    board:
        ['.', 3, 1, 0]
        ['.', '.', 1, 0]
    dimensions: [2, 4]
    hidden:
        [False, False, True, True]
        [True, True, True, True]
    squares_left: 4
    state: defeat
    """
    return dig_nd(game,(row,col))

def render_2d_locations(game, xray=False):
    """
    Prepare a game for display.

    Returns a two-dimensional array (list of lists) of '_' (hidden squares),
    '.' (bombs), ' ' (empty squares), or '1', '2', etc. (squares neighboring
    bombs).  game['hidden'] indicates which squares should be hidden.  If
    xray is True (the default is False), game['hidden'] is ignored and all
    cells are shown.

    Parameters:
       game (dict): Game state
       xray (bool): Whether to reveal all tiles or just the that are not
                    game['hidden']

    Returns:
       A 2D array (list of lists)

    >>> render_2d_locations({'dimensions': (2, 4),
    ...         'state': 'ongoing',
    ...         'board': [['.', 3, 1, 0],
    ...                   ['.', '.', 1, 0]],
    ...         'hidden':  [[True, False, False, True],
    ...                   [True, True, False, True]],
    ...         'squares_left': 2}, False)        
    [['_', '3', '1', '_'], ['_', '_', '1', '_']]

    >>> render_2d_locations({'dimensions': (2, 4),
    ...         'state': 'ongoing',
    ...         'board': [['.', 3, 1, 0],
    ...                   ['.', '.', 1, 0]],
    ...         'hidden':  [[True, False, True, False],
    ...                   [True, True, True, False]],
    ...         'squares_left': 2}, True)      
    [['.', '3', '1', ' '], ['.', '.', '1', ' ']]
    """

    return render_nd(game, xray)


def render_2d_board(game, xray=False):
    """
    Render a game as ASCII art.

    Returns a string-based representation of argument 'game'.  Each tile of the
    game board should be rendered as in the function
        render_2d_locations(game)

    Parameters:
       game (dict): Game state
       xray (bool): Whether to reveal all tiles or just the ones allowed by
                    game['hidden']

    Returns:
       A string-based representation of game

    >>> render_2d_board({'dimensions': (2, 4),
    ...                  'state': 'ongoing',
    ...                  'board': [['.', 3, 1, 0],
    ...                            ['.', '.', 1, 0]],
    ...                  'hidden':  [[False, False, False, True],
    ...                            [True, True, False, True]],
    ...                  'squares_left': 2})                 
    '.31_\\n__1_'
    """
    string = ""
    updated = render_2d_locations(game, xray)
    for index, row in enumerate(updated):
        for val in row:
            string += val
        if index != len(game["board"]) - 1:
            string += "\n"
    
    return string

# N-D IMPLEMENTATION
def create_game_0(dimensions, bombs):
    """
    Creates a game with all 0's everywhere except for at bomb locations given
    the dimensions of the board, and a list of bomb locations as tuples.
    """
    board = []
    hidden = []

    if len(dimensions) == 1:
        board = [0] * dimensions[0]
        hidden = [True] * dimensions[0]
        for bomb in bombs:
            board[bomb[0]] = "."
    
    else:
        for i in range(dimensions[0]):
            smaller_dim = dimensions[1:]
            smaller_bombs = []
            for bomb in bombs:
                if bomb[0] == i:
                    smaller_bombs.append(bomb[1:])
            game = create_game_0(smaller_dim, smaller_bombs)
            board.append(game["board"])
            hidden.append(game["hidden"])
    
    total = 1
    for dim in dimensions:
        total = total * dim
    return {
        "dimensions": dimensions,
        "board": board,
        "hidden": hidden,
        "state": "ongoing",
        "squares_left": total-len(bombs)
    }

def new_game_nd(dimensions, bombs):
    """
    Start a new game.

    Return a game state dictionary, with the 'dimensions', 'state', 'board' and
    'hidden' fields adequately initialized.


    Args:
       dimensions (tuple): Dimensions of the board
       bombs (list): Bomb locations as a list of tuples, each an
                     N-dimensional coordinate

    Returns:
       A game state dictionary

    >>> g = new_game_nd((2, 4, 2), [(0, 0, 1), (1, 0, 0), (1, 1, 1)])
    >>> dump(g)
    board:
        [[3, '.'], [3, 3], [1, 1], [0, 0]]
        [['.', 3], [3, '.'], [1, 1], [0, 0]]
    dimensions: (2, 4, 2)
    hidden:
        [[True, True], [True, True], [True, True], [True, True]]
        [[True, True], [True, True], [True, True], [True, True]]
    squares_left: 13
    state: ongoing
    """
    
    game = create_game_0(dimensions, bombs) #create board of 0's
    update_bombs_nd(game["board"], bombs, dimensions)
    return game
    
def update_bombs_nd(board, bombs, dimensions):
    """
    Given a list of bomb locations (bombs), the dimensions of a board, and 
    a game board represented as a N-d list of all 0's except for bombs 
    represented by ".", updates the board with numbers indicating the number
    of nearby bombs. Changes the game board directly.

    """
    for bomb in bombs:
        neighbors = get_neighors_nd(dimensions, bomb)
        for neighbor in neighbors:    
            if neighbor not in bombs:
                update_pos(board, neighbor, 1) #value at bomb coords

def get_neighors_nd(dimensions, location):
    """
    Given the dimensions of a game, and a location on the board, returns a set
    of tuples indicating the locations of location's neighbors.
    """
    neighbors = set()
    if len(neighbors) == 0: #len(dimensions) == 1:
        if location[0] >= 1:
            neighbors.add((location[0]-1,))
        if location[0] <= dimensions[0]-2:
            neighbors.add((location[0]+1,))
        neighbors.add((location[0],))
        
    for index in range(1, len(location)): 
        new_neighbors = set()
        for neighbor in neighbors:
            if location[index] >= 1:
                new_neighbors.add(neighbor + (location[index]-1,))
            if location[index] <= dimensions[index]-2:
                new_neighbors.add(neighbor + (location[index]+1,))
            new_neighbors.add(neighbor + (location[index],))

        neighbors = new_neighbors
    return neighbors

def update_pos(board, coords, val):
    """
    Given a game board as a nested N-d list, and coordinates coords in the 
    form of a tuple, adds val to the current value at coords.
    """
    if len(coords) == 1:
        board[coords[0]] += val
    else:
        update_pos(board[coords[0]], coords[1:], val)

def get_val(board, coords):
    """
    Given a board and a tuple representing coordinates, returns the value
    at the coordinate.

    """
    if len(coords) == 1:
        return board[coords[0]]
    else:
        return get_val(board[coords[0]], coords[1:])
    
def set_val(board, coords, val):
    """
    Given a board and a tuple representing coordinates, sets the value
    at the coordinate to val.

    """
    if len(coords) == 1:
        board[coords[0]] = val
    else:
        set_val(board[coords[0]], coords[1:], val)

def dig_nd(game, coordinates):
    """
    Recursively dig up square at coords and neighboring squares.

    Update the hidden to reveal square at coords; then recursively reveal its
    neighbors, as long as coords does not contain and is not adjacent to a
    bomb.  Return a number indicating how many squares were revealed.  No
    action should be taken and 0 returned if the incoming state of the game
    is not 'ongoing'.

    The updated state is 'defeat' when at least one bomb is revealed on the
    board after digging, 'victory' when all safe squares (squares that do
    not contain a bomb) and no bombs are revealed, and 'ongoing' otherwise.

    Args:
       coordinates (tuple): Where to start digging

    Returns:
       int: number of squares revealed

    >>> g = {'dimensions': (2, 4, 2),
    ...      'board': [[[3, '.'], [3, 3], [1, 1], [0, 0]],
    ...                [['.', 3], [3, '.'], [1, 1], [0, 0]]],
    ...      'hidden': [[[True, True], [True, False], [True, True],
    ...                [True, True]],
    ...               [[True, True], [True, True], [True, True],
    ...                [True, True]]],
    ...      'state': 'ongoing',
    ...      'squares_left': 12}
    >>> dig_nd(g, (0, 3, 0))
    8
    >>> dump(g)
    board:
        [[3, '.'], [3, 3], [1, 1], [0, 0]]
        [['.', 3], [3, '.'], [1, 1], [0, 0]]
    dimensions: (2, 4, 2)
    hidden:
        [[True, True], [True, False], [False, False], [False, False]]
        [[True, True], [True, True], [False, False], [False, False]]
    squares_left: 4
    state: ongoing
    >>> g = {'dimensions': (2, 4, 2),
    ...      'board': [[[3, '.'], [3, 3], [1, 1], [0, 0]],
    ...                [['.', 3], [3, '.'], [1, 1], [0, 0]]],
    ...      'hidden': [[[True, True], [True, False], [True, True],
    ...                [True, True]],
    ...               [[True, True], [True, True], [True, True],
    ...                [True, True]]],
    ...      'state': 'ongoing',
    ...      'squares_left': 12}
    >>> dig_nd(g, (0, 0, 1))
    1
    >>> dump(g)
    board:
        [[3, '.'], [3, 3], [1, 1], [0, 0]]
        [['.', 3], [3, '.'], [1, 1], [0, 0]]
    dimensions: (2, 4, 2)
    hidden:
        [[True, False], [True, False], [True, True], [True, True]]
        [[True, True], [True, True], [True, True], [True, True]]
    squares_left: 12
    state: defeat
    """
    
    if game["state"] == "defeat" or game["state"] == "victory": #if game over
        return 0
    if not get_val(game["hidden"], coordinates): #if already uncovered
        return 0
    
    set_val(game["hidden"], coordinates, False) #uncover square
    if get_val(game["board"], coordinates) != ".":
        game["squares_left"] = game["squares_left"] - 1
    revealed = 1

    if get_val(game["board"], coordinates) == ".": #if uncover bomb
        game["state"] = "defeat"
        return 1

    if game["squares_left"] == 0:
        game["state"] = "victory"
        return 1
    
    if get_val(game["board"], coordinates) == 0: #if uncovered a 0
        neighbors = get_neighors_nd(game["dimensions"], coordinates)
        for neighbor in neighbors:
            revealed += dig_nd(game, neighbor)

    return revealed

def render_nd(game, xray=False):
    """
    Prepare the game for display.

    Returns an N-dimensional array (nested lists) of '_' (hidden squares), '.'
    (bombs), ' ' (empty squares), or '1', '2', etc. (squares neighboring
    bombs).  The game['hidden'] array indicates which squares should be
    hidden.  If xray is True (the default is False), the game['hidden'] array
    is ignored and all cells are shown.

    Args:
       xray (bool): Whether to reveal all tiles or just the ones allowed by
                    game['hidden']

    Returns:
       An n-dimensional array of strings (nested lists)

    >>> g = {'dimensions': (2, 4, 2),
    ...      'board': [[[3, '.'], [3, 3], [1, 1], [0, 0]],
    ...                [['.', 3], [3, '.'], [1, 1], [0, 0]]],
    ...      'hidden': [[[True, True], [True, False], [False, False],
    ...                [False, False]],
    ...               [[True, True], [True, True], [False, False],
    ...                [False, False]]],
    ...      'state': 'ongoing',
    ...      'squares_left': 4}
    >>> render_nd(g, False)
    [[['_', '_'], ['_', '3'], ['1', '1'], [' ', ' ']],
     [['_', '_'], ['_', '_'], ['1', '1'], [' ', ' ']]]

    >>> render_nd(g, True)
    [[['3', '.'], ['3', '3'], ['1', '1'], [' ', ' ']],
     [['.', '3'], ['3', '.'], ['1', '1'], [' ', ' ']]]
    """
    locations = []
    if len(game["dimensions"]) == 1:
        for coord in range(game["dimensions"][0]):
            if get_val(game["hidden"], (coord,)) == True and not xray:
                locations.append("_")
            else:
                if get_val(game["board"], (coord,)) == 0:
                    locations.append(" ")
                else:
                    locations.append(str(get_val(game["board"], (coord,))))
    else:
        for index in range(game["dimensions"][0]):
            new_game = {"dimensions": game["dimensions"][1:], 
                        "board": game["board"][index],
                        "hidden": game["hidden"][index], 
                        "state": "ongoing"}
            render = render_nd(new_game, xray)
            locations.append(render)
    return locations


if __name__ == "__main__":
    #example usage
    # g = new_game_nd((3,), [(1,)])
    # print(g)
    # dig_nd(g, (0,))
    # print(g)
    # dig_nd(g, (2,))
    # print(g)
    
    # g = new_game_nd((3,5), [(1,1), (2,2)])
    # print(g, "\n")
    # dig_nd(g, (0,4))
    # print(g)
    # print(render_nd(g))
    # dig_nd(g, (0,0))
    # dig_nd(g, (0,1))
    # dig_nd(g, (0,2))
    # dig_nd(g, (1,0))
    # dig_nd(g, (1,2))
    # dig_nd(g, (1,3))
    # dig_nd(g, (2,0))
    # dig_nd(g, (2,1))
    # dig_nd(g, (2,3))
    # print(g)
    # g = new_game_nd((3,3,2), [(1,2,0)])
    # print(g)
    # h = hidden_squares(g)
    # print(h)
    # update_game(g["board"], (0,1,1), 3)
    # print(g["board"])
    # update_game(g["board"], (0,1,1), 2)
    # print(g["board"])

    #doctest.run_docstring_examples(
    #    render_2d_locations,
    #    globals(),
    #    optionflags=_doctest_flags,
    #    verbose=False
    # )
