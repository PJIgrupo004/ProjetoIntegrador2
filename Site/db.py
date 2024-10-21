#Vou reunir tudo que necessitar de conexão ao banco em um arquivo só
from flask import current_app, g
import mysql.connector
import db_connection_data

#Verifica se já tem uma conexão no banco, caso contrário, cria uma nova
def getdb():
    if 'db' not in g or not g.db.is_connected():
        g.db = mysql.connector.connect(
            host=db_connection_data.host,
            user=db_connection_data.db_user,
            password=db_connection_data.db_password,
            database=db_connection_data.db_database
        )
    return g.db

#Função para fechar a conexão após cada solicitação para evitar múltiplas conexões
def close_db(e=None):
    db = g.pop('db', None)

    if db is not None and db.is_connected():
        db.close()

#Traz o ID de todos os usuários
def get_users():
    db = getdb()
    cursor = db.cursor(dictionary=True)
    cursor.execute('select id_usuario from usuarios')
    usuarios = cursor.fetchall()
    cursor.close()
    return usuarios

#Retorna o ID e a senha a partir do nome do usuário
def get_password_user(user_name):
    db = getdb()
    cursor = db.cursor(dictionary=True)
    print('select id_usuario,senha from usuarios where usuario ="'+user_name+'"')
    cursor.execute('select id_usuario,senha from usuarios where usuario ="'+user_name+'"')
    rt = cursor.fetchone()    
    cursor.close()
    return rt

#Retorna o ID e a senha a partir do ID
def get_password_id(id):
    db = getdb()
    cursor = db.cursor(dictionary=True)
    print('select id_usuario,senha from usuarios where id_usuario ='+id)
    cursor.execute('select id_usuario,senha from usuarios where id_usuario ='+id)
    rt = cursor.fetchone()    
    cursor.close()
    return rt

class cliente():
    #Retorna todos os clientes
    def get_clientes():
        db = getdb()
        cursor = db.cursor(dictionary=True)
        cursor.execute('select * from clientes')
        clientes = cursor.fetchall()    
        print(clientes)
        cursor.close()
        return clientes
    
    #Insere um cliente novo na tabela
    def insert_cliente(nome,telefone,data_nascimento, cpf_cnpj, endereco, cep, rua, numero, bairro, cidade, estado, referencia):
        db = getdb()
        cursor = db.cursor(dictionary=True)
        cursor.execute('insert clientes set nome = %s, telefone = %s, data_nascimento = %s, cpf_cnpj = %s, endereco = %s, cep = %s, rua = %s, numero_casa = %s, bairro = %s, cidade = %s, estado = %s, referencia_end = %s', (nome, telefone, data_nascimento, cpf_cnpj, endereco, cep, rua, numero, bairro, cidade, estado, referencia))
        db.commit()  
        cursor.close()
        return 1
    
    def update_cliente(cliente_id, nome, telefone, data_nascimento, cpf_cnpj, endereco, cep, rua, numero, bairro, cidade, estado, referencia):
        db = getdb()
        cursor = db.cursor(dictionary=True)
        cursor.execute('update clientes set nome = %s, telefone = %s, data_nascimento = %s, cpf_cnpj = %s, endereco = %s, cep = %s, rua = %s, numero_casa = %s, bairro = %s, cidade = %s, estado = %s, referencia_end = %s', (nome, telefone, data_nascimento, cpf_cnpj, endereco, cep, rua, numero, bairro, cidade, estado, referencia))
        db.commit()  
        affected_rows = cursor.rowcount
        if affected_rows is not None and affected_rows > 0:
            cursor.close()
            return True
        else:
            return False

    def delete_cliente(cliente_id):
        db = getdb()
        cursor = db.cursor(dictionary=True)
        try:
            cursor.execute('DELETE FROM clientes where id_cliente = %s', (cliente_id,))
            db.commit()
        except Exception as e:
            db.rollback()
            raise e 
        finally:
            cursor.close()

    def get_cliente(cliente_id):
        db = getdb()
        cursor = db.cursor(dictionary=True)
        cursor.execute('select * from clientes where id_cliente = %s', (cliente_id,))
        cliente = cursor.fetchone()    
        print(cliente)
        cursor.close()
        return cliente

