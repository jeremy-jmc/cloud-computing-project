const express = require('express');
const mongoose = require('mongoose');
const bodyParser = require('body-parser');

mongoose.connect(process.env.MONGO_URI, {
  // useNewUrlParser: true,
  // useUnifiedTopology: true
})
  .then(db => console.log('Db is connected to ', db.connection.host))
  .catch(err => console.error(err));

const app = express();
app.use((req, res, next) => {
    console.log('Método:', req.method, 'Ruta:', req.url, 'Cuerpo:', req.body);
    next();
});
app.use(bodyParser.json());

const promocionSchema = new mongoose.Schema({
  promocion_id: Number,
  monto: Number,
  nombre: String,
  descripcion: String,
  fecha_inicio: String, // TODO: cambiarlo a Date
  fecha_fin: String, // TODO: cambiarlo a Date
  dni: String
});

const campaniaSchema = new mongoose.Schema({
  campania_id: Number,
  monto: Number,
  nombre: String,
  descripcion: String,
  fecha_inicio: Date,
  fecha_fin: Date,
});

const Promocion = mongoose.model('promociones_exclusivas', promocionSchema);
const Campania = mongoose.model('campanias', campaniaSchema);

app.get('/', (req, res) => {
  res.json({ message: 'API Promociones is alive' });
});
// Obtener las promociones de campaña
app.get('/promociones', async (req, res) => {
  try {
    const currentDate = new Date();
    console.log(currentDate);
    const campania = await Campania.find({
      fecha_inicio: { $lte: currentDate },
      fecha_fin: { $gte: currentDate }
    }).lean();
    res.json(campania);
  } catch (error) {
    console.error(`Error: ${error.message}`);
    res.status(500).json({ error: 'Internal Server Error' });
  }
});

// Obtener las promociones exclusivas por DNI
app.get('/promociones_exclusivas/:dni', async (req, res) => {
  const { dni } = req.params;
  try {
    const promociones = await Promocion.find({ 'dni': dni }).lean();
    res.json(promociones);
  } catch (error) {
    console.error(`Error: ${error.message}`);
    res.status(500).json({ error: 'Internal Server Error' });
  }
});


app.listen(8003, () => {
  console.log('API de Promociones corriendo en el puerto 8003');
  console.log(process.env.MONGO_URI)
});
