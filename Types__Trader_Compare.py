import json
import xml.etree.ElementTree as ET
import os
import shutil

ignore_list = """
object1
object2
object3
"""
ignore_list = [item.lower().strip() for item in ignore_list.split("\n") if item.strip()]

# Point towards your TraderPlusPriceConfig.json
json_file_path = r"Path-to-your-TraderPlusPriceConfig"
# Point towards your types.xml
xml_path = r"Path-to-your-Types"

backup_folder = os.path.join(os.path.expanduser("~"), "Downloads\\Export\\Backup")
os.makedirs(backup_folder, exist_ok=True)
json_backup_path = os.path.join(backup_folder, "TraderPlusPriceConfig.json")
xml_backup_path = os.path.join(backup_folder, "types.xml")
shutil.copyfile(json_file_path, json_backup_path)
shutil.copyfile(xml_path, xml_backup_path)

json_temp_path = os.path.join(backup_folder, "TraderPlusPriceConfig_temp.json")
xml_temp_path = os.path.join(backup_folder, "types_temp.xml")

with open(json_file_path, "r") as json_file:
    json_content = json_file.read().lower()
with open(json_temp_path, "w") as json_temp_file:
    json_temp_file.write(json_content)

tree = ET.parse(xml_path)
root = tree.getroot()
xml_content = ET.tostring(root, encoding="utf-8").decode("utf-8").lower()
with open(xml_temp_path, "w") as xml_temp_file:
    xml_temp_file.write(xml_content)

with open(json_temp_path, "r") as json_file:
    trader_data = json.load(json_file)

tree = ET.parse(xml_temp_path)
root = tree.getroot()


json_items = set()
for category in trader_data["tradercategories"]:
    for product in category["products"]:
        item_name = product.split(",")[0]
        if item_name not in ignore_list:
            json_items.add(item_name)

xml_items = set()
for item_type in root.findall("type"):
    item_name = item_type.attrib["name"]
    if item_name in ignore_list:
        continue
    nominal = item_type.find("nominal")
    if nominal is not None and int(nominal.text) >= 1:
        xml_items.add(item_name)

missing_in_xml = set()
for item in json_items:
    if item in ignore_list:
        continue
    xml_item = root.find(f"./type[@name='{item}']")
    if xml_item is None:
        missing_in_xml.add(item)

missing_in_json = xml_items - json_items

missing_in_xml_content = (
    "----------------------------------------------------------------------------\nClasses missing in types.xml but are found in TraderPlusPriceConfig.json\n----------------------------------------------------------------------------\n\n"
    + "\n".join(missing_in_xml)
    if missing_in_xml
    else "No items missing in types.xml."
)

missing_in_json_content = (
    "----------------------------------------------------------------------------\nClasses missing in TraderPlusPriceConfig.json but are found in types.xml AND which has a nominal value => 1 \n----------------------------------------------------------------------------\n\n"
    + "\n".join(missing_in_json)
    if missing_in_json
    else "No items missing in TraderPlusPriceConfig.json."
)

# Save logs
log_folder = os.path.join(
    os.path.expanduser("~"), "Downloads\\Export\\Missing"
)  # Saves to your downloads folder.
os.makedirs(log_folder, exist_ok=True)

log_xml_path = os.path.join(log_folder, "missing_in_types.txt")
log_json_path = os.path.join(log_folder, "missing_in_trader.txt")

with open(log_xml_path, "w") as log_xml_file:
    log_xml_file.write(missing_in_xml_content)

with open(log_json_path, "w") as log_json_file:
    log_json_file.write(missing_in_json_content)

print(f"Missing items log (XML) has been saved to: {log_xml_path}")
print(f"Missing items log (JSON) has been saved to: {log_json_path}")

os.remove(json_temp_path)
os.remove(xml_temp_path)
