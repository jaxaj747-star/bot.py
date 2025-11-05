import os
from aiogram import Bot, Dispatcher, Router, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("8532872889:AAHa7YANNJrhqpH98PI8JCNUxE2Q16uxb0Q")
bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)
router = Router()

class PhoneStates(StatesGroup):
    brand = State()
    model = State()
    box_docs = State()
    battery = State()
    region = State()
    storage = State()
    color = State()
    condition = State()  # "Zarar" emas, balki "Holat"
    final = State()

# START
@router.message(Command("start"))
async def start_handler(message: types.Message, state: FSMContext):
    await state.clear()
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📱 iPhone", callback_data="brand_iphone")],
        [InlineKeyboardButton(text="📱 Samsung", callback_data="brand_samsung")],
    ])
    await message.answer(
        "Assalomu Aleykum! Xush kelibsiz 🎉\n"
        "Telefoningizni ajoyib narxda baholating!",
        reply_markup=kb
    )
    await state.set_state(PhoneStates.brand)

# Brend tanlash
@router.callback_query(lambda c: c.data.startswith("brand_"))
async def choose_brand(callback: types.CallbackQuery, state: FSMContext):
    brand = "iPhone" if callback.data == "brand_iphone" else "Samsung"
    await state.update_data(brand=brand)
    await callback.answer()

    if brand == "iPhone":
        models = [
            "iPhone 11", "iPhone 11 Pro", "iPhone 11 Pro Max",
            "iPhone 12", "iPhone 12 Mini", "iPhone 12 Pro", "iPhone 12 Pro Max",
            "iPhone 13", "iPhone 13 Mini", "iPhone 13 Pro", "iPhone 13 Pro Max",
            "iPhone 14", "iPhone 14 Plus", "iPhone 14 Pro", "iPhone 14 Pro Max",
            "iPhone 15", "iPhone 15 Plus", "iPhone 15 Pro", "iPhone 15 Pro Max",
            "iPhone 16", "iPhone 16 Plus", "iPhone 16 Pro", "iPhone 16 Pro Max",
            "iPhone 17"
        ]
    else:
        models = [
            "Galaxy S20", "Galaxy S20+", "Galaxy S20 Ultra",
            "Galaxy S21", "Galaxy S21+", "Galaxy S21 Ultra",
            "Galaxy S22", "Galaxy S22+", "Galaxy S22 Ultra",
            "Galaxy S23", "Galaxy S23+", "Galaxy S23 Ultra",
            "Galaxy S24", "Galaxy S24+", "Galaxy S24 Ultra",
            "Galaxy S25", "Galaxy S25+", "Galaxy S25 Ultra"
        ]

    builder = InlineKeyboardBuilder()
    for model in models:
        builder.button(text=model, callback_data=f"model_{model}")
    builder.adjust(2)

    await callback.message.edit_text("📱 Qaysi model?", reply_markup=builder.as_markup())
    await state.set_state(PhoneStates.model)

# Model tanlash
@router.callback_query(lambda c: c.data.startswith("model_"))
async def choose_model(callback: types.CallbackQuery, state: FSMContext):
    model = callback.data.replace("model_", "")
    await state.update_data(model=model)
    await callback.answer()

    data = await state.get_data()
    if data["brand"] == "iPhone":
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="✅ Ha", callback_data="box_yes")],
            [InlineKeyboardButton(text="❌ Yo'q", callback_data="box_no")]
        ])
        await callback.message.edit_text("📦 Karobka va hujjatlar bormi?", reply_markup=kb)
        await state.set_state(PhoneStates.box_docs)
    else:
        await ask_battery(callback.message, state)

# Karobka (iPhone)
@router.callback_query(lambda c: c.data.startswith("box_"))
async def choose_box(callback: types.CallbackQuery, state: FSMContext):
    await state.update_data(box_docs=(callback.data == "box_yes"))
    await callback.answer()
    await ask_battery(callback.message, state)

# Batareya
async def ask_battery(message: types.Message, state: FSMContext):
    await message.edit_text("🔋 Batareya sog'lig'ini foizda kiriting (masalan: 88):")
    await state.set_state(PhoneStates.battery)

@router.message(PhoneStates.battery)
async def get_battery(message: types.Message, state: FSMContext):
    try:
        battery = int(message.text)
        if not (1 <= battery <= 100):
            raise ValueError
        await state.update_data(battery=battery)
        await ask_region(message, state)
    except:
        await message.answer("Iltimos, 1-100 oralig'ida butun son kiriting:")
        return

# Hudud
async def ask_region(message: types.Message, state: FSMContext):
    regions = ["🇺🇸 AQSH", "🇪🇺 Yevropa", "🇨🇳 Xitoy", "🇯🇵 Yaponiya", "🇰🇷 Janubiy Koreya", "🌍 Boshqa"]
    builder = InlineKeyboardBuilder()
    for r in regions:
        builder.button(text=r, callback_data=f"region_{r}")
    builder.adjust(2)
    await message.answer("📍 Hududingizni tanlang:", reply_markup=builder.as_markup())
    await state.set_state(PhoneStates.region)

@router.callback_query(lambda c: c.data.startswith("region_"))
async def choose_region(callback: types.CallbackQuery, state: FSMContext):
    region = callback.data.replace("region_", "")
    await state.update_data(region=region)
    await callback.answer()
    await ask_storage(callback.message, state)

# Xotira
async def ask_storage(message: types.Message, state: FSMContext):
    storages = ["64 GB", "128 GB", "256 GB", "512 GB", "1 TB"]
    builder = InlineKeyboardBuilder()
    for s in storages:
        builder.button(text=s, callback_data=f"storage_{s}")
    builder.adjust(2)
    await message.answer("💾 Xotira hajmini tanlang:", reply_markup=builder.as_markup())
    await state.set_state(PhoneStates.storage)

