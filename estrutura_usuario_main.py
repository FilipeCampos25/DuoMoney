class CarteiraVirtual:
    def __init__(self):
        self.__saldo = 0

    def receita(self, quantidade):
        if quantidade < 0:
            return 'a quantidade ganha deve ser positiva.'
        else:
            self.__saldo += quantidade
            return f'operação realizada com sucesso, foram depositado R$:{quantidade} ao seu saldo.'

    def despesa(self, quantidade):
        if quantidade < 0:
            return 'a quantidade gasta deve ser positiva.'
        elif quantidade > self.__saldo:
            return 'saldo insuficiente.'
        else:
            self.__saldo -= quantidade
            return f'operação realizada com sucesso, foram retirados R$:{quantidade} do seu saldo.'

    def consultar_saldo(self):
        return f'saldo atual: R$:{self.__saldo}.'


class Pontuacao:
    def __init__(self, pontos=0):
        self.pontos = pontos

    def ganhar_pontos(self, quantidade):
        if quantidade < 0:
            raise "quantidade deve ser positiva"
        self.pontos += quantidade

    def perder_pontos(self, quantidade):
        if quantidade < 0:
            raise "quantidade deve ser positiva"
        self.pontos -= quantidade
        if self.pontos < 0:
            self.pontos = 0


class Usuario:
    def _init_(self, nome, email, senha, data_nascimento):
        self.__nome = self.inserir_nome(nome)
        self.__email = self.inserir_email(email)
        self.__senha = self.definir_senha(senha)
        self.__data_nascimento = self.validar_data_nascimento(data_nascimento)
        # ligando usuario com carteira virtual
        self.__carteira = CarteiraVirtual()
        # ligando usuário com pontuação
        self.pontuacao = Pontuacao()

    def inserir_nome(self, nome):
        if not nome or nome.strip() == '':
            raise ValueError("Nome não pode estar vazio")
        return nome.strip()

    def inserir_email(self, email):
        valid_domains = ['@gmail.com', '@hotmail.com', '@outlook.com']
        if not email or email.strip() == '':
            raise ValueError("Email não pode estar vazio")
        if not any(domain in email for domain in valid_domains):
            raise ValueError("Email inválido! Use @gmail, @hotmail ou @outlook")
        return email.strip()

    def definir_senha(self, senha):
        if not senha or senha.strip() == '':
            raise ValueError("Senha não pode estar vazia")
        return senha.strip()

    def validar_data_nascimento(self, data_nasc):
        try:
            from datetime import datetime
            data = datetime.strptime(data_nasc, '%Y-%m-%d')
            return data.strftime('%d/%m/%Y')
        except ValueError:
            raise ValueError("Data de nascimento inválida. Use o formato YYYY-MM-DD")

    @property
    def nome(self):
        return self.__nome

    @property
    def email(self):
        return self.__email

    @property
    def senha(self):
        return self.__senha

    @property
    def data_nascimento(self):
        return self.__data_nascimento

    def to_dict(self):
        return {
            "nome": self.__nome,
            "email": self.__email,
            "senha": self.__senha,
            "data_nascimento": self.__data_nascimento
        }

    def mostrar_dados(self):
        print('\n')
        print(f"Nome: {self.__nome}")
        print(f'email: {self.__email}')
        print(f"Senha: {self.__senha}")
        print(f"Data de Nascimento: {self.__data_nascimento}")
        print('\n')

    # métodos para interagir com carteira do usuario
    def adicionar_moedas(self, quantidade):
        return self.__carteira.receita(quantidade)

    def retirar_moedas(self, quantidade):
        return self.__carteira.despesa(quantidade)

    def ver_saldo(self):
        return self.__carteira.consultar_saldo()

    # métodos para interagir com pontuação do usuario
    def ganhar_pontos(self, quatidade):
        return self.pontuacao.ganhar_pontos(quatidade)

    def perder_pontos(self, quantidade):
        return self.pontuacao.perder_pontos(quantidade)