
import os

import google.genai.types as types

from app.util.file import FileUtil

class ImageUtil:

    IMAGE_EXTENSIONS = ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'tiff', 'webp']

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
        return mime_types.get(extension, '')  # Default to JPEG if unknown

    @staticmethod
    def build_image_part(image_path: str, bytes_data: bytes) -> types.Part:
        return types.Part(
            inline_data=types.Blob(
                mime_type=ImageUtil.get_mime_type(image_path),
                data=bytes_data
            )
        )

    @staticmethod
    def read_image(image_path: str) -> tuple[str, types.Part]:
        """Reads an image from the specified path and returns its bytes."""
        bytes_data = FileUtil.read_file(image_path)
        return image_path, ImageUtil.build_image_part(image_path, bytes_data)

    @staticmethod
    def read_images_from_file_paths(file_paths: list[str]) -> list[tuple[str, types.Part]]:
        """Reads images from the specified files and returns their bytes."""
        images = []
        for file_path in file_paths:
            images.append(ImageUtil.read_image(file_path))
        return images

    @staticmethod
    def read_images_from_folder(folder_path: str) -> list[tuple[str, types.Part]]:
        """Reads images from the specified folder and returns their bytes."""
        images = []
        image_bytes = FileUtil.read_files_from_folder(folder_path, ImageUtil.IMAGE_EXTENSIONS)
        images.append([
            (file_path, ImageUtil.build_image_part(file_path, bytes_data)) 
            for file_path, bytes_data in image_bytes
        ])
        return images