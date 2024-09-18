const express = require('express');
const app = express();
const dbConfig = require('./db'); // Import the db.js file
const tutorRoute = require('./routes/tutorRoute');

// Middleware to parse JSON requests
app.use(express.json());

// Register the tutor route
app.use('/api/tutor', tutorRoute);

const port = process.env.PORT || 5000;
app.listen(port, () => console.log(`Node Server Started on port ${port}`));
