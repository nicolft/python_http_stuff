import requests
import bs4.element
from bs4 import BeautifulSoup

ichimoe_url = 'https://ichi.moe/cl/qr/'

def get_words(jp_text: str) -> set[str]:
    words : set[str] = set()

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

        # Get all <dt> tags and add its content to the words sets.
        dt_tags = soup.find_all('dt')
        for dt_tag in dt_tags:
            words.add(dt_tag.text.strip())

        # For every <dt> tag, find the first parent <dl> tag and remove
        # their child <dt> content from the set.
        for dt_tag in dt_tags:
            dl_opt = dt_tag.find_parent('dl').find_parent('dl')
            if dl_opt != None:
                dt_opt = dl_opt.find('dt', recursive=False)
                if dt_opt != None:
                    words.discard(dt_opt.text.strip())
        

    return set() # TODO