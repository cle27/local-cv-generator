from project.utils.path_utils import save_content

from bs4 import BeautifulSoup
import requests

def read_url(url, isSaved, output_file):
    # Load the HTML content
    response = requests.get(url)
    html_content = response.text

    # Parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')

    # Extract text from the HTML
    text_content = soup.get_text(separator='\n', strip=True)

    # Print the extracted text
    print(text_content)
    if isSaved :
        save_content(text_content, output_file)
    
if __name__ == "__main__":
    read_url("http://www.example.com/", 1)

