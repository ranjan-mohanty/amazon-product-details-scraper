## Amazon Product Details Scraper

[![GitHub Release](https://img.shields.io/github/v/release/ranjan-mohanty/amazon-product-details-scraper)](https://github.com/ranjan-mohanty/amazon-product-details-scraper/releases)
[![GitHub License](https://img.shields.io/github/license/ranjan-mohanty/amazon-product-details-scraper)](https://github.com/ranjan-mohanty/amazon-product-details-scraper/blob/main/LICENSE)
[![PyPI - Version](https://img.shields.io/pypi/v/amazon-product-details-scraper)](https://pypi.org/project/amazon-product-details-scraper/)
[![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/ranjan-mohanty/amazon-product-details-scraper/build.yml)](https://github.com/ranjan-mohanty/amazon-product-details-scraper/actions/workflows/build.yml)
[![Downloads](https://static.pepy.tech/badge/amazon-product-details-scraper)](https://pepy.tech/project/amazon-product-details-scraper)
[![GitHub Issues or Pull Requests](https://img.shields.io/github/issues/ranjan-mohanty/amazon-product-details-scraper)](https://github.com/ranjan-mohanty/amazon-product-details-scraper/issues)
[![GitHub forks](https://img.shields.io/github/forks/ranjan-mohanty/amazon-product-details-scraper)](https://github.com/ranjan-mohanty/amazon-product-details-scraper/forks)
[![GitHub Repo stars](https://img.shields.io/github/stars/ranjan-mohanty/amazon-product-details-scraper)](https://github.com/ranjan-mohanty/amazon-product-details-scraper/stargazers)

This script helps you scrape product details from Amazon product pages. It extracts information like title, description, and image URLs, saving them to JSON files.

### Features

- Fetches product details from a single Amazon product URL or a list of URLs in a file.
- Writes extracted data to JSON files for easy storage and processing.
- Optionally downloads product images along with details.

### Installation

**Requirements:**

- Python 3 (tested with 3.7+)
- Libraries:
  - requests
  - beautifulsoup4
  - urllib3

**Instructions:**

1. Make sure you have Python 3 installed. You can check by running `python3 --version` in your terminal.
2. **Create a virtual environment (recommended):**

   - Virtual environments help isolate project dependencies and avoid conflicts with other Python installations on your system.
   - Here's how to create a virtual environment using `venv`:

     ```bash
     python3 -m venv my_env  # Replace "my_env" with your desired environment name
     ```

   - Activate the virtual environment:

     ```bash
     source my_env/bin/activate
     ```

3. **Install:**

   ```bash
   python3 setup.py install
   ```

   This will automatically download and install the necessary libraries based on the specifications within the activated virtual environment.

### Usage

**Basic Usage:**

```bash
amazon-scraper --url https://www.amazon.com/product-1  # Replace with your product URL
```

This will scrape details from the provided Amazon product URL and write them to a JSON file in the "output" directory (default).

**Using a URL List:**

1. Create a text file containing a list of Amazon product URLs (one per line).
2. Run the script with the `--url-list` option and provide the file path:

```bash
amazon-scraper --url-list product_urls.txt
```

This will process each URL in the file and save the scraped details for each product in separate directories within "output".

**Optional: Downloading Images**

```bash
amazon-scraper --url https://www.amazon.com/product-1 --download-image
```

The `--download-image` flag enables downloading product images along with other details.

**Getting Help:**

The script offers a built-in help message that provides a quick overview of available options and usage instructions. To access the help, run the script with the `--help` option:

```bash
amazon_scraper --help
```

### Configuration

**Logging:**

- The script uses basic logging for information and error messages.
- You can modify the logging level by editing the `DEFAULT_LOG_LEVEL` in `config.py` line in the code (refer to the Python documentation for logging configuration).

### Example

**Scenario:**

Scrape details for two products from a file named "products.txt" and download images:

1. Create a file named "products.txt" with the following content:

```
https://www.amazon.com/product-1
https://www.amazon.com/product-2
```

2. Run the script with the following command:

```bash
amazon-scraper --url-list products.txt --download-image
```

This will process both URLs in the file, scrape details, create separate output directories for each product, and download images.

### Disclaimer

This script is for educational purposes only. Please be respectful of Amazon's terms of service when using it. Consider using official APIs provided by Amazon for extensive data collection.
