import requests
from bs4 import BeautifulSoup

ichimoe_url = 'https://ichi.moe/cl/qr/'

def add_chars(set: set[str], jp_text: str) -> None:
    # Get Ichimoe page HTML
    jp_text = jp_text.replace("\n", " ")
    response : requests.Response = requests.get(
        ichimoe_url, params={'q': jp_text}
        )

    if response.status_code == 200:
        # In ichi.moe, every word is described within a <dl> tag.
        # <dl>
        #   <dt>WORD</dt>
        #   <dd>info. and defn. about word</dd>
        # </dl>
        # These may be recursively nested (inside the dd tag) to show
        # compound words and conjugations.
        #
        # Hence, we filter for dictionary forms by getting only
        # <dl> tags which have no <dl> as descendant.
        
        soup = BeautifulSoup(response.text, 'html.parser')
        # TODO
    return