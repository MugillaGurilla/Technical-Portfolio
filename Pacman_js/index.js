// Game Framework stuff
const canvas = document.querySelector('canvas');
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;
const c = canvas.getContext('2d');
const scoreElement = document.getElementById('score-element');


// Classes
class Boundary {
    static width = 40;
    static height = 40;

    constructor({position, image}) {
        this.position = position;
        this.width = 40;
        this.height = 40;
        this.image = image;
    }

    draw() {
        c.drawImage(this.image, this.position.x, this.position.y)
    }
}

class Player {
    constructor({position, velocity}) {
        this.position = position;
        this.velocity = velocity;
        this.radius = 15;
        this.radians = 0.75;
        this.openRate = 0.04
        this.rotation = 0;
    }

    draw() {
        c.save();
        c.translate(this.position.x, this.position.y)
        c.rotate(this.rotation);
        c.translate(-this.position.x, -this.position.y);
        c.beginPath();
        c.arc(this.position.x, this.position.y, this.radius, this.radians, Math.PI * 2 - this.radians);
        c.lineTo(this.position.x, this.position.y)
        c.fillStyle = "yellow";
        c.fill();
        c.closePath();
        c.restore();
    }

    update() {
        this.draw();
        this.position.x += this.velocity.x;
        this.position.y += this.velocity.y;

        if (this.radians < 0 || this.radians > 0.75) {
            this.openRate = -this.openRate;
        }
        this.radians += this.openRate;
    }

    detectGapThenMove(planeOfMovement, xVelocity, yVelocity,) {
        for (let i = 0; i < boundaries.length; i++) {
            const boundary = boundaries[i];
            if (circleCollidingWithRectangle({circle: {...player, velocity: {x: xVelocity, y: yVelocity}}, 
                                                rectangle: boundary})) {
                if (planeOfMovement == 'y') { 
                    player.velocity.y = 0;
                    break;
                }
                else if (planeOfMovement == 'x') { 
                    player.velocity.x = 0;
                    break;
                }
            }
            else {
                if (planeOfMovement == 'y') { 
                    player.velocity.y = yVelocity;
                }
                else if (planeOfMovement == 'x') { 
                    player.velocity.x = xVelocity;
                }
            }
        }
    }

    move(boundary) {
        if (keys.w.pressed && lastKey === 'w') {
            this.detectGapThenMove('y', 0, -5)
        }
        else if (keys.a.pressed && lastKey === 'a') {
            this.detectGapThenMove('x', -5, 0)
        }
        else if (keys.s.pressed && lastKey === 's') {
            this.detectGapThenMove('y', 0, 5)
        }
        else if (keys.d.pressed && lastKey === 'd') {
            this.detectGapThenMove('x', 5, 0)
        }
    }

    collideWithBoundary(boundary) {
        if (circleCollidingWithRectangle({circle: player, rectangle: boundary})) {
                player.velocity.x = 0;
                player.velocity.y = 0;
        }
    }

    discernRotation() {
        if (player.velocity.x > 0) player.rotation = 0                          // Going Right
        else if (player.velocity.x < 0) player.rotation = Math.PI               // Going Left
        else if (player.velocity.y > 0) player.rotation = Math.PI / 2           // Going Up
        else if (player.velocity.y < 0) player.rotation = Math.PI * 1.5         // Going Down
    }
}

class Pellet {
    constructor({position}) {
        this.position = position;
        this.radius = 3;
    }

    draw() {
        c.beginPath();
        c.arc(this.position.x, this.position.y, this.radius, 0, Math.PI * 2);
        c.fillStyle = "white";
        c.fill();
        c.closePath();
    }

    pelletEaten(pellet, player, pelletIndex) {
        if (Math.hypot(
            pellet.position.x - player.position.x, 
            pellet.position.y - player.position.y)
            < pellet.radius + player.radius
            ) {
                pellets.splice(pelletIndex, 1)
                score += 10;
                scoreElement.innerHTML = score;
            }
    }
}

class PowerUp {
    constructor({position}) {
        this.position = position;
        this.radius = 8;
    }

    draw() {
        c.beginPath();
        c.arc(this.position.x, this.position.y, this.radius, 0, Math.PI * 2);
        c.fillStyle = "white";
        c.fill();
        c.closePath();
    }

    getPowerUp(powerUp, player, powerUpIndex) {
        if (Math.hypot(
            powerUp.position.x - player.position.x, 
            powerUp.position.y - player.position.y)
            < powerUp.radius + player.radius
            ) {
                powerUps.splice(powerUpIndex, 1)

                //make ghosts scared
                ghosts.forEach((ghost) => {
                    ghost.scared = true;
                    console.log(ghost.scared);
                    setTimeout(() => {
                        ghost.scared = false;
                        console.log(ghost.scared);
                    }, 5000)
                })
            }
    }
}

