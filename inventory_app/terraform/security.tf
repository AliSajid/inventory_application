resource "aws_iam_role" "default-role" {
  name = "inventory_app-dev"

  assume_role_policy = "{\"Version\": \"2012-10-17\", \"Statement\": [{\"Sid\": \"\", \"Effect\": \"Allow\", \"Principal\": {\"Service\": \"lambda.amazonaws.com\"}, \"Action\": \"sts:AssumeRole\"}]}"
}

resource "aws_iam_role_policy" "default-role" {
  name = "default-rolePolicy"

  policy = "{\"Version\": \"2012-10-17\", \"Statement\": [{\"Effect\": \"Allow\", \"Action\": [\"logs:CreateLogGroup\", \"logs:CreateLogStream\", \"logs:PutLogEvents\"], \"Resource\": \"arn:*:logs:*:*:*\"}]}"

  role = aws_iam_role.default-role.id
}


resource "aws_iam_role_policy" "s3-crud" {
  name = "s3crud-rolePolicy"

  policy = templatefile("${path.module}/s3_iam_policy.tpl", { bucket_arn = aws_s3_bucket.inventory_bucket.arn })

  role = aws_iam_role.default-role.id

  depends_on = [aws_s3_bucket.inventory_bucket]
}

resource "aws_lambda_permission" "update_inventory-s3event" {
  statement_id = "update_inventory-s3event"

  action = "lambda:InvokeFunction"

  function_name = aws_lambda_function.update_inventory.arn

  principal = "s3.amazonaws.com"

  source_account = data.aws_caller_identity.chalice.account_id

  source_arn = aws_s3_bucket.inventory_bucket.arn
}

resource "aws_lambda_permission" "rest_api_invoke" {
  function_name = aws_lambda_function.api_handler.arn

  action = "lambda:InvokeFunction"

  principal = "apigateway.amazonaws.com"

  source_arn = "${aws_api_gateway_rest_api.rest_api.execution_arn}/*"
}
