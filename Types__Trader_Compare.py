"""
This Python script serves the purpose of comparing the contents of two files: TraderPlusPriceConfig.json and Types.xml.
It generates two separate logs that highlight discrepancies between the two files. These logs are saved in the \downloads directory.

1. missing_in_types_log.txt: This log documents items that are absent in Types.xml but are present in TraderPlusPriceConfig.json.
2. missing_in_trader_log.txt: This log records items that are absent in TraderPlusPriceConfig.json but exist in Types.xml.

The purpose of this script is to facilitate the identification of inconsistencies between the two mentioned files.

Please adjust the file paths and other configurations as needed before running the script.
"""
__author__ = "naps"
__copyright__ = "Copyright (C) 2023 Nick Shepherd"
__license__ = "General Public License v3.0"
__version__ = "1.0"

import json
import xml.etree.ElementTree as ET
import os

# Point towards your TraderPlusPriceConfig.json
with open(
        r'Path-to-your-TraderPlusPriceConfig',
        'r') as json_file:
    trader_data = json.load(json_file)

# Point towards your types.xml
xml_path = r'Path-to-your-Types'
tree = ET.parse(xml_path)
root = tree.getroot()

json_items = set()
for category in trader_data['TraderCategories']:
    for product in category['Products']:
        item_name = product.split(',')[0].lower()
        json_items.add(item_name)

xml_items = set()
for item_type in root.findall('type'):
    item_name = item_type.attrib['name'].lower()
    nominal = item_type.find('nominal')
    if nominal is not None and int(nominal.text) >= 1:
        xml_items.add(item_name)

missing_in_xml = set()
for item in json_items:
    xml_item = root.find(f"./type[@name='{item}']")
    if xml_item is None:
        missing_in_xml.add(item)

missing_in_json = xml_items - json_items

missing_in_xml_content = "----------------------------------------------------------------------------\nClasses missing in types.xml but are found in TraderPlusPriceConfig.json\n----------------------------------------------------------------------------\n\n" + "\n".join(
    missing_in_xml) if missing_in_xml else "No items missing in types.xml."

missing_in_json_content = "----------------------------------------------------------------------------\nClasses missing in TraderPlusPriceConfig.json but are found in types.xml AND which has a nominal value => 1 \n----------------------------------------------------------------------------\n\n" + "\n".join(
    missing_in_json) if missing_in_json else "No items missing in TraderPlusPriceConfig.json."

log_folder = os.path.join(os.path.expanduser('~'), 'Downloads\\Export\\Missing')  # Saves to your downloads folder.
os.makedirs(log_folder, exist_ok=True)

log_xml_path = os.path.join(log_folder, 'missing_in_types.txt')
log_json_path = os.path.join(log_folder, 'missing_in_trader.txt')

with open(log_xml_path, 'w') as log_xml_file:
    log_xml_file.write(missing_in_xml_content)

with open(log_json_path, 'w') as log_json_file:
    log_json_file.write(missing_in_json_content)

print(f"Missing items log (XML) has been saved to: {log_xml_path}")
print(f"Missing items log (JSON) has been saved to: {log_json_path}")
