import wikipedia as w
import requests
import os
from ascii_magic import AsciiArt

def get_img_url_from_wiki(word):
    """
    Retrieves an image URL from Wikipedia for a given word.
    Returns None if no suitable image is found.
    """
    try:
        w_page = w.page(word, auto_suggest=False)
        w_page_images = w_page.images

        # Filter for PNG and JPG images
        filtered_images = [img for img in w_page_images if img.lower().endswith((".png", ".jpg"))]

        return filtered_images[-1] if filtered_images else None  # Return last image in list if available
    except (w.DisambiguationError, w.PageError):
        return None  # If no valid page or ambiguous term, return None

def display_pic_in_terminal(img_path):
    """
    Converts an image to ASCII art and displays it in the terminal.
    """
    try:
        art = AsciiArt.from_image(img_path)
        print(art.to_ascii(columns=60))
    except Exception as e:
        print(f"Error displaying ASCII image: {e}")

def download_image(img_url, filename):
    """
    Downloads an image from a URL and saves it locally.
    Silently skips errors if the image is blocked.
    """
    headers = {"User-Agent": "Mozilla/5.0"}  # Simple default User-Agent

    try:
        response = requests.get(img_url, headers=headers, timeout=5)
        response.raise_for_status()  # ✅ Raise an exception if the request fails

        with open(filename, "wb") as f:
            f.write(response.content)

        return filename
    except requests.RequestException:
        return None  # ❌ Silently skip this image

def show_pic_from_url(img_url):
    """
    Downloads an image from the URL and displays it as ASCII art.
    If the image fails to download, it tries a fallback.
    """
    if not img_url:
        return  # ❌ If no image URL, do nothing

    filename = "temp_img.jpg" if img_url.lower().endswith(".jpg") else "temp_img.png"
    img_path = download_image(img_url, filename)

    if img_path:
        display_pic_in_terminal(img_path)
        os.remove(img_path)  # ✅ Delete temporary file

def show_pic(word):
    """
    Retrieves an image from Wikipedia for a given word and displays it in ASCII format.
    """
    img_url = get_img_url_from_wiki(word)
    show_pic_from_url(img_url)
# show_pic("Ninetales")
# show_pic("Apple")