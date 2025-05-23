﻿# ETLPIPELINE

# ETL Pipeline with Google Sheets

## Overview
This project implements an ETL (Extract, Transform, Load) pipeline using Google Sheets API. The pipeline extracts data from source, performs necessary transformations, and loads the processed data into a destination.

## Prerequisites
- Python 3.x
- Google Cloud Platform Account
- Google Sheets API enabled
- Required Python packages (install via pip):
  ```bash
  pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib pandas
  ```

## Setup
1. Create a Google Cloud Project
2. Enable Google Sheets API
3. Create credentials (Service Account Key)
4. Download the credentials and save as `google-sheets-api.json`
5. Share your Google Sheet with the service account email

## Project Structure


## Configuration
Create a `google-sheets-api.json` file with your Google Sheets API credentials. This file should be kept private and is included in `.gitignore`.

## Usage
Run the main script:
```bash
python src/main.py
```

## Security Notes
- Never commit API credentials to the repository
- Keep your `google-sheets-api.json` file secure
- Use environment variables for sensitive information

## Contributing
1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License
[MIT License](LICENSE)
