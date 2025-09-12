window.addEventListener('DOMContentLoaded', () => {
    submitForm();
});

function submitForm() {
    const form = document.getElementById("submitForm");
    form.addEventListener("submit", function(event) {
        event.preventDefault();

        const inputs = form.querySelectorAll("input");
        for (const input of inputs) {
            if (!input.value.trim()) {
                alert("Por favor, preencha todos os campos.");
                return;
            }
        }
        
        const cpfValido = validarCpf(document.getElementById("cpf").value);
        if (!cpfValido) {
            alert("CPF inválido.");
            return;
        }

        const cnpjValido = validarCnpj(document.getElementById("cnpj").value);
        if (!cnpjValido) {
            alert("CNPJ inválido.");
            return;
        }

        alert("Formulário enviado com sucesso!");
        form.submit();
    });
}