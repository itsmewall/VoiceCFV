import nltk
from nltk.chat.util import Chat, reflections

pairs = [    ['oi|olá|bom dia|boa tarde|boa noite', ['Olá!', 'Oi!', 'E aí?', 'Tudo bem?']],
    ['qual é o seu nome?', ['Meu nome é VOICECFV', 'Eu sou o VoiceCFV']],
    ['como você está?', ['Estou bem, obrigado por perguntar. E você?']],
    ['qual é a sua idade?', ['Eu não tenho idade, sou apenas um programa de computador']],
    ['adeus|tchau|até mais', ['Até mais!', 'Tchau!']]
]

def chatbot():
    print('Olá! Eu sou o ChatGPT. Como posso ajudar?')
    chat = Chat(pairs, reflections)
    while True:
        user_input = input('Você: ')
        if user_input.lower() == 'sair':
            break
        response = chat.respond(user_input)
        print('ChatGPT:', response)

if __name__ == '__main__':
    nltk.download('punkt')
    chatbot()