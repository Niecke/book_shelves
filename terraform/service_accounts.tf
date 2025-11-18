# Create a new service account for Cloud Run
resource "google_service_account" "cloud_run_sa" {
  account_id   = "cloud-run-app"
  display_name = "Cloud Run Service Account for Flask App"
}

resource "google_secret_manager_secret_iam_member" "cloud_run_access" {
  secret_id = google_secret_manager_secret.db_password.id
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:${google_service_account.cloud_run_sa.email}"
}

# These secrets are managed outside of this terraform code, but we need to grant access to them
resource "google_secret_manager_secret_iam_member" "google_client_id" {
  secret_id = "projects/1018120441073/secrets/GOOGLE_CLIENT_ID"
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:${google_service_account.cloud_run_sa.email}"
}

resource "google_secret_manager_secret_iam_member" "google_client_secret" {
  secret_id = "projects/1018120441073/secrets/GOOGLE_CLIENT_SECRET"
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:${google_service_account.cloud_run_sa.email}"
}

resource "google_project_iam_member" "cloud_run_sql_access" {
  project = var.project_id
  role    = "roles/cloudsql.client"
  member  = "serviceAccount:${google_service_account.cloud_run_sa.email}"
}

# this is needed for the deploy_app.yml
output "cloud_run_service_account_email" {
  value = google_service_account.cloud_run_sa.email
}
