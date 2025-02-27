import wikipedia as w
import requests

def get_summary_from_wiki(word):
    """
    Retrieves a summary from Wikipedia for a given word.
    Limits the summary to 5 sentences.
    """
    try:
        return w.summary(word, sentences=5, auto_suggest=False)
    except (w.DisambiguationError, w.PageError):
        return "No summary available for this term."

def mask_out_word_in_summary(word):
    """
    Retrieves the Wikipedia summary for the given word and masks out the word in the text.
    Returns a list of sentences excluding the first one.
    """
    text = get_summary_from_wiki(word)
    masked_text = text.replace(word, "***")
    return masked_text.split(".")[1:] if "." in masked_text else []

def get_first_wiki_hint(word):
    """
    Retrieves the first sentence (hint) from the masked summary.
    """
    hints = mask_out_word_in_summary(word)
    return hints[0].strip() if hints else "No hints available."

def get_second_wiki_hint(word):
    """
    Retrieves the second and third sentence (hint) from the masked summary.
    """
    hints = mask_out_word_in_summary(word)
    return hints[1].strip() if len(hints) > 1 else "No additional hints available."


def get_third_wiki_hint(word):
    """
    Retrieves the second and third sentence (hint) from the masked summary.
    """
    hints = mask_out_word_in_summary(word)
    return hints[2].strip() if len(hints) > 2 else ""

def get_img_url_from_wiki(word):
    """
    Retrieves an image URL from Wikipedia for a given word.
    If an image is blocked or unavailable, it silently skips and tries another.
    Now supports SVG images (for flags).
    If all images fail, returns a fallback image.
    """
    headers = {"User-Agent": "Mozilla/5.0"}  # Simple default User-Agent

    try:
        w_page = w.page(word, auto_suggest=False)
        w_page_images = w_page.images

        # Collect only PNG, JPG, and SVG images
        valid_images = [img for img in w_page_images if img.lower().endswith((".png", ".jpg", ".svg"))]

        # 🔁 Keep trying images until one works
        for img_url in valid_images:
            if check_image_accessible(img_url, headers):
                return img_url  # ✅ Found a working image!

        # 🔹 If no valid images, try related Wikipedia pages
        related_titles = w.search(word, results=5)
        for title in related_titles:
            try:
                related_page = w.page(title, auto_suggest=False)
                related_images = [img for img in related_page.images if img.lower().endswith((".png", ".jpg", ".svg"))]

                for img_url in related_images:
                    if check_image_accessible(img_url, headers):
                        return img_url  # ✅ Found a working image!
            except (w.DisambiguationError, w.PageError):
                continue  # Skip problematic pages

    except (w.DisambiguationError, w.PageError):
        pass  # Skip if page is missing or ambiguous

    return "https://upload.wikimedia.org/wikipedia/commons/6/65/No-Image-Placeholder.svg"  # Fallback image


def check_image_accessible(img_url, headers):
    """
    Checks if an image URL is accessible.
    Returns True if the image is valid, False otherwise.
    """
    try:
        response = requests.get(img_url, headers=headers, timeout=5)
        return response.status_code == 200
    except requests.RequestException:
        return False  # ❌ Silently skip blocked images without printing anything
