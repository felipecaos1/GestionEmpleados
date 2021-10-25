var open2=document.querySelector('#crearEmpleado');
var close2=document.querySelector('#cancelar-ventana-crear');
var ventana2=document.querySelector('#modal-crear-empleado');

open2.addEventListener('click',()=>{
    ventana2.classList.add('show-modal-crear-empleado');
})

close2.addEventListener('click', () =>{
    ventana2.classList.remove('show-modal-crear-empleado');
})

///////////////////////////////////////////////////////////////////////////////////


///////////////////////////////////////////////////////////////////////////////////

var ver=document.getElementsByClassName("ver");
var verinfo=document.querySelector('.modal-ver-empleado');
var closever=document.querySelector('.cancelar-ventana-ver');



for(var i=0;i<ver.length;i++){
    ver[i].addEventListener('click',() =>{
        verinfo.classList.add('show-modal-retro');
        })

}
closever.addEventListener('click',()=>{
    verinfo.classList.remove('show-modal-retro');
})

function CargarInfoEmpleado(User) {
    let nombre =document.getElementById('MostrarNombre').value = User['nombre'];
    let apellido =document.getElementById('Mostrarapellido').value = User['apellido']; 
    let Cedula =document.getElementById('crear-cedula'); 
    let usuario =document.getElementById('crear-usuario'); 
    let pass =document.getElementById('crear-contraseña'); 
}
///////////////////////////////////////////////////////////////////////////////////////////

var editar=document.getElementsByClassName("editar");
var editarinfo=document.querySelector('.modal-editar-empleado');
var closeeditar=document.querySelector('.cancelar-ventana-editar');

for(var i=0;i<ver.length;i++){
    editar[i].addEventListener('click',() =>{
        editarinfo.classList.add('show-modal-retro');
        })

}
closeeditar.addEventListener('click',()=>{
    editarinfo.classList.remove('show-modal-retro');
})

function CargarInfoEmpleadoEditar(User, key){
    let nombre =document.getElementById('EditarNombre').value = User['nombre'];
    let apellido =document.getElementById('EditarApellido').value = User['apellido']; 
    let Cedula =document.getElementById('EditarCedula'); 
    let usuario =document.getElementById('EditarUsuario'); 
    let pass =document.getElementById('crear-contraseña'); 

    
    var formulario = document.getElementById('FormularioEditarEmpleado');
    formulario.setAttribute('action','/editar_empleado/'+key.id);
}
////////////////////////////////////////////////////////////////////////////////
