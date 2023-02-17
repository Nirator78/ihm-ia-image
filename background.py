from rembg import remove
from PIL import Image
import easygui as eg
input_path = 'IMG_1016.jpg'
output_path = 'IMG_1016_background.jpg'
input = Image.open(input_path)
output = remove(input)
output.save(output_path)