import json
import boto3
import botocore
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key
import core
import requests
from bs4 import BeautifulSoup
from datetime import datetime


# Sanitize the date
def sanitize_date(date_str, date_format="%Y/%m/%d"):
    try:
        # Attempt to parse the date
        return datetime.strptime(date_str, date_format)
    except ValueError:
        # If the date is invalid, handle the error
        print("Invalid date format")
        return None


# Get the html content of an url
def get_html(page_url: str):
    try:
        response = requests.get(
            page_url, headers=core.generate_random_browser_headers()
        )
        match response.status_code:
            case 200:
                return BeautifulSoup(response.text, "html.parser")
            case 403:
                print(
                    f"403 error trying to access {page_url}. Reason: {response.reason} "
                )
                return None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the URL: {e}")


# Get the url of the publication page
def get_publication_page_url(page_url: str):
    soup = get_html(page_url)
    if soup is not None:
        soup.getText()
        link = soup.find("article").find("a", href=True)
        return f"https://www.legifrance.gouv.fr{link['href']}"


# Get the content of the publication page
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
            # break
        return output


# Get each article of the publication page
def get_publication_page_content_detail(page_url: str):
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
            # print(f"[ERROR] {error}")
            try:
                main_block = soup.find(id="liste-sommaire")
                articles_block = main_block.find_all("article")
                for article_block in articles_block:
                    article_content = article_block.find("div", class_="content")

                    output.append(
                        {
                           article_content.getText(),
                        }
                    )
            except AttributeError as error:
                print(f"[ERROR] {error}")
        return output
    return output

#     with table.batch_write_item() as batch:
#         for item in items:
#             batch.put_item(Item=item)


# Create a dynamodb table
def create_table(dynamodb):
    table = dynamodb.create_table(
        TableName="journal-officiel",
        KeySchema=[
            {"AttributeName": "PublicationDate", "KeyType": "HASH"},  # Partition key
            {"AttributeName": "PublicationId", "KeyType": "RANGE"},  # Sort key
        ],
        AttributeDefinitions=[
            {"AttributeName": "PublicationDate", "AttributeType": "S"},
            {"AttributeName": "PublicationId", "AttributeType": "S"},
        ],
        ProvisionedThroughput={"ReadCapacityUnits": 10, "WriteCapacityUnits": 10},
    )
    return table

def create_dynamodb_table_if_not_exists(table_name):
    # Initialize a session using Amazon DynamoDB
    dynamodb_client = boto3.client(
        "dynamodb",
        endpoint_url="http://localhost:8000",
        region_name="localhost",
        aws_access_key_id="dummy",
        aws_secret_access_key="dummy",
    )
    try:
        # Check if the table exists
        response = dynamodb_client.describe_table(TableName=table_name)
        print(f"Table {table_name} already exists.")
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceNotFoundException':
            # If the table does not exist, create it
            print(f"Table {table_name} does not exist. Creating the table.")
            dynamodb_resource = boto3.resource(
                "dynamodb",
                endpoint_url="http://localhost:8000",
                region_name="localhost",
                aws_access_key_id="dummy",
                aws_secret_access_key="dummy",
            )
            table = create_table(dynamodb_resource)
            print("Table status:", table.table_status)
            table_name = "journal-officiel"
            table.meta.client.get_waiter("table_exists").wait(TableName=table_name)
            print(f"Table {table_name} created with success.")


def check_sort_key_exists(partition_key_value, sort_key_value):
    response = table.query(
        KeyConditionExpression=Key('PublicationDate').eq(partition_key_value) & Key('PublicationId').eq(
            sort_key_value)
    )

    # If the count of items is greater than 0, the sort key exists
    if response['Count'] > 0:
        return True
    else:
        return False



if __name__ == "__main__":
    response = []
    date = input("Type the date (YYYY/MM/DD): ")
    sanitized_date = sanitize_date(date)
    if sanitized_date:
        url = f"https://www.legifrance.gouv.fr/jorf/jo/{date}"
    else:
        print("Invalid date.")
        exit(0)
    create_dynamodb_table_if_not_exists('journal-officiel')

    dynamodb = boto3.resource(
        "dynamodb",
        endpoint_url="http://localhost:8000",
        region_name="localhost",
        aws_access_key_id="dummy",
        aws_secret_access_key="dummy",
    )
    number_of_files = 0
    publication_page_url = get_publication_page_url(url)
    # Create a Bedrock Runtime client in the AWS Region of your choice.
    bedrock_client = boto3.client("bedrock-runtime", region_name="eu-west-3")
    # Set the model ID, e.g., Titan Text Premier.
    model_id = "amazon.titan-text-express-v1"
    if publication_page_url is not None:
        publication_page_content = get_publication_page_content(publication_page_url)
        for item in publication_page_content:
            articles = get_publication_page_content_detail(item["link"])
            item["articles"] = articles
            response.append(item)
            table = dynamodb.Table('journal-officiel')

            # Define the prompt for the model.
            prompt = f"Résume le texte sans liste: {str(articles)}"
            # Format the request payload using the model's native structure.
            native_request = {
                "inputText": prompt,
                "textGenerationConfig": {
                    "maxTokenCount": 512,
                    "temperature": 0,
                },
            }
            # Convert the native request to JSON.
            request = json.dumps(native_request)
            try:
                # Invoke the model with the request.
                ia_response = bedrock_client.invoke_model(modelId=model_id, body=request)
            except (ClientError, Exception) as e:
                print(f"ERROR: Can't invoke '{model_id}'. Reason: {e}")
                exit(1)
            # Decode the response body.
            model_response = json.loads(ia_response["body"].read())
            # Extract and print the response text.
            Content_Summary = model_response["results"][0]["outputText"]
            print(Content_Summary)

            # Check if sort key is already in the table
            if check_sort_key_exists(date, item["id"]) is True:
                print(f"The '{item["id"]}' article is already in the table, file not added.")
            else:
                table.put_item(
                    Item={
                        "PublicationDate": date,
                        "PublicationId": item["id"],
                        "PublicationUrl": item["link"],
                        "ContentItems": str(articles),
                        "ContentSummary": Content_Summary,
                    }
                )
            number_of_files += 1
            # response.append(publication_page_content.update())
        # print(json.dumps(response, indent=4))
        print("----")
        if number_of_files == 0:
            print("All files were already in the table, no file added.")
        else:
            print(f"{number_of_files} file(s) added with success.")







