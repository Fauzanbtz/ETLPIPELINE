import unittest
import pandas as pd
import numpy as np
from utils.transform import transform_data

class TestTransform(unittest.TestCase):

    def test_transform_price(self):
        data = [{'Price': '$10.00'}]
        transformed_df = transform_data(data)
        self.assertEqual(transformed_df['Price'][0], 160000.0)

    def test_transform_invalid_price(self):
        data = [{'Price': 'Invalid'}]
        transformed_df = transform_data(data)
        self.assertTrue(pd.isna(transformed_df['Price'][0]))

    def test_transform_rating(self):
        data = [{'Rating': '4.8 / 5'}]
        transformed_df = transform_data(data)
        self.assertEqual(transformed_df['Rating'][0], 4.8)

    def test_transform_invalid_rating(self):
        data = [{'Rating': 'Invalid Rating / 5'}]
        transformed_df = transform_data(data)
        self.assertTrue(pd.isna(transformed_df['Rating'][0]))

    def test_transform_colors(self):
        data = [{'Colors': '3 Colors'}]
        transformed_df = transform_data(data)
        self.assertEqual(transformed_df['Colors'][0], '3')

    def test_transform_size(self):
        data = [{'Size': 'Size : M'}]
        transformed_df = transform_data(data)
        self.assertEqual(transformed_df['Size'][0], 'M')

    def test_transform_gender(self):
        data = [{'Gender': 'Gender : Female'}]
        transformed_df = transform_data(data)
        self.assertEqual(transformed_df['Gender'][0], 'Female')

    def test_transform_timestamp_exists(self):
        data = [{}]
        transformed_df = transform_data(data)
        self.assertIn('timestamp', transformed_df.columns)

    def test_transform_multiple_records(self):
        data = [
            {'Price': '$10.00', 'Rating': '4.0 / 5', 'Colors': '2 Colors', 'Size': 'Size : S', 'Gender': 'Gender : Male'},
            {'Price': '$25.50', 'Rating': 'Invalid Rating / 5', 'Colors': '4 Colors', 'Size': 'Size : L', 'Gender': 'Gender : Female'}
        ]
        transformed_df = transform_data(data)
        self.assertEqual(len(transformed_df), 2)
        self.assertEqual(transformed_df['Price'][0], 160000.0)
        self.assertTrue(pd.isna(transformed_df['Rating'][1]))
        self.assertEqual(transformed_df['Colors'][1], '4')
        self.assertEqual(transformed_df['Size'][0], 'S')
        self.assertEqual(transformed_df['Gender'][1], 'Female')

    def test_transform_empty_data(self):
        data = []
        transformed_df = transform_data(data)
        self.assertTrue(transformed_df.empty)

    def test_transform_all_invalid_data(self):
        data = [{
            'Price': 'Invalid',
            'Rating': 'Invalid',
            'Colors': '',
            'Size': '',
            'Gender': ''
        }]
        transformed_df = transform_data(data)
        self.assertTrue(pd.isna(transformed_df['Price'][0]))
        self.assertTrue(pd.isna(transformed_df['Rating'][0]))
        self.assertEqual(transformed_df['Colors'][0], '')
        self.assertEqual(transformed_df['Size'][0], '')
        self.assertEqual(transformed_df['Gender'][0], '')

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
