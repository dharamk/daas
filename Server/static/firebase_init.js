var firebaseConfig = {
      apiKey: "AIzaSyD2REY8_lmDFUZPbmFzi1LsI6C4hWTSkkc",
      authDomain: "fir-example-252109.firebaseapp.com",
      databaseURL: "https://fir-example-252109.firebaseio.com",
      projectId: "firebase-example-252109",
      storageBucket: "firebase-example-252109.appspot.com",
      messagingSenderId: "591717006674",
      appId: "1:591717006674:web:a3c9a1ca10e9d20b928e8b"
};

function emwebedSignInWithTokenId(){
  var xhttp = new XMLHttpRequest();
  if (!xhttp) {
    alert('Fails to create XMLHttpRequest instance');
    return false;
  }
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      document.getElementById("demo").innerHTML = this.responseText;
    }
  };
  xhttp.open("GET", "/ajax/info", true);
  xhttp.send();
}



