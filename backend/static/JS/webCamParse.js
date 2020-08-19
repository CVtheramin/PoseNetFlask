function generateThumbnail() {
    var thecanvas = document.getElementById('thecanvas')
    //generate thumbnail URL data
    var context = thecanvas.getContext('2d');
    context.drawImage(videoElement, 0, 0, 440, 300);
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
    par.innerHTML = JSON.stringify(pose)
    // console.log(typeof pose.keypoints)
    CURRENT_POSE = pose.keypoints
  });
}
// global or parent scope of handlers
var videoElement = document.getElementById("videoElement");
var CURRENT_POSE = None

setInterval(function(){generateThumbnail(); getPose(); detect_movement(CURRENT_POSE);}, 1000)
