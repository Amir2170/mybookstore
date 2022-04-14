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
 


// Rating System For Books

let books = Array.from(document.querySelectorAll('.book'));

/* Here i add an event listener on each book in order to 
   differenciate between each book rating otherwise ratings 
   would have impacts on one another 
*/

books.map((book) => {
  book.addEventListener('click', function(event) {
    if(event.target.classList.contains('fa-star')) {
      let ratingStars = Array.from(book.querySelectorAll('.book-rating .fa-star'));
      executeRating(ratingStars);
      /* And finally click the target so it triggers handlers on it
        otherwise it would need another click to trigger it when the 
        page first loads...very annoying experience if you ask me!*/  
      event.target.click(); 
    }
  });
});
/*
   recieves an array of stars and add click handler to each 
   array member, get it's index and check if it's active or inactive 
   and do the appropriate action.
 */
function executeRating(stars) { 
  // with stars array length being here loop shouldn't 
  // check it every time it iterates
  let starLength = stars.length;  
  let i;

  stars.map((star) => {
    star.addEventListener('click', function(event) {
      i = stars.indexOf(star);

      if(star.classList.contains('checked')) {
        for(i; i < starLength; i++) {
          stars[i].classList.remove('checked');
        }
      } else {
        for(i; i >= 0; i--) {
          stars[i].classList.add('checked');
        }
      };
    });
  });
}