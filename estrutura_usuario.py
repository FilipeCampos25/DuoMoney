class Usuario:
    def __init__(self, nome, email, senha, data_nascimento):  # declaração dos principais atributos do class
        self.__nome = self.inserir_nome(nome)
        self.__email = self.inserir_email(email)
        self.__senha = self.definir_senha(senha, senha)
        self.__data_nascimento = self.validar_data_nascimento(data_nascimento)

    def inserir_nome(self, nome):
        while True:
            if nome.strip() == '':  # não aceita nome vazio
                print('Seu nome não pode estar vazio')
                nome = input('Digite seu nome: ')  # inserir um novo nome apropriado
            else:
                return nome

    def inserir_email(self, email):
        emails = ['@gmail.com', '@hotmail.com', '@outlook.com']
        while True:
            if email.strip() == '':  # não aceita email vazio
                print('Email não pode estar em branco')
                email = input('Digite seu email: ')
            elif not any(dominio in email for dominio in emails):  # verificar se email possui um dominio
                print('Email inválido! Use @gmail, @hotmail ou @outlook')
                email = input('Digite seu email: ')
            else:
                return email

    def definir_senha(self, senha, confirmar):
        while True:
            if senha.strip() == '' or confirmar.strip() == '':  # não aceita senha em branco
                print('Senha não pode estar em branco')
                senha = input('Digite a senha: ')
                confirmar = input('Confirme a senha: ')
            elif senha == confirmar:  # confirmar se ambas senhas são iguais
                return senha
            else:    # senha e confirmar senha diferentes
                print('senha ou confirmar senha incorretos')
                senha = input('Digite a senha: ')
                confirmar = input('Confirme a senha: ')

    def validar_data_nascimento(self, data_nasc):
        data = data_nasc.split('/')

        if len(data) != 3:  # verificar se possui dia, mes e ano
            while True:
                nova_data = input('escolha uma data valida: ')
                data = nova_data.split('/')
                if len(data) == 3:
                    break

        dia = int(data[0])
        mes = int(data[1])
        ano = int(data[2])

        return f'{dia}/{mes}/{ano}'

    def mostrar_dados(self):
        print('\n')
        print(f"Nome: {self.__nome}")
        print(f'email: {self.__email}')
        print(f"Senha: {self.__senha}")
        print(f"Data de Nascimento: {self.__data_nascimento}")
        print('\n')


# teste padrão
nome = 'nome'
email = 'email@gmail.com'
senha = 'SenhaComNumeros'
data_nasc = '00/00/0000'
user1 = Usuario(nome, email, senha, data_nasc)
Usuario.mostrar_dados(user1)

print('\n^ meio certo ^\nv meio errado v\n')

# teste com erros
nome = ''
email = ''
senha = ''
data_nasc = ''
user2 = Usuario(nome, email, senha, data_nasc)
Usuario.mostrar_dados(user2)
