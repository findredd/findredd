function typeDate() {
    document.getElementById('id_date_of_birth').setAttribute("type", "date");
}

function errorList() {
    var x = document.querySelectorAll("ul.errorlist");
    var text = "";
    var i;
    for (i = 1; i < x.length; i++) {
        text += x[i].innerHTML;
    }
    
    if (text != "") {
        document.getElementById("id_message").innerHTML = text;
    }
}
