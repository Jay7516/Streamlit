from markdown import markdown
from bs4 import BeautifulSoup

def markdown_to_text(md):
    # Convert markdown to HTML
    html = markdown(md)
    # Strip HTML tags
    soup = BeautifulSoup(html, "html.parser")
    return soup.get_text()