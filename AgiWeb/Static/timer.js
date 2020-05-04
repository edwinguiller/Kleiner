
function dateTimeConverter(timeMs) { //convertit  le temps en ms en heures minutes secondes
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


class Chrono {
  constructor() {
    this.el = document.getElementById("chrono") //(objet html) il n'y a qu'un seul chrono, d'où l'"id"
    this.timeOffset = parseInt(this.el.getAttribute("chrono"))*1000 // convertit en entier ms le temps de la BDDà l'instant où la page s'actualise
    this.timeInit = TIME_SCRIPT_START - this.timeOffset;
    }

  handler(timeNow) { //propre à la classe chrono
    var timeDelta = timeNow - this.timeInit
    this.el.innerText = dateTimeConverter(timeDelta)
  }
}

class TimerProducts{
  constructor(el) {
    this.el = el //ici il y a plusieurs timer product d'où l'argument el pour le faire plusieurs fois
    this.deadline = TIME_SCRIPT_START + parseInt(this.el.getAttribute("timer"))*1000
  }
  handler(timeNow) { //propriété de la classe TimerProducts
    var timeDelta = this.deadline - timeNow

    // If the count down is finished, write some text
    if (timeDelta < 0) {
      this.el.innerHTML = "Terminé"; // quand le cool down devient nul on afficher "terminé""
      this.el.parentNode.getElementsByClassName("validation")[0].removeAttribute("hidden") // et on dévoile le "oui" : le parent de l'élément de classe "validation"
    } else {
      this.el.innerText = dateTimeConverter(timeDelta)
    }
  }
}

class TimerFournisseurs{
  constructor(el) {
    this.el = el
    this.deadline = TIME_SCRIPT_START + parseInt(this.el.getAttribute("timer"))*1000
  }
  handler(timeNow) {
    var timeDelta = this.deadline - timeNow

    // If the count down is finished, write some text
    if (timeDelta < 0) {
      this.el.innerHTML = "0s" // quand le cool down devient nul on affiche "0s"
    } else {
      this.el.innerText = dateTimeConverter(timeDelta)
    }
  }
}
//script begin now
const TIME_SCRIPT_START = new Date().getTime();


timerProductsHtml = document.getElementsByClassName("timer") // on recupére tout les timers (objets html) que l'on met dans cette liste

toWatchEl = [] //on va mettre tout les chronos, timers (objet js) dans cette liste
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
  var timeNow = new Date().getTime();//temps actuel en ms depuis le 1er janvier 1970

  for (const el of toWatchEl) {
    el.handler(timeNow)
  }
  }

timerHandler()
// setInterval est une "builtin" fonction de js
var x = setInterval(timerHandler, 1000)
