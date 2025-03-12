import pywhatkit
import time
import random
import pyautogui

# Lista de números para envio (no formato internacional com +55 para Brasil, por exemplo)
contatos = [
    {"nome": "Caynan Santos", "telefone": "557998007470"},
    # {"nome": "Idelfonso Carlos da Silva Filho", "telefone": "5561985442727"},
    # {"nome": "Fábio Alves", "telefone": "5581992069266"},
    # {"nome": "Simone Cruz", "telefone": "55"},
    # {"nome": "Valmir Bruno da Silva Araujo", "telefone": "5596991706396"},
    # {"nome": "Lucas Praxedes Vieira dos Santos", "telefone": "5513988324773"},
    # {"nome": "Allan Toledo", "telefone": "5517997314409"},
    # {"nome": "Thiago Gomes de Barros", "telefone": "555571996074211"},
    # {"nome": "Cristiano Machado", "telefone": "5548998058476"},
    # {"nome": "Jessica Caroline Silva", "telefone": "5548984710309"},
    # {"nome": "Edelson Pacheco", "telefone": "5598981910527"},
    # {"nome": "Cybelle Florencio", "telefone": "5581997888570"},
    # {"nome": "Jarbas Gomes Duarte Neto", "telefone": "5569981575822"},
    # {"nome": "Joaninha Dias", "telefone": "5581988760306"},
    # {"nome": "Reginaldo Nascimento", "telefone": "5544998014647"},
    # {"nome": "Rodolfo Morete", "telefone": "5521995657769"},
    # {"nome": "Eduardo Alves", "telefone": "5562985582182"},
    # {"nome": "Mateus Antonio Gionedis", "telefone": "5512992074054"},
    # {"nome": "Adriano Rigo", "telefone": "5519994206336"},
    # {"nome": "James de Jesus", "telefone": "5531975978272"},
    # {"nome": "Felipe Carvalho", "telefone": "5521986939614"},
    # {"nome": "Marcelo Rodrigues Sampaio", "telefone": "5568999136106"},
    # {"nome": "Adonias dos Santos Oliveira", "telefone": "5579961729967"},
    # {"nome": "Francelene Lima dos Santos", "telefone": "5591982337447"},
    # {"nome": "Rafael Alves Theodoro", "telefone": "5524998346101"},
    # {"nome": "Brenda Guimaraes Vieira dos Passos", "telefone": "5521998476548"},
    # {"nome": "Kennedy Luan da Silva Oliveira", "telefone": "5555981548511"},
    # {"nome": "Millena de Sousa", "telefone": "5511981975147"},
    # {"nome": "Danillo Bessa", "telefone": "5584991138583"},
    # {"nome": "Makley Guedes Claudino", "telefone": "5562981222185"},
    # {"nome": "Eliezer Duarte de Siqueira", "telefone": "5512997046398"},
    # {"nome": "Tiago Henrique de Oliveira", "telefone": "11913525905"},
    # {"nome": "Mateus Fernandes", "telefone": "5593999548092"},
    # {"nome": "Emerson Marques", "telefone": "5511986778658"},
    # {"nome": "Geraldo de Assis Alves Júnior", "telefone": "61993038903"},
    # {"nome": "Jose Rafael de Macedo Lopes", "telefone": "558199114355"},
    # {"nome": "Junio Pereira Luciano", "telefone": "5531991141714"},
    # {"nome": "Allan Celso Ribeiro Rodrigues", "telefone": "5581991963236"},
    # {"nome": "João Carlos Neves Belicio", "telefone": "5522991034749"},
    # {"nome": "Rogério Tadeu Panza", "telefone": "5592984572744"},
    # {"nome": "Luiz Sérgio de Souza Junior", "telefone": "11983692255"},
    # {"nome": "Letícia de Alencar Santos", "telefone": "5585996275798"},
    # {"nome": "Laís Sant Ana Oliveira", "telefone": "5531991096398"},
    # {"nome": "Saulo de Lima Torres Filho", "telefone": "5581983056560"},
    # {"nome": "Antonio Celso Onorato da Silva Filho", "telefone": "5512992023093"},
    # {"nome": "Ricardo Toro", "telefone": "5571991918552"},
    # {"nome": "Dionisio de Sousa", "telefone": "5561984024934"},
    # {"nome": "Wilson David Rodrigues Sousa", "telefone": "5588994402502"},
    # {"nome": "Pedro Henrique Nogueira Grobério", "telefone": "11989391863"},
    # {"nome": "Valério José Correia Neto", "telefone": "5594992262767"},
    # {"nome": "Bruno Brito Amorim", "telefone": "5527999684062"},
    # {"nome": "Andrei Leite Mesquita", "telefone": "5512981278368"},
    # {"nome": "Natanael Luan de Lima", "telefone": "5549991210977"},
    # {"nome": "Geraldo Silva Junior", "telefone": "555"},
    # {"nome": "Marcos Antonio Nunes da Silva", "telefone": "5541992161499"},
    # {"nome": "Viviane da Silva", "telefone": "5521975450975"},
    # {"nome": "Aline Torres", "telefone": "5531999869378"},
    # {"nome": "Polyana Lemasson", "telefone": "19999424183"},
    # {"nome": "Danilo Santana dos Santos", "telefone": "5579991186035"},
    # {"nome": "Rodrigo da Silva Honorato", "telefone": "5527988590263"},
    # {"nome": "Ciro Jose Cardoso Pimenta", "telefone": "5541999400477"},
    # {"nome": "Sabrine Lima", "telefone": "5521997443821"},
    # {"nome": "Claudiney de Souza Oliveira", "telefone": "5527997746374"},
    # {"nome": "Enzo Dias Arguelles", "telefone": "5521974556621"},
    # {"nome": "Fabiana Maria do Canto", "telefone": "5521977363258"},
    # {"nome": "João Henrique Bomfim", "telefone": "5585981228137"},
    # {"nome": "Eduardo Veiga", "telefone": "555562984121164"},
    # {"nome": "Alex Bittencourt", "telefone": "41999302882"},
    # {"nome": "Magno Sousa", "telefone": "5545988441446"},
    # {"nome": "RC Eletricidade", "telefone": "5519993059852"},
    # {"nome": "Marion de A Cavalcante Melo", "telefone": "5511991218062"},
    # {"nome": "Cleberson dos Santos Paulo", "telefone": "5545998272606"},
    # {"nome": "Leandro Araujo", "telefone": "553799970421"},
    # {"nome": "Rodrigo Garcia Silva", "telefone": "5543996854651"},
    # {"nome": "Robinson Fernandes Martins", "telefone": "5585988546873"},
    # {"nome": "Giovanna Bacci Brigato", "telefone": "5516991496049"},
    # {"nome": "Pamela Quenuti", "telefone": "5533991971484"},
    # {"nome": "Sergio Ricardo de Almeida", "telefone": "5579999729246"},
    # {"nome": "Witalo Fernando", "telefone": "5586999775175"},
    # {"nome": "Crislaine P Gomes", "telefone": "5591992042102"},
    # {"nome": "Robert Junio Rocha Silva", "telefone": "5562982028034"},
    # {"nome": "Cristiane Galvão Lazzaretti", "telefone": "5549998271079"},
    # {"nome": "Playbiane da Silva Rodrigues", "telefone": "5563984204638"},
    # {"nome": "Eliana de Oliveira Leite", "telefone": "5565996175641"},
    # {"nome": "Edejanio Ferreira Barros", "telefone": "5599981120292"},
    # {"nome": "Diego Victor Reis Pereira", "telefone": "5531920080521"},
    # {"nome": "Egon H Bittencourt", "telefone": "5519999222147"},
    # {"nome": "Kátia Nunes", "telefone": "5511986541185"},
    # {"nome": "Jaderson da Silva Crescencio", "telefone": "5551985974995"},
    # {"nome": "Jaqueline da Conceição Viana", "telefone": "5569992964643"},
    # {"nome": "Viviane Rabelo", "telefone": "5511983688800"},
    # {"nome": "Adriano Verdejo Melchiorre", "telefone": "5541992442552"},
    # {"nome": "Erica Monteiro", "telefone": "5531984421934"},
    # {"nome": "Bruno Oliveira", "telefone": "5511960269087"},
]


# Mensagem a ser enviada
mensagem = (
    "Olá, sua vida precisa de disciplina e bons hábitos! Vi que se interessou pelo *Projeto 9/90*. "
    "Me chamo Caynan e vai ser um prazer conversar contigo hoje e esclarecer possíveis dúvidas. "
    "Para começarmos, me explique o que te levou a desistir da compra?"
)

# Função para enviar mensagens com intervalo aleatório
def enviar_mensagens(contatos, mensagem):
    for contato in contatos:
        telefone = contato["telefone"]
        nome = contato["nome"]
        try:
            # Envia mensagem de texto instantânea
            pywhatkit.sendwhatmsg_instantly(f"+{telefone}", mensagem, wait_time=10)
            time.sleep(5)
            
            pyautogui.press("enter")
            
            print(f"Mensagem enviada para {nome} ({telefone}).")

            # Define intervalo aleatório entre 30 e 120 segundos entre mensagens
            intervalo = random.randint(8, 120)
            print(f"Próxima mensagem será enviada em {intervalo} segundos.")
            time.sleep(intervalo)

        except Exception as e:
            print(f"Erro ao enviar mensagem para {nome} ({telefone}): {e}")

# Executa a função
enviar_mensagens(contatos, mensagem)
