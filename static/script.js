// Auto tab functie voor question.html
function autotab(current,to){
    if (current.value.length==1) {
        to.focus()
        }
}

function backspace(current,to){
    if (current.value.length == 0 && event.code == "Backspace") {
        to.focus()
        }
}
