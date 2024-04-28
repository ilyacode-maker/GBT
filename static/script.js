const url = window.location + "audio";


//====================Variables==================//
var name = $("#BookName").val();
var tone = $("#prompt").val();
var audio1 = new Audio("./static/out000.mp3");
var audio2 = new Audio("./static/out001.mp3");
var audio3 = new Audio("./static/out002.mp3");
var audio4 = new Audio("./static/out003.mp3");
var audio5 = new Audio("./static/out004.mp3");
var Audios = [audio1, audio2, audio3];



/* 
TODO LIST/:

-Input Handling
-Requests to The server side
-Live Audio Playing                   -Done
-Audio controls settings

*/

//======Given a Name Only=============//

function GetAudioName(BookName,tone) {

  FirstAudio = SendChunk(BookName,tone,url);
  var index = 0;
  Audios.push(FirstAudio);
  Audios[0].play();
  LiveAudio(0);

}



//======Simulating a late response======//
setTimeout(() => {

  Audios.push(audio4);

},2000);

setTimeout(() => {

  Audios.push(audio5);

},5000);

setTimeout(() => {

  SendChunk("Something","who_cares", url);

}, 7500);
//====Piecing Audio Chunks together====// 

Audios[0].play();
LiveAudio(0);

function LiveAudio(index) {

  Audios[index].onended = () => {
    if (index + 1 < Audios.length) {

      Audios[index + 1].play();
      LiveAudio(index + 1);

    }

  }

}



//========== Sending Request to get Audio Chunk in return =============//
async function SendChunk(chunk,tone, url) {
  try {
    data  = {"Chunk" : chunk};
    var response = await fetch(url, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data)
      });
      var audioBlob = await response.blob();
      var AudioURL = URL.createObjectURL(audioBlob);
      var AudioObject = new Audio(AudioURL);
      Audios.push(AudioObject);
  } catch (error) {

    console.log("error : " + error);

  }
  
}
