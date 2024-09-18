from PIL import Image
import os

def convert_jfif_to_jpg(input_path, output_path):
    with Image.open(input_path) as im:
        rgb_im = im.convert('RGB')
        rgb_im.save(output_path, 'JPEG')

def convert_all_jfif_to_jpg():
    current_dir = os.getcwd()
    for filename in os.listdir(current_dir):
        if filename.lower().endswith('.jfif'):
            input_path = os.path.join(current_dir, filename)
            output_path = os.path.join(current_dir, os.path.splitext(filename)[0] + '.jpg')
            convert_jfif_to_jpg(input_path, output_path)
            print(f'已將 {filename} 轉換為 {os.path.basename(output_path)}')

if __name__ == '__main__':
    convert_all_jfif_to_jpg()
