const express = require('express');
const mongoose = require('mongoose');
const bodyParser = require('body-parser');

// Conectar con MongoDB
const db = async () => {
    try {
      const conn = await mongoose.connect(process.env.MONGO_URI);
      console.log(`MongoDB connected: ${conn.connection.host}`);
    } catch (error) {
      console.error(`Error: ${error.message}`);
      process.exit(1); // Detener la aplicación si hay un error en la conexión
    }
  };
  
const app = express();
app.use((req, res, next) => {
    console.log('Método:', req.method, 'Ruta:', req.url, 'Cuerpo:', req.body);
    next();
});
app.use(bodyParser.json());

const promocionSchema = new mongoose.Schema({
  promocion_id: Number,
  nombre: String,
  descuento: Number,
  tipo_membresia: String
});

const Promocion = mongoose.model('Promocion', promocionSchema);

// Obtener todas las promociones
app.get('/promociones', async (req, res) => {
    try {
        const promociones = await Promocion.find().lean();
        console.log('Promociones:', promociones);
        res.json(promociones);
    } catch (error) {
        console.error(`Error: ${error.message}`);
        res.status(500).json({ error: 'Internal Server Error' });
    }
});

// Crear una nueva promoción
app.post('/promociones', async (req, res) => {
  const { nombre, descuento, tipo_membresia } = req.body;
  const nuevaPromocion = new Promocion({ nombre, descuento, tipo_membresia });
  await nuevaPromocion.save();
  res.json({ message: 'Promoción creada' });
});

app.listen(8003, () => {
  console.log('API de Promociones corriendo en el puerto 8003');
});
