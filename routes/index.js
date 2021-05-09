const express = require('express');
const router = express.Router();
const { exec } = require("child_process");
/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('index', { title: 'Express' });
});

router.post('/', function(req, res, next) {
  exec("python3 main2.py " +
      req.body.API_KEY + " " +
      req.body.SECRET_KEY + " " +
      req.body.USDT + " " +
      req.body.rate + " " +
      req.body.multipler + " " +
      req.body.symbol
      , (error, stdout, stderr) => {
    if (error) {
      res.send(`error: ${error.message}`);
      return;
    }
    if (stderr) {
      res.send(`stderr: ${stderr}`);
      return;
    }
    res.send(`stdout: ${stdout}`);
  });
  res.send(req.body);
});

module.exports = router;
