resource "aws_glue_catalog_database" "journal_officiel" {
  name = "journal-officiel-database"

  tags = merge({
    Name = "journal-officiel-database"
  }, local.tags)
}

resource "aws_glue_catalog_table" "journal_officiel" {
  name          = "journal-officiel-table"
  database_name = "journal-officiel-database"

  parameters = {
    "classification" = "json"
  }

  storage_descriptor {
    additional_locations      = []
    bucket_columns            = []
    compressed                = false
    input_format              = "json"
    number_of_buckets         = 0
    output_format             = "json"
    parameters                = {}
    stored_as_sub_directories = false

    ser_de_info {
      name       = null
      parameters = {}
    }

    columns {
      comment = "Unique ID of the decret. Eg: JORFTEXT000049757275"
      name    = "id"
      type    = "string"
    }

    columns {
      comment = "Decret title. Eg: 'Décret n° 2024-565 du 20 ju......'"
      name    = "title"
      type    = "string"
    }

    columns {
      comment = "Link of the decret. Eg: https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000049757275"
      name    = "link"
      type    = "string"
    }

    columns {
      comment = "Content of the decret."
      name    = "content"
      type    = "string"
    }
  }

  partition_keys {
    comment = "Unique ID of the decret. Eg: JORFTEXT000049757275"
    name    = "id"
    type    = "string"
  }

  depends_on = [aws_glue_catalog_database.journal_officiel]
}

resource "aws_glue_data_quality_ruleset" "journal_officiel_rule_content" {
  name    = "journal-officiel-rule-content"
  description = "This rule checks tether text in column named 'content' is filled."
  ruleset = "Rules = [ColumnValues \"content\" != NULL]"

  target_table {
    database_name = aws_glue_catalog_database.journal_officiel.name
    table_name    = aws_glue_catalog_table.journal_officiel.name
  }

  tags = merge({
    Name = "journal-officiel-rule-content"
  }, local.tags)
}