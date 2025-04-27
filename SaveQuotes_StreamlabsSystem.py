# -*- coding: utf-8 -*-
import clr
clr.AddReference("IronPython.Modules")
import os
import sys
import json
import codecs
import re
import csv
import logging
from datetime import datetime

logging.basicConfig(filename=os.path.join(os.path.dirname(__file__), "debug.log"), level=logging.DEBUG)

# import requests
sys.path.append(os.path.join(os.path.dirname(__file__), "lib")) #point at lib folder for classes / references

#---------------------------
#   [Required] Script Information
#---------------------------
ScriptName = "Save Quotes"
Website = "https://twitch.tv/1eft0ver"
Description = "Saves quotes to a CSV file"
Creator = "1eft0ver"
Version = "1.0.1"

#---------------------------
#   Define Global Variables
#---------------------------
settingsFile = os.path.join(os.path.dirname(__file__), "Settings", "save_quotes_settings.json")
defaultCsvPath = os.path.join(os.path.dirname(__file__), "quotes.csv")
settings = {}

# Add settings handling similar to SyrslyRegBot
class SaveQuotesSettings:
    def __init__(self, settings_file=None):
        try:
            with codecs.open(settings_file, encoding="utf-8-sig", mode="r") as f:
                self.__dict__ = json.load(f, encoding="utf-8")
        except:
            Parent.Log(ScriptName, "Failed to open settings file {}".format(str(e)))
            self.CsvPath = defaultCsvPath
            self.CommandName = "!名言"
            self.CustomMessage = "「{quote}」 by 知名實況主 1eft0ver on {date}"

    def Reload(self, json_data):
        self.__dict__ = json.loads(json_data, encoding="utf-8")

    def Save(self, settings_file):
        try:
            with codecs.open(settings_file, encoding="utf-8-sig", mode="w+") as f:
                json.dump(self.__dict__, f, encoding="utf-8")
        except Exception as e:
            Parent.Log(ScriptName, "Failed to save settings: {}".format(str(e)))

# Update global variables
settings = SaveQuotesSettings(settingsFile)

#---------------------------
#   [Required] Initialize Data (Only called on load)
#---------------------------
def ensure_absolute_path(path):
    if not os.path.isabs(path):
        return os.path.abspath(path)
    return path

# Update Init to ensure CSV file includes headers and uses utf-8-sig encoding
def Init():
    logging.debug("Init function called.")
    global settings
    settings = SaveQuotesSettings(settingsFile)
    settings.CsvPath = ensure_absolute_path(settings.CsvPath)
    settings.CommandName = settings.CommandName if hasattr(settings, 'CommandName') else "!名言"
    settings.CustomMessage = settings.CustomMessage if hasattr(settings, 'CustomMessage') else "「{quote}」 by 1eft0ver"
    settings.Save(settingsFile)
    updateUi()

    # Ensure the CSV file exists
    csv_path = settings.CsvPath
    if not os.path.exists(csv_path):
        logging.debug("CSV file not found at {}. Creating file with headers.".format(csv_path))
        with codecs.open(csv_path, mode="w", encoding="utf-8-sig") as csvfile:
            writer = csv.writer(csvfile, lineterminator="\n")
            writer.writerow(["Timestamp", "Username", "Quote"])
    else:
        logging.debug("CSV file already exists at {}.".format(csv_path))

def sanitize_csv_file(file_path):
    """Remove BOM from the CSV file if present."""
    with codecs.open(file_path, 'r', encoding='utf-8-sig') as f:
        lines = f.readlines()

    with codecs.open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(lines)

# Call this function during initialization to sanitize the CSV file
sanitize_csv_file(settings.CsvPath)

#---------------------------
#   [Required] Execute Data / Process messages
#---------------------------
# Ensure all data is sanitized before writing to the CSV file
def sanitize_data(data):
    return data.replace("\n", " ").replace("\r", " ")

# Update Execute to write data to CSV file
def Execute(data):
    if not data.IsChatMessage():
        return

    message = data.Message.strip()
    username = data.User

    command_name = settings.CommandName if hasattr(settings, 'CommandName') else "!名言"

    if message.lower().startswith(command_name.lower()):
        quote = sanitize_data(message[len(command_name):].strip())
        if quote:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            current_date = datetime.now().strftime("%Y/%m/%d") # Format date as YYYY/MM/DD
            csv_path = settings.CsvPath
            with codecs.open(csv_path, mode="a", encoding="utf-8-sig") as csvfile:
                writer = csv.writer(csvfile, lineterminator="\n")
                writer.writerow([timestamp, sanitize_data(username), quote])

            custom_message = settings.CustomMessage.format(quote=quote, date=current_date)
            Parent.SendStreamMessage(custom_message)

#---------------------------
#   [Required] Tick method (Gets called during every iteration even when there is no incoming data)
#---------------------------
def Tick():
    return

#---------------------------
#   [Optional] Save Settings (Called when settings are updated)
#---------------------------
# Ensure SaveSettings updates both UI_Config.json and save_quotes_settings.json

def SaveSettings():
    global settings
    uiConfigPath = os.path.join(os.path.dirname(__file__), "UI_Config.json")
    try:
        with codecs.open(uiConfigPath, encoding="utf-8-sig", mode="r") as f:
            uiConfig = json.load(f)
        # Update settings from UI_Config.json
        settings.CsvPath = uiConfig["CsvPath"].get("value", defaultCsvPath)
        settings.CommandName = uiConfig["CommandName"].get("value", settings.CommandName)
        settings.CustomMessage = uiConfig["CustomMessage"].get("value", settings.CustomMessage)
    except Exception as e:
        Parent.Log(ScriptName, "Failed to read UI_Config.json: {}".format(str(e)))

    # Save updated settings to save_quotes_settings.json
    settings.Save(settingsFile)

    try:
        # Update UI_Config.json with the latest settings values
        uiConfig["CsvPath"]["value"] = settings.CsvPath
        uiConfig["CommandName"]["value"] = settings.CommandName
        uiConfig["CustomMessage"]["value"] = settings.CustomMessage
        with codecs.open(uiConfigPath, encoding="utf-8-sig", mode="w+") as f:
            json.dump(uiConfig, f, indent=4)
    except Exception as e:
        Parent.Log(ScriptName, "Failed to update UI_Config.json: {}".format(str(e)))

#---------------------------
#   [Optional] Reload Settings (Called when settings are updated)
#---------------------------
# Add logging to ReloadSettings to confirm it is called

def ReloadSettings(jsonData):
    global settings
    logging.debug("Reload Settings called.")  # Log when ReloadSettings is called
    settings.Reload(jsonData)  # Reload settings from the provided JSON data
    settings.Save(settingsFile)  # Save the updated settings to the settings file
    updateUi()  # Update the UI to reflect the new settings
    logging.debug("Settings reloaded and saved.")

# Add updateUi function

def updateUi():
    uiConfigPath = os.path.join(os.path.dirname(__file__), "UI_Config.json")
    try:
        with codecs.open(uiConfigPath, encoding="utf-8-sig", mode="r") as f:
            uiConfig = json.load(f)
        uiConfig["CsvPath"]["value"] = ensure_absolute_path(settings.CsvPath)
        uiConfig["CommandName"]["value"] = settings.CommandName
        uiConfig["CustomMessage"]["value"] = settings.CustomMessage
        with codecs.open(uiConfigPath, encoding="utf-8-sig", mode="w+") as f:
            json.dump(uiConfig, f, indent=4)
    except Exception as e:
        Parent.Log(ScriptName, "Failed to update UI: {}".format(str(e)))