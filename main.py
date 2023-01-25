import hashlib
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def sprawdzenie_strony(adres):
    # Uzyskanie aktualnej wersji strony internetowej
    aktualna_strona = requests.get(adres).content
    soup = BeautifulSoup(aktualna_strona, 'html.parser')
    resource_hashes = {}

    # Obliczenie wartości hashu kodu HTML
    obecny_hash = hashlib.sha256(aktualna_strona).hexdigest()
    resource_hashes[adres] = obecny_hash

    # Obliczenie hashu wszystkich pozostałych zasobów
    for tag in soup.find_all(['img', 'link', 'script']):
        src = tag.get('src') or tag.get('href')
        if src:
            resource_url = urljoin(adres, src)
            try:
                resource = requests.get(resource_url).content
                resource_hash = hashlib.sha256(resource).hexdigest()
                resource_hashes[resource_url] = resource_hash
            except requests.exceptions.RequestException as e:
                print(e)
                continue

    # Przechowanie aktualnych hashy w pliku
    with open("website_hashes.txt", "w") as f:
        f.write(str(resource_hashes))

    # Sprawdzenie ponownie strony po określonym czasie
    # Można użyć programu do harmonogramowania, takiego jak Cron, aby okresowo uruchamiać ten skrypt
    nowa_strona = requests.get(adres).content
    soup = BeautifulSoup(nowa_strona, 'html.parser')
    new_resource_hashes = {}

    # Obliczenie nowego hashu kodu HTML
    nowy_hash = hashlib.sha256(nowa_strona).hexdigest()
    new_resource_hashes[adres] = nowy_hash

    # Obliczenie nowych hashy wszystkich pozostałych zasobów
    for tag in soup.find_all(['img', 'link', 'script']):
        src = tag.get('src') or tag.get('href')
        if src:
            resource_url = urljoin(adres, src)
            try:
                resource = requests.get(resource_url).content
                resource_hash = hashlib.sha256(resource).hexdigest()
                new_resource_hashes[resource_url] = resource_hash
            except requests.exceptions.RequestException as e:
                print(e)
                continue

    # Porównanie nowych hashy z przechowywanymi hashami
    with open("website_hashes.txt", "r") as f:
        stare_hashe = eval(f.read())
    for resource_url, nowy_hash in new_resource_hashes.items():
        if resource_url not in stare_hashe or nowy_hash != stare_hashe[resource_url]:
            print("ALERT: Zasób {} został zmieniony!".format(resource_url))
    else:
        print("Strona jest bezpieczna.")


sprawdzenie_strony("https://www.wp.pl")
