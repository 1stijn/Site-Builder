import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from tqdm import tqdm

def check_mobile_compatibility(url):
    try:
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=375x667")  

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.get(url)
        time.sleep(2)

        try:
            viewport = driver.find_element(By.CSS_SELECTOR, "meta[name='viewport']")
            if 'width=device-width' in viewport.get_attribute('content'):
                result = f"{url} is mobile-compatible (has viewport meta tag)"
            else:
                result = f"{url} is NOT mobile-compatible (viewport meta tag missing proper content)"
        except:
            result = f"{url} is NOT mobile-compatible (no viewport meta tag found)"

        driver.quit()
        return result

    except Exception as e:
        return f"Error checking {url}: {str(e)}"

def check_urls_in_file(file_path, output_file="mobile_compatibility_results.txt"):
    with open(file_path, 'r') as file:
        urls = file.readlines()

    with open(output_file, 'w') as file:  
        for url in tqdm(urls, desc="Checking URLs", unit="url"):
            url = url.strip()
            if url:
                result = check_mobile_compatibility(url)
                file.write(result + '\n')  

if __name__ == "__main__":
    input_file = input("Enter file path: ")
    check_urls_in_file(input_file)
    print("Mobile compatibility check complete. Results saved to 'mobile_compatibility_results.txt'.")
