export default class Player {
    rightPressed = false;
    leftPressed = false;
    shootPressed = false;
    
    constructor (canvas, velocity, bulletController) {
        this.canvas = canvas;
        this.velocity = velocity;
        this.bulletController = bulletController;
        this.x = this.canvas.width / 2;
        this.y = this.canvas.height - 75;
        this.width = 50;
        this.height = 48;
        this.image = new Image();
        this.image.src = "Images/player.png";

        // Controls
        document.addEventListener('keydown', this.keydown);
        document.addEventListener('keyup', this.keyup);
    }

    draw(context) {
        if (this.shootPressed) {
            this.bulletController.shoot(this.x + this.width / 2, this.y, 4, 10)
        }
        this.move();
        this.collideWithWalls()
        context.drawImage(this.image, this.x, this.y, this.width, this.height);
    }

    move() {
        if (this.rightPressed) {
            this.x += this.velocity;
        }
        if (this.leftPressed) {
            this.x += -this.velocity;
        }
    }

    collideWithWalls() {
        if (this.x < 0) {
            this.x = 0;
        } else if (this.x > this.canvas.width - this.width) {
            this.x = this.canvas.width - this.width;
        }
    }

    keydown = (event) => {
        if (event.code == 'ArrowRight') {
            this.rightPressed = true;
        }
        if (event.code == 'ArrowLeft') {
            this.leftPressed = true;
        }
        if (event.code == 'Space') {
            this.shootPressed = true;
        }
    };
    keyup = (event) => {
        if (event.code == 'ArrowRight') {
            this.rightPressed = false;
        }
        if (event.code == 'ArrowLeft') {
            this.leftPressed = false;
        }
        if (event.code == 'Space') {
            this.shootPressed = false;
        }
    };
    
}