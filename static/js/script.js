document.addEventListener('DOMContentLoaded', function() {
    
    // === 1. LÓGICA DEL OJITO (MOSTRAR/OCULTAR CONTRASEÑA) ===
    // Buscamos todos los iconos de ojo (sirve para Login y Signup)
    const togglePasswords = document.querySelectorAll('#eyeIcon');
    
    togglePasswords.forEach(eye => {
        eye.addEventListener('click', function() {
            // Buscamos el input que está justo antes o en el mismo grupo
            const passwordInput = this.parentElement.querySelector('input');
            
            if (passwordInput) {
                // Intercambiamos el tipo de input
                const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
                passwordInput.setAttribute('type', type);
                
                // Intercambiamos el icono (ojo abierto / ojo tachado)
                this.classList.toggle('fa-eye');
                this.classList.toggle('fa-eye-slash');
            }
        });
    });

    // === 2. CONFIRMACIÓN AL CERRAR SESIÓN ===
    // Para que Armando o los alumnos no se salgan por error
    const logoutLinks = document.querySelectorAll('.logout-link, .logout-btn');
    
    logoutLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            const respuesta = confirm("¿Estás seguro de que deseas salir de EDIFICA?");
            if (!respuesta) {
                e.preventDefault(); // Cancela el redireccionamiento
            }
        });
    });

    // === 3. EFECTO DE SELECCIÓN EN EMOCIONES (INDEX) ===
    // Para que el alumno sienta que el click funcionó antes de enviar
    const emotionCards = document.querySelectorAll('.card-option');
    
    emotionCards.forEach(card => {
        card.addEventListener('click', function() {
            // Quitamos la clase 'selected' de todos
            emotionCards.forEach(c => c.style.transform = "scale(1)");
            // La ponemos en el actual
            this.style.transform = "scale(1.05)";
            this.style.transition = "0.2s";
        });
    });

});