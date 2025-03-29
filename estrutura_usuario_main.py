class CarteiraVirtual:
    def __init__(self):
        self.saldo = 0  # Saldo em moedas, que também representa os pontos

    def receita(self, quantidade):
        if quantidade < 0:
            return 'A quantidade ganha deve ser positiva.'
        else:
            self.saldo += quantidade
            return f'Operação realizada com sucesso, foram depositados R$:{quantidade} ao seu saldo.'

    def despesa(self, quantidade):
        if quantidade < 0:
            return 'A quantidade gasta deve ser positiva.'
        elif quantidade > self.saldo:
            return 'Saldo insuficiente.'
        else:
            self.saldo -= quantidade
            return f'Operação realizada com sucesso, foram retirados R$:{quantidade} do seu saldo.'

    def consultar_saldo(self):
        return f'Saldo atual: R$:{self.saldo}.'

    @property
    def pontos(self):
        return self.saldo  # O saldo agora também é a pontuação


class Progresso:
    def __init__(self, id_progresso: int, id_licao: int, status_progresso: str = "iniciado", pontos_ganho: int = 0):
        self.id_progresso = id_progresso
        self.id_licao = id_licao
        self.status_progresso = status_progresso  # ex: "iniciado", "concluído"
        self.pontos_ganho = pontos_ganho  # Armazena os pontos ganhos nesta lição específica

    def atualizar_status(self, novo_status: str):
        self.status_progresso = novo_status

    def adicionar_pontos(self, pontos: int):
        if pontos < 0:
            raise "Pontos devem ser positivos"
        self.pontos_ganho += pontos

    def to_dict(self):
        return {
            "id_progresso": self.id_progresso,
            "id_licao": self.id_licao,
            "status_progresso": self.status_progresso,
            "pontos_ganho": self.pontos_ganho
        }


class Usuario:
    def __init__(self, nome, email, senha, data_nascimento):
        self.__nome = self.inserir_nome(nome)
        self.__email = self.inserir_email(email)
        self.__senha = self.definir_senha(senha)
        self.__data_nascimento = self.validar_data_nascimento(data_nascimento)
        self.__carteira = CarteiraVirtual()  # Carteira agora gerencia saldo e pontos
        self.__progressos = []  # Lista de objetos Progresso

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
            "data_nascimento": self.__data_nascimento,
            "progressos": [progresso.to_dict() for progresso in self.__progressos]
        }

    def mostrar_dados(self):
        print('\n')
        print(f"Nome: {self.__nome}")
        print(f"email: {self.__email}")
        print(f"Data de Nascimento: {self.__data_nascimento}")
        print(f"Saldo da Carteira: {self.__carteira.consultar_saldo()}")
        print(f"Pontuação Total: {self.__carteira.pontos}")
        print("Progressos:")
        for progresso in self.__progressos:
            print(f"  Lição {progresso.id_licao}: {progresso.status_progresso} - {progresso.pontos_ganho} pontos")
        print('\n')

    # Métodos para interagir com a carteira do usuário
    def adicionar_moedas(self, quantidade):
        return self.__carteira.receita(quantidade)

    def retirar_moedas(self, quantidade):
        return self.__carteira.despesa(quantidade)

    def ver_saldo(self):
        return self.__carteira.consultar_saldo()
