import requests
import sys
import os
from dataclasses import dataclass
from bs4 import BeautifulSoup


@dataclass
class TableRowData:
    url: str
    page_name: str


def download_html(url):
    try:
        response = requests.get(url)
        response.raise_for_status()

        html_content = response.text
        return html_content
    except requests.exceptions.RequestException as e:
        print(f"Error downloading content: {e}")
    except Exception as e:
        print(f"Error processing content: {e}")


def extract_table_row_data(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    table_rows = soup.find_all("tr")

    data_list = []
    for row in table_rows:
        span = row.find("span", class_="titleline")
        if span:
            url = span.a["href"]
            page_name = span.a.text
            data_list.append(TableRowData(url, page_name))

    return data_list


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python download_html.py <url>")
        sys.exit(1)

    url = sys.argv[1]

    html_content = download_html(url)
    data_list = extract_table_row_data(html_content)

    file_mode = "a" if os.path.exists("favorites.md") else "w"
    with open("favorites.md", file_mode, encoding="utf-8") as f:
        for data in data_list:
            f.write(f"* [{data.page_name}]({data.url})\n")
