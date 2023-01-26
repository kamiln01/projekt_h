# Kamil Najdek, 259011
import hashlib
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def check_website(url):
    # Uzyskanie aktualnej wersji strony internetowej
    current_site = requests.get(url).content
    soup = BeautifulSoup(current_site, 'html.parser')
    resource_hashes = {}

    # Obliczenie wartości hashu kodu HTML
    current_hash = hashlib.sha256(current_site).hexdigest()
    resource_hashes[url] = current_hash

    # Obliczenie hashu wszystkich pozostałych zasobów
    for tag in soup.find_all(['img', 'link', 'script']):
        src = tag.get('src') or tag.get('href')
        if src:
            resource_url = urljoin(url, src)
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
    new_site = requests.get(url).content
    soup = BeautifulSoup(new_site, 'html.parser')
    new_resource_hashes = {}

    # Obliczenie nowego hashu kodu HTML
    new_hash = hashlib.sha256(new_site).hexdigest()
    new_resource_hashes[url] = new_hash

    # Obliczenie nowych hashy wszystkich pozostałych zasobów
    for tag in soup.find_all(['img', 'link', 'script']):
        src = tag.get('src') or tag.get('href')
        if src:
            resource_url = urljoin(url, src)
            try:
                resource = requests.get(resource_url).content
                resource_hash = hashlib.sha256(resource).hexdigest()
                new_resource_hashes[resource_url] = resource_hash
            except requests.exceptions.RequestException as e:
                print(e)
                continue

    # Porównanie nowych hashy z przechowywanymi hashami
    with open("website_hashes.txt", "r") as f:
        stored_hashes = eval(f.read())
    for resource_url, new_hash in new_resource_hashes.items():
        if resource_url not in stored_hashes or new_hash != stored_hashes[resource_url]:
            print("ALERT: Zasób {} został zmieniony!".format(resource_url))
    else:
        print("Strona jest bezpieczna.")


check_website("https://www.wp.pl")
