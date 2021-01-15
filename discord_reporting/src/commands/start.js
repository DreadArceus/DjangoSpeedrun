const fetch = require("node-fetch");
const Discord = require("discord.js");

const execute = async function (msg, args) {
  const game_id = Math.floor(msg.channel.id / Math.pow(2, 30));
  await fetch(`https://tambola-django.herokuapp.com/init/${game_id}`)
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      console.log(data);
      msg.channel.send(
        `${
          data.Started ? "Game in progress" : "Game has not begun"
        }\nCurrently registered: ${data.Registered} (Use $register)`
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
