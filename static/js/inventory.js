export async function confirmInventory() {

    const input =
        document.getElementById("inventoryInput").value;

    const button =
        document.getElementById("search-button");

    button.disabled = true;
    button.textContent = "Searching...";

    try {

        const response =
            await fetch("/search", {

                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    text: input
                })

            });

        const data =
            await response.json();

        if (!response.ok) {

            displaySearchError(data);

            return null;
        }

        const notFound =
            data.filter(item => item.found === false);

        notFound.forEach(item => {

            displaySearchError({
                detail: `${item.name}: not found`
            });

        });

        return data;

    } finally {

        button.disabled = false;
        button.textContent = "Search";
    }
}


function displaySearchError(data) {

    let container =
        document.getElementById("toast-container");

    if (!container) {

        container =
            document.createElement("div");

        container.id =
            "toast-container";

        document.body.appendChild(container);
    }

    const error =
        document.createElement("div");

    error.className =
        "error-toast";

    error.textContent =
        data.detail || "An unknown error occurred.";

    container.appendChild(error);

    setTimeout(() => {

        error.remove();

        if (container.children.length === 0) {
            container.remove();
        }

    }, 4000);
}