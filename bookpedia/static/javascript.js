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
  let dots = document.getElementsByClassName('dot');
  /* in case there is no books to recommend return and do nothing  
  so javascript file works */
  if( dots.length == 0) return
  
  let i;
  let slides = document.getElementsByClassName('mySlides');


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



// Rating System For Book

let logOutElem = document.querySelector('.log-out');

if(logOutElem !== null) {
  let stars = Array.from(document.querySelectorAll('.book-info .book-rating .fa-star'));
  let starsLength = stars.length;
  let i;

  if(stars.length != 0) {
    stars.map((star) => {
      star.addEventListener('click', ratingHandler);
    });
  }

  // Rating handler function 
  // reason behind defining a function is removing it later 
  // at fetch request after a successfull vote.
  function ratingHandler(event) {

    i = stars.indexOf(this)


    if(stars[i].classList.contains('checked')){      
      for(i; i < starsLength; i++) {
        stars[i].classList.remove('checked')
      }
    } else {
      for(i; i >= 0; i--) {
        stars[i].classList.add('checked')
      }
    }
  }
}


//function executeRating(stars) {
//  let starsLength = stars.length;
//  let i;
//
//  stars.map((star) => {
//    star.addEventListener('click', function(event) {
//        i = stars.indexOf(star)
//
//
//        if(stars[i].classList.contains('checked')){      
//          for(i; i < starsLength; i++) {
//            stars[i].classList.remove('checked')
//          }
//        } else {
//          for(i; i >= 0; i--) {
//            stars[i].classList.add('checked')
//          }
//        }
//      });
//    });
//};

/* Pagination functionality */

let url = new URL(window.location.href); // get the full url first

if(url.searchParams.has('page')) {

  let page_num = Number(url.searchParams.get('page')); // get page number from search parameters in url

  let pages = Array.from(document.querySelectorAll('.pagination .page-nums')); // get an array from page buttons aka links so they can be accessed easily later


  let current_page = pages[page_num - 1];

  current_page.classList.add('active'); // now add the active class using page number

}
/* Rating system fetch api */


let rating_form = document.querySelector('.rate .book-rating');

if(rating_form !== null) { /* if there is such an element in docuement 
                              otherwise remove code snippet below in 
                              if statement in order to avoid errros */

  rating_form.addEventListener('submit', async function(event) {
    event.preventDefault();

    let form = new FormData(rating_form);
    /* Append the sumbit button name AKA rate so that server can access that and actually 
       save this number if this line was not here server wouldn't have any number to create 
       a review object with */
    form.append(event.submitter.getAttribute('name'), event.submitter.getAttribute('name'));

    let url = rating_form.getAttribute('action')
    let response = await fetch(url, {
      method: 'POST',
      body: form,
    });

    let result = await response.json();

    /* in case user is not authenticated,
      view returns a 401 status code */
    if(response.status == 401) {
      Swal.fire({
        icon: "error",
        title: "Login, Please.",
        text: "Login In Order To Be Able To Rate This Book.",
        background: "#ECECEC",
      });
      return;
    /* and if user has voted this book before
      view returns 423 status code */
    } else if(response.status == 423) {                                     
      Swal.fire({                       
        icon: "error",
        title: "Sorry, You Can't Rate Twice.",
        text: "You Have Rated This Book Before.",
        background: "#ECECEC",
      });
      return;
    } else if(response.status == 400 && result['error'] == 'invalid form') {
      window.location.replace('');
      Swal.fire({                       
        icon: "error",
        title: "Ooops...",
        text: "Something Went Wrong, Invalid Inputs",
        background: "#ECECEC",
      });
      return;
    } else if(response.status == 400 && result['error'] == 'book does not exists') {
      window.location.replace('');
      Swal.fire({                       
        icon: "error",
        title: "Ooops...",
        text: "Something Went Wrong, No Such A Book Available.",
        background: "#ECECEC",
      });
      return;
    }
    // now user can rate ask first
    Swal.fire({
      icon: "success",
      title: "Thanks",
      text: "Your Score Has Been Submitted.",
      background: "#ECECEC",
    });
  });
}
/* Modals Functionality */

window.onload = function() {

  let auth_modal = document.querySelector('.modal-auth');

  let usr_create_modal = document.querySelector('.modal-user-create');

  let modal_cls_btns =  Array.from(document.querySelectorAll('.modal-close')); /* 1-Get buttons that closes modal and turn then into an array*/

  let auth_modal_btn = document.querySelector('.myaccount .sign-in'); /* Button that opens login modal */

  let usr_creation_btn = document.querySelector('.myaccount .create-account'); /* Button that opens user creation modal */ 

  auth_modal_btn.addEventListener('click', function(event) {
    auth_modal.style.display = 'block';
  });
 
  /* 2-Add event listener to close both modals to each close button using map function an earlier mentioned array*/
  modal_cls_btns.map((btn) => { 
    btn.addEventListener('click', function(event) {
      auth_modal.style.display = 'none';
      usr_create_modal.style.display = 'none';
    });
  });

  usr_creation_btn.addEventListener('click', function(event) {
    usr_create_modal.style.display = 'block';
  });

};


