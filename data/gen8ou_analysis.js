// Script to perform some data analysis on showdown matches and pokemon in general
// Also sorts moves.json, items.json, abilities.json based on usage stats
// Data from ~15000 matches played in November 2021
// https://www.smogon.com/stats/2021-11/chaos/gen8ou-0.json

const data = require("./gen8ou_1121.json");
const fs = require("fs");

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


// Printing number of moves, items, and abilities with # of uses greater than some threshold
let moveThreshold = 1000;
let itemThreshold = 1000;
let abilityThreshold = 100;

for (var i = 0; i < sortedMoves.length; ++i) {
    if (moves[sortedMoves[i]] < moveThreshold) break;
}
console.log(`Number of Moves Used >${moveThreshold} times: ${i}`);

for (var i = 0; i < sortedItems.length; ++i) {
    if (items[sortedItems[i]] < itemThreshold) break;
}
console.log(`Number of Items Used >${itemThreshold} times: ${i}`);

for (var i = 0; i < sortedAbilities.length; ++i) {
    if (abilities[sortedAbilities[i]] < abilityThreshold) break;
}
console.log(`Number of Abilities Used >${abilityThreshold} times: ${i}`);


// Sort moves.json, items.json, abilities.json
const allMoves = require("./moves.json");
const allItems = require("./items.json");
const allAbilities = require("./abilities.json");

for (let move of allMoves)
    if (!sortedMoves.includes(move))
        sortedMoves.push(move)
for (let item of allItems)
    if (!sortedItems.includes(item))
        sortedItems.push(item)
for (let ability of allAbilities)
    if (!sortedAbilities.includes(ability))
        sortedAbilities.push(ability)

fs.writeFileSync("./moves.json", JSON.stringify(sortedMoves), "utf8");
fs.writeFileSync("./items.json", JSON.stringify(sortedItems), "utf8");
fs.writeFileSync("./abilities.json", JSON.stringify(sortedAbilities), "utf8");