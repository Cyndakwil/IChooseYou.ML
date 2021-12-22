// Script to perform some data analysis on showdown matches and pokemon in general
// Data from ~15000 matches played in November 2021
// https://www.smogon.com/stats/2021-11/chaos/gen8ou-0.json

const {Dex} = require("pokemon-showdown");
const data = require("./gen8ou.json");

// 1. Compile list of moves and number of uses
console.log("MOVES\n---------")
let moves = {}
for (let pokemon of Object.values(data.data)) {
    for (let move of Object.entries(pokemon.Moves)) {
        if (moves[move[0]]) {
            moves[move[0]] += move[1];
        } else {
            moves[move[0]] = move[1];
        }
    }
}

let sortedMoves = Object.keys(moves).sort((a, b) => {return moves[b] - moves[a];});
let ctr = 1;
for (let move of sortedMoves) {
    console.log(ctr++ + " " + move + " " + moves[move]);
}
console.log();


// 2. Compile list of items and number of uses
console.log("ITEMS\n---------")
let items = {}
for (let pokemon of Object.values(data.data)) {
    for (let item of Object.entries(pokemon.Items)) {
        if (items[item[0]]) {
            items[item[0]] += item[1];
        } else {
            items[item[0]] = item[1];
        }
    }
}

let sortedItems = Object.keys(items).sort((a, b) => {return items[b] - items[a];});
ctr = 1;
for (let item of sortedItems) {
    console.log(ctr++ + " " + item + " " + items[item]);
}
console.log();


// 3. Compile list of abilities and number of uses
console.log("ABILITIES\n---------")
let abilities = {}
for (let pokemon of Object.values(data.data)) {
    for (let ability of Object.entries(pokemon.Abilities)) {
        if (abilities[ability[0]]) {
            abilities[ability[0]] += ability[1];
        } else {
            abilities[ability[0]] = ability[1];
        }
    }
}

let sortedAbilities = Object.keys(abilities).sort((a, b) => {return abilities[b] - abilities[a];});
ctr = 1;
for (let ability of sortedAbilities) {
    console.log(ctr++ + " " + ability + " " + abilities[ability]);
}
console.log();