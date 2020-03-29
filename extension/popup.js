// JS function that can perform get requestions
var HttpClient = function() {
  this.get = function(aUrl, aCallback) {
    var anHttpRequest = new XMLHttpRequest();
    anHttpRequest.onreadystatechange = function() {
      if (anHttpRequest.readyState == 4 && anHttpRequest.status == 200)
      aCallback(anHttpRequest.responseText);
    }

    anHttpRequest.open( "GET", aUrl, true );
    anHttpRequest.send( null );
  }
}
// Sends get request to URL
chrome.tabs.executeScript( {
  code: "window.getSelection().toString();"
}, function(selection) {

  // chrome.extension.getBackgroundPage().console.log('foo');
  // console.log('foo');

  var configURL = chrome.extension.getURL("config.json");
  var donkeyURL = chrome.extension.getURL("images/donkey.png");
  var elephantURL = chrome.extension.getURL("images/elephant.png");

  fetch(configURL)
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      console.log(data);

      var url = data.ip + ":" + data.port + "/?query=";
      var str = selection[0];
      str = str.replace(/\s+/g, '+');
      var query = url.concat(str);

      var client = new HttpClient();
      client.get(query, function(res) {

        document.getElementById("output").innerHTML = createResponseHTML(res, donkeyURL, elephantURL);

        document.getElementById("loader").style.display = "none";
        document.getElementById("output").style.display = "inline-block";
      });

    });

});

function createResponseHTML(res, donkeyURL, elephantURL) {
  var response = JSON.parse(res);
  var url = "";

  if(response.prediction == "Democrat") {
    url = donkeyURL;
  }
  else {
    url = elephantURL;
  }

  html = `<div style="content:url(${url});max-width:100%;height:auto;"></div>`
  html += "<h1>";
  html += "Prediction: ";
  html += response.prediction;
  html += "</h1>";
  html += "<h4>";
  html += "Total prediciton time: ";
  html += response.pred_time;
  html += "</h4>";
  return html;

}
