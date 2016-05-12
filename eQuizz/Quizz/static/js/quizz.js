
$(function() {
  $("#acces-etudiant").submit(function() {
    var code = $("#code").val();
    window.location.href = "etudiant/" + code;
    return false;
  });

  if (window.page == "etudiant") {
    console.log("Page étudiant");
    
    window.question_numero = -1;

    window.refresh_etudiant = function() {
      $.getJSON("/etudiant_refresh/" + window.code, function(res) {
        if (res.error) {
          alert('Erreur : ' + res.error);
        }
        else if (res.question_type == "QCM" && res.numero > window.question_numero) {
          window.question_numero = res.numero;
          $("input[name=id]").val(res.id);
          $(".numero").text(res.numero);

          $(".question-qcm").removeClass('hidden');
          $("#rien-en-cours").addClass('hidden');
          $(".question-open").addClass('hidden');
        }
        //Expérimental par Thomas
        else if (res.question_type == "Open" && res.numero > window.question_numero) {
          window.question_numero = res.numero;
          $("input[name=id]").val(res.id);
          $(".numero").text(res.numero);

          $(".question-open").removeClass('hidden');
          $(".question-qcm").addClass('hidden');
          $("#rien-en-cours").addClass('hidden');
        }

        setTimeout(window.refresh_etudiant, 1000);
      });
    };
    window.refresh_etudiant();

    $(".reponse").click(function() {
      $(".question-qcm").addClass('hidden');
      $(".question-open").addClass('hidden');
      $("#rien-en-cours").removeClass('hidden');
      $(".warning_yellow").removeClass('hidden');
      $("#warning_red").addClass('hidden');
      $("input[name=valeur]").val($(this).attr('data-valeur'));
      $(".question-qcm form").ajaxSubmit();
    });

    $(".warning_yellow").click(function(){
      $(".warning_yellow").addClass('hidden');
      $("#warning_red").removeClass('hidden');
      //$("input[name = valeur_lost]").val($(this).attr('data-valeur'));
      $("#warning form").ajaxSubmit();
    });


    $(".open-submit").click(function() {
      $(".question-qcm").addClass('hidden');
      $(".question-open").addClass('hidden');
      $("#rien-en-cours").removeClass('hidden');
      //$("input[name=valeur]").val($(this).attr('data-valeur'));
      $(".question-open form").ajaxSubmit();
    });

  }


  //Expérimental
  /*if(window.page=="prof"){
  window.question_numero=-1;
  window.refresh_prof = function(){
  $.getJSON("/prof_refresh/"+window.code+"/"+window.question_numero, function(res){
  if (res.error) {
  alert('Erreur : ' + res.error);
}
else if(res.question_type="QCM"



}
}
}*/

});
