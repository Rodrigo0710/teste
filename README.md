# IA Simples (Assistente CLI)

Um pequeno projeto em Python que simula uma **IA completa** de forma didática: 
- **NLU básica** com reconhecimento de intenções.
- **Memória de usuário** persistida em arquivo.
- **Base de conhecimento** editável em JSON.
- **Respostas contextualizadas** e fallback inteligente.

> Tudo feito apenas com a biblioteca padrão do Python.

## Como executar

```bash
python3 ai_assistant.py
```

## Exemplos

```
Você: oi
IA: Oi! Em que posso ajudar hoje?

Você: me chamo Ana
IA: Prazer, Ana! Vou lembrar disso.

Você: qual é o seu nome?
IA: Eu sou a IA Simples, sua assistente local.
```

## Personalização rápida

Edite o arquivo `knowledge_base.json` para adicionar novas respostas e intenções.

## Arquivos principais

- `ai_assistant.py` — motor principal da IA.
- `knowledge_base.json` — base de conhecimento e intenções.
- `memory.json` — memória persistente (gerada automaticamente).
