$(document).ready(function() {
    $('#uploadMe').submit(function(e) {
        e.preventDefault();
        $('#lsg').empty();
        $('#lsg').hide();
        $('#lsgShow').prop("checked", false);
        $('#waiting-wheel').show();
        $('#svgOutput').empty();
        $('#hint').empty();
        $('#faqText').hide();
        $('#lsgDiv').hide();

        formData = new FormData($(this)[0]);

        $.ajax({
            url: "api/neueAufgabe",
            type: 'POST',
            data: formData,
            success: function (data) {
                console.log(data);
                if (!data.done) {
                    alert(data.err)
                }
                else {
                    $('#waiting-wheel').hide();
                    $('#rightSide').hide();
                    if (data.hint) {
                        $('#hint').append(data.hint);
                        $('#rightSide').show();  
                    }
                    $('#svgOutput').append(data.svg);
                    $('#svgOutput').show();
                    if (data.lsg) {
                        $('#lsg').empty();
                        $('#lsg').hide();
                        $('#lsg').append(data.lsg);
                        $('#lsgDiv').show();
                    }
                    else {
                        $('#lsg').empty()
                        alert("Keine Lösung hinterlegt. Good luck!")
                    }
                }
            },
            cache: false,
            contentType: false,
            processData: false
        });
    });
});


$(document).ready(function() {
    $('#myonoffswitch').change(function() {
        if (this.checked) {
            $('#menucontainer').show(500);
        } else {
            $('#menucontainer').hide(500);
        }
    });
});

$(document).ready(function() {
    $('#lsgShow').change(function() {
        if (this.checked) {
            $('#lsg').show(500);
        } else {
            $('#lsg').hide(500);
        }
    });
});

$(document).ready(function() {
    $('select').niceSelect();
  });

$(document).ready(function() {
    $('#faq').click(function() {
        $('#rightSide').hide();
        $('#hint').empty();
        $('#svgOutput').hide();
        $('#lsg').hide();
        $("#lsgDiv").hide();
        $("#faqText").show();
    });
  });