class Ghost {
    static speed = 2;
    constructor({position, velocity, colour = "red"}) {
        this.position = position;
        this.velocity = velocity;
        this.radius = 15;
        this.colour = colour;
        this.prevCollisions = [];
        this.speed = 2;
        this.scared = false;

    }

    draw() {
        c.beginPath();
        c.arc(this.position.x, this.position.y, this.radius, 0, Math.PI * 2);
        c.fillStyle = this.scared ? 'blue' : this.colour;
        c.fill();
        c.closePath();
    }

    update() {
        this.draw();
        this.position.x += this.velocity.x;
        this.position.y += this.velocity.y
    }

    detectBoundaryCollision(boundary, ghost) {
        if (!collisions.includes('right') && circleCollidingWithRectangle({circle: {...ghost, velocity: {x: ghost.speed, y: 0}}, 
                                            rectangle: boundary})) {
            collisions.push('right');
        }
        if (!collisions.includes('up') && circleCollidingWithRectangle({circle: {...ghost, velocity: {x: 0, y: -ghost.speed}}, 
            rectangle: boundary})) {
            collisions.push('up');
        }
        if (!collisions.includes('left') && circleCollidingWithRectangle({circle: {...ghost, velocity: {x: -ghost.speed, y: 0}}, 
                                            rectangle: boundary})) {
            collisions.push('left');
        }
        if (!collisions.includes('down') && circleCollidingWithRectangle({circle: {...ghost, velocity: {x: 0, y: ghost.speed}}, 
                                            rectangle: boundary})) {
            collisions.push('down');
        }
    }

    move(ghost) {
        if (collisions.length > ghost.prevCollisions.length) {
            ghost.prevCollisions = collisions;
        }
        if (JSON.stringify(collisions) !== JSON.stringify(ghost.prevCollisions)) {
            if (ghost.velocity.x > 0) ghost.prevCollisions.push('right'); 
            else if (ghost.velocity.x < 0) ghost.prevCollisions.push('left'); 
            else if (ghost.velocity.y < 0) ghost.prevCollisions.push('up'); 
            else if (ghost.velocity.y > 0) ghost.prevCollisions.push('down'); 

            const pathways = ghost.prevCollisions.filter((collision) => {
                return !collisions.includes(collision)
            })
            const direction = pathways[Math.floor(Math.random() * pathways.length)]

            switch (direction) {
                case 'down':
                    ghost.velocity.y = ghost.speed;
                    ghost.velocity.x = 0;
                    break
                case 'up':
                    ghost.velocity.y = -ghost.speed;
                    ghost.velocity.x = 0;
                    break
                case 'left':
                    ghost.velocity.y = 0;
                    ghost.velocity.x = -ghost.speed;
                    break
                case 'right':
                    ghost.velocity.y = 0;
                    ghost.velocity.x = ghost.speed;
                    break
            }
            ghost.prevCollisions = []
        }
        
    }

    ghostCatchesPlayer(ghost, ghostIndex) {
        if (Math.hypot(
            ghost.position.x - player.position.x, 
            ghost.position.y - player.position.y)
            < ghost.radius + player.radius 
            ) {
            if (ghost.scared) {
                ghosts.splice(ghostIndex, 1);
            }
            else {
                cancelAnimationFrame(animationId);
                console.log('you lose');
            }
        }
    }
}

// Non Class-specific functions
function circleCollidingWithRectangle({circle, rectangle}) {
    const padding = Boundary.width / 2 - circle.radius - 1;
    return (
        circle.position.y - circle.radius + circle.velocity.y <= rectangle.position.y + rectangle.height + padding &&
        circle.position.x + circle.radius + circle.velocity.x >= rectangle.position.x - padding &&
        circle.position.y + circle.radius + circle.velocity.y >= rectangle.position.y - padding &&
        circle.position.x - circle.radius + circle.velocity.x <= rectangle.position.x + rectangle.width + padding
    )
}

function gameWon() {
    if (pellets.length === 0) {
        console.log('Game Won!')
        cancelAnimationFrame(animationId);
    }
}

function createImage(src) {
    const image = new Image();
    image.src = src;
    return image;
}