@router.callback_query(lambda c: c.data.startswith("storage_"))
async def choose_storage(callback: types.CallbackQuery, state: FSMContext):
    storage = callback.data.replace("storage_", "")
    await state.update_data(storage=storage)
    await callback.answer()
    await ask_color(callback.message, state)

# Rang
async def ask_color(message: types.Message, state: FSMContext):
    colors = ["Qora", "Oq", "Ko'k", "Yashil", "Qizil", "Sariq", "Binafsha", "Kulrang", "Tasodifiy"]
    builder = InlineKeyboardBuilder()
    for c in colors:
        builder.button(text=c, callback_data=f"color_{c}")
    builder.adjust(3)
    await message.answer("🎨 Rangini tanlang:", reply_markup=builder.as_markup())
    await state.set_state(PhoneStates.color)

@router.callback_query(lambda c: c.data.startswith("color_"))
async def choose_color(callback: types.CallbackQuery, state: FSMContext):
    color = callback.data.replace("color_", "")
    await state.update_data(color=color)
    await callback.answer()
    await ask_condition(callback.message, state)

# Holat (Zarar emas!)
async def ask_condition(message: types.Message, state: FSMContext):
    options = [
        "Ko'p ehtimoliylikda umuman yoriq, qirilish yo'q",
        "1-3 ta kichik yoriq yoki shikast",
        "4-7 ta ayon yoriq/shikast",
        "8+ ta katta shikast yoki yoriq"
    ]
    builder = InlineKeyboardBuilder()
    for opt in options:
        builder.button(text=opt, callback_data=f"cond_{opt}")
    builder.adjust(1)
    await message.answer("📋 Telefonning joriy holatini tanlang:", reply_markup=builder.as_markup())
    await state.set_state(PhoneStates.condition)

@router.callback_query(lambda c: c.data.startswith("cond_"))
async def choose_condition(callback: types.CallbackQuery, state: FSMContext):
    condition = callback.data.replace("cond_", "")
    await state.update_data(condition=condition)
    await callback.answer()
    await calculate_price(callback.message, state)

# Narx hisoblash
async def calculate_price(message: types.Message, state: FSMContext):
    data = await state.get_data()
    brand = data["brand"]
    model = data["model"]
    battery = data["battery"]
    region = data["region"]
    storage = data["storage"]
    condition = data["condition"]

    base_price = 0

    # iPhone asosiy narxlari
    if brand == "iPhone":
        if "11" in model:
            base_price = 280 if "Pro Max" in model else (260 if "Pro" in model else 230)
        elif "12" in model:
            base_price = 350 if "Pro Max" in model else (330 if "Pro" in model else (300 if "Mini" in model else 310))
        elif "13" in model:
            base_price = 450 if "Pro Max" in model else (430 if "Pro" in model else (400 if "Mini" in model else 410))
        elif "14" in model:
            base_price = 550 if "Pro Max" in model else (530 if "Pro" in model else (490 if "Plus" in model else 500))
        elif "15" in model:
            base_price = 700 if "Pro Max" in model else (680 if "Pro" in model else (630 if "Plus" in model else 640))
        elif "16" in model:
            base_price = 820 if "Pro Max" in model else (800 if "Pro" in model else (750 if "Plus" in model else 760))
        elif "17" in model:
            base_price = 900
        else:
            base_price = 400

        if data.get("box_docs"):
            base_price += 40

    # Samsung
    else:
        if "S20" in model:
            base_price = 220 if "Ultra" in model else (200 if "+" in model else 180)
        elif "S21" in model:
            base_price = 260 if "Ultra" in model else (240 if "+" in model else 220)
        elif "S22" in model:
            base_price = 320 if "Ultra" in model else (300 if "+" in model else 280)
        elif "S23" in model:
            base_price = 420 if "Ultra" in model else (400 if "+" in model else 380)
        elif "S24" in model:
            base_price = 520 if "Ultra" in model else (500 if "+" in model else 480)
        elif "S25" in model:
            base_price = 620 if "Ultra" in model else (600 if "+" in model else 580)
        else:
            base_price = 350

    # Xotira ta'siri
    if "512" in storage or "1 TB" in storage:
        base_price += 70
    elif "256" in storage:
        base_price += 40
    elif "64" in storage:
        base_price -= 40

    # Batareya
    if battery >= 95:
        base_price += 25
    elif battery >= 85:
        pass
    elif battery >= 75:
        base_price -= 30
    else:
        base_price -= 70

    # Holat
    if "umuman yoriq" in condition.lower():
        base_price += 60
    elif "1-3" in condition:
        base_price -= 20
    elif "4-7" in condition:
        base_price -= 60
    elif "8+" in condition:
        base_price -= 120

    final_price = max(50, round(base_price))

    result = (
        f"✅ Baholash yakunlandi!\n\n"
        f"📱 {brand} {model}\n"
        f"🔋 Batareya: {battery}%\n"
        f"📍 Hudud: {region}\n"
        f"💾 Xotira: {storage}\n"
        f"🎨 Rang: {data['color']}\n"
        f"📋 Holat: {condition}\n\n"
        f"💡 Taxminiy sotish narxi: <b>${final_price}</b>"
    )

    await message.answer(result, parse_mode="HTML")
    await state.clear()

# Router va ishga tushirish
dp.include_router(router)

if __name__ == "__main__":
    import asyncio
    print("Bot ishga tushdi...")
    asyncio.run(dp.start_polling(bot))
