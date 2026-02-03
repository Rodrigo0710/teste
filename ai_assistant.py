#!/usr/bin/env python3
"""IA simples em linha de comando com memória e base de conhecimento."""

from __future__ import annotations

import json
import random
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional

BASE_DIR = Path(__file__).resolve().parent
KNOWLEDGE_PATH = BASE_DIR / "knowledge_base.json"
MEMORY_PATH = BASE_DIR / "memory.json"


@dataclass
class Intent:
    name: str
    patterns: List[str]
    responses: List[str]


@dataclass
class KnowledgeBase:
    intents: List[Intent] = field(default_factory=list)
    fallback: List[str] = field(default_factory=list)

    @staticmethod
    def load(path: Path) -> "KnowledgeBase":
        data = json.loads(path.read_text(encoding="utf-8"))
        intents = [Intent(**intent) for intent in data.get("intents", [])]
        fallback = data.get("fallback", [])
        return KnowledgeBase(intents=intents, fallback=fallback)


@dataclass
class Memory:
    data: Dict[str, str] = field(default_factory=dict)

    @staticmethod
    def load(path: Path) -> "Memory":
        if path.exists():
            content = json.loads(path.read_text(encoding="utf-8"))
            return Memory(data=content)
        return Memory()

    def save(self, path: Path) -> None:
        path.write_text(json.dumps(self.data, indent=2, ensure_ascii=False), encoding="utf-8")


class SimpleAI:
    def __init__(self, knowledge: KnowledgeBase, memory: Memory) -> None:
        self.knowledge = knowledge
        self.memory = memory
        self.intent_regex = self._compile_patterns()

    def _compile_patterns(self) -> Dict[str, re.Pattern[str]]:
        compiled: Dict[str, re.Pattern[str]] = {}
        for intent in self.knowledge.intents:
            escaped = [re.escape(pattern) for pattern in intent.patterns]
            regex = r"\\b(?:" + "|".join(escaped) + r")\\b"
            compiled[intent.name] = re.compile(regex, flags=re.IGNORECASE)
        return compiled

    def detect_intent(self, text: str) -> Optional[Intent]:
        for intent in self.knowledge.intents:
            pattern = self.intent_regex.get(intent.name)
            if pattern and pattern.search(text):
                return intent
        return None

    def remember_name(self, text: str) -> Optional[str]:
        match = re.search(r"me chamo (.+)$|meu nome é (.+)$", text, flags=re.IGNORECASE)
        if not match:
            return None
        name = next(group for group in match.groups() if group)
        name = name.strip().title()
        if name:
            self.memory.data["name"] = name
            return name
        return None

    def respond(self, text: str) -> str:
        if name := self.remember_name(text):
            return f"Prazer, {name}! Vou lembrar disso."

        if re.search(r"meu nome", text, flags=re.IGNORECASE) and "name" in self.memory.data:
            return f"Você me disse que seu nome é {self.memory.data['name']}."

        intent = self.detect_intent(text)
        if intent:
            return random.choice(intent.responses)

        if "name" in self.memory.data:
            return (
                f"{self.memory.data['name']}, ainda estou aprendendo. "
                "Pode reformular a pergunta?"
            )

        return random.choice(self.knowledge.fallback)


def run_cli() -> None:
    knowledge = KnowledgeBase.load(KNOWLEDGE_PATH)
    memory = Memory.load(MEMORY_PATH)
    assistant = SimpleAI(knowledge, memory)

    print("IA: Olá! Sou uma IA simples. Digite 'sair' para encerrar.")

    try:
        while True:
            user_input = input("Você: ").strip()
            if not user_input:
                print("IA: Pode dizer algo? Estou ouvindo.")
                continue
            if user_input.lower() in {"sair", "exit", "quit"}:
                print("IA: Até mais!")
                break
            response = assistant.respond(user_input)
            print(f"IA: {response}")
    finally:
        memory.save(MEMORY_PATH)


if __name__ == "__main__":
    run_cli()
