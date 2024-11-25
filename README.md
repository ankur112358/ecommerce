# E-Commerce App
Basic e commerce app to manage products and orders.

# How to run
We can run the database and the service using
`docker compose up db web -d`

To specifically run the test
`docker compose up web-test`

## Configuration
The db configuration can be controlled using the env vars setup in the
[docker compose file](/docker-compose.yml).

Postman collection from [here](/postman_collection.json) can be loaded to play around with the APIs.
