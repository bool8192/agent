"""
ТЕСТИРОВАНИЕ API КЛЮЧЕЙ
Проверяет что все ключи правильно настроены и работают
"""

from dotenv import load_dotenv
import os
import requests

load_dotenv()

print("="*60)
print("ПРОВЕРКА API КЛЮЧЕЙ")
print("="*60 + "\n")

# ===== ПРОВЕРКА 1: HUGGING FACE =====
print("1️⃣  Проверка Hugging Face Token...")

hf_token = os.getenv("HF_TOKEN")
if hf_token:
    print(f"   ✅ HF_TOKEN найден: {hf_token[:10]}...{hf_token[-10:]}")
    
    # Проверяем валидность
    try:
        response = requests.get(
            "https://huggingface.co/api/whoami-v2",
            headers={"Authorization": f"Bearer {hf_token}"},
            timeout=5
        )
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Токен валиден! Пользователь: {data.get('name', 'Unknown')}")
        else:
            print(f"   ❌ Токен невалиден! Код ошибки: {response.status_code}")
    except Exception as e:
        print(f"   ⚠️  Не удалось проверить токен: {e}")
else:
    print("   ❌ HF_TOKEN не найден в .env файле!")

print()

# ===== ПРОВЕРКА 2: SERPER.DEV =====
print("2️⃣  Проверка Serper.dev API...")

serper_key = os.getenv("SERPER_API_KEY")
if serper_key:
    print(f"   ✅ SERPER_API_KEY найден: {serper_key[:10]}...{serper_key[-10:]}")
    
    # Тестовый запрос
    try:
        import json
        
        response = requests.post(
            "https://google.serper.dev/search",
            headers={
                "X-API-KEY": serper_key,
                "Content-Type": "application/json"
            },
            data=json.dumps({"q": "test", "num": 1}),
            timeout=10
        )
        
        if response.status_code == 200:
            print("   ✅ API работает! Тестовый поиск выполнен успешно")
            data = response.json()
            if "organic" in data and data["organic"]:
                print(f"   ✅ Получено результатов: {len(data['organic'])}")
            
            # Проверяем кредиты
            if "credits" in data:
                print(f"   ℹ️  Осталось запросов: {data['credits']}")
                
        elif response.status_code == 401:
            print("   ❌ Неверный API ключ (401 Unauthorized)")
        elif response.status_code == 402:
            print("   ❌ Закончились бесплатные запросы (402 Payment Required)")
            print("   💡 Проверьте Dashboard: https://serper.dev/dashboard")
        elif response.status_code == 429:
            print("   ⚠️  Превышен лимит запросов (429 Too Many Requests)")
        else:
            print(f"   ❌ Ошибка API: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Ошибка при проверке: {e}")
else:
    print("   ⚠️  SERPER_API_KEY не найден в .env файле")
    print("   💡 Получите бесплатный ключ (2500 запросов): https://serper.dev/")

print()

# ===== ПРОВЕРКА 3: BRAVE SEARCH =====
print("3️⃣  Проверка Brave Search API...")

brave_key = os.getenv("BRAVE_API_KEY")
if brave_key:
    print(f"   ✅ BRAVE_API_KEY найден: {brave_key[:10]}...{brave_key[-10:]}")
    
    # Тестовый запрос
    try:
        response = requests.get(
            "https://api.search.brave.com/res/v1/web/search",
            headers={
                "Accept": "application/json",
                "X-Subscription-Token": brave_key
            },
            params={"q": "test", "count": 1},
            timeout=10
        )
        
        if response.status_code == 200:
            print("   ✅ API работает! Тестовый поиск выполнен успешно")
            data = response.json()
            if "web" in data and "results" in data["web"]:
                print(f"   ✅ Получено результатов: {len(data['web']['results'])}")
        elif response.status_code == 401:
            print("   ❌ Неверный API ключ (401 Unauthorized)")
        elif response.status_code == 429:
            print("   ⚠️  Превышен лимит запросов (429 Too Many Requests)")
        else:
            print(f"   ❌ Ошибка API: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Ошибка при проверке: {e}")
else:
    print("   ⚠️  BRAVE_API_KEY не найден в .env файле")
    print("   💡 Получите бесплатный ключ: https://brave.com/search/api/")

print()

# ===== ПРОВЕРКА 3: SERPAPI =====
print("3️⃣  Проверка SerpAPI...")

serpapi_key = os.getenv("SERPAPI_KEY")
if serpapi_key:
    print(f"   ✅ SERPAPI_KEY найден: {serpapi_key[:10]}...{serpapi_key[-10:]}")
    
    # Тестовый запрос
    try:
        response = requests.get(
            "https://serpapi.com/search",
            params={
                "q": "test",
                "api_key": serpapi_key,
                "engine": "google",
                "num": 1
            },
            timeout=10
        )
        
        if response.status_code == 200:
            print("   ✅ API работает! Тестовый поиск выполнен успешно")
            data = response.json()
            
            # Проверяем оставшиеся запросы
            if "search_metadata" in data:
                print(f"   ℹ️  Поиск занял: {data['search_metadata'].get('total_time_taken', 'N/A')} сек")
            
            # Проверяем аккаунт инфо
            try:
                account_response = requests.get(
                    "https://serpapi.com/account",
                    params={"api_key": serpapi_key},
                    timeout=5
                )
                if account_response.status_code == 200:
                    account_data = account_response.json()
                    searches_left = account_data.get("plan_searches_left", "N/A")
                    print(f"   ℹ️  Осталось запросов: {searches_left}")
            except:
                pass
                
        elif response.status_code == 401:
            print("   ❌ Неверный API ключ (401 Unauthorized)")
        else:
            print(f"   ❌ Ошибка API: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Ошибка при проверке: {e}")
else:
    print("   ⚠️  SERPAPI_KEY не найден в .env файле")
    print("   💡 Получите бесплатный ключ (100 запросов): https://serpapi.com/")

print()

# ===== ИТОГОВАЯ СВОДКА =====
print("="*60)
print("ИТОГОВАЯ СВОДКА")
print("="*60)

working_apis = 0
total_apis = 4

if hf_token:
    working_apis += 1
    print("✅ Hugging Face Token")
else:
    print("❌ Hugging Face Token - НУЖЕН!")

if serper_key:
    working_apis += 1
    print("✅ Serper.dev API")
else:
    print("⚠️  Serper.dev API - рекомендуется")

if brave_key:
    working_apis += 1
    print("✅ Brave Search API")
else:
    print("⚠️  Brave Search API - опционально")

if serpapi_key:
    working_apis += 1
    print("✅ SerpAPI")
else:
    print("⚠️  SerpAPI - опционально")

print()
print(f"Настроено API: {working_apis}/{total_apis}")

if not hf_token:
    print("\n❌ КРИТИЧЕСКАЯ ОШИБКА:")
    print("HF_TOKEN обязателен для работы агента!")
    print("Получите токен: https://huggingface.co/settings/tokens")

if not serper_key and not brave_key and not serpapi_key:
    print("\n⚠️  ПРЕДУПРЕЖДЕНИЕ:")
    print("Не настроен ни один поисковый API!")
    print("Рекомендуется получить Serper API: https://serper.dev/")
    print("Или Brave Search API: https://brave.com/search/api/")

if hf_token and (serper_key or brave_key or serpapi_key):
    print("\n🎉 ВСЁ ГОТОВО!")
    if serper_key:
        print("Запустите: python serper_agent.py")
    else:
        print("Запустите: python real_search_agent.py")

print("="*60)
