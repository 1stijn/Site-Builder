import requests
import time
import sys
import platform
import json
import xml.etree.ElementTree as ET
import os
import colorama
from tqdm import tqdm
from urllib.parse import urlparse, urljoin
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from bs4 import BeautifulSoup
from colorama import Fore, Style, init

def set_terminal_size():
    title = "▬▬ι═══════ﺤ / Stijn's Lib \\ ▄︻デ══━一"

    if platform.system() == 'Darwin':
        os.system('printf "\\e[8;55;87t"')
        os.system(f'echo -n -e "\\033]0;{title}\\007"')

    elif platform.system() == 'Windows':
        os.system('mode con: cols=87 lines=55')
        os.system(f'title {title}')

set_terminal_size()

init(autoreset=True)

def clear_console():
    print("\033c", end="")

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

def try_sitemap_url(url): #243 sitemaps, more will follow =)
    sitemap_paths = [ 
        '/sitemap.xml', '/sitemap_index.xml', '/sitemap1.xml', '/sitemap2.xml',
        '/sitemap_main.xml', '/sitemap-news.xml', '/sitemap-products.xml', 
        '/sitemap-posts.xml', '/sitemap-pages.xml', '/sitemap-category.xml', 
        '/sitemap-tags.xml', '/sitemap-articles.xml', '/sitemap-blog.xml', 
        '/sitemap-content.xml', '/sitemap-blog-posts.xml', '/sitemap-categories.xml',
        '/sitemap-subpages.xml', '/sitemap-media.xml', '/sitemap-videos.xml',
        '/sitemap-images.xml', '/sitemap-events.xml', '/sitemap-reviews.xml',
        '/sitemap-recent.xml', '/sitemap-directory.xml', '/sitemap-products-pages.xml',
        '/sitemap-services.xml', '/sitemap-team.xml', '/sitemap-locations.xml',
        '/sitemap-faq.xml', '/sitemap-guides.xml', '/sitemap-tutorials.xml',
        '/sitemap-portfolio.xml', '/sitemap-case-studies.xml', '/sitemap-testimonials.xml',
        '/sitemap-offers.xml', '/sitemap-promotions.xml', '/sitemap-specials.xml',
        '/sitemap-announcements.xml', '/sitemap-updates.xml', '/sitemap-newsletters.xml',
        '/sitemap-archive.xml', '/sitemap-releases.xml', '/sitemap-podcasts.xml',
        '/sitemap-interviews.xml', '/sitemap-quizzes.xml', '/sitemap-resources.xml',
        '/sitemap-demos.xml', '/sitemap-partners.xml', '/sitemap-jobs.xml',
        '/sitemap-careers.xml', '/sitemap-press.xml', '/sitemap-books.xml',
        '/sitemap-wholesale.xml', '/sitemap-distributors.xml', '/sitemap-brands.xml',
        '/sitemap-subscriptions.xml', '/sitemap-latest.xml', '/sitemap-featured.xml',
        '/sitemap-galleries.xml', '/sitemap-downloads.xml', '/sitemap-links.xml',
        '/sitemap-events-list.xml', '/sitemap-news-archive.xml', '/sitemap-upcoming.xml',
        '/sitemap-sales.xml', '/sitemap-trends.xml', '/sitemap-papers.xml',
        '/sitemap-workshops.xml', '/sitemap-webinars.xml', '/sitemap-research.xml',
        '/sitemap-articles-list.xml', '/sitemap-reports.xml', '/sitemap-podcasts-list.xml',
        '/sitemap-videos-list.xml', '/sitemap-ebooks.xml', '/sitemap-patents.xml',
        '/sitemap-standards.xml', '/sitemap-guides-list.xml', '/sitemap-tutorials-list.xml',
        '/sitemap-seminars.xml', '/sitemap-conferences.xml', '/sitemap-courses.xml',
        '/sitemap-summits.xml', '/sitemap-articles-summary.xml', '/sitemap-news-summary.xml',
        '/sitemap-features.xml', '/sitemap-topics.xml', '/sitemap-discussions.xml',
        '/sitemap-articles-featured.xml', '/sitemap-resources-list.xml', '/sitemap-tools.xml',
        '/sitemap-software.xml', '/sitemap-hardware.xml', '/sitemap-inventory.xml',
        '/sitemap-services-list.xml', '/sitemap-products-list.xml', '/sitemap-brands-list.xml',
        '/sitemap-affiliates.xml', '/sitemap-discounts.xml', '/sitemap-coupons.xml',
        '/sitemap-promotions-list.xml', '/sitemap-articles-updated.xml', '/sitemap-reviews-list.xml',
        '/sitemap-articles-recent.xml', '/sitemap-top-reviews.xml', '/sitemap-case-studies-list.xml',
        '/sitemap-books-list.xml', '/sitemap-wholesale-list.xml', '/sitemap-distributors-list.xml',
        '/sitemap-subscriptions-list.xml', '/sitemap-latest-news.xml', '/sitemap-featured-posts.xml',
        '/sitemap-guides-updated.xml', '/sitemap-tutorials-updated.xml', '/sitemap-events-upcoming.xml',
        '/sitemap-news-releases.xml', '/sitemap-press-releases.xml', '/sitemap-articles-published.xml',
        '/sitemap-articles-archived.xml', '/sitemap-podcast-episodes.xml', '/sitemap-video-episodes.xml',
        '/sitemap-podcasts-recent.xml', '/sitemap-webinars-upcoming.xml', '/sitemap-courses-list.xml',
        '/sitemap-seminars-upcoming.xml', '/sitemap-articles-archived.xml', '/sitemap-reports-updated.xml',
        '/sitemap-research-papers.xml', '/sitemap-guides-recent.xml', '/sitemap-tutorials-recent.xml',
        '/sitemap-updates-recent.xml', '/sitemap-upcoming-events.xml', '/sitemap-coupons-list.xml',
        '/sitemap-affiliates-list.xml', '/sitemap-discounts-list.xml', '/sitemap-new-products.xml',
        '/sitemap-featured-products.xml', '/sitemap-press-releases-recent.xml', '/sitemap-case-studies-updated.xml',
        '/sitemap-book-reviews.xml', '/sitemap-featured-books.xml', '/sitemap-latest-research.xml',
        '/sitemap-upcoming-releases.xml', '/sitemap-latest-guides.xml', '/sitemap-trending.xml',
        '/sitemap-latest-releases.xml', '/sitemap-video-tutorials.xml', '/sitemap-ebooks-list.xml',
        '/sitemap-news-features.xml', '/sitemap-research-updated.xml', '/sitemap-articles-recent.xml',
        '/sitemap-recent-guides.xml', '/sitemap-recent-tutorials.xml', '/sitemap-podcast-releases.xml',
        '/sitemap-webinars-recent.xml', '/sitemap-seminars-recent.xml', '/sitemap-upcoming-research.xml',
        '/sitemap-recent-papers.xml', '/sitemap-latest-webinars.xml', '/sitemap-featured-courses.xml',
        '/sitemap-archive-updated.xml', '/sitemap-podcast-recent.xml', '/sitemap-webinar-archives.xml',
        '/sitemap-guide-archives.xml', '/sitemap-tutorial-archives.xml', '/sitemap-news-features-recent.xml',
        '/sitemap-research-recent.xml', '/sitemap-event-archives.xml', '/sitemap-latest-updates.xml',
        '/sitemap-coupons-recent.xml', '/sitemap-affiliates-recent.xml', '/sitemap-discounts-recent.xml',
        '/sitemap-new-releases.xml', '/sitemap-featured-releases.xml', '/sitemap-book-categories.xml',
        '/sitemap-research-categories.xml', '/sitemap-tutorial-categories.xml', '/sitemap-guide-categories.xml',
        '/sitemap-webinar-categories.xml', '/sitemap-event-categories.xml', '/sitemap-podcast-categories.xml',
        '/sitemap-video-categories.xml', '/sitemap-product-categories.xml', '/sitemap-service-categories.xml',
        '/sitemap-team-categories.xml', '/sitemap-case-study-categories.xml', '/sitemap-featured-case-studies.xml',
        '/sitemap-press-categories.xml', '/sitemap-papers-categories.xml', '/sitemap-book-collections.xml',
        '/sitemap-research-collections.xml', '/sitemap-tutorial-collections.xml', '/sitemap-guide-collections.xml',
        '/sitemap-webinar-collections.xml', '/sitemap-event-collections.xml', '/sitemap-podcast-collections.xml',
        '/sitemap-video-collections.xml', '/sitemap-product-collections.xml', '/sitemap-service-collections.xml',
        '/sitemap-team-collections.xml', '/sitemap-case-study-collections.xml', '/sitemap-featured-case-studies-list.xml',
        '/sitemap-press-releases-list.xml', '/sitemap-papers-collections.xml', '/sitemap-research-summaries.xml',
        '/sitemap-tutorial-summaries.xml', '/sitemap-guide-summaries.xml', '/sitemap-webinar-summaries.xml',
        '/sitemap-event-summaries.xml', '/sitemap-podcast-summaries.xml', '/sitemap-video-summaries.xml',
        '/sitemap-product-summaries.xml', '/sitemap-service-summaries.xml', '/sitemap-team-summaries.xml',
        '/sitemap-case-study-summaries.xml', '/sitemap-featured-case-studies-summaries.xml', '/sitemap-press-releases-summaries.xml',
        '/sitemap-papers-summaries.xml', '/sitemap-book-summaries.xml', '/sitemap-research-summaries.xml',
        '/sitemap-tutorial-summaries.xml', '/sitemap-guide-summaries.xml', '/sitemap-webinar-summaries.xml',
        '/sitemap-event-summaries.xml', '/sitemap-podcast-summaries.xml', '/sitemap-video-summaries.xml',
        '/sitemap-product-summaries.xml', '/sitemap-service-summaries.xml', '/sitemap-team-summaries.xml',
        '/sitemap-case-study-summaries.xml', '/sitemap-featured-case-studies-summaries.xml', '/sitemap-press-releases-summaries.xml',
        '/sitemap-papers-summaries.xml', '/sitemap-book-collections-list.xml', '/sitemap-research-collections-list.xml',
        '/sitemap-tutorial-collections-list.xml', '/sitemap-guide-collections-list.xml', '/sitemap-webinar-collections-list.xml',
        '/sitemap-event-collections-list.xml', '/sitemap-podcast-collections-list.xml', '/sitemap-video-collections-list.xml',
        '/sitemap-product-collections-list.xml', '/sitemap-service-collections-list.xml', '/sitemap-team-collections-list.xml',
        '/sitemap-case-study-collections-list.xml', '/sitemap-featured-case-studies-list.xml', '/sitemap-press-releases-list.xml'
    ]

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

