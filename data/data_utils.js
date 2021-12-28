const fs = require('fs');

// Import data
const target = JSON.parse(fs.readFileSync("./randomdata.json"));
const dex = JSON.parse(fs.readFileSync("./../bin/pokedex.json"));
const data = JSON.parse(fs.readFileSync("./gen8randombattle.json"));

// Find common name of pokemon
Object.keys(target).forEach(id => {
    if (dex[id] == undefined) return;
    let commonName = dex[id].species;
    if (data[commonName] == undefined) commonName = dex[id].name;
    // Import items and abilities
    target[id].abilities = data[commonName].abilities;
    target[id].items = data[commonName].items;
});

fs.truncateSync("./randomdata.json", 0);
fs.writeFileSync("./randomdata.json", JSON.stringify(target));
console.log(JSON.stringify(target));