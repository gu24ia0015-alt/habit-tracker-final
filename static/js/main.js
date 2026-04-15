// Alternar Dark Mode
document.getElementById('dark-mode-toggle').addEventListener('click', () => {
    document.body.classList.toggle('dark');
});

// Función para obtener hábitos del servidor
async function loadHabits() {
    const response = await fetch('/habits');
    const habits = await response.json();
    
    const list = document.getElementById('habit-list');
    list.innerHTML = '';

    habits.forEach(habit => {
        const card = document.createElement('div');
        card.className = 'habit-card';
        card.innerHTML = `
            <h3>${habit.name}</h3>
            <p>Estado: ${habit.status}</p>
            <button onclick="updateStatus(${habit.id})">Completar</button>
        `;
        list.appendChild(card);
    });
    updateChart(habits);
}

// Función para enviar nuevo hábito al backend
async function addHabit() {
    const name = document.getElementById('habit-input').value;
    if(!name) return;

    await fetch('/habits', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ name: name })
    });
    
    document.getElementById('habit-input').value = '';
    loadHabits();
}

// Inicializar gráfica
function updateChart(habits) {
    const ctx = document.getElementById('progressChart').getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: habits.map(h => h.name),
            datasets: [{
                label: 'Progreso de Hábitos',
                data: habits.map(h => h.status === 'completed' ? 100 : 0),
                backgroundColor: '#4CAF50'
            }]
        }
    });
}

window.onload = loadHabits;