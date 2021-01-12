const heading = document.getElementById("heading");
heading.textContent = "Wait up";
const cells = document.getElementsByClassName("cell");
const key = prompt("Enter key:");
getTicket = async () => {
  var ticketData = [];
  await fetch(`http://127.0.0.1:8000/ticket/${key}`)
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      ticketData = data.grid;
      heading.textContent = "Your Ticket";
    })
    .catch((err) => {
      console.log("fk");
    });
  for (var i = 0; i < 9; i++) {
    for (var j = 0; j < 3; j++) {
      cells[i + j * 9].textContent =
        ticketData[i][j] === "X" ? "." : ticketData[i][j];
    }
  }
};
getTicket();
for (var i = 0; i < 27; i++) {
  cells[i].addEventListener("click", (e) => {
    const cell = e.toElement;
    if (cell.textContent != ".") {
      if (cell.style.textDecoration === "line-through") {
        cell.style.textDecoration = "";
      } else {
        cell.style.textDecoration = "line-through";
      }
    }
  });
}
document.getElementById("claim-btn").addEventListener("click", () => {
  var ticket_state = "";
  for (var i = 0; i < 27; i++) {
    if (cells[i].style.textDecoration === "line-through") {
      ticket_state += "1";
    } else {
      ticket_state += "0";
    }
  }
  fetch(`http://127.0.0.1:8000/claim/${ticket_state}/${key}`, {method: 'PUT'})
  .then((response) => {
    return response.json();
  })
  .then((data) => {
    console.log("Claim Successful");
  })
  .catch((err) => {
    console.log("fk");
  });
});
