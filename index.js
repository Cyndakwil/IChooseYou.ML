const { State } = require('pokemon-showdown');
const Sim = require("pokemon-showdown");
const fs = require("fs");
const spawn = require("child_process").spawn;
const https = require('https');
var http_server = https.createServer( app ).listen( 3000 );
var io = require( "socket.io" )( http_server );
const smogon_api = 'https://smogon-usage-stats.herokuapp.com/2019/12/gen8randombattle/1630/';

const num_games = 32;

// Game instance used to run concurrent games for training
class Game {
    constructor(id) {
        this.stream = new Sim.BattleStream();

        // UID of both models
        this.id = id;

        // Get live state of game
        (async () => {
            for await (var output of this.stream) {
                // console.log(output)

                let msg = output.split("|");

                if (msg.includes("turn")) {
                    let data = this.stream.battle.toJSON();

                    // Adding data for each side
                    data.sides.forEach(side => {
                        side.volatiles = [];
                        side.opponent = {};
                        let other = side == data.sides[0] ? data.sides[1] : data.sides[0];

                        side.pokemon.forEach(mon => {
                            // Get HP% for each pokemon
                            mon.percenthp = 1.0 * mon.hp / mon.maxhp // ensure float division

                            // Create list of volatiles for each side
                            for (let i = 0; i < Object.keys(mon.volatiles).length; i++) {
                                side.volatiles.push(mon.volatiles[Object.keys(mon.volatiles)[i]]);
                            }
                        });

                        // TODO only include known pokemon
                        // Set opposing pokemon data
                        side.opponent.volatiles = [];
                        side.opponent.sideConditions = other.sideConditions;
                        side.opponent.dynamaxUsed = other.dynamaxUsed;
                        side.opponent.pokemon = {};
                        other.pokemon.forEach(mon => {
                            for (let i = 0; i < Object.keys(mon.volatiles).length; i++) {
                                side.opponent.volatiles.push(mon.volatiles[Object.keys(mon.volatiles)[i]]);
                            }
                            side.opponent.pokemon[mon.speciesState.id] = {};
                            side.opponent.pokemon[mon.speciesState.id].name = mon.speciesState.id;
                            side.opponent.pokemon[mon.speciesState.id].isActive = mon.isActive;
                            side.opponent.pokemon[mon.speciesState.id].types = mon.types;
                            side.opponent.pokemon[mon.speciesState.id].percenthp = 1.0 * mon.hp / mon.maxhp;
                            side.opponent.pokemon[mon.speciesState.id].baseStats = dex[mon.speciesState.id].baseStats;
                            side.opponent.pokemon[mon.speciesState.id].abilities = mon.boosts;
                            side.opponent.pokemon[mon.speciesState.id].moves = genericInfo[mon.speciesState.id].randomBattleMoves;
                            side.opponent.pokemon[mon.speciesState.id].items = genericInfo[mon.speciesState.id].items;
                            side.opponent.pokemon[mon.speciesState.id].abilities = genericInfo[mon.speciesState.id].abilities;
                        });
                    });

                    // Write data to request file for model use
                    fs.writeFileSync("./bin/request_" + this.id + ".json", JSON.stringify(data, null, "\t"));

                }
            }
        })();

        // START GAME
        this.stream.write(`>start {"formatid":"gen8randombattle"}`);
        this.stream.write(`>player p1 {"name":"Cock"}`);
        this.stream.write(`>player p2 {"name":"Balls"}`);
    }

    move(p) {
        // call model here

        // s.write(`>p` + p + ` move 1`); // model choice
    }
}

//instantiate python process
// let py = spawn("python", ["training.py"]);

//socket.io stuff
// io.on( "connection", function( socket ) {
//     socket.on( 'python-message', function( fromPython ) {
//         socket.broadcast.emit( 'message', fromPython );
//     });
// })

const dex = JSON.parse(fs.readFileSync('./data/pokedex.json'));
const genericInfo = JSON.parse(fs.readFileSync('./data/randomdata.json'));

let games = []; // list of running games

for (let i = 0; i < num_games; i++) { // create games
    games.push(new Game(i));
}