from flask import Flask

def validar_cpf(cpf):
    cpf = ''.join(filter(str.isdigit, cpf))  # Remove tudo que não é número

    if len(cpf) != 11:
        return False

    if cpf == cpf[0] * 11:  # Verifica se todos os números são iguais (ex: 11111111111)
        return False

    def calc_digito(cpf_parcial, fator):
        soma = 0
        for i in range(len(cpf_parcial)):
            soma += int(cpf_parcial[i]) * (fator - i)
        resto = soma % 11
        return 0 if resto < 2 else 11 - resto

    digito1 = calc_digito(cpf[:9], 10)
    digito2 = calc_digito(cpf[:9] + str(digito1), 11)

    return cpf[-2:] == f"{digito1}{digito2}"
