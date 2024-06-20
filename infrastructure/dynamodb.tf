resource "aws_dynamodb_table" "journal_officiel" {
  name           = "journal-officiel"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "PublicationId"
  range_key      = "PublicationDate"

  attribute {
    name = "PublicationId"
    type = "S"
  }

  attribute {
    name = "PublicationDate"
    type = "S"
  }

  attribute {
    name = "PublicationUrl"
    type = "S"
  }

  attribute {
    name = "PublicationUrl"
    type = "S"
  }

  attribute {
    name = "ContentItem"
    type = "S"
  }

  attribute {
    name = "ContentLink"
    type = "S"
  }

  attribute {
    name = "ContentSummary"
    type = "S"
  }

  ttl {
    attribute_name = "TimeToExist"
    enabled        = false
  }

  tags = {
    Name        = "journal-officiel"
  }
}