import json

def extract_urls_from_json(input_file):
    try:
        with open(input_file, 'r') as file:
            data = json.load(file)

        if "sitemap" in data and isinstance(data["sitemap"], list):
            return data["sitemap"]
        else:
            print(f"'sitemap' key not found or is not a list in {input_file}")
            return []

    except FileNotFoundError:
        print(f"The file {input_file} was not found.")
        return []
    except json.JSONDecodeError:
        print(f"The file {input_file} is not a valid JSON file.")
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

class FileChangeHandler(FileSystemEventHandler):
    def process(self, event):
        if event.is_directory:
            return

        if event.event_type == 'created':
            print(f"{Fore.GREEN}―――ι═══════ﺤ @ file ADDED: {event.src_path}")
        elif event.event_type == 'deleted':
            print(f"{Fore.RED}―――ι═══════ﺤ @ file DELETED: {event.src_path}")
        elif event.event_type == 'modified':
            print(f"{Fore.YELLOW}―――ι═══════ﺤ @ file EDITED: {event.src_path}")

    def on_modified(self, event):
        self.process(event)
    
    def on_created(self, event):
        self.process(event)
    
    def on_deleted(self, event):
        self.process(event)

def start_monitoring(path):
    event_handler = FileChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

def display_ascii_art():
    print(Fore.RED + """
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⣗⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣹⠿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⡿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⡿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⡿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠐⢶⣤⡠⡀⠀⠀⠀⠀⠀⠀⠀⢠⣿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠈⠛⠳⠦⣄⣤⣤⣼⣴⡿⡏⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠋⢿⣿⣾⣿⣿⣅⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡟⣯⢻⣟⠏⠛⠳⢤⣄⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⡿⣿⡾⠁⠀⠀⠀⠀⠀⠙⠓⠷⣤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣔⣱⡃⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠴⢜⡢⠄⠀⠀⠀⠀⠀⢰⣛⣿⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⡄⠀⠀⠀⠀⠀⢀⣿⠷⣻⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⢿⣾⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⣦⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡜⠁⢾⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡃⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⡿⠃⡜⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠇⠀⠀⠀⠀⠀⠀⠀⠀⢠⢯⡷⡰⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⠀⠀⠀⠀⠀⠀⠀⢀⢏⡾⡷⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡄⠀⠀⠀⠸⠀⢀⣄⠀⠀⠀⢀⣾⣿⢉⠃⠀⠀⠀⠀⠀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠺⠍⠁⠀⠀⠐⠀⠀⣋⠀⠀⠀⣼⣴⣻⠇⠀⠀⠀⠀⠀⡄⠁⠀⠀⠀⠀⡆⢀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡄⠀⠀⢃⠄⣸⣿⠿⡗⠀⢠⠀⠀⠀⠆⠀⠀⠀⠀⠀⠘⡋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠐⡄⠀⠀⠀⠀⠀⡀⠀⠀⡀⠀⠀⠀⡀⣰⣿⢭⡝⠁⠈⠛⠁⠰⠁⠀⠀⠀⠀⠀⠀⠀⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⠘⠈⣠⡅⢀⠰⠀⣦⡏⢛⠦⠃⡀⠀⠀⠜⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠐⠀⠀⠙⠀⠐⡈⡠⠌⠀⠼⠉⣵⢼⠛⠀⠁⡠⠂⡀⠶⠂⠀⠒⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⢀⠔⠣⠁⢀⠢⠂⠣⠄⣀⣉⢨⠰⠁⠀⡅⠔⠀⠄⢀⠀⠀⠀⠚⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣆⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠈⠀⠀⠀⡀⠀⠈⡀⠈⠅⡀⠀⡆⠀⣸⢃⠃⠢⠃⠀⠈⠀⠀⠷⠔⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠄⠉⠁⢂ - @stijn ▄︻デ══━一 ?
⠀⠀⠀⠀⠀⠀⠀⠀⡐⢤⠃⠘⡋⠐⠁⠼⢞⠈⡞⠁⠴⠖⢠⡘⠀⠈⠏⠀⠤⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁⡕⡂⠃⠠⠠⠈
⠀⠀⠀⠀⠀⠀⠐⠀⠏⠘⠀⠀⠀⠆⡠⣄⠜⢀⡀⣁⡀⠁⠈⠀⣀⠀⠥⠀⠒⠒⠂⠀⠀⠭⠉⠙⣻⣿⣶⠄⠠⠠⠤⠤⠀⠀⠀⠀⠀⠒⠒⠚⢒⠚⠛⠻⠽⠛⠛⠒⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣠⠐⣶⠂⠈⢳⢄⡠⠉⢠⠀⢰⠀⠜⠅⠈⠁⠀⠀⠀⠄⠀⠀⠀⠀⠈⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠂⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⢀⢨⠀⠊⣸⠞⣠⠘⣧⢸⠘⡀⠘⠃⠤⠀⠈⢌⠨⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⣠⠀⠀⠐⢠⣎⠪⢀⣁⠒⠳⢸⠠⣗⢶⠂⢀⠀⡀⠀⡈⠀⠀⠈⠀⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠐⠇⠀⠀⠀⠈⠠⠀⠈⢈⣯⠖⣞⠃⠀⠀⢸⠀⢠⠘⢀⠁⢀⠂⠢⠁⠀⠀⠛⠀⠀⠀⠀⠐⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⡠⠀⠉⠀⠀⠀⠀⠊⠁⣠⢃⠁⠶⢠⢸⠀⠆⠈⠀⠣⠁⠁⠀⠀⠀⠀⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠘⠀⢀⣯⣧⡞⠁⡌⠀⠀⣦⢸⠀⢀⠀⢁⠀⢀⠀⠁⠀⠀⠑⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⣼⣿⠟⠀⠠⠀⠀⠀⠀⠀⠀⢘⠀⠀⠀⠈⢁⠀⠀⠀⠀⠈⠀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠐⢮⠗⠒⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⣼⣿⠃⠀⠀⠀⠀⠀⠁⠀⠀⠀⢘⠀⠀⠀⠀⠈⠂⠀⠀⠀⠀⠀⠈⢀⠀⠀⠀⠀⠀⠀⠀⠀⠈⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⢀⡿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠨⠀⠀⠀⠀⠀⠈⠀⠀⠀⣴⡀⠀⠀⠐⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠈⠀⠀⠀⠀⠀⡀⠀⠀⠀⠀⠀⠀⠀⡀⠀⠀⠀⠀⠀⠠⠄⠀⠸⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⡏⠁⠀⠀⠀⠀⠀⠀⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀

    """)  

