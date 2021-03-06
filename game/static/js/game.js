//
// Credit to https://github.com/lostdecade/simple_canvas_game
// For the original game and tutorial
//

// Create the canvas
var canvas = document.createElement("canvas");
var ctx = canvas.getContext("2d");
canvas.width = 512;
canvas.height = 480;
document.body.appendChild(canvas);

// Background image
var bgReady = false;
var bgImage = new Image();
bgImage.onload = function () {
    bgReady = true;
};
bgImage.src = "static/images/background.png";

// Hero image
var heroReady = false;
var heroImage = new Image();
heroImage.onload = function () {
    heroReady = true;
};
heroImage.src = "static/images/hero.png";

// Monster image
var monsterReady = false;
var monsterImage = new Image();
monsterImage.onload = function () {
    monsterReady = true;
};
monsterImage.src = "static/images/monster.png";

// Game objects
var hero = {
    speed: 256 // movement in pixels per second
};
var monster = {
    speed: 256 // movement in pixels per second
};
var monstersCaught = 0;

// Handle keyboard controls
var keysDown = {};

addEventListener("keydown", function (e) {
    keysDown[e.keyCode] = true;
}, false);

addEventListener("keyup", function (e) {
    delete keysDown[e.keyCode];
}, false);

// Reset the game when the player catches a monster
var reset = function () {
    hero.x = canvas.width / 2;
    hero.y = canvas.height / 2;

    // Throw the monster somewhere on the screen randomly
    monster.x = 32 + (Math.random() * (canvas.width - 64));
    monster.y = 32 + (Math.random() * (canvas.height - 64));
};

// Query the backend action API
var monster_action = function(hero_x, hero_y, mon_x, mon_y, caught) {
    // construct an HTTP request
    var xhr = new XMLHttpRequest();
    xhr.open('POST', 'http://localhost:1337/api/action', false);
    xhr.setRequestHeader('Content-Type', 'application/json; charset=UTF-8');
    data = {
        'hero': {
            'x': hero_x,
            'y': hero_y,
        },
        'monster': {
            'x': mon_x,
            'y': mon_y,
        },
        'caught': caught
    };
    // send the collected data as JSON and return the direction
    xhr.send(JSON.stringify(data));
    var jsonResponse = JSON.parse(xhr.responseText);
    return jsonResponse.direction;
}

// Update game objects
var update = function (modifier) {
    // If player has been caught
    if (
        hero.x <= (monster.x + 32)
        && monster.x <= (hero.x + 32)
        && hero.y <= (monster.y + 32)
        && monster.y <= (hero.y + 32)
    ) {
        // Broadcast state and reward to back end
        var direction = monster_action(hero.x, hero.y, monster.x, monster.y, true);
        // Reset
        ++monstersCaught;
        reset();
    }
    // If player yet to be caught
    else {
        // Determine monster action
        var direction = monster_action(hero.x, hero.y, monster.x, monster.y, false);

        // Move Monster
        switch(direction) {
            case 'up':
                monster.y = Math.max(monster.y - monster.speed * modifier, 0);
                break;
            case 'down':
                monster.y = Math.min(monster.y + monster.speed * modifier, canvas.height - 32);
                break;
            case 'left':
                monster.x = Math.max(monster.x - monster.speed * modifier, 0);
                break;
            case 'right':
                monster.x = Math.min(monster.x + monster.speed * modifier, canvas.width - 32);
        }

        // Move Player
        if (38 in keysDown) { // Player holding up
            hero.y = Math.max(hero.y - hero.speed * modifier, 0);
        }
        else if (40 in keysDown) { // Player holding down
            hero.y = Math.min(hero.y + hero.speed * modifier, canvas.height - 32);
        }
        else if (37 in keysDown) { // Player holding left
            hero.x = Math.max(hero.x - hero.speed * modifier, 0);
        }
        else if (39 in keysDown) { // Player holding right
            hero.x = Math.min(hero.x + hero.speed * modifier, canvas.width - 32);
        }
    }
};

// Draw everything
var render = function () {
    if (bgReady) {
        ctx.drawImage(bgImage, 0, 0);
    }

    if (heroReady) {
        ctx.drawImage(heroImage, hero.x, hero.y);
    }

    if (monsterReady) {
        ctx.drawImage(monsterImage, monster.x, monster.y);
    }

    // Score
    ctx.fillStyle = "rgb(250, 250, 250)";
    ctx.font = "24px Helvetica";
    ctx.textAlign = "left";
    ctx.textBaseline = "top";
    ctx.fillText("Times caught: " + monstersCaught, 32, 32);
};

// The main game loop
var main = function () {
    var now = Date.now();
    var delta = now - then;

    update(delta / 1000);
    render();

    then = now;

    // Request to do this again ASAP
    requestAnimationFrame(main);
};

// Cross-browser support for requestAnimationFrame
var w = window;
requestAnimationFrame = w.requestAnimationFrame || w.webkitRequestAnimationFrame || w.msRequestAnimationFrame || w.mozRequestAnimationFrame;

// Let's play this game!
var then = Date.now();
reset();
main();
