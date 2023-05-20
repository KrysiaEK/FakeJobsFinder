from abc import ABC, abstractmethod
from playwright.sync_api import sync_playwright
from dataclasses import dataclass
from datetime import datetime
 
class Browser:
    def __enter__(self):
        self.context = sync_playwright()
        self.playwright = self.context.__enter__()
        self.browser = self.playwright.chromium.launch()
        self.page = self.browser.new_page()
        return self.page

    def __exit__(self, exc_type, exc_value, traceback):
        self.browser.close()
        self.context.__exit__()

@dataclass
class OfferDetails:
    url: str
    title: str
    description: str
    author: str
    date: datetime 
    screenshot: bytes

class BasePlatform:
    @abstractmethod
    def get_offers(self, page: int) -> list[str]:
        pass

    @abstractmethod
    def get_offer(self, url) -> OfferDetails:
        pass
