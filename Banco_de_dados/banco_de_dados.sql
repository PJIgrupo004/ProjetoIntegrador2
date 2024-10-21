-- Remove qualquer tabela prévia
DROP TABLE IF EXISTS Agendamentos;
DROP TABLE IF EXISTS clientes;
DROP TABLE IF EXISTS Procedimentos;

-- Tabela Clientes
CREATE TABLE clientes (
  `id_cliente` int NOT NULL AUTO_INCREMENT,
  `nome` varchar(255) DEFAULT NULL,
  `telefone` varchar(20) DEFAULT NULL,
  `data_nascimento` date DEFAULT NULL,
  `cpf_cnpj` varchar(20) DEFAULT NULL,
  `endereco` varchar(255) DEFAULT NULL,
  `rua` varchar(255) DEFAULT NULL,
  `bairro` varchar(255) DEFAULT NULL,
  `cidade` varchar(255) DEFAULT NULL,
  `estado` varchar(255) DEFAULT NULL,
  `numero_casa` varchar(255) DEFAULT NULL,
  `referencia_end` varchar(255) DEFAULT NULL,
  `cep` varchar(8) DEFAULT NULL,
  PRIMARY KEY (`id_cliente`)
);


-- Tabela Usuários
CREATE TABLE IF NOT EXISTS usuarios (
  id_usuario INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  usuario VARCHAR(255) NULL,
  senha VARCHAR(45) NULL
);

-- Tabela Procedimentos
CREATE TABLE Procedimentos (
	id_procedimento INT AUTO_INCREMENT PRIMARY KEY,
  nome TEXT,
  descricao TEXT
);

-- Tabela Agendamentos
CREATE TABLE Agendamentos (
    id_agendamento INT AUTO_INCREMENT PRIMARY KEY,
    id_cliente INT,
    id_procedimento INT,
    datahora_agendamento DATETIME,
    datahora_realizacao DATETIME,
    descricao_servico TEXT,
    status ENUM('pendente', 'confirmado', 'realizado', 'cancelado'),
    observacoes TEXT,
    FOREIGN KEY (id_cliente) REFERENCES Clientes(id_cliente),
    FOREIGN KEY (id_procedimento) REFERENCES Procedimentos(id_procedimento)
);