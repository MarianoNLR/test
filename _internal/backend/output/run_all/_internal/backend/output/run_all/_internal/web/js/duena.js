// duena.js

// Base URL de la API (ajusta según el entorno de producción si es necesario)
const BASE_URL = 'http://127.0.0.1:8000/duena'; // Cambia '127.0.0.1' según la IP o el dominio en producción

// Cargar reservas al cargar la página
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

// Crear nuevo empleado
document.getElementById('crear-empleado-form').addEventListener('submit', async (e) => {
    e.preventDefault();

    const nombreEmpleado = document.getElementById('nombre-empleado').value;
    const emailEmpleado = document.getElementById('email-empleado').value;
    const rolEmpleado = document.getElementById('rol-empleado').value;

    const token = localStorage.getItem('token');
    try {
        const response = await fetch(`${BASE_URL}/empleados`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({ nombre: nombreEmpleado, email: emailEmpleado, rol: rolEmpleado })
        });

        if (!response.ok) {
            throw new Error('Error al crear el empleado.');
        }

        // Recargar la lista de empleados
        window.location.reload();
    } catch (error) {
        console.error('Error al crear el empleado:', error);
    }
});

// Cargar empleados
document.addEventListener('DOMContentLoaded', async () => {
    const token = localStorage.getItem('token');
    try {
        const response = await fetch(`${BASE_URL}/empleados`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        const empleados = await response.json();
        const empleadosList = document.querySelector('#empleados-list');
        empleadosList.innerHTML = empleados.map(empleado => `
            <li>${empleado.nombre} - ${empleado.rol} 
                <button onclick="borrarEmpleado(${empleado.id})">Borrar</button>
            </li>
        `).join('');
    } catch (error) {
        console.error('Error al cargar los empleados:', error);
    }
});

// Borrar empleado
async function borrarEmpleado(empleadoId) {
    const token = localStorage.getItem('token');
    try {
        const response = await fetch(`${BASE_URL}/empleados/${empleadoId}`, {
            method: 'DELETE',
            headers: { 'Authorization': `Bearer ${token}` }
        });

        if (!response.ok) {
            throw new Error('Error al borrar el empleado.');
        }

        // Recargar la lista de empleados
        window.location.reload();
    } catch (error) {
        console.error('Error al borrar el empleado:', error);
    }
}

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
