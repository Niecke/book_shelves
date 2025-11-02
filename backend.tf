terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 4.40"
    }
  }
  backend "gcs" {
    bucket = "book-shelves-terraform-state" # must already exist
    prefix = "terraform/state"
  }
}