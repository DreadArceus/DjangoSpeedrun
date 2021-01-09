const fetch = require("node-fetch");
const Discord = require("discord.js");

const execute = async function (msg, args) {
  await fetch(`http://127.0.0.1:8000/count`)
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      console.log(data);
      msg.channel.send(
        `${
          data.Started ? "Game in progress" : "Game has not begun"
        }\nCurrently registered: ${data.Registered}`
      );
    })
    .catch((err) => {
      console.log("fk");
    });
};

module.exports = {
  name: "start",
  description: "Start a new tambola game",
  usage: "start",
  execute,
};
