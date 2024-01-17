const form = document.querySelector('#form');

form.addEventListener('submit', function (e) {
  e.preventDefault();
  getColors();
});

function getColors() {
  const query = form.elements.query.value;
  fetch('/palette', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      query: query,
    }),
  })
    .then((response) => response.json())
    .then((data) => {
      const colors = data.colors;
      const container = document.querySelector('.container');
      createColorBoxes(colors, container);
    })
    .catch((error) => console.error('Error:', error));
}

function createColorBoxes(colors, parent) {
    parent.innerHTML = '';
    for (const color of colors) {
        const div = document.createElement('div');
        div.classList.add('color-box');
        div.style.backgroundColor = color.hex;

        const colorNameSpan = document.createElement('span');
        colorNameSpan.classList.add('color-name');
        colorNameSpan.innerText = color.name;
        div.appendChild(colorNameSpan);

        const colorHexSpan = document.createElement('span');
        colorHexSpan.classList.add('color-hex');
        colorHexSpan.innerText = color.hex;
        div.appendChild(colorHexSpan);

        parent.appendChild(div);
    }
}

// Initialize Default Color Scheme
function initializeDefaultColors() {
    const defaultColors = [
        {"name": "Red", "hex": "#FF0000"},
        {"name": "Orange", "hex": "#FFA500"},
        {"name": "Yellow", "hex": "#FFFF00"},
        {"name": "Green", "hex": "#008000"},
        {"name": "Blue", "hex": "#0000FF"},
        {"name": "Violet", "hex": "#8B00FF"},
        {"name": "Indigo", "hex": "#4B0082"}
    ];
    createColorBoxes(defaultColors, document.querySelector('.container'));
}

// Call the function on page load
document.addEventListener('DOMContentLoaded', function () {
    initializeDefaultColors();
    form.elements.query.value = '';  
});