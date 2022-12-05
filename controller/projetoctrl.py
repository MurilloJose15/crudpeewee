from kivy.uix.button import Button
from kivy.uix.label import Label
from peewee import ModelSelect

from controller.utils import Util
from model.models import Projeto, Departamento


class ProjetoCtrl:

    def salvar_atualizar_projeto(self, id=None, nome=None, tempo_estimado=None, depart=None):
        try:
            d = Departamento.get(nome=depart)
            temp = self._tempo_est_tela_banco(tempo_estimado)
            if id:
                projeto = Projeto.get_by_id(id)
                projeto.nome = nome
                projeto.tempo_estimado = temp
                projeto.fk_departamento = d
            else:
                projeto = Projeto(nome=nome, tempo_estimado=temp, fk_departamento=d)
            projeto.save()
            return "Operação realizada com sucesso!"
        except Exception as e:
            print(e)
            return "Houve uma falha na operação!"

    def excluir_projeto(self, id):

        try:
            projeto = Projeto.get_by_id(id)
            projeto.delete_instance()
            return "Projeto excluído com sucesso!"
        except Exception as e:
            print(e)
            return "Não foi possível excluir o Projeto!"

    def _tempo_est_tela_banco(self, tempo_est):

        if Util.valida_data(tempo_est):
            d = tempo_est.split('/')
            databanco = f"{d[2]}-{d[1]}-{d[0]}"
            return databanco

    def buscar_projeto(self, id=None, nome=None):

        try:
            if id:
                projeto = Projeto.get_by_id(id)
            elif nome:
                projeto = Projeto.select().where(Projeto.nome % f'%{nome}%')
            else:
                projeto = Projeto.select()
        except Exception as e:
            print(e)
            return None
        itens = []
        if type(projeto) is Projeto:
            itens.append(self._montar_projeto(projeto.id, projeto.nome, projeto.tempo_estimado, projeto.fk_departamento.nome))
        elif type(projeto) is ModelSelect:
            for p in projeto:
                itens.append(self._montar_projeto(p.id, p.nome, p.tempo_estimado, p.fk_departamento.nome))
        return itens

    def _tempo_est_banco_tela(self, data):
        data_tela = ""
        if data:
            data_array = str(data).split("-")
            data_tela = f'{data_array[2]}/{data_array[1]}/{data_array[0]}'
        return data_tela

    def _montar_projeto(self, id, nome, tempo_est, depart):
        tempo = self._tempo_est_banco_tela(tempo_est)
        meuprojeto = {
            'lblId': self._criarLabel(id, 0.1),
            'lblNome': self._criarLabel(nome, 0.4),
            'lblTemp': self._criarLabel(tempo, 0.1),
            'lblDepart': self._criarLabel(depart, 0.1),
            'btAtualizar': self._criarBotao("Atualizar"),
            'btExcluir': self._criarBotao("Excluir")
        }
        return meuprojeto

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
                       height='30dp',
                       size_hint_x = .1)
        return botao

    def buscarDeparts(self):
        departsbanco = Departamento.select()
        departs = []
        for depart in departsbanco:
            departs.append({"id": depart.id, "nome": depart.nome})
        return departs
