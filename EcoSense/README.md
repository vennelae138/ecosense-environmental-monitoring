# EcoSense — Environmental Monitoring System

Software-first IoT dashboard prototype using Flask, SQLite, HTML, CSS, JavaScript and Chart.js.

**Important:** Readings are simulated demo data. No physical sensor is connected. AQI values are illustrative and are not official measurements.

## Run on Windows
1. Install Python 3.10+ from https://www.python.org/downloads/ and enable **Add Python to PATH**.
2. Extract this ZIP file.
3. Open the extracted `EcoSense` folder in File Explorer.
4. Click the address bar, type `cmd`, and press Enter.
5. Run these commands one at a time:

   ```bat
   py -m venv .venv
   .venv\Scripts\activate
   py -m pip install -r requirements.txt
   py app.py
   ```

6. Open http://127.0.0.1:5000 in your browser.
7. Keep the terminal open while using the site. Press Ctrl+C to stop it.

If `py` is not recognized, use `python` instead.

## Features
- Responsive dashboard and selectable demo locations
- Simulated temperature, humidity and illustrative AQI
- Automatic refresh every 15 seconds
- SQLite history and charts
- Demo alerts and CSV export
- `/health` endpoint

## Public deployment
Push these files to a GitHub repository, then create a Python web service on a hosting provider such as Render.
- Build command: `pip install -r requirements.txt`
- Start command: `gunicorn app:app`

For persistent history, configure a persistent disk and set `ECOSENSE_DB` to a file path on that disk. Some free hosting services may sleep after inactivity or reset local files.

## Future hardware integration
The current `/api/reading` route generates demo values. For real hardware, implement an authenticated sensor-ingestion endpoint, validate incoming values, and clearly identify readings by source. Do not expose an unauthenticated public sensor-write endpoint.
