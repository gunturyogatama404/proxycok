import requests
import re

# Regex untuk memvalidasi format ip:port
ip_port_pattern = re.compile(r"^\d{1,3}(\.\d{1,3}){3}:\d{2,5}$")

# Fungsi untuk membaca daftar URL dari file
def load_urls(file_name):
    try:
        with open(file_name, "r", encoding="utf-8") as file:
            urls = [line.strip() for line in file if line.strip()]
        return urls
    except FileNotFoundError:
        print(f"File {file_name} not found.")
        return []

# Fungsi untuk scrape, filter, dan simpan ke satu file
def scrape_and_save_to_allproxy(urls, output_file):
    proxies_set = set()  # Gunakan set untuk otomatis menghapus duplikat
    for url in urls:
        try:
            print(f"Fetching data from: {url}")
            response = requests.get(url, timeout=10)
            response.raise_for_status()  # Memastikan tidak ada error dari HTTP
            
            # Filter hanya baris yang sesuai dengan format ip:port
            proxies = response.text.splitlines()
            valid_proxies = [proxy for proxy in proxies if ip_port_pattern.match(proxy)]
            
            # Tambahkan ke set untuk menghapus duplikat
            proxies_set.update(valid_proxies)
            print(f"Valid proxies from {url} added to the set.")
        except requests.exceptions.RequestException as e:
            print(f"Failed to fetch {url}: {e}")
    
    # Tulis semua proxy unik ke file output
    with open(output_file, "w", encoding="utf-8") as all_file:
        all_file.write("\n".join(sorted(proxies_set)) + "\n")
    print(f"All unique proxies saved to {output_file}")

# Nama file input dan output
url_list_file = "url_list.txt"
output_file = "allproxy.txt"

# Muat URL dari file dan jalankan scraping
urls = load_urls(url_list_file)
if urls:
    scrape_and_save_to_allproxy(urls, output_file)
else:
    print("No URLs to process. Please check your url_list.txt file.")