// Sprite Variables
const boundaries = [];
const pellets = [];
const powerUps = [];
const ghosts = [
    new Ghost ({
        position: {
            x: Boundary.width * 6.5,
            y: Boundary.height * 1.5
        },
        velocity: {
            x: Ghost.speed, 
            y: 0
        }, 
    }),
    new Ghost ({
        position: {
            x: Boundary.width * 6.5,
            y: Boundary.height * 3.5
        },
        velocity: {
            x: Ghost.speed, 
            y: 0
        }, 
        colour: 'pink'
    }),
    new Ghost ({
        position: {
            x: Boundary.width * 4.5,
            y: Boundary.height * 4.5
        },
        velocity: {
            x: Ghost.speed, 
            y: 0
        }, 
        colour: 'purple'
    })
];
const player = new Player({
    position: {
        x: Boundary.width * 1.5,
        y: Boundary.height * 1.5
    },
    velocity: {
        x: 0,
        y: 0
    }
});

// Game Map Stuff
const map = [
    ["1", "-", "-", "-", "-", "-", "-", "-", "-", "-", "2"],
    ["|", ".", ".", ".", ".", ".", ".", ".", ".", ".", "|"],
    ["|", ".", "b", ".", "[", "7", "]", ".", "b", ".", "|"],
    ["|", ".", ".", ".", ".", "_", ".", ".", ".", ".", "|"],
    ["|", ".", "[", "]", ".", ".", ".", "[", "]", ".", "|"],
    ["|", ".", ".", ".", ".", "^", ".", ".", ".", ".", "|"],
    ["|", ".", "b", ".", "[", "+", "]", ".", "b", ".", "|"],
    ["|", ".", ".", ".", ".", "_", ".", ".", ".", ".", "|"],
    ["|", ".", "[", "]", ".", ".", ".", "[", "]", ".", "|"],
    ["|", ".", ".", ".", ".", "^", ".", ".", ".", ".", "|"],
    ["|", ".", "b", ".", "[", "5", "]", ".", "b", ".", "|"],
    ["|", ".", ".", ".", ".", ".", ".", ".", ".", "p", "|"],
    ["3", "-", "-", "-", "-", "-", "-", "-", "-", "-", "4"],
];

map.forEach((row, i) => {
    row.forEach((symbol, j) => {
        switch (symbol) {
            case "-":
                boundaries.push(
                    new Boundary({
                        position: {
                            x: Boundary.width * j,
                            y: Boundary.height * i,
                        },
                        image: createImage("./img/pipeHorizontal.png"),
                    })
                );
                break;
            case "|":
                boundaries.push(
                    new Boundary({
                        position: {
                            x: Boundary.width * j,
                            y: Boundary.height * i,
                        },
                        image: createImage("./img/pipeVertical.png"),
                    })
                );
                break;
            case "1":
                boundaries.push(
                    new Boundary({
                        position: {
                            x: Boundary.width * j,
                            y: Boundary.height * i,
                        },
                        image: createImage("./img/pipeCorner1.png"),
                    })
                );
                break;
            case "2":
                boundaries.push(
                    new Boundary({
                        position: {
                            x: Boundary.width * j,
                            y: Boundary.height * i,
                        },
                        image: createImage("./img/pipeCorner2.png"),
                    })
                );
                break;
            case "3":
                boundaries.push(
                    new Boundary({
                        position: {
                        x: Boundary.width * j,
                        y: Boundary.height * i,
                        },
                        image: createImage("./img/pipeCorner3.png"),
                    })
                );
                break;
            case "4":
                boundaries.push(
                    new Boundary({
                        position: {
                        x: Boundary.width * j,
                        y: Boundary.height * i,
                        },
                        image: createImage("./img/pipeCorner4.png"),
                    })
                );
                break;
            case "b":
                boundaries.push(
                    new Boundary({
                        position: {
                        x: Boundary.width * j,
                        y: Boundary.height * i,
                        },
                        image: createImage("./img/block.png"),
                    })
                );
                break;
            case "[":
                boundaries.push(
                    new Boundary({
                        position: {
                        x: j * Boundary.width,
                        y: i * Boundary.height,
                        },
                        image: createImage("./img/capLeft.png"),
                    })
                );
                break;
            case "]":
                boundaries.push(
                    new Boundary({
                        position: {
                        x: j * Boundary.width,
                        y: i * Boundary.height,
                        },
                        image: createImage("./img/capRight.png"),
                    })
                );
                break;
            case "_":
                boundaries.push(
                    new Boundary({
                        position: {
                        x: j * Boundary.width,
                        y: i * Boundary.height,
                        },
                        image: createImage("./img/capBottom.png"),
                    })
                );
                break;
            case "^":
                boundaries.push(
                    new Boundary({
                        position: {
                        x: j * Boundary.width,
                        y: i * Boundary.height,
                        },
                        image: createImage("./img/capTop.png"),
                    })
                );
                break;
            case "+":
                boundaries.push(
                    new Boundary({
                        position: {
                        x: j * Boundary.width,
                        y: i * Boundary.height,
                        },
                        image: createImage("./img/pipeCross.png"),
                    })
                );
                break;
            case "5":
                boundaries.push(
                    new Boundary({
                        position: {
                        x: j * Boundary.width,
                        y: i * Boundary.height,
                        },
                        color: "blue",
                        image: createImage("./img/pipeConnectorTop.png"),
                    })
                );
                break;
            case "6":
                boundaries.push(
                    new Boundary({
                        position: {
                        x: j * Boundary.width,
                        y: i * Boundary.height,
                        },
                        color: "blue",
                        image: createImage("./img/pipeConnectorRight.png"),
                    })
                );
                break;
            case "7":
                boundaries.push(
                    new Boundary({
                        position: {
                        x: j * Boundary.width,
                        y: i * Boundary.height,
                        },
                        color: "blue",
                        image: createImage("./img/pipeConnectorBottom.png"),
                    })
                );
                break;
            case "8":
                boundaries.push(
                    new Boundary({
                        position: {
                        x: j * Boundary.width,
                        y: i * Boundary.height,
                        },
                        image: createImage("./img/pipeConnectorLeft.png"),
                    })
                );
                break;
            case ".":
                pellets.push(
                    new Pellet({
                        position: {
                        x: j * Boundary.width + Boundary.width / 2,
                        y: i * Boundary.height + Boundary.height / 2,
                        }
                    })
                );
                break;
            case "p":
                powerUps.push(
                    new PowerUp({
                        position: {
                        x: j * Boundary.width + Boundary.width / 2,
                        y: i * Boundary.height + Boundary.height / 2,
                        }
                    })
                );
                break;
            }
        });
});


