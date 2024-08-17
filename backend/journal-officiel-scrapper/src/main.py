import boto3
import json
import core
import logging
import requests
import os
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


def get_html(page_url: str):
    """
    Fetches and parses the HTML content of a web page.

    The function sends a GET request to the specified URL using random browser headers to mimic a real browser.
    If the request is successful (status code 200), it returns a BeautifulSoup object containing the parsed HTML.
    If the request is forbidden (status code 403), it prints an error message and returns None.
    Any other request exceptions are caught and printed.

    Args:
        page_url (str): The URL of the web page to fetch and parse.

    Returns:
        BeautifulSoup or None: A BeautifulSoup object if the request is successful, or None if there is an error.
    """
    try:
        response = requests.get(
            page_url, headers=core.generate_random_browser_headers()
        )
        match response.status_code:
            case 200:
                return BeautifulSoup(response.text, "html.parser")
            case 403:
                logger.error(
                    f"403 error trying to access {page_url}. Reason: {response.reason} "
                )
                return None
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching the URL: {e}")


def get_publication_page_url(page_url: str):
    """
    Fetches the publication page URL from a given page URL.

    The function uses the `get_html` function to fetch and parse the HTML content of the specified page URL.
    If the HTML content is successfully fetched and parsed, it extracts the first link within an article element
    and constructs the full URL to the publication page.

    Args:
        page_url (str): The URL of the page to fetch and parse.

    Returns:
        str or None: The full URL to the publication page if found, or None if the HTML content could not be fetched
        or the link could not be found.
    """
    soup = get_html(page_url)
    if soup is not None:
        soup.getText()
        link = soup.find("article").find("a", href=True)
        return f"https://www.legifrance.gouv.fr{link['href']}"


def get_publication_page_content(page_url: str) -> []:
    """
    Fetches the publication page content from a given page URL.

    The function uses the `get_html` function to fetch and parse the HTML content of the specified page URL.
    If the HTML content is successfully fetched and parsed, it extracts all links with the class "jorfLink" and
    compiles a list of dictionaries containing the id, title, and full URL of each link.

    Args:
        page_url (str): The URL of the page to fetch and parse.

    Returns:
        list: A list of dictionaries containing the id, title, and link of each publication, or an empty list if no links are found.
    """

    output = []
    soup = get_html(page_url)
    if soup is not None:
        links = soup.find_all(class_="jorfLink")
        for link in links:
            link_id = link["id"]
            link_href = link["href"]
            output.append(
                {
                    "id": link_id,
                    "title": link.text,
                    "link": f"https://www.legifrance.gouv.fr{link_href}",
                }
            )
            break
        return output


def get_publication_page_content_detail(page_url: str):
    """
    Fetches detailed content from a publication page.

    The function uses the `get_html` function to fetch and parse the HTML content of the specified page URL.
    If the HTML content is successfully fetched and parsed, it extracts details from the main content block
    identified by the id "liste-sommaire". It gathers article numbers and their respective content,
    and compiles a list of dictionaries with article numbers as keys and content as values.

    Args:
        page_url (str): The URL of the page to fetch and parse.

    Returns:
        list: A list of dictionaries with article numbers as keys and their content as values, or an empty list if no articles are found.
    """
    output = []

    soup = get_html(page_url)
    if soup is not None:
        try:
            main_block = soup.find(id="liste-sommaire")
            articles_block = main_block.find_all("article")
            for article_block in articles_block:
                article_number = article_block.find("p", {"class": "name-article"})
                article_content = article_block.find("div", class_="content")

                output.append(
                    {
                        int(
                            article_number.getText().replace("Article", "").strip()
                        ): article_content.getText(),
                    }
                )
        except AttributeError as error:
            logger.error(f"[ERROR] {error}")
    return output


def handler(event, context):
    """
    Handles the event by fetching and processing publication page content from a specified URL.

    The function constructs a URL based on a given date, retrieves the publication page URL,
    then fetches and processes the publication page content and its details. It compiles a response
    containing the publication content and its associated articles.

    Args:
        event: The event data (not used in the function).
        context: The context data (not used in the function).

    Returns:
        None: This function does not return anything but prints the response.
    """
    logging.basicConfig(level=logging.INFO)

    s3_client = boto3.client("s3")

    response = []
    date = "2024/06/14"
    url = f"https://www.legifrance.gouv.fr/jorf/jo/{date}"
    publication_page_url = get_publication_page_url(url)
    if publication_page_url is not None:
        publication_page_content = get_publication_page_content(publication_page_url)
        for item in publication_page_content:
            articles = get_publication_page_content_detail(item["link"])
            item["articles"] = articles
            response.append(item)

        # Save the response to a JSON file
        filename = f"publication_content_{date.replace('/', '-')}.json"
        with open(filename, "w", encoding="utf-8") as json_file:
            json.dump(response, json_file, ensure_ascii=False, indent=4)

        # Upload the JSON file to S3
        bucket_name = os.environ["datalake_s3_bucket_name"]
        s3_key = f"publications/{filename}"
        try:
            s3_client.upload_file(
                filename, bucket_name, s3_key, ExtraArgs={"StorageClass": "ONEZONE_IA"}
            )
            logger.info(f"File uploaded to S3: s3://{bucket_name}/{s3_key}")
        except Exception as e:
            logger.error(f"Error uploading file to S3: {e}")
