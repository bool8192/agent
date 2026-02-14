"""
МИНИМАЛЬНАЯ ВЕРСИЯ AI-АГЕНТА
Этот файл показывает самую простую реализацию
"""

from smolagents import DuckDuckGoSearchTool, HfApiModel, ToolCallingAgent, VisitWebpageTool, PromptTemplates
import os
from dotenv import load_dotenv

load_dotenv()

# 1. МОДЕЛЬ
model = HfApiModel(
    model_id="Qwen/Qwen2.5-72B-Instruct",
    token=os.getenv("HF_TOKEN")
)

# 2. ИНСТРУМЕНТЫ
tools = [
    DuckDuckGoSearchTool(max_results=5),
    VisitWebpageTool()
]

# 3. ПРОМПТ
prompt_template = PromptTemplates(system_prompt="""
Ты - исследователь интернета.
Твоя задача - искать информацию используя DuckDuckGoSearchTool и VisitWebpageTool.
Когда находишь ответ, вызывай final_answer.
""")

# 4. АГЕНТ
agent = ToolCallingAgent(
    tools=tools,
    model=model,
    prompt_templates=prompt_template,
    max_steps=10
)

# 5. ЗАПУСК
query = "В каком году Кассиус Клей сменил имя?"
print(f"Вопрос: {query}\n")
result = agent.run(query)
print(f"\nОтвет: {result}")
