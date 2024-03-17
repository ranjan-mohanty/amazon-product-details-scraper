from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()
# Get the long description from the README file
long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="amazon-product-details-scraper",
    version="1.0.1",
    description="Scrapes product details from Amazon product pages and also downloads the images",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ranjan-mohanty/amazon-product-details-scraper/blob/main/README.md",
    author="Ranjan Mohanty",
    author_email="ranjan@duck.com",
    packages=find_packages(),
    keywords="amazon, scraper",
    entry_points={
        "console_scripts": [
            "amazon-scraper=amazon_product_details_scraper.app:main",
        ]
    },
    install_requires=["requests==2.31.0", "beautifulsoup4==4.11.1", "urllib3==1.26.18"],
    project_urls={
        "Source": "https://github.com/ranjan-mohanty/amazon-product-details-scraper",
    },
)
