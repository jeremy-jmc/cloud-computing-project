package main

import (
	"log"
	"net/http"
	"github.com/gorilla/mux"
)

func main() {
	initDB()

	router := mux.NewRouter()

	router.HandleFunc("/membresias/{dni}", GetMembresia).Methods("GET")
	router.HandleFunc("/membresias/{dni}", CreateMembresia).Methods("POST")
	router.HandleFunc("/membresias/{dni}", UpdateMembresia).Methods("PUT")

	log.Fatal(http.ListenAndServe(":8002", router))

	

}

