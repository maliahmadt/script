import pandas as pd
import requests
import os
import re

excel_file_path = 'test.xlsx'
output_directory = 'output'

os.makedirs(output_directory, exist_ok=True)

df = pd.read_excel(excel_file_path)


image_links = df['Pictures']

def extract_file_id(drive_link):
    match = re.search(r'/file/d/([a-zA-Z0-9_-]+)', drive_link)
    if match:
        return match.group(1)
    return None

def download_image_from_drive(drive_link, output_folder):
    file_id = extract_file_id(drive_link)
    if file_id:
        download_url = f"https://drive.google.com/uc?export=download&id={file_id}"
        try:
            response = requests.get(download_url, stream=True)
            if response.status_code == 200:
                image_name = f"{file_id}.jpg"
                with open(os.path.join(output_folder, image_name), 'wb') as file:
                    for chunk in response.iter_content(1024):
                        file.write(chunk)
                print(f"Image {image_name} downloaded successfully.")
            else:
                print(f"Failed to download image from {drive_link}")
        except Exception as e:
            print(f"Error downloading {drive_link}: {e}")
    else:
        print(f"Invalid Google Drive link: {drive_link}")

for link in image_links:
    download_image_from_drive(link, output_directory)

print("All images downloaded.")
