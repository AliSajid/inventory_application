data "aws_caller_identity" "chalice" {}

data "aws_partition" "chalice" {}

data "aws_region" "chalice" {}

data "null_data_source" "chalice" {

  inputs = {
    app   = "inventory_app"
    stage = "dev"
  }
}

data "template_file" "chalice_api_swagger" {
  template = "{\"swagger\": \"2.0\", \"info\": {\"version\": \"1.0\", \"title\": \"inventory_app\"}, \"schemes\": [\"https\"], \"paths\": {\"/item\": {\"post\": {\"consumes\": [\"application/json\"], \"produces\": [\"application/json\"], \"responses\": {\"200\": {\"description\": \"200 response\", \"schema\": {\"$ref\": \"#/definitions/Empty\"}}}, \"x-amazon-apigateway-integration\": {\"responses\": {\"default\": {\"statusCode\": \"200\"}}, \"uri\": \"${aws_lambda_function.api_handler.invoke_arn}\", \"passthroughBehavior\": \"when_no_match\", \"httpMethod\": \"POST\", \"contentHandling\": \"CONVERT_TO_TEXT\", \"type\": \"aws_proxy\"}}, \"get\": {\"consumes\": [\"application/json\"], \"produces\": [\"application/json\"], \"responses\": {\"200\": {\"description\": \"200 response\", \"schema\": {\"$ref\": \"#/definitions/Empty\"}}}, \"x-amazon-apigateway-integration\": {\"responses\": {\"default\": {\"statusCode\": \"200\"}}, \"uri\": \"${aws_lambda_function.api_handler.invoke_arn}\", \"passthroughBehavior\": \"when_no_match\", \"httpMethod\": \"POST\", \"contentHandling\": \"CONVERT_TO_TEXT\", \"type\": \"aws_proxy\"}}}, \"/inventory\": {\"get\": {\"consumes\": [\"application/json\"], \"produces\": [\"application/json\"], \"responses\": {\"200\": {\"description\": \"200 response\", \"schema\": {\"$ref\": \"#/definitions/Empty\"}}}, \"x-amazon-apigateway-integration\": {\"responses\": {\"default\": {\"statusCode\": \"200\"}}, \"uri\": \"${aws_lambda_function.api_handler.invoke_arn}\", \"passthroughBehavior\": \"when_no_match\", \"httpMethod\": \"POST\", \"contentHandling\": \"CONVERT_TO_TEXT\", \"type\": \"aws_proxy\"}}}}, \"definitions\": {\"Empty\": {\"type\": \"object\", \"title\": \"Empty Schema\"}}, \"x-amazon-apigateway-binary-media-types\": [\"application/octet-stream\", \"application/x-tar\", \"application/zip\", \"audio/basic\", \"audio/ogg\", \"audio/mp4\", \"audio/mpeg\", \"audio/wav\", \"audio/webm\", \"image/png\", \"image/jpg\", \"image/jpeg\", \"image/gif\", \"video/ogg\", \"video/mpeg\", \"video/webm\"]}"

}


