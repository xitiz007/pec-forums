
function show_password()
{
    var password_field = document.querySelector('#id_password');
    var checkbox = document.querySelector('#checkbox');

    const type= password_field.getAttribute('type') === "text" ? "password" : "text";
    password_field.setAttribute('type', type);
}


function like_button()
{
    console.log('clicked');
}

