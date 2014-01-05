/* (c) 2013 Aaron Land - Digital Blacksmith */

var gDebug = null;

function init() {
	gDebug = document.getElementById('debug');
	gDebug.innerHTML = '<b>DEBUG</b><br>';
	//gDebug.innerHTML += 'gBrightness = ' + gBrightness + '<br>';
}

function httpGET(url) {
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open("GET", '/'+url, false);
    xmlHttp.send(null);
	//console.log(xmlHttp.responseText);
    return xmlHttp.responseText;
}

function httpPOST(url, data) {
	//console.log(url, data)
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open("POST", '/'+url, true);
    xmlHttp.onload = function () {
    	console.log(this.responseText);
	};
	xmlHttp.send(data);
}

function moveDisplay(x) {
	var d = document.getElementById("displays");
	d.style.left = -x+'px';
}