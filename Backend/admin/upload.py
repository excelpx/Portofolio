"""
Cloudinary File Upload Handler
Handles image uploads to Cloudinary cloud storage
"""

import os
import cloudinary
import cloudinary.uploader
import cloudinary.api
from werkzeug.utils import secure_filename
import logging

logger = logging.getLogger(__name__)

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif', 'webp'}
MAX_FILE_SIZE = 10 * 1024 * 1024


def initialize_cloudinary():
    """
    Initialize Cloudinary configuration from environment variables
    Should be called once when application starts
    """
    try:
        cloudinary.config(
            cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
            api_key=os.getenv("CLOUDINARY_API_KEY"),
            api_secret=os.getenv("CLOUDINARY_API_SECRET")
        )
        logger.info("✓ Cloudinary initialized successfully")
        return True
    except Exception as e:
        logger.error(f"✗ Failed to initialize Cloudinary: {e}")
        return False


def is_file_allowed(filename):
    """
    Check if uploaded file extension is allowed
    
    Args:
        filename (str): Name of the uploaded file
    
    Returns:
        bool: True if allowed, False otherwise
    """
    if '.' not in filename:
        return False
    
    extension = filename.rsplit('.', 1)[1].lower()
    return extension in ALLOWED_EXTENSIONS


def upload_gambar(file_obj, folder="portfolio"):
    """
    Upload image file to Cloudinary and return the secure URL
    
    This function handles image uploads to Cloudinary cloud storage,
    validates file type and size, and returns the secure URL
    of the uploaded image.
    
    Args:
        file_obj (FileStorage): File object from Flask form/request
        folder (str): Cloudinary folder name for organizing uploads
                     Default: "portfolio"
    
    Returns:
        dict: Dictionary containing:
            - 'success' (bool): Whether upload was successful
            - 'secure_url' (str): URL of uploaded image (if successful)
            - 'public_id' (str): Public ID in Cloudinary (if successful)
            - 'error' (str): Error message (if failed)
    
    Raises:
        None - Returns error in dict instead
    
    Example:
        from Backend.admin.upload import upload_gambar
        
        result = upload_gambar(request.files['foto'])
        if result['success']:
            image_url = result['secure_url']
        else:
            error_msg = result['error']
    """
    
    if not file_obj or file_obj.filename == '':
        return {
            'success': False,
            'error': 'No file selected'
        }
    
    if not is_file_allowed(file_obj.filename):
        return {
            'success': False,
            'error': f'File type not allowed. Allowed types: {", ".join(ALLOWED_EXTENSIONS)}'
        }
    
    file_obj.seek(0, os.SEEK_END)
    file_size = file_obj.tell()
    file_obj.seek(0)
    
    if file_size > MAX_FILE_SIZE:
        return {
            'success': False,
            'error': f'File size exceeds maximum limit of {MAX_FILE_SIZE // (1024 * 1024)} MB'
        }
    
    try:
        filename = secure_filename(file_obj.filename)
        
        upload_result = cloudinary.uploader.upload(
            file_obj,
            folder=folder,
            resource_type="auto",
            overwrite=False,
            quality="auto",
            fetch_format="auto"
        )
        
        logger.info(f"✓ Image uploaded successfully: {upload_result['public_id']}")
        
        return {
            'success': True,
            'secure_url': upload_result['secure_url'],
            'public_id': upload_result['public_id'],
            'width': upload_result.get('width'),
            'height': upload_result.get('height'),
            'format': upload_result.get('format'),
            'size': upload_result.get('bytes')
        }
    
    except cloudinary.exceptions.Error as e:
        logger.error(f"✗ Cloudinary upload error: {e}")
        return {
            'success': False,
            'error': f'Failed to upload to Cloudinary: {str(e)}'
        }
    
    except Exception as e:
        logger.error(f"✗ Unexpected error during upload: {e}")
        return {
            'success': False,
            'error': f'Unexpected error during upload: {str(e)}'
        }


def delete_gambar(public_id):
    """
    Delete image from Cloudinary by public ID
    
    Args:
        public_id (str): Public ID of the image in Cloudinary
    
    Returns:
        dict: Dictionary containing:
            - 'success' (bool): Whether deletion was successful
            - 'message' (str): Status message
    """
    try:
        result = cloudinary.uploader.destroy(public_id)
        
        if result.get('result') == 'ok':
            logger.info(f"✓ Image deleted successfully: {public_id}")
            return {
                'success': True,
                'message': 'Image deleted successfully'
            }
        else:
            logger.warning(f"✗ Image not found in Cloudinary: {public_id}")
            return {
                'success': False,
                'message': 'Image not found in Cloudinary'
            }
    except Exception as e:
        logger.error(f"✗ Failed to delete image: {e}")
        return {
            'success': False,
            'message': f'Failed to delete image: {str(e)}'
        }


def get_gambar_info(public_id):
    """
    Get information about an uploaded image
    
    Args:
        public_id (str): Public ID of the image in Cloudinary
    
    Returns:
        dict: Image information from Cloudinary
    """
    try:
        result = cloudinary.api.resource(public_id)
        return result
    except Exception as e:
        logger.error(f"✗ Failed to get image info: {e}")
        return None

"""
# In Flask route:
from flask import request, jsonify
from Backend.admin.upload import upload_gambar

@app.route('/api/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    result = upload_gambar(file)
    
    if result['success']:
        return jsonify(result), 200
    else:
        return jsonify(result), 400


# In form submission:
result = upload_gambar(request.files['foto'], folder="profil")
if result['success']:
    image_url = result['secure_url']
    # Save image_url to database
else:
    error = result['error']
    # Handle error
"""
