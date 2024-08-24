resource "aws_resourcegroups_group" "journal_officiel" {
  name = "journal-officiel-resources"

  resource_query {
    query = jsonencode({
      ResourceTypeFilters = [
        "AWS::AllSupported"
      ]

      TagFilters = [
        {
          Key = "Application"
          Values = [
            "journal-officiel"
          ]
        }
      ]
    })
  }

  tags = local.tags
}