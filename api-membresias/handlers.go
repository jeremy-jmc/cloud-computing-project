package main 

import (
	"encoding/json"
	"net/http"

	"github.com/gorilla/mux"
)



type Response struct {
	Status string `json:"status"`
	Message string `json:"message"`
	Data interface{} `json:"data"`
}


func GetMembresia(w http.ResponseWriter, r *http.Request) {
	// print 

	fmt.Println("GetMembresia")

	vars := mux.Vars(r)
	dni := vars["dni"]

	m := Membresia{}
	err := db.QueryRow("SELECT id, tipo, fecha_inicio, fecha_fin, estado, cliente_id FROM membresias WHERE dni=$1", dni).Scan(&m.id, &m.dni,  &m.tipo, &m.fecha_inicio, &m.fecha_fin, &m.estado, &m.cliente_id)
	if err != nil {

		response := Response{Status: "404", Message: "No se encontró la membresía", Data: nil}
		json.NewEncoder(w).Encode(response)
		return
	}

	response := Response{Status: "success", Message: "Membresía encontrada", Data: m}
	json.NewEncoder(w).Encode(response)

}

func CreateMembresia(w http.ResponseWriter, r *http.Request) {

	var m Membresia

	

	err := json.NewDecoder(r.Body).Decode(&m)
    if err != nil {
        response := Response{Status: "400", Message: "Invalid request payload", Data: nil}
        json.NewEncoder(w).Encode(response)
        return
    }	

	
    _, err = db.Exec("INSERT INTO membresias (dni, tipo, fecha_inicio, fecha_fin, estado, cliente_id) VALUES ($1, $2, $3, $4, $5, $6)", m.dni, m.tipo, m.fecha_inicio, m.fecha_fin, m.estado, m.cliente_id)
	if err != nil {
		response := Response{Status: "500", Message: "No se pudo crear la membresía", Data: nil}
		json.NewEncoder(w).Encode(response)
		return
	}

	response := Response{Status: "success", Message: "Membresía creada", Data: m}
	json.NewEncoder(w).Encode(response)

}


func UpdateMembresia( w http.ResponseWriter, r *http.Request) {
	vars := mux.Vars(r)
	id := vars["id"]

	var m Membresia
	json.NewDecoder(r.Body).Decode(&m)

	_, err := db.Exec("UPDATE membresias SET tipo=$1, fecha_inicio=$2, fecha_fin=$3, estado=$4, cliente_id=$5 WHERE id=$6", m.tipo, m.fecha_inicio, m.fecha_fin, m.estado, m.cliente_id, id)
	if err != nil {
		response := Response{Status: "500", Message: "No se pudo actualizar la membresía", Data: nil}
		json.NewEncoder(w).Encode(response)
		return
	}

	response := Response{Status: "success", Message: "Membresía actualizada", Data: m}
	json.NewEncoder(w).Encode(response)
}


