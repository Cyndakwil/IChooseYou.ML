const {Teams, TeamValidator} = require('pokemon-showdown');
const Sim = require("pokemon-showdown");
const fs = require("fs");
const spawn = require("child_process").spawn;

// /*
// Get a random team using the Pokemon Showdown API.
// */
// function getTeam() {
// var options = {format: "gen8ou"};
// var team = Teams.generate("gen8randombattle", options);
// return team;
// }

stream = new Sim.BattleStream();

(async () => {
    for await (var output of stream) {
        const pp = spawn("python", ["C:/Users/rshet/Documents/IChooseYou.ML/Python/stream_reader.py", "output", output]);
    }
})();

stream.write(`>start {"formatid":"gen8randombattle"}`);
stream.write(`>player p1 {"name":"Cock"}`);
stream.write(`>player p2 {"name":"Balls"}`);