import datetime


class Util:

    @staticmethod
    def valida_data(data):
        dt = data.split('/') # converte data string em vetor
        # 10/04/2006
        if len(dt) == 3:
            if 0 < int(dt[0]) <= 31:
                if 0 < int(dt[1]) <= 12:
                    hoje = datetime.date.today()
                    if 1900 < int(dt[2]) <= hoje.year:
                        return True
        return False