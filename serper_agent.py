"""
AI-АГЕНТ С SERPER.DEV (ПАРСИТ GOOGLE)
Использует Serper.dev API для поиска через Google
"""

import os
import requests
import json
from dotenv import load_dotenv
from smolagents import HfApiModel, CodeAgent, tool

load_dotenv()


@tool
def serper_search(query: str) -> str:
    """
    Search Google for general information.
    Args:
        query: The search query.
    """
    api_key = os.getenv("SERPER_API_KEY")
    url = "https://google.serper.dev/search"
    headers = {"X-API-KEY": api_key, "Content-Type": "application/json"}
    payload = json.dumps({"q": query, "num": 5})

    response = requests.post(url, headers=headers, data=payload, timeout=10)
    data = response.json()

    results = []
    if "answerBox" in data:
        results.append(f"Answer: {data['answerBox'].get('snippet') or data['answerBox'].get('answer')}")

    for item in data.get("organic", []):
        results.append(f"Title: {item['title']}\nSnippet: {item['snippet']}\nURL: {item['link']}\n")

    return "\n".join(results) if results else "No results found."


@tool
def serper_news(query: str) -> str:
    """
    Search Google News for the latest events.
    Args:
        query: News topic.
    """
    api_key = os.getenv("SERPER_API_KEY")
    url = "https://google.serper.dev/news"
    headers = {"X-API-KEY": api_key, "Content-Type": "application/json"}
    payload = json.dumps({"q": query, "num": 5})

    response = requests.post(url, headers=headers, data=payload, timeout=10)
    data = response.json()

    results = [f"News for {query}:"]
    for item in data.get("news", []):
        results.append(f"- {item['title']} ({item.get('source')}): {item['link']}")

    return "\n".join(results)


@tool
def read_webpage(url: str) -> str:
    """
    Reads the full text content of a webpage.
    Args:
        url: The URL to read.
    """
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, timeout=10, headers=headers)
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.get_text(separator=' ', strip=True)
        return text[:4000] + "..." if len(text) > 4000 else text
    except Exception as e:
        return f"Error reading page: {str(e)}"

# Проверяем наличие ключей
hf_token = os.getenv("HF_TOKEN")
serper_key = os.getenv("SERPER_API_KEY")

if not hf_token:
    print("ОШИБКА: HF_TOKEN не найден")
    exit(1)

if not serper_key:
    print("ОШИБКА: SERPER_API_KEY не найден")
    exit(1)

model = HfApiModel(
    model_id="meta-llama/Llama-4-Scout-17B-16E-Instruct",
    token=hf_token
)

tools = [
    serper_search,
    serper_news,     # Поиск новостей
    read_webpage     # Чтение страниц
]

system_prompt = """
# Operating Protocol:
1. **Analyze:** Before using tools, state your search strategy (what keywords and which tool).
2. **Execute:** - Use `serper_news` if the query mentions "today," "latest," or events from the last 7 days.
   - Use `serper_search` for evergreen knowledge or historical data.
   - Use `read_webpage` for any source that seems crucial to the final answer. **Never rely on snippets alone for complex topics.**
3. **Validate:** If sources conflict, highlight the discrepancy. Check the publication date of every source.
4. **Synthesize:** Combine findings into a coherent report, not just a list of facts.

# Tool Guidelines:
- `serper_search`: Use precise queries. If no results, broaden keywords.
- `read_webpage`: Mandatory for technical, legal, or medical queries to ensure accuracy.

# Output Format:
- **Executive Summary:** A 2-3 sentence overview.
- **Detailed Findings:** Use bullet points and subheadings.
- **Verification:** Mention which facts were cross-checked.
- **Sources:** List as [Source Name](URL) at the end of the response.

# Constraints:
- Current Year: 2026.
- If information is not found after 3 search attempts, admit it and suggest alternative keywords.
- No fluff. Be objective, concise, and professional.
"""

agent = CodeAgent(
    tools=tools,
    model=model,
    max_steps=10,
    verbosity_level=2  # Показывает подробные логи
)

#agent.system_prompt = system_prompt
agent.default_summarizer_template = system_prompt

test_queries = [
    # Факты
    "When did Cassius Clay change his name to Muhammad Ali?",
    
    # Актуальные данные
    "What is the current price of Bitcoin?",
    
    # Новости
    "Latest developments in artificial intelligence",
    
    # Сравнения
    "Compare Python vs JavaScript for beginners",
    
    # На русском
    "Какая погода в Москве сегодня?",
    
    # Сложный вопрос
    "Who won the Nobel Prize in Physics in 2024 and what was it for?",
]

print("\n" + "="*60)

# Выбираем вопрос (измените индекс для других вопросов)
query = "Какая самая продвинутая библиотека\фреймворк\инструмент для обработки данных нейронной и рентгеновской рефлектометрии и почему "

print(f"\n❓ Вопрос: {query}\n")
print("🔄 Агент ищет в Google...\n")

try:
    result = agent.run(query)
    
    print("\n" + "="*60)
    print("✅ РЕЗУЛЬТАТ:")
    print("="*60)
    print(result)
    
except Exception as e:
    print(f"\n❌ Ошибка: {e}")
    import traceback
    traceback.print_exc()
