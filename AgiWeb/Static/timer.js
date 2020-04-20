console.log("ça marche")

timersHtml = document.getElementsByClassName("timer")
console.log(timersHtml)
let now = new Date().getTime();
console.log(now)

let deadlines = []

for (var timerHtml of timersHtml) {
  console.log(timerHtml.getAttribute("timer"))

  var deadline = now + parseInt(timerHtml.getAttribute("timer"))*1000
  deadlines.push(deadline)
}

console.log(deadlines)

function timerHandler() {

  // Get today's date and time
  var now = new Date().getTime();

  // Find the distance between now and the count down date
  for (var i=0; i < timersHtml.length; i++ ) {
    var distance = deadlines[i] - now;

    // Time calculations for days, hours, minutes and seconds
    var hours = Math.floor((distance / (1000 * 60 * 60)));
    var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
    var seconds = Math.floor((distance % (1000 * 60)) / 1000);
    // Display the result in the element with id="demo"
    if (hours) {
      timersHtml[i].innerHTML = hours + "h "+ minutes + "m " + seconds + "s ";
    } else {
      timersHtml[i].innerHTML = minutes + "m " + seconds + "s ";

    }

    // If the count down is finished, write some text
    if (distance < 0) {
      timersHtml[i].innerHTML = "PATATTTTEs";
    }
  }
}

timerHandler()
var x = setInterval(timerHandler, 1000)
