function showPassword(){
    let eye = document.getElementById('showPassword');
    let password = document.getElementById('Inputpassword');
    if(password.type == 'password'){
        password.type = 'text';
        eye.style.color = '#024485c9';
        eye.style.transitionDuration = '0.5s';
    }else{
        eye.style.transitionDuration = '0.5s';
        eye.style.color = 'black';
        password.type = 'password';
    }
}


