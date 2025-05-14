import unittest
import pandas as pd
import os
from unittest.mock import patch, MagicMock
from utils.load import load_data_to_csv, load_data_to_google_sheets

class TestLoad(unittest.TestCase):

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.test_df = pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})
        self.test_filename = 'test_data.csv'

    def tearDown(self):
        """Clean up after each test method."""
        if os.path.exists(self.test_filename):
            os.remove(self.test_filename)

    def test_load_data_to_csv_success(self):
        """Test successful CSV save."""
        result = load_data_to_csv(self.test_df, self.test_filename)
        self.assertTrue(result)
        self.assertTrue(os.path.exists(self.test_filename))
        loaded_df = pd.read_csv(self.test_filename)
        pd.testing.assert_frame_equal(loaded_df, self.test_df)

    def test_load_data_to_csv_error(self):
        """Test CSV save with error."""
        with patch('pandas.DataFrame.to_csv') as mock_to_csv:
            mock_to_csv.side_effect = Exception("Failed to write CSV")
            result = load_data_to_csv(self.test_df, self.test_filename)
            self.assertFalse(result)
        self.assertFalse(os.path.exists(self.test_filename))

    def test_load_data_to_csv_empty_df(self):
        """Test CSV save with empty DataFrame."""
        empty_df = pd.DataFrame()
        result = load_data_to_csv(empty_df, self.test_filename)
        self.assertTrue(result)  # Should still save empty DataFrame
        self.assertTrue(os.path.exists(self.test_filename))

    def test_load_data_to_csv_invalid_path(self):
        """Test CSV save with invalid path."""
        result = load_data_to_csv(self.test_df, '/invalid/path/test.csv')
        self.assertFalse(result)

class TestLoadGoogleSheets(unittest.TestCase):

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.test_df = pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})
        self.spreadsheet_id = 'test_spreadsheet_id'
        self.sheet_name = 'Sheet1'

    @patch('google.oauth2.service_account.Credentials.from_service_account_file')
    @patch('googleapiclient.discovery.build')
    def test_load_data_to_google_sheets_success(self, mock_build, mock_creds):
        """Test successful Google Sheets save."""
        # Setup mock objects
        mock_service = MagicMock()
        mock_sheets = MagicMock()
        mock_values = MagicMock()
        mock_clear = MagicMock()
        mock_update = MagicMock()

        # Configure mocks
        mock_build.return_value = mock_service
        mock_service.spreadsheets.return_value = mock_sheets
        mock_sheets.values.return_value = mock_values
        mock_values.clear.return_value = mock_clear
        mock_values.update.return_value = mock_update
        mock_update.execute.return_value = {'updatedCells': 10}
        mock_clear.execute.return_value = {}

        # Call function
        result = load_data_to_google_sheets(self.test_df, self.spreadsheet_id, self.sheet_name)

        # Assertions
        self.assertTrue(result)
        mock_build.assert_called_once_with('sheets', 'v4', credentials=mock_creds.return_value)
        mock_values.clear.assert_called_once()
        mock_values.update.assert_called_once()

    @patch('google.oauth2.service_account.Credentials.from_service_account_file')
    @patch('googleapiclient.discovery.build')
    def test_load_data_to_google_sheets_clear_error(self, mock_build, mock_creds):
        """Test Google Sheets save with clear error."""
        mock_service = MagicMock()
        mock_service.spreadsheets.return_value.values.return_value.clear.side_effect = Exception("Clear failed")
        mock_build.return_value = mock_service

        result = load_data_to_google_sheets(self.test_df, self.spreadsheet_id, self.sheet_name)
        self.assertFalse(result)

    @patch('google.oauth2.service_account.Credentials.from_service_account_file')
    @patch('googleapiclient.discovery.build')
    def test_load_data_to_google_sheets_update_error(self, mock_build, mock_creds):
        """Test Google Sheets save with update error."""
        mock_service = MagicMock()
        mock_service.spreadsheets.return_value.values.return_value.clear.return_value.execute.return_value = {}
        mock_service.spreadsheets.return_value.values.return_value.update.side_effect = Exception("Update failed")
        mock_build.return_value = mock_service

        result = load_data_to_google_sheets(self.test_df, self.spreadsheet_id, self.sheet_name)
        self.assertFalse(result)

    @patch('google.oauth2.service_account.Credentials.from_service_account_file')
    def test_load_data_to_google_sheets_build_error(self, mock_creds):
        """Test Google Sheets save with build error."""
        mock_creds.side_effect = Exception("Failed to load credentials")
        
        result = load_data_to_google_sheets(self.test_df, self.spreadsheet_id, self.sheet_name)
        self.assertFalse(result)

    def test_load_data_to_google_sheets_empty_df(self):
        """Test Google Sheets save with empty DataFrame."""
        empty_df = pd.DataFrame()
        result = load_data_to_google_sheets(empty_df, self.spreadsheet_id, self.sheet_name)
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)