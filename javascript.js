/*
    Here i add hovering abilty to elements with '.hov-elemet' class
    so only they get triggered by a hover in a container with
    '.hov-container' class.
*/

let hoverContainers = document.querySelectorAll('.hov-container');

for(let hoverContainer of hoverContainers) {
  let hoverElem = hoverContainer.querySelector('.hov-elem');

  hoverContainer.addEventListener('mouseover', function(event) {
    if(!hoverElem) return;
    hoverElem.classList.add('hovered');
  });

  hoverContainer.addEventListener('mouseout', function(event) {
    if (!hoverElem.classList.contains('hovered')) return;
    hoverElem.classList.remove('hovered');
  });
}


/* Adding toggling functionality to account arrow */
