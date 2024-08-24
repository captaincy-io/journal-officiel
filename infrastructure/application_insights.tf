resource "aws_applicationinsights_application" "journal_officiel" {
  resource_group_name = aws_resourcegroups_group.journal_officiel.name
}