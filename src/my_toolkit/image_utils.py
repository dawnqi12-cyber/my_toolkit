import os
from PIL import Image


def resize_images(input_folder, output_folder, size = (800, 600)):
 
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)

            with Image.open(input_path) as img:
                img_resized = img.resize(size, Image.LANCZOS)
                img_resized.save(output_path)

            print(f"已处理:{filename}")

if __name__ == "__main__":
    resize_images("./input","./output")