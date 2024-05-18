import logging
import os
import re
import json
import uuid
import codecs
import requests

from bs4 import BeautifulSoup
from urllib3.util.url import parse_url

from amazon_product_details_scraper.config import (
    DEFAULT_OUTPUT_FILENAME,
    VALID_DOMAIN_NAMES,
)
from amazon_product_details_scraper.core.utils import create_folder, download_image, extract_image_extension


def get_product_detail(url):
    """Extracts product data from an Amazon product page URL.

    This function scrapes the product title, description, and image URLs from a given Amazon product page URL.

    Args:
        url (str): The URL of the Amazon product page.

    Returns:
        dict: A dictionary containing the extracted data, including:
            - title (str): The product title.
            - description (str): The product description.
            - image_urls (list): A list of image URLs for the product.

    Raises:
        Exception: An exception may be raised if there's an issue fetching or parsing the product details.
    """
    if not is_valid_url(url):
        raise Exception("Invalid amazon product URL")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" +
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
    }

    response = requests.get(url, headers=headers, timeout=10000)
    response.raise_for_status()  # Raise an exception for non-200 status codes

    soup = BeautifulSoup(response.content, "html.parser")

    asin_element = soup.find("input", id="ASIN")
    item_id = asin_element["value"] if asin_element else str(uuid.uuid4())

    title_element = soup.find("span", id="productTitle")
    title = title_element.text.strip() if title_element else None

    description_element = soup.find("div", id="feature-bullets")
    description = description_element.text.strip() if description_element else None

    image_block_element = soup.find("div", id="imageBlock_feature_div")

    image_urls = []
    if image_block_element:
        for script_element in image_block_element.find_all("script"):
            script_text = script_element.string if script_element else None
            if script_text and "ImageBlockATF" in script_text:
                image_url_pattern = r'"hiRes":"(.*?)",'
                image_urls.extend(re.findall(image_url_pattern, script_text))

    return {
        "id": item_id,
        "title": title,
        "description": description,
        "image_urls": image_urls,
    }


def write_product_details(product_details, output_dir):
    """Writes product details to a JSON file.

    This function takes a dictionary containing product details and writes them to a JSON file
    in the specified output directory.

    Args:
        product_details (dict): A dictionary containing product data as returned by `get_product_detail`.
        output_dir (str): The path to the output directory.
    """

    output_file = os.path.join(output_dir, DEFAULT_OUTPUT_FILENAME)
    with codecs.open(output_file, "w", encoding="utf8") as f:
        json.dump(product_details, f, ensure_ascii=False, indent=2)


def download_product_images(image_urls, output_dir):
    """Downloads product images from the provided URLs.

    This function downloads images from a list of URLs and saves them to a subdirectory named "images"
    within the specified output directory.

    Args:
        image_urls (list): A list of image URLs for the product.
        output_dir (str): The path to the output directory.
    """

    output_dir = os.path.join(output_dir, "images")
    create_folder(output_dir)
    for i, image_url in enumerate(image_urls, start=1):
        file_name = f"image_{i}.{extract_image_extension(image_url)}"
        download_image(image_url, output_dir, file_name)


def is_valid_url(url):
    """Validates the provided URL.

    This function validates the URL and checks if the hostname is a valid domain name.

    Args:
        url (str): The URL to validate.

    Returns:
        bool: True if the URL is valid, False otherwise.
    """

    try:
        parsed_url = parse_url(url)
        if not parsed_url.netloc or not parsed_url.scheme:
            return False  # Not a valid URL format
        domain = parsed_url.netloc.lower()

        # Check if the domain ends with any of the valid domains
        return any(domain.endswith(tld.lower()) for tld in VALID_DOMAIN_NAMES)
    except Exception as e:
        logging.error(f"Error validating URL: {e}")
        return False
