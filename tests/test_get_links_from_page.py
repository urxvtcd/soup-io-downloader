import os
import unittest

from typing import ClassVar

from soup_downloader.get_content_links import (
    Soup,
    SoupPage,
    AbstractSoupPageSourceProvider,
)


def _get_current_file_dirname() -> str:
    return os.path.dirname(os.path.realpath(__file__))


class _TestSoupPageSourceProvider(AbstractSoupPageSourceProvider):
    def __init__(self, test_pages_path: str):
        self.test_pages_path = test_pages_path

    def get_source(self, file_name: str) -> str:
        file_path = self._get_test_page_path(file_name)
        with open(file_path) as source_file:
            return source_file.read()

    def _get_test_page_path(self, test_page_file_name: str) -> str:
        return os.path.join(self.test_pages_path, test_page_file_name)


class TestGetLinksFromPage(unittest.TestCase):
    page_provider: ClassVar[_TestSoupPageSourceProvider]

    @classmethod
    def setUpClass(cls) -> None:
        cls.page_provider = _TestSoupPageSourceProvider(_get_current_file_dirname())

    def test_getting_simple_img_url(self) -> None:
        soup = Soup("test_page.html", self.page_provider)
        page: SoupPage = next(iter(soup))
        urls = page.get_content_urls()

        assert "simple_img_url" in urls

    def test_getting_content_urls_from_page(self) -> None:
        soup = Soup("test_page.html", self.page_provider)
        page: SoupPage = next(iter(soup))
        urls = page.get_content_urls()

        assert "lightbox_img_url" in urls

    def test_getting_next_page_url(self) -> None:
        soup = Soup("test_page.html", self.page_provider)
        page = next(iter(soup))

        next_page = page.get_next_page_relative_url()

        assert next_page == "second_page"
