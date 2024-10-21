from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import LoginManager, UserMixin, login_required, current_user, login_user, logout_user
from dotenv import load_dotenv
from datetime import datetime
import importlib
import os
import db


app = Flask(__name__)
app.secret_key = 'chave'
app.app_context().push()
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
db.getdb()

# Carregar variáveis do arquivo .env_local
load_dotenv(dotenv_path='.env_local')

def load_strings(module_access,module_name):
    if module_access == '':
        module = importlib.import_module(f"static.strings.{module_name}_strings")
    else:
        module = importlib.import_module(f"static.strings.{module_access}.{module_name}_strings")
    return module.STRINGS

status = load_strings('','status')
nav_strings = load_strings('adm','dashboard')

class User(UserMixin):

    def __init__(self, username, password):
        self.id = username
        self.password = password

    def is_active(self):
        return True

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

@login_manager.user_loader
def load_user(user_id):
    usuario = db.get_password_user(user_id)
    return User(usuario['id_usuario'],usuario['senha'])


#Tela inicial
@app.route("/")
def homepage():
    strings = load_strings('landpage','home')
    phone_number = os.getenv('PHONE_NUMBER')
    return render_template("/landpage/jinja_home.html", strings=strings, phone_number=phone_number)

#Lista de agendamentos
@app.route("/agendamento")
def agendamento():
    return render_template("/landpage/jinja_agendamento.html")

#Tela de login
@app.route("/login", methods=['GET', 'POST'])
def login():
    strings = load_strings('landpage','login')
    if current_user.is_authenticated:
         return redirect(url_for('dashboard'))
    else:
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            ret = db.get_password_user(username)
            if ret != None:
                user = User(username,password)
                if user.password == password:
                    login_user(user)
                    return redirect(url_for('dashboard'))
            else:
                flash(status['user_not_found'], 'danger')
                return redirect(url_for('login'))
        
        return render_template('/landpage/jinja_login.html', strings=strings)

#Tela principal do administrador
@app.route("/dashboard")
@login_required
def dashboard():
    strings = load_strings('adm','dashboard')
    return render_template("/adm/jinja_dashboard.html",nav_strings=strings, strings=strings)

#Tela Clientes Cadastrados
@app.route("/clientes")
@login_required
def clientes_cadastrados():
    strings = load_strings('adm','clients')
    return render_template("/adm/Client/jinja_clients_list.html",clientes=db.cliente.get_clientes(), strings=strings, nav_strings=nav_strings)

#Tela Cadastro de Clientes
@app.route("/clientes/cadastro", methods=['GET','POST'])
@login_required
def cadastro_cliente():
    strings = load_strings('adm','register_client')
    if request.method == 'POST':
        nome = request.form['nome']
        telefone = request.form['telefone']
        data_nascimento = request.form['data_nascimento'] if request.form['data_nascimento'] != '' else "null"
        cpf_cnpj = request.form['cpf_cnpj']
        cep = request.form['cep'].replace('.', '').replace('-', '')
        rua = request.form['rua']
        numero = request.form['numero']
        bairro = request.form['bairro']
        cidade = request.form['cidade']
        estado = request.form['estado']
        referencia = request.form['referencia'] if request.form['referencia'] != '' else "null"
        endereco = "${rua},${numero},${bairro},${cidade},${estado}"
        retorno = db.cliente.insert_cliente(nome, telefone ,data_nascimento, cpf_cnpj, endereco, cep, rua, numero, bairro, cidade, estado, referencia)
        if retorno != None:
            flash( status['success_register_user'], 'success')
            return redirect(url_for('clientes_cadastrados'))
    return render_template("/adm/Client/jinja_client_register.html", nav_strings=nav_strings, strings=strings, cliente=None)

