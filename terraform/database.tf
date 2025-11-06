resource "google_sql_database_instance" "default" {
  name             = "book_shelves"
  database_version = "POSTGRES_16"
  region           = var.region

  settings {
    tier = "db-f1-micro"
  }
}

resource "google_sql_user" "users" {
  name     = "dbuser"
  instance = google_sql_database_instance.default.name
  password = random_password.db_password.result
}

resource "google_sql_database" "database" {
  name     = "book_shelves"
  instance = google_sql_database_instance.default.name
}

resource "google_secret_manager_secret" "db_password" {
  secret_id = "db-password"
  replication {
    #automatic = true
  }
}

resource "random_password" "db_password" {
  length  = 20
  special = false  # Set to true if you want symbols
}

resource "google_secret_manager_secret_version" "db_password_version" {
  secret      = google_secret_manager_secret.db_password.id
  secret_data = random_password.db_password.result
}
