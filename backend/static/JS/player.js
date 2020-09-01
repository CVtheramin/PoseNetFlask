function play(){
  var notes = JSON.get("{{url_for('log_pose')}}");
  var noteSequences = [];
  var start;
  var end;
  var timeStart = 0;
  var timeEnd = 0.5;
  var pitchVal;
  notes.forEach(loop);
  function loop(value, index, array){
    start, end, pitchVal = value;
	if (pitchVal <48 || pitchVal > 200) return;
	console.log(timeStart);
	console.log(timeEnd);
	console.log(pitchVal);
    noteSequences.push({pitch: pitchVal, startTime: timeStart, endTime: timeEnd});
	timeStart+=0.5;
	timeEnd+=0.5;
  }
    bodySequence = {
        notes: noteSequences,
        totalTime: timeEnd
      };
    player = new mm.Player();
    player.start(bodySequence);
    console.log("WEIRD");
}