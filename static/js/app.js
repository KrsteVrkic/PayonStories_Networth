import { confirmInventory } from "./inventory.js";
import { displayResults } from "./items.js";
import { pricecheck } from "./pricecheck.js";


window.confirmInventory = async function () {

    const results =
        await confirmInventory();

    if (results === null) {
        return;
    }

    displayResults(results);
};


window.pricecheck = pricecheck;