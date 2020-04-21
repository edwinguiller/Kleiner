class Chrono {
  constructor() {
    this.el = document.getElementById("chrono")
    this.timeOffset = parseInt(this.el.getAttribute("chrono"))*1000
    this.timeInit = new Date().getTime() - this.timeOffset;
    console.log(this.timeOffset)
    console.log(this.timeInit)

  }

  handler(timeNow) {
    var timeDelta = timeNow - this.timeInit
    this.el.innerText = dateTimeConverter(timeDelta)
  }
}

class TimerProducts{
  constructor(el) {
    this.el = el
    this.deadline = timeInit + parseInt(this.el.getAttribute("timer"))*1000
  }
  handler(timeNow) {
    var timeDelta = this.deadline - timeNow

    // If the count down is finished, write some text
    if (timeDelta < 0) {
      this.el.innerHTML = "PATATTTTEs";
      this.el.parentNode.getElementsByClassName("validation")[0].removeAttribute("hidden")
    } else {
      this.el.innerText = dateTimeConverter(timeDelta)
    }
  }
}

class TimerFournisseurs{
  constructor(el) {
    this.el = el
    this.deadline = timeInit + parseInt(this.el.getAttribute("timer"))*1000
  }
  handler(timeNow) {
    var timeDelta = this.deadline - timeNow

    // If the count down is finished, write some text
    if (timeDelta < 0) {
      this.el.innerHTML = "0s"
    } else {
      this.el.innerText = dateTimeConverter(timeDelta)
    }
  }
}

let timeInit = new Date().getTime();


timerProductsHtml = document.getElementsByClassName("timer")

toWatchEl = []
for (const timerProductHtml of timerProductsHtml) {
  toWatchEl.push(new TimerProducts(timerProductHtml))
}

timerFournisseursHtml = document.getElementsByClassName("timer-fournisseurs")

for (const timerFournisseur of timerFournisseursHtml) {
  toWatchEl.push(new TimerFournisseurs(timerFournisseur))
}

const chrono = new Chrono()
toWatchEl.push(chrono)

function timerHandler() {

  // Get today's date and time
  var timeNow = new Date().getTime();

  for (const el of toWatchEl) {
    el.handler(timeNow)
  }
  }




function dateTimeConverter(timeMs) {
  var convertedTime;
  var hours = Math.floor((timeMs / (1000 * 60 * 60)));
  var minutes = Math.floor((timeMs % (1000 * 60 * 60)) / (1000 * 60));
  var seconds = Math.floor((timeMs % (1000 * 60)) / 1000);
  // Display the result in the element with id="demo"
  if (hours) {
    convertedTime = hours + "h "+ minutes + "m " + seconds + "s ";
  } else {
    convertedTime = minutes + "m " + seconds + "s ";

  }
  return convertedTime
}


timerHandler()
var x = setInterval(timerHandler, 1000)
