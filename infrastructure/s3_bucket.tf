resource "aws_s3_bucket" "journal_officiel_datalake" {
  bucket = "journal-officiel-datalake"

  tags = merge({
    Name = "journal-officiel-datalake"
  }, local.tags)
}

resource "aws_s3_bucket_policy" "journal_officiel_datalake" {
  bucket = aws_s3_bucket.journal_officiel_datalake.id
  policy = file("policies/s3_journal_officiel_datalake.json")
}