// Game Implementation Stuff
const keys = {
    w: {
        pressed: false
    }, 
    a: {
        pressed: false
    },
    s: {
        pressed: false
    },
    d: {
        pressed: false
    }
}
let lastKey = "";
let score = 0;
let collisions = [];
let animationId = 0;

// Game Loop
function animate() {
    animationId = requestAnimationFrame(animate);
    c.clearRect(0, 0, canvas.width, canvas.height);

    // Creating Boundaries 
    boundaries.forEach(boundary => {
        boundary.draw();
        player.collideWithBoundary(boundary);
    });

    // Creating PowerUps 
    for (let powerUpIndex = powerUps.length - 1; powerUpIndex >= 0; powerUpIndex--) {
        const powerUp = powerUps[powerUpIndex];
        powerUp.draw();
        powerUp.getPowerUp(powerUp, player, powerUpIndex);
    }
    
    // Creating Pellets 
    for (let pelletIndex = pellets.length - 1; pelletIndex >= 0; pelletIndex--) {
        const pellet = pellets[pelletIndex];
        pellet.draw();
        pellet.pelletEaten(pellet, player, pelletIndex);
    }

    // Creating Ghosts 

    for (let ghostIndex = ghosts.length - 1; ghostIndex >= 0; ghostIndex--) {
        const ghost = ghosts[ghostIndex];
        ghost.ghostCatchesPlayer(ghost, ghostIndex);
    }

    // Creating and Moving Player
    player.update();
    player.move();
    player.discernRotation();

    // Ghost AI
    ghosts.forEach((ghost) => {
        ghost.update();
        collisions = [];
        boundaries.forEach(boundary => {
            ghost.detectBoundaryCollision(boundary, ghost);
        });
        ghost.move(ghost);
    });

    // Win Condition
    gameWon();

}
animate();

// Listeners: w is up, s is down, a is left and d is to go right.
window.addEventListener('keydown', ({key}) => {
    switch (key) {
        case 'w':
            keys.w.pressed = true;
            lastKey = 'w';
            break;
        case 's':
            keys.s.pressed = true;
            lastKey = 's';
            break;
        case 'a':
            keys.a.pressed = true;
            lastKey = 'a';
            break;
        case 'd':
            keys.d.pressed = true;
            lastKey = 'd';
            break;
    }
})

window.addEventListener('keyup', ({key}) => {
    switch (key) {
        case 'w':
            keys.w.pressed = false;
            break;
        case 's':
            keys.s.pressed = false;
            break;
        case 'a':
            keys.a.pressed = false;
            break;
        case 'd':
            keys.d.pressed = false;
            break;
    }
})