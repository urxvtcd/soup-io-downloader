#!/bin/env python3

import logging
import os
import sys

import requests


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.NullHandler())


def download_content(urls_file_name: str, download_dir: str) -> None:
    with open(urls_file_name, "r") as content_links_file:
        for url in content_links_file.readlines():
            url = url.strip()
            target_path = os.path.join(download_dir, url.split("/")[-1])
            download_single(url, target_path)


def download_single(url: str, target_path: str) -> None:
    try:
        response = requests.get(url)
        response.raise_for_status()
    except Exception:
        logger.error(f"Could not get {url}")
        return

    logger.info(f"Got {url}")

    with open(target_path, mode="wb") as target_file:
        target_file.write(response.content)


if __name__ == "__main__":
    logger.addHandler(logging.StreamHandler())

    urls_file_name, download_dir = sys.argv[1:]
    download_content(urls_file_name, download_dir)
