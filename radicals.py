import requests
from bs4 import BeautifulSoup

file = open('./radicals.txt')
words = file.read().split('\n')  # Your list of words
file.close()

base_url = 'https://jisho.org/search/%23kanji%20'     # Replace with the real base URL

results = []

counter = 0
for word in words:
    result = ''

    try:
        if len(word) > 1:
            response = requests.get(word)

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                info = soup.find('span', class_='page-header__icon page-header__icon--radical')

                if info:
                    result = info.text.strip()

            else:
                result = "-"
            
        else:
            url = f"{base_url}{word}"
            response = requests.get(url)

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Example: find a specific element by class or tag
                # Change this to match the structure of the site
                dict = soup.find('div', class_='kanji-details__main-meanings')
                rad = soup.find('span', class_="radical_meaning")

                if dict is None:
                    dict = ''
                else:
                    dict = dict.text.split(',')[0].strip()
                if rad is None:
                    rad = ''
                else:
                    rad = rad.text.strip()
                
                result = dict + ',' + rad
    except _:
        pass
    results.append(result)
    print(result, end='.', flush=True)
print('')

# Print or save the results
with open("radicals_output.txt", "w") as f:
  f.write('\n'.join(results))