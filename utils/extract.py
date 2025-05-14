import requests
from bs4 import BeautifulSoup

HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                    "(KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
    }

def extract_product_data(product):
    """Mengekstrak data produk fashion dari satu elemen produk."""
    try:
        title_element = product.find('h3', class_='product-title')
        price_element = product.find('span', class_='price')
        colors_element = product.find('p', string=lambda text: "Colors" in text)
        size_element = product.find('p', string=lambda text: "Size" in text)
        gender_element = product.find('p', string=lambda text: "Gender" in text)

        title = title_element.text.strip() if title_element else None
        price = price_element.text.strip() if price_element else None
        colors = colors_element.text.strip().replace("Colors", "").strip() if colors_element else None
        size = size_element.text.strip().replace("Size :", "").strip() if size_element else None
        gender = gender_element.text.strip().replace("Gender :", "").strip() if gender_element else None

        return {
            "Title": title,
            "Price": price,
            "Colors": colors,
            "Size": size,
            "Gender": gender
        }
    except AttributeError as e:
        print(f"Error extracting data from a product: {e}")
        return None

def fetch_page_content(url):
    """Mengambil konten HTML dari URL dengan user-agent."""
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        return response.content
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

def extract_fashion_data(url, num_pages=50):
    """Mengekstrak data produk fashion dari semua halaman."""
    all_data = []
    for page_number in range(1, num_pages + 1):
        page_url = f"{url}?page={page_number}"
        content = fetch_page_content(page_url)
        if not content:
            print(f"Failed to fetch page {page_number}. Stopping extraction.")
            break

        soup = BeautifulSoup(content, 'html.parser')
        product_list = soup.find_all('div', class_='collection-card')

        if not product_list:
            print(f"No products found on page {page_number}. Stopping extraction.")
            break

        for product in product_list:
            product_data = extract_product_data(product)
            if product_data:
                all_data.append(product_data)
        print(f"Successfully extracted data from page {page_number}")
    return all_data
