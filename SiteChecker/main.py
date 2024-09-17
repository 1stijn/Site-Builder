import requests
from bs4 import BeautifulSoup
import json
from tqdm import tqdm
from urllib.parse import urlparse, urljoin
import xml.etree.ElementTree as ET
import os
import time

def clear_console():
    os.system('clear' if os.name != 'nt' else 'cls')

def has_content(soup):
    return bool(soup.find('h1') or soup.find('h2') or soup.find('h3') or soup.find('p'))

def extract_domain(url):
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    domain = domain.lstrip('www.')
    domain = domain.replace('.', '_')
    return domain

def normalize_url(url):
    parsed_url = urlparse(url)
    if not parsed_url.scheme:
        url = 'https://' + url  
    return urlparse(url).geturl()

def get_base_url(url):
    parsed_url = urlparse(url)
    return f"{parsed_url.scheme}://{parsed_url.netloc}"


def try_sitemap_url(url):
    sitemap_paths = ['/sitemap.xml', '/sitemap_index.xml', '/sitemap1.xml', '/sitemap2.xml', 
                     '/sitemap_main.xml', '/sitemap-news.xml', '/sitemap-products.xml']
    
    if check_sitemap(url):
        return url

    base_url = get_base_url(url)  
    for path in sitemap_paths:
        full_url = urljoin(base_url, path)
        if check_sitemap(full_url):
            return full_url

    parsed_url = urlparse(url)
    path_parts = parsed_url.path.split('/')
    for i in range(len(path_parts)-1, 0, -1):
        stripped_url = urljoin(f"{parsed_url.scheme}://{parsed_url.netloc}", '/'.join(path_parts[:i]))
        for path in sitemap_paths:
            full_url = urljoin(stripped_url, path)
            if check_sitemap(full_url):
                return full_url

    return None

def get_tag_count(soup, tag_list):
    tag_counts = {tag: len(soup.find_all(tag)) for tag in tag_list}
    return tag_counts

def compare_files(old_file, new_file):
    try:
        with open(old_file, 'r') as file:
            old_urls = file.readlines()

        with open(new_file, 'r') as file:
            new_urls = file.readlines()

        if len(old_urls) != len(new_urls):
            print("The number of URLs in both files does not match. Cannot proceed.")
            return

        tag_list = [
            'html', 'head', 'title', 'body', 'header', 'footer', 'div', 'p', 
            'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'span', 'img', 'a', 'video', 
            'audio', 'iframe', 'ul', 'ol', 'li', 'table', 'tr', 'td', 'th', 
            'thead', 'tbody', 'tfoot', 'form', 'input', 'textarea', 'button', 
            'select', 'option', 'article', 'section', 'nav', 'aside', 'main', 
            'strong', 'em', 'br', 'hr', 'blockquote', 'code', 'pre', 'script', 
            'link'
        ]
        comparison_results = {}

        total_urls = len(old_urls)
        with tqdm(total=total_urls, desc="Comparing URLs", unit="url") as pbar:
            for i, (old_url, new_url) in enumerate(zip(old_urls, new_urls)):
                old_url, new_url = old_url.strip(), new_url.strip()
                
                try:
                    old_response = requests.get(old_url)
                    new_response = requests.get(new_url)
                    old_response.raise_for_status()
                    new_response.raise_for_status()

                    old_soup = BeautifulSoup(old_response.text, 'html.parser')
                    new_soup = BeautifulSoup(new_response.text, 'html.parser')

                    old_tag_counts = get_tag_count(old_soup, tag_list)
                    new_tag_counts = get_tag_count(new_soup, tag_list)

                    comparison_results[f"URL {i+1}: {old_url} vs {new_url}"] = {
                        "Old": old_tag_counts,
                        "New": new_tag_counts
                    }

                except requests.RequestException as e:
                    print(f"Error fetching URLs {old_url} or {new_url}: {e}")
                    continue

                pbar.update(1)

        comparison_filename = 'comparison_results.json'
        with open(comparison_filename, 'w') as json_file:
            json.dump(comparison_results, json_file, indent=4)

        print(f"Comparison results saved to {comparison_filename}.")

    except FileNotFoundError:
        print(f"One or both of the files {old_file} and {new_file} do not exist.")
    except Exception as e:
        print(f"An error occurred during comparison: {e}")

