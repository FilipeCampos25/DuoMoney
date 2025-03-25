informações sobre o class Usuários


ATENÇÂO: o código atualemente se encontra no formato feito para rodar somente no prompt do python, deve ser
feitas as devidas alterações para inseri-lo ao projeto.


Método inserir_nome
    sera verificado o nome que foi inserido que, se estiver em branco não será aceito e sera pedido para o
    usuario inserir um nome valido

método inserir_email
    sera verificado o email que foi inserido que, se estiver em branco não será aceito e sera pedido para o 
    usuario insira um email valido, ou caso não aja dominio sera pedido para reinserir o email junto com o
    dominio

método definir_senha
    sera verificado a senha inserida que, se estiver em branco não sera aceito e sera pedido para o usuario
    inserir uma senha valida (sera pedido a senha + confirmar a senha), o mesmo vale para caso ambas as se-
    nhas sejam diferentes

método validar_data_nascimento
    sera verificado a data inserida que, se não conter o dia/mes/ano não sera aceito e sera pedido para o 
    usuario inserir uma data valida contendo dia/mes/ano, após a validação essas informações serão guarda-
    das em variáveis próprias para cada elemento antes de entregar a data completa final

método mostrar_dados
    as informações foram guardadas usando "self.__atributo" onde o "__" após o "self." impede de acessar
    qual quer atributo criado no "class Usuario" fora da classe, portanto o unico meio de obter informa-
    ções de itens dentro do class é através deste método.