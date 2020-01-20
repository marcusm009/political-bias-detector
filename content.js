
// Can parse through HTML and replace specified words
var elements = document.getElementsByTagName('*');

for (var i = 0; i < elements.length; i++){

    var element = elements[i];
    for (var j = 0; j < element.childNodes.length; j++){

        // Checks if it is text
        var node = element.childNodes[j];
        if (node.nodeType === 3){ 
            var text = node.nodeValue;
            var replacedText = text.replace(/Donald/gi , 'Aaron Mares');

            if (replacedText !== text) {
                element.replaceChild(document.createTextNode(replacedText), node);
            }

        }

    }

}

