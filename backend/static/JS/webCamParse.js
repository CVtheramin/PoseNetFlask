function generateThumbnail() {

    context.drawImage(videoElement, 0, 0, 440, 300);
    // var dataURL = thecanvas.toDataURL();

    // //create img
    // var img = document.getElementById('thumb');
    // img.setAttribute('src', dataURL);

    // hideThumbs()
}


function drawPoint(x, y, r){
  context.beginPath();
  context.arc(x, y, r, 0, 2 * Math.pi);
  context.stroke();
  context.fillStyle = '#FFFFFF';
  context.fill();
}

function drawKeypoints(keypoints) {
    for (let i = 0; i < keypoints.length; i++) {
      const keypoint = keypoints[i];
      console.log(keypoint);
      const { y, x } = keypoint.position;
      console.log(x)
      drawPoint(y, x, 3);
    }
    return keypoints
  }


function hideThumbs() {
  var x = document.getElementById("thecanvas");
  x.style.display = "none"
}

function getPose() {
  var flipHorizontal = false;

  var imageElement = document.getElementById('thecanvas');

  return posenet.load().then(function(net) {
    const pose = net.estimateSinglePose(imageElement, {
      flipHorizontal: true,
      decodingMethod: "single-person"
    });
    return pose;
  }).then(function(pose){
    var par = document.getElementById('stats')
    // par.innerHTML = JSON.stringify(pose)
    currentPose=pose.keypoints
    return pose.keypoints
  }).then(drawKeypoints)
}
// global or parent scope of handlers
const videoElement = document.getElementById("videoElement");
const theCanvas = document.getElementById('thecanvas')
const context = thecanvas.getContext('2d');

function runPipeline(){
  generateThumbnail();
  getPose().then(detect_movement);
};
let currentPose;

setInterval(runPipeline, 1000)
