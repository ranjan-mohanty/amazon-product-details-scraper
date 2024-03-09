import argparse
import codecs
import json
import logging
import os
import re

import requests
from bs4 import BeautifulSoup

from . import config
from . import utils


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

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Raise an exception for non-200 status codes

    soup = BeautifulSoup(response.content, "html.parser")

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

    output_file = os.path.join(output_dir, config.DEFAULT_OUTPUT_FILENAME)
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
    utils.create_folder(output_dir)
    for i, image_url in enumerate(image_urls, start=1):
        file_name = f"image_{i}.{utils.extract_image_extension(image_url)}"
        utils.download_image(image_url, output_dir, file_name)


def main():
    """Main function for the script.

    This function parses command-line arguments, reads product URLs,
    fetches product details for each URL, writes details to JSON files,
    and optionally downloads product images.
    """

    logging.basicConfig(level=config.DEFAULT_LOG_LEVEL)

    parser = argparse.ArgumentParser(description="Amazon Product Details Scrapper")

    # A mutually exclusive group for URL input (either single URL or file)
    required_group = parser.add_mutually_exclusive_group(required=True)
    required_group.add_argument(
        "-u",
        "--url",
        type=str,
        help="URL of the Amazon product page you want to scrape.",
        metavar="<url>",
    )
    required_group.add_argument(
        "-ul",
        "--url-list",
        type=str,
        help="Path to a file containing a list of Amazon product URLs (one per line).",
        metavar="<file-path>",
    )

    # Optional arguments
    parser.add_argument(
        "-o",
        "--output-dir",
        type=str,
        default="output",
        help="Output directory to store scraped data (default: output).",
        metavar="<file-path>",
    )
    parser.add_argument(
        "-d",
        "--download-image",
        action="store_true",
        help="Download product images along with details (default: False).",
    )

    args = parser.parse_args()

    input_url = args.url
    url_list_path = args.url_list
    output_dir = args.output_dir
    download_image = args.download_image

    if input_url:
        url_list = [input_url]
    else:
        try:
            url_list = utils.read_file(url_list_path)
        except FileNotFoundError as e:
            logging.error(f"Error: URL list file not found: {url_list_path}")
            exit(1)

    # Process each product URL
    for item_num, url in enumerate(url_list, start=1):
        try:
            product_details = get_product_detail(url)

            if product_details:
                logging.info(f"Fetched Data for url {url}")
                # Log details with indentation for readability
                # logging.info(json.dumps(product_details, indent=2))

                product_output_dir = os.path.join(output_dir, f"item_{item_num}")
                utils.create_folder(product_output_dir, overwrite=True)

                write_product_details(product_details, product_output_dir)

                if download_image:
                    image_urls = product_details.get(
                        "image_urls", []
                    )  # Handle potential absence of image_urls key
                    download_product_images(image_urls, product_output_dir)
            else:
                logging.error(f"Failed to fetch product details for {url}")
        except Exception as e:
            logging.exception(f"Failed to fetch product details for {url}", e)


if __name__ == "__main__":
    print(__name__)
    main()
