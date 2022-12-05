from kivy.uix.button import Button
from kivy.uix.label import Label

from model.models import Departamento

class DepartamentoCtrl:

    def __init__(self):
        self._lista = []

    def sv_atu_departamento(self, nome, id=None):
        try:
            if id:
                departamento = Departamento.get_by_id(id)
                departamento.nome = nome
            else:
                departamento = Departamento(nome=nome)
            departamento.save()
            return "Operação realizada com sucesso!"
        except Exception as e:
            print(e)
            return "Não foi possível realizar a operação!"

    def del_departamento(self, id):
        try:
            departamento = Departamento.get_by_id(id)
            departamento.delete_instance()
            return "Departamento excluído com sucesso!"
        except Exception as e:
            print(e)
            return "Não foi possível excluir o Departamento"

    def buscar_por_id(self, id):
        self._lista = []
        try:
            departamento = Departamento.get_by_id(id)
            self._lista.append(self._montar_depart(departamento.id, departamento.nome))
            return self._lista
        except:
            return None

    def buscar_por_nome(self, nome):
        self._lista = []
        try:
            departamento = Departamento.get(nome=nome)
            self._lista.append(self._montar_depart(departamento.id, departamento.nome))
            return self._lista
        except:
            return self._lista

    def buscar_todos(self):
        try:
            ds = Departamento.select()
            for d in ds:
                self._lista.append(self._montar_depart(d.id, d.nome))
            return self._lista
        except:
            return None

    def _montar_depart(self, id, nome):
        meudepart = {
            'lblId': self._criarLabel(id, 0.2),
            'lblNome': self._criarLabel(nome, 0.4),
            'btAtualizar': self._criarBotao("Atualizar"),
            'btExcluir': self._criarBotao("Excluir")
        }
        return meudepart

    def _criarLabel(self, texto, tam):
        label = Label()
        label.text = str(texto)
        label.size_hint_y = None
        label.size_hint_x = tam
        label.height = '30dp'
        return label

    def _criarBotao(self, texto):
        botao = Button(text=texto,
                       font_size='10sp',
                       size_hint_y = None,
                       height= '30dp',
                       size_hint_x = .1)
        return botao
