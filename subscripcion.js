document.getElementById('form-suscripcion').addEventListener('submit', async function(e) {
    e.preventDefault();
    const formData = new FormData(this);
    const data = Object.fromEntries(formData.entries());

    if (!data.terminos) {
        mostrarMensaje('Debes aceptar los términos y condiciones', 'error');
        return;
    }
    
    try {
        const response = await fetch('suscripcion.py', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        if (result.success) {
            mostrarMensaje('¡Suscripción exitosa! Ya puedes acceder a la tienda', 'exito');
            this.reset();
            
            // Guardar sesión del usuario
            localStorage.setItem('usuario_logueado', JSON.stringify({
                username: data.username,
                email: data.email
            }));
            setTimeout(() => {
                window.location.href = '#tienda';
            }, 2000);
        } else {
            mostrarMensaje(result.message || 'Error al procesar la suscripción', 'error');
        }
    } catch (error) {
        mostrarMensaje('Error de conexión. Intenta nuevamente', 'error');
        console.error('Error:', error);
    }
});
function mostrarMensaje(mensaje, tipo) {
    const mensajeDiv = document.getElementById('mensaje-respuesta');
    mensajeDiv.textContent = mensaje;
    mensajeDiv.className = tipo;
    mensajeDiv.style.display = 'block';

    setTimeout(() => {
        mensajeDiv.style.display = 'none';
    }, 5000);
}