document.addEventListener('DOMContentLoaded', function () {
    const likeButtons = document.querySelectorAll('.like-btn');

    likeButtons.forEach(button => {
        button.addEventListener('click', function (event) {
            event.preventDefault(); // Evita el envío del formulario al hacer clic

            const likeIcon = this.querySelector('.like-icon');
            likeIcon.classList.add('zoom'); // Añade la clase de zoom

            // Simula el envío del formulario después de un pequeño retraso para mostrar el efecto
            setTimeout(() => {
                this.closest('form').submit();
            }, 300); // Ajusta el tiempo del delay según prefieras
        });
    });
});

$(document).ready(function(){
    // No mostrar el modal al cargar la página
    // Mostrar el modal solo cuando se haga clic en el enlace "Registrarse"
    $('.btn[data-target="#registerModal"]').on('click', function() {
        $('#registerModal').modal('show');
    });
});

