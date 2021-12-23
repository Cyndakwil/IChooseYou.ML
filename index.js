const {State} = require('pokemon-showdown');
const Sim = require("pokemon-showdown");
const fs = require("fs");
const spawn = require("child_process").spawn;
const { randomInt } = require('crypto');

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
        // const pp = spawn("python", ["C:/Users/rshet/Documents/IChooseYou.ML/Python/stream_reader.py", "output", output]);
        fs.writeFileSync("./bin/request.json", JSON.stringify(stream.battle.toJSON(), null, "\t"));
    }
})();

stream.write(`>start {"formatid":"gen8randombattle"}`);
stream.write(`>player p1 {"name":"Cock"}`);
stream.write(`>player p2 {"name":"Balls"}`);
for (let i=0; i < 30; i++) {
    stream.write(`>p1 move ` + randomInt(1, 5));
    stream.write(`>p2 move ` + randomInt(1, 5));
}


