data "google_secret_manager_secret_version" "openai_api_key" {
  secret = "openai-key"
}