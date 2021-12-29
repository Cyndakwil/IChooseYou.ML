const fs = require('fs');

// Import data
const target = JSON.parse(fs.readFileSync("./randomdata.json"));
const dex = JSON.parse(fs.readFileSync("./../bin/pokedex.json"));
const data = JSON.parse(fs.readFileSync("./gen8randombattle.json"));

const abilitiesData = JSON.parse(fs.readFileSync("./../bin/abilities_unencoded.json"));
const itemsData = JSON.parse(fs.readFileSync("./../bin/items_unencoded.json"));

// Find common name of pokemon
Object.keys(target).forEach(id => {
    if (dex[id] == undefined) return;
    let commonName = dex[id].species;
    if (data[commonName] == undefined) commonName = dex[id].name;
    // Import items and abilities
    target[id].abilities = data[commonName].abilities;
    target[id].items = data[commonName].items;

    // Convert ability names to ids
    target[id].abilities.forEach(ability => {
        for (let i = 0; i < Object.keys(abilitiesData).length; i++) {
            if (abilitiesData[Object.keys(abilitiesData)[i]].name == ability) {
                target[id].abilities[target[id].abilities.indexOf(ability)] = Object.keys(abilitiesData)[i];
                break;
            }
        }
    });

    console.log(id);
});

fs.truncateSync("./randomdata.json", 0);
fs.writeFileSync("./randomdata.json", JSON.stringify(target));
// console.log(JSON.stringify(target));