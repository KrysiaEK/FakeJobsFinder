from .base import BasePlatform, Browser, OfferDetails
from datetime import datetime

class Sprzedajemy(BasePlatform):
    def get_offers(self, page: int) -> list[str]:
        with Browser() as browser:
            offset = page * 30
            browser.goto(f'https://sprzedajemy.pl/praca?offset={offset}')    
            browser.wait_for_load_state('domcontentloaded')
            offers = browser.evaluate("""() => {
                var elements = document.getElementsByTagName("a");
                var offers = [];
                for(var i = 0; i < elements.length; ++i) {
                    if(elements[i].href && elements[i].className == 'offerLink') {
                        offers.push(elements[i].href);
                    }
                }
                return offers;        
            }""")
            return list(set(offers))

    def get_offer(self, url) -> OfferDetails:
        with Browser() as browser:
            browser.goto(url)                
            browser.wait_for_load_state('domcontentloaded')
            browser.wait_for_selector('div#offerDetailsBottom')

            # set resolution
            dimensions = browser.evaluate("""() => {
                return {
                    width: 1000,
                    height: document.documentElement.clientHeight,
                    deviceScaleFactor: window.devicePixelRatio,
                }
            }""")
            browser.set_viewport_size = dimensions
        
            # accept cookies
            browser.evaluate("""() => {
                let el = document.getElementById("didomi-notice-agree-button");
                if(el) { el.click(); }
            }""")

            # get offer description
            title = browser.evaluate("""() => {
                var title = document.getElementsByClassName('offerDetailsTop');
                return title[0].innerText.split('\\n')[0];        
            }""")

            user = browser.evaluate("""() => {
                var user = document.getElementsByClassName("name");
                return user[0].innerText;        
            }""")

            offer_description = browser.evaluate("""() => {
                var divs = document.getElementsByClassName("offerDescription");
                return divs[0].innerText;        
            }""")

            # take screenshot
            screenshot = browser.screenshot(full_page=True)

            return OfferDetails(
                url,
                title,
                offer_description,
                user,
                datetime.now(),  # todo
                screenshot
            )
