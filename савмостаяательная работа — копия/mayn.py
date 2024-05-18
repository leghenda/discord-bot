import discord
from random import randint
import requests
import random
import asyncio

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

TOKEN = 'YOUR_DISCORD_BOT_TOKEN'
WEATHER_API_KEY = '62b0c0b5f22d40223203f8b2e9f2b78d'
WEATHER_API_URL = 'http://api.openweathermap.org/data/2.5/weather'

def get_questions_from_file():
    with open('viktorina.txt', 'r', encoding='utf-8') as f:
        qs = f.read().split('\n')[:-1]

    questions = []
    for q in qs:
        question, answer = q.split('|')
        questions.append({"question": question, "answer": answer})
    return questions

questions = get_questions_from_file()

def kelvin_to_celsius(temp):
    return temp - 273.15

def get_weather_data(city):
    try:
        response = requests.get(f'{WEATHER_API_URL}?q={city}&appid={WEATHER_API_KEY}')
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except Exception as e:
        print(f'Ошибка при получении данных о погоде: {e}')
        return None

# Определение событий on_ready и on_message
@client.event
async def on_ready():
    print('Бот готов к работе.')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('погода'):
        city = message.content.split(' ', 1)[1]
        weather_data = get_weather_data(city)
        
        if weather_data:
            weather_description = weather_data['weather'][0]['description']
            temperature = kelvin_to_celsius(weather_data['main']['temp'])
            humidity = weather_data['main']['humidity']
            wind_speed = weather_data['wind']['speed']
            
            response = (f'Погода в городе {city}:\n'
                        f'Описание: {weather_description}\n'
                        f'Температура: {temperature}°C\n'
                        f'Влажность: {humidity}%\n'
                        f'Скорость ветра: {wind_speed} м/с')
            await message.channel.send(response)
        else:
            await message.channel.send(f'Не удалось получить погоду для города {city}. Пожалуйста, попробуйте снова.')
           
    elif message.content == "конец света":
        images = [
            r"C:\Users\TUF\Desktop\савмостаяательная работа\Без названия (1).jpeg",
            r"C:\Users\TUF\Desktop\савмостаяательная работа\Без названия (2).jpeg",
            r"C:\Users\TUF\Desktop\савмостаяательная работа\Без названия.jpeg",
            # Добавьте остальные пути к изображениям
        ]
        random_image = random.choice(images)
        file = discord.File(random_image)
        
        await message.channel.send(file=file)
        await message.channel.send("вот что будет если мы не будем беречь нашу планету")

    elif message.content.startswith('тест'):
        await message.channel.send("Добро пожаловать в Викторину которая проверит ваши знание про голобальное потипление! Ответьте на следующие вопросы.")
        random.shuffle(questions)
        score = 0
        for q in questions:
            await message.channel.send(q["question"])
            try:
                response = await client.wait_for('message', timeout=60, check=lambda m: m.author == message.author)
            except asyncio.TimeoutError:
                await message.channel.send("Время вышло! Викторина завершена.")
                break
            if response.content == q["answer"]:
                score += 1
                await message.channel.send("Правильно!")
            else:
                await message.channel.send(f"Неправильно! Правильный ответ: {q['answer']}.")
        await message.channel.send(f"Викторина завершена! Ваш счет: {score}/{len(questions)}")


   


client.run('ваш токен бота')