class servico():

    def get_servicos():
        db = getdb()
        cursor = db.cursor(dictionary=True)
        cursor.execute('select * from Procedimentos')
        procedimentos = cursor.fetchall()    
        print(procedimentos)
        cursor.close()
        return procedimentos
    
    def insert_servico(nome,descricao):
        db = getdb()
        cursor = db.cursor(dictionary=True)
        cursor.execute('insert Procedimentos set nome = %s, descricao = %s', (nome, descricao))
        db.commit()  
        cursor.close()
        return 1
    
    def update_servico(id_procedimento,nome,descricao):
        db = getdb()
        cursor = db.cursor(dictionary=True)
        cursor.execute('update Procedimentos set nome = %s, descricao = %s WHERE id_procedimento = %s', (nome, descricao, id_procedimento))
        db.commit()
        cursor.close()
        affected_rows = cursor.rowcount
        if affected_rows is not None and affected_rows > 0:
            cursor.close()
            return True
        else:
            return False,

    def delete_servico(work_id):
        db = getdb()
        cursor = db.cursor(dictionary=True)
        try:
            cursor.execute('DELETE FROM Procedimentos WHERE id_procedimento = %s', (work_id,))
            db.commit()
        except Exception as e:
            db.rollback()
            raise e 
        finally:
            cursor.close()

    def get_servico(work_id):
        db = getdb()
        cursor = db.cursor(dictionary=True)
        cursor.execute('select * from Procedimentos where id_procedimento = %s', (work_id,))
        work = cursor.fetchone()    
        print(work)
        cursor.close()
        return work
    
class agendamento():

    def get_agendamentos():
        db = getdb()
        cursor = db.cursor(dictionary=True)
        cursor.execute('select * from agendamentos')
        agendamentos = cursor.fetchall()    
        print(agendamentos)
        cursor.close()
        return agendamentos
    
    def insert_agendamento(id_cliente, id_procedimento, datahora_agendamento, datahora_realizacao, status, descricao_servico, observacoes):
        db = getdb()
        cursor = db.cursor(dictionary=True)
        cursor.execute('insert agendamentos set id_cliente = %s, id_procedimento = %s, datahora_agendamento = %s, datahora_realizacao = %s, status = %s, descricao_servico = %s, observacoes = %s ', (id_cliente, id_procedimento, datahora_agendamento, datahora_realizacao, status, descricao_servico, observacoes))
        db.commit()
        cursor.close()
        return 1
    
    def update_agendamento(id_agendamento, id_cliente, id_procedimento, datahora_agendamento, datahora_realizacao, status, descricao_servico, observacoes):
        db = getdb()
        cursor = db.cursor(dictionary=True)
        cursor.execute('update agendamentos set id_cliente = %s, id_procedimento = %s, datahora_agendamento = %s,datahora_realizacao = %s, status = %s, descricao_servico = %s, observacoes = %s WHERE id_agendamento = %s', (id_cliente,id_procedimento,datahora_agendamento,datahora_realizacao,status,descricao_servico,observacoes, id_agendamento))
        db.commit()
        cursor.close()
        affected_rows = cursor.rowcount
        if affected_rows is not None and affected_rows > 0:
            cursor.close()
            return True
        else:
            return False

    def delete_agendamento(schedule_id):
        db = getdb()
        cursor = db.cursor(dictionary=True)
        try:
            cursor.execute('DELETE FROM agendamentos WHERE id_agendamento = %s', (schedule_id,))
            db.commit()
        except Exception as e:
            db.rollback()
            raise e 
        finally:
            cursor.close()

    def get_agendamento(schedule_id):
        db = getdb()
        cursor = db.cursor(dictionary=True)
        cursor.execute('select * from agendamentos where id_agendamento = %s', (schedule_id,))
        schedule = cursor.fetchone()    
        print(schedule)
        cursor.close()
        return schedule