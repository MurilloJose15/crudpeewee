from functools import partial

from kivy.uix.label import Label
from kivy.uix.popup import Popup

from controller.projetoctrl import ProjetoCtrl
#from controller.utils import Util


class ViewProjeto:

    def __init__(self, gerenc_tela):
        self._gt = gerenc_tela
        self._telacad = self._gt.get_screen("CadastroProjeto")
        self._telalistar = self._gt.get_screen("ListarProjetos")

    def cad_atual_projeto(self):
        control = ProjetoCtrl()
        try:
            id_projeto = self._telacad.lblId.text
            nome_projeto = self._telacad.txi_nome.text
            tempo_est = self._telacad.txi_temp.text
            depart = self._telacad.sp_depart.text
            if self._telacad.bt_cad_atual.text == "Excluir":
                result = control.excluir_projeto(id_projeto)
                self.busca_projetos()
                self._gt.current = "ListarProjetos"
            else:
                result = control.salvar_atualizar_projeto(id=id_projeto,
                                                          nome=nome_projeto,
                                                          tempo_estimado=tempo_est,
                                                          depart=depart)
            self._popJanela(result)
            self._limpar_tela()
            self._telacad.txi_nome.focus = True
        except Exception as e:
            print(str(e))
            self._popJanela(f"Não foi possível {self._telacad.bt_cad_atual.text} o projeto!")

    def _limpar_tela_listar(self):
        self._telalistar.txi_pesq_id.text = ""
        self._telalistar.txi_pesq_nome.text = ""
        cabecalho = [
            self._telalistar.ids.col_id,
            self._telalistar.ids.col_nome,
            self._telalistar.ids.col_temp_projeto,
            self._telalistar.ids.col_depart,
            self._telalistar.ids.lbl_atual,
            self._telalistar.ids.lbl_excluir
        ]
        self._telalistar.layout_lista_projetos.clear_widgets()
        for c in cabecalho:
            self._telalistar.layout_lista_projetos.add_widget(c)

    def busca_projetos(self, nome=""):
        try:
            control = ProjetoCtrl()
            id_pesq = self._telalistar.txi_pesq_id.text
            resultado = control.buscar_projeto(id=id_pesq, nome=nome)
            self._limpar_tela_listar()
            for res in resultado:
                res['btAtualizar'].bind(on_release=partial(self._gt.tela_cadastro_projeto, res['lblId'].text))
                res['btExcluir'].bind(on_release=partial(self._gt.tela_cadastro_projeto, res['lblId'].text))
                self._telalistar.layout_lista_projetos.add_widget(res['lblId'])
                self._telalistar.layout_lista_projetos.add_widget(res['lblNome'])
                self._telalistar.layout_lista_projetos.add_widget(res['lblTemp'])
                self._telalistar.layout_lista_projetos.add_widget(res['lblDepart'])
                self._telalistar.layout_lista_projetos.add_widget(res['btAtualizar'])
                self._telalistar.layout_lista_projetos.add_widget(res['btExcluir'])
        except Exception as e:
            print(e)

    def montar_tela_at(self, id_projeto="", botao=None):
        control = ProjetoCtrl()
        self._montar_spinner()
        projetos = []
        if id_projeto:
            projetos = control.buscar_projeto(id=id_projeto)
        if projetos:
            for p in projetos:
                self._telacad.lblId.text = p["lblId"].text
                self._telacad.txi_nome.text = p["lblNome"].text
                self._telacad.txi_temp.text = p["lblTemp"].text
                self._telacad.sp_depart.text = p["lblDepart"].text
                self._telacad.bt_cad_atual.text = botao.text

    def _montar_spinner(self):
        lista_valores = self._buscar_departs_tela()
        self._telacad.sp_depart.values = lista_valores

    def _buscar_departs_tela(self):
        control = ProjetoCtrl()
        departs = control.buscarDeparts()
        nomesDeparts = []
        for depart in departs:
            nomesDeparts.append(depart['nome'])
        return tuple(nomesDeparts)

    def _limpar_tela(self):
        self._telacad.lblId.text = ""
        self._telacad.txi_nome.text = ""
        self._telacad.txi_temp.text = ""
        self._telacad.sp_depart.text = "Selecione..."
        self._telacad.bt_cad_atual.text = "Cadastrar"

    def _popJanela(self, texto=""):
        popup = Popup(title='Informação', content=Label(text=texto), auto_dismiss=True)
        popup.size_hint = (0.98, 0.4)
        popup.open()

    def alternar_pesq(self, tipo):
        if self._telalistar.txi_pesq_id:
            self._telalistar.txi_pesq_id.text = ""
        if self._telalistar.txi_pesq_nome:
            self._telalistar.txi_pesq_nome.text = ""
        pesqNome = self._telalistar.gl_pesquisa_nome
        pesqId = self._telalistar.gl_pesquisa_id
        self._telalistar.pesq.remove_widget(pesqNome)
        self._telalistar.pesq.remove_widget(pesqId)
        if tipo == "id":
            pesqId.active = True
            pesqNome.active = False
            self._telalistar.pesq.add_widget(pesqId, 2)
        elif tipo == "nome":
            pesqNome.active = True
            pesqId.active = False
            self._telalistar.pesq.add_widget(pesqNome,2)
