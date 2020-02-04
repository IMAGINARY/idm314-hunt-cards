/* eslint-disable no-console,no-param-reassign */
const fs = require('fs').promises;
const path = require('path');
const GSheeter = require('@imaginary-maths/gsheeter');
const config = require('./config.json');
const credentials = require('./client_secret.json');

const destinationPath = '../data';


GSheeter.get(config.spreadsheetID, config.worksheetID, { credentials })
  .then((items) => {
    const translations = {};
    config.languages.forEach((lang) => {
      translations[lang] = {};
    });
    items
      .filter(item => !(config.ignoredIDs.includes(item.id)))
      .forEach((item) => {
        Object.entries(translations).forEach(([lang, translation]) => {
          if (translation[item.id] === undefined) {
            translation[item.id] = {};
          }
          const object = translation[item.id];
          if (item[lang].trim().length > 0) {
            object[item.field] = item[lang].trim();
          } else {
            object[item.field] = item.en.trim();
          }
        });
      });

    return translations;
  })
  .then((translations) => {
    const filePromises = [];
    Object.entries(translations).forEach(([lang, translation]) => {
      const filename = path.resolve(path.join(destinationPath, `${lang}.json`));
      const jsonData = JSON.stringify({
        cards: translation,
      }, null, 2);

      filePromises.push(
        fs.writeFile(filename, jsonData).then(() => {
          console.log(`Data written to ${filename}`);
        })
      );
    });
    return Promise.all(filePromises);
  })
  .then(() => {
    console.log('Done.');
  });
