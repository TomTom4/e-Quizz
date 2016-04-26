
$(function() {
    $("#acces-etudiant").submit(function() {
      var code = $("#code").val();
      window.location.href = "etudiant/" + code;
      return false;
    });

    window.question_id = -1;

    window.refresh_etudiant = function() {
      $.getJSON("/etudiant_refresh/" + window.code, function(res) {
        if (res.error) {
          alert('Erreur : ' + res.error);
        }
        else if (res.question_type == "QCM" && res.id > window.question_id) {
          window.question_id = res.id;
          $("#question-qcm").removeClass('hidden');
          $("#rien-en-cours").addClass('hidden');
        }

        setTimeout(window.refresh_etudiant, 2000);
      });
    };

    $(".reponse").click(function() {
      $("#question-qcm").addClass('hidden');
      $("#rien-en-cours").removeClass('hidden');
    });

    window.refresh_etudiant();

});
