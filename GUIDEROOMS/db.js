const mongoose = require('mongoose');

// MongoDB connection URI
const mongoURL = 'mongodb+srv://RubenRaj2405:Ruben2405@guide-room.3jevp.mongodb.net/guide-room';

// Connect to MongoDB
mongoose.connect(mongoURL, {
 
})
  .then(() => console.log('MongoDB Connection Successful'))
  .catch((error) => {
    console.error('MongoDB Connection Failed', error);
    process.exit(1); // Exit the process if the connection fails
  });

// Export the mongoose instance to use in other parts of the application
module.exports = mongoose;
