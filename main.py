# main.py
from utils.extract import extract_fashion_data
from utils.transform import transform_data
from utils.load import load_data_to_csv, load_data_to_google_sheets

def main():
    """Fungsi utama untuk menjalankan ETL pipeline."""
    url = 'https://fashion-studio.dicoding.dev/'
    print("Memulai proses ETL...")

    # Extract
    print("Tahap Extract: Mengambil data dari website...")
    fashion_data = extract_fashion_data(url)
    if not fashion_data:
        print("Ekstraksi data gagal. Menghentikan proses.")
        return

    # Transform
    print("Tahap Transform: Membersihkan dan mengubah data...")
    transformed_df = transform_data(fashion_data)
    if transformed_df.empty:
        print("Transformasi data gagal. Menghentikan proses.")
        return

    # Load
    print("Tahap Load: Menyimpan data ke CSV...")
    csv_success = load_data_to_csv(transformed_df)
    if not csv_success:
        print("Penyimpanan data ke CSV gagal.")

    
    print("Tahap Load: Menyimpan data ke Google Sheets...")
    spreadsheet_id = '1QLWBNdKIhIiA9vlThFBm3fJpgEXl_1o5fLMZWcEpPVk'
    sheets_success = load_data_to_google_sheets(transformed_df, spreadsheet_id)
    if not sheets_success:
        print("Penyimpanan data ke Google Sheets gagal.")

    print("Proses ETL selesai.")


if __name__ == "__main__":
    main()