chrome.runtime.onInstalled.addListener(function() {
  chrome.storage.sync.set({color: '#3aa757'}, function() {
    console.log("The color is green.");
    var configURL = chrome.extension.getURL("config.json");
    fetch(configURL)
      .then((response) => {
        return response.json();
      })
      .then((data) => {
        console.log(data);
      });
  });
});
