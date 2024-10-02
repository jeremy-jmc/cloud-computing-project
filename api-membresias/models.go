package main

import (
	"database/sql"
	"fmt"
	"log"
	"os"

	_ "github.com/lib/pq"
	"github.com/joho/godotenv"

)




var db *sql.DB


type Membresia struct {
	id     int    `json:"id"`
	dni string `json:"dni"`
	tipo string `json:"tipo"`
	fecha_inicio string    `json:"fecha_inicio"`
	fecha_fin string    `json:"fecha_fin"`
	estado string `json:"estado"`
	cliente_id int `json:"cliente_id"`
}




func initDB() {
	err := godotenv.Load()
    if err != nil {
        log.Fatalf("Error loading .env file")
    }

    // Get environment variables
    dbHost := os.Getenv("DB_HOST")
    dbUser := os.Getenv("DB_USER")
    dbPassword := os.Getenv("DB_PASSWORD")
    dbName := os.Getenv("DB_NAME")
    dbPort := os.Getenv("DB_PORT")

    // Create connection string
    connStr := fmt.Sprintf("host=%s port=%s user=%s password=%s dbname=%s sslmode=disable",
        dbHost, dbPort, dbUser, dbPassword, dbName)

	db, err := sql.Open("postgres", connStr)

	if err != nil {
		log.Fatal(err)
	}
	if err = db.Ping(); err != nil {
		log.Fatal(err)
	}


	create_table := 
	`CREATE TABLE IF NOT EXISTS membresias (
		id SERIAL PRIMARY KEY,
		dni VARCHAR(8) NOT NULL,
		tipo VARCHAR(100) NOT NULL,
		fecha_inicio DATE NOT NULL,
		fecha_fin DATE NOT NULL,
		estado VARCHAR(100) NOT NULL,
		cliente_id INT NOT NULL
	);`

	_ , err = db.Exec(create_table)
	if err != nil {
		log.Fatal(err)
	}

	


	fmt.Println("Connected to the database")
}

