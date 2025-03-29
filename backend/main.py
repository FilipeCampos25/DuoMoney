from funcoes import Email_sender, objeto, vincular
import mysql.connector
import pandas as pd
from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime
import hashlib
import os
import logging


""" Cadastro/Login """


# Configuração do Flask
cadastro = Flask(__name__, template_folder='../frontend')
cadastro.secret_key = 'herekinkajou613'

# Configuração de logging para depuração
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Configuração do banco de dados
db_config = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': 'lipe250505',
    'database': 'projeto_pi',
    'port': 3306
}

# Função para conectar ao banco de dados
def get_db_connection():
    try:
        conn = mysql.connector.connect(**db_config)
        if conn.is_connected():
            logging.info("Conexão ao banco de dados estabelecida com sucesso.")
        return conn
    except mysql.connector.Error as err:
        logging.error(f"Erro ao conectar ao banco de dados: {err}")
        return None

# Função para hash da senha
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Inicialização do banco de dados
def init_db():
    conn = get_db_connection()
    if conn is None:
        logging.error("Não foi possível inicializar o banco de dados.")
        return
    
    try:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id_usuario INT AUTO_INCREMENT PRIMARY KEY,
                nome VARCHAR(255) NOT NULL UNIQUE,
                idade INT,
                email VARCHAR(255),
                senha VARCHAR(255) NOT NULL,
                data_criacao DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        logging.info("Tabela 'usuarios' verificada/criada com sucesso.")
    except mysql.connector.Error as err:
        logging.error(f"Erro ao criar tabela: {err}")
    finally:
        if 'cursor' in locals():
            cursor.close()
        if conn and conn.is_connected():
            conn.close()
            logging.info("Conexão ao banco de dados fechada após inicialização.")

# Rota principal
@cadastro.route('/')
def index():
    return render_template('cadastro.html')

@cadastro.route('/tela')
def tela():
    return render_template('telaPrincipal.html')

# Rota para processar login e cadastro
@cadastro.route('/submit', methods=['POST'])
def submit():
    conn = get_db_connection()
    if conn is None:
        flash('Erro: Não foi possível conectar ao banco de dados.')
        return redirect(url_for('index'))

    try:
        cursor = conn.cursor()

        # Verifica se é login ou cadastro
        if 'confirm_password' not in request.form:
            # Login
            username = request.form.get('username')
            password = hash_password(request.form.get('password', ''))

            if not username or not password:
                flash('Preencha todos os campos de login.')
                return redirect(url_for('index'))

            cursor.execute('SELECT * FROM usuarios WHERE nome = %s AND senha = %s', (username, password))
            user = cursor.fetchone()

            if user:
                flash('Login realizado com sucesso!')
                logging.info(f"Login bem-sucedido para o usuário: {username}")
                return redirect(url_for('tela'))
            else:
                flash('Usuário ou senha inválidos!')
                logging.warning(f"Tentativa de login falhou para o usuário: {username}")

        else:
            # Cadastro
            username = request.form.get('username')
            email = request.form.get('email')
            password = request.form.get('password')
            confirm_password = request.form.get('confirm_password')
            birth_date = request.form.get('birth_date')
            logging.info(f"Email capturado: {email}")

            # Validação dos campos
            if not all([username, password, confirm_password, birth_date]):
                flash('Preencha todos os campos de cadastro.')
                return redirect(url_for('index'))

            if password != confirm_password:
                flash('As senhas não coincidem!')
                return redirect(url_for('index'))

            # Criação do objeto Usuario com validação
            try:
                usuario = objeto.Usuario(username, email, password, birth_date)
                logging.info(f"Objeto Usuario criado: nome={usuario.nome}, email={usuario.email}, birth_date={birth_date}")
            except ValueError as e:
                flash(str(e))
                print("problema no objeto")
                return redirect(url_for('index'))

            # Calcula idade
            birth = datetime.strptime(birth_date, '%Y-%m-%d')
            today = datetime.now()
            idade = today.year - birth.year - ((today.month, today.day) < (birth.month, birth.day))
            password_hash = hash_password(password)

            # Verifica se o usuário já existe
            cursor.execute('SELECT * FROM usuarios WHERE nome = %s', (username,))
            if cursor.fetchone():
                flash('Usuário já existe!')
                return redirect(url_for('index'))

            # Insere novo usuário no banco
            cursor.execute('''
                INSERT INTO usuarios (nome, idade, email, senha, data_criacao)
                VALUES (%s, %s, %s, %s, %s)
            ''', (usuario.nome, idade, usuario.email, password_hash, datetime.now()))
            
            conn.commit()
            objeto.Usuario(username, email, password, idade) # cria um objeto usuario
            vincular.vinc(email)
            Email_sender.e_mail(usuario.email, usuario.nome) # envia um email confirmando o cadastro


            # inicializa o gamificacao e progresso

            cursor = conn.cursor()
            cursor.execute("SELECT id FROM usuarios WHERE email = %s", (email,))
            result = cursor.fetchone()
            usuario_id = result[0]
            
            cursor.execute('''INSERT INTO gamificacao (id_usuario, tipo, valor, data_criacao) 
                            VALUES (%s, %s, %s, %s)''', 
                        (usuario_id, "moeda", 0, datetime.now()))
            
            cursor.execute('''INSERT INTO progresso (id_usuario, id_licao, status_progresso, pontos_ganhos) 
                            VALUES (%s, %s, %s, %s)''', 
                        (usuario_id, 0, "defalt", 0))
            
            conn.commit()

            # Backup com pandas
            df = pd.read_sql_query("SELECT * FROM usuarios", conn)
            logging.info("Dados da tabela 'usuarios' após cadastro:")
            logging.info(df)

            # Salva backup em CSV no diretório atual
            backup_path = os.path.join(os.getcwd(), 'usuarios_backup.csv')
            df.to_csv(backup_path, index=False)
            logging.info(f"Backup salvo em: {backup_path}")

            flash('Cadastro realizado com sucesso!')

    except mysql.connector.Error as err:
        flash(f'Erro no processamento: {err}')
        logging.error(f"Erro no banco de dados durante submit: {err}")
    except Exception as e:
        flash(f'Ocorreu um erro inesperado: {e}')
        logging.error(f"Erro inesperado: {e}")
    finally:
        if 'cursor' in locals():
            cursor.close()
        if conn and conn.is_connected():
            conn.close()
            logging.info("Conexão ao banco de dados fechada após operação.")

    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    cadastro.run(debug=True, host='127.0.0.1', port=5000)