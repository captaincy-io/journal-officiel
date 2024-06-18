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


def get_publication_page_url(url: str):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the URL: {e}")
        return []
    soup = BeautifulSoup(response.text, "html.parser")
    link = soup.find("article").find("a", href=True)
    return f"https://www.legifrance.gouv.fr{link['href']}"


def get_publication_page_content(url: str) -> []:
    output = []
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the URL: {e}")
        return []
    soup = BeautifulSoup(response.text, "html.parser")
    links = soup.find_all(class_="jorfLink")
    for link in links:
        output.append(
            {
                "id": link["id"],
                "title": link.text,
                "link": f"https://www.legifrance.gouv.fr{link["href"]}",
            }
        )
    return output


def get_publication_page_content_detail(url: str):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the URL: {e}")
        return []
    soup = BeautifulSoup(response.text, "html.parser")
    name_article = (
        soup.find(id="liste-sommaire").find("li").find("article").find("p").getText()
    )
    content_article = (
        soup.find(id="liste-sommaire")
        .find("li")
        .find("article")
        .find("div", class_="content")
        .getText()
    )
    print(name_article)
    print(content_article)


if __name__ == "__main__":
    # date = input("Type the date (YYYY/MM/DD): ")
    date = "2024/06/16"
    # sanitized_date = sanitize_date(date_input)
    # if sanitized_date:
    url = f"https://www.legifrance.gouv.fr/jorf/jo/{date}"
    # else:
    #    print("Invalid date.")
    publication_page_url = get_publication_page_url(url)
    publication_page_content = get_publication_page_content(publication_page_url)
    for item in publication_page_content:
        url = item["link"]
        articles = get_publication_page_content_detail(url)
        print(articles)
