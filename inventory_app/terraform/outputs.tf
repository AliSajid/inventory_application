output "EndpointURL" {
  value = aws_api_gateway_deployment.rest_api.invoke_url
}

output "RestAPIId" {
  value = aws_api_gateway_rest_api.rest_api.id
}

output "APIKey" {
  value     = aws_api_gateway_api_key.rest_api.value
  sensitive = true
}
