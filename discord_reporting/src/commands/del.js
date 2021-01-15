const fetch = require("node-fetch");
const Discord = require("discord.js");

const execute = async function (msg) {
  const game_id = Math.floor(msg.channel.id / Math.pow(2, 30));
  if (msg.author.id != 202776600645861376) {
    msg.reply("NOPE");
    return;
  }
  await fetch(`https://tambola-django.herokuapp.com/del/${game_id}`, { method: "DELETE" })
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      console.log(data);
    })
    .catch((err) => {
      console.log("fk");
    });
  msg.reply("Successful");
};

module.exports = {
  name: "del",
  description: "Command to clear game data, only usable by superuser",
  usage: "del",
  execute,
};
