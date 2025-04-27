# Save Quotes Streamlabs Chatbot Script

## Overview
The **Save Quotes** script is a Streamlabs Chatbot extension that allows users to save memorable quotes from chat into a CSV file. The script also provides customizable messages to display after saving a quote.

## Features
- Save quotes to a CSV file with timestamps and usernames.
- Customize the command name used to trigger the quote-saving functionality.
- Customize the message displayed after saving a quote.

## Files
- **SaveQuotes_StreamlabsSystem.py**: The main script that handles the logic for saving quotes and managing settings.
- **UI_Config.json**: Configuration file for the Streamlabs Chatbot UI, allowing customization of settings like the CSV path, command name, and custom message.
- **Settings/save_quotes_settings.json**: Stores the user's settings, including the CSV path, command name, and custom message.
- **Settings/save_quotes_settings.js**: JavaScript file for additional settings management.

## Installation
1. Download the repository as a `.zip` file.
2. Open Streamlabs Chatbot and navigate to the **Scripts** tab.
3. Click on the **Import** button and select the downloaded `.zip` file.
4. The script will be automatically imported and ready to use.

## Configuration
1. Open the Streamlabs Chatbot UI.
2. Navigate to the **Scripts** tab and select the **Save Quotes** script.
3. Configure the following settings:
   - **Path to CSV File**: Specify the file path where quotes will be saved.
   - **Command Name**: Set the command name to trigger the quote-saving functionality (e.g., `!quote`).
   - **Custom Message**: Define the message to display after saving a quote. Use placeholders like `{quote}` and `{date}` for dynamic content.

## Usage
1. In the chat, use the configured command (e.g., `!quote`) followed by the quote text to save a quote.
   - Example: `!quote This is a memorable moment!`
2. The script will save the quote to the specified CSV file and display the custom message in the chat.

## CSV File Format
The CSV file will contain the following columns:
- **Timestamp**: The date and time when the quote was saved.
- **Username**: The username of the person who triggered the command.
- **Quote**: The text of the saved quote.

## Customization
### Custom Message
The custom message supports the following placeholders:
- `{quote}`: The text of the saved quote.
- `{date}`: The current date in `YYYY/MM/DD` format.

### Example Custom Message
```
"{quote}" by {username} on {date}
```

## Troubleshooting
- Ensure the CSV file path is valid and writable.
- Check the Streamlabs Chatbot logs for any errors related to the script.