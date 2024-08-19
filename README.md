# Metadata Extractor

**Metadata Extractor** is a Flask web application that allows users to upload image files and retrieve detailed metadata about the uploaded images. The application extracts various types of metadata, including file system information, image dimensions, and EXIF data (if available).

## Features

- Upload image files and retrieve metadata
- Extract file system metadata (e.g., file size, modification date)
- Extract image metadata (e.g., dimensions, format)
- Extract EXIF metadata (e.g., camera make, model, GPS information)
- Display metadata in a user-friendly format

## Technologies

- Flask: Web framework for building the application
- Pillow: Library for image processing
- piexif: Library for working with EXIF data
- Various other dependencies for file handling and metadata extraction

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Karthikdude/your-repo-name.git
   ```
2. Navigate to the project directory:
   ```bash
   cd your-repo-name
   ```
3. Install the required dependencies:
   ```bash
   pip install Flask Pillow piexif PyPDF2 python-docx xlrd openpyxl python-pptx moviepy mutagen
   ```

## Usage

1. Start the Flask application:
   ```bash
   python app.py
   ```
2. Open your web browser and go to `http://127.0.0.1:5000/` to access the application.
3. Upload an image file using the provided form on the upload page.
4. View the extracted metadata on the results page.

## Code Overview

- `app.py`: Main Flask application file that handles routes and metadata extraction.
- `templates/`: Directory containing HTML templates for the web pages (`landing.html`, `upload.html`, `result.html`).
- `static/`: Directory for static files such as CSS and JavaScript (if any).

### `get_metadata(image_file)`

This function extracts metadata from an uploaded image file. It retrieves file system metadata, image dimensions, and EXIF data. It handles various image formats and cleans up temporary files after extraction.

### Routes

- `/`: Landing page
- `/upload`: Page for uploading files and displaying results

## Example

Upload an image file to see detailed metadata such as:

- File size
- Modification date
- Image dimensions
- Camera make and model (if available)
- GPS coordinates (if available)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Feel free to submit issues or pull requests to improve the application. Contributions are welcome!

## Acknowledgements

- Flask: [Flask Documentation](https://flask.palletsprojects.com/)
- Pillow: [Pillow Documentation](https://pillow.readthedocs.io/)
- piexif: [piexif Documentation](https://piexif.readthedocs.io/)
- Various other libraries used in the project

For any questions or feedback, please contact [Karthik S Sathyan](https://www.linkedin.com/in/karthik-s-sathyan/).

