import pandas as pd
import numpy as np

def load_data_to_csv(df, filename='products.csv'):
    """Menyimpan DataFrame ke dalam file CSV."""
    try:
        df.to_csv(filename, index=False)
        print(f"Data successfully loaded to {filename}")
        return True
    except Exception as e:
        print(f"Error loading data to CSV: {e}")
        return False


def load_data_to_google_sheets(df, spreadsheet_id, sheet_name='Sheet1'):
    """Melakukan loading data ke Google Sheets."""

    from google.oauth2.service_account import Credentials
    from googleapiclient.discovery import build

    # Path ke berkas google-sheets-api.json 
    creds_file = 'google-sheets-api.json'  # Using relative path

    # Scope yang dibutuhkan untuk mengakses Google Sheets
    scope = ['https://www.googleapis.com/auth/spreadsheets']

    creds = Credentials.from_service_account_file(creds_file, scopes=scope)
    service = build('sheets', 'v4', credentials=creds)

    try:
        # Bersihkan sheet sebelum menulis
        clear_body = {}
        service.spreadsheets().values().clear(spreadsheetId=spreadsheet_id, range=sheet_name, body=clear_body).execute()

        # Replace NaN with empty string and convert DataFrame to list
        df_clean = df.replace({np.nan: '', float('nan'): ''})
        
        # Konversi DataFrame ke list of lists
        values = [df_clean.columns.tolist()] + df_clean.values.tolist()
        
        # Convert all values to strings to avoid JSON issues
        values = [[str(cell) if cell != '' else '' for cell in row] for row in values]
        
        body = {'values': values}
        result = service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id, range=sheet_name,
            valueInputOption='USER_ENTERED', body=body).execute()
        print(f"{result.get('updatedCells')} cells updated in Google Sheet '{sheet_name}'")
        return True
    except Exception as e:
        print(f"Error loading data to Google Sheets: {e}")
        return False