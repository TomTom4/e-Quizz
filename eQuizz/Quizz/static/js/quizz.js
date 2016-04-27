
$(function() {
    $("#acces-etudiant").submit(function() {
      var code = $("#code").val();
      window.location.href = "etudiant/" + code;
      return false;
    });

    if (window.page == "etudiant") {
      window.question_numero = -1;

      window.refresh_etudiant = function() {
        $.getJSON("/etudiant_refresh/" + window.code, function(res) {
          if (res.error) {
            alert('Erreur : ' + res.error);
          }
          else if (res.question_type == "QCM" && res.numero > window.question_numero) {
            window.question_numero = res.numero;
            $(".numero").text(res.numero);
            $("#question-qcm").removeClass('hidden');
            $("#rien-en-cours").addClass('hidden');
          }

          setTimeout(window.refresh_etudiant, 2000);
        });
      };
      window.refresh_etudiant();

      $(".reponse").click(function() {
        $("#question-qcm").addClass('hidden');
        $("#rien-en-cours").removeClass('hidden');
      });
    }

});
