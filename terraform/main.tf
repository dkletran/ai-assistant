resource "google_service_account" "service_account" {
  account_id   = "ai-assistant-sa"
  display_name = "AI Assistant Service Account"
}

resource "google_project_iam_binding" "sa_binding" {
  project = local.project
  for_each = toset([
    "roles/secretmanager.secretAccessor",
    "roles/aiplatform.user"
  ])
  role    = each.key
  members = ["serviceAccount:${google_service_account.service_account.email}"]
}


resource "google_cloud_run_v2_service" "default" {
  project  = local.project
  name     = "ai-assistant"
  location = local.region
  template {
    scaling {
      max_instance_count = 5
    }
    containers {
      image = var.image_name
      ports {
        container_port = 8501
      }
      env {
        name = "OPENAI_API_KEY"
        value_source {
          secret_key_ref {
            secret  = local.openai_api_key_secret
            version = "latest"
          }
        }
      }
    }
    service_account = google_service_account.service_account.account_id

  }
  traffic {
    percent = 100
    type    = "TRAFFIC_TARGET_ALLOCATION_TYPE_LATEST"
  }
  depends_on = [google_project_iam_binding.sa_binding]
}

resource "google_cloud_run_domain_mapping" "default" {
  count    = var.domain_name == "" ? 0 : 1
  name     = var.domain_name
  location = google_cloud_run_v2_service.default.location
  metadata {
    namespace = local.project
  }
  spec {
    route_name = google_cloud_run_v2_service.default.name
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
  location    = google_cloud_run_v2_service.default.location
  project     = google_cloud_run_v2_service.default.project
  service     = google_cloud_run_v2_service.default.name
  policy_data = data.google_iam_policy.noauth.policy_data
}
