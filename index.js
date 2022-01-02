const {State} = require('pokemon-showdown');
const Sim = require("pokemon-showdown");
const fs = require("fs");
const spawn = require("child_process").spawn;
const { randomInt } = require('crypto');
const https = require('https');
const smogon_api = 'https://smogon-usage-stats.herokuapp.com/2019/12/gen8randombattle/1630/';

// Game instance used to run concurrent games for training
class Game {
    constructor(id1, id2) {
        this.stream = new Sim.BattleStream();
        this.process = spawn('python', [''])

        // UID of both models
        this.p1 = id1;
        this.p2 = id2;
    }

    move(p) {
        // call model here
    
        // s.write(`>p` + p + ` move 1`); // model choice
    }
}



const dex = JSON.parse(fs.readFileSync('./data/pokedex.json'));
const genericInfo = JSON.parse(fs.readFileSync('./data/randomdata.json'));

game = new Game();

// Get live state of game
(async () => {
    for await (var output of game.stream) {
        // console.log(output)

        let msg = output.split("|");

        if (msg.includes("turn")) {
            let data = game.stream.battle.toJSON();

            // Adding data for each side
            data.sides.forEach(side => {         
                side.volatiles = [];
                side.opponent = {};
                let other = side == data.sides[0] ? data.sides[1] : data.sides[0];

                side.pokemon.forEach(mon => {
                    // Get HP% for each pokemon
                    mon.percenthp = 1.0 * mon.hp / mon.maxhp // ensure float division

                    // Create list of volatiles for each side
                    for (let i=0; i < Object.keys(mon.volatiles).length; i++) {
                        side.volatiles.push(mon.volatiles[Object.keys(mon.volatiles)[i]]);
                    }
                });

                // TODO only include known pokemon
                // Set opposing pokemon data
                side.opponent.volatiles = [];
                side.opponent.sideConditions = other.sideConditions;
                other.pokemon.forEach(mon => {
                    for (let i=0; i < Object.keys(mon.volatiles).length; i++) {
                        side.opponent.volatiles.push(mon.volatiles[Object.keys(mon.volatiles)[i]]);
                    }
                    side.opponent[mon.speciesState.id] = {};
                    side.opponent[mon.speciesState.id].name = mon.speciesState.id;
                    side.opponent[mon.speciesState.id].types = mon.types;
                    side.opponent[mon.speciesState.id].percenthp = 1.0 * mon.hp / mon.maxhp;
                    side.opponent[mon.speciesState.id].baseStats = dex[mon.speciesState.id].baseStats;
                    side.opponent[mon.speciesState.id].moves = genericInfo[mon.speciesState.id].randomBattleMoves;
                    side.opponent[mon.speciesState.id].items = genericInfo[mon.speciesState.id].items;
                    side.opponent[mon.speciesState.id].abilities = genericInfo[mon.speciesState.id].abilities;
                });
            });

            // Write data to request file for model use
            fs.writeFileSync("./data/samplerequest.json", JSON.stringify(data, null, "\t"));

            // CALL MOVES HERE
        }
    }
})();

// TESTING
game.stream.write(`>start {"formatid":"gen8randombattle"}`);
game.stream.write(`>player p1 {"name":"Cock"}`);
game.stream.write(`>player p2 {"name":"Balls"}`);
game.stream.write(`>p1 default`);
game.stream.write(`>p2 move 1 max`);