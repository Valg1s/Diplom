function myFunction() {
  event.preventDefault();

  let menu = document.getElementById("myDropdown");
    menu.classList.toggle("show");
  }
  
 window.onclick = function(event) {
    if (!event.target.matches('.header__menu-img')) {
      var dropdowns = document.getElementsByClassName("dropdown-content");
      var i;
      for (i = 0; i < dropdowns.length; i++) {
        var openDropdown = dropdowns[i];
        if (openDropdown.classList.contains('show')) {
          openDropdown.classList.remove('show');
        }
      }
    }
  }
function ChangeWindow(number){
  event.preventDefault();
  
  let buttons = document.querySelectorAll(".myteam__link-button");
  let windows = document.querySelectorAll('.myteam__bloock'); 

  for (let i = 0;i < 3;i++){
    console.log(windows[i]);
    if (number == i+1){
      windows[i].classList.add('open');
      buttons[i].classList.add('opened');
    }else{
      windows[i].classList.remove('open');
      buttons[i].classList.remove('opened');
    }
  }
};

let input = document.getElementById("search_input");
tableRows = document.querySelectorAll('[id^="player_"]');

input.addEventListener("input",(event) => {
  let value = event.target.value.toLowerCase();

  tableRows.forEach(function(row) {
    const fullName = row.querySelector('.table_fullname').textContent.toLowerCase();

    if (value == ""){
      row.style.display = '';
    }else if (fullName.startsWith(value)) {
      row.style.display = '';
    }else{
      row.style.display = 'none';
    };

})
});

function sendDeleteForm(event,player_id,csrf_token){
  event.preventDefault();

  Swal.fire({
    title: 'Ви впевнені?',
    text: "Ви не зможете повернути назад!",
    icon: 'warning',
    showCancelButton: true,
    cancelButtonText:"Назад",
    confirmButtonColor: '#3085d6',
    cancelButtonColor: '#d33',
    confirmButtonText: 'Так,видалити'
  }).then((result) => {
    if (result.isConfirmed) {
      Swal.fire({
        title:'Видалено!',
        text:'Гравець був видалений з команди',
        icon:'success',
        timer: 2500,
      })

      let data = {
        "player_id":player_id,
        "method": "delete",
      }
  
      axios.post('/my_team/',
        data,
        {
          headers: {
            'X-CSRFToken': csrf_token,
            'Content-Type': 'application/json',
          }
        }
      ).then((request)=>{
        let tr = document.getElementById(`player_${player_id}`);
        tr.remove();
      })

    };
  })
}

function changeData(event){
  event.preventDefault();
  
  let change_password_block = document.getElementById('change_user_password');
  let email_field = document.getElementById("user_email");
  let button = document.getElementById("change_data_open")
  
  change_password_block.className = 'open';
  email_field.removeAttribute("readonly");
  email_field.className = '';
  button.classList.add("none");
}

function changeUserData(event,csrf_token){
  event.preventDefault();

  let email_field = document.getElementById("user_email").value;
  let password_1 = document.getElementById("password1").value;
  let password_2 = document.getElementById("password2").value;
  let error_email = document.getElementById("error_email");
  let error_password = document.getElementById("error_password");

  if (!email_field){
    error_email.className = "open";
    return;
  }
  console.log(password_1 != "" && password_2 != '')
  if (password_1 != "" && password_2 != ''){
    if (password_1.length < 6){
      error_password.textContent = "Пароль повинен бути більше 6 символів";
      error_password.className = "open";
      return; 
    }
    else if (password_1 != password_2){
      error_password.textContent = "Паролі повинні бути однакові";
      error_password.className = "open";
      return;
    }
  }

  let data = {
    'email_field':email_field,
    "password_1":password_1,
    "password_2":password_2,
    'method':"change_data"
  }

  axios.post("/my_team/",
  data,
  {headers:{
    'X-CSRFToken': csrf_token,
    'Content-Type': 'application/json',
  }}
  ).then((request) => {
    Swal.fire({
      title:'Змінено!',
      text:'Ваші дані успішно змінені',
      icon:'success',
      timer: 2500,
    })
    error_email.className = "none";
    error_password.className = "none";

  let change_password_block = document.getElementById('change_user_password');
  let email_field = document.getElementById("user_email");
  let button = document.getElementById("change_data_open")

  change_password_block.className = 'none';
  email_field.setAttribute("readonly","readonly");
  email_field.className = "blocked__input";
  button.classList.remove("none");

  } )
}

function createStatement(event){
  event.preventDefault();
  
  let form = document.getElementById("statement_form");

  Swal.fire({
    title:'Успішно!',
    text:'Заява успішно створена,очікуйте відповіді від адміністрації!\nПереадресація....',
    icon:'success',
    timer: 2500,
  }).then(() => {
    form.submit();
  })

}

function getStatistic(fullName,year,games,atack,defence){
  event.preventDefault();
  
  Swal.fire({
      title:`Статистика гравця \n ${fullName}`,
      html: `
      <p>Рік статистики: ${year}</p>
      <p>Кількість ігор: ${games}</p>
      <p>Зароблено пунктів: ${atack}</p>
      <p>Успішних захистів: ${defence}</p>
      `,
      showCloseButton: true,
      closeButtonText: "Закрити"
  })
}