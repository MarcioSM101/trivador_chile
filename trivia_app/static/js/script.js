$(document).ready(function(){
    // No mostrar el modal al cargar la página
    // Mostrar el modal solo cuando se haga clic en el enlace "Registrarse"
    $('.btn[data-target="#registerModal"]').on('click', function() {
        $('#registerModal').modal('show');
    });
});