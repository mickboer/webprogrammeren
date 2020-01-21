const fills = document.querySelectorAll('#fill1, #fill2');
const empties = document.querySelectorAll('.empty');

console.log(fills)
console.log(empties)
// Fill listeners
for (const empty of empties) {
  empty.addEventListener('dragover', dragOver);
  empty.addEventListener('dragenter', dragEnter);
  empty.addEventListener('dragleave', dragLeave);

for (var fill of fills) {

  fill.addEventListener('dragstart', dragStart);
  fill.addEventListener('dragend', dragEnd);

  // Loop through empty boxes and add listeners
  empty.addEventListener('drop', dragDrop);

  }
  console.log(fill)

  // Drag Functions
  function dragDrop(even) {

    console.log(even, 'The event from drag')
    console.log('drop')
    this.className = 'empty';
    this.append(fill);
  }

}

function dragStart() {
  console.log('start')
  this.className += ' hold';
  setTimeout(() => (this.className = 'invisible'), 0);
}

function dragEnd() {
  console.log('end')
  this.className = 'fill';
}

function dragOver(e) {
  console.log('over')
  e.preventDefault();

}

function dragEnter(e) {
  console.log('enter')
  var filldrag = fill
  e.preventDefault();
  this.className += ' hovered';
}

function dragLeave() {
  console.log('leave')
  this.className = 'empty';
}
