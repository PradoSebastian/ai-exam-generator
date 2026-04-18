
import os

import google.genai.types as types

class ImageUtil:
    @staticmethod
    def get_mime_type(file_path: str) -> str:
        """Helper method to determine the MIME type based on the file extension."""
        extension = file_path.split('.')[-1].lower()
        mime_types = {
            'jpg': 'image/jpeg',
            'jpeg': 'image/jpeg',
            'png': 'image/png',
            'gif': 'image/gif',
            'bmp': 'image/bmp',
            'tiff': 'image/tiff',
            'webp': 'image/webp'
        }
        return mime_types.get(extension, 'image/jpeg')  # Default to JPEG if unknown

    @staticmethod
    def read_image(image_path: str) -> tuple[str, types.Part]:
        """Reads an image from the specified path and returns its bytes."""
        with open(image_path, 'rb') as img_file:
            return image_path, types.Part(
                inline_data=types.Blob(
                    mime_type=ImageUtil.get_mime_type(image_path),
                    data=img_file.read()
                )
            )

    @staticmethod
    def read_images_from_folder(folder_path: str) -> list[tuple[str, types.Part]]:
        """Reads images from the specified folder and returns their bytes."""
        images = []
        for root, dirs, files in os.walk(folder_path):
            for filename in files:
                if filename.endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp')):
                    full_path = os.path.join(root, filename)
                    #image_path = os.path.join(folder_path, filename)
                    images.append(ImageUtil.read_image(full_path))
            
        return images