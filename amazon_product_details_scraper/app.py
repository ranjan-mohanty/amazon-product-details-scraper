import os
import logging
import argparse

from amazon_product_details_scraper.config import DEFAULT_LOG_LEVEL
from amazon_product_details_scraper.core.utils import create_folder, read_file
from amazon_product_details_scraper.core.scraper import (
    download_product_images,
    get_product_detail,
    write_product_details,
)


def main():
    """Main function for the script.

    This function parses command-line arguments, reads product URLs,
    fetches product details for each URL, writes details to JSON files,
    and optionally downloads product images.
    """

    logging.basicConfig(level=DEFAULT_LOG_LEVEL)

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
            url_list = read_file(url_list_path)
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
                create_folder(product_output_dir, overwrite=True)

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
    main()
