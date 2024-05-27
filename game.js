// Get the canvas element
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

// Game variables
let unicornX = 50;
let unicornY = canvas.height / 2;
const unicornSize = 50;
const obstacles = [];
let score = 0;

// Create obstacles
function createObstacle() {
  const height = Math.random() * 100 + 50;
  const obstacle = {
    x: canvas.width,
    y: canvas.height - height - 200,
    width: 50,
    height: height
  };
  obstacles.push(obstacle);
}

// Draw game objects
function draw() {
  // Clear the canvas
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  // Draw the unicorn
  ctx.fillStyle = 'purple';
  ctx.beginPath();
  ctx.arc(unicornX, unicornY, unicornSize, 0, 2 * Math.PI);
  ctx.fill();

  // Draw obstacles
  ctx.fillStyle = 'brown';
  obstacles.forEach(obstacle => {
    ctx.fillRect(obstacle.x, obstacle.y, obstacle.width, obstacle.height);
  });

  // Draw score
  ctx.fillStyle = 'black';
  ctx.font = '24px Arial';
  ctx.fillText(`Score: ${score}`, 10, 30);
}

// Move the unicorn
function moveUnicorn(direction) {
  if (direction === 'up' && unicornY > unicornSize) {
    unicornY -= 10;
  } else if (direction === 'down' && unicornY < canvas.height - unicornSize) {
    unicornY += 10;
  }
}

// Update game state
function update() {
  // Move obstacles
  obstacles.forEach(obstacle => {
    obstacle.x -= 5;
  });

  // Remove obstacles that are off-screen
  obstacles.filter(obstacle => obstacle.x < -obstacle.width);

  // Create new obstacles
  if (Math.random() < 0.01) {
    createObstacle();
  }

  // Check for collisions
  obstacles.forEach(obstacle => {
    if (
      unicornX + unicornSize > obstacle.x &&
      unicornX < obstacle.x + obstacle.width &&
      unicornY + unicornSize > obstacle.y &&
      unicornY < obstacle.y + obstacle.height
    ) {
      // Game over
      alert(`Game Over! Your score is ${score}`);
      resetGame();
    }
  });

  // Increase score
  score++;
}

// Reset game state
function resetGame() {
  unicornX = 50;
  unicornY = canvas.height / 2;
  obstacles.length = 0;
  score = 0;
}

// Game loop
function gameLoop() {
  draw();
  update();
  requestAnimationFrame(gameLoop);
}

// Event listeners
document.addEventListener('keydown', event => {
  if (event.code === 'ArrowUp') {
    moveUnicorn('up');
  } else if (event.code === 'ArrowDown') {
    moveUnicorn('down');
  }
});

// Start the game
resetGame();
gameLoop();