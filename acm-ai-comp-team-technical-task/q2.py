import numpy as np
from pathlib import Path

EXPECTED_FILE_NAMES = ['walls', 'terrain']
CSV_SUFFIX = '.csv'
CSV_DIR = 'csvs'

EMPTY, DRYWALL, WOOD, STONE = [0, 1, 2, 3]
MUD, DIRT, STONE, BEDROCK = [0, 1, 2, 3]

LEAK_ORIGIN = (6, 5)

def unstable_walls(walls: np.ndarray, terrain: np.ndarray, threshold: int = MUD) -> int:

    #------------------------------------------ YOUR CODE GOES HERE ------------------------------------------
    # Question 2a
    unstable = 0
    wall_shape = walls.shape
    terrain_shape = terrain.shape
    #empty wall and terrain
    if walls.size==0 or terrain.size==0:
        return 0
    #different sized inputs
    if (wall_shape[0]!=terrain_shape[0]) or (wall_shape[1]!=terrain_shape[1]):
        raise("Wall and terrain size mismatch")
    #iterate through wall and terrain arrays
    for i in range(0, wall_shape[0]):
        for j in range(0, wall_shape[1]):
            if (walls[i][j]!=EMPTY) and (terrain[i][j]==MUD or terrain[i][j]==DIRT):
                unstable += 1
    return unstable
    #---------------------------------------------------------------------------------------------------------

def leak_territory(walls: np.ndarray, leak_origin: tuple[int] = LEAK_ORIGIN) -> int:

    #------------------------------------------ YOUR CODE GOES HERE ------------------------------------------
    # Question 2b
    leak = 0
    wall_shape = walls.shape
    #empty walls
    if walls.size==0 :
        return 0
    #leak origin out of bounds
    if (leak_origin[0] not in range(0,wall_shape[0])) or (leak_origin[1] not in range(0,wall_shape[1])):
        raise("Leak origin out of bounds")
    #leak origin is a wall
    if walls[leak_origin[0], leak_origin[1]]!=EMPTY:
        return 0
    #keep track of visited vertices
    visited = np.full((wall_shape[0], wall_shape[1]), False)
    queue = []
    neighbors = [(-1,0), (1,0), (0,1), (0,-1)]
    queue.append(leak_origin)
    visited[leak_origin[0], leak_origin[1]] = True
    while queue:
        curr = queue.pop(0)
        leak += 1
        for n in neighbors:
            i = n[0]
            j = n[1]
            if (curr[0]+i in range(0,wall_shape[0])) and (curr[1]+j in range(0,wall_shape[1])):
                if (not visited[curr[0]+i, curr[1]+j]) and (walls[curr[0]+i][curr[1]+j]==EMPTY):
                    queue.append((curr[0]+i, curr[1]+j))
                    visited[curr[0]+i, curr[1]+j] = True
    return leak
    #---------------------------------------------------------------------------------------------------------

def validate_env(csv_dir: Path):
    
    if (not csv_dir.exists()):
        raise('csv dir does not exist')
    for expected_file in EXPECTED_FILE_NAMES:
        expected_file_path = csv_dir / (expected_file + CSV_SUFFIX)
        if (not expected_file_path.exists()):
            raise(f'{expected_file_path} does not exist')

def main():

    parent_dir = Path(__file__).parent.resolve()
    csv_dir = parent_dir / CSV_DIR
    validate_env(csv_dir)

    WALLS = np.loadtxt(CSV_DIR / Path('walls.csv'), delimiter=',').astype(np.int8)
    TERRAIN = np.loadtxt(CSV_DIR / Path('terrain.csv'), delimiter=',').astype(np.int8)

    # Q2a result printed here
    print('unstable_walls:', unstable_walls(np.copy(WALLS), np.copy(TERRAIN), threshold=DIRT))

    # Q2b result printed here
    print('leak_territory:', leak_territory(np.copy(WALLS), leak_origin=LEAK_ORIGIN))

if __name__ == '__main__':
    main()
