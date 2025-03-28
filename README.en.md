# Beykent Exam Result Notifier

[![English](https://img.shields.io/badge/English-EN-blue)](README.en.md)
[![Türkçe](https://img.shields.io/badge/Türkçe-TR-red)](README.md)

This Python script automatically checks exam results for Beykent University students and sends notifications via ntfy.sh when results are published.

## Features

- Automatic exam result checking
- Real-time notifications via ntfy.sh
- Customizable check interval
- Secure credential management
- 100% local operation - your data stays on your device

## Installation

1. Create and activate Python virtual environment:

```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux/MacOS
python3 -m venv venv
source venv/bin/activate
```

2. Install required packages:

```bash
pip install -r requirements.txt
```

3. Configure environment variables:

```bash
# Windows
copy .env.example .env

# Linux/MacOS
cp .env.example .env
```

4. Edit the `.env` file and enter the following information:
   - `USERNAME`: Your student number
   - `PASSWORD`: Your student portal password
   - `HEADLESS`: Browser visibility (default: false)
   - `NTFY_TOPIC`: ntfy.sh notification topic

> **Note**: Remember to edit the file after renaming `.env.example` to `.env`.

## Usage

> **Recommendation**: It is recommended to use a remote server (VPS/VDS) for automatic running.

### Automatic Running on Windows

1. Open Task Scheduler
2. Click "Create Basic Task"
3. Enter task name and description
4. Select "Daily" as trigger
5. Set start time
6. Select "Start a program" as action
7. Enter the following command in the program/script field:
   ```
   C:\Path\To\Your\venv\Scripts\python.exe C:\Path\To\Your\main.py
   ```
8. Click "Finish"

### Automatic Running on Linux

1. Edit crontab:
   ```bash
   crontab -e
   ```

2. Add the following line (runs every hour):
   ```
   0 * * * * cd /path/to/your/project && source /path/to/your/project/venv/bin/activate && python main.py
   ```

> **Note**: Remember to replace `/path/to/your/project` with your project's full path.

## Manual Running

Remember to activate the virtual environment before running the script:

```bash
# Windows
.\venv\Scripts\activate

# Linux/MacOS
source venv/bin/activate

# Run the script
python main.py
```

> **Note**: The virtual environment must be active before running the script. If it's not active, use the appropriate command above to activate it.

## Requirements

- Python 3.8 or higher
- Internet connection
- ntfy.sh notification topic (no account required)

## Security and Privacy

- All operations are performed 100% locally
- Your credentials are stored only on your device in the `.env` file
- No data is sent to servers or shared with third parties
- Code is open source, you can verify its security
- ntfy.sh notifications are encrypted and sent only to your specified topic

## Troubleshooting

- If the script doesn't run, make sure the virtual environment is active
- Check your internet connection
- Verify the information in the `.env` file
- Check the log files in the logs folder

## Credits

- The captcha solving module is adapted from [AmireNoori/MathCaptchaSolver](https://github.com/AmireNoori/MathCaptchaSolver). While the original code supported basic arithmetic operations and sign detection, the following improvements have been made:
  - Added logging system integration for debugging
  - Added error handling and validation
  - Implemented dynamic data folder management
  - Added support for saving processed images in a dedicated folder
  - Removed hardcoded file paths
  - Optimized image cropping positions and dimensions
  - Added better number cleaning and validation

## License

This project is licensed under the MIT License. 