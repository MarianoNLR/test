// masajista.js

// Base URL de la API (ajusta según el entorno de producción si es necesario)
const BASE_URL = 'http://127.0.0.1:8000/masajista'; // Cambia '127.0.0.1' según la IP o el dominio en producción

// Cargar citas totales
document.addEventListener('DOMContentLoaded', async () => {
    const token = localStorage.getItem('token');
    try {
        const response = await fetch(`${BASE_URL}/citas-totales`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        const citas = await response.json();
        const tableBody = document.querySelector('#citas-totales-table tbody');
        tableBody.innerHTML = citas.map(cita => `
            <tr>
                <td>${cita.cliente}</td>
                <td>${cita.servicio}</td>
                <td>${new Date(cita.fecha).toLocaleDateString()}</td>
                <td>${cita.estado}</td>
            </tr>
        `).join('');
    } catch (error) {
        console.error('Error al cargar las citas totales:', error);
    }
});

// Cargar citas del día
document.addEventListener('DOMContentLoaded', async () => {
    const token = localStorage.getItem('token');
    try {
        const response = await fetch(`${BASE_URL}/citas-dia`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        const citas = await response.json();
        const tableBody = document.querySelector('#citas-dia-table tbody');
        tableBody.innerHTML = citas.map(cita => `
            <tr>
                <td>${cita.cliente}</td>
                <td>${cita.servicio}</td>
                <td>${new Date(cita.fecha).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</td>
            </tr>
        `).join('');
    } catch (error) {
        console.error('Error al cargar las citas del día:', error);
    }
});

// Cargar historial de servicios
document.addEventListener('DOMContentLoaded', async () => {
    const token = localStorage.getItem('token');
    try {
        const response = await fetch(`${BASE_URL}/historial`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        const historial = await response.json();
        const historialList = document.querySelector('#historial-list');
        historialList.innerHTML = historial.map(servicio => `
            <li>${servicio.servicio} - ${new Date(servicio.fecha).toLocaleDateString()}</li>
        `).join('');
    } catch (error) {
        console.error('Error al cargar el historial de servicios:', error);
    }
});
