const fetch = require("node-fetch");
const Discord = require("discord.js");

const execute = async function (msg, args) {
  const game_id = Math.floor(msg.channel.id / Math.pow(2, 30));
  await fetch(`https://tambola-django.herokuapp.com/result/${game_id}`)
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      console.log(data);
      const report_fields = [];
      for (const x of data.winners) {
        x[0] = x[0][0].toUpperCase() + x[0].slice(1);
        if (x[1] !== 'NONE') {
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
  name: "result",
  description: "Check for results",
  usage: "result",
  execute,
};
