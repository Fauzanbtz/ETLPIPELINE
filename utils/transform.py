import datetime
import pandas as pd

def transform_data(data):
    """Melakukan transformasi data pada data produk yang telah di-scrape."""
    transformed_data = []
    for item in data:
        try:
            # Konversi Price ke Rupiah
            price_str = item.get('Price')
            if price_str:
                price_str = price_str.replace('$', '').strip()
                try:
                    price = float(price_str)
                    item['Price'] = price * 16000
                except ValueError:
                    item['Price'] = None
            else:
                item['Price'] = None

            # Konversi Rating ke float
            rating_str = item.get('Rating')
            if rating_str and "Invalid" not in rating_str:
                try:
                    item['Rating'] = float(rating_str.split('/')[0].strip())
                except ValueError:
                    item['Rating'] = None
            else:
                item['Rating'] = None

            # Bersihkan data Colors, Size, dan Gender
            item['Colors'] = item.get('Colors', '').replace("Colors", "").strip()
            item['Size'] = item.get('Size', '').replace("Size :", "").strip()
            item['Gender'] = item.get('Gender', '').replace("Gender :", "").strip()

            # Tambahkan timestamp
            item['timestamp'] = datetime.datetime.now().isoformat()
            transformed_data.append(item)
        except AttributeError as e:
            print(f"Error transforming item: {e} - {item}")
        except KeyError as e:
            print(f"Missing key in item: {e} - {item}")
    return pd.DataFrame(transformed_data)