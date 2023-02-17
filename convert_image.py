import os
from PIL import Image

# Chemin du dossier racine
root_dir = 'C:/Users/nirat/Documents/IA/ihm-ia/data5g_cleaned'

# Parcourir récursivement tous les fichiers et dossiers à partir du dossier racine
for root, dirs, files in os.walk(root_dir):
    for file in files:
        if file.endswith('.png'):
            # Chemin complet du fichier PNG
            png_file_path = os.path.join(root, file)

            # Charger l'image PNG avec PIL
            with Image.open(png_file_path) as img:
                print('Converting %s...' % png_file_path)
                # Convertir en JPG et enregistrer
                jpg_file_path = os.path.splitext(png_file_path)[0] + '.jpg'
                img.save(jpg_file_path, 'JPEG')

            # Supprimer le fichier PNG
            os.remove(png_file_path)