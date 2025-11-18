# book_shelves

## ToDo

* [x] add renovate bot
* [ ] only run terraform after changes detected by plan
* [ ] reduce rights of terraform key
* [x] add Alembic with Invite Codes + Local Postgres
* [x] Change Cloud SQL + Cloud Run to use private IP
* [x] add user management via Google Auth
    * [x] add invite codes in DB
    * [x] add login process for registered users
    * [x] add add registration process for invited members
* [x] add basic book list
    * store data in Clodu SQL
    * [x] search books by isbn
    * [x] delete books
    * [x] list books
    * [x] search books by title
* [x] block users which are not registered
* [x] Integrate Google Book API
* [ ] move to gunicorn setup
* [ ] change logs to json format
* [ ] integrate cloud profiler 

## GCP Project Setup

The GitHub secret `GOOGLE_CREDENTIALS` must be set in order for the terraform worflow to work.
