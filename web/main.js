// Navbar File
function postRequest(data){
	eel.api(data)
}

function openFile(){
	eel.apiOpenFile()(aux_openFile)
}

function aux_openFile(text){
	document.getElementById("content_text").value = text[0]
	document.getElementById("fileName").innerHTML = text[1]
	document.getElementById("filePath").innerHTML = text[2]
}

function saveAs(){
	var content = document.getElementById("content_text").value
	eel.apiSaveAs(content)(aux_saveAs)
}

function aux_saveAs(fileName){
	document.getElementById("fileName").innerHTML = fileName[0]
	document.getElementById("filePath").innerHTML = fileName[1]
}


function save(){
	var content = document.getElementById("content_text").value
	var path = document.getElementById("filePath").innerHTML
	eel.apiSave([content,path])
}

function newDoc(){
	document.getElementById("content_text").value = ""
	document.getElementById("fileName").innerHTML = "Untitled Document"
	document.getElementById("filePath").innerHTML = ""
}



// Navbar Edit
function undoBtn(){
	document.execCommand("undo")
}

function redoBtn(){
	document.execCommand("redo")
}

function cutBtn(){
	document.execCommand("cut")
}

function copyBtn(){
	document.execCommand("copy")
}

function pasteBtn(){
	document.execCommand("paste")
}

function selectAllBtn(){
	document.execCommand("selectAll")
}

function background1() {
            document.body.style.backgroundImage = "url(img/bg-img/BLUE.png)"
          }

		  function background2() {
            document.body.style.backgroundImage = "url(img/bg-img/WHITE.png)"
          }

		  function background3() {
            document.body.style.backgroundImage = "url(img/bg-img/GREEN.png)"
          }



// Test
function test(){
	document.getElementById("ErrorText").value = document.getElementById("file-input").files[0].name
	document.getElementById("AllText").value = "eoooooo"
	document.getElementById("WarningsText").value = "racso"
	var url = URL.createObjectURL(document.getElementById("file-input").files[0]);
	postRequest(url)
	eel.testing()
}