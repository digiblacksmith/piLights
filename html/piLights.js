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

/*Object.prototype.toType = function() {
  return ({}).toString.call(this).match(/\s([a-zA-Z]+)/)[1].toLowerCase()
}*/

/*function httpGet(url) {
	var xhr = new XMLHttpRequest();
	xhr.open("GET", '/'+url, true);
	xhr.onload = function (e) {
		if (xhr.readyState === 4) {
			if (xhr.status === 200) {
				console.log(xhr.responseText);
				return xhr.responseText
			} else {
				console.error(xhr.statusText);
			}
		}
	};
	xhr.onerror = function (e) {
		console.error(xhr.statusText);
	};
	xhr.send(null);
}*/