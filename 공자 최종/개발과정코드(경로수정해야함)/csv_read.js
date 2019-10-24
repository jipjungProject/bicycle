const csv = require('csv-parser');
const fs = require('fs');


//Here, we create a readStream using the fs module, pipe it into the csv object that will then fire the data event each time a new row from the CSV file is processed. The end event is triggered when all the rows from the CSV file are processed and we log a short message to the console to indicate that.

// data.csv를 읽는다. 

fs.createReadStream('data.csv')
  .pipe(csv())
  .on('data', (row) => {
    console.log(row);
  })
  .on('end', () => {
    console.log('CSV file successfully processed');
  });

