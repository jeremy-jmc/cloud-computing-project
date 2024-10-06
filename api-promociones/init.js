// Selecciona la base de datos (si no existe, MongoDB la creará automáticamente)
db = db.getSiblingDB('promociones_db');

// Verificar si la colección 'promociones_exclusivas' existe
if (db.getCollectionNames().indexOf('promociones_exclusivas') < 0) {
  // Crear la colección sin validación de esquema temporalmente
  db.createCollection('promociones_exclusivas');  // Sin validación
  print("Colección 'promociones_exclusivas' creada sin validación temporalmente.");
} else {
  print("La colección 'promociones_exclusivas' ya existe.");
}

// Insertar datos de ejemplo solo si no existen en 'promociones_exclusivas'
if (db.promociones_exclusivas.countDocuments() === 0) {
  db.promociones_exclusivas.insertMany([
    {
      promocion_id: 1,
      monto: 50.00,
      nombre: "Promoción Exclusiva Cliente 1",
      descripcion: "Descuento especial para el cliente",
      fecha_inicio: "2024-10-01T00:00:00Z",  // Mantiene string
      fecha_fin: "2024-12-31T00:00:00Z",     // Mantiene string
      dni: "77777777"
    },
    {
      promocion_id: 2,
      monto: 30.00,
      nombre: "Promoción Exclusiva Cliente 2",
      descripcion: "Promoción personalizada para fidelización",
      fecha_inicio: "2024-09-01T00:00:00Z",  // Mantiene string
      fecha_fin: "2024-11-30T00:00:00Z",     // Mantiene string
      dni: "87654321"
    }
  ]);
  print("Datos insertados en la colección 'promociones_exclusivas'.");
} else {
  print("Los datos ya existen en la colección 'promociones_exclusivas'.");
}


// Verificar si la colección 'campanias' existe
if (db.getCollectionNames().indexOf('campanias') < 0) {
  // Definir esquema y crear la colección 'campanias'
  db.createCollection('campanias');
  print("Colección 'campanias' creada exitosamente.");
} else {
  print("La colección 'campanias' ya existe.");
}

// Insertar datos de ejemplo solo si no existen en 'campanias'
if (db.campanias.countDocuments() === 0) {
  db.campanias.insertMany([
    {
      campania_id: 1,
      monto: 20.00,
      nombre: "Campaña de Invierno",
      descripcion: "Descuentos generales para todos los usuarios",
      fecha_inicio: new Date("2024-07-01"),
      fecha_fin: new Date("2024-09-30")
    },
    {
      campania_id: 2,
      monto: 15.00,
      nombre: "Campaña de Verano",
      descripcion: "Ofertas generales para todos los socios del gimnasio",
      fecha_inicio: new Date("2025-01-01"),
      fecha_fin: new Date("2025-03-31")
    }
  ]);
  print("Datos insertados en la colección 'campanias'.");
} else {
  print("Los datos ya existen en la colección 'campanias'.");
}
    
// Mostrar los datos insertados en 'promociones_exclusivas'
print("Datos en la colección 'promociones_exclusivas':");
printjson(db.promociones_exclusivas.find().toArray());

// Mostrar los datos insertados en 'campanias'
print("Datos en la colección 'campanias':");
printjson(db.campanias.find().toArray());
