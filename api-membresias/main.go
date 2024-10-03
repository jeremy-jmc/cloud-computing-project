package main

import (
	"log"
	"net/http"

	"github.com/gorilla/mux"
)

func main() {
	initDB()

	router := mux.NewRouter()

	router.Handle("/is_alive", http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusOK)
		w.Write([]byte("I'm alive!"))
	}))
	router.HandleFunc("/membresias/{dni}", GetMembresia).Methods("GET")
	router.HandleFunc("/membresias/{dni}", CreateMembresia).Methods("POST")
	router.HandleFunc("/membresias/{dni}", UpdateMembresia).Methods("PUT")

	log.Fatal(http.ListenAndServe(":8002", router))

}

/*
go get github.com/gorilla/mux
go get github.com/lib/pq

go run *.go

https://ramadhansalmanalfarisi8.medium.com/how-to-dockerize-your-api-with-go-postgresql-gin-docker-9a2b16548520
https://github.com/ramadhanalfarisi/go-simple-dockerizing/blob/master/docker-compose.yml

*/
