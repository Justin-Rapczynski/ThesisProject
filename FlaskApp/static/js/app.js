

// $(document).ready(function() {

// 	$('index').on('submit', function(event) {

// 		$.ajax({
// 			data : {
// 				zip : $('#zipCodeInput').val(),
// 			},
// 			type : 'POST',
// 			url : '/process'
// 		})
// 		.done(function(data) {

// 			document.getElementById("output").innerHTML = data.zip;


// 		});

// 		event.preventDefault();

// 	});

// });


const menu = document.querySelector('#mobile-menu')
const menuLinks = document.querySelector('.navbar__menu')

//Display menu (for mobile)
const mobileMenu = () => {
    menu.classList.toggle('is-active')
    menuLinks.classList.toggle('active')

}

menu.addEventListener('click', mobileMenu)
