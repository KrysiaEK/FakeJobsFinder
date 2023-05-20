from .base import BasePlatform, Browser, OfferDetails
from datetime import datetime
 
class OLX(BasePlatform):
    def get_offers(self, page: int) -> list[str]:
        with Browser() as browser:
            browser.goto(f'https://www.olx.pl/praca/?page={page}')    
            browser.wait_for_load_state('networkidle')
            offers = browser.evaluate("""() => {
                var elements = document.getElementsByTagName("a");
                var offers = [];
                for(var i = 0; i < elements.length; ++i) {
                    if(elements[i].href && elements[i].href.indexOf('/oferta/praca') >= 0) {
                        offers.push(elements[i].href);
                    }
                }
                return offers;        
            }""")
            return offers

    def get_offer(self, url) -> OfferDetails:
        with Browser() as browser:
            browser.goto(url)    
            browser.wait_for_load_state('networkidle')

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
            browser.evaluate('() => document.getElementById("onetrust-accept-btn-handler").click();')

            # get offer description
            title = browser.evaluate("""() => {
                var title = document.getElementsByTagName("h1");
                return title[0].innerText;        
            }""")

            offer_description = browser.evaluate("""() => {
                var divs = document.getElementsByTagName("div");
                var description;
                for(var i = 0; i < divs.length; ++i) {
                    if(divs[i].innerText.indexOf("OPIS") >= 0 && divs[i].innerText.indexOf("Dodane") >= 0) {
                        var text = divs[i].innerText;
                        if(!description || description.length > text.length) {
                        description = text;
                    }
                    }
                }
                return description;        
            }""")

            # take screenshot
            screenshot = browser.screenshot(full_page=True)

            return OfferDetails(
                url,
                title,
                offer_description,
                "",
                datetime.now(),
                screenshot
            )            
