import json

import core
import requests
from bs4 import BeautifulSoup
from datetime import datetime


def sanitize_date(date_str, date_format="%Y/%m/%d"):
    try:
        # Attempt to parse the date
        return datetime.strptime(date_str, date_format)
    except ValueError:
        # If the date is invalid, handle the error
        print("Invalid date format")
        return None


def get_html(page_url: str):
    try:
        response = requests.get(page_url, headers=core.generate_random_browser_headers())
        match response.status_code:
            case 200:
                return BeautifulSoup(response.text, "html.parser")
            case 403:
                print(f"403 error trying to access {page_url}. Reason: {response.reason} ")
                return None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the URL: {e}")


def get_publication_page_url(page_url: str):
    soup = get_html(page_url)
    if soup is not None:
        soup.getText()
        link = soup.find("article").find("a", href=True)
        return f"https://www.legifrance.gouv.fr{link['href']}"


def get_publication_page_content(page_url: str) -> []:
    output = []
    soup = get_html(page_url)
    if soup is not None:
        links = soup.find_all(class_="jorfLink")
        for link in links:
            output.append(
                {
                    "id": link["id"],
                    "title": link.text,
                    "link": f"https://www.legifrance.gouv.fr{link["href"]}",
                }
            )
            break
        return output


def get_publication_page_content_detail(page_url: str):
    output = []

    soup = get_html(page_url)
    if soup is not None:
        try:
            main_block = soup.find(id="liste-sommaire")
            articles_block = main_block.find_all('article')
            for article_block in articles_block:
                article_number = article_block.find("p", {"class": "name-article"})
                article_content = article_block.find("div", class_="content")

                output.append({
                    int(article_number.getText().replace("Article", "").strip()): article_content.getText(),
                })
        except AttributeError as error:
            print(f"[ERROR] {error}")
    return output


if __name__ == "__main__":
    # Variables
    response = []


    # date = input("Type the date (YYYY/MM/DD): ")
    date = "2024/06/14"
    # sanitized_date = sanitize_date(date_input)
    # if sanitized_date:
    url = f"https://www.legifrance.gouv.fr/jorf/jo/{date}"
    # else:
    #    print("Invalid date.")
    publication_page_url = get_publication_page_url(url)
    if publication_page_url is not None:
        publication_page_content = get_publication_page_content(publication_page_url)
        for item in publication_page_content:
            articles = get_publication_page_content_detail(item["link"])
            # print(json.dumps(articles, indent=4))
            item['articles'] = articles
            response.append(item)

            # response.append(publication_page_content.update())
        print(json.dumps(response, indent=4))
        print("----")