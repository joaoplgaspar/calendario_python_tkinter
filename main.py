import calendar
import tkinter as tk
from tkinter import messagebox, simpledialog
import json

def carregar_lembretes():
    try:
        with open('lembretes.json', 'r') as arquivo:
            return json.load(arquivo)
    except FileNotFoundError:
        return {}

def salvar_lembretes(lembretes):
    with open('lembretes.json', 'w') as arquivo:
        json.dump(lembretes, arquivo)

class AplicativoCalendario(tk.Tk):
    def __init__(self, lembretes):
        super().__init__()
        self.lembretes = lembretes
        self.title("Calendário")
        self.geometry("800x700")

        ano_atual = calendar.datetime.date.today().year
        mes_atual = calendar.datetime.date.today().month

        self.calendario = calendar.monthcalendar(ano_atual, mes_atual)
        self.labels = []

        self.criar_calendario()

    def criar_calendario(self):
        frame = tk.Frame(self)
        frame.pack(padx=20, pady=20)

        mes_atual = calendar.datetime.date.today().month
        header_label = tk.Label(frame, text=calendar.month_name[mes_atual], font=("Arial", 16, "bold"))
        header_label.pack()

        frame_dias_semana = tk.Frame(frame)
        frame_dias_semana.pack(pady=10)

        dias_semana = calendar.day_name
        for i, dia_semana in enumerate(dias_semana):
            label = tk.Label(frame_dias_semana, text=dia_semana[:3].capitalize(), font=("Arial", 12, "bold"))
            label.grid(row=0, column=i, padx=(5, 15), pady=5)
            label.bind('<Button-1>', self.destacar_dia_semana)

        frame_dias_mes = tk.Frame(frame)
        frame_dias_mes.pack()

        for linha, semana in enumerate(self.calendario):
            for coluna, dia in enumerate(semana):
                frame_dia = tk.Frame(frame_dias_mes, bd=1, relief="solid")
                frame_dia.grid(row=linha+1, column=coluna, padx=5, pady=5)

                label_dia = tk.Label(frame_dia, width=8, height=3, text=str(dia), font=("Arial", 12))
                label_dia.pack(pady=2)
                label_dia.bind('<Button-1>', self.adicionar_lembrete)
                self.labels.append((label_dia, dia))

                if str(dia) in self.lembretes:
                    lembrete_texto = self.lembretes[str(dia)]
                    frame_lembrete = tk.Frame(frame_dia, bg='yellow', width=100, height=30)
                    frame_lembrete.pack(pady=2)

                    # Botão para excluir lembrete
                    botao_excluir = tk.Button(frame_lembrete,text="Concluir",
                                              command=lambda d=dia: self.excluir_lembrete(d))
                    botao_excluir.pack(pady=2)

    def adicionar_lembrete(self, evento):
        dia = int(evento.widget['text'])
        lembrete = simpledialog.askstring("Lembrete", "Digite o lembrete para o dia {}:".format(dia))
        if lembrete:
            self.lembretes[str(dia)] = lembrete
            messagebox.showinfo("Lembrete Adicionado", "Lembrete adicionado para o dia {}.".format(dia))
            self.atualizar_calendario()
            salvar_lembretes(self.lembretes)

    def excluir_lembrete(self, dia):
        dia_str = str(dia)
        if dia_str in self.lembretes:
            del self.lembretes[dia_str]
            messagebox.showinfo("Lembrete Removido", "Lembrete removido do dia {}.".format(dia))
            self.atualizar_calendario()
            salvar_lembretes(self.lembretes)

    def atualizar_calendario(self):
        for label_dia, dia in self.labels:
            if str(dia) in self.lembretes:
                label_dia.configure(bg='yellow')
            else:
                label_dia.configure(bg='white')

    def destacar_dia_semana(self, evento):
        label = evento.widget
        label.configure(bg='light blue')

    def mostrar_lembretes(self):
        janela_lembretes = tk.Toplevel(self)
        janela_lembretes.title("Todos os Lembretes")
        texto_lembretes = tk.Text(janela_lembretes)
        texto_lembretes.pack()

        for dia, lembrete in self.lembretes.items():
            texto_lembretes.insert(tk.END, "Dia {}: {}\n".format(dia, lembrete))

if __name__ == '__main__':
    lembretes = carregar_lembretes()

    app = AplicativoCalendario(lembretes)
    app.atualizar_calendario()

    botao_mostrar_lembretes = tk.Button(app, text="Mostrar Lembretes", command=app.mostrar_lembretes)
    botao_mostrar_lembretes.pack(pady=10)

    app.mainloop()
