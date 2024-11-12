// secretaria.js

// Base URL de la API (ajusta según el entorno de producción si es necesario)
const BASE_URL = 'http://127.0.0.1:8000/secretaria'; // Cambia '127.0.0.1' según la IP o el dominio en producción

// Cargar reservas
document.addEventListener('DOMContentLoaded', async () => {
    const token = localStorage.getItem('token');
    try {
        const response = await fetch(`${BASE_URL}/reservas`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        const reservas = await response.json();
        const tableBody = document.querySelector('#reservas-table tbody');
        tableBody.innerHTML = reservas.map(reserva => `
            <tr>
                <td>${reserva.cliente}</td>
                <td>${reserva.servicio}</td>
                <td>${new Date(reserva.fecha).toLocaleDateString()}</td>
                <td>${reserva.profesional}</td>
                <td><button onclick="editarReserva(${reserva.id})">Editar</button></td>
            </tr>
        `).join('');
    } catch (error) {
        console.error('Error al cargar las reservas:', error);
    }
});

// Cargar clientes
document.addEventListener('DOMContentLoaded', async () => {
    const token = localStorage.getItem('token');
    try {
        const response = await fetch(`${BASE_URL}/clientes`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        const clientes = await response.json();
        const clientesList = document.querySelector('#clientes-list');
        clientesList.innerHTML = clientes.map(cliente => `
            <li>${cliente.nombre} - ${cliente.email}</li>
        `).join('');
    } catch (error) {
        console.error('Error al cargar los clientes:', error);
    }
});

// Descargar informe de ganancias
document.getElementById('informe-ganancias').addEventListener('click', async () => {
    const token = localStorage.getItem('token');
    try {
        const response = await fetch(`${BASE_URL}/informes/ganancias`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });

        if (!response.ok) {
            throw new Error('Error al descargar el informe.');
        }

        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'informe_ganancias.pdf';
        document.body.appendChild(a);
        a.click();
        a.remove();
    } catch (error) {
        console.error('Error al descargar el informe de ganancias:', error);
    }
});

// Descargar informe de servicios
document.getElementById('informe-servicios').addEventListener('click', async () => {
    const token = localStorage.getItem('token');
    try {
        const response = await fetch(`${BASE_URL}/informes/servicios`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });

        if (!response.ok) {
            throw new Error('Error al descargar el informe.');
        }

        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'informe_servicios.pdf';
        document.body.appendChild(a);
        a.click();
        a.remove();
    } catch (error) {
        console.error('Error al descargar el informe de servicios:', error);
    }
});
