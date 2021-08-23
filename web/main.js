// Navbar File
function postRequest(data){
	eel.api(data)
}

function openFile(){
	eel.apiOpenFile()(aux_openFile)
}

function openExample(filename){
	eel.apiOpenExample(filename)(aux_openFile)
}

function aux_openFile(text){
	//document.getElementById("content_text").value = text[0]
	document.querySelector('.CodeMirror').CodeMirror.setValue(text[0])
	document.getElementById("fileName").innerHTML = text[1]
	document.getElementById("filePath").innerHTML = text[2]
}

function saveAs(){
	var content = document.querySelector('.CodeMirror').CodeMirror.getValue()
	eel.apiSaveAs(content)(aux_saveAs)
}

function aux_saveAs(fileName){
	document.getElementById("fileName").innerHTML = fileName[0]
	document.getElementById("filePath").innerHTML = fileName[1]
	document.getElementById("InfoText").value = "File saved"
}


function save(){

	if(document.getElementById("fileName").innerHTML == "Untitled document"){
		saveAs()
	}else{
		var content = document.querySelector('.CodeMirror').CodeMirror.getValue()
		var path = document.getElementById("filePath").innerHTML
		eel.apiSave([content,path])
		document.getElementById("InfoText").value = "File saved"
	}
}

function newDoc(){
	document.querySelector('.CodeMirror').CodeMirror.setValue("")
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

// Run
function runBtn(){

	if (document.getElementById("analysis_content").value == ""){
		
		var analysis1 = document.getElementById("analysis1")
		var analysis2 = document.getElementById("analysis2")
		var analysis3 = document.getElementById("analysis3")
		var analysis4 = document.getElementById("analysis4")
		var analysis5 = document.getElementById("analysis5")
		var analysis = [analysis1,analysis2,analysis3,analysis4,analysis5]

		if(analysis[0].checked == false && analysis[1].checked == false && analysis[2].checked == false && analysis[3].checked == false && analysis[4].checked == false){
			$( function() {
				$( "#dialog" ).dialog();
			} );
			return false;
		}
		
		document.getElementById("InfoText").value = "Analysing in process"

		var selection = []
		for(let i=0;i < analysis.length;i++){
			if(analysis[i].checked == true){
				selection.push(analysis[i].value)
			}
		}

		var path = document.getElementById("filePath").innerHTML
		//var content = document.getElementById("analysis_content").value
		eel.apiRun([path,selection])(aux_runBtn)

	}else{
		let analysisFlow = document.getElementById("analysis_content").value
		var flow = analysisFlow.split(" ")
		var path = document.getElementById("filePath").innerHTML
		document.getElementById("analysis_content").value = ""
		eel.apiRun([path,flow])(aux_runBtn)
	}
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


function aux_runBtn(data){
	document.getElementById("ErrorText").value = data[0]
	document.getElementById("WarningsText").value = data[1]
	document.getElementById("InfoText").value = data[2]
	document.getElementById("analysis_content").value = "Type analysis"
}

function caret(){
	eel.api("IS TYPING\n")
}