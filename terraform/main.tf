resource "google_service_account" "service_account" {
  account_id   = "ai-assistant-sa"
  display_name = "AI Assistant Service Account"
}

resource "google_project_iam_binding" "sa_binding" {
  project = "ai-assistant-399819"
  role    = "roles/aiplatform.user"
  members = ["serviceAccount:${google_service_account.service_account.email}"]
}

resource "google_cloud_run_service" "default" {
  project  = "ai-assistant-399819"
  name     = "ai-assistant"
  location = "europe-west9"

  template {
    spec {
      containers {
        image = "europe-west9-docker.pkg.dev/ai-assistant-399819/docker-repo/ai-assistant:${var.image_tag}"
        ports {
          container_port = 8501
        }
      }
      service_account_name = google_service_account.service_account.account_id
    }
  }

  traffic {
    percent         = 100
    latest_revision = true
  }

}

data "google_iam_policy" "noauth" {
  binding {
    role = "roles/run.invoker"
    members = [
      "allUsers",
    ]
  }
}

resource "google_cloud_run_service_iam_policy" "noauth" {
  location    = google_cloud_run_service.default.location
  project     = google_cloud_run_service.default.project
  service     = google_cloud_run_service.default.name
  policy_data = data.google_iam_policy.noauth.policy_data
}
