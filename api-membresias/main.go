package main

import (
	"database/sql"
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"os"

	"github.com/gorilla/mux"
	_ "github.com/lib/pq"
)

type Membresia struct {
    ID          int    `json:"id"`
    Tipo        string `json:"tipo"`
    FechaInicio string `json:"fecha_inicio"`
    FechaFin    string `json:"fecha_fin"`
    Estado      string `json:"estado"`
    ClienteID   int    `json:"cliente_id"`
}

type Cliente struct {
    ID   int    `json:"id"`
    DNI  string `json:"dni"`
    Nombre string `json:"nombre"`
}

var db *sql.DB

func main() {
    var err error
	host := os.Getenv("DB_HOST")
	port := os.Getenv("DB_PORT")
	user := os.Getenv("DB_USER")
	password := os.Getenv("DB_PASSWORD")
	dbname := os.Getenv("DB_NAME")

	var connStr string

	// Verificar si todas las variables de entorno están definidas
	if host != "" && port != "" && user != "" && password != "" && dbname != "" {
		connStr = fmt.Sprintf("host=%s port=%s user=%s password=%s dbname=%s sslmode=disable",
			host,
			port,
			user,
			password,
			dbname,
		)
	} else {
		// Usar cadena de conexión por defecto
		connStr = "host=localhost port=5432 user=postgres password=postgres dbname=postgres sslmode=disable"
	}

	fmt.Println("Using connection string: ", connStr)
    db, err = sql.Open("postgres", connStr)
    if err != nil {
        log.Fatal(err)
    }
    defer db.Close()

    err = db.Ping()
    if err != nil {
        log.Fatal(err)
    }

    // Inicializar la base de datos
    initializeDB()

    router := mux.NewRouter()
    router.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
        response := struct {
            StatusCode int    `json:"status_code"`
            Message    string `json:"message"`
        }{
            StatusCode: http.StatusOK,
            Message:    "API Membresias is alive",
        }

        w.Header().Set("Content-Type", "application/json")
        w.WriteHeader(http.StatusOK)
        json.NewEncoder(w).Encode(response)
    }).Methods("GET")

    router.HandleFunc("/membresias/{dni}", getMembresia).Methods("GET")
    router.HandleFunc("/membresias/{dni}", createOrRenewMembresia).Methods("POST")
    router.HandleFunc("/membresias/{dni}", updateMembresia).Methods("PUT")

    fmt.Println("Servidor corriendo en el puerto 8002")
    log.Fatal(http.ListenAndServe(":8002", router))
}

func initializeDB() {
    _, err := db.Exec(`
        CREATE TABLE IF NOT EXISTS clientes (
            id SERIAL PRIMARY KEY,
            dni VARCHAR(20) UNIQUE NOT NULL,
            nombre VARCHAR(100)
        );
        CREATE TABLE IF NOT EXISTS membresias (
            id SERIAL PRIMARY KEY,
            tipo VARCHAR(50),
            fecha_inicio DATE,
            fecha_fin DATE,
            estado VARCHAR(20),
            cliente_id INTEGER REFERENCES clientes(id)
        );
        CREATE TABLE IF NOT EXISTS pagos (
            id SERIAL PRIMARY KEY,
            fecha DATE,
            monto DECIMAL(10, 2),
            membresia_id INTEGER REFERENCES membresias(id)
        );
    `)
    if err != nil {
        log.Fatal(err)
    }
}

func getMembresia(w http.ResponseWriter, r *http.Request) {
    vars := mux.Vars(r)
    dni := vars["dni"]

    var membresia Membresia

    err := db.QueryRow(`
        SELECT m.id, m.tipo, m.fecha_inicio, m.fecha_fin, m.estado, m.cliente_id
        FROM membresias m
        JOIN clientes c ON m.cliente_id = c.id
        WHERE c.dni = $1
        ORDER BY m.fecha_fin DESC
        LIMIT 1
    `, dni).Scan(&membresia.ID, &membresia.Tipo, &membresia.FechaInicio, &membresia.FechaFin, &membresia.Estado, &membresia.ClienteID)

    if err == sql.ErrNoRows {
        http.Error(w, "Membresía no encontrada", http.StatusNotFound)
        return
    } else if err != nil {
        http.Error(w, err.Error(), http.StatusInternalServerError)
        return
    }

    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(membresia)
}

func createOrRenewMembresia(w http.ResponseWriter, r *http.Request) {
    vars := mux.Vars(r)
    dni := vars["dni"]

	// // print w and r
	// fmt.Println(w)
	// fmt.Println(r)

    var input struct {
        Tipo      string `json:"tipo"`
        ClienteID int    `json:"cliente_id"`
    }

    err := json.NewDecoder(r.Body).Decode(&input)
    if err != nil {
        http.Error(w, err.Error(), http.StatusBadRequest)
        return
    }

    var clienteID int
    err = db.QueryRow("SELECT id FROM clientes WHERE dni = $1", dni).Scan(&clienteID)
    if err == sql.ErrNoRows {
        err = db.QueryRow("INSERT INTO clientes (dni) VALUES ($1) RETURNING id", dni).Scan(&clienteID)
        if err != nil {
            http.Error(w, err.Error(), http.StatusInternalServerError)
            return
        }
    } else if err != nil {
        http.Error(w, err.Error(), http.StatusInternalServerError)
        return
    }

    _, err = db.Exec(`
        INSERT INTO membresias (tipo, fecha_inicio, fecha_fin, estado, cliente_id)
        VALUES ($1, CURRENT_DATE, CURRENT_DATE + INTERVAL '1 month', 'activa', $2)
    `, input.Tipo, clienteID)
    if err != nil {
        http.Error(w, err.Error(), http.StatusInternalServerError)
        return
    }

    w.WriteHeader(http.StatusOK)
    w.Write([]byte("Membresía creada o renovada exitosamente"))
}

func updateMembresia(w http.ResponseWriter, r *http.Request) {
    vars := mux.Vars(r)
    dni := vars["dni"]

    var input struct {
        Tipo        string `json:"tipo"`
        FechaInicio string `json:"fecha_inicio"`
        FechaFin    string `json:"fecha_fin"`
    }

    err := json.NewDecoder(r.Body).Decode(&input)
    if err != nil {
        http.Error(w, err.Error(), http.StatusBadRequest)
        return
    }

    var clienteID int
    err = db.QueryRow("SELECT id FROM clientes WHERE dni = $1", dni).Scan(&clienteID)
    if err == sql.ErrNoRows {
        http.Error(w, "Cliente no encontrado", http.StatusNotFound)
        return
    } else if err != nil {
        http.Error(w, err.Error(), http.StatusInternalServerError)
        return
    }

    _, err = db.Exec(`
        UPDATE membresias
        SET tipo = $1, fecha_inicio = $2, fecha_fin = $3
        WHERE cliente_id = $4
    `, input.Tipo, input.FechaInicio, input.FechaFin, clienteID)
    if err != nil {
        http.Error(w, err.Error(), http.StatusInternalServerError)
        return
    }

    w.WriteHeader(http.StatusOK)
    w.Write([]byte("Membresía actualizada"))
}

/*
go get github.com/gorilla/mux
go get github.com/lib/pq

go run *.go

https://ramadhansalmanalfarisi8.medium.com/how-to-dockerize-your-api-with-go-postgresql-gin-docker-9a2b16548520
https://github.com/ramadhanalfarisi/go-simple-dockerizing/blob/master/docker-compose.yml

*/
