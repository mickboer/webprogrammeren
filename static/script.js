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
  var x = document.forms["input_nickname"]["nickname"].value;
  if (x == "") {
    alert("Please fill in Nickname");
    return false;
  } else if (x.length > 15) {
    alert("Nickname to long (max 15 characters)");
    return false;
  }
}


