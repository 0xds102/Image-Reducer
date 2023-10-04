from PIL import Image
import os
import logging

logging.basicConfig(level=logging.INFO)

Image.MAX_IMAGE_PIXELS = None

def get_image_size(image_path):
    size_bytes = os.path.getsize(image_path)
    return size_bytes / (1024 * 1024)

def reduce_image_size(image_path, output_path, max_size_mb):
    try:
        max_size_bytes = max_size_mb * 1024 * 1024
        with Image.open(image_path) as img:
            img.save(output_path)
            current_size = os.path.getsize(output_path)
            
            scale_factor = 0.95
            while current_size > max_size_bytes:
                new_size = (int(img.width * scale_factor), int(img.height * scale_factor))
                img = img.resize(new_size, Image.LANCZOS)
                img.save(output_path)
                current_size = os.path.getsize(output_path)
                scale_factor *= 0.95
                
                logging.info(f"Resized to {new_size[0]}x{new_size[1]}. Current size: {current_size / (1024 * 1024):.2f}MB")
        
        logging.info(f"Final image size: {current_size / (1024 * 1024):.2f}MB")
    except Exception as e:
        logging.error(f"Error while reducing image size: {e}")

if __name__ == "__main__":
    input_path = 'YOUR_IMAGE.jpg' # YOUR IMAGE NAME
    output_path = 'reduced_image.jpg'
    
    current_size = get_image_size(input_path)
    print(f"Current image size: {current_size:.2f} MB")
    
    desired_size_mb = float(input("What size would you like the image reduced to in MB? "))
    
    logging.info(f"Reducing image size to below {desired_size_mb}MB")
    reduce_image_size(input_path, output_path, desired_size_mb)
