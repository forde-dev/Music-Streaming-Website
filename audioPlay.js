(function() {

  document.addEventListener('DOMContentLoaded', init, false);

  audioPlayer();
  function audioPlayer(){
    $('#audioPlayer')[0].src = $('#songlist tr td a')[0];
    $('#audioPlayer')[0].play();
    $('#songlist tr td a').click(function(e){
      e.preventDefault();
      $('#audioPlayer')[0].src = this;
      $("#audioPlayer")[0].play();
    });
  }

})();
