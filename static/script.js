// Auto tab functie voor question.html
function autotab(current,to){
    if (current.getAttribute && current.value.length==current.getAttribute("maxlength")) {
        to.focus()
        }
}
