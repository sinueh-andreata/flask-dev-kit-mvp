window.addEventListener('DOMContentLoaded', () => {
    mascaraTelefone();
    mascaraCpf();
    mascaraCnpj();
});


function mascaraTelefone(){
    const telefoneInput = document.getElementById('telefone');
    telefoneInput.addEventListener('input', function () {
        let v = this.value;

        v = v.replace(/\D/g, ''); // Remove tudo que não for número
        v = v.slice(0, 11);       // Limita a 11 dígitos
        v = v.replace(/^(\d{2})(\d{5})(\d{4})$/, '($1) $2-$3'); // Formata

        this.value = v;
    });
}

function mascaraCpf(){
    const cpfInput = document.getElementById('cpf');
    cpfInput.addEventListener('input', function () {
        let v = this.value;

        v=v.replace(/\D/g,"");
        v=v.replace(/(\d{3})(\d)/,"$1.$2");
        v=v.replace(/(\d{3})(\d)/,"$1.$2");
        v=v.replace(/(\d{3})(\d{1,2})$/,"$1-$2");
        this.value = v;
    });
}

function mascaraCnpj(){
    const cnpjInput = document.getElementById('cnpj');
    cnpjInput.addEventListener('input', function () {
        let v = this.value;

        v=v.replace(/\D/g,"");
        v=v.replace(/^(\d{2})(\d)/,"$1.$2");
        v=v.replace(/^(\d{2})\.(\d{3})(\d)/,"$1.$2.$3");
        v=v.replace(/\.(\d{3})(\d)/,".$1/$2");
        v=v.replace(/(\d{4})(\d)/,"$1-$2");
        this.value = v;
    })
}

function validarCpf(cpf) {
    cpf = cpf.replace(/\D/g, '');

    if (cpf.length !== 11 || /^(\d)\1+$/.test(cpf)) return false;

    const calcDigito = (slice, fator) => {
        const soma = slice
            .split('')
            .reduce((acc, num, i) => acc + +num * (fator - i), 0);
        const resto = soma % 11;
        return resto < 2 ? 0 : 11 - resto;
    };

    const dig1 = calcDigito(cpf.slice(0, 9), 10);
    const dig2 = calcDigito(cpf.slice(0, 10), 11);

    return cpf[9] == dig1 && cpf[10] == dig2;
}

function validarCnpj(cnpj) {
    cnpj = cnpj.replace(/[^\d]+/g, '');
    if (cnpj.length !== 14 || /^(\d)\1+$/.test(cnpj)) return false;

    let tamanho = cnpj.length - 2;
    let numeros = cnpj.substring(0, tamanho);
    let digitos = cnpj.substring(tamanho);
    let soma = 0;
    let pos = tamanho - 7;

    for (let i = tamanho; i >= 1; i--) {
        soma += parseInt(numeros.charAt(tamanho - i)) * pos--;
        if (pos < 2) pos = 9;
    }

    let resultado = soma % 11 < 2 ? 0 : 11 - (soma % 11);
    if (resultado != parseInt(digitos.charAt(0))) return false;

    tamanho += 1;
    numeros = cnpj.substring(0, tamanho);
    soma = 0;
    pos = tamanho - 7;

    for (let i = tamanho; i >= 1; i--) {
        soma += parseInt(numeros.charAt(tamanho - i)) * pos--;
        if (pos < 2) pos = 9;
    }

    resultado = soma % 11 < 2 ? 0 : 11 - (soma % 11);
    return resultado == parseInt(digitos.charAt(1));
}