/* Login Modal Authentication */

let auth_form = document.querySelector('.auth-form');
let auth_error_container = document.querySelector('.modal-auth .modal-error'); 
let auth_error = document.querySelector('.modal-auth .modal-error .error-content');

auth_form.addEventListener('submit', async function(event) {
  
  event.preventDefault();

  let url = auth_form.getAttribute('action');

  let response = await fetch(url, {
    method: 'POST',
    body: new FormData(auth_form),
  });

  let result = await response.json();

  if(response.status == 400) {
    auth_error.textContent = result['__all__'];
    auth_error_container.style.display = 'block';
  } else {
    auth_error.textContent = "";
    auth_error_container.style.display = 'none';
    location.reload();
  }

});


/* Creating Account Modal */

let usr_creation_form = document.querySelector('.user-creation-form');
let usr_error_container = document.querySelector('.modal-user-create .modal-error');
let usr_creation_error = document.querySelector('.modal-user-create .modal-error .error-content');

usr_creation_form.addEventListener('submit', async function(event) {
  event.preventDefault();

  let url = usr_creation_form.getAttribute('action')

  let response = await fetch(url, {
    method: 'POST',
    body: new FormData(usr_creation_form),
  });

  let result = await response.json();
  let errors = "";

  /* In order to be able to show errors whether they are username or password related
     i have put them inside a string variable and then placed them inside error container */ 
  for(let error of Object.values(result)) {
    errors += (String(error) + '\n');
  }

  if(response.status == 400) {
    usr_creation_error.textContent = errors;
    usr_error_container.style.display = 'block';
  } else {
    usr_creation_error.textContent = "";
    usr_error_container.style.display = 'none';
    location.reload();
  }
});


/* Adding books to favorite list */

let fav_forms = Array.from(document.querySelectorAll('.add-fav-form'));

fav_forms.map(form => {
  form.addEventListener('submit', async function(event) {
    event.preventDefault();
    
    let url = form.getAttribute('action');
    let response = await fetch(url, {
      method: 'POST',
      body: new FormData(form),
    });

    let result = await response.json();

    /* if user is not authenticated */
    if(response.status == 401 && result['success'] == false) {
      Swal.fire({                       
        icon: "error",
        title: "Ooops...",
        html: "You Need To Log In In Order To Be Able<br>To Add This Book To Your Favorites.",
        background: "#ECECEC",
      });
      return; /* return here so success message won't show up */
    }

    /* if book already exists in user favorite list
       already took care of this in template by not 
       showing add button for these books but i didn't 
       want to leave anything unhandled */
    if(response.status == 400 && result['success'] == false) {
      Swal.fire({                       
        icon: "error",
        title: "Ooops...",
        text: "Book Already Exists In Your Favorites List.",
        background: "#ECECEC",
      });
      return;
    }
    
    if(response.status == 200 && result['success'] == true) {
      /* success case */
      Swal.fire({
        icon: "success",
        title: "Book Just Added!",
        text: "This Book Has Been Added To Your Favorites List.",
        background: "#ECECEC",
      }).then(function() { /* then reload when sweetalert promise is resolved */
        location.reload();
      });
      return;
    }

    // Handle unsuccessful cases for whatever unusual reasons
    Swal.fire({                       
      icon: "error",
      title: "Ooops...",
      text: "Sorry, There Is An Error Removing This Book From Your Favorites.",
      background: "#ECECEC",
    });

  })
});

/* Removing Book From Favorites List */

// get all remove from favorites buttons and turn them into an array
let rmv_fav_btns = Array.from(document.querySelectorAll('.rmv-fav-form'));

// now use map on'em to add eventlistener and fetch api 
rmv_fav_btns.map(btn => {
  btn.addEventListener('submit', async function(event) {
    // prevernt form from submitting to add some logic to it
    event.preventDefault();

    let url = btn.getAttribute('action');
    let response = await fetch(url, {
      method: 'POST',
      body: new FormData(btn),
    });

    let result = await response.json();

    // handle successful case
    if(response.status == 200 && result['success'] == true) {
      Swal.fire({
        icon: "success",
        title: "Book Just Removed!",
        text: "This Book Has Been Removed From Your Favorites List.",
        background: "#ECECEC",
      }).then(function() {
        location.reload();
      });
    } else {
      // Handle unsuccessful cases for whatever unusual reasons
      Swal.fire({                       
        icon: "error",
        title: "Ooops...",
        text: "Sorry, There Is An Error Removing This Book From Your Favorites.",
        background: "#ECECEC",
      });
    }
  })
});