#Rota de deleção de Clientes
@app.route("/clientes/<int:cliente_id>", methods=['GET', 'DELETE', 'POST'])
@login_required
def delete_cliente(cliente_id):
    strings = load_strings('adm','register_client')
    if request.method == 'DELETE':
        try:
            db.cliente.delete_cliente(cliente_id)
            flash(status['success_delete_user'], 'success')
            return jsonify({"success": True}), 200
        except Exception as e:
            flash(status['error_delete_user'], 'danger')
            return jsonify({"error": str(e)}), 400
    if request.method == 'GET':
         return render_template("/adm/Client/jinja_client_register.html", nav_strings=nav_strings, strings=strings,cliente=db.cliente.get_cliente(cliente_id))
    if request.method == 'POST':
        nome = request.form['nome']
        cpf_cnpj = request.form['cpf_cnpj']
        telefone = request.form['telefone']
        data_nascimento = request.form['data_nascimento'] if request.form['data_nascimento'] != "" else "null"
        cep = request.form['cep'].replace('.', '').replace('-', '')
        rua = request.form['rua']
        numero = request.form['numero']
        bairro = request.form['bairro']
        cidade = request.form['cidade']
        estado = request.form['estado']
        referencia = request.form['referencia'] if request.form['referencia'] != '' else "null"
        endereco = "${rua},${numero},${bairro},${cidade},${estado}"
        retorno = db.cliente.update_cliente(cliente_id, nome, telefone, data_nascimento, cpf_cnpj, endereco, cep, rua, numero, bairro, cidade, estado, referencia)
        if retorno != None:
            flash( status['success_edit_user'], 'success')
            return redirect(url_for('clientes_cadastrados'))
        else:
            flash( status['error_edit_user'], 'success')


#Tela Serviços Cadastrados
@app.route("/serviços")
@login_required
def servicos_cadastrados():
    strings = load_strings('adm','works')
    return render_template("/adm/Work/jinja_works_list.html",works=db.servico.get_servicos(), strings=strings, nav_strings=nav_strings)

#Tela Cadastro de Serviços
@app.route("/serviços/cadastro", methods=['GET','POST'])
@login_required
def cadastro_servico():
    strings = load_strings('adm','register_work')
    if request.method == 'POST':
        # Informações do serviço
        nome = request.form['nome']
        descricao = request.form['descricao']
        retorno = db.servico.insert_servico(nome, descricao)
        if retorno != None:
            flash( status['success_register_work'], 'success')
            return redirect(url_for('cadastro_servico'))
    return render_template("/adm/Work/jinja_work_register.html", nav_strings=nav_strings, strings=strings, work=None)  

#Rota de deleção de Serviços
@app.route("/serviços/<int:service_id>", methods=['GET', 'DELETE', 'POST'])
@login_required
def delete_service(service_id):
    strings = load_strings('adm','register_work')
    if request.method == 'DELETE':
        try:
            db.servico.delete_servico(service_id)
            flash(status['success_delete_work'], 'success')
            return jsonify({"success": True}), 200
        except Exception as e:
            flash(status['error_delete_work'], 'danger')
            return jsonify({"error": str(e)}), 400
    if request.method == 'GET':
         return render_template("/adm/Work/jinja_work_register.html", nav_strings=nav_strings, strings=strings,work=db.servico.get_servico(service_id))
    if request.method == 'POST':
        # Informações do serviço
        nome = request.form['nome']
        descricao = request.form['descricao']
        retorno = db.servico.update_servico(service_id, nome, descricao)
        if retorno != None:
            flash( status['success_edit_work'], 'success')
            return redirect(url_for('servicos_cadastrados'))
        else:
            flash( status['error_edit_work'], 'success')

#Tela Agendamentos Cadastrados
@app.route("/agendamentos")
@login_required
def agendamentos_cadastrados():
    strings = load_strings('adm','schedulings')
    schedulings = db.agendamento.get_agendamentos()

    clientes = db.cliente.get_clientes() 
    servicos = db.servico.get_servicos()

    clientes_dict = {cliente['id_cliente']: cliente['nome'] for cliente in clientes}
    servicos_dict = {servico['id_procedimento']: servico['nome'] for servico in servicos}

    for scheduling in schedulings:
        scheduling['cliente_nome'] = clientes_dict.get(scheduling['id_cliente'], '')
        scheduling['servico_nome'] = servicos_dict.get(scheduling['id_procedimento'], '')
        scheduling['hora_formatada'] = scheduling['datahora_realizacao'].strftime('%H:%M')
   
    return render_template("/adm/Schedule/jinja_schedules_list.html",schedulings=schedulings, strings=strings, nav_strings=nav_strings)

