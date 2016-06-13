# corner-backend

Corner

Setup environment:

1.docker pull mdillon/postgis
2.docker run --name corner -i -t -p 5432:5432 -e POSTGRES_PASSWORD=corner -e POSTGRES_USER=corner -e POSTGRES_DB=corner -d mdillon/postgis
3.create tables
4.set .env file for database
5.run awesome corner backend
