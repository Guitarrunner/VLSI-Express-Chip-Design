function generateQRCode() {
	var data = document.getElementById("data").value
	eel.generate_qr(data)(setImage)
}

function setImage(base64) {
	document.getElementById("qr").src = base64
}

function postRequest(data){
	eel.api(data)
}

function test(){
	document.getElementById("ErrorText").value = "RACSO\nRACSO\nRACSO\nRACSO\nRACSO\nRACSO\nRACSO\nRACSO\nRACSO\nRACSO\nRACSO\nRACSO\nRACSO\nRACSO\nRACSO"
	document.getElementById("AllText").value = "RACSO"
	document.getElementById("WarningsText").value = "RACSO"
	eel.testing()
}