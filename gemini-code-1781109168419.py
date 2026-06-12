# Participantes da Equipe: Caio Marcelo dos Santos Fonseca, Felipe Costa do Nascimento, Jefferson Alves de Oliveira

import sys
from abc import ABC, abstractmethod

class Funcionario(ABC):
    def __init__(self, matricula: int, nome: str, departamento: str):
        self.__matricula = matricula
        self.__nome = nome
        self.__departamento = departamento

    @property
    def matricula(self) -> int:
        return self.__matricula

    @property
    def nome(self) -> str:
        return self.__nome

    @property
    def departamento(self) -> str:
        return self.__departamento

    @nome.setter
    def nome(self, novo_nome: str):
        if novo_nome.strip():
            self.__nome = novo_nome

    @departamento.setter
    def departamento(self, novo_departamento: str):
        if novo_departamento.strip():
            self.__departamento = novo_departamento

    @abstractmethod
    def calcular_salario(self) -> float:
        pass

    def __str__(self) -> str:
        return f"Matrícula: {self.__matricula} | Nome: {self.__nome} | Depto: {self.__departamento}"


class FuncionarioMensalista(Funcionario):
    def __init__(self, matricula: int, nome: str, departamento: str, salario_mensal: float):
        super().__init__(matricula, nome, departamento)
        self._salario_mensal = salario_mensal

    @property
    def salario_mensal(self) -> float:
        return self._salario_mensal

    @salario_mensal.setter
    def salario_mensal(self, novo_salario: float):
        if novo_salario > 0:
            self._salario_mensal = novo_salario

    def calcular_salario(self) -> float:
        return self._salario_mensal

    def __str__(self) -> str:
        base_str = super().__str__()
        return f"{base_str} | Tipo: Mensalista | Salário: R$ {self.calcular_salario():.2f}"


class FuncionarioHorista(Funcionario):
    def __init__(self, matricula: int, nome: str, departamento: str, valor_hora: float, horas_trabalhadas: float):
        super().__init__(matricula, nome, departamento)
        self._valor_hora = valor_hora
        self._horas_trabalhadas = horas_trabalhadas

    @property
    def valor_hora(self) -> float:
        return self._valor_hora

    @valor_hora.setter
    def valor_hora(self, novo_valor: float):
        if novo_valor > 0:
            self._valor_hora = novo_valor

    @property
    def horas_trabalhadas(self) -> float:
        return self._horas_trabalhadas

    @horas_trabalhadas.setter
    def horas_trabalhadas(self, novas_horas: float):
        if novas_horas >= 0:
            self._horas_trabalhadas = novas_horas

    def calcular_salario(self) -> float:
        return self._valor_hora * self._horas_trabalhadas

    def __str__(self) -> str:
        base_str = super().__str__()
        return f"{base_str} | Tipo: Horista | Horas: {self._horas_trabalhadas}h | Salário: R$ {self.calcular_salario():.2f}"


class Diretor(FuncionarioMensalista):
    def __init__(self, matricula: int, nome: str, departamento: str, salario_base: float, bonificacao: float):
        super().__init__(matricula, nome, departamento, salario_base)
        self._bonificacao = bonificacao

    @property
    def bonificacao(self) -> float:
        return self._bonificacao
        
    @bonificacao.setter
    def bonificacao(self, nova_bonificacao: float):
        if nova_bonificacao >= 0:
            self._bonificacao = nova_bonificacao

    def calcular_salario(self) -> float:
        return self._salario_mensal + self._bonificacao

    def __str__(self) -> str:
        base = f"Matrícula: {self.matricula} | Nome: {self.nome} | Depto: {self.departamento}"
        return f"{base} | Tipo: Diretor | Bônus: R$ {self._bonificacao:.2f} | Salário Total: R$ {self.calcular_salario():.2f}"


class GerenciadorRH:
    def __init__(self):
        self.__lista_funcionarios = {}

    def adicionar_funcionario(self, funcionario: Funcionario) -> bool:
        if funcionario.matricula in self.__lista_funcionarios:
            return False
        self.__lista_funcionarios[funcionario.matricula] = funcionario
        return True

    def remover_funcionario(self, matricula: int) -> bool:
        if matricula in self.__lista_funcionarios:
            del self.__lista_funcionarios[matricula]
            return True
        return False

    def buscar_funcionario(self, matricula: int) -> Funcionario:
        return self.__lista_funcionarios.get(matricula, None)

    def buscar_por_departamento(self, departamento: str) -> list:
        lista_filtrada = []
        for func in self.__lista_funcionarios.values():
            if func.departamento.lower() == departamento.lower():
                lista_filtrada.append(func)
        return lista_filtrada

    def obter_todos(self) -> list:
        return list(self.__lista_funcionarios.values())

    def calcular_folha_total(self) -> float:
        total = 0.0
        for func in self.__lista_funcionarios.values():
            total += func.calcular_salario()
        return total


def exibir_menu():
    print("\n" + "="*60)
    print("           SISTEMA DE GESTÃO DE RECURSOS HUMANOS           ")
    print("="*60)
    print("1. Cadastrar Funcionário Mensalista")
    print("2. Cadastrar Funcionário Horista")
    print("3. Cadastrar Diretor")
    print("4. Listar Todos os Colaboradores")
    print("5. Buscar Funcionário por Matrícula")
    print("6. Filtrar Funcionários por Departamento")
    print("7. Atualizar Horas de Funcionário Horista")
    print("8. Remover Funcionário por Matrícula")
    print("9. Exibir Custo Total da Folha de Pagamento")
    print("10. Sair do Programa")
    print("="*60)