#Tela Cadastro de Agendamentos
@app.route("/agendamentos/cadastro", methods=['GET','POST'])
@login_required
def cadastro_agendamento():
    strings = load_strings('adm','register_schedule')
    if request.method == 'GET':
        schedule = {'servicos': [], 'clientes': []}
        schedule['servicos'] = db.servico.get_servicos()
        schedule['clientes'] = db.cliente.get_clientes()
        schedule['servico'] = ''
        schedule['cliente'] = ''
        schedule['status_list'] = ['Pendente', 'Confirmado', 'Realizado', 'Cancelado']
    if request.method == 'POST':
        # Informações do agendamento
        cliente = int(request.form.get('cliente_select'))
        servico = int(request.form.get('servico_select'))
        status_select = request.form.get('status_select')
        datahora_agendamento = request.form['datahora_agendamento']
        datahora_realizacao = request.form['datahora_realizacao'] if request.form['datahora_realizacao'] != '' else "null"
        descricao_servico = request.form['descricao_servico'] if request.form['descricao_servico'] != '' else "null"
        observacoes = request.form['observacoes'] if request.form['observacoes'] != '' else "null"
        retorno = db.agendamento.insert_agendamento(cliente, servico, datahora_agendamento, datahora_realizacao, status_select, descricao_servico, observacoes)
        if retorno != None:
            flash(status['success_register_schedule'], 'success')
            return redirect(url_for('cadastro_agendamento'))
    return render_template("/adm/Schedule/jinja_schedule_register.html", nav_strings=nav_strings, strings=strings, schedule=schedule) 

#Rota de deleção de Agendamentos
@app.route("/agendamentos/<int:schedule_id>", methods=['GET', 'POST', 'DELETE'])
@login_required
def delete_schedule(schedule_id):
    strings = load_strings('adm','register_schedule')
    if request.method == 'DELETE':
        try:
            db.agendamento.delete_agendamento(schedule_id)
            flash(status['success_delete_schedule'], 'success')
            return jsonify({"success": True}), 200
        except Exception as e:
            flash(status['error_delete_schedule'], 'danger')
            return jsonify({"error": str(e)}), 400
    if request.method == 'GET':
        schedule = db.agendamento.get_agendamento(schedule_id)
        schedule['servicos'] = schedule.get('servicos', db.servico.get_servicos())
        schedule['clientes'] = schedule.get('clientes', db.cliente.get_clientes())
        schedule['status_list'] = ['Pendente', 'Confirmado', 'Realizado', 'Cancelado']
        schedule['servico'] = [servico for servico in schedule['servicos'] if servico['id_procedimento'] == schedule['id_procedimento']][0]
        schedule['cliente'] = [cliente for cliente in schedule['clientes'] if cliente['id_cliente'] == schedule['id_cliente']][0]
        return render_template("/adm/Schedule/jinja_schedule_register.html", nav_strings=nav_strings, strings=strings,schedule=schedule)
    if request.method == 'POST':
        # Informações do agendamento
        cliente = int(request.form.get('cliente_select') if request.form.get('cliente_select') else request.form['cliente_id'])
        servico = int(request.form.get('servico_select') if request.form.get('servico_select') else request.form['servico_id'])
        status_select = request.form.get('status_select') if request.form.get('status_select') else request.form['status_not_changed']
        datahora_agendamento = request.form['datahora_agendamento']
        datahora_realizacao = request.form['datahora_realizacao'] if request.form['datahora_realizacao'] != '' else "null"
        descricao_servico = request.form['descricao_servico'] if request.form['descricao_servico'] != '' else "null"
        observacoes = request.form['observacoes'] if request.form['observacoes'] != '' else "null"
        retorno = db.agendamento.update_agendamento(schedule_id,cliente, servico, datahora_agendamento, datahora_realizacao, status_select, descricao_servico, observacoes)
        if retorno != None:
            flash( status['success_edit_schedule'], 'success')
            return redirect(url_for('agendamentos_cadastrados'))
        else:
            flash( status['error_edit_schedule'], 'success')

# Rota de logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('homepage'))

if __name__ == '__main__':
    app.run(debug=True)

