// cliente.js (optimizado)

// Base URL de la API (ajusta según el entorno de producción si es necesario)
const BASE_URL = 'http://127.0.0.1:8000/client'; // Cambia '127.0.0.1' según la IP o el dominio en producción
const BASE_URL2= 'http://127.0.0.1:8000/reservas'
const BASE_URL3= 'http://127.0.0.1:8000/reservas2'
// Función para mostrar mensajes de error
function mostrarError(elemento, mensaje) {
    elemento.innerText = mensaje;
    elemento.style.display = 'block';
}

// Cargar reservas del cliente al cargar la página
document.addEventListener('DOMContentLoaded', async () => {
    const token = localStorage.getItem('token');
    const errorElemento = document.getElementById('reservas-error');
    
    try {
        const response = await fetch(`${BASE_URL2}`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });

        if (!response.ok) {
            throw new Error('No se pudieron cargar las reservas.');
        }

        const reservas = await response.json();
        console.log(reservas)
        const tableBody = document.querySelector('#reservas-table tbody');
        tableBody.innerHTML = reservas.map(reserva => `
            <tr>
                <td>${reserva.servicio_id}</td>
                <td>${new Date(reserva.fecha).toLocaleDateString()}</td>
                <td>${reserva.cliente_id}</td>
                <td>${reserva.trabajador_id}</td>
                <td><button onclick="cancelarReserva(${reserva.id})">Cancelar</button></td>
            </tr>
        `).join('');
    } catch (error) {
        mostrarError(errorElemento, error.message);
    }
});
// Agendar una nueva cita
document.getElementById('agendar-form').addEventListener('submit', async (e) => {
    e.preventDefault();

    const servicio = parseInt(document.getElementById('servicio').value,10);
    const fecha = document.getElementById('fecha').value;
    const profesional = Math.floor(Math.random() * (5 - 1 + 1)) + 1;
    const errorElemento = document.getElementById('agendar-error');

    errorElemento.style.display = 'none'; // Ocultar mensaje de error

    const token = localStorage.getItem('token');
    try {
        console.log({ servicio_id: servicio, fecha: fecha, trabajador_id: profesional });

        const response = await fetch(`${BASE_URL3}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({
                servicio_id: servicio,
                fecha: fecha,
                trabajador_id: profesional})
        });

        if (!response.ok) {
            throw new Error('Error al agendar la cita. Intenta nuevamente.');
        }

        // Cita agendada exitosamente, recargar reservas
        window.location.reload();
    } catch (error) {
        mostrarError(errorElemento, error.message);
    }
});

// Realizar pago
// document.getElementById('pago-form').addEventListener('submit', async (e) => {
//     e.preventDefault();

//     const monto = parseFloat(document.getElementById('monto').value);
//     const metodoPago = document.getElementById('metodo-pago').value;
//     const errorElemento = document.getElementById('pago-error');

//     errorElemento.style.display = 'none'; // Ocultar mensaje de error

//     const token = localStorage.getItem('token');
//     try {
//         const response = await fetch(`${BASE_URL}/pagos`, {
//             method: 'POST',
//             headers: {
//                 'Content-Type': 'application/json',
//                 'Authorization': `Bearer ${token}`
//             },
//             body: JSON.stringify({ monto, metodoPago })
//         });

//         if (!response.ok) {
//             throw new Error('Error al realizar el pago.');
//         }

//         // Pago realizado exitosamente
//         alert('Pago realizado con éxito.');
//     } catch (error) {
//         mostrarError(errorElemento, error.message);
//     }
// });
