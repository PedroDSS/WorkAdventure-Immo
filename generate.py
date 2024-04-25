import cv2
import numpy as np
import json

IMPORTANT_LAYERS = ['floor', 'walls']

# Main Developers : Gokhan KABAR & Pedro DA SILVA SOUSA

# Important walls :
# TOP-LEFT : 403
# TOP-RIGHT : 404
# VERTICAL : 477
# HORIZONTAL : 479
# BOTTOM-LEFT : 428
# BOTTOM-RIGHT : 429
# SUB-WALL TOP INSIDE : 578
# SUB-WALL BOTTOM INSIDE : 603
# SUB-WALL OUTSIDE : 685
# VOID : 0

def generate_file():
    """
        Method used to generate json map for Tiled by scan on architect plan of house or apartment.
    """
    # Chargement de l'image
    image = cv2.imread('frame-diago.jpg')

    # Détection des zones rouges
    lower_red = np.array([0, 0, 100])
    upper_red = np.array([100, 100, 255])
    mask = cv2.inRange(image, lower_red, upper_red)

    # Dilation pour améliorer la détection
    kernel = np.ones((5, 5), np.uint8)
    dilated_mask = cv2.dilate(mask, kernel, iterations=1)

    # Inversion du masque pour obtenir le sol
    floor_mask = cv2.bitwise_not(dilated_mask)

    # Recherche des contours dans la zone rouge
    contours, _ = cv2.findContours(dilated_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Coordonnées des murs
    wall_coordinates = []

    for contour in contours:
        points = contour.reshape(-1, 2)
        wall_coordinates.extend(points.tolist())

    grid_width = 31
    grid_height = 21

    # Remplissage des données du calque des murs
    with open('plan.tmj', 'r') as file:
        map_data = json.load(file)

        for layer in map_data['layers']:
            if layer['type'] == 'group':
                if 'layers' in layer and layer['name'] in IMPORTANT_LAYERS:
                    for sub_layer in layer['layers']:
                        if layer['name'] == 'walls':
                            fill_wall_data(sub_layer, wall_coordinates, floor_mask, grid_width, grid_height, image.shape[1], image.shape[0])
                        elif layer['name'] == 'floor':
                            fill_floor_data(sub_layer, floor_mask, grid_width, grid_height)

        with open('plan_updated.tmj', 'w') as file:
            json.dump(map_data, file)

    print('File updated successfully!')

def fill_wall_data(layer, wall_coordinates, floor_mask, grid_width, grid_height, image_width, image_height):
    """
        Method used to generate walls
    """
    # Recherche des pixels noirs dans le masque (sol)
    black_pixels = np.where(floor_mask == 0)

    for i in range(len(black_pixels[0])):
        x = black_pixels[1][i]
        y = black_pixels[0][i]

        # Convertir les coordonnées en indices de grille
        grid_x = int(x / (floor_mask.shape[1] / grid_width))
        grid_y = int(y / (floor_mask.shape[0] / grid_height))

        # Vérifier que les coordonnées sont dans les limites de la grille
        if 0 <= grid_x < grid_width and 0 <= grid_y < grid_height:
            # Calculer l'index correspondant dans la liste de données de la couche
            index = grid_y * grid_width + grid_x
            # Remplir la donnée pour le mur à l'index calculé
            layer['data'][index] = 477


def fill_floor_data(layer, floor_mask, grid_width, grid_height):
    """
        Method used to generate floor
    """
    # Recherche des pixels blancs dans le masque (sol)
    white_pixels = np.where(floor_mask == 255)

    for i in range(len(white_pixels[0])):
        x = white_pixels[1][i]
        y = white_pixels[0][i]

        # Convertir les coordonnées en indices de grille
        grid_x = int(x / (floor_mask.shape[1] / grid_width))
        grid_y = int(y / (floor_mask.shape[0] / grid_height))

        # Vérifier que les coordonnées sont dans les limites de la grille
        if 0 <= grid_x < grid_width and 0 <= grid_y < grid_height:
            # Calculer l'index correspondant dans la liste de données de la couche
            index = grid_y * grid_width + grid_x
            # Remplir la donnée pour le sol à l'index calculé
            layer['data'][index] = 755


generate_file()
