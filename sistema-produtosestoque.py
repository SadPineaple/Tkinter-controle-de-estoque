from tkinter import *
from tkinter import ttk
import _sqlite3 

root = Tk()

class Funcs():
    def limpa_tela(self):
        self.id_entry.delete(0, END)
        self.nome_entry.delete(0, END)
        self.idestoque_entry.delete(0, END)
        self.descricao_entry.delete(0, END)
        self.estoque_entry.delete(0, END)
    def conecta_bd(self):
        self.conn = _sqlite3.connect("estoque.db")
        self.cursor = self.conn.cursor(); print("Conectando ao banco de dados")
    def desconecta_bd(self):
        self.conn.close();  print("Desconectando do banco de dados")
    def montaTabelas(self):
        self.conecta_bd()
        ### Criação tabela
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS estoque (
                id INTEGER PRIMARY KEY,
                nome CHAR(50) NOT NULL,
                idestoque CHAR(50),
                descricao CHAR(100),
                estoque CHAR(50)
            );
        """)
        self.conn.commit();print("Banco de dados criado")
        self.desconecta_bd()
    def variaveis(self):
        self.id = self.id_entry.get()
        self.nome = self.nome_entry.get()
        self.idestoque = self.idestoque_entry.get()
        self.descricao = self.descricao_entry.get()
        self.estoque = self.estoque_entry.get()
    def add_produtos(self):
        self.variaveis()
        self.conecta_bd()

        self.cursor.execute("""
            INSERT INTO estoque (
            nome,
            idestoque,
            descricao,
            estoque
            )
        VALUES (
            ?,
            ?,
            ?,
            ?
        )""", (
            self.nome,
            self.idestoque,
            self.descricao,
            self.estoque
            ))
        self.conn.commit()
        self.desconecta_bd()
        self.select_lista()
        self.limpa_tela()
    def select_lista(self):
        self.listaPro.delete(*self.listaPro.get_children())
        self.conecta_bd()
        lista = self.cursor.execute(""" 
        SELECT 
            id,
            nome,
            idestoque,
            descricao,
            estoque
             FROM estoque
        ORDER BY nome ASC""")
        for i in lista:
            self.listaPro.insert("", END, values=i)
        self.desconecta_bd()
    def busca_produtos(self):
        self.conecta_bd()
        self.listaPro.delete(*self.listaPro.get_children())

        self.nome_entry.insert(END, '%')
        nome = self.nome_entry.get()
        self.cursor.execute("""
        SELECT 
            id,
            nome,
            idestoque,
            descricao,
            estoque
        FROM estoque WHERE nome LIKE '%s'
        ORDER BY nome ASC
        """ % nome )
        buscanomeForm = self.cursor.fetchall()
        for i in buscanomeForm:
            self.listaPro.insert("", END, values=i)
        self.limpa_tela()
        self.desconecta_bd()
    def OnDoubleClick(self, event):

        self.limpa_tela()
        self.listaPro.selection()
        
        for n in self.listaPro.selection():
            col1, col2, col4, col3, col5 = self.listaPro.item(n, 'values')
            self.id_entry.insert(END, col1)
            self.nome_entry.insert(END, col2)
            self.idestoque_entry.insert(END, col4)
            self.descricao_entry.insert(END, col5)
    def deleta_produtos(self):
        self.variaveis()
        self.conecta_bd()
        self.cursor.execute("""
            DELETE FROM estoque WHERE id = ? """, ([self.id]))
        self.conn.commit()
        self.desconecta_bd()
        self.limpa_tela()
        self.select_lista()
    def altera_produtos(self):
        self.variaveis()
        self.conecta_bd()
        self.cursor.execute(""" UPDATE estoque SET 
            nome = ?,
            idestoque = ?,
            descricao = ?,
            estoque = ?
        WHERE id = ?
            """, (
            self.nome,
            self.idestoque,
            self.descricao,
            self.estoque,
            self.id
            ))
        self.conn.commit()
        self.desconecta_bd()
        self.select_lista()
        self.limpa_produtos()

class Application(Funcs):
    def __init__(self):
        self.root = root
        self.tela()
        self.frames_da_tela()
        self.widgets_frame1()
        self.lista_frame2()
        self.montaTabelas()
        self.select_lista()
        self.Menus()
        root.mainloop()
    def tela(self):
        self.root.title("Produtos Estoque")
        self.root.configure(background= "#DCD4BA")
        self.root.state("zoomed")
        self.root.resizable(True, True)
        self.root.maxsize(width= 1366, height= 768)
        self.root.minsize(width=1240, height=600)
    def frames_da_tela(self):
        self.frame_1 = Frame(self.root, bg= "#DCD4BA")
        self.frame_1.place(relx= 0.015, rely= 0.025, relwidth= 0.475, relheight= 0.95)

        self.frame_2 = Frame(self.root, bg= "#DCD4BA")
        self.frame_2.place(relx= 0.508, rely= 0.025, relwidth= 0.475, relheight= 0.95)
    def widgets_frame1(self):
        ### Criaçao do botao limpar
        self.bt_limpar = Button(self.frame_1, font = ('calibri', 14), text="Limpar", bd=0, bg="#FE4A49", fg="#fff", command= self.limpa_tela,
                                activebackground='#721817', activeforeground="white")
        self.bt_limpar.place(relx= 0.80, rely= 0.25, relwidth= 0.13, relheight= 0.07)

        ### Criaçao do botao buscar
        self.bt_buscar = Button(self.frame_1, font = ('calibri', 14), text="Buscar",  bd=0, bg="#FE4A49", fg="#fff", command= self.busca_produtos,
                                activebackground='#721817', activeforeground="white")
        self.bt_buscar.place(relx= 0.80, rely= 0.39, relwidth= 0.13, relheight= 0.07)

        ### Criaçao do botao novo
        self.bt_novo = Button(self.frame_1, font = ('calibri', 14), text="Novo",  bd=0, bg="#FE4A49", fg="#fff", command= self.add_produtos,
                              activebackground='#721817', activeforeground="white")
        self.bt_novo.place(relx= 0.26, rely= 0.25, relwidth= 0.13, relheight= 0.07)

        ### Criaçao do botao alterar
        self.bt_alterar = Button(self.frame_1, font = ('calibri', 14), text="Alterar", bd=0, bg="#FE4A49", fg="#fff", command= self.altera_produtos,
                                 activebackground='#721817', activeforeground="white")
        self.bt_alterar.place(relx= 0.44, rely= 0.25, relwidth= 0.13, relheight= 0.07)

        ### Criaçao do botao apagar
        self.bt_apagar = Button(self.frame_1, font = ('calibri', 14), text="Apagar", bd=0, bg="#FE4A49", fg="#fff", command=self.deleta_produtos,
                                activebackground='#721817', activeforeground="white")
        self.bt_apagar.place(relx= 0.62, rely= 0.25, relwidth= 0.13, relheight= 0.07)

        
        ### Criaçao da label e entrada do ID
        self.lb_id = Label(self.frame_1, font = ('calibri', 12), text = "ID", bg="#DCD4BA")
        self.lb_id.place(relx= 0.1, rely= 0.20)

        self.id_entry = Entry(self.frame_1, font = ('arial', 18))
        self.id_entry.place(relx= 0.1, rely= 0.25, relwidth= 0.10, relheight= 0.07)

        ### Criaçao da label e entrada do Nome
        self.lb_nome = Label(self.frame_1, font = ('calibri', 12), text = "Nome", bg="#DCD4BA")
        self.lb_nome.place(relx= 0.1, rely= 0.35)

        self.nome_entry = Entry(self.frame_1, font = ('arial', 13), bg= "#F8C2C2")
        self.nome_entry.place(relx= 0.1, rely= 0.4, relwidth= 0.65, relheight= 0.05)

        ### Criaçao da label e entrada do Estoque
        self.lb_estoque = Label(self.frame_1, font = ('calibri', 12), text = "Em Estoque", bg="#DCD4BA")
        self.lb_estoque.place(relx= 0.1, rely= 0.45)

        self.estoque_entry = Entry(self.frame_1, font = ('arial', 13))
        self.estoque_entry.place(relx= 0.1, rely= 0.5, relwidth= 0.83, relheight= 0.05)

        ### Criaçao da label e entrada do Id de Estoque
        self.lb_idestoque = Label(self.frame_1, font = ('calibri', 12), text = "ID de Estoque", bg="#DCD4BA")
        self.lb_idestoque.place(relx= 0.1, rely= 0.55)

        self.idestoque_entry = Entry(self.frame_1, font = ('arial', 13))
        self.idestoque_entry.place(relx= 0.1, rely= 0.6, relwidth= 0.83, relheight= 0.05)

        ### Criaçao da label e entrada do Descrição
        self.lb_descricao = Label(self.frame_1, font = ('calibri', 12), text = "Descrição", bg="#DCD4BA")
        self.lb_descricao.place(relx= 0.1, rely= 0.65)

        self.descricao_entry = Entry(self.frame_1, font = ('arial', 13))
        self.descricao_entry.place(relx= 0.1, rely= 0.7, relwidth= 0.83, relheight= 0.05)


    def lista_frame2(self):
        self.listaPro = ttk.Treeview(self.frame_2, height= 3, column=(
            "col1",
            "col2",
            "col3",
            "col4",
            "col5",
            ))
        self.listaPro.heading("#0", text="")
        self.listaPro.heading("#1", text="Código")
        self.listaPro.heading("#2", text="Nome")
        self.listaPro.heading("#3", text="Id de Estoque")
        self.listaPro.heading("#4", text="Descrição")
        self.listaPro.heading("#5", text="Em Estoque")
        
        self.listaPro.column("#0", width=1)
        self.listaPro.column("#1", width=50)
        self.listaPro.column("#2", width=100)
        self.listaPro.column("#3", width=100)
        self.listaPro.column("#4", width=100)
        self.listaPro.column("#5", width=100)
        

        self.listaPro.place(relx=0.02, rely=0.02, relwidth=0.92, relheight=0.96)

        self.scroolLista = Scrollbar(self.frame_2, orient='vertical')
        self.listaPro.configure(yscroll=self.scroolLista.set)
        self.scroolLista.place(relx= 0.94, rely=0.02, relwidth=0.04, relheight=0.96)
        self.listaPro.bind("<Double-1>", self.OnDoubleClick)
    def Menus(self):
        menubar = Menu(self.root)
        self.root.config(menu=menubar)
        filemenu = Menu(menubar)
        filemenu2 = Menu(menubar)

        def Quit(): self.root.destroy()

        menubar.add_cascade(label= "Opções", menu= filemenu)

        filemenu.add_command(label="Sair", command= Quit)

Application()