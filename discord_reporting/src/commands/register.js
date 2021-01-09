const fetch = require("node-fetch");
const Discord = require("discord.js");

const execute = async function (msg, args) {
  var key = "";
  for(var i = 0; i < 13; i++){
    key += String.fromCharCode(Math.floor(Math.random() * 26 + 65))
  }
    await fetch(`http://127.0.0.1:8000/new/${key}/${msg.author.id}`)
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
  msg.author.send(`Your secret key is ${key}, enter this in https://www.someshit.com/ to enter the game`);
};

module.exports = {
  name: "register",
  description: "Register for the next game, a secret key is sent to your DMs",
  usage: "register",
  execute,
};
