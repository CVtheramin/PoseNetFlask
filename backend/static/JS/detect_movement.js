let PREVIOUS_POSITION;
let THRESHOLD = 2
// all caps generally don't change in JS
// generally use cammel case for identifiers
// if you don't use let in for loops it defines in the global scope
// vars should have descriptive names

function detect_movement(pose){
  document.getElementById('stats').innerHTML = '';
  if (PREVIOUS_POSITION){
    let moves = {}
    for (let i=0; i<pose.length; i++){
      const startCoord = PREVIOUS_POSITION[i]['position'];
      const endCoord = pose[i]['position'];
      const dist = get_distance(startCoord, endCoord);
      if (dist > THRESHOLD){
        const part = pose[i]['part'];
        document.getElementById('stats').textContent += `${part} moved ${dist} \n`;
        moves[part] = dist
      }
    }; //end for
    PREVIOUS_POSITION = pose;
    console.log(moves)
    return moves
  } else {
    PREVIOUS_POSITION = pose;
    return {'None': 0}
  }

}

function get_distance(pointa, pointb){
  var a = pointa['x'] - pointb['x'];
  var b = pointa['y'] - pointb['y'];
  return Math.sqrt(a*a + b*b)
}
