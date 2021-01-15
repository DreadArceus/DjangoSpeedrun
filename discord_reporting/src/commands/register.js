const fetch = require("node-fetch");
const Discord = require("discord.js");

const execute = async function (msg, args) {
  const game_id = Math.floor(msg.channel.id / Math.pow(2, 30));
  var key = "";
  for(var i = 0; i < 13; i++){
    key += String.fromCharCode(Math.floor(Math.random() * 26 + 65))
  }
    await fetch(`https://tambola-django.herokuapp.com/ticket/${game_id}/${key}/${msg.author.id}`, {method: 'POST'})
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      console.log(data);
      msg.reply("You have been successfully registered, check DMs for key");
    })
    .catch((err) => {
      console.log("fk");
    });
  msg.author.send(`Open https://dreadarceus.github.io/Tambola_FrontEnd?game_id=${game_id}&key=${key} to enter the game`);
};

module.exports = {
  name: "register",
  description: "Register for the next game, a secret key is sent to your DMs",
  usage: "register",
  execute,
};
