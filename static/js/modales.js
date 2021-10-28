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
    console.log(User)
    let nombre =document.getElementById('MostrarNombre').value = User["nombre"];
    let apellido =document.getElementById('Mostrarapellido').value=User["apellido"]; 
    let Cedula =document.getElementById('mostrar-cedula').value=User["cedula"];
    let usuario=document.getElementById('mostrar-usuario').value=User["usuario"];
    let pass =document.getElementById('mostrar-contraseña'); 
    let cargo =document.getElementById('mostrar-cargo').value=User["cargo"]; 
    let salario=document.getElementById('mostrar-salario').value=User["salario"];
    let fecha1=document.getElementById('mostrar-fecha-ingreso').value=User["fechaingreso"];
    let fecha2=document.getElementById('mostrar-fecha-termino').value=User["fechatermino"];
    let contrato=document.getElementById('mostrar-contrato').value=User["tipocontrato"];
    let dependencia=document.getElementById('mostrardependencia').value=User["dependencia"];
    
    
}

function CargarInfoEmpleadoEditar(User, key){
    
    let nombre =document.getElementById('EditarNombre').value = User['nombre'];
    let apellido =document.getElementById('EditarApellido').value = User['apellido']; 
    let Cedula =document.getElementById('EditarCedula').value=User["cedula"]; 
    let usuario =document.getElementById('EditarUsuario').value=User["usuario"]; 
    let pass =document.getElementById('editarcontraseña').value="sin modificar"; 
    let fecha1=document.getElementById('editarfechaingreso').value=User["fechaingreso"];
    let fecha2=document.getElementById('editarfechasalida').value=User["fechatermino"];
    let tipocontrato=document.getElementById('tipo-contrato').value=User["tipocontrato"];
    let cargo=document.getElementById('tipo-rol').value=User["cargo"];
    let salario=document.getElementById('editar-salario').value=User["salario"];
    let dependencia=document.getElementById('editar-dependencia').value=User["dependencia"];

    var formulario = document.getElementById('FormularioEditarEmpleado');
    formulario.setAttribute('action','/editar_empleado/'+key);
}




function CargarRetro(User) {
    let Autor =document.getElementById('Autoramostrar').value = User["autor"];
    let fecha1=document.getElementById('fechamostrar').value=User["fecha"];
    let retro =document.getElementById('retroalimentacion-text').value=User["retro"];
    let puntaje =document.getElementById('puntaje').value=User["puntaje"];
    
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


////////////////////////////////////////////////////////////////////////////////
