function applyMask(selector, masks) {
    $('input[name="' + selector + '"]').inputmask({
        mask: masks,
        showMaskOnHover: false,
        showMaskOnFocus: true
    });
}

$(document).ready(function() {
    applyMask("telefone", ['(99) 9999-9999','(99) 99999-9999']);
    applyMask("cpf_cnpj", ['999.999.999-99','99.999.999/9999-99']);
    applyMask("cep", ['99999-999']);
});
