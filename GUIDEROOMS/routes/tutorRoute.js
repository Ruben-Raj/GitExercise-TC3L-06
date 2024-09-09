const express = require('express');
const router = express.Router();
const tutorModel = require('../models/tutor');

// Route to get all tutors
router.get('/getalltutor', async (req, res) => {
  try {
    const tutor = await tutorModel.find();
    res.json(tutor); 
  } catch (error) {
    console.error('Error fetching tutors:', error);
    res.status(500).json({ message: 'Server Error' });
  }
});

// Add other routes here if needed

module.exports = router;
