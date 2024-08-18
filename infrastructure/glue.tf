resource "aws_glue_catalog_database" "journal_officiel" {
  name = "journal-officiel-database"
}

resource "aws_glue_catalog_table" "journal_officiel" {
  name          = "journal-officiel-table"
  database_name = "journal-officiel-database"

  depends_on = [aws_glue_catalog_database.journal_officiel]
}
