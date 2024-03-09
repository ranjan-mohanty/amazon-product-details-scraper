import os
import shutil
import requests


def create_folder(path: str, overwrite: bool = False) -> None:
    """Creates a folder at the specified path.

    Args:
        path: The path to the directory to create. Must be a string.
        overwrite: If True (default), an existing directory at the path will be removed
            before creating a new one.

    Raises:
        TypeError: If the 'path' argument is not a string.
        ValueError: If the 'path' argument is empty.
        OSError: If there's an error creating the directory (e.g., permission issues).
    """

    if not isinstance(path, str):
        raise TypeError("Path must be a string.")

    if not path:
        raise ValueError("Path cannot be empty.")

    if os.path.exists(path):
        if overwrite:
            shutil.rmtree(path)

    os.makedirs(path)


def extract_image_extension(url: str) -> str:
    """Extracts the image file extension from a URL, handling query params and unknown extensions.

    Args:
        url: The URL of the image.

    Returns:
        The extracted file extension (e.g., ".jpg", ".png"), or an empty string if no valid extension is found.
    """

    parts = url.rsplit("?", 1)
    url_without_query = parts[0]

    parts = url_without_query.rsplit(".", 1)

    if len(parts) == 1:
        return ""

    extension = parts[1].lower()
    return extension


def download_image(
    url: str, output_dir: str, file_name: str, overwrite: bool = False
) -> None:
    """Downloads an image from the specified URL and saves it to the given output directory.

    Args:
        url: The URL of the image to download.
        output_dir: The directory path to save the image.
        file_name: The desired filename for the downloaded image.
        overwrite: If True (default), an existing file with the same name will be overwritten.

    Raises:
        OSError: If there's an error creating the output directory, downloading the image, or writing the image to file.
        requests.exceptions.RequestException: If there's an error downloading the image from the URL.
    """

    # Construct the full path for the image
    image_path = os.path.join(output_dir, file_name)

    # Download the image using requests
    response = requests.get(url, stream=True)
    response.raise_for_status()  # Raise an exception for unsuccessful requests

    # Write the image data to the file
    with open(image_path, "wb") as f:
        for chunk in response.iter_content(1024):
            f.write(chunk)


def read_file(file_path: str) -> list[str]:
    """Reads a text file and returns a list of its lines.

    Args:
        file_path: The path to the text file to read.

    Raises:
        OSError: If there's an error opening the file.
        TypeError: If the 'file_path' argument is not a string.
    """

    if not isinstance(file_path, str):
        raise TypeError("File path must be a string.")

    with open(file_path, "r") as f:
        # Read lines from the file directly within the 'with' block
        return f.readlines()