def obter_float_valido(mensagem: str) -> float:
    while True:
        try:
            valor = float(input(mensagem))
            if valor < 0:
                print("--> Erro: O valor não pode ser negativo.")
                continue
            return valor
        except ValueError:
            print("--> Erro: Digite um número válido (ex: 1500.50).")


def obter_dados_basicos():
    while True:
        try:
            mat = int(input("Digite a matrícula (apenas números): "))
            break
        except ValueError:
            print("--> Erro: Matrícula inválida. Digite um número inteiro.")
            
    nome = input("Digite o nome do colaborador: ").strip()
    depto = input("Digite o departamento: ").strip()
    return mat, nome, depto


def main():
    rh = GerenciadorRH()
    
    rh.adicionar_funcionario(FuncionarioMensalista(101, "Ana Silva", "TI", 4500.0))
    rh.adicionar_funcionario(FuncionarioHorista(102, "Bruno Souza", "Suporte", 25.0, 160))
    rh.adicionar_funcionario(Diretor(103, "Carla Dias", "Diretoria", 12000.0, 3500.0))

    while True:
        exibir_menu()
        opcao = input("Selecione uma opção (1-10): ").strip()
        
        if opcao == "1":
            mat, nome, depto = obter_dados_basicos()
            salario = obter_float_valido("Digite o salário mensal fixo: R$ ")
            novo_func = FuncionarioMensalista(mat, nome, depto, salario)
            if rh.adicionar_funcionario(novo_func):
                print("--> Funcionário Mensalista cadastrado com sucesso!")
            else:
                print("--> Erro: Já existe um funcionário com esta matrícula.")
                
        elif opcao == "2":
            mat, nome, depto = obter_dados_basicos()
            valor_h = obter_float_valido("Digite o valor por hora trabalhada: R$ ")
            horas_t = obter_float_valido("Digite a quantidade de horas trabalhadas: ")
            novo_func = FuncionarioHorista(mat, nome, depto, valor_h, horas_t)
            if rh.adicionar_funcionario(novo_func):
                print("--> Funcionário Horista cadastrado com sucesso!")
            else:
                print("--> Erro: Já existe um funcionário com esta matrícula.")
                
        elif opcao == "3":
            mat, nome, depto = obter_dados_basicos()
            salario_b = obter_float_valido("Digite o salário-base do diretor: R$ ")
            bonus = obter_float_valido("Digite a bonificação de lucros: R$ ")
            novo_func = Diretor(mat, nome, depto, salario_b, bonus)
            if rh.adicionar_funcionario(novo_func):
                print("--> Diretor cadastrado com sucesso!")
            else:
                print("--> Erro: Já existe um funcionário com esta matrícula.")
                
        elif opcao == "4":
            funcionarios = rh.obter_todos()
            if not funcionarios:
                print("\n--> Nenhum funcionário cadastrado no sistema no momento.")
            else:
                print("\n" + "-"*18 + " LISTA DE COLABORADORES " + "-"*18)
                for f in funcionarios:
                    print(f)
                print("-" * 60)
            input("\n👉 Pressione ENTER para voltar ao menu...")
                    
        elif opcao == "5":
            try:
                mat = int(input("Digite a matrícula para busca: "))
                func = rh.buscar_funcionario(mat)
                if func:
                    print("\n--> DADOS DO FUNCIONÁRIO:")
                    print(func)
                else:
                    print("--> Aviso: Funcionário não encontrado no sistema.")
            except ValueError:
                print("--> Erro: Digite apenas números para a matrícula.")
            input("\n👉 Pressione ENTER para voltar ao menu...")

        elif opcao == "6":
            depto_busca = input("Digite o nome do departamento: ").strip()
            lista_depto = rh.buscar_por_departamento(depto_busca)
            if not lista_depto:
                print(f"--> Nenhum funcionário encontrado no departamento '{depto_busca}'.")
            else:
                print(f"\n--> FUNCIONÁRIOS DO DEPARTAMENTO: {depto_busca.upper()}")
                for f in lista_depto:
                    print(f)
            input("\n👉 Pressione ENTER para voltar ao menu...")

        elif opcao == "7":
            try:
                mat = int(input("Digite a matrícula do funcionário horista: "))
                func = rh.buscar_funcionario(mat)
                if func:
                    if isinstance(func, FuncionarioHorista):
                        novas_horas = obter_float_valido(f"Digite as novas horas totais para {func.nome}: ")
                        func.horas_trabalhadas = novas_horas
                        print("--> Horas trabalhadas atualizadas com sucesso!")
                    else:
                        print("--> Erro: O funcionário selecionado não é do tipo Horista.")
                else:
                    print("--> Aviso: Funcionário não encontrado.")
            except ValueError:
                print("--> Erro: Digite apenas números para a matrícula.")
                
        elif opcao == "8":
            try:
                mat = int(input("Digite a matrícula do funcionário que deseja remover: "))
                if rh.remover_funcionario(mat):
                    print("--> Funcionário removido do sistema com sucesso!")
                else:
                    print("--> Aviso: Nenhuma matrícula correspondente foi encontrada.")
            except ValueError:
                print("--> Erro: Matrícula inválida. Digite apenas números.")
                
        elif opcao == "9":
            total_folha = rh.calcular_folha_total()
            print(f"\n--> Custo Total da Folha de Pagamento Atual: R$ {total_folha:.2f}")
            input("\n👉 Pressione ENTER para voltar ao menu...")
            
        elif opcao == "10":
            print("\nFinalizando o sistema de Gestão de RH. Até mais!")
            sys.exit(0)
            
        else:
            print("--> Opção inválida! Por favor, selecione um número de 1 a 10.")

if __name__ == "__main__":
    main()