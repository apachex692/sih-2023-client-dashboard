/*
 * Author: Sakthi Santhosh
 * Created on: 25/03/2024
 */
let socketHandle = io("/rtdatastream");

socketHandle.on("data_egress", data => {
    var element = document.getElementById("live-feed");

    element.style.display = "block";

    element.appendChild(
        document.createTextNode(`${JSON.stringify(new Date())} => ${JSON.stringify(data)}`)
    );
    element.appendChild(
        document.createElement("br")
    );
});

document.getElementById("live-data-btn").addEventListener("click", function () {
    var element = document.getElementById("live-feed");

    element.innerHTML = "";
    element.style.display = "block";

    element.appendChild(
        document.createTextNode(`${JSON.stringify(new Date())} => Waiting for data...`)
    );
    element.appendChild(
        document.createElement("br")
    );
});
