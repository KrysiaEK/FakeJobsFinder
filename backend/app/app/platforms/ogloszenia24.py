from .base import BasePlatform, Browser, OfferDetails
from datetime import datetime

class Ogloszenia24(BasePlatform):
    def get_offers(self, page: int) -> list[str]:
        with Browser() as browser:
            browser.goto(f'https://www.oglaszamy24.pl/ogloszenia/praca/oferty-pracy/?std=1&results={page}')    
            browser.wait_for_load_state('domcontentloaded')
            offers = browser.evaluate("""() => {
                var elements = document.getElementsByTagName("a");
                var offers = [];
                for(var i = 0; i < elements.length; ++i) {
                    if(elements[i].href && elements[i].href.indexOf('/ogloszenie/') >= 0) {
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
            browser.wait_for_selector('div#page_c')

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
            # browser.evaluate('() => document.getElementById("onetrust-accept-btn-handler").click();')

            # get offer description
            title = browser.evaluate("""() => {
                var title = document.getElementsByTagName("h1");
                return title[0].innerText;        
            }""")

            user = browser.evaluate("""() => {
                var user = document.getElementsByClassName("std_text_b");
                return user[0].innerText;        
            }""")

            offer_description = browser.evaluate("""() => {
                var description = document.getElementById("adv_desc");
                return description.innerText;        
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
