import Enemy from "./enemy.js";
import movingDirection from "./movingdirection.js";


export default class EnemyController {

    enemyMap = [
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [2, 2, 2, 3, 3, 3, 3, 2, 2, 2],
        [2, 2, 2, 3, 3, 3, 3, 2, 2, 2],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
    ];
    
    enemyRows = [];

    // Enemy Variables
    currentDirection = movingDirection.right;
    xVelocity = 0;
    yVelocity = 0;
    defaultXVelocity = 1;
    defaultYVelocity = 1;
    moveDownTimerDefault = 30;
    moveDownTimer = this.moveDownTimerDefault;
    fireBulletTimerDefault = 100;
    fireBulletTimer = this.fireBulletTimerDefault;

    constructor(canvas, enemyBulletController, playerBulletController) {
        this.canvas = canvas;
        this.enemyBulletController = enemyBulletController;
        this.playerBulletController = playerBulletController;
        this.enemyDeathSound = new Audio ("Sounds/enemy-death.wav");
        this.enemyDeathSound.volume = 0.2;
        this.createEnemies();
    }

    draw(context) {
        this.decrementMoveDownTimer();
        this.updateVelocityAndDirection();
        this.collisionDetection();
        this.drawEnemies(context);
        this.resetMoveDownTimer();
        this.fireBullet();        
    }

    fireBullet() {
        this.fireBulletTimer--;
        if (this.fireBulletTimer <= 0) {
            this.fireBulletTimer = this.fireBulletTimerDefault;
            const allEnemies = this.enemyRows.flat();
            const enemyIndex = Math.floor(Math.random() * allEnemies.length);
            const enemy = allEnemies[enemyIndex];
            this.enemyBulletController.shoot((enemy.x + (enemy.width / 2)), enemy.y, -3);
            console.log(enemyIndex);
        }
    }

    createEnemies() {
        this.enemyMap.forEach((row, rowIndex) => {
            this.enemyRows[rowIndex] = [];
            row.forEach((enemyNumber, enemyIndex) => {
                if (enemyNumber > 0) {
                    this.enemyRows[rowIndex].push(
                        new Enemy(enemyIndex*50, rowIndex*35, enemyNumber)
                    );
                }
            });
        });
    }

    updateVelocityAndDirection() {
        for (const enemyRow of this.enemyRows) {
            if (this.currentDirection == movingDirection.right) {
                this.xVelocity = this.defaultXVelocity;
                this.yVelocity = 0;
                const rightMostEnemy = enemyRow[enemyRow.length - 1];
                if (rightMostEnemy.x + rightMostEnemy.width >= this.canvas.width) {
                    this.currentDirection = movingDirection.downLeft;
                    break;
                }
            }
            else if (this.currentDirection === movingDirection.downLeft) {
                if (this.moveDown(movingDirection.left)) {
                    break;
                }
            }
            else if (this.currentDirection == movingDirection.left) {
                this.xVelocity = -this.defaultXVelocity;
                this.yVelocity = 0;
                const leftMostEnemy = enemyRow[0];
                if (leftMostEnemy.x <= 0) {
                    this.currentDirection = movingDirection.downRight;
                    break;
                }
            }
            else if (this.currentDirection === movingDirection.downRight) {
                if (this.moveDown(movingDirection.right)) {
                    break;
                }
            }
        }
    }

    // This one is for bullets
    collisionDetection () {
        this.enemyRows.forEach(enemyRow => {
            enemyRow.forEach((enemy, enemyIndex) => {
                if (this.playerBulletController.collideWith(enemy)) {
                    this.enemyDeathSound.currentTime = 0
                    this.enemyDeathSound.play();
                    enemyRow.splice(enemyIndex, 1)
                }
            });
        });

        this.enemyRows = this.enemyRows.filter((enemyRow) => enemyRow.length > 0);
    }

    // This one is for ships 
    collideWith (sprite) {
        return this.enemyRows.flat().some(enemy => enemy.collideWith(sprite))
    }

    moveDown (newDirection) {
        this.xVelocity = 0;
        this.yVelocity = this.defaultYVelocity;
        if (this.moveDownTimer <= 0) {
            this.currentDirection = newDirection;
            return true;
        }
        return false;
    }

    decrementMoveDownTimer() {
        if (this.currentDirection === movingDirection.downLeft || 
            this.currentDirection === movingDirection.downRight
        ) {
            this.moveDownTimer--;
        }
    }

    resetMoveDownTimer () {
        if (this.moveDownTimer <= 0) {
            this.moveDownTimer =this.moveDownTimerDefault;
        }
    }

    drawEnemies (context) {
        this.enemyRows.flat().forEach((enemy) => {
            enemy.move(this.xVelocity, this.yVelocity);
            enemy.draw(context);
        });
    }
}
