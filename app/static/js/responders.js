/*
 * Author: Sakthi Santhosh
 * Created on: 14/02/2023
 */
const filterByElement = document.getElementById("filter-by");
const querySelectorElement = document.getElementById("query-selector");
const queryInputElement = document.getElementById("query-input");
const querySets = {
    area: null,
    preferred_language: null
};

function createOption(value, text) {
    const option = document.createElement("option");

    option.value = value;
    option.text = text;

    return option;
}

async function setQuerySetAndDisplay(querySetKey) {
    if (querySets[querySetKey] === null)
        querySets[querySetKey] = await fetchQuerySet(querySetKey);

    querySelectorElement.style.display = "block";
    queryInputElement.style.display = "none";
    queryInputElement.disabled = true;

    removeOptions();

    querySets[querySetKey].forEach((datum) => {
        querySelectorElement.appendChild(createOption(datum, datum));
    })
}

function removeOptions() {
    while (querySelectorElement.options.length > 0)
        querySelectorElement.remove(0);
}

async function fetchQuerySet(endpoint) {
    const response = await fetch(`/responders/api?query_set=${ endpoint }`);
    const json = await response.json();

    return json.data;
}

filterByElement.onchange = function() {
    const selectedOption = filterByElement.options[filterByElement.selectedIndex].value;

    switch (selectedOption) {
        case "activation_status":
        case "is_working":
            querySelectorElement.style.display = "block";
            queryInputElement.style.display = "none";
            queryInputElement.disabled = true;
            querySelectorElement.disabled = false;

            removeOptions();
            querySelectorElement.appendChild(createOption('0', "Unverified"));
            querySelectorElement.appendChild(createOption('1', "Suspended"));
            querySelectorElement.appendChild(createOption('2', "Email ID Verified"));
            querySelectorElement.appendChild(createOption('3', "Phone Verified"));
            querySelectorElement.appendChild(createOption('4', "Verified"));
            break;
        case "area":
            setQuerySetAndDisplay("area");
            break;
        case "preferred_language":
            setQuerySetAndDisplay("preferred_language");
            break;
        case "first_name":
        case "last_name":
        case "email_id":
        case "phone":
            querySelectorElement.style.display = "none";
            queryInputElement.style.display = "block";
            querySelectorElement.disabled = true;
            queryInputElement.disabled = false;
    }
};
