var openretro=document.getElementsByClassName("retro");
var ventanaRetro=document.querySelector('.modal-retro');
var closeRetro=document.querySelector('.cancelar-retro');
var fechaActual=document.getElementById('fechaActual');

console.log(openretro);


console.log(ventanaRetro);
    for(var i=0;i<openretro.length;i++){
        openretro[i].addEventListener('click',() =>{
            ventanaRetro.classList.add('show-modal-retro');
            })
    
    }

closeRetro.addEventListener('click',()=>{
    ventanaRetro.classList.remove('show-modal-retro');
})


function CambiarRuta(botom){
    var  today = new Date();
    var m = today.getMonth() + 1;
    fechaActual.value = today.getDate()+'/'+m+'/'+today.getFullYear();
    var formulario = document.getElementById('formularioRetroalimentacion');
    formulario.setAttribute('action','/generar_retroalimentación/'+botom.id);  
}