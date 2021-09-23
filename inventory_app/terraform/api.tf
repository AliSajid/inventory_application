resource "aws_api_gateway_rest_api" "rest_api" {
  body = data.template_file.chalice_api_swagger.rendered

  name = "inventory_app"

  binary_media_types = ["application/octet-stream", "application/x-tar", "application/zip", "audio/basic", "audio/ogg", "audio/mp4", "audio/mpeg", "audio/wav", "audio/webm", "image/png", "image/jpg", "image/jpeg", "image/gif", "video/ogg", "video/mpeg", "video/webm"]

  endpoint_configuration {
    types = ["EDGE"]
  }
}

resource "aws_api_gateway_deployment" "rest_api" {
  stage_name = "api"

  stage_description = md5(data.template_file.chalice_api_swagger.rendered)

  rest_api_id = aws_api_gateway_rest_api.rest_api.id

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_api_gateway_stage" "dev" {
  deployment_id = aws_api_gateway_deployment.rest_api.id
  rest_api_id   = aws_api_gateway_rest_api.rest_api.id
  stage_name    = "dev"
}

resource "aws_api_gateway_stage" "prod" {
  deployment_id = aws_api_gateway_deployment.rest_api.id
  rest_api_id   = aws_api_gateway_rest_api.rest_api.id
  stage_name    = "prod"
}

resource "aws_api_gateway_usage_plan" "rest_api" {
  name        = "USAGE PLAN"
  description = "my description"

  api_stages {
    api_id = aws_api_gateway_rest_api.rest_api.id
    stage  = aws_api_gateway_stage.dev.stage_name
  }

  api_stages {
    api_id = aws_api_gateway_rest_api.rest_api.id
    stage  = aws_api_gateway_stage.prod.stage_name
  }

  quota_settings {
    limit  = 200
    offset = 2
    period = "WEEK"
  }

  throttle_settings {
    burst_limit = 5
    rate_limit  = 10
  }
}


resource "aws_api_gateway_api_key" "rest_api" {
  name = "inventory_app"
}

resource "aws_api_gateway_usage_plan_key" "rest_api" {
  key_id        = aws_api_gateway_api_key.rest_api.id
  key_type      = "API_KEY"
  usage_plan_id = aws_api_gateway_usage_plan.rest_api.id
}
