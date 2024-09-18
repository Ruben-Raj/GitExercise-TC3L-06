const mongoose = require('mongoose');

// Define the tutor schema
const tutorSchema = new mongoose.Schema({
  name: {
    type: String,
    required: true,
  },
  eligibility: {
    type: String,
    required: true,
  },
  teachinghour: {
    type: String,
    required: true,
  },
  phonenumber: {
    type: String,
    required: true,
  },
  imageurls: [String],
  currentbookings: [String],
  language: {
    type: String,
    required: true,
  },
  description: {
    type: String,
    required: true,
  },
}, {
  timestamps: true,
});

// Create the model from the schema
const tutorModel = mongoose.model('Tutor', tutorSchema);

module.exports = tutorModel;
