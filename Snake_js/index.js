
// Variables
// Screens
const canvas = document.getElementById('game');
const context = canvas.getContext('2d');
const startScreen = document.querySelector('#start-screen');
const gameScreen = document.querySelector('#game-screen');

// Game Info
let speed  = 7;
let tileCount = 20;
let tileSize = canvas.width / tileCount - 2


// Apple info
let appleX = 5;
let appleY = 5;
// const gulp = new Audio("gulp.mp3");

// Sprite Info
let headX = 10;
let headY = 10;
let xVelocity = 0;
let yVelocity = 0;
class SnakePart {
    constructor(x, y) {
        this.x = x;
        this.y = y;
    }
}
let snakeParts = [];
let tailLength = 2;

//Sprite controls
document.body.addEventListener('keydown', keyDown);

// UI
let score = 0;


document.querySelector('#btn-new-game').addEventListener('click', () => {
    startGame();
})

function drawGame() {
    changeSnakePosition();
    let result = isGameOver();
    if (result) {
        return;
        
    }
    
    clearScreen();
    
    checkAppleCollsion();
    drawApple();
    drawSnake();
    
    drawScore();
    increaseSpeed();
    
    setTimeout(drawGame, 1000 / speed)
}

function startGame() {
    startScreen.classList.remove('active');
    gameScreen.classList.add('active');
}

function returnStartScreen() {
    gameScreen.classList.remove('active');
    startScreen.classList.add('active');
    resetGameValues();
    drawGame();
}

function resetGameValues() {
    headX = 10;
    headY = 10;
    xVelocity = 0;
    yVelocity = 0;
    tailLength = 2;
    score = 0;
    speed = 7;
    snakeParts = [];
}

function clearScreen() {
    context.fillStyle = "black";
    context.fillRect(0,0,canvas.width,canvas.height);
}

function isGameOver() {
    let gameOver = false;

    if (yVelocity === 0 && xVelocity === 0) {
        return false;
    }

    // Wall Checks
    if (headX < 0 || headX >= tileCount || headY < 0 || headY >= tileCount) {
        gameOver = true
    }

    // Snake Checks
    for (let i = 0; i < snakeParts.length; i++) {
        let part = snakeParts[i];
        if (part.x === headX && part.y === headY) {
            gameOver = true;
            break;
        }
    }

    if (gameOver) {
        context.fillStyle = "white";
        context.font = "50px Verdana";
        context.fillText("Game Over!", canvas.width / 6.5, canvas.height / 2);
        setTimeout(returnStartScreen, 2000);
    }    
    return gameOver;
}

function drawScore() {
    context.fillStyle = "white";
    context.font = "10px Verdana"
    context.fillText("Score: " + score, canvas.width - 50, 10)
}

function drawSnake() { 
    // tail
    context.fillStyle = "green";
    for (let i = 0; i < snakeParts.length; i++) {
        let part = snakeParts[i];
        context.fillRect(part.x * tileCount, part.y * tileCount, tileSize, tileSize)
    }
    snakeParts.push(new SnakePart(headX, headY));
    if (snakeParts.length > tailLength) {
        snakeParts.shift();
    }

    // head
    context.fillStyle = "orange";
    context.fillRect(headX * tileCount, headY * tileCount, tileSize, tileSize)
}

function changeSnakePosition() {
    headX += xVelocity;
    headY += yVelocity;
}

function drawApple() {
    context.fillStyle = "red";
    context.fillRect(appleX * tileCount, appleY * tileCount, tileSize, tileSize)
}

function checkAppleCollsion() {
    if (appleX == headX && appleY == headY) {
        appleX = Math.floor(Math.random() * tileCount);
        appleY = Math.floor(Math.random() * tileCount);
        tailLength++;
        score++;
        // gulp.play();
    }
}

function increaseSpeed() {
    if (score > 2) {
        speed = 11;
    }
    if (score > 6) {
        speed = 15;
    }
}

function keyDown(event) {
    // Going Up
    if (event.keyCode == 38) {
        if (yVelocity == 1) return;
        yVelocity = -1;
        xVelocity = 0;
    }
    // Going Down
    if (event.keyCode == 40) {
        if (yVelocity == -1) return;
        yVelocity = 1;
        xVelocity = 0;
    }
    // Going Left
    if (event.keyCode == 37) {
        if (xVelocity == 1) return;
        yVelocity = 0;
        xVelocity = -1;
    }
    // Going Right
    if (event.keyCode == 39) {
        if (xVelocity == -1) return;
        yVelocity = 0;
        xVelocity = 1;
    }
}

drawGame();