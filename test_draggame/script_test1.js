function allowDrop(ev) {
  console.log(ev, "EV allowDrop");
  ev.preventDefault();
  // var isempty =
}

function drag(ev) {
  ev.dataTransfer.setData("text", ev.target.id);
}

function drop(ev) {
  ev.preventDefault();
  var data = ev.dataTransfer.getData("text");
  ev.target.appendChild(document.getElementById(data));
}
