from flask import Flask, request, render_template, redirect, url_for
from PIL import Image
import piexif
import io
import os
import mimetypes
from datetime import datetime
import stat

app = Flask(__name__, static_folder='static', template_folder='templates')

def get_metadata(image_file):
    try:
        # Convert the file to a BytesIO object
        img_bytes = io.BytesIO(image_file.read())
        
        # Get the file extension
        file_extension = os.path.splitext(image_file.filename)[1].lower()
        
        # Determine the MIME type
        mime_type, _ = mimetypes.guess_type(image_file.filename)
        
        # Open the image with PIL
        image = Image.open(img_bytes)
        
        # Get file system metadata
        temp_path = os.path.join(os.getcwd(), 'temp_' + image_file.filename)  # Use a temporary file
        image_file.seek(0)
        with open(temp_path, 'wb') as f:
            f.write(image_file.read())
        
        file_stat = os.stat(temp_path)
        file_permissions = oct(file_stat.st_mode & stat.S_IRWXU & stat.S_IRWXG & stat.S_IRWXO)[2:]
        file_size = round(file_stat.st_size / 1024, 2)  # Convert size to kB
        file_modify_date = datetime.fromtimestamp(file_stat.st_mtime).strftime('%Y:%m:%d %H:%M:%S')
        file_access_date = datetime.fromtimestamp(file_stat.st_atime).strftime('%Y:%m:%d %H:%M:%S')
        file_inode_change_date = datetime.fromtimestamp(file_stat.st_ctime).strftime('%Y:%m:%d %H:%M:%S')

        # Extract image metadata
        info_dict = {
            "file_name": os.path.basename(image_file.filename),
            "file_size": f"{file_size} kB",
            "file_modify_date": file_modify_date,
            "file_access_date": file_access_date,
            "file_inode_change_date": file_inode_change_date,
            "file_permissions": file_permissions,
            "file_type": image.format,
            "file_type_extension": file_extension,
            "mime_type": mime_type if mime_type else 'N/A',
            "image_width": image.width,
            "image_height": image.height,
            "image_size": f"{image.width}x{image.height}",
            "megapixels": round((image.width * image.height) / 1_000_000, 3),
            "encoding_process": "Baseline DCT, Huffman coding",  # This is typically fixed for JPEGs
            "bits_per_sample": image.info.get('bits', 'N/A'),
            "color_components": 3,  # Assumed; for JPEGs, this is usually 3 (RGB)
            "y_cb_cr_sub_sampling": "YCbCr4:2:0 (2 2)",  # Typical for JPEG
            "jfif_version": "1.01",  # Common version
            "resolution_unit": "inches",  # Assumed default
            "x_resolution": image.info.get('dpi', [96, 96])[0],
            "y_resolution": image.info.get('dpi', [96, 96])[1],
            "location": "N/A"  # Default value
        }
        
        # Reset the file pointer to the beginning
        img_bytes.seek(0)
        
        # Load EXIF data
        try:
            exif_data = piexif.load(img_bytes.read())
            print("EXIF data loaded successfully.")
        except Exception as exif_exception:
            print(f"EXIF data load error: {str(exif_exception)}")
            exif_data = {}
        
        if '0th' in exif_data:
            try:
                info_dict['make'] = exif_data['0th'].get(piexif.ImageIFD.Make, b'N/A').decode(errors='ignore')
                info_dict['model'] = exif_data['0th'].get(piexif.ImageIFD.Model, b'N/A').decode(errors='ignore')
                info_dict['date_time_original'] = exif_data['0th'].get(piexif.ImageIFD.DateTime, b'N/A').decode(errors='ignore')
                info_dict['software'] = exif_data['0th'].get(piexif.ImageIFD.Software, b'N/A').decode(errors='ignore')

                # Extract sub-seconds if available
                info_dict['sub_sec_time_original'] = exif_data['Exif'].get(piexif.ExifIFD.SubSecTimeOriginal, b'N/A').decode(errors='ignore')
                info_dict['sub_sec_date_time_original'] = exif_data['Exif'].get(piexif.ExifIFD.SubSecTimeOriginal, b'N/A').decode(errors='ignore')

                # Extract GPS information if available
                gps_info = exif_data.get('GPS', {})
                if gps_info:
                    latitude = gps_info.get(piexif.GPSIFD.GPSLatitude, b'N/A').decode(errors='ignore')
                    longitude = gps_info.get(piexif.GPSIFD.GPSLongitude, b'N/A').decode(errors='ignore')
                    info_dict['location'] = f"Latitude: {latitude}, Longitude: {longitude}"
            except Exception as e:
                print(f"Error processing EXIF data: {str(e)}")
        
        # Clean up temporary file
        os.remove(temp_path)
        
        return info_dict
    except Exception as e:
        print(f"Error: {str(e)}")
        return {"error": str(e)}

@app.route('/')
def landing_page():
    return render_template('landing.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            metadata = get_metadata(file)
            return render_template('result.html', metadata=metadata)
    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True)
pip install Flask Pillow piexif PyPDF2 python-docx xlrd openpyxl python-pptx moviepy mutagen
