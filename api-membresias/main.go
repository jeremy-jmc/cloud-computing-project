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
    cliente_id          int    `json:"cliente_id"`
    dni                 string `json:"dni"`
    promo_id            int    `json:"promo_id"`
    fecha_inicio        string `json:"fecha_inicio"`
    fecha_fin           string `json:"fecha_fin"`
    estado              string `json:"estado"`
}

type Pago struct {
    pago_id             int    `json:"pago_id"`
    promo_id            int    `json:"promo_id"`
    cliente_id          int    `json:"cliente_id"`
    fecha_pago          string `json:"fecha_pago"`
    monto               float64 `json:"monto"`
    metodo_pago         string `json:"metodo_pago"`
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
    router.HandleFunc("/membresias/", createOrRenewMembresia).Methods("POST")
    router.HandleFunc("/membresias/", updateMembresia).Methods("PUT")

    fmt.Println("Servidor corriendo en el puerto 8002")
    log.Fatal(http.ListenAndServe(":8002", router))
}

func initializeDB() {
    _, err := db.Exec(`
        CREATE TABLE IF NOT EXISTS membresia_cliente (
            cliente_id SERIAL PRIMARY KEY,
            dni VARCHAR(20),
            promo_id INTEGER,
            fecha_inicio DATE,
            fecha_fin DATE,
            estado VARCHAR(20)
        );

        CREATE TABLE IF NOT EXISTS membresia_historial (
            id SERIAL PRIMARY KEY,
            tipo VARCHAR(50),
            fecha_inicio DATE,
            fecha_fin DATE,
            estado VARCHAR(20),
            cliente_id INTEGER REFERENCES membresia_cliente(cliente_id),
            promo_id INTEGER
        );

        CREATE TABLE IF NOT EXISTS membresia_pagos (
            pago_id SERIAL PRIMARY KEY,
            promo_id INTEGER,
            cliente_id INTEGER REFERENCES membresia_cliente(cliente_id),
            fecha_pago DATE,
            monto DECIMAL(10,2),
            metodo_pago VARCHAR(20)
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
        SELECT m.cliente_id, m.dni, m.promo_id, m.fecha_inicio, m.fecha_fin, m.estado
        FROM membresia_cliente m
        WHERE m.dni = $1
        ORDER BY m.fecha_fin DESC
        LIMIT 1
    `, dni).Scan(&membresia.cliente_id, &membresia.dni, &membresia.promo_id, &membresia.fecha_inicio, &membresia.fecha_fin, &membresia.estado)

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


func getClientePagos(w http.ResponseWriter, r *http.Request) {

    vars := mux.Vars(r)
    dni := vars["dni"]

    var pagos []Pago

    rows, err := db.Query(`
        SELECT p.pago_id, p.promo_id, p.cliente_id, p.fecha_pago, p.monto, p.metodo_pago
        FROM membresia_pagos p
        JOIN membresia_cliente m ON p.cliente_id = m.cliente_id
        WHERE m.dni = $1
        ORDER BY p.fecha_pago DESC
    `, dni)
    if err != nil {
        http.Error(w, err.Error(), http.StatusInternalServerError)
        return
    }
    defer rows.Close()

    for rows.Next() {
        var pago Pago
        err := rows.Scan(&pago.pago_id, &pago.promo_id, &pago.cliente_id, &pago.fecha_pago, &pago.monto, &pago.metodo_pago)
        if err != nil {
            http.Error(w, err.Error(), http.StatusInternalServerError)
            return
        }
        pagos = append(pagos, pago)
    }

    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(pagos)
}






func createOrRenewMembresia(w http.ResponseWriter, r *http.Request) {

	// // print w and r
	// fmt.Println(w)
	// fmt.Println(r)
    type Input struct {
        promoID   int    `json:"promo_id"`
        dni       string `json:"dni"`
        monto    float64 `json:"monto"`
        metodoPago string `json:"metodo_pago"`
    }
    var input Input

    err := json.NewDecoder(r.Body).Decode(&input)
    body, _ := json.Marshal(input)
    fmt.Println("body: ", string(body))
    

    if err != nil {
        http.Error(w, err.Error(), http.StatusBadRequest)
        return
    }

    //print 
    fmt.Println("promoID: ", input.promoID)
    fmt.Println("dni: ", input.dni)
    fmt.Println("monto: ", input.monto)
    fmt.Println("metodoPago: ", input.metodoPago)
    

    var clienteID int
    var fechaFin string
    err = db.QueryRow("SELECT cliente_id, fecha_fin FROM membresia_cliente WHERE dni = $1", input.dni).Scan(&clienteID, &fechaFin)

    // Si el cliente no existe, se crea una nueva membresía
    if err == sql.ErrNoRows {
        // print 
        fmt.Println("No se encontró el cliente")


        err = db.QueryRow(`
        INSERT INTO membresia_cliente (promo_id, dni, fecha_inicio, fecha_fin, estado)
        VALUES ($1, $2, CURRENT_DATE, CURRENT_DATE + INTERVAL '1 month', 'activa') RETURNING cliente_id
        `, input.promoID,  input.dni).Scan(&clienteID)
        if err != nil {
            http.Error(w, err.Error(), http.StatusInternalServerError)
            return
        }
        fmt.Println("cliente_id: ", clienteID)

        _, err = db.Exec(`
            INSERT INTO membresia_pagos (promo_id, cliente_id, fecha_pago, monto, metodo_pago)
            VALUES ($1, $2, CURRENT_DATE, $3, $4)
        `, input.promoID, clienteID, input.monto, input.metodoPago)

        if err != nil {
            http.Error(w, err.Error(), http.StatusInternalServerError)
            return
        }

        

        
        w.WriteHeader(http.StatusOK)
        w.Write([]byte("Membresía creada exitosamente"))
        return
    } else if err != nil {
        http.Error(w, err.Error(), http.StatusInternalServerError)
        return
    }

    // Si el cliente existe, se crea una nueva membresía

    err = db.QueryRow(`
        INSERT INTO membresia_cliente (dni, promo_id,fecha_inicio, fecha_fin, estado )
        VALUES ($1, $2, $3, $3 + INTERVAL '1 month', 'activa') RETURNING cliente_id
    `,  input.dni, input.promoID, fechaFin ).Scan(&clienteID)
    if err != nil {
        http.Error(w, err.Error(), http.StatusInternalServerError)
        return
    }

    _, err = db.Exec(`
        INSERT INTO membresia_pagos (promo_id, cliente_id, fecha_pago, monto, metodo_pago)
        VALUES ($1, $2, CURRENT_DATE, $3, $4)
    `, input.promoID, clienteID, input.monto, input.metodoPago)

    if err != nil {
        http.Error(w, err.Error(), http.StatusInternalServerError)
        return
    }

    w.WriteHeader(http.StatusOK)
    w.Write([]byte("Membresía renovada exitosamente"))
}

func updateMembresia(w http.ResponseWriter, r *http.Request) {

    var input struct {
        cliente_id  int    `json:"cliente_id"`        
        dni        string `json:"dni"`
        estado        string `json:"estado"`                
    }

    err := json.NewDecoder(r.Body).Decode(&input)
    if err != nil {
        http.Error(w, err.Error(), http.StatusBadRequest)
        return
    }

    

    _, err = db.Exec(`
        UPDATE membresia_cliente
        SET estado = $1
        WHERE cliente_id = $2 AND dni = $3
    `, input.estado,  input.cliente_id, input.dni)
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
