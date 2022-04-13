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
/* Note that this code snippet can be used in combination
   with 'data-toggle-id' attribute to add toggling functionality
   to any element in DOM */

document.addEventListener('click', function(event) {
  let container = event.target.closest('[data-toggle-id]');
  if(!container) return;

  let elem = document.getElementById(container.dataset.toggleId);
  let arrow = document.querySelector('.account .arrow-svg');

  elem.hidden = !elem.hidden;

  arrow.classList.toggle('rotate');
});


/* Slide Show For Aside Book Reccomendation */

let slideIndex = 1;
showSlides(slideIndex);

// Next/Prev Control
function plusSlides(n) {
  showSlides(slideIndex += n);
}

function currentSlide(n) {
  showSlides(slideIndex = n);
}

function showSlides(n) {
  let i;
  let slides = document.getElementsByClassName('mySlides');
  let dots = document.getElementsByClassName('dot');
  if(n > slides.length) slideIndex = 1;
  if(n < 1) slideIndex = slides.length;

  for(i = 0; i < slides.length; i++) {
    slides[i].style.display = "none";
  }

  for(i = 0; i < dots.length; i++) {
    dots[i].classList.remove('active');
  }

  dots[slideIndex - 1].classList.add('active');
  slides[slideIndex - 1].style.display = "block";
}
 

