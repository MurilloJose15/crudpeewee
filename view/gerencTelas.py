from kivy.properties import ObjectProperty, StringProperty, NumericProperty
from kivy.uix.screenmanager import Screen, ScreenManager

from telaDepartamento import ViewDepartamento
from telaProjeto import ViewProjeto


class TelaInicial(Screen):
    pass


class CadastroDepartamento(Screen):
    lbl_id_depart: ObjectProperty(None)
    txi_nome: ObjectProperty(None)
    bt_cad_atual: ObjectProperty(None)


class ListarDepartamentos(Screen):
    id_depart: ObjectProperty(None)
    col_id: ObjectProperty(None)
    col_nome: ObjectProperty(None)
    grid_lista: ObjectProperty(None)


class CadastroProjeto(Screen):
    lbl_id: NumericProperty()
    txi_nome: StringProperty()
    txi_temp: StringProperty()
    sp_depart: ObjectProperty()


class ListarProjetos(Screen):
    chk_pesq_id: ObjectProperty()
    chk_pesq_nome: ObjectProperty()
    txi_pesq_id: StringProperty()
    txi_pesq_nome: StringProperty()
    gl_pesquisa_id: ObjectProperty()
    gl_pesquisa_nome: ObjectProperty()
    layout_pesq_id: ObjectProperty()
    layout_pesq_nome: ObjectProperty()
    layout_lista_projetos: ObjectProperty()
    pesq: ObjectProperty()


class GerenciaTelas(ScreenManager):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._tela_depart = ViewDepartamento(self)
        self._tela_projeto = ViewProjeto(self)

    def tela_inicial(self):
        self.current = "TelaInicial"

    def tela_cadastro_depart(self, id=None, botao=None):
        self.current = 'CadastroDepartamento'
        self._tela_depart.montarTelaAt(id, botao)

    def tela_listar_departs(self):
        self.current = "ListarDepartamentos"
        self._tela_depart._limpar_tela_listar()

    def tela_cadastro_projeto(self, id="", botao='None'):
        self.current = "CadastroProjeto"
        self._tela_projeto.montar_tela_at(id, botao)

    def tela_listar_projetos(self):
        self._tela_projeto.alternar_pesq("id")
        self.current = "ListarProjetos"
        self._tela_projeto._limpar_tela_listar()

    def cadastrar_atualizar(self):
        self._tela_depart.cad_atual_depart()

    def cadastrar_atualizar_projeto(self):
        self._tela_projeto.cad_atual_projeto()

    def buscar_departs(self):
        self._tela_depart.busca_departs()

    def buscar_projetos(self):
        self._tela_projeto.busca_projetos()

    def buscar_projetos_nome(self, nome=""):
        self._tela_projeto.busca_projetos(nome)
