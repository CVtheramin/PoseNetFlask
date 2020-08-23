(() => {
  'use strict';
  const TWILIO_DOMAIN = location.host;
  const ROOM_NAME = 'tf';
  // const Video = Twilio.Video;
  let videoRoom, localStream;
  const video = document.getElementById("video");
  const canvas = document.getElementById("canvas");
  const ctx = canvas.getContext("2d");
  const minConfidence = 0.6;
  const VIDEO_WIDTH = 320;
  const VIDEO_HEIGHT = 240;
  const frameRate = 20;

  // preview screen
  navigator.mediaDevices.getUserMedia({ video: true, audio: true })
    .then(vid => {
      video.srcObject = vid;
      localStream = vid;
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
  function drawSegment(
    pair1,
    pair2,
    color,
    scale
  ) {
    ctx.beginPath();
    ctx.moveTo(pair1.x * scale, pair1.y * scale);
    ctx.lineTo(pair2.x * scale, pair2.y * scale);
    ctx.lineWidth = 2;
    ctx.strokeStyle = color;
    ctx.stroke();
  }

  function drawSkeleton(keypoints) {
    const color = "#FFFFFF";
    const adjacentKeyPoints = posenet.getAdjacentKeyPoints(
      keypoints,
      minConfidence
    );

    adjacentKeyPoints.forEach((keypoint) => {
      drawSegment(
        keypoint[0].position,
        keypoint[1].position,
        color,
        1,
      );
    });
  }

  const estimateMultiplePoses = () => {
    posenet
      .load()
      .then(function (net) {
        //console.log("estimateMultiplePoses .... ");
        return net.estimatePoses(video, {
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
        poses.forEach(({ score, keypoints }) => {
          if (score >= minConfidence) {
            drawKeypoints(keypoints);
            //drawSkeleton(keypoints);
            postPose(keypoints)
            PASSED += 1;
          } else {
            FAILED += 1;
          }
        });
        console.log(`passed:failed ${PASSED}:${FAILED}`);
      });
  };

})();

const LOGURL = '/log_pose';
let PASSED = 0;
let FAILED = 0;

function postPose(pose){
  let xhr = new XMLHttpRequest();
  xhr.open("POST", LOGURL, true);
  xhr.setRequestHeader('Content-Type', 'application/json');
  xhr.send(JSON.stringify(pose));
}
