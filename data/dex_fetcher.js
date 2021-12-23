// Fetches array of moves, item, ability names from Dex
const {Dex} = require("pokemon-showdown");
const fs = require("fs");

// Data sorted in order of uses
data = {
    "Moves": [],
    "Items": [],
    "Abilities": []
};
categories = ["Moves", "Items", "Abilities"];
for (let category of categories) {
    for (let value of Object.keys(Dex.data[category])) {
        data[category].push(value);
    }
}
console.log(data);

// Write data
let moves = JSON.stringify(data.Moves);
let items = JSON.stringify(data.Items);
let abilities = JSON.stringify(data.Abilities);

fs.writeFileSync("./moves.json", moves, "utf8");
fs.writeFileSync("./items.json", items, "utf8");
fs.writeFileSync("./abilities.json", abilities, "utf8");
