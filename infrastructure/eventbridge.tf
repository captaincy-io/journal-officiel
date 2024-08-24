resource "aws_scheduler_schedule" "scrapper" {
  name       = "schedule-journal-officiel-scrapper"
  description = "Schedule used to trigger Lambda to scrap data of Journal Officiel."

  flexible_time_window {
    mode = "OFF"
  }

  schedule_expression = "cron(0 14 * * ? *)"

  target {
    arn      = data.aws_lambda_function.scrapper.arn
    role_arn = aws_iam_role.schedule_lambda_scrapper.arn
  }
}

data "aws_iam_policy_document" "schedule_assume_role" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["scheduler.amazonaws.com"]
    }
  }
}

data "aws_iam_policy_document" "invoke_lambda" {
  statement {
    actions = ["lambda:InvokeFunction"]
    effect = "Allow"
    resources = [
      "arn:aws:lambda:${data.aws_region.current.id}:${data.aws_caller_identity.current.account_id}:function:journal-officiel-scrapper"
    ]
  }
}

resource "aws_iam_role" "schedule_lambda_scrapper" {
  name               = "schedule-lambda-journal-officiel-scrapper"
  path               = "/system/"
  assume_role_policy = data.aws_iam_policy_document.schedule_assume_role.json
}

resource "aws_iam_policy" "allow_invoke_lambda_scrapper" {
  name        = "policy-invoke-lambda-journal-officiel-scrapper"
  path        = "/"
  description = "Policy allowing EventBridge Schedule to invoke Lambda 'journal-officiel-scrapper'."
  policy = data.aws_iam_policy_document.invoke_lambda.json
}

resource "aws_iam_role_policy_attachment" "scheduler_lambda" {
  role       = aws_iam_role.schedule_lambda_scrapper.name
  policy_arn = aws_iam_policy.allow_invoke_lambda_scrapper.arn
}