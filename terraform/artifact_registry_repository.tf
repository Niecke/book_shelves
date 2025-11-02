resource "google_artifact_registry_repository" "docker_repo" {
  project        = var.project_id
  location       = var.region                  # e.g., "europe-west3" for Frankfurt
  repository_id  = "book-shelves-docker-repo"  # Choose a name for your repo
  format         = "DOCKER"
}