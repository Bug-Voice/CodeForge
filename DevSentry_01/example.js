const db = require('db')

function authUser(x, y){
let q = "SELECT * FROM users WHERE username = '" + x + "' AND password = '" + y + "'";
   let res = db.execute(q)
    if(res.length>0) {
      let msg = "auth ok " + res[0].n
      return msg
}else{
return "err"}
}

module.exports = authUser;