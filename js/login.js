window.addEventListener('DOMContentLoaded', () => {
    loginForm();
});

function loginForm() {
    const form = document.getElementById("loginForm");
    form.addEventListener("submit", function(event) {
        event.preventDefault();

        const inputs = form.querySelectorAll("input");
        for (const input of inputs) {
            if (!input.value.trim()) {
                alert("Por favor, preencha todos os campos.");
                return;
            }
        }

        const senha = form.querySelector('input[name="senha"]').value;
        const cpfValido = validarCpf(senha);
        if (!cpfValido) {
            alert("CPF inválido.");
            return;
        }

        const formData = new FormData(form);

        fetch('/login/usuarios', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert("Login realizado com sucesso!");
            } else {
                alert("Falha no login: " + data.message);
            }
        });
    });
}

window.addEventListener('DOMContentLoaded', () => {
    loginForm();
});
