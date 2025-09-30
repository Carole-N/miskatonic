// Fonction pour générer une couleur hex aléatoire
function getRandomColor() {
    const letters = '0123456789ABCDEF';
    let color = '#';
    for (let i = 0; i < 6; i++) {
        color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
}

// Sélection de tous les liens dans les <li>
const links = document.querySelectorAll('h1');

links.forEach(link => {
    // Couleur initiale aléatoire
    link.style.color = getRandomColor();

    // Changement automatique tout les x temps
    setInterval(() => {
        link.style.color = getRandomColor();
    }, 500); 
});
