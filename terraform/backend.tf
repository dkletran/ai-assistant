terraform {
  backend "gcs" {
    bucket = "ai-assistant-399819"
    prefix = "tfstates"
  }
}
