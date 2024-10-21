document.addEventListener("DOMContentLoaded", function() {
    const alertModal = document.getElementById("alert-modal");
    if (alertModal) {
        setTimeout(() => {
            alertModal.style.display = 'none';
        }, 3000);
    }
});

function hideModal() {
    const alertModal = document.getElementById('alert-modal');
    alertModal.classList.remove('show');
    alertModal.style.display = 'none'; // Esconde o modal
}

function goBackOneLevel() {
    const currentUrl = window.location.pathname;
    const newUrl = currentUrl.substring(0, currentUrl.lastIndexOf('/'));
    window.location.href = newUrl;
}