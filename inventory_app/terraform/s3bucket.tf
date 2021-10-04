resource "aws_s3_bucket" "inventory_bucket" {
  bucket_prefix = "inventory-app-"
  force_destroy = true
}

resource "aws_s3_bucket_notification" "inventory-banseljaj-com_notify" {
  bucket = aws_s3_bucket.inventory_bucket.id

  lambda_function {
    events = ["s3:ObjectCreated:*"]

    lambda_function_arn = aws_lambda_function.update_inventory.arn

    filter_suffix = ".json"
  }

  depends_on = [aws_lambda_permission.update_inventory-s3event]
}