def custom_input(prompt):
    return input(Fore.RED + "▬▬ι═══════ﺤ @ " + prompt + Fore.WHITE)

def get_links_from_page(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        links = [a.get('href') for a in soup.find_all('a', href=True)]
        
        links_data = {url: {"total links": len(links)}}
        for idx, link in enumerate(links, 1):
            links_data[url][idx] = link

        return links_data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return {}

def load_existing_data(filename):
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                print("Error decoding JSON file. Starting with empty data.")
                return {}
    return {}

import json
import os

def load_existing_data(filename):
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            return json.load(file)
    else:
        return {}

def load_existing_data(filename):
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            return json.load(file)
    else:
        return {}

def save_links_to_json(new_links_data, filename='links.json'):
    existing_data = load_existing_data(filename)
    
    if isinstance(new_links_data, dict):
        for url, links in new_links_data.items():
            if url not in existing_data:
                existing_data[url] = {"total links": len(links)}
            
            for index, link in enumerate(links, start=1):
                existing_data[url][str(index)] = link

    elif isinstance(new_links_data, list):
        if 'url' in existing_data:
            existing_data['url']["total links"] = len(new_links_data)
            for index, link in enumerate(new_links_data, start=1):
                existing_data['url'][str(index)] = link
        else:
            existing_data['url'] = {"total links": len(new_links_data)}
            for index, link in enumerate(new_links_data, start=1):
                existing_data['url'][str(index)] = link
                
    else:
        raise ValueError("new_links_data must be a dictionary or list.")
    
    with open(filename, 'w') as file:
        json.dump(existing_data, file, indent=4)

def link_scraping_menu():
    while True:
        mode = custom_input("Enter '1' to scrape a URL, '2' from a text file, or 'x' to stop: ")
        
        if mode.lower() == 'x':
            print("Exiting the link scraping.")
            break
        
        if mode == '1':
            url = custom_input("Enter the URL to scrape (type 'x' to stop): ")
            
            if url.lower() == 'x':
                print("Exiting the link scraping.")
                break
            
            new_links_data = get_links_from_page(url)
            
            if new_links_data:
                save_links_to_json(new_links_data, 'links.json')
                print(f"Links from '{url}' added to 'links.json'")
            else:
                print("No links found or error occurred.")
                
        elif mode == '2':
            file_path = custom_input("Enter the path to the text file containing URLs: ")
            
            try:
                with open(file_path, 'r') as file:
                    urls = file.readlines()
                
                all_links_data = []
                
                total_urls = len(urls)
                with tqdm(total=total_urls, desc="Scraping URLs", unit="url") as pbar:
                    for url in urls:
                        url = url.strip()
                        if url:
                            new_links_data = get_links_from_page(url)
                            
                            if new_links_data:
                                all_links_data.extend(new_links_data)
                        
                        pbar.update(1)

                if all_links_data:
                    save_links_to_json(all_links_data, 'links.json')
                    print("All links from the file have been added to 'links.json'.")
                else:
                    print("No links were found in the URLs provided.")
            
            except FileNotFoundError:
                print(f"The file '{file_path}' was not found.")
            except Exception as e:
                print(f"An error occurred: {e}")
        
        else:
            print("Invalid option. Please enter '1' or '2', or 'x'.")

def main_menu():
    while True:
        clear_console()
        display_ascii_art()
        print(Fore.RED + "\nSelect an option:")
        print(Fore.RED + "1) Scrape Sitemap")
        print(Fore.RED + "2) Check Empty Pages")
        print(Fore.RED + "3) Compare Two Files for Missing Tags")
        print(Fore.RED + "4) Extract JSON to raw text for your files")
        print(Fore.RED + "5) Scrape Links from a Webpage")
        print(Fore.RED + "6) File path watchdog")
        print(Fore.RED + "X) Exit")
        
        choice = custom_input("Enter your choice: ")

        if choice == '1':
            sitemap_url = custom_input("Enter the sitemap URL (e.g., https://example.com/sitemap.xml): ")
            sitemap_urls = scrape_sitemap(sitemap_url)

            if sitemap_urls:
                domain_name = extract_domain(sitemap_url)
                sitemap_filename = f'{domain_name}_results.json'
                with open(sitemap_filename, 'w') as json_file:
                    json.dump({"sitemap": sitemap_urls}, json_file, indent=4)
                print(f"Sitemap URLs have been written to {sitemap_filename}.")
            else:
                print("No URLs found in the sitemap.")
            custom_input("Press Enter to return to the main menu...")
        
        elif choice == '2':
            file_path = custom_input("Enter the path to the file containing URLs: ")
            check_urls(file_path)
            custom_input("Press Enter to return to the main menu...")
        
        elif choice == '3':
            old_file = custom_input("Enter the path to the first file (Old version): ")
            new_file = custom_input("Enter the path to the second file (New version): ")
            compare_files(old_file, new_file)
            custom_input("Press Enter to return to the main menu...")
        
        elif choice == '4':
            input_file = custom_input("Enter the path to the JSON file: ")
            urls = extract_urls_from_json(input_file)
                
            if urls:
                output_file = f"extracted_urls_{extract_domain(input_file)}.txt"
                with open(output_file, 'w') as f:
                    for url in urls:
                        f.write(url + "\n")
                print(f"URLs extracted and saved to {output_file}.")
            else:
                print("No URLs found or an error occurred.")
                
            custom_input("Press Enter to return to the main menu...")

        elif choice == '5':
            link_scraping_menu()
            custom_input("Press Enter to return to the main menu...")

        elif choice == '6':
            url = custom_input("Enther path to watchdog: ")
            start_monitoring(url)
            custom_input("Press Enter to return to the main menu...")


        elif choice.lower() == 'x':
            print(Fore.RED + "Exiting...")
            break

        else:
            print(Fore.RED + "Invalid choice. Please select a valid option.")
            time.sleep(1)

if __name__ == "__main__":
    main_menu()
