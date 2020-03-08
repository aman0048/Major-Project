//webkitURL is deprecated but nevertheless
URL = window.URL || window.webkitURL;
var link = document.createElement('a');
var gumStream; 						//stream from getUserMedia()
var rec; 							//Recorder.js object
var input; 							//MediaStreamAudioSourceNode we'll be recording

// shim for AudioContext when it's not avb. 
var AudioContext = window.AudioContext || window.webkitAudioContext;
var audioContext; //audio context to help us record

var recordButton = document.getElementById("recordButton");
var stopButton = document.getElementById("stopButton");
var pauseButton = document.getElementById("pauseButton");
var sendBtn = document.getElementById("sendBtn");
var saveSound = document.getElementById('saveSound');

//add events to those 2 buttons
recordButton.addEventListener("click", startRecording);
stopButton.addEventListener("click", stopRecording);
pauseButton.addEventListener("click", pauseRecording);

function startRecording() {
	console.log("recordButton clicked");    
	var constraints = { audio: true, video: false };
	
	recordButton.disabled = true;
	stopButton.disabled = false;
	pauseButton.disabled = false;
	sendBtn.disabled=false;
	navigator.mediaDevices.getUserMedia(constraints).then(function(stream) {
		console.log("getUserMedia() success, stream created, initializing Recorder.js ...");
	
		audioContext = new AudioContext();
		gumStream = stream;
		
		/* use the stream */
		input = audioContext.createMediaStreamSource(stream);
		rec = new Recorder(input,{numChannels:1})

		//start the recording process
		rec.record()

		console.log("Recording started");

	}).catch(function(err) {
    	recordButton.disabled = false;
    	stopButton.disabled = true;
		pauseButton.disabled = true;
	});
}

function pauseRecording(){
	console.log("pauseButton clicked rec.recording=",rec.recording );
	if (rec.recording){
		//pause
		rec.stop();
		pauseButton.innerHTML="Resume";
	}else{
		//resume
		rec.record()
		pauseButton.innerHTML="Pause";

	}
}

function stopRecording() {
	console.log("stopButton clicked");
	stopButton.disabled = true;
	recordButton.disabled = false;
	pauseButton.disabled = true;
	pauseButton.innerHTML="Pause";
	rec.stop();
	gumStream.getAudioTracks()[0].stop();
	rec.exportWAV(createDownloadLink);
}

function createDownloadLink(blob) {
	
	var url = URL.createObjectURL(blob);
	var file = new File([blob], "sound.wav")
	saveSound.href = url;
	saveSound.download = 'sound.wav'; 
		var formData = new FormData()
      formData.append("audio", file);

      console.log('File : '+ file);
      console.log('Form Data : '+ formData);

		$.ajax({
			url: "http://127.0.0.1:5000/done",
			method: "POST",
			data: formData,
			processData: false,
			contentType: false,
			success: function (data) {
                localStorage.setItem("patient_name", data["patient_name"]);
                localStorage.setItem("patient_age", data["patient_age"]);
                localStorage.setItem("patient_gender", data["patient_gender"]);
                localStorage.setItem("patient_phone_number", data["patient_phone_number"]);			
                localStorage.setItem("Attendee_name", data["Attendee_name"]);
                localStorage.setItem("Attendee_phone_number", data["Attendee_phone_number"]);
                localStorage.setItem("Attendee_relationship_with_patient", data["Attendee_relationship_with_patient"]);

			}
		  })	
}

const ocr = document.getElementById('ocr-call').addEventListener('click', function(){
	$.get('http://127.0.0.1:5000/ocr', function(data){
		console.log(data);
		localStorage.setItem('ocr', data);
		document.getElementById('formats').innerHTML = data;
	})
})