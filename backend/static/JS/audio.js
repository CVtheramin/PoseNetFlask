var mediaRecorder = null,
    chunks = [],
    i = 0;

function onSuccess( stream ) {
    mediaRecorder = new MediaRecorder( stream );
    mediaRecorder.ondataavailable = function( event ) {
        chunks.push(event.data);
        var audioBlob = new Blob([event.data]);
        var audioUrl = URL.createObjectURL(audioBlob);
        var audio = new Audio();
        audio.autoplay = true;
        audio.src = audioUrl;
    }

    mediaRecorder.onstop = function() {
        for (i = 0; i<chunks.length; i++){
            console.log(i);
        }
        var audio = document.createElement('audio'),
            audio_blob = new Blob(chunks, {
                'type' : 'audio/mpeg'
            });
        audio.controls = 'controls';
        audio.autoplay = 'autoplay';
        audio.src = window.URL.createObjectURL(audio_blob);
        document.body.appendChild(audio);

        var upload = document.getElementById("upload");
        upload.addEventListener("click", function(event) {
            var xhr = new XMLHttpRequest();
            xhr.onload = function(e) {
                if (this.readyState === 4) {
                    console.log("Server returned: ", e.target.responseText);
                }
            };
            var fd = new FormData();
            fd.append("audio_data", audio_blob, "blob");
            xhr.open("POST", "/api/upload", true);
            xhr.send(fd);
        })
    };
}


var onError = function(err) {
    console.log('Error: ' + err);
}

navigator.mediaDevices.getUserMedia({ audio: true }).then(onSuccess, onError);
