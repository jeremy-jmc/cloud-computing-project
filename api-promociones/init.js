// Selecciona la base de datos (si no existe, MongoDB la creará automáticamente)
db = db.getSiblingDB('promociones_db');

// Verificar si la colección 'promocions' existe
if (db.getCollectionNames().indexOf('promocions') < 0) {
  // Definir esquema y crear la colección
  db.createCollection('promocions', {
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
  print("Colección 'promocions' creada exitosamente.");
} else {
  print("La colección 'promocions' ya existe.");
}

// Insertar datos de ejemplo solo si no existen
if (db.promocions.countDocuments() === 0) {
  db.promocions.insertMany([
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
  print("Datos insertados en la colección 'promocions'.");
} else {
  print("Los datos ya existen en la colección 'promocions'.");
}

// Mostrar los datos insertados
print("Datos en la colección 'promocions':");
printjson(db.promocions.find().toArray());
