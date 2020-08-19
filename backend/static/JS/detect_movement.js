var PREVIOUS_POSITION = getPose();
var THRESHOLD = 2


function detect_movement(pose){
  for (i=0; i<pose.length; i++){
    dist = get_distance(pose[i]['position'], PREVIOUS_POSITION[i]['position'])
    if (dist > THRESHOLD){
      document.getElementById('stats').textContent += `${pose['i']['part']} moved ${dist} \n`
    }
    PREVIOUS_POSITION = pose
  }

}

function get_distance(pointa, pointb){
  var a = pointa['x'] - pointb['x']
  var b = pointa['y'] - pointb['y']
  return Math.sqrt(a*a + b*b)
}
