var myVideoStream = document.getElementById('myVideo')
var currentImage;

const canvas = document.querySelector("#canvas");
const photos = document.querySelector("#photos");
let width= 640, height= 0, bStreaming = false;

//csrf token
function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie !== '') {
      var cookies = document.cookie.split(';');
      for (var i = 0; i < cookies.length; i++) {
          var cookie = cookies[i].trim();
          // Does this cookie string begin with the name we want?
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
}

var csrftoken = getCookie('csrftoken');

function GetVideo(){ 
  navigator.mediaDevices.getUserMedia({video: true, audio: false})
  .then(function(stream){
    myVideoStream.srcObject = stream;
    myVideoStream.onloadedmetadata = function(e) {
      myVideoStream.play();
      height = myVideoStream.videoHeight /(myVideoStream.videoWidth / width);
      myVideoStream.setAttribute('width', width);
      myVideoStream.setAttribute('height', height);
      canvas.setAttribute('width', width);
      canvas.setAttribute('height', height);
     streaming = true;
    };
})
.catch(function(err){
    console.log('Error: ' + err.name + "/" + err.message);
});
}

function TakePicture(){
  const context = canvas.getContext('2d');
  if(width && height){
    canvas.width = width;
    canvas.height = height;
    context.drawImage(myVideoStream, 0, 0, width, height);
    const imgUrl = canvas.toDataURL('image/png');
    currentImage = imgUrl;
    const img = document.createElement('img');
    img.setAttribute('src', imgUrl);
    img.setAttribute('id', 'Base64Image');
    photos = img;
  }
}

var httpRequest = new XMLHttpRequest();
function Upload(){
  var imageName = encodeURIComponent(document.getElementById('name').value);
  //Initiate the request   

  httpRequest.onreadystatechange = callFunc;
  httpRequest.open('POST', 'UploadPhoto', true);

  //Send proper headers
  httpRequest.setRequestHeader("Content-type", "application/json");
  httpRequest.setRequestHeader('X-CSRFToken', csrftoken);
  httpRequest.setRequestHeader('ImageName', imageName);

  //Send your data
  httpRequest.send(currentImage);
}

function callFunc(){
	if(httpRequest.readyState == 4){
		if(httpRequest.status == 200){
			var responseData = httpRequest.responseText;
      const obj = JSON.parse(responseData);
			document.getElementById("result").innerHTML = obj.result;
		}
	}
}