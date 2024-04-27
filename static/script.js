const url = window.location + "audio";

var name = $("#BookName").val();
var tone = $("#prompt").val();
SendChunk(name,tone);
/* 
TODO LIST/:

-Input Handling
-Requests to The server side
-Piecing Everything Together 

*/



async function SendChunk(chunk,tone) {
  try {
    data  = {"Chunk" : chunk};
    var response = await fetch(url, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data)
      });
    var something = await response.arrayBuffer();
    console.log(something.slice())

  } catch (error) {

    console.log("error : " + error);

  }
}