def check_sitemap(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        if 'xml' in response.headers.get('Content-Type', ''):
            return True
    except requests.RequestException:
        pass
    return False

def scrape_sitemap(sitemap_url):
    try:
        sitemap_url = normalize_url(sitemap_url)
        final_sitemap_url = try_sitemap_url(sitemap_url)

        if final_sitemap_url is None:
            print("No valid sitemap found at the given URL or common sitemap paths.")
            return []

        sitemap_urls = [final_sitemap_url]
        response = requests.get(final_sitemap_url)
        response.raise_for_status()

        try:
            root = ET.fromstring(response.content)
            urls = set()

            for sitemap in root.findall('.//{*}sitemap'):
                loc = sitemap.find('{*}loc').text
                if loc:
                    sitemap_urls.append(loc)

            for url in root.findall('.//{*}url'):
                loc = url.find('{*}loc').text
                if loc:
                    urls.add(loc)

            total_sitemaps = len(sitemap_urls)
            total_urls = len(urls)

            print(f"Processing {total_sitemaps} sitemaps...")
            with tqdm(total=total_urls, desc="Processing URLs", unit="url") as pbar:
                for sitemap in sitemap_urls:
                    if sitemap != final_sitemap_url:
                        response = requests.get(sitemap)
                        response.raise_for_status()
                        try:
                            root = ET.fromstring(response.content)
                            for url in root.findall('.//{*}url'):
                                loc = url.find('{*}loc').text
                                if loc:
                                    urls.add(loc)
                                    pbar.update(1)
                        except ET.ParseError as e:
                            print(f"Error parsing XML from {sitemap}: {e}")

            return list(urls)
        except ET.ParseError as e:
            print(f"Error parsing XML from {final_sitemap_url}: {e}")
            return []

    except requests.RequestException as e:
        print(f"Error fetching sitemap {sitemap_url}: {e}")
        return []

def check_urls(file_path):
    has_content_urls = []
    no_content_urls = []
    errors = []

    try:
        with open(file_path, 'r') as file:
            urls = file.readlines()

        if not urls:
            print("No URLs found in the file.")
            return

        first_url = urls[0].strip()
        domain_name = extract_domain(first_url)
        output_filename = f'{domain_name}_results.json'

        total_urls = len(urls)
        print(f"Processing {total_urls} URLs...")

        with tqdm(total=total_urls, desc="Processing URLs", unit="url") as pbar:
            for url in urls:
                url = url.strip()
                if not url:
                    pbar.update(1)
                    continue
                
                try:
                    response = requests.get(url)
                    response.raise_for_status()  
                    
                    soup = BeautifulSoup(response.text, 'html.parser')

                    if has_content(soup):
                        has_content_urls.append(url)
                    else:
                        no_content_urls.append(url)

                except requests.RequestException as e:
                    errors.append(f"Error fetching {url}: {e}")

                pbar.update(1)

        result = {
            "has content": has_content_urls,
            "has no content": no_content_urls
        }

        with open(output_filename, 'w') as json_file:
            json.dump(result, json_file, indent=4)

        print(f"Results have been written to {output_filename}.")

        if errors:
            print("\nErrors encountered during processing:")
            for error in errors:
                print(error)

    except FileNotFoundError:
        print(f"The file {file_path} does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")

def display_ascii_art():
    art = """
   ▄████████     ███      ▄█       ▄█ ███▄▄▄▄         ▄█        ▄█  ▀█████████▄  
  ███    ███ ▀█████████▄ ███      ███ ███▀▀▀██▄      ███       ███    ███    ███ 
  ███    █▀     ▀███▀▀██ ███▌     ███ ███   ███      ███       ███▌   ███    ███ 
  ███            ███   ▀ ███▌     ███ ███   ███      ███       ███▌  ▄███▄▄▄██▀  
▀███████████     ███     ███▌     ███ ███   ███      ███       ███▌ ▀▀███▀▀▀██▄  
         ███     ███     ███      ███ ███   ███      ███       ███    ███    ██▄ 
   ▄█    ███     ███     ███      ███ ███   ███      ███▌    ▄ ███    ███    ███ 
 ▄████████▀     ▄████▀   █▀   █▄ ▄███  ▀█   █▀       █████▄▄██ █▀   ▄█████████▀  
                              ▀▀▀▀▀▀                 ▀                           
                                                
                                                - @Stijn
    """
    print(art)

def main_menu():
    while True:
        clear_console()
        display_ascii_art()
        print("\nSelect an option:")
        print("1) Scrape Sitemap")
        print("2) Check Empty Pages")
        print("4) Compare Two Files for Missing Tags")
        print("X) Exit")

        choice = input("Enter your choice (1/2/3): ")

        if choice == '1':
            sitemap_url = input("Enter the sitemap URL (e.g., https://example.com/sitemap.xml): ")
            sitemap_urls = scrape_sitemap(sitemap_url)

            if sitemap_urls:
                domain_name = extract_domain(sitemap_url)
                sitemap_filename = f'{domain_name}_results.json'
                with open(sitemap_filename, 'w') as json_file:
                    json.dump({"sitemap": sitemap_urls}, json_file, indent=4)
                print(f"Sitemap URLs have been written to {sitemap_filename}.")
            else:
                print("No URLs found in the sitemap.")
            input("Press Enter to return to the main menu...")
        elif choice == '2':
            file_path = input("Enter the path to the file containing URLs: ")
            check_urls(file_path)
            input("Press Enter to return to the main menu...")
        elif choice == 'x'.lower():
            print("Exiting...")
            break
        elif choice == '4':
            old_file = input("Enter the path to the first file (Old version): ")
            new_file = input("Enter the path to the second file (New version): ")
            compare_files(old_file, new_file)
            input("Press Enter to return to the main menu...")

        else:
            print("Invalid choice. Please select 1, 2, or 3.")
            time.sleep(1)

if __name__ == "__main__":
    main_menu()
