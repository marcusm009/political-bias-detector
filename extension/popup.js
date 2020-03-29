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
      client.get(query, function(response) {
          document.getElementById("output").innerHTML = response + " " + query;

          document.getElementById("loader").style.display = "none";
          document.getElementById("output").style.display = "block";
      });

    });



});
