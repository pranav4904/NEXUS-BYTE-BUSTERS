function getLocation() {
    if (navigator.geolocation) {
      navigator.geolocation.watchPosition(showPosition);
    } else {
      alert("Geolocation is not supported by this browser.");
    }
  }

  function showPosition(position) {
    var latitude = position.coords.latitude;
    var longitude = position.coords.longitude;
    var speed = position.coords.speed;

    document.getElementById("latitude").innerHTML = "<h3>Latitude: <br></h3>" + "<h2>" +latitude+"</h2>";
    document.getElementById("longitude").innerHTML = "<h3>Longitude: <br></h3>" + "<h2>" +longitude+"</h2>";
    document.getElementById("speed").innerHTML = "<h3>Speed: <br></h3>" + "<h2>" + speed*18/5 + " km/h" + "</h2>";

    checkSpeedLimit(speed);
}

var maxSpeedLimit = 80; // in km/h
var speedExceedCount = 0;

function checkSpeedLimit(speed) {

    if (speed*18/5 > maxSpeedLimit) {
        speedExceedCount++;

        if(speedExceedCount < 5) {
            alert("CAUTION: You are trying to exceed your maximum speed limit");
        }

        if (speedExceedCount >= 5) {
            alert("CAUTION: OVERSPEEDING -- There is going to be a deduction!");
        }

    } else {
        speedExceedCount = 0;
    }
}
