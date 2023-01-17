// Imports
import EnemyController from "./enemycontrolller.js";
import Player from "./player.js";
import bulletController from "./bulletcontroller.js";


const canvas = document.getElementById("game");
const context = canvas.getContext("2d");

// Game Variables
// Screens
canvas.width = 600;
canvas.height = 600;
const background = new Image();
background.src = "Images/space.png";

// Bullet Controllers
const enemyBulletController = new bulletController(canvas, 4, "white", false);
const playerBulletController = new bulletController(canvas, 10, "red", true);

// Enemies  
const enemyControlller = new EnemyController(canvas, enemyBulletController, playerBulletController);

// Player
const player = new Player(canvas, 3, playerBulletController);

// Game
let isGameOver = false;
let didWin = false;

function game() {
    checkGameOver();
    context.drawImage(background, 0, 0, canvas.width, canvas.height);
    displayGameOver();
    if (!isGameOver) {
        enemyControlller.draw(context);
        player.draw(context);
        playerBulletController.draw(context);
        enemyBulletController.draw(context);
        console.log(isGameOver);
    }
}

function checkGameOver () {
    if (isGameOver) {
        return;
    }

    if (enemyBulletController.collideWith(player)) {
        isGameOver = true;
    }

    if (enemyControlller.collideWith(player)) {
        isGameOver = true;
    }

    if (enemyControlller.enemyRows.length === 0) {
        didWin = true;
        isGameOver = true;
    }
}

function displayGameOver() {
    if (isGameOver) {
        let text = didWin ? "You Win!" : "Game Over!";
        let textOffset = didWin ? 3.5 : 5;

        context.fillStyle = "white";
        context.font = "70px Cambria";
        context.fillText(text, canvas.width / textOffset, canvas.height / 2);
    }
}

setInterval(game, 1000/60);