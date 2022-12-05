import peewee
from playhouse.mysql_ext import MySQLConnectorDatabase


class BaseModel(peewee.Model):

    def __init__(self, *args, **kwargs):
        try:
            self.create_table()
        except peewee.OperationalError as erro:
            print(erro)
        super().__init__(*args, **kwargs)


    class Meta:
        database = MySQLConnectorDatabase(
            'companhia',
            user='root',
            password='',
            host='localhost',
            port=3306,
            charset='utf8mb4')


class Departamento(BaseModel):
    nome = peewee.CharField(max_length=100, unique=True)


class Projeto(BaseModel):
    nome = peewee.CharField(max_length=100, unique=True)
    tempo_estimado = peewee.DateField()
    fk_departamento = peewee.ForeignKeyField(Departamento, related_name='departamento')


class Funcionario(BaseModel):
    nome = peewee.CharField(max_length=100)
    endereco = peewee.CharField(max_length=200)
    sexo = peewee.CharField(max_length=1)
    data_nasc = peewee.DateField()
    salario = peewee.DecimalField(max_digits=12, decimal_places=2)
    fk_departamento = peewee.ForeignKeyField(Departamento, related_name='departamento')
    fk_projeto = peewee.ForeignKeyField(Projeto, related_name='projeto')


class Pesquisador(BaseModel):
    fk_funcionario = peewee.ForeignKeyField(Funcionario, related_name='funcionario')
    area_atuacao = peewee.CharField(max_length=100)
    horas_semanais = peewee.TimeField()


class Secretario(BaseModel):
    fk_funcionario = peewee.ForeignKeyField(Funcionario, related_name='funcionario')
    grau_escolar = peewee.CharField(max_length=50)


class Limpeza(BaseModel):
    fk_funcionario = peewee.ForeignKeyField(Funcionario, related_name='funcionario')
    jornada_trabalho = peewee.TimeField()
    cargo_nivel = peewee.CharField(max_length=20, default='padrao')


class Dependente(BaseModel):
    fk_funcionario = peewee.ForeignKeyField(Funcionario, related_name='funcionario')
    nome = peewee.CharField(max_length=100)
    sexo = peewee.CharField(max_length=1)
    data_nasc = peewee.DateField()
    parentesco = peewee.CharField(max_length=20)

