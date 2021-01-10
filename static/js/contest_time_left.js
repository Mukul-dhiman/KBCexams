function getTimeRemaining(endtime) {
    var t = Date.parse(endtime) - Date.parse(new Date());
    var seconds = Math.floor((t / 1000) % 60);
    var minutes = Math.floor((t / 1000 / 60) % 60);
    var hours = Math.floor((t / (1000 * 60 * 60)) % 24);
    var days = Math.floor(t / (1000 * 60 * 60 * 36));
    return days + "Days: " + hours + ":" + minutes + ":" + seconds ;
  
  }
  
  function initializeClock(id, endtime) {
    var clock = document.getElementById(id);
  
    function updateClock() {
      var t = getTimeRemaining(endtime);

      clock.innerHTML = t;
  
      if (t.total <= 0) {
        clearInterval(timeinterval);
      }
    }
  
    updateClock();
    var timeinterval = setInterval(updateClock, 1000);
  }