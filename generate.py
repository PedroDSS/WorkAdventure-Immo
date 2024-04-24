import cv2
import json

IMPORTANT_LAYERS = ['floor', 'walls']

def generate_file():
    #Traitement de l'image pour détecter les murs
    image = cv2.imread('plan.jpeg')
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, 50, 150)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    threshold_area = 1000
    filtered_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > threshold_area]
    
    # Coordonnées des murs
    wall_coordinates = []

    for contour in filtered_contours:
        points = contour.reshape(-1, 2)
        wall_coordinates.extend(points.tolist())
    
    grid_width = 31
    grid_height = 21

    #Remplissage des données du calque des murs
    with open('plan.tmj', 'r') as file:
        map_data = json.load(file)
        
        for layer in map_data['layers']:
            if layer['type'] == 'group':
                if 'layers' in layer and layer['name'] in IMPORTANT_LAYERS:
                    for sub_layer in layer['layers']:
                        if layer['name'] == 'walls':
                            fill_wall_data(sub_layer, wall_coordinates, grid_width, grid_height, image.shape[1], image.shape[0])
                        elif layer['name'] == 'floor':
                            fill_floor_data(sub_layer, grid_width, grid_height)

        with open('plan_updated.tmj', 'w') as file:
            json.dump(map_data, file)

    print('File updated successfully!')

def fill_wall_data(layer, wall_coordinates, grid_width, grid_height, image_width, image_height):
    pixel_width = image_width / grid_width
    pixel_height = image_height / grid_height
    
    for coord in wall_coordinates:
        #Convertir les coordonnées des murs en indices de grille
        grid_x = int(coord[0] / pixel_width)
        grid_y = int(coord[1] / pixel_height)
        
        #Vérifier que les coordonnées sont dans les limites de la grille
        if 0 <= grid_x < grid_width and 0 <= grid_y < grid_height:
            # Calculer l'index correspondant dans la liste de données de la couche
            index = grid_y * grid_width + grid_x
            # Remplir la donnée pour le mur à l'index calculé
            layer['data'][index] = 477

def fill_floor_data(layer, grid_width, grid_height):
    #Remplir toute la couche floor avec l'identifiant 755
    for i in range(grid_height * grid_width):
        if layer['data'][i] == 0:  # Si la case est vide (pas de mur),remplir avec du sol
            layer['data'][i] = 755
generate_file()
