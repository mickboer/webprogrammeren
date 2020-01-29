// Auto tab function for question.html
function autotab(current,to) {
    if (current.value.length==1) {
        to.focus()
        }
}

// Backspage function in the game (question.html)
function backspace(current,to) {
    if (current.value.length == 0 && event.code == "Backspace") {
        to.focus()
        }
}


function validateForm() {
  var nickname = document.forms["input_nickname"]["nickname"].value;
  if (nickname == "") {
    alert("Please fill in Nickname");
    return false;
  }
  else if (nickname.length > 15) {
    alert("Nickname to long (max 15 characters)");
    return false;
  }
  const request = new XMLHttpRequest();
  request.open("GET", "/check?nickname="+ nickname);
  request.onload = () =>{
    const response = JSON.parse(request.responseText);
    if (response == false) {
      alert("Nickname already in use, please pick another");
    }
  }
  request.send();

}


