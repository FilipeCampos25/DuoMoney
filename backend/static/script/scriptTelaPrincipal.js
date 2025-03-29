let progress = 0;
let completedExercises = new Set();

function toggleExercises(sectionId) {
    console.log(`Toggling exercises for ${sectionId}`);
    const section = document.getElementById(sectionId);
    if (section) {
        const isVisible = section.classList.contains('active');
        if (isVisible) {
            section.classList.remove('active');
        } else {
            section.classList.add('active');
            section.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
    } else {
        console.error(`Section with ID ${sectionId} not found`);
    }
}

function startExercise(sectionNum, exerciseNum) {
    console.log(`Starting exercise: Section ${sectionNum}, Exercise ${exerciseNum}`);
    const exerciseKey = `s${sectionNum}e${exerciseNum}`;
    if (!completedExercises.has(exerciseKey)) {
        completedExercises.add(exerciseKey);
        updateProgress();
        const exerciseElement = document.querySelector(`#section-${sectionNum} .exercise-circle:nth-child(${exerciseNum})`);
        if (exerciseElement) {
            exerciseElement.classList.add('completed');
        } else {
            console.error(`Exercise element not found for Section ${sectionNum}, Exercise ${exerciseNum}`);
        }
    }
    alert(`Iniciando Seção ${sectionNum} - Exercício ${exerciseNum}`);
}

function updateProgress() {
    const totalExercises = document.querySelectorAll('.exercise-circle').length;
    progress = (completedExercises.size / totalExercises) * 100;
    const progressFill = document.querySelector('.progress-fill');
    if (progressFill) {
        progressFill.style.width = `${progress}%`;
    }
}

function mostrarTela(telaId) {
    console.log(`Showing screen: ${telaId}`);
    const telas = document.querySelectorAll('.tela');
    telas.forEach(tela => {
        tela.classList.remove('ativa');
    });
    const telaSelecionada = document.getElementById(telaId);
    if (telaSelecionada) {
        telaSelecionada.classList.add('ativa');
        // Ajustar a posição de rolagem para considerar o header
        const headerHeight = document.querySelector('.header-container').offsetHeight;
        window.scrollTo({
            top: telaSelecionada.offsetTop - headerHeight,
            behavior: 'smooth'
        });
    } else {
        console.error(`Screen with ID ${telaId} not found`);
    }
}

// Inicialização
document.addEventListener('DOMContentLoaded', () => {
    console.log("Page loaded, initializing...");
    mostrarTela('inicio'); // Mostra a tela inicial
    document.querySelectorAll('.exercises-container').forEach(container => {
        container.classList.remove('active'); // Garante que exercícios comecem escondidos
    });
});