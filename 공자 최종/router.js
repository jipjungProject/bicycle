var express = require('express');
var router = express.Router();
var PythonShell = require('python-shell');
var realresults;
var id;

require('date-utils');
var newDate = new Date();
var time = newDate.toFormat('YYYY-MM-DD HH24:MI:SS');

router.route('/').get(function(req,res){ // '/test' -> '/'
    res.render('index.html');
});

router.post('/send', function(req,res){
    console.log("input")
   
    var options = {
    mode: 'text',
    pythonPath: "C:\\Users\\romaa\\Anaconda3\\python.exe",     //window path
    pythonOptions: ['-u'],
    scriptPath: '', //실행할 파일의 path.
    args: [req.body.number, time],       // 대여소번호
    };


    // 여기서 python 실행하게.
    PythonShell.PythonShell.run('finaltest.py', options, function(err, results){
        if (err) throw err;
        
        else{
            console.log('finaltest.py 실행')
            console.log
            ('수요량: %j', results[0]);    // 수요.
            console.log
            ('공급량: %j', results[1]);    // 공급. 
            console.log
            ('공급-수요: %j', results[2]);    // 뺀거
            
            console.log
            ('현재 남은 대수: %j', results[3]);    // 수요.
            console.log
            ('ㅇ: %j', results[4]);    // 공급. 
            console.log
            ('ㅇ: %j', results[5]);    // 뺀거
            console.log
            ('대여소번호:%j',results[6]);
            
            
            realresults = results;    


            // 파이썬 쉘이 끝나기 전에 render는 무조건 최우선. 밖에 넣으면 값이 나오기전에 렌더한다.
            // undefined되버리니까, 파이썬 쉘 안에서 렌더해야함.
            res.render('result.html', {results123: realresults});
        }
    });
    
});

router.get('/info', function(req, res){
    console.log("info.html")
    
    var options1 = {
    mode: 'text',
    pythonPath: "C:\\Users\\romaa\\Anaconda3\\python.exe",     //window path
    pythonOptions: ['-u'],
    scriptPath: '', //실행할 파일의 path
    };

    var nowleft;
    // 여기서 python 실행하게.
    PythonShell.PythonShell.run('all.py', options1, function(err, results){
        if (err) throw err;
        
        else{
            console.log('all.py 실행')
            console.log
            ('현재대수: %j', results[0]);
            nowleft = results;    
            res.render('info.html', {results123: nowleft});
        }
    });
})



router.get('/intro', function(req, res){
    console.log("intro.html 페이지");
    res.render("intro.html");
});

router.get('/moveBicycle', function(req, res){
    
    var options2 = {
    mode: 'text',
    pythonPath: "C:\\Users\\romaa\\Anaconda3\\python.exe",     //window path
    pythonOptions: ['-u'],
    scriptPath: '', //실행할 파일의 path
    };

    var result;
    // 여기서 python 실행하게.
    PythonShell.PythonShell.run('route.py', options2, function(err, results){
        if (err) throw err;
        
        else{
            console.log('route.py 실행')
            console.log
            ('<메시지> %j', results);
            result = results;    
            res.render('moveBicycle.html', {results123: result});
        }
    });
})


module.exports =router;