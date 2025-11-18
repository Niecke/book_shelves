# book_shelves

## ToDo

* [ ] add renovate bot
* [ ] only run terraform after changes detected by plan
* [ ] reduce rights of terraform key
* [x] add Alembic with Invite Codes + Local Postgres
* [ ] Change Cloud SQL + Cloud Run to use private IP
* [x] add user management via Google Auth
    * [x] add invite codes in DB
    * [x] add login process for registered users
    * [x] add add registration process for invited members
* [ ] add basic book list
    * store data in Cloud Spanner
    * [ ] add book
    * [ ] edit book
    * [ ] delete book
    * [ ] list books
* [x] block users which are not registered
* [ ] Integrate Google Book API

## GCP Project Setup

The GitHub secret `GOOGLE_CREDENTIALS` must be set in order for the terraform worflow to work.
