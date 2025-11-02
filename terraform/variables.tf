variable "project_id" {
  description = "The GCP project ID to deploy resources into"
  type        = string
}

variable "region" {
  description = "The region for GCP resources"
  type        = string
  default     = "europe-west3" # Frankfurt
}