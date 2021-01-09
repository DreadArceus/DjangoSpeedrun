const fetch = require("node-fetch");
const Discord = require("discord.js");

const execute = async function (msg, args) {
  await fetch(`http://127.0.0.1:8000/results`)
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      console.log(data);
      const report_fields = [];
      for (const x of Object.entries(data)) {
        x[0] = x[0][0].toUpperCase() + x[0].slice(1);
        if (x[1] === false) {
          x[1] = "Not Won Yet";
        } else {
          x[1] = `<@${x[1]}>`;
        }
        report_fields.push({ name: x[0], value: x[1] });
      }
      const report_embed = new Discord.MessageEmbed()
        .setColor("#0099ff")
        .setTitle("Results (so far)")
        .addFields(report_fields)
        .setFooter("This report is generated at the time of command");
      msg.channel.send(report_embed);
    })
    .catch((err) => {
      console.log("fk");
    });
};

module.exports = {
  name: "finish",
  description: "Check for results and clear the game data",
  usage: "finish",
  execute,
};
