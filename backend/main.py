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


def get_html(url: str):
    try:
        response = requests.get(url)
        #response.raise_for_status()  # Raise an exception for HTTP errors
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the URL: {e}")
    response = requests.get(url)
    print(response)
    match response.status_code:
        case 200:
            return BeautifulSoup(response.text, "html.parser")
        case 403:
            print(f"403 error trying to access {url}. Reason: {response.reason} ")
            return None






def get_publication_page_url(url: str):
    soup = get_html(url)
    if soup is not None:
        soup.getText()
        link = soup.find("article").find("a", href=True)
        print(f"https://www.legifrance.gouv.fr{link['href']}")
        return f"https://www.legifrance.gouv.fr{link['href']}"




def get_publication_page_content(url: str) -> []:
    output = []
    soup = get_html(url)
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
        return output


def get_publication_page_content_detail(url: str):
    soup = get_html(url)
    if soup is not None:
        content_article: str = ""
        name_article: str = ""
        try:
            liste_sommaire = soup.find(id="liste-sommaire")
            li_elements = liste_sommaire.find_all("li")
            for li in li_elements:
                article = li.find("article")
                if article:
                    p = article.find("p")
                    if p:
                        article_name = p.getText()
                        print(f"{article_name} : ")
                    div = article.find("div", class_="content")
                    if div:
                        article_content = div.getText()
                        print(article_content)
                        print("")
        except AttributeError as error:
            print(f"[ERROR] {error}")
    return ""


if __name__ == "__main__":
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
            url = item["link"]
            articles = get_publication_page_content_detail(url)
            print(articles)
