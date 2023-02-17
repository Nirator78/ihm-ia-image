import os
import cv2
from tqdm import tqdm

# Chemins des dossiers source et destination
source_dir = r'C:\Users\nirat\Documents\IA\ihm-ia\data5g'
dest_dir = r'C:\Users\nirat\Documents\IA\ihm-ia\data5g_cleaned'

# Création du dossier de destination s'il n'existe pas déjà
if not os.path.exists(dest_dir):
    os.makedirs(dest_dir)

# Parcourt des sous-dossiers du dossier source
pbar = tqdm(os.listdir(source_dir))
for subdir in os.listdir(source_dir):
    pbar.set_description("Processing %s" % subdir)
    subdir_path = os.path.join(source_dir, subdir)
    
    # Vérification que l'élément en cours est bien un dossier
    if os.path.isdir(subdir_path):
        # Création du dossier de destination correspondant s'il n'existe pas déjà
        dest_subdir_path = os.path.join(dest_dir, subdir)
        if not os.path.exists(dest_subdir_path):
            os.makedirs(dest_subdir_path)
        
        # Parcourt des fichiers images du sous-dossier en cours
        for filename in os.listdir(subdir_path):
            file_path = os.path.join(subdir_path, filename)
            
            # Vérification que l'élément en cours est bien un fichier image
            if os.path.isfile(file_path) and filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                # Ouverture de l'image avec OpenCV et redimensionnement en 224x224 pixels
                img = cv2.imread(file_path)
                img_resized = cv2.resize(img, (224, 224))
                
                # Sauvegarde de l'image redimensionnée dans le dossier de destination
                dest_file_path = os.path.join(dest_subdir_path, filename)
                cv2.imwrite(dest_file_path, img_resized)
