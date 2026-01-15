class Pessoa:
    def __init__(self, nome, idade, CPF):
        self.nome = nome
        self.idade = idade
        self.CPF = CPF

    def apresentar(self):
        print(f'Olá, meu nome é {self.nome} e tenho {self.idade} anos de idade e meu número de CPF é {self.CPF}.')

p1 = Pessoa('cinthia', 39, 92484018215)
p1.apresentar()


