document.addEventListener('DOMContentLoaded', function() {
    // Verificar se já existe um handler de login na página
    if (document.getElementById('loginForm')) {
        initializeLoginForm();
    }
});

function initializeLoginForm() {
    const form = document.getElementById("loginForm");
    if (!form) return;

    // Evitar múltiplos event listeners
    if (form.dataset.initialized) return;
    form.dataset.initialized = "true";

    form.addEventListener("submit", function(event) {
        event.preventDefault();
        handleLogin(form);
    });
}

function handleLogin(form) {
    // Verificar se existe seletor de tipo de usuário (versão nova)
    const userTypeSelector = form.querySelector('input[name="userType"]:checked');
    
    if (userTypeSelector) {
        // Nova versão com seletor de tipo de usuário
        handleModernLogin(form, userTypeSelector.value);
    } else {
        // Versão legacy/simples
        handleLegacyLogin(form);
    }
}

function handleModernLogin(form, userType) {
    // Esta função é usada quando há seletor de tipo de usuário
    // O código principal está no HTML inline para evitar conflitos
    console.log('Login moderno detectado - delegando para handler inline');
}

function handleLegacyLogin(form) {
    // Validação para versão legacy
    const inputs = form.querySelectorAll("input[required]");
    for (const input of inputs) {
        if (!input.value.trim()) {
            showMessage("Por favor, preencha todos os campos obrigatórios.", "error");
            return;
        }
    }

    // Verificar se há campo CPF e validá-lo
    const cpfInput = form.querySelector('input[name="cpf"]');
    if (cpfInput && cpfInput.value.trim()) {
        if (typeof validarCpf === 'function' && !validarCpf(cpfInput.value)) {
            showMessage("CPF inválido.", "error");
            return;
        }
    }

    const loginUrl = '/login/usuarios';
    const formData = new FormData(form);

    fetch(loginUrl, {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success || data.message === 'Login feito com sucesso') {
            showMessage("Login realizado com sucesso!", "success");
            setTimeout(() => {
                window.location.href = '/usuario/dashboard';
            }, 1500);
        } else {
            showMessage("Falha no login: " + (data.message || data.error || 'Erro desconhecido'), "error");
        }
    })
    .catch(error => {
        showMessage("Erro de conexão. Tente novamente.", "error");
        console.error('Erro:', error);
    });
}

function showMessage(message, type) {
    // Tentar usar alert personalizado se existir
    const alertElement = document.getElementById('alert');
    if (alertElement && typeof showAlert === 'function') {
        showAlert(message, type);
    } else {
        // Fallback para alert nativo
        alert(message);
    }
}

// Função de compatibilidade para validação de CPF
function validarCpfCompat(cpf) {
    if (typeof validarCpf === 'function') {
        return validarCpf(cpf);
    }
    
    // Implementação fallback
    cpf = cpf.replace(/\D/g, '');
    if (cpf.length !== 11 || /^(\d)\1+$/.test(cpf)) return false;
    
    const calcDigito = (slice, fator) => {
        const soma = slice.split('').reduce((acc, num, i) => acc + +num * (fator - i), 0);
        const resto = soma % 11;
        return resto < 2 ? 0 : 11 - resto;
    };
    
    const dig1 = calcDigito(cpf.slice(0, 9), 10);
    const dig2 = calcDigito(cpf.slice(0, 10), 11);
    
    return cpf[9] == dig1 && cpf[10] == dig2;
}

// Exportar função para uso global se necessário
window.loginForm = initializeLoginForm;
window.validarCpfCompat = validarCpfCompat;