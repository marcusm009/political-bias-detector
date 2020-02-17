
chrome.browserAction.onClicked.addListener(buttonClicked);

function buttonClicked() {
    fetch('https://twitter.com?par=0').then(r => r.text()).then(result => {
        console.log(result);
    })
}



