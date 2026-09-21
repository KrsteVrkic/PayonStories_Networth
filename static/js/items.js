let cards = null;


async function loadCards() {

    if (cards) {
        return cards;
    }

    const response =
        await fetch("/cards");

    cards =
        await response.json();

    return cards;
}


export async function displayResults(searchResults) {

    const container =
        document.getElementById("results");

    container.innerHTML = "";

    const hasEquipment =
        searchResults.some(
            item => item.equipment === true
        );

    let cardData = null;

    if (hasEquipment) {
        cardData = await loadCards();
    }

    searchResults.forEach(
        (item, itemIndex) => {

            const itemDiv =
                document.createElement("div");

            itemDiv.className = "item";

            const name =
                document.createElement("div");

            name.className = "item-name";

            name.textContent =
                `${item.name} × ${item.quantity}`;

            itemDiv.appendChild(name);


            if (item.equipment === false) {

                itemDiv.dataset.itemId =
                    item.item.id;

            } else {

                createEquipmentRow(
                    itemDiv,
                    item.variants,
                    cardData
                );

            }


            container.appendChild(itemDiv);

        }
    );
}


function createEquipmentRow(
    itemDiv,
    variants,
    cards,
    selectedItemId = null,
    selectedRefine = null,
    selectedCards = []
) {

    const oldRow =
        itemDiv.querySelector(
            ".equipment-config"
        );

    if (oldRow) {
        oldRow.remove();
    }


    const row =
        document.createElement("div");

    row.className =
        "equipment-config";


    /*
     * SLOTS
     */

    const slotsSelect =
        document.createElement("select");

    slotsSelect.className =
        "equipment-select";

    slotsSelect.dataset.config =
        "slots";


    const slotsPlaceholder =
        document.createElement("option");

    slotsPlaceholder.value = "";

    slotsPlaceholder.textContent =
        "Slots";

    slotsPlaceholder.disabled = true;

    slotsPlaceholder.selected =
        !selectedItemId;

    slotsSelect.appendChild(
        slotsPlaceholder
    );


    variants.forEach(
        variant => {

            const option =
                document.createElement("option");

            option.value =
                variant.id;

            option.textContent =
                variant.slots === 1
                    ? "1 slot"
                    : `${variant.slots} slots`;

            slotsSelect.appendChild(
                option
            );

        }
    );


    if (selectedItemId) {

        slotsSelect.value =
            String(selectedItemId);

        itemDiv.dataset.itemId =
            String(selectedItemId);

    }


    row.appendChild(
        slotsSelect
    );


    /*
     * REFINE
     */

    const refineSelect =
        document.createElement("select");

    refineSelect.className =
        "equipment-select";

    refineSelect.dataset.config =
        "refine";

    refineSelect.disabled =
        !selectedItemId;


    const refinePlaceholder =
        document.createElement("option");

    refinePlaceholder.value =
        "";

    refinePlaceholder.textContent =
        "Refine";

    refinePlaceholder.disabled = true;

    refinePlaceholder.selected =
        selectedRefine === null;

    refineSelect.appendChild(
        refinePlaceholder
    );


    for (let i = 0; i <= 10; i++) {

        const option =
            document.createElement("option");

        option.value =
            i;

        option.textContent =
            `+${i}`;

        refineSelect.appendChild(
            option
        );

    }


    if (selectedRefine !== null) {

        refineSelect.value =
            String(selectedRefine);

    }


    row.appendChild(
        refineSelect
    );


    /*
     * CARD SELECTS
     */

    if (selectedItemId) {

        const selectedVariant =
            variants.find(
                variant =>
                    String(variant.id) ===
                    String(selectedItemId)
            );


        const cardEntries =
            Object.entries(cards);


        for (
            let slot = 0;
            slot < selectedVariant.slots;
            slot++
        ) {

            const cardSelect =
                document.createElement("select");

            cardSelect.className =
                "equipment-select";

            cardSelect.dataset.config =
                `c${slot}`;


            const placeholder =
                document.createElement("option");

            placeholder.value =
                "";

            placeholder.textContent =
                `Card ${slot + 1}`;

            placeholder.disabled = true;

            placeholder.selected =
                selectedCards[slot] === undefined;

            cardSelect.appendChild(
                placeholder
            );


            const emptyOption =
                document.createElement("option");

            emptyOption.value =
                "0";

            emptyOption.textContent =
                "Empty";

            cardSelect.appendChild(
                emptyOption
            );


            cardEntries.forEach(
                ([cardId, card]) => {

                    const option =
                        document.createElement("option");

                    option.value =
                        cardId;

                    option.textContent =
                        card.name;

                    cardSelect.appendChild(
                        option
                    );

                }
            );


            if (
                selectedCards[slot] !== undefined
            ) {

                cardSelect.value =
                    String(
                        selectedCards[slot]
                    );

            }


            row.appendChild(
                cardSelect
            );

        }

    }


    /*
     * SLOT CHANGE
     */

    slotsSelect.addEventListener(
        "change",
        () => {

            itemDiv.dataset.itemId =
                slotsSelect.value;

            createEquipmentRow(
                itemDiv,
                variants,
                cards,
                slotsSelect.value,
                null,
                []
            );

        }
    );


    itemDiv.appendChild(
        row
    );
}