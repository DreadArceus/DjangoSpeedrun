const fetch = require("node-fetch");
const Discord = require("discord.js");

const execute = async function (msg, args) {
  var calls = [];
  await fetch(`http://127.0.0.1:8000/calls`)
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      calls = data;
      console.log(calls);
    })
    .catch((err) => {
      console.log("fk");
    });
  if (calls.length === 90) {
    msg.channel.send("Game Ended");
    return;
  }
  const bag = [];
  for (var i = 1; i <= 90; i++) {
    if (calls.findIndex((x) => x === `${i}`) === -1) {
      bag.push(i);
    }
  }
  var num = bag[Math.floor(Math.random() * bag.length)];
  await fetch(`http://127.0.0.1:8000/numcall/${num}`)
    .then((response) => {
      comm = response.json();
      console.log(`Returning this: ${JSON.stringify(comm)}`);
      return comm;
    })
    .then((data) => {
      console.log(data);
    })
    .catch((err) => {
      console.log("fk");
    });
  msg.channel.send(`Called Number: ${num}`);
};

module.exports = {
  name: "call",
  description: "Call next number",
  usage: "call",
  execute,
};
