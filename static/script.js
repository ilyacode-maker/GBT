const url = window.location + "audio";


//====================Variables==================//
var name = $("#BookName").val();
var tone = $("#prompt").val();
const END_SIGNATURE = [1,2,3,4,5,6,7,8]
var audio1 = new Audio("./static/out000.mp3");
var audio2 = new Audio("./static/out001.mp3");
var Audios = [audio1, audio2];




/* 
TODO LIST/:

-Input Handling
-Requests to The server side
-Live Audio Playing                   -Done
-Audio controls settings

*/

//====== Handling Ebook Input =============//

// var book = ePub();
// var rendition;


// document.getElementById("FileInput").addEventListener("change", function(e) {
//   var file = e.target.files[0];
//   if (window.FileReader) {

//     var reader = new FileReader();
//     reader.onload = openBook;
//     reader.readAsArrayBuffer(file);

//   }
// });



// function openBook(e){
//   var bookData = e.target.result;

//   book.open(bookData, "binary");

//   rendition = book.renderTo("area", {
//     width: "100%",
//     height: 600
//   });

//   rendition.display();

// }



//======Simulating a late response======//
// setTimeout(() => {

//   Audios.push(audio4);

// },2000);

// setTimeout(() => {

//   Audios.push(audio5);

// },5000);

// setTimeout(() => {

//   SendChunk("Something","who_cares", url);

// }, 7500);
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
// async function SendChunk(chunk,tone, url) {
//   try {
//     data  = {"Chunk" : chunk};
//     var response = await fetch(url, {
//         method: "POST",
//         headers: {
//           "Content-Type": "application/json",
//         },
//         body: JSON.stringify(data)
//       });
//       console.log(response);
//       var audioBlob = await response.blob();
//       var AudioURL = URL.createObjectURL(audioBlob);
//       var AudioObject = new Audio(AudioURL);
//       Audios.push(AudioObject);
//   } catch (error) {

//     console.log("error : " + error);

//   }
  
// }

// SendChunk("something","who_cares",url)



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

async function consumeStream(reader) {
  chunks = [];
  while (true) {
      var { done, value } = await reader.read();
      if (done) {
          console.log("Stream is done");
          break;
      }
      console.log(value);
      LastEight = value.slice(-8);
      value = value.slice(0, value.length - 8);
      chunks.push(value); 
      if (EqualList(LastEight,END_SIGNATURE)) {

        var arr = new Uint8Array(chunks.reduce((acc, chunks) => acc.concat(Array.from(chunks)), []));
        var audioBlob = new Blob([arr]);
        var AudioURL = URL.createObjectURL(audioBlob);
        var AudioObject = new Audio(AudioURL);
        Audios.push(AudioObject);
        chunks = [];

      }else {

        chunks.push(LastEight)

      }
      
      

      
      
      
  }
}

fetch(url)
    .then(response => response.body)
    .then(stream => {
        var reader = stream.getReader();
      consumeStream(reader);
    });