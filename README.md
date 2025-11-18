# book_shelves

## ToDo

* [ ] add renovate bot
* [ ] only run terraform after changes detected by plan
* [ ] reduce rights of terraform key
* [ ] add Alembic with Invite Codes + Local Postgres
* [ ] Change Cloud SQL + Cloud Run to use private IP
* [ ] add user management via Google Auth
    * [ ] add invite codes in DB
    * [ ] add login process for registered users
    * [ ] add add registration process for invited members
* [ ] add basic book list
    * store data in Cloud Spanner
    * [ ] add book
    * [ ] edit book
    * [ ] delete book
    * [ ] list books
* [ ] Integrate Google Book API

## GCP Project Setup

The GitHub secret `GOOGLE_CREDENTIALS` must be set in order for the terraform worflow to work.
