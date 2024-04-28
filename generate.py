import cv2
import numpy as np
import json
import sys
import os
import random
import copy

# Main Developers : Pedro DA SILVA SOUSA & Gokhan KABAR
# Helper Developers : Erwann JOUVET & Mohammad GONS SAIB

IMPORTANT_LAYERS = ['floor', 'walls']
COLLISIONS_TILES = [403, 404, 477, 479, 428, 429, 578, 603, 685]
SUB_WALLS_FURNITURES = [187, 15]
SOLID_FURNITURES = [1688, 169]
FURNITURES = [1495]
MAX_FURNITURES_GENERATION = 10

# Initial values used to store datas
SUB_WALLS = []
NO_WALLS = []

# Future used in case of dynamically size map.
PIXEL_SCALE = 32

# Important walls :
# TOP-LEFT : 403
# TOP-RIGHT : 404
# VERTICAL : 479
# HORIZONTAL : 477
# BOTTOM-LEFT : 428
# BOTTOM-RIGHT : 429
# SUB-WALL TOP INSIDE : 578
# SUB-WALL BOTTOM INSIDE : 603
# SUB-WALL OUTSIDE : 685
# COLLIDE BLOCK : 2653
# VOID : 0

def generate_file(filepath):
    """
        Main method to generate JSON map data for Tiled by scanning an architectural plan of a house or apartment.

        Args:
            filepath (str): The file path to the architectural plan image.

        Raises:
            Exception: If an error occurs during map generation.
    """
    try :
        # Read the image
        image = cv2.imread(filepath)

        # Get the name of the image file (used for the map name)
        filename = os.path.splitext(os.path.basename(filepath))[0]

        # Detect black zones
        lower_black = np.array([0, 0, 0])
        upper_black = np.array([50, 50, 50])
        mask = cv2.inRange(image, lower_black, upper_black)

        # Dilation to improve detection
        kernel = np.ones((5, 5), np.uint8)
        dilated_mask = cv2.dilate(mask, kernel, iterations=1)

        # Inverting the mask to get the ground
        floor_mask = cv2.bitwise_not(dilated_mask)

        # Finding contours in the black area
        contours, _ = cv2.findContours(dilated_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Wall coordinates
        wall_coordinates = []

        for contour in contours:
            points = contour.reshape(-1, 2)
            wall_coordinates.extend(points.tolist())

        grid_width = 31
        grid_height = 21

        # Filling wall layer data
        with open('plan.tmj', 'r') as file:
            map_data = json.load(file)
            # Get furnitures and collisions layers.
            furnitures_layer = [layer for layer in map_data['layers'] if layer['name'] == 'furniture'][0]['layers'][0]
            collisions_layer = [layer for layer in map_data['layers'] if layer['name'] == 'collisions'][0]

            for layer in map_data['layers']:
                if layer['type'] == 'group':
                    if 'layers' in layer and layer['name'] in IMPORTANT_LAYERS:
                        for sub_layer in layer['layers']:
                            if layer['name'] == 'walls':
                                fill_base_data('walls', sub_layer, floor_mask, grid_width, grid_height)
                                wall_layer = sub_layer
                                # Start Clean Generation
                                clean_generation(sub_layer)
                            elif layer['name'] == 'floor':
                                fill_base_data('floor', sub_layer, floor_mask, grid_width, grid_height)
            generate_base_furnitures(furnitures_layer)
            # Generate collisions at the end after all generated objects and walls
            generate_collisions(collisions_layer, wall_layer, furnitures_layer)

            with open(f'{filename}.tmj', 'w') as file:
                json.dump(map_data, file)

        print('File updated successfully!')
    except Exception as error:
        print(f"Error while trying to generate map because : {error}")

def fill_base_data(data_type, layer, floor_mask, grid_width, grid_height):
    """
        Method to fill data for walls or floor layer based on the given data type.

        Args:
            data_type (str): Type of data to fill ('walls' or 'floor').
            layer (dict): The layer to fill with data.
            floor_mask (numpy.ndarray): Mask representing the floor area.
            grid_width (int): Width of the grid.
            grid_height (int): Height of the grid.
    """
    if data_type == "walls":
        # Recherche des pixels noirs dans le masque (sol)
        filtered_pixels = np.where(floor_mask == 0)
        tile_index = 477
    elif data_type == "floor":
        # Recherche des pixels blancs dans le masque (sol)
        filtered_pixels = np.where(floor_mask == 255)
        tile_index = 755


    for i in range(len(filtered_pixels[0])):
        x = filtered_pixels[1][i]
        y = filtered_pixels[0][i]

        # Convertir les coordonnées en indices de grille
        grid_x = int(x / (floor_mask.shape[1] / grid_width))
        grid_y = int(y / (floor_mask.shape[0] / grid_height))

        # Vérifier que les coordonnées sont dans les limites de la grille
        if 0 <= grid_x < grid_width and 0 <= grid_y < grid_height:
            # Calculer l'index correspondant dans la liste de données de la couche
            index = grid_y * grid_width + grid_x
            # Remplir la donnée pour le mur à l'index calculé
            layer['data'][index] = tile_index

def clean_generation(layer):
    """
        Method to clean wall tiles based on their position in the grid and the environment.

        Args:
            layer (dict): The layer containing wall data to clean.
    """
    for w in range(layer['width']):
        for h in range(layer['height']):
            index = h * layer['width'] + w
            tile_value = layer["data"][index]
            if tile_value == 477:
                cleaned_tile_value = 477
                # Start cleaning wall
                if index == 0:
                    # TOP LEFT OR CORNER
                    cleaned_tile_value = 403
                elif index == (0 * layer['width'] + layer['width'] - 1):
                    # TOP RIGHT OR CORNER
                    cleaned_tile_value = 404
                elif index == (layer['height'] * layer['width'] - layer['width']):
                    # BOTTOM LEFT OR CORNER
                    cleaned_tile_value = 428
                elif index == (layer['height'] * layer['width'] - 1):
                    # BOTTOM RIGHT OR CORNER
                    cleaned_tile_value = 429
                elif index in range(1, layer['width'] - 1) or index in range((layer['height'] * layer['width'] - layer['width']), (layer['height'] * layer['width'] + layer['width'] - 1)):
                    # VERTICAL WALLS
                    cleaned_tile_value = 479
                elif (index % layer['width'] == 0 and 1 <= index // layer['width'] < layer['height'] - 1) or ((index + 1) % layer['width'] == 0 and 1 <= index // layer['width'] < layer['height'] - 1):
                    # HORIZONTAL WALLS
                    cleaned_tile_value = 477
                layer["data"][index] = cleaned_tile_value

                # This part generate sub walls for the others walls.
                if cleaned_tile_value == 477:
                    # Check if there are no walls in the two bottom indices
                    bottom_indices = [index + layer['width'], index + (2 * layer['width'])]
                    if all(layer["data"][bottom_index] not in COLLISIONS_TILES for bottom_index in bottom_indices):
                        SUB_WALLS.extend(bottom_indices)
            else:
                # In case there is no walls, append index to this list in order to know where we can put any furnitures or other items.
                NO_WALLS.append(index)

    # This part generate subwalls for the top
    for w in range(layer['width']):
        # Check if there are no walls in the two bottom indices
        bottom_indices = [w + layer['width'], w + (2 * layer['width'])]
        if all(layer["data"][bottom_index] not in COLLISIONS_TILES for bottom_index in bottom_indices):
            SUB_WALLS.extend(bottom_indices)

    for index in SUB_WALLS:
        layer['data'][index] = 578

def generate_base_furnitures(furnitures_layer):
    """
    Method to generate furniture randomly in the map.

        Args:
            furnitures_layer (dict): The layer to fill with furniture data.
    """
    # Get index where we can put furniture without including sub walls.
    no_walls_indexes = [index for index in NO_WALLS if index not in SUB_WALLS]
    # Create a copy of SUB_WALLS array to ensure original array is unaffected in case we use for other functions
    sub_walls_indexes = copy.deepcopy(SUB_WALLS)
    
    # Iterate over a range of MAX_FURNITURES_GENERATION to generate furniture
    for iteration in range(MAX_FURNITURES_GENERATION):
        # Check if there are still available indices in no walls
        if no_walls_indexes:
            # Select a random index from no_walls_indexes
            index = random.choice(no_walls_indexes)
            # Remove the selected index from no_walls_indexes
            no_walls_indexes.remove(index)
            # Select a random furniture ID from the two furnitures list and place it in the selected index
            furnitures_layer['data'][index] = random.choice(FURNITURES + SOLID_FURNITURES)
        # Check if there are still available indices in sub walls
        if sub_walls_indexes:
            # Select a random index from sub_walls_indexes
            index = random.choice(sub_walls_indexes)
            # Remove the selected index from sub_walls_indexes
            sub_walls_indexes.remove(index)
            # Select a random furniture ID from the sub walls furnitures list and place it in the selected index
            furnitures_layer['data'][index] = random.choice(SUB_WALLS_FURNITURES)


def generate_collisions(collision_layer, wall_layer, furnitures_layer):
    """
        Method to generate collision data in the map based on walls and solid furniture.

        Args:
            collision_layer (dict): The layer to fill with collision data.
            wall_layer (dict): The layer containing wall data.
            furnitures_layer (dict): The layer containing furniture data.
    """
    for w in range(wall_layer['width']):
        for h in range(wall_layer['height']):
            if wall_layer['data'][h * wall_layer['width'] + w] in COLLISIONS_TILES or furnitures_layer['data'][h * wall_layer['width'] + w] in SOLID_FURNITURES:
                collision_layer['data'][h * collision_layer['width'] + w] = 3

if __name__ == "__main__":
    # Check if the correct number of command-line arguments is provided
    if len(sys.argv) != 2:
        print("Bad function call, example of call : python3 generation.py <file_path>")
        sys.exit(1)

    # Call the generate_file function with the file path argument
    generate_file(sys.argv[1])
