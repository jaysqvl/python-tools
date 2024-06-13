import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin

def download_images_from_page(url, folder_name='downloaded_images'):
    # Send a GET request to the URL
    response = requests.get(url)
    response.raise_for_status()  # Check for request errors

    # Create a folder to save images
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all image tags
    img_tags = soup.find_all('img')

    # Download each image
    for img in img_tags:
        img_url = img.get('src')
        if img_url:
            # Convert relative URL to absolute URL
            img_url = urljoin(url, img_url)

            try:
                img_response = requests.get(img_url)
                img_response.raise_for_status()

                # Get the image file name
                img_name = os.path.join(folder_name, os.path.basename(img_url))

                # Save the image
                with open(img_name, 'wb') as f:
                    f.write(img_response.content)

                print(f'Downloaded {img_name}')
            except requests.exceptions.RequestException as e:
                print(f'Could not download {img_url}. Error: {e}')

if __name__ == '__main__':
    # Example usage
    url = 'https://www.example.com/'
    download_images_from_page(url)
