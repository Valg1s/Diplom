
let form = document.getElementById('statement_form');

alert(form);

form.addEventListener('submit', function(event) {
        alert("Event created")
        event.preventDefault();

        document.getElementById('popup').style.display = 'block';

        setTimeout(function() {
            window.location.href = '/';
        }, 2000);
   });