function generateThumbnail() {
    var thecanvas = document.getElementById('thecanvas')
    //generate thumbnail URL data
    var context = thecanvas.getContext('2d');
    context.drawImage(video, 0, 0, 440, 300);
    // var dataURL = thecanvas.toDataURL();

    // //create img
    // var img = document.getElementById('thumb');
    // img.setAttribute('src', dataURL);

    // hideThumbs()
}


function hideThumbs() {
  var x = document.getElementById("thecanvas");
  x.style.display = "none"
}

function getPose() {
  var flipHorizontal = false;

  var imageElement = document.getElementById('thecanvas');

  posenet.load().then(function(net) {
    const pose = net.estimateSinglePose(imageElement, {
      flipHorizontal: true,
      decodingMethod: "single-person"
    });
    return pose;
  }).then(function(pose){
    var par = document.getElementById('stats')
    par.innerHTML = JSON.stringify(pose['keypoints'])
  })
}
// global or parent scope of handlers
var video = document.getElementById("videoElement");


setInterval(function(){generateThumbnail(); getPose();}, 1000)
