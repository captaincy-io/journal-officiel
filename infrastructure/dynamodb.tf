resource "aws_dynamodb_table" "journal_officiel" {
  name         = "journal-officiel"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "PublicationId"
  range_key    = "PublicationDate"

  attribute {
    name = "PublicationId"
    type = "S"
  }

  attribute {
    name = "PublicationDate"
    type = "S"
  }

  tags = merge({
    Name           = "journal-officiel"
  }, local.tags)
}