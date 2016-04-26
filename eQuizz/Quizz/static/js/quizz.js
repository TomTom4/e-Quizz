
$(function() {
    $("#acces-etudiant").submit(function() {
      var code = $("#code").val();
      window.location.href = "etudiant/" + code;
      return false;
    });

    
});
