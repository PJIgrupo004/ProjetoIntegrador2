// Função para ir par ao whatsapp
function redirectToWhatsapp(phoneNumber ) {
    var contentMessage = "";
    var initialMessage = encodeURIComponent("Olá!\nSolicito um orçamento\nSeguem os dados:\n")
    var e = document.getElementById("tipo_servico");

    contentMessage += "*Nome*: " + document.getElementById("name").value + "\n";
    contentMessage += "*Tipo de Serviço*: " + e.options[e.selectedIndex].text + "\n";
    contentMessage += "*Descrição*: " + document.getElementById("message").value +"\n";
    
    // Abre o WhatsApp com a mensagem
    window.open("https://api.whatsapp.com/send?phone=" + phoneNumber + "&text="+ initialMessage + encodeURIComponent(contentMessage));

    return false;
}

function scrollToBottom() {
    window.scrollTo(0, document.body.scrollHeight);
}

function updateArrow(up, down) {
    const arrowUp = document.getElementById(up);
    const arrowDown = document.getElementById(down);

    if (arrowDown.style.display === "none") {
        arrowUp.style.display = 'none'; 
        arrowDown.style.display = 'inline';
    } else {
        arrowUp.style.display = 'inline';
        arrowDown.style.display = 'none';
    }
}
