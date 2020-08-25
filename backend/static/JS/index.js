(() => {
  'use strict';
  const video = document.getElementById("video");
  const canvas = document.getElementById("canvas");
  const ctx = canvas.getContext("2d");
  const minConfidence = 0.6;
  const VIDEO_WIDTH = 320;
  const VIDEO_HEIGHT = 240;
  const frameRate = FRAME_RATE;

  // preview screen
  navigator.mediaDevices.getUserMedia({ video: true, audio: true })
    .then(vid => {
      video.srcObject = vid;
      const intervalID = setInterval(async () => {
        try {
          estimateMultiplePoses();
        } catch (err) {
          clearInterval(intervalID)
          setErrorMessage(err.message)
        }
      }, Math.round(1000 / frameRate))
      return () => clearInterval(intervalID)
    });
    // end of then
   function drawPoint(y, x, r) {
    ctx.beginPath();
    ctx.arc(x, y, r, 0, 2 * Math.PI);
    ctx.fillStyle = "#FFFFFF";
    ctx.fill();
  }
  function drawKeypoints(keypoints) {
    for (let i = 0; i < keypoints.length; i++) {
      const keypoint = keypoints[i];
      // console.log(`keypoint in drawkeypoints ${keypoint}`);
      const { y, x } = keypoint.position;
      drawPoint(y, x, 3);
    }
  }

  const estimateMultiplePoses = () => {
    console.log('estimating pose')
    posenet
      .load()
      .then(function (net) {
        //console.log("estimateMultiplePoses .... ");
        return net.estimateSinglePose(video, {
          decodingMethod: "single-person",
        });
      })
      .then(function (poses) {
        canvas.width = VIDEO_WIDTH;
        canvas.height = VIDEO_HEIGHT;
        ctx.clearRect(0, 0, VIDEO_WIDTH, VIDEO_HEIGHT);
        ctx.save();
        ctx.drawImage(video, 0, 0, VIDEO_WIDTH, VIDEO_HEIGHT);
        ctx.restore();
        console.log('starting to draw pose')
        if (poses['score'] >= minConfidence) {
            drawKeypoints(poses['keypoints']);
            //drawSkeleton(keypoints);
            if (running) {
              postRequest(poses['keypoints'], '/log_pose');
            }
            PASSED += 1;
          } else {
            FAILED += 1;
          }
        console.log(`passed:failed ${PASSED}:${FAILED}`);
      });
  };

})();


const LOGURL = '/log_pose';
let PASSED = 0;
let FAILED = 0;
let running = false;

function postRequest(pose, url){
  let xhr = new XMLHttpRequest();
  xhr.open("POST", url, true);
  xhr.setRequestHeader('Content-Type', 'application/json');
  xhr.send(JSON.stringify(pose));
}

const START_BUTTON = document.getElementById('startButton');
const MOVEMENT_THRESHOLD = document.getElementById('MOVEMENT_THRESHOLD');
const END_BUTTON = document.getElementById('stopButton')


START_BUTTON.addEventListener('click', function(){
  if (!running) {
    payload = {"MOVEMENT_THRESHOLD": MOVEMENT_THRESHOLD.value,
               "FRAME_RATE": FRAME_RATE,
               "SONG_TIME": SONG_TIME};
    postRequest(payload, '/start');
    running = true;
  }
}, false)

END_BUTTON.addEventListener('click', function(){
  if (running) {
    payload = {"Audio": "Placeholder"};
    postRequest(payload, '/stop');
    running = false;
  }
}, false)
