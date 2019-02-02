#!/bin/env python3

import logging
import sys

from abc import ABC, abstractmethod
from typing import Dict, Iterator, List, Optional

from bs4 import BeautifulSoup
from bs4.element import Tag
import requests


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.NullHandler())


def get_content_url(content_tag: Tag) -> Optional[str]:
    content: Dict[str, str] = content_tag.find(name="a", attrs={"class": "lightbox"})

    if content:
        return content["href"]

    content = content_tag.find(name=["img", "video"])

    return content["src"] if content else None


class AbstractSoupPageSourceProvider(ABC):
    @abstractmethod
    def get_source(self, url: str) -> str:
        pass


class WebSoupPageSourceProvider(AbstractSoupPageSourceProvider):
    @staticmethod
    def get_source(url: str) -> str:
        return requests.get(url).text


class SoupPage:
    def __init__(self, html: str) -> None:
        self.bs = BeautifulSoup(html, "html.parser")

    def get_next_page_relative_url(self) -> Optional[str]:
        next_page_link_tag = self.bs.find(name="a", attrs={"class": "more keephash"})
        return next_page_link_tag["href"] if next_page_link_tag is not None else None

    def get_content_urls(self) -> List[str]:
        content_tags: List[Tag] = self.bs.find_all(name="div", attrs={"class": "content"})

        content_urls = []

        for content_tag in content_tags:
            content_url = get_content_url(content_tag)
            if content_url:
                content_urls.append(content_url)
            else:
                logger.error(f"Could not find item in content tag: {content_tag}")

        return content_urls


class Soup:
    def __init__(self, url: str, source_provider: AbstractSoupPageSourceProvider) -> None:
        self.url = url
        self.source_provider = source_provider

    def __iter__(self) -> Iterator[SoupPage]:
        next_page_url: Optional[str] = self.url

        while next_page_url:
            logger.info(f"Current page url: {next_page_url}")
            page_source = self.source_provider.get_source(next_page_url)
            soup_page = SoupPage(page_source)
            next_page_url = self.get_next_page_url(soup_page)

            yield soup_page

    def get_next_page_url(self, soup_page: SoupPage) -> Optional[str]:
        next_page_relative_url = soup_page.get_next_page_relative_url()
        return f"{self.url}/{next_page_relative_url}" if next_page_relative_url else None


if __name__ == "__main__":
    logger.addHandler(logging.StreamHandler())

    soup_url: str = sys.argv[1]
    soup = Soup(soup_url, WebSoupPageSourceProvider())
    for page in soup:
        for link in page.get_content_urls():
            print(link)
