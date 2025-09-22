import re
from flask import jsonify

def validar_cpf(cpf):
    cpf = re.sub(r'[^\d]', '', cpf) 
    if not re.match(r'^\d{11}$', cpf):
        return jsonify({"error": "CPF deve ter 11 dígitos numéricos"}), 400

    if cpf == cpf[0] * 11:
        return jsonify({"error": "CPF inválido"}), 400

    def calc_digito(cpf_parcial, fator):
        soma = 0
        for i in range(len(cpf_parcial)):
            soma += int(cpf_parcial[i]) * (fator - i)
        resto = soma % 11
        return 0 if resto < 2 else 11 - resto

    digito1 = calc_digito(cpf[:9], 10)
    digito2 = calc_digito(cpf[:9] + str(digito1), 11)

    return cpf[-2:] == f"{digito1}{digito2}"


def validar_cnpj(cnpj):
    cnpj = re.sub(r'[^\d]', '', cnpj)
    if not re.match(r'^\d{14}$', cnpj):
        return jsonify({"error": "CNPJ deve ter 14 dígitos numéricos"}), 400

    if cnpj == cnpj[0] * 14:
        return jsonify({"error": "CNPJ inválido"}), 400

    def calc_digito(cnpj_parcial, pesos):
        soma = sum(int(cnpj_parcial[i]) * pesos[i] for i in range(len(cnpj_parcial)))
        resto = soma % 11
        return 0 if resto < 2 else 11 - resto

    pesos1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    pesos2 = [6] + pesos1

    digito1 = calc_digito(cnpj[:12], pesos1)
    digito2 = calc_digito(cnpj[:12] + str(digito1), pesos2)

    return cnpj[-2:] == f"{digito1}{digito2}"

def validar_numero_celular(num_celular):
    num_limpo = re.sub(r'[^\d]', '', num_celular)
    
    if len(num_limpo) != 11:
        return jsonify({"error": "Celular deve ter 11 dígitos"}), 400
    
    num_formatado = f"({num_limpo[:2]}) {num_limpo[2:7]}-{num_limpo[7:]}"
    
    if num_limpo[2] != '9':
        return jsonify({"error": "Celular deve começar com 9 após o DDD"}), 400
    
    return True

def validar_numero_fixo(num_fixo):
    num_limpo = re.sub(r'[^\d]', '', num_fixo)
    
    if len(num_limpo) != 10:
        return jsonify({"error": "Telefone fixo deve estar no formato (XX) 1234-5678"}), 400
    
    num_formatado = f"({num_limpo[:2]}) {num_limpo[2:6]}-{num_limpo[6:]}"
    
    return True

def validar_cep(cep):
    cep_limpo = re.sub(r'[^\d]', '', cep)
    
    if len(cep_limpo) != 8:
        return jsonify({"error": "CEP deve ter 8 dígitos"}), 400
    
    cep_formatado = f"{cep_limpo[:5]}-{cep_limpo[5:]}"
    
    return True

def validar_email(email):
    email = email.strip()
    
    if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
        return jsonify({"error": "Email inválido"}), 400

    return True

def validar_senha(senha):
    if len(senha) < 8:
        return jsonify({"error": "Senha deve ter pelo menos 8 caracteres"}), 400
    if not re.search(r'[A-Z]', senha):
        return jsonify({"error": "Senha deve conter ao menos uma letra maiúscula"}), 400
    if not re.search(r'[a-z]', senha):
        return jsonify({"error": "Senha deve conter ao menos uma letra minúscula"}), 400
    if not re.search(r'\d', senha):
        return jsonify({"error": "Senha deve conter ao menos um número"}), 400
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', senha):
        return jsonify({"error": "Senha deve conter ao menos um caractere especial"}), 400
    return True

def validar_nome(nome):
    
    # nome = nome.upper() # Converte para maiúsculas IGNORE
    if not re.match(r'^[A-Za-zÀ-ÖØ-öø-ÿ\s]+$', nome):
        return jsonify({"error": "Nome deve conter apenas letras e espaços"}), 400
    if len(nome) < 2 or len(nome) > 100:
        return jsonify({"error": "Nome deve ter entre 2 e 100 caracteres"}), 400
    return True