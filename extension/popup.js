// JS function that can perform get requests
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

  var configURL = chrome.extension.getURL("config.json");
  var donkeyURL = chrome.extension.getURL("images/donkey.png");
  var elephantURL = chrome.extension.getURL("images/elephant.png");
  var unsureURL = chrome.extension.getURL("images/unsure.png");

  fetch(configURL)
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      console.log(data);

      var url = data.ip + ":" + data.port + "/?query=";
      var str = encodeURIComponent(parseTweet(selection[0]));
      var query = url.concat(str);

      var client = new HttpClient();
      client.get(query, function(res) {

        document.getElementById("output").innerHTML = createResponseHTML(res, donkeyURL, elephantURL, unsureURL);

        document.getElementById("loading").style.display = "none";
        document.getElementById("output").style.display = "inline-block";
      });

    });

});

function createResponseHTML(res, donkeyURL, elephantURL, unsureURL) {
  var response = JSON.parse(res);
  var pred = getActualPrediction(response.prediction, response.confidence);

  var url = "";
  if(pred == "Democrat" || pred == "Possibly Democrat") {
    url = donkeyURL;
  }
  else if(pred == "Republican" || pred == "Possibly Republican") {
    url = elephantURL;
  }
  else {
    url = unsureURL;
  }

  html = `<div style="content:url(${url});max-width:100%;height:auto;"></div>`
  html += "<h1>";
  html += pred;
  html += "</h1>";
  html += "<p>";
  html += "Top Choice: <b>";
  html += response.prediction;
  html += "</b></p>";
  html += "<p>";
  html += "Confidence: <b>";
  html += parseFloat(response.confidence)*100;
  html += "%</b></p>";
  html += "<p>";
  html += "Total prediciton time: <b>";
  html += response.pred_time;
  html += "</b></p>";
  return html;
}

function getActualPrediction(pred, confidence) {
  if(confidence >= 0.8) {
    return pred;
  }
  if(confidence >= 0.6) {
    return "Possibly " + pred;
  }
  return "Unsure";
}

function parseTweet(str) {
  // Replace newlines
  str = str.replace(/\n/g, ' <nl> ').replace(/\r/g, ' <nl> ');
  // Replace hashtags
  str = str.replace(/#\w+\b/g, ' <ht> ');
  // Replace mentions
  str = str.replace(/@\w+\b/g, ' <@> ');
  return str
}
