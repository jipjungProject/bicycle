//const csv = require('csv-parser');
//const fs = require('fs');


// CSV를 write해서 저장한다.

const createCsvWriter = require('csv-writer').createObjectCsvWriter;
const csvWriter = createCsvWriter({
  path: 'out.csv',
  header: [
    {id: 'number', title: 'number'},    // title이 맨위 컬럼 이름.
    {id: 'date', title: 'date'},
    {id: 'temperature', title: 'temperature'},
    {id: 'rain', title: 'rain'},
    {id: 'wind', title:'wind'},
    {id: 'humidity', title:'humidity'},
    {id: 'snow', title:'snow'}]
});

const data = [
    {
        number: 700,
        date: '2019-10-14 10:00:00',
        temperature: 10,
        rain: 10,
        wind: 10,
        humidity:10,
        snow:10,
    }, 
    {
        number: 700,
        date: '2019-10-14 11:00:00',
        temperature: 11,
        rain: 11,
        wind: 11,
        humidity:11,
        snow:11,  
    }, 
    {
        number: 700,
        date: '2019-10-14 12:00:00',
        temperature: 12,
        rain: 12,
        wind: 12,
        humidity:12,
        snow:12,
    }
];

csvWriter
  .writeRecords(data)
  .then(()=> console.log('The CSV file was written successfully'));