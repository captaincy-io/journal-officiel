import boto3
import botocore

dynamodb_client = boto3.client(
    'dynamodb',
    endpoint_url='http://localhost:8000',
    region_name='eu-west-3',
    aws_access_key_id="5weug8",
    aws_secret_access_key="uksvb3"
)

table_name = "journal-officiel"
# table_name = 'MyTable'
# attribute_definitions = [
#     {
#         'AttributeName': 'PrimaryKey',
#         'AttributeType': 'S'  # 'S' for string, 'N' for number, 'B' for binary
#     },
#     {
#         'AttributeName': 'SortKey',
#         'AttributeType': 'N'  # 'N' for number
#     }
# ]
# key_schema = [
#     {
#         'AttributeName': 'PrimaryKey',
#         'KeyType': 'HASH'  # Partition key
#     },
#     {
#         'AttributeName': 'SortKey',
#         'KeyType': 'RANGE'  # Sort key
#     }
# ]
# provisioned_throughput = {
#     'ReadCapacityUnits': 5,
#     'WriteCapacityUnits': 5
# }
#
# # Create the table
#
# table = dynamodb_client.create_table(
#     TableName=table_name,
#     AttributeDefinitions=attribute_definitions,
#     KeySchema=key_schema,
#     ProvisionedThroughput=provisioned_throughput
# )
# print(f"Table {table_name} is being created.")
#
#
#
# test = dynamodb_client.list_tables()
new_items = dynamodb_client.put_item(
    TableName=table_name,
    Item={
        "PublicationDate": {"S": "24/04/2023"},
        "PublicationId": {"S": "NLA&ALN"},
        "PublicationUrl": {"S": "test"},
        "ContentItem": {"S": "Test"},
        "ContentLink": {"S": "test"},
        "ContentSummary": {"S": "test"}
    },
)
print(new_items)
