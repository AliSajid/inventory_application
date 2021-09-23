resource "aws_lambda_function" "update_inventory" {
  function_name = "inventory_app-dev-update_inventory"

  runtime = "python3.9"

  handler = "app.update_inventory"

  memory_size = 128

  tags = {
    "aws-chalice" = "version=1.24.2:stage=dev:app=inventory_app"
  }

  timeout = 60

  source_code_hash = filebase64sha256("${path.module}/deployment.zip")

  filename = "${path.module}/deployment.zip"

  role = aws_iam_role.default-role.arn
}

resource "aws_lambda_function" "api_handler" {
  function_name = "inventory_app-dev"

  runtime = "python3.9"

  handler = "app.app"

  memory_size = 128

  tags = {
    "aws-chalice" = "version=1.24.2:stage=dev:app=inventory_app"
  }

  timeout = 60

  source_code_hash = filebase64sha256("${path.module}/deployment.zip")

  filename = "${path.module}/deployment.zip"

  environment {

    variables = {
      "INVENTORY_BUCKET_NAME" = aws_s3_bucket.inventory_bucket.id
    }
  }

  role = aws_iam_role.default-role.arn
}
