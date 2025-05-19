import csv
import requests
import re
from bs4 import BeautifulSoup
from typing import TypedDict

ichimoe_url = 'https://ichi.moe/cl/qr/'

class Word(TypedDict):
    jp: str
    reading: str
    trans: str

def get_words(jp_text: str) -> dict[str, Word]:
    words : dict[str, Word] = dict()

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
            text = re.sub(r'^\d+\.\s*', '', dt_tag.text).strip().split(' 【')
            jp = text[0]
            reading = jp
            if len(text) > 1:
                reading = text[1][:-1]
            trans = dt_tag.find_next_sibling('dd').find('span', 'gloss-desc')
            if trans != None:
                trans = trans.text.strip()
            else:
                trans = ''
            
            words[jp] = {'jp': jp, 'reading': reading, 'trans': trans}

        # For every <dt> tag, find the first parent <dl> tag and remove
        # their child <dt> content from the set.
        for dt_tag in dt_tags:
            dl_opt = dt_tag.find_parent('dl').find_parent('dl')
            if dl_opt != None:
                dt_opt = dl_opt.find('dt', recursive=False)
                if dt_opt != None:
                    words.pop(re.sub(r'^\d+\.\s*', '', dt_opt.text).strip().split(' 【')[0], None)

    return words

if __name__ == "__main__":
    '''
    Take an input file (which contains Japanese) and output
    Japanese words, readings, and translations into a .tsv file.
    '''
    import sys

    if len(sys.argv) != 2:
        print(f"Usage: python3 {sys.argv[0]} <input_file>")
        sys.exit(1)

    input_file = sys.argv[1]

    with open(input_file, "r", encoding="utf-8") as f:
        s = f.read()

    # Ichimoe can handle upwards of 700+ characters. But somewhere there is a limit.
    paragraphs = s.split('\n')

    words = dict()
    for paragraph in paragraphs:
        words |= get_words(paragraph)

    with open('ichimoe_output.tsv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter='\t')
        writer.writerow(['Japanese', 'Reading', 'Translation'])  # Header
        for item in words.values():
            writer.writerow([item['jp'], item['reading'], item['trans']])