/**
 * Aggregates move, abilities, and item data from randomdata.json
 * into their own respective files. For encoding purposes.
 */

const data = require("./randomdata.json");
const fs = require("fs");

moves = []
items = []
abilities = []

for (let species of Object.values(data)) {
    for (move of species.randomBattleMoves) {
        if (!moves.includes(move)) moves.push(move);
    }

    for (item of species.items || []) {
        if (!items.includes(item)) items.push(item);
    }

    for (ability of species.abilities || []) {
        if (!abilities.includes(ability)) abilities.push(ability);
    }
}

fs.writeFileSync("moves.json", JSON.stringify(moves), "utf-8");
fs.writeFileSync("items.json", JSON.stringify(items), "utf-8");
fs.writeFileSync("abilities.json", JSON.stringify(abilities), "utf-8");

console.log(`No. of Moves: ${moves.length}`);
console.log(`No. of Items: ${items.length}`);
console.log(`No. of Abilities: ${abilities.length}`);
console.log("Written to moves.json, items.json, abilities.json")