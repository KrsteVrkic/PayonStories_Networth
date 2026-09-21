export async function pricecheck() {

    const button =
        document.getElementById("pricecheck-button");

    button.disabled = true;
    button.textContent = "Pricechecking...";

    try {

        const selectedItems = [];

        const itemDivs =
            document.querySelectorAll(".item");

        itemDivs.forEach(
            (itemDiv) => {

                const itemName =
                    itemDiv.querySelector(".item-name")
                        .textContent;

                const quantity =
                    parseInt(
                        itemName.split("×")[1]
                    );

                if (!itemDiv.dataset.itemId) {
                    return;
                }

                const item = {
                    id: itemDiv.dataset.itemId,
                    name: itemName
                        .split("×")[0]
                        .trim(),
                    quantity: quantity,
                    refine: 0,
                    c0: 0,
                    c1: 0,
                    c2: 0,
                    c3: 0
                };

                const config =
                    itemDiv.querySelector(
                        ".equipment-config"
                    );

                if (config) {

                    const refineSelect =
                        config.querySelector(
                            '[data-config="refine"]'
                        );

                    if (
                        refineSelect &&
                        refineSelect.value !== ""
                    ) {

                        item.refine =
                            parseInt(
                                refineSelect.value,
                                10
                            );

                    }

                    for (let i = 0; i < 4; i++) {

                        const cardSelect =
                            config.querySelector(
                                `[data-config="c${i}"]`
                            );

                        if (
                            cardSelect &&
                            cardSelect.value !== ""
                        ) {

                            item[`c${i}`] =
                                parseInt(
                                    cardSelect.value,
                                    10
                                ) || 0;

                        } else {

                            item[`c${i}`] = 0;

                        }

                    }

                }

                selectedItems.push(item);

            }
        );


        console.log(
            "PRICECHECK REQUEST:",
            selectedItems
        );


        const response =
            await fetch("/pc", {

                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify(
                    selectedItems
                )

            });


        const results =
            await response.json();


        console.log(
            "PRICECHECK RESULTS:",
            results
        );


        displayPricecheckResults(
            results
        );

    } finally {

        button.disabled = false;
        button.textContent = "Pricecheck";

    }

}


function displayPricecheckResults(results) {

    const container =
        document.getElementById(
            "calculationResults"
        );

    container.innerHTML = "";

    const numberFormat =
        new Intl.NumberFormat("nl-NL");


    results.forEach(result => {

        const resultDiv =
            document.createElement("div");

        resultDiv.className =
            "price-result";


        const name =
            document.createElement("div");

        name.className =
            "price-name";

        name.textContent =
            `${result.name} - ${result.id}`;

        resultDiv.appendChild(
            name
        );


        const priceRow =
            document.createElement("div");

        priceRow.className =
            "price-row";


        const average =
            document.createElement("div");

        average.className =
            "price-total";


        if (result.average !== null) {

            average.dataset.basePrice =
                result.average;

            average.textContent =
                `Average sold price: ${
                    numberFormat.format(
                        result.average
                    )
                }`;

        } else {

            average.textContent =
                "Average sold price: No data";

        }


        priceRow.appendChild(
            average
        );


        if (result.average !== null) {

            const copyButton =
                document.createElement("button");

            copyButton.className =
                "copy-price-button";

            copyButton.textContent =
                "⧉";

            copyButton.title =
                "Copy price";

            copyButton.type =
                "button";


            copyButton.addEventListener(
                "click",
                async () => {

                    const slider =
                        document.getElementById(
                            "price-adjustment"
                        );

                    const modifier =
                        Number(slider.value) / 100;

                    const adjustedPrice =
                        Math.round(
                            result.average * modifier
                        );

                    await navigator.clipboard.writeText(
                        String(adjustedPrice)
                    );

                    displayPriceCopied();

                }
            );


            priceRow.appendChild(
                copyButton
            );

        }


        resultDiv.appendChild(
            priceRow
        );

        container.appendChild(
            resultDiv
        );

    });

}


function displayPriceCopied() {

    let container =
        document.getElementById(
            "toast-container"
        );


    if (!container) {

        container =
            document.createElement("div");

        container.id =
            "toast-container";

        document.body.appendChild(
            container
        );

    }


    const toast =
        document.createElement("div");

    toast.className =
        "success-toast";

    toast.textContent =
        "Price Copied";

    container.appendChild(
        toast
    );


    setTimeout(() => {

        toast.remove();

        if (container.children.length === 0) {
            container.remove();
        }

    }, 2000);

}


const priceSlider =
    document.getElementById(
        "price-adjustment"
    );

const priceSliderValue =
    document.getElementById(
        "price-adjustment-value"
    );


priceSlider.addEventListener(
    "input",
    () => {

        const modifier =
            Number(priceSlider.value) / 100;

        priceSliderValue.textContent =
            `${priceSlider.value}%`;


        const numberFormat =
            new Intl.NumberFormat("nl-NL");


        document
            .querySelectorAll(".price-total")
            .forEach(
                priceElement => {

                    const basePrice =
                        Number(
                            priceElement.dataset.basePrice
                        );

                    if (
                        Number.isNaN(basePrice)
                    ) {
                        return;
                    }


                    const adjustedPrice =
                        Math.round(
                            basePrice * modifier
                        );


                    priceElement.textContent =
                        `Average sold price: ${
                            numberFormat.format(
                                adjustedPrice
                            )
                        }`;

                }
            );

    }
);