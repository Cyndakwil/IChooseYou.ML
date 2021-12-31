const {State} = require('pokemon-showdown');
const Sim = require("pokemon-showdown");
const fs = require("fs");
const spawn = require("child_process").spawn;
const { randomInt } = require('crypto');
const https = require('https');
const smogon_api = 'https://smogon-usage-stats.herokuapp.com/2019/12/gen8randombattle/1630/';

const dex = JSON.parse(fs.readFileSync('./bin/pokedex.json'));
const genericInfo = JSON.parse(fs.readFileSync('./data/randomdata.json'));

stream = new Sim.BattleStream();

// Get live state of game
(async () => {
    for await (var output of stream) {
        let msg = output.split("|");

        if (msg.includes("turn")) {
            let data = stream.battle.toJSON();

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
                other.pokemon.forEach(mon => {
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
            fs.writeFileSync("./bin/request.json", JSON.stringify(data, null, "\t"));
        }
    }
})();

// TESTING
stream.write(`>start {"formatid":"gen8randombattle"}`);
stream.write(`>player p1 {"name":"Cock"}`);
stream.write(`>player p2 {"name":"Balls"}`);
stream.write(`>p1 default`);
stream.write(`>p2 move 1 max`);