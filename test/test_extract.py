import unittest
from unittest.mock import patch
from bs4 import BeautifulSoup
from utils.extract import extract_product_data, fetch_page_content, extract_fashion_data

class TestExtract(unittest.TestCase):

    def test_extract_product_data_valid(self):
        product_html = """
        <div class="collection-card">
            <div class="product-details">
                <h3 class="product-title">Test Product</h3>
                <div class="price-container">
                    <span class="price">$25.00</span>
                </div>
                <p style="font-size: 14px; color: #777;">3 Colors</p>
                <p style="font-size: 14px; color: #777;">Size : S</p>
                <p style="font-size: 14px; color: #777;">Gender : Female</p>
            </div>
        </div>
        """
        soup = BeautifulSoup(product_html, 'html.parser')
        product = soup.find('div', class_='collection-card').find('div', class_='product-details')
        expected_data = {'Title': 'Test Product', 'Price': '$25.00', 'Colors': '3', 'Size': 'S', 'Gender': 'Female'}
        self.assertEqual(extract_product_data(product), expected_data)

    def test_extract_product_data_missing_elements(self):
        product_html = """
        <div class="collection-card">
            <div class="product-details">
                <h3 class="product-title">Test Product</h3>
            </div>
        </div>
        """
        soup = BeautifulSoup(product_html, 'html.parser')
        product = soup.find('div', class_='collection-card').find('div', class_='product-details')
        expected_data = {'Title': 'Test Product', 'Price': None, 'Colors': None, 'Size': None, 'Gender': None}
        self.assertEqual(extract_product_data(product), expected_data)

    @patch('requests.get')
    def test_fetch_page_content_success(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.content = "<html><body>Data</body></html>".encode('utf-8')
        url = "http://example.com"
        content = fetch_page_content(url)
        self.assertEqual(content, b"<html><body>Data</body></html>")
        mock_get.assert_called_once_with(url, headers=unittest.mock.ANY)

    @patch('requests.get')
    def test_fetch_page_content_failure(self, mock_get):
        mock_get.return_value.status_code = 404
        url = "http://example.com"
        content = fetch_page_content(url)
        self.assertIsNone(content)
        mock_get.assert_called_once_with(url, headers=unittest.mock.ANY)

    @patch('utils.extract.fetch_page_content')
    @patch('utils.extract.extract_product_data')
    def test_extract_fashion_data_single_page(self, mock_fetch_page, mock_extract_product):
        mock_fetch_page.return_value = """
        <div class="collection-grid" id="collectionList" bis_skin_checked="1" flex="">
            <div class="collection-card" bis_skin_checked="1" flex="">
                <div class="product-details" bis_skin_checked="1" flex="">
                    <h3 class="product-title">Product 1</h3>
                    <div class="price-container" bis_skin_checked="1" flex="">
                        <span class="price">$10.00</span>
                    </div>
                    <p style="font-size: 14px; color: rgb(119, 119, 119);">3 Colors</p>
                    <p style="font-size: 14px; color: rgb(119, 119, 119);">Size : S</p>
                    <p style="font-size: 14px; color: rgb(119, 119, 119);">Gender : Female</p>
                </div>
            </div>
        </div>
        """.encode('utf-8')
        mock_extract_product.return_value = {'Title': 'Product 1', 'Price': '$10.00', 'Colors': '3', 'Size': 'S', 'Gender': 'Female'}
        url = "http://example.com"
        data = extract_fashion_data(url, num_pages=1)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0], {'Title': 'Product 1', 'Price': '$10.00', 'Colors': '3', 'Size': 'S', 'Gender': 'Female'})

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)