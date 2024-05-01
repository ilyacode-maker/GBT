
//====================Variables==================//
var name = $("#BookName").val();
const url = window.location + "audio";
var tone = $("#prompt").val();
const END_SIGNATURE = [1,2,3,4,5,6,7,8]
fileInput = document.getElementById("FileInput");
var audio1 = new Audio("./static/out000.mp3");
var audio2 = new Audio("./static/out001.mp3");
var Audios = [audio1, audio2];
var Type = "File"





/* 
TODO LIST/:

-Input Handling                       -Done
-Requests to The server side          -Done
-Receiving Audio Chunks               -Done
-Live Audio Playing                   -Done
-Audio controls settings

*/






//============= Start Functionalities ============//


$("#tone").hide();
$("#FileInput").hide();
$("#BookName").hide();
$("#SendButton").hide();
$("#ChooseButton").show();
$("#InputDiv").show();


//========= Handling File/Text Choice ==========//
$("#ChooseButton").click(ShowForm);


function ShowForm() {

    var Chosen = $("#InputType").val();
    console.log(Chosen);
    $("#tone").show();
    $("#SendButton").show();
    $("#InputDiv").hide();
    $("#ChooseButton").hide();
    if (Chosen == "text") {
      Type = "Text";
      $("#BookName").show();

    }else {

      $("#FileInput").show();

    }

}


//========== Sending Data To Server Side ==========//
$("#SendButton").click(SendData);

function SendData() {

    var formData = new FormData();
    formData.append("Type",Type);
    formData.append('Tone', $("#tone").val());

    if (Type == "File") {

      var file = fileInput.files[0];
      formData.append('Content', file);

    } else {

      formData.append("Content",$("#BookName").val());
    }

    //Send a POST request to get the audios back
    fetch(url, {

      method: "POST",
      body : formData


    })
    .then(response => response.body)
    .then(stream => {
        var reader = stream.getReader();
        ReadStream(reader);
    })
    .catch( (error) => {

       console.error(error);

    });
    
}




//====Piecing Audio Chunks together====// 
var i = 0;
var SnowBallEffect = false;
var event = new Event("NewAudio");

//========== Listening for new Added Audios =============//
document.addEventListener("NewAudio", function() {
  
  if (i < Audios.length && !SnowBallEffect) {

    Audios[i].play()
    LiveAudio();
    SnowBallEffect = true;

  }

},false);

//========== Plays the next audio once the current one is done ==================//
function LiveAudio() {
  // console.log(i);
  Audios[i].onended = () => {
    if (i + 1 < Audios.length) {
      SnowBallEffect = true;
      i++;
      Audios[i].play();
      LiveAudio(i);
      
      

    }else {

      i++;
      SnowBallEffect = false;

    }

  }

}




//============ Checks If 2 Lists are Equal ===================//
function EqualList(list1,list2) {

  if (list1.length != list2.length) {

    return false;

  }
  var Different = false
  for (var i = 0; i < list1.length;i++) {

    if (list1[i] != list2[i]) {

      Different = true;
      break;

    }

  }
  return !Different

}

//======= Opening a ReadStream to Get Audio Chunks============//
async function ReadStream(reader) {
  chunks = [];
  while (true) {
      var { done, value } = await reader.read();
      if (done) {
          console.log("Stream is done");
          break;
      }
      LastEight = value.slice(-8);
      value = value.slice(0, value.length - 8);
      chunks.push(value); 
      
      //Check for the end signature to mark the chunks array as a new file
      if (EqualList(LastEight,END_SIGNATURE)) {

        var arr = new Uint8Array(chunks.reduce((acc, chunks) => acc.concat(Array.from(chunks)), []));
        var audioBlob = new Blob([arr]);
        var AudioURL = URL.createObjectURL(audioBlob);
        var AudioObject = new Audio(AudioURL);
        Audios.push(AudioObject);
        document.dispatchEvent(event);
        chunks = [];

      }else {

        chunks.push(LastEight)

      }
  }
}
