// Selecciona la base de datos (si no existe, MongoDB la creará automáticamente)
db = db.getSiblingDB('promociones_db');

// Definir esquema y colección
db.createCollection('Promocion', {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["promocion_id", "nombre", "descuento", "tipo_membresia"],
      properties: {
        promocion_id: {
          bsonType: "int",
          description: "Debe ser un número entero y es obligatorio"
        },
        nombre: {
          bsonType: "string",
          description: "Debe ser una cadena de texto y es obligatorio"
        },
        descuento: {
          bsonType: "double",
          minimum: 0,
          maximum: 100,
          description: "Debe ser un número entre 0 y 100 y es obligatorio"
        },
        tipo_membresia: {
          bsonType: "string",
          description: "Debe ser una cadena de texto y es obligatorio"
        }
      }
    }
  }
});

// Insertar datos de ejemplo en la colección "Promocion"
db.Promocion.insertMany([
  {
    promocion_id: 1,
    nombre: "Promoción Verano",
    descuento: 0.15,
    tipo_membresia: "premium"
  },
  {
    promocion_id: 2,
    nombre: "Promoción Invierno",
    descuento: 0.2,
    tipo_membresia: "estándar"
  },
  {
    promocion_id: 3,
    nombre: "Promoción Primavera",
    descuento: 0.1,
    tipo_membresia: "básica"
  }
]);

// Mostrar los datos insertados
print("Datos insertados en la colección 'Promocion':");
printjson(db.Promocion.find().toArray());
