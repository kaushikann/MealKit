import streamlit as st
import json
import os
from datetime import datetime, timedelta
from io import BytesIO

# ─────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="NutriSupply",
    page_icon="🥗",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────────────────────
# GLOBAL STYLES
# ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: #0A0F0D;
    color: #E8F5E9;
}
.stApp { background-color: #0A0F0D; }

h1, h2, h3 { font-family: 'DM Serif Display', serif !important; color: #E8F5E9 !important; }

/* Hide default streamlit elements */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 1.5rem; padding-bottom: 3rem; max-width: 960px; }

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #4ADE80, #22C55E) !important;
    color: #0A0F0D !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 700 !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 10px 24px !important;
    transition: all 0.2s !important;
}
.stButton > button:hover { opacity: 0.88 !important; transform: translateY(-1px) !important; }

/* Secondary button */
.stButton > button[kind="secondary"] {
    background: transparent !important;
    border: 1.5px solid #1E3325 !important;
    color: #6B8F71 !important;
}

/* Text input / text area */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    background-color: #111A14 !important;
    border: 1px solid #1E3325 !important;
    color: #E8F5E9 !important;
    border-radius: 10px !important;
    font-family: 'DM Sans', sans-serif !important;
}

/* Selectbox */
.stSelectbox > div > div {
    background-color: #111A14 !important;
    border: 1px solid #1E3325 !important;
    color: #E8F5E9 !important;
    border-radius: 10px !important;
}

/* Multiselect */
.stMultiSelect > div > div {
    background-color: #111A14 !important;
    border: 1px solid #1E3325 !important;
    border-radius: 10px !important;
}

/* Checkbox */
.stCheckbox label { color: #E8F5E9 !important; }

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background-color: #111A14;
    border-radius: 12px;
    padding: 4px;
    gap: 4px;
}
.stTabs [data-baseweb="tab"] {
    background-color: transparent !important;
    color: #6B8F71 !important;
    font-weight: 600 !important;
    border-radius: 8px !important;
    font-family: 'DM Sans', sans-serif !important;
}
.stTabs [aria-selected="true"] {
    background-color: #14532D !important;
    color: #4ADE80 !important;
}

/* Expander */
.streamlit-expanderHeader {
    background-color: #111A14 !important;
    border: 1px solid #1E3325 !important;
    border-radius: 10px !important;
    color: #E8F5E9 !important;
    font-weight: 600 !important;
}
.streamlit-expanderContent {
    background-color: #111A14 !important;
    border: 1px solid #1E3325 !important;
    border-radius: 0 0 10px 10px !important;
}

/* Divider */
hr { border-color: #1E3325 !important; }

/* Metric */
[data-testid="metric-container"] {
    background: #111A14;
    border: 1px solid #1E3325;
    border-radius: 12px;
    padding: 14px !important;
}
[data-testid="metric-container"] label { color: #6B8F71 !important; font-size: 12px !important; }
[data-testid="metric-container"] [data-testid="metric-value"] { color: #4ADE80 !important; font-family: 'DM Serif Display', serif !important; }

/* Custom cards */
.nutri-card {
    background: #111A14;
    border: 1px solid #1E3325;
    border-radius: 16px;
    padding: 20px;
    margin-bottom: 14px;
    transition: border-color 0.2s;
}
.nutri-card:hover { border-color: #14532D; }
.nutri-card-accent { border-color: #14532D; background: linear-gradient(135deg, #111A14 0%, #0E2018 100%); }

.choice-card {
    background: #111A14;
    border: 2px solid #1E3325;
    border-radius: 20px;
    padding: 32px 24px;
    text-align: center;
    cursor: pointer;
    transition: all 0.25s;
    height: 220px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}
.choice-card:hover { border-color: #4ADE80; background: #162019; transform: translateY(-3px); }

.badge {
    display: inline-block;
    padding: 3px 12px;
    border-radius: 100px;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.5px;
}
.badge-green { background: #14532D; color: #4ADE80; }
.badge-orange { background: #2D1F0E; color: #FB923C; }
.badge-purple { background: #1A1030; color: #A78BFA; }
.badge-blue { background: #0F1E30; color: #60A5FA; }
.badge-yellow { background: #2D2200; color: #FCD34D; }

.ing-chip {
    display: inline-block;
    background: #162019;
    border: 1px solid #1E3325;
    border-radius: 8px;
    padding: 4px 10px;
    font-size: 12px;
    color: #6B8F71;
    margin: 3px;
}
.ing-chip strong { color: #E8F5E9; }

.logo-text {
    font-family: 'DM Serif Display', serif;
    font-size: 28px;
    color: #4ADE80;
}
.logo-text span { color: #E8F5E9; }

.page-title {
    font-family: 'DM Serif Display', serif;
    font-size: 32px;
    color: #E8F5E9;
    margin-bottom: 4px;
}
.page-sub { color: #6B8F71; font-size: 14px; margin-bottom: 24px; }

.nutrition-bar-wrap { margin: 6px 0; }
.nutrition-label { display: flex; justify-content: space-between; font-size: 12px; margin-bottom: 3px; }
.nutrition-bar { height: 6px; border-radius: 3px; background: #1E3325; overflow: hidden; }
.nutrition-fill { height: 100%; border-radius: 3px; }

.dish-card {
    background: #111A14;
    border: 1.5px solid #1E3325;
    border-radius: 16px;
    padding: 18px;
    margin-bottom: 10px;
    transition: all 0.2s;
}
.dish-card.selected { border-color: #4ADE80; background: #0E2018; }

.order-card {
    background: #111A14;
    border: 1px solid #1E3325;
    border-radius: 14px;
    padding: 18px;
    margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# DISH CATALOGUE DATA
# ─────────────────────────────────────────────────────────────
DISH_CATALOGUE = {
    "🧀 Paneer Butter Masala": {
        "emoji": "🧀",
        "category": "North Indian",
        "diet": ["Vegetarian", "Gluten-Free"],
        "calories": 320,
        "cook_time": "30 min",
        "description": "Rich, creamy tomato-based curry with soft paneer cubes. A North Indian classic.",
        "ingredients": [
            {"name": "Paneer", "qty": "150g", "protein_pct": 18, "carb_pct": 3, "fat_pct": 22, "fiber_pct": 0, "price": 1.20},
            {"name": "Tomatoes", "qty": "120g", "protein_pct": 1, "carb_pct": 4, "fat_pct": 0, "fiber_pct": 1, "price": 0.30},
            {"name": "Onion", "qty": "60g", "protein_pct": 1, "carb_pct": 9, "fat_pct": 0, "fiber_pct": 2, "price": 0.15},
            {"name": "Butter", "qty": "15g", "protein_pct": 0, "carb_pct": 0, "fat_pct": 81, "fiber_pct": 0, "price": 0.20},
            {"name": "Heavy Cream", "qty": "30ml", "protein_pct": 2, "carb_pct": 3, "fat_pct": 36, "fiber_pct": 0, "price": 0.25},
            {"name": "Ginger-Garlic Paste", "qty": "10g", "protein_pct": 2, "carb_pct": 6, "fat_pct": 0, "fiber_pct": 1, "price": 0.10},
            {"name": "Kashmiri Chilli Powder", "qty": "5g", "protein_pct": 3, "carb_pct": 18, "fat_pct": 12, "fiber_pct": 7, "price": 0.10},
            {"name": "Garam Masala", "qty": "3g", "protein_pct": 5, "carb_pct": 50, "fat_pct": 10, "fiber_pct": 15, "price": 0.10},
            {"name": "Kasuri Methi", "qty": "2g", "protein_pct": 23, "carb_pct": 58, "fat_pct": 6, "fiber_pct": 25, "price": 0.05},
            {"name": "Salt & Sugar", "qty": "to taste", "protein_pct": 0, "carb_pct": 0, "fat_pct": 0, "fiber_pct": 0, "price": 0.02},
        ],
        "recipe": [
            "Blanch tomatoes and blend to a smooth purée. Set aside.",
            "Sauté finely chopped onions in butter over medium heat until golden (8 min).",
            "Add ginger-garlic paste and cook 2 min until raw smell disappears.",
            "Pour in the tomato purée and simmer 10 min, stirring occasionally.",
            "Add Kashmiri chilli powder, garam masala, salt and a pinch of sugar.",
            "Cube paneer (2cm pieces) and gently fold into the gravy.",
            "Pour in heavy cream, stir well and simmer on low for 5 min.",
            "Crush kasuri methi between palms and sprinkle over the dish.",
            "Garnish with a swirl of cream and serve hot with naan or rice.",
        ],
        "nutrition_per_100g": {"Calories": "185 kcal", "Protein": "9.2g", "Carbs": "8.4g", "Fat": "13.5g", "Fiber": "1.2g"},
    },
    "🍚 Veg Biryani": {
        "emoji": "🍚",
        "category": "Mughlai",
        "diet": ["Vegetarian", "Vegan-optional"],
        "calories": 380,
        "cook_time": "45 min",
        "description": "Fragrant basmati rice layered with spiced vegetables and whole spices.",
        "ingredients": [
            {"name": "Basmati Rice", "qty": "100g (dry)", "protein_pct": 7, "carb_pct": 78, "fat_pct": 1, "fiber_pct": 1, "price": 0.40},
            {"name": "Mixed Vegetables (carrot, peas, beans)", "qty": "150g", "protein_pct": 3, "carb_pct": 10, "fat_pct": 0, "fiber_pct": 4, "price": 0.50},
            {"name": "Onion (thinly sliced)", "qty": "80g", "protein_pct": 1, "carb_pct": 9, "fat_pct": 0, "fiber_pct": 2, "price": 0.15},
            {"name": "Yogurt", "qty": "50g", "protein_pct": 4, "carb_pct": 5, "fat_pct": 3, "fiber_pct": 0, "price": 0.20},
            {"name": "Ghee", "qty": "15ml", "protein_pct": 0, "carb_pct": 0, "fat_pct": 99, "fiber_pct": 0, "price": 0.30},
            {"name": "Whole Spices (bay leaf, cloves, cardamom, star anise)", "qty": "5g", "protein_pct": 4, "carb_pct": 65, "fat_pct": 8, "fiber_pct": 28, "price": 0.15},
            {"name": "Biryani Masala", "qty": "8g", "protein_pct": 5, "carb_pct": 45, "fat_pct": 10, "fiber_pct": 12, "price": 0.15},
            {"name": "Saffron", "qty": "a pinch", "protein_pct": 12, "carb_pct": 65, "fat_pct": 6, "fiber_pct": 4, "price": 0.50},
            {"name": "Mint Leaves", "qty": "10g", "protein_pct": 3, "carb_pct": 14, "fat_pct": 1, "fiber_pct": 7, "price": 0.10},
            {"name": "Fried Onions (birista)", "qty": "20g", "protein_pct": 2, "carb_pct": 24, "fat_pct": 14, "fiber_pct": 2, "price": 0.25},
        ],
        "recipe": [
            "Wash and soak basmati rice for 30 minutes. Drain and parboil with whole spices until 70% cooked.",
            "In a heavy-bottomed pot, heat ghee and fry sliced onions until deep golden (birista).",
            "Add ginger-garlic paste, then marinated vegetables mixed with yogurt and biryani masala.",
            "Cook vegetables on medium heat until semi-tender (8 min).",
            "Dissolve saffron in 2 tbsp warm milk.",
            "Layer parboiled rice over vegetables. Drizzle saffron milk and ghee.",
            "Top with mint leaves and half the fried onions.",
            "Seal the pot with a tight lid (or dough seal) and cook on dum (low heat) for 20 min.",
            "Gently fluff and mix. Garnish with remaining fried onions and serve with raita.",
        ],
        "nutrition_per_100g": {"Calories": "148 kcal", "Protein": "4.1g", "Carbs": "28.2g", "Fat": "2.8g", "Fiber": "2.1g"},
    },
    "🍜 Thai Green Curry": {
        "emoji": "🍜",
        "category": "Thai",
        "diet": ["Vegan", "Gluten-Free"],
        "calories": 290,
        "cook_time": "25 min",
        "description": "Aromatic coconut milk curry with fresh vegetables and fragrant Thai herbs.",
        "ingredients": [
            {"name": "Coconut Milk (full fat)", "qty": "200ml", "protein_pct": 2, "carb_pct": 6, "fat_pct": 24, "fiber_pct": 0, "price": 0.80},
            {"name": "Thai Green Curry Paste", "qty": "25g", "protein_pct": 3, "carb_pct": 15, "fat_pct": 8, "fiber_pct": 2, "price": 0.40},
            {"name": "Tofu (firm)", "qty": "120g", "protein_pct": 8, "carb_pct": 2, "fat_pct": 5, "fiber_pct": 0, "price": 0.60},
            {"name": "Zucchini", "qty": "80g", "protein_pct": 1, "carb_pct": 3, "fat_pct": 0, "fiber_pct": 1, "price": 0.25},
            {"name": "Bell Pepper (red + green)", "qty": "80g", "protein_pct": 1, "carb_pct": 7, "fat_pct": 0, "fiber_pct": 2, "price": 0.30},
            {"name": "Baby Spinach", "qty": "40g", "protein_pct": 3, "carb_pct": 4, "fat_pct": 0, "fiber_pct": 2, "price": 0.20},
            {"name": "Lemongrass", "qty": "1 stalk", "protein_pct": 1, "carb_pct": 25, "fat_pct": 1, "fiber_pct": 0, "price": 0.20},
            {"name": "Kaffir Lime Leaves", "qty": "4 leaves", "protein_pct": 0, "carb_pct": 0, "fat_pct": 0, "fiber_pct": 3, "price": 0.15},
            {"name": "Fish Sauce / Soy Sauce", "qty": "10ml", "protein_pct": 4, "carb_pct": 3, "fat_pct": 0, "fiber_pct": 0, "price": 0.10},
            {"name": "Palm Sugar / Brown Sugar", "qty": "5g", "protein_pct": 0, "carb_pct": 98, "fat_pct": 0, "fiber_pct": 0, "price": 0.05},
            {"name": "Thai Basil", "qty": "10g", "protein_pct": 4, "carb_pct": 8, "fat_pct": 1, "fiber_pct": 3, "price": 0.15},
        ],
        "recipe": [
            "Press tofu firmly to remove excess moisture. Cube and pan-fry in a little oil until golden.",
            "In a wok or pan, heat 2 tbsp of the thick coconut cream (top layer) until it sizzles.",
            "Add green curry paste and fry for 2 min until fragrant.",
            "Add lemongrass (bruised), kaffir lime leaves and pour in remaining coconut milk.",
            "Bring to a gentle simmer. Add tofu, zucchini and bell peppers.",
            "Cook 7 min on medium. Season with fish sauce (or soy sauce) and palm sugar.",
            "Fold in baby spinach and Thai basil. Simmer 1 min more.",
            "Taste and balance — salty (fish sauce), sweet (sugar), spicy (paste).",
            "Serve over jasmine rice, garnished with fresh Thai basil and sliced chilli.",
        ],
        "nutrition_per_100g": {"Calories": "112 kcal", "Protein": "4.8g", "Carbs": "8.1g", "Fat": "7.2g", "Fiber": "1.8g"},
    },
    "🥘 Dal Makhani": {
        "emoji": "🥘",
        "category": "North Indian",
        "diet": ["Vegetarian", "Gluten-Free", "High Protein"],
        "calories": 280,
        "cook_time": "60 min",
        "description": "Slow-cooked whole black lentils in a buttery, smoky tomato gravy.",
        "ingredients": [
            {"name": "Whole Black Lentils (urad dal)", "qty": "80g (dry)", "protein_pct": 25, "carb_pct": 57, "fat_pct": 1, "fiber_pct": 11, "price": 0.35},
            {"name": "Kidney Beans (rajma)", "qty": "30g (dry)", "protein_pct": 24, "carb_pct": 60, "fat_pct": 1, "fiber_pct": 15, "price": 0.20},
            {"name": "Tomato Purée", "qty": "100ml", "protein_pct": 2, "carb_pct": 7, "fat_pct": 0, "fiber_pct": 1, "price": 0.25},
            {"name": "Butter", "qty": "20g", "protein_pct": 1, "carb_pct": 0, "fat_pct": 81, "fiber_pct": 0, "price": 0.25},
            {"name": "Heavy Cream", "qty": "30ml", "protein_pct": 2, "carb_pct": 3, "fat_pct": 36, "fiber_pct": 0, "price": 0.25},
            {"name": "Onion", "qty": "60g", "protein_pct": 1, "carb_pct": 9, "fat_pct": 0, "fiber_pct": 2, "price": 0.15},
            {"name": "Ginger-Garlic Paste", "qty": "12g", "protein_pct": 2, "carb_pct": 6, "fat_pct": 0, "fiber_pct": 1, "price": 0.10},
            {"name": "Chilli Powder", "qty": "4g", "protein_pct": 3, "carb_pct": 18, "fat_pct": 12, "fiber_pct": 7, "price": 0.05},
            {"name": "Garam Masala", "qty": "3g", "protein_pct": 5, "carb_pct": 50, "fat_pct": 10, "fiber_pct": 15, "price": 0.05},
            {"name": "Salt", "qty": "to taste", "protein_pct": 0, "carb_pct": 0, "fat_pct": 0, "fiber_pct": 0, "price": 0.02},
        ],
        "recipe": [
            "Soak urad dal and rajma overnight (minimum 8 hours). Drain.",
            "Pressure cook lentils with salt and water for 6-7 whistles (or 45 min). They should be very soft.",
            "In a heavy pan, melt butter and sauté finely diced onions until deep golden.",
            "Add ginger-garlic paste, cook 3 min. Add tomato purée and simmer 12 min.",
            "Add chilli powder, garam masala. Cook the masala until oil separates.",
            "Add cooked lentils (with cooking liquid) to the masala. Stir well.",
            "Simmer on very low heat for 20-30 min, stirring every 5 min (longer = better).",
            "Add cream, stir gently. Adjust salt.",
            "Optional: finish with a coal smoke (dhungar) for authentic restaurant flavour.",
            "Garnish with butter and cream swirl. Serve with naan.",
        ],
        "nutrition_per_100g": {"Calories": "138 kcal", "Protein": "9.4g", "Carbs": "18.2g", "Fat": "3.8g", "Fiber": "5.6g"},
    },
    "🥗 Mediterranean Quinoa Bowl": {
        "emoji": "🥗",
        "category": "Mediterranean",
        "diet": ["Vegan", "Gluten-Free", "Diabetic-Friendly"],
        "calories": 340,
        "cook_time": "20 min",
        "description": "Protein-rich quinoa with roasted veggies, chickpeas and lemon-herb dressing.",
        "ingredients": [
            {"name": "Quinoa", "qty": "80g (dry)", "protein_pct": 14, "carb_pct": 64, "fat_pct": 6, "fiber_pct": 7, "price": 0.70},
            {"name": "Chickpeas (cooked)", "qty": "100g", "protein_pct": 19, "carb_pct": 61, "fat_pct": 6, "fiber_pct": 17, "price": 0.35},
            {"name": "Cherry Tomatoes", "qty": "80g", "protein_pct": 1, "carb_pct": 4, "fat_pct": 0, "fiber_pct": 1, "price": 0.40},
            {"name": "Cucumber", "qty": "60g", "protein_pct": 1, "carb_pct": 4, "fat_pct": 0, "fiber_pct": 1, "price": 0.20},
            {"name": "Red Onion", "qty": "30g", "protein_pct": 1, "carb_pct": 9, "fat_pct": 0, "fiber_pct": 2, "price": 0.10},
            {"name": "Kalamata Olives", "qty": "20g", "protein_pct": 1, "carb_pct": 4, "fat_pct": 11, "fiber_pct": 3, "price": 0.30},
            {"name": "Roasted Bell Peppers", "qty": "60g", "protein_pct": 1, "carb_pct": 7, "fat_pct": 0, "fiber_pct": 2, "price": 0.30},
            {"name": "Extra Virgin Olive Oil", "qty": "15ml", "protein_pct": 0, "carb_pct": 0, "fat_pct": 100, "fiber_pct": 0, "price": 0.25},
            {"name": "Lemon Juice", "qty": "20ml", "protein_pct": 0, "carb_pct": 6, "fat_pct": 0, "fiber_pct": 0, "price": 0.10},
            {"name": "Fresh Herbs (parsley, mint)", "qty": "10g", "protein_pct": 3, "carb_pct": 6, "fat_pct": 1, "fiber_pct": 3, "price": 0.15},
        ],
        "recipe": [
            "Rinse quinoa well. Cook in 1.5x water (salted) for 15 min until fluffy. Fluff with fork.",
            "Drain and rinse chickpeas. Toss with olive oil, cumin, salt and roast at 200°C for 20 min until crispy.",
            "Halve cherry tomatoes, dice cucumber, thinly slice red onion.",
            "Make dressing: whisk olive oil, lemon juice, minced garlic, salt and pepper.",
            "Combine quinoa, chickpeas and all vegetables in a large bowl.",
            "Pour dressing over and toss well.",
            "Top with olives, fresh herbs and optional crumbled feta.",
            "Serve immediately or refrigerate — tastes even better after 1 hour.",
        ],
        "nutrition_per_100g": {"Calories": "156 kcal", "Protein": "6.8g", "Carbs": "22.4g", "Fat": "5.1g", "Fiber": "4.3g"},
    },
    "🐟 Baked Lemon Herb Salmon": {
        "emoji": "🐟",
        "category": "Western",
        "diet": ["Keto", "High Protein", "Gluten-Free", "Diabetic-Friendly"],
        "calories": 350,
        "cook_time": "25 min",
        "description": "Omega-3-rich salmon fillet baked with fresh herbs, lemon and garlic.",
        "ingredients": [
            {"name": "Salmon Fillet", "qty": "200g", "protein_pct": 25, "carb_pct": 0, "fat_pct": 13, "fiber_pct": 0, "price": 4.50},
            {"name": "Lemon", "qty": "1 medium", "protein_pct": 1, "carb_pct": 11, "fat_pct": 0, "fiber_pct": 3, "price": 0.30},
            {"name": "Garlic Cloves", "qty": "3 cloves", "protein_pct": 4, "carb_pct": 33, "fat_pct": 1, "fiber_pct": 2, "price": 0.10},
            {"name": "Fresh Dill", "qty": "8g", "protein_pct": 3, "carb_pct": 7, "fat_pct": 1, "fiber_pct": 2, "price": 0.20},
            {"name": "Fresh Parsley", "qty": "8g", "protein_pct": 3, "carb_pct": 6, "fat_pct": 1, "fiber_pct": 3, "price": 0.15},
            {"name": "Olive Oil", "qty": "15ml", "protein_pct": 0, "carb_pct": 0, "fat_pct": 100, "fiber_pct": 0, "price": 0.25},
            {"name": "Dijon Mustard", "qty": "8g", "protein_pct": 4, "carb_pct": 8, "fat_pct": 4, "fiber_pct": 2, "price": 0.15},
            {"name": "Capers (optional)", "qty": "10g", "protein_pct": 2, "carb_pct": 4, "fat_pct": 1, "fiber_pct": 2, "price": 0.20},
            {"name": "Salt & Black Pepper", "qty": "to taste", "protein_pct": 0, "carb_pct": 0, "fat_pct": 0, "fiber_pct": 0, "price": 0.02},
        ],
        "recipe": [
            "Preheat oven to 200°C (400°F). Line a baking tray with parchment paper.",
            "Pat salmon dry. Season both sides with salt and pepper.",
            "Mix olive oil, Dijon mustard, minced garlic, chopped dill and parsley.",
            "Spread the herb mixture generously over the top of the salmon.",
            "Lay lemon slices over and around the salmon.",
            "Bake 12-15 min depending on thickness (internal temp 63°C / 145°F).",
            "Rest 2 min before serving.",
            "Serve with steamed greens, quinoa or cauliflower rice.",
            "Top with capers and a final squeeze of lemon.",
        ],
        "nutrition_per_100g": {"Calories": "176 kcal", "Protein": "20.4g", "Carbs": "1.2g", "Fat": "9.8g", "Fiber": "0.4g"},
    },
}

DIET_OPTIONS = ["All", "Vegetarian", "Vegan", "Keto", "High Protein", "Gluten-Free", "Diabetic-Friendly"]

BAR_COLORS = {
    "protein": "#4ADE80",
    "carb": "#60A5FA",
    "fat": "#FB923C",
    "fiber": "#A78BFA",
}

# ─────────────────────────────────────────────────────────────
# SESSION STATE INIT
# ─────────────────────────────────────────────────────────────
def init_state():
    defaults = {
        "mode": None,           # "plan" or "explore"
        "meal_plan_result": None,
        "meals": {},            # {meal_name: [dish_key, ...]}
        "active_meal": None,
        "orders": [],
        "scheduled": {},        # {date_str: [dish_key, ...]}
        "view_dish": None,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

# ─────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────
def nutrition_bar(label, pct, color):
    pct_capped = min(max(pct, 0), 100)
    st.markdown(f"""
    <div class='nutrition-bar-wrap'>
        <div class='nutrition-label'><span style='color:#6B8F71'>{label}</span><span style='color:#E8F5E9;font-weight:600'>{pct}%</span></div>
        <div class='nutrition-bar'><div class='nutrition-fill' style='width:{pct_capped}%;background:{color}'></div></div>
    </div>
    """, unsafe_allow_html=True)

def render_badge(text, color_class):
    st.markdown(f"<span class='badge {color_class}'>{text}</span>", unsafe_allow_html=True)

def get_week_days():
    days = []
    today = datetime.today()
    for i in range(7):
        d = today + timedelta(days=i)
        days.append({
            "label": d.strftime("%a, %b %d"),
            "key": d.strftime("%Y-%m-%d"),
            "short": d.strftime("%a\n%d"),
        })
    return days

def total_order_price(dish_keys):
    total = 0.0
    for dk in dish_keys:
        dish = DISH_CATALOGUE.get(dk, {})
        total += sum(i.get("price", 0) for i in dish.get("ingredients", []))
    return round(total, 2)

def generate_recipe_text(dish_name, dish):
    lines = [f"RECIPE: {dish_name}", f"Category: {dish['category']} | Diet: {', '.join(dish['diet'])}", f"Calories: {dish['calories']} kcal | Cook Time: {dish['cook_time']}", "", dish['description'], "", "─" * 50, "INGREDIENTS (per 1 person)", "─" * 50]
    for ing in dish['ingredients']:
        lines.append(f"  • {ing['name']}: {ing['qty']}  [P:{ing['protein_pct']}% C:{ing['carb_pct']}% F:{ing['fat_pct']}% Fb:{ing['fiber_pct']}%]  ~${ing['price']:.2f}")
    lines += ["", "─" * 50, "RECIPE STEPS", "─" * 50]
    for i, step in enumerate(dish['recipe'], 1):
        lines.append(f"{i}. {step}")
    lines += ["", "─" * 50, f"NUTRITIONAL VALUES (per 100g)", "─" * 50]
    for k, v in dish['nutrition_per_100g'].items():
        lines.append(f"  {k}: {v}")
    lines.append(f"\nIngredient Cost (1 person): ${total_order_price([dish_name]):.2f}")
    return "\n".join(lines)

# ─────────────────────────────────────────────────────────────
# AI: ANALYZE MEAL PLAN
# ─────────────────────────────────────────────────────────────
def analyze_meal_plan_ai(plan_text, diet_type):

    prompt = f"""You are a nutrition expert. Parse this meal plan and return ONLY valid JSON (no markdown, no backticks).

Meal Plan:
{plan_text}
Diet Type: {diet_type}

Return this exact structure:
{{
  "meals": [
    {{
      "id": "m1",
      "name": "Meal name",
      "type": "breakfast|lunch|snack|dinner",
      "calories": 380,
      "protein_g": 22,
      "carbs_g": 45,
      "fat_g": 12,
      "ingredients": [
        {{"name": "Oats", "qty": "60g", "price": 0.30, "protein_pct": 13, "carb_pct": 68, "fat_pct": 7, "fiber_pct": 10}}
      ],
      "notes": "Short nutrition tip"
    }}
  ],
  "diet_summary": "2-sentence summary of this plan for {diet_type}",
  "total_calories": 1800,
  "total_protein_g": 90,
  "estimated_daily_cost": 14.50
}}

Parse the EXACT meals from the plan. Return ONLY the JSON object."""

    try:
        lines = [l.strip() for l in plan_text.splitlines() if l.strip()]
        meals = []

        def guess_type(name: str) -> str:
            n = name.lower()
            if "breakfast" in n or "bf" in n:
                return "breakfast"
            if "lunch" in n:
                return "lunch"
            if "snack" in n:
                return "snack"
            if "dinner" in n or "supper" in n:
                return "dinner"
            return "lunch"

        def default_calories(meal_type: str) -> int:
            return {
                "breakfast": 400,
                "lunch": 600,
                "snack": 200,
                "dinner": 600,
            }.get(meal_type, 500)

        meal_id = 1
        for line in lines:
            if ":" in line:
                name_part, detail_part = line.split(":", 1)
                meal_name = name_part.strip()
                desc = detail_part.strip()
            else:
                meal_name = line
                desc = ""

            m_type = guess_type(meal_name)
            calories = default_calories(m_type)

            ingredients = []
            ing_source = ""
            if "(" in desc and ")" in desc:
                ing_source = desc[desc.index("(") + 1 : desc.rindex(")")]
            elif desc:
                ing_source = desc

            if ing_source:
                for raw in ing_source.split(","):
                    txt = raw.strip()
                    if not txt:
                        continue
                    ingredients.append(
                        {
                            "name": txt,
                            "qty": "",
                            "price": 1.0,
                            "protein_pct": 15,
                            "carb_pct": 50,
                            "fat_pct": 25,
                            "fiber_pct": 10,
                        }
                    )

            if not ingredients:
                ingredients.append(
                    {
                        "name": "Ingredients as per plan",
                        "qty": "",
                        "price": 5.0,
                        "protein_pct": 15,
                        "carb_pct": 50,
                        "fat_pct": 25,
                        "fiber_pct": 10,
                    }
                )

            meals.append(
                {
                    "id": f"m{meal_id}",
                    "name": meal_name or f"Meal {meal_id}",
                    "type": m_type,
                    "calories": calories,
                    "protein_g": 25,
                    "carbs_g": 60,
                    "fat_g": 20,
                    "ingredients": ingredients,
                    "notes": f"Auto-parsed meal for {diet_type.lower()} plan.",
                }
            )
            meal_id += 1

        if not meals:
            return None

        total_calories = sum(m["calories"] for m in meals)
        total_protein = sum(m["protein_g"] for m in meals)
        estimated_daily_cost = round(
            sum(sum(i["price"] for i in m["ingredients"]) for m in meals), 2
        )

        return {
            "meals": meals,
            "diet_summary": f"A {diet_type.lower()}-oriented plan with {len(meals)} meal(s) totalling roughly {total_calories} kcal.",
            "total_calories": total_calories,
            "total_protein_g": total_protein,
            "estimated_daily_cost": estimated_daily_cost,
        }
    except Exception:
        return None

# ─────────────────────────────────────────────────────────────
# COMPONENTS
# ─────────────────────────────────────────────────────────────
def render_header():
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("<div class='logo-text'>nutri<span>supply</span></div>", unsafe_allow_html=True)
        st.markdown("<p style='color:#6B8F71;font-size:14px;margin-top:2px'>Fresh ingredients, delivered to your door</p>", unsafe_allow_html=True)
    with col2:
        if st.session_state.mode:
            if st.button("🏠 Home", use_container_width=True):
                st.session_state.mode = None
                st.session_state.view_dish = None
                st.rerun()
    st.markdown("<hr>", unsafe_allow_html=True)

def render_dish_detail(dish_name):
    dish = DISH_CATALOGUE[dish_name]
    col_back, _ = st.columns([1, 5])
    with col_back:
        if st.button("← Back"):
            st.session_state.view_dish = None
            st.rerun()

    st.markdown(f"<div class='page-title'>{dish_name}</div>", unsafe_allow_html=True)
    badges = ""
    for d in dish["diet"]:
        color = "badge-green" if "Veg" in d else "badge-blue" if "Keto" in d or "Gluten" in d else "badge-orange"
        badges += f"<span class='badge {color}' style='margin-right:6px'>{d}</span>"
    st.markdown(badges, unsafe_allow_html=True)
    st.markdown(f"<p style='color:#6B8F71;margin-top:10px'>{dish['description']}</p>", unsafe_allow_html=True)

    # Quick stats
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("🔥 Calories", f"{dish['calories']} kcal")
    c2.metric("⏱ Cook Time", dish["cook_time"])
    c3.metric("🌍 Cuisine", dish["category"])
    c4.metric("💰 Cost/Person", f"${total_order_price([dish_name]):.2f}")

    st.markdown("<hr>", unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["📦 Ingredients & Nutrition", "👨‍🍳 Recipe Steps", "📊 Nutritional Summary"])

    with tab1:
        st.markdown("<h3 style='margin-bottom:4px'>Ingredients (per 1 person)</h3>", unsafe_allow_html=True)
        st.markdown("<p style='color:#6B8F71;font-size:13px'>Quantities and nutritional breakdown per ingredient</p>", unsafe_allow_html=True)
        for ing in dish["ingredients"]:
            with st.container():
                st.markdown(f"""
                <div class='nutri-card'>
                  <div style='display:flex;justify-content:space-between;align-items:center;margin-bottom:10px'>
                    <div>
                      <span style='font-weight:700;color:#E8F5E9;font-size:15px'>{ing['name']}</span>
                      <span style='color:#6B8F71;font-size:13px;margin-left:10px'>{ing['qty']}</span>
                    </div>
                    <span style='color:#4ADE80;font-weight:600'>~${ing['price']:.2f}</span>
                  </div>
                """, unsafe_allow_html=True)
                cols = st.columns(2)
                with cols[0]:
                    nutrition_bar("Protein", ing["protein_pct"], BAR_COLORS["protein"])
                    nutrition_bar("Carbs", ing["carb_pct"], BAR_COLORS["carb"])
                with cols[1]:
                    nutrition_bar("Fat", ing["fat_pct"], BAR_COLORS["fat"])
                    nutrition_bar("Fiber", ing["fiber_pct"], BAR_COLORS["fiber"])
                st.markdown("</div>", unsafe_allow_html=True)

    with tab2:
        st.markdown("<h3>Step-by-Step Recipe</h3>", unsafe_allow_html=True)
        for i, step in enumerate(dish["recipe"], 1):
            st.markdown(f"""
            <div class='nutri-card' style='display:flex;gap:14px;align-items:flex-start'>
              <div style='min-width:32px;height:32px;border-radius:50%;background:#14532D;color:#4ADE80;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:14px'>{i}</div>
              <div style='color:#E8F5E9;line-height:1.7;font-size:14px'>{step}</div>
            </div>
            """, unsafe_allow_html=True)

        # Download recipe button
        recipe_text = generate_recipe_text(dish_name, dish)
        st.download_button(
            label="⬇️ Download Full Recipe",
            data=recipe_text.encode("utf-8"),
            file_name=f"{dish_name.replace(' ', '_').replace('/', '_')}_recipe.txt",
            mime="text/plain",
            use_container_width=True,
        )

    with tab3:
        st.markdown("<h3>Nutritional Values per 100g</h3>", unsafe_allow_html=True)
        cols = st.columns(5)
        for i, (k, v) in enumerate(dish["nutrition_per_100g"].items()):
            cols[i % 5].metric(k, v)

        st.markdown("<br>", unsafe_allow_html=True)
        col_l, col_r = st.columns([2, 1])
        with col_l:
            st.markdown("<h3>Macronutrient Distribution (avg across ingredients)</h3>", unsafe_allow_html=True)
            ings = [i for i in dish["ingredients"] if i.get("protein_pct", 0) + i.get("carb_pct", 0) + i.get("fat_pct", 0) > 0]
            if ings:
                avg_p = round(sum(i["protein_pct"] for i in ings) / len(ings))
                avg_c = round(sum(i["carb_pct"] for i in ings) / len(ings))
                avg_f = round(sum(i["fat_pct"] for i in ings) / len(ings))
                avg_fb = round(sum(i["fiber_pct"] for i in ings) / len(ings))
                nutrition_bar("🟢 Protein", avg_p, BAR_COLORS["protein"])
                nutrition_bar("🔵 Carbohydrates", avg_c, BAR_COLORS["carb"])
                nutrition_bar("🟠 Fat", avg_f, BAR_COLORS["fat"])
                nutrition_bar("🟣 Fiber", avg_fb, BAR_COLORS["fiber"])

# ─────────────────────────────────────────────────────────────
# ROUTE: HOME — Choose Mode
# ─────────────────────────────────────────────────────────────
def render_home():
    st.markdown("<div class='page-title' style='text-align:center;margin-top:30px'>How would you like to start?</div>", unsafe_allow_html=True)
    st.markdown("<div class='page-sub' style='text-align:center'>Choose a path below to get fresh ingredients delivered</div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="large")
    with col1:
        st.markdown("""
        <div class='choice-card'>
          <div style='font-size:52px;margin-bottom:16px'>📋</div>
          <div style='font-family:DM Serif Display,serif;font-size:20px;color:#E8F5E9;margin-bottom:8px'>I have a Meal Plan</div>
          <div style='color:#6B8F71;font-size:13px;line-height:1.5'>Upload or paste your dietician's meal plan — we'll extract all ingredients automatically</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Start with Meal Plan →", use_container_width=True, key="btn_plan"):
            st.session_state.mode = "plan"
            st.rerun()

    with col2:
        st.markdown("""
        <div class='choice-card'>
          <div style='font-size:52px;margin-bottom:16px'>🍽</div>
          <div style='font-family:DM Serif Display,serif;font-size:20px;color:#E8F5E9;margin-bottom:8px'>Explore Recipes</div>
          <div style='color:#6B8F71;font-size:13px;line-height:1.5'>Browse our curated dish catalogue, build custom meals and order ingredients for each dish</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Explore Dishes →", use_container_width=True, key="btn_explore"):
            st.session_state.mode = "explore"
            st.rerun()

    # Show orders summary if any
    if st.session_state.orders:
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("<h3>📦 Recent Orders</h3>", unsafe_allow_html=True)
        for order in st.session_state.orders[-3:]:
            st.markdown(f"""
            <div class='order-card'>
              <div style='display:flex;justify-content:space-between'>
                <span style='font-weight:700;color:#E8F5E9'>{order['id']}</span>
                <span class='badge badge-green'>CONFIRMED</span>
              </div>
              <div style='color:#6B8F71;font-size:13px;margin-top:6px'>{order['date']} · {order['items']} item(s) · <span style='color:#4ADE80'>${order['total']}</span></div>
            </div>
            """, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# ROUTE: MEAL PLAN MODE
# ─────────────────────────────────────────────────────────────
def render_meal_plan_mode():
    st.markdown("<div class='page-title'>📋 Upload Your Meal Plan</div>", unsafe_allow_html=True)
    st.markdown("<div class='page-sub'>Paste your dietician's meal plan and we'll break down every ingredient with quantities & prices</div>", unsafe_allow_html=True)

    if not st.session_state.meal_plan_result:
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown("**Paste your meal plan below:**")
            plan_text = st.text_area(
                "Meal Plan",
                height=220,
                placeholder="Breakfast: Oats with banana and almonds (60g oats, 1 banana, 30g almonds)\nLunch: Grilled chicken salad (150g chicken, 100g spinach, 1 tomato)\nSnack: Greek yogurt with berries (200g yogurt, 80g berries)\nDinner: Baked salmon with quinoa (200g salmon, 80g quinoa, 100g broccoli)",
                label_visibility="collapsed",
            )
            diet_type = st.selectbox(
                "Diet Type",
                ["General Health", "Diabetic", "Keto", "High Protein", "Vegan", "Low Carb", "Heart-Healthy"],
            )

            if st.button("🔍 Analyze & Break Down Ingredients", use_container_width=True):
                if plan_text.strip():
                    with st.spinner("🤖 AI is analyzing your meal plan..."):
                        result = analyze_meal_plan_ai(plan_text, diet_type)
                        if result:
                            st.session_state.meal_plan_result = result
                            st.rerun()
                else:
                    st.warning("Please paste your meal plan first.")

        with col2:
            st.markdown("""
            <div class='nutri-card nutri-card-accent'>
              <div style='font-weight:700;color:#4ADE80;margin-bottom:10px'>💡 Sample Format</div>
              <div style='font-size:13px;color:#6B8F71;line-height:1.8'>
                <b style='color:#E8F5E9'>Breakfast:</b> Oats with milk<br>
                <b style='color:#E8F5E9'>Lunch:</b> Chicken salad<br>
                <b style='color:#E8F5E9'>Snack:</b> Fruit & nuts<br>
                <b style='color:#E8F5E9'>Dinner:</b> Grilled fish<br><br>
                Include quantities where possible for more accurate breakdowns.
              </div>
            </div>
            """, unsafe_allow_html=True)

    else:
        result = st.session_state.meal_plan_result
        col_reset, _ = st.columns([1, 4])
        with col_reset:
            if st.button("↩ New Plan"):
                st.session_state.meal_plan_result = None
                st.rerun()

        # Summary
        st.markdown("<h2>Plan Summary</h2>", unsafe_allow_html=True)
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("🍽 Meals", len(result.get("meals", [])))
        c2.metric("🔥 Total Calories", f"{result.get('total_calories', '—')} kcal")
        c3.metric("💪 Protein", f"{result.get('total_protein_g', '—')}g")
        c4.metric("💰 Daily Cost", f"${result.get('estimated_daily_cost', 0):.2f}")

        st.markdown(f"""
        <div class='nutri-card nutri-card-accent'>
          <div style='color:#6B8F71;font-size:14px;line-height:1.7'>{result.get('diet_summary', '')}</div>
        </div>
        """, unsafe_allow_html=True)

        # Meals
        st.markdown("<h2>Meals & Ingredients</h2>", unsafe_allow_html=True)
        MEAL_COLORS = {"breakfast": ("badge-green", "🍳"), "lunch": ("badge-orange", "🥗"), "snack": ("badge-blue", "🥜"), "dinner": ("badge-purple", "🐟")}

        for meal in result.get("meals", []):
            badge_cls, emoji = MEAL_COLORS.get(meal.get("type", ""), ("badge-green", "🍽"))
            with st.expander(f"{emoji} {meal['name']} — {meal.get('calories', '?')} kcal"):
                col_a, col_b, col_c = st.columns(3)
                col_a.metric("Protein", f"{meal.get('protein_g', '?')}g")
                col_b.metric("Carbs", f"{meal.get('carbs_g', '?')}g")
                col_c.metric("Fat", f"{meal.get('fat_g', '?')}g")
                if meal.get("notes"):
                    st.info(f"💡 {meal['notes']}")

                st.markdown("**Ingredients:**")
                chips = ""
                for ing in meal.get("ingredients", []):
                    chips += f"<span class='ing-chip'><strong>{ing['name']}</strong> {ing['qty']} ~${ing.get('price', 0):.2f}</span>"
                st.markdown(chips, unsafe_allow_html=True)

        # Schedule
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("<h2>📅 Schedule Deliveries (up to 7 days)</h2>", unsafe_allow_html=True)
        week_days = get_week_days()
        day_labels = [d["label"] for d in week_days]
        selected_days = st.multiselect("Select delivery days:", day_labels)

        if selected_days and st.button("🛒 Place Order for Selected Days", use_container_width=True):
            total_cost = result.get("estimated_daily_cost", 0) * len(selected_days)
            order = {
                "id": f"ORD-{len(st.session_state.orders)+1:04d}",
                "date": datetime.today().strftime("%b %d, %Y"),
                "items": len(result.get("meals", [])) * len(selected_days),
                "total": round(total_cost, 2),
                "days": selected_days,
                "type": "meal_plan",
            }
            st.session_state.orders.append(order)
            st.success(f"✅ Order placed for {len(selected_days)} day(s)! Total: ${total_cost:.2f}")
            st.balloons()

# ─────────────────────────────────────────────────────────────
# ROUTE: EXPLORE MODE
# ─────────────────────────────────────────────────────────────
def render_explore_mode():
    # If viewing a dish detail page
    if st.session_state.view_dish:
        render_dish_detail(st.session_state.view_dish)
        return

    tab1, tab2, tab3 = st.tabs(["🍽 Dish Catalogue", "📂 My Meals", "📦 Orders"])

    # ── TAB 1: CATALOGUE ──────────────────────────────────────
    with tab1:
        st.markdown("<div class='page-title'>Dish Catalogue</div>", unsafe_allow_html=True)
        st.markdown("<div class='page-sub'>Browse dishes, view recipes and ingredients — portioned for 1 person</div>", unsafe_allow_html=True)

        col_filter, col_search = st.columns([2, 3])
        with col_filter:
            diet_filter = st.selectbox("Filter by diet:", DIET_OPTIONS, label_visibility="collapsed")
        with col_search:
            search_q = st.text_input("Search dishes...", placeholder="🔍  Search dishes...", label_visibility="collapsed")

        # Filter
        filtered = {
            k: v for k, v in DISH_CATALOGUE.items()
            if (diet_filter == "All" or diet_filter in v["diet"])
            and (search_q.lower() in k.lower() or search_q.lower() in v["category"].lower() or not search_q)
        }

        if not filtered:
            st.warning("No dishes match your filter.")
        else:
            for dish_name, dish in filtered.items():
                with st.container():
                    col_info, col_actions = st.columns([4, 2])
                    with col_info:
                        st.markdown(f"""
                        <div class='dish-card'>
                          <div style='display:flex;justify-content:space-between;align-items:flex-start'>
                            <div>
                              <div style='font-size:18px;font-weight:700;color:#E8F5E9'>{dish_name}</div>
                              <div style='color:#6B8F71;font-size:13px;margin-top:4px'>{dish['description']}</div>
                              <div style='margin-top:10px'>
                                {''.join(f"<span class='badge badge-green' style='margin-right:5px'>{d}</span>" for d in dish['diet'])}
                              </div>
                            </div>
                          </div>
                          <div style='display:flex;gap:20px;margin-top:12px;font-size:13px;color:#6B8F71'>
                            <span>🔥 {dish['calories']} kcal</span>
                            <span>⏱ {dish['cook_time']}</span>
                            <span>🌍 {dish['category']}</span>
                            <span style='color:#4ADE80'>💰 ${total_order_price([dish_name]):.2f}/person</span>
                          </div>
                        </div>
                        """, unsafe_allow_html=True)
                    with col_actions:
                        if st.button("👁 View Details", key=f"view_{dish_name}", use_container_width=True):
                            st.session_state.view_dish = dish_name
                            st.rerun()

                        if st.session_state.meals:
                            meal_options = list(st.session_state.meals.keys())
                            selected_meal = st.selectbox("Add to meal:", meal_options, key=f"sel_{dish_name}", label_visibility="collapsed")
                            if st.button("➕ Add to Meal", key=f"add_{dish_name}", use_container_width=True):
                                if dish_name not in st.session_state.meals[selected_meal]:
                                    st.session_state.meals[selected_meal].append(dish_name)
                                    st.success(f"Added to '{selected_meal}'!")
                        else:
                            st.markdown("<div style='color:#6B8F71;font-size:12px;text-align:center;margin-top:8px'>Create a meal first in My Meals tab</div>", unsafe_allow_html=True)

    # ── TAB 2: MY MEALS ───────────────────────────────────────
    with tab2:
        st.markdown("<div class='page-title'>My Meals</div>", unsafe_allow_html=True)
        st.markdown("<div class='page-sub'>Create meal collections and schedule ingredient deliveries</div>", unsafe_allow_html=True)

        # Create new meal
        with st.container():
            st.markdown("""
            <div class='nutri-card nutri-card-accent'>
              <div style='font-weight:700;color:#4ADE80;font-size:16px;margin-bottom:12px'>➕ Create New Meal</div>
            """, unsafe_allow_html=True)
            col_inp, col_btn = st.columns([3, 1])
            with col_inp:
                new_meal_name = st.text_input("Meal name", placeholder="e.g. Monday Lunch, Post-Workout, Week 1...", label_visibility="collapsed")
            with col_btn:
                if st.button("Create", use_container_width=True, key="create_meal_btn"):
                    if new_meal_name.strip():
                        if new_meal_name not in st.session_state.meals:
                            st.session_state.meals[new_meal_name] = []
                            st.success(f"✅ Meal '{new_meal_name}' created! Now go to the Dish Catalogue to add dishes.")
                            st.rerun()
                        else:
                            st.warning("A meal with this name already exists.")
                    else:
                        st.warning("Enter a meal name first.")
            st.markdown("</div>", unsafe_allow_html=True)

        if not st.session_state.meals:
            st.markdown("""
            <div style='text-align:center;padding:50px 20px;color:#6B8F71'>
              <div style='font-size:48px;margin-bottom:16px'>🍽</div>
              <div style='font-family:DM Serif Display,serif;font-size:22px;color:#E8F5E9;margin-bottom:8px'>No meals yet</div>
              <div>Create your first meal above, then add dishes from the Catalogue tab.</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            for meal_name, dish_keys in st.session_state.meals.items():
                st.markdown(f"<h3 style='margin-top:24px'>📂 {meal_name}</h3>", unsafe_allow_html=True)

                col_del, _ = st.columns([1, 5])
                with col_del:
                    if st.button(f"🗑 Delete Meal", key=f"del_meal_{meal_name}"):
                        del st.session_state.meals[meal_name]
                        st.rerun()

                if not dish_keys:
                    st.markdown("<div style='color:#6B8F71;font-size:14px;padding:12px'>No dishes yet — add from the Catalogue tab.</div>", unsafe_allow_html=True)
                else:
                    total = total_order_price(dish_keys)
                    total_cal = sum(DISH_CATALOGUE[dk]["calories"] for dk in dish_keys)
                    c1, c2, c3 = st.columns(3)
                    c1.metric("Dishes", len(dish_keys))
                    c2.metric("Total Calories", f"{total_cal} kcal")
                    c3.metric("Ingredient Cost", f"${total:.2f}")

                    for dk in dish_keys:
                        dish = DISH_CATALOGUE.get(dk, {})
                        col_name, col_r, col_x = st.columns([4, 1, 1])
                        with col_name:
                            st.markdown(f"<div class='nutri-card' style='padding:12px 16px'><span style='font-weight:600;color:#E8F5E9'>{dk}</span><span style='color:#6B8F71;font-size:13px;margin-left:10px'>{dish.get('calories',0)} kcal · ${total_order_price([dk]):.2f}</span></div>", unsafe_allow_html=True)
                        with col_r:
                            if st.button("👁", key=f"view_m_{meal_name}_{dk}"):
                                st.session_state.view_dish = dk
                                st.rerun()
                        with col_x:
                            if st.button("✕", key=f"rm_{meal_name}_{dk}"):
                                st.session_state.meals[meal_name].remove(dk)
                                st.rerun()

                    # Schedule order
                    st.markdown("**📅 Schedule delivery (up to 7 days):**")
                    week_days = get_week_days()
                    day_labels = [d["label"] for d in week_days]
                    sel_days = st.multiselect(f"Delivery days for '{meal_name}':", day_labels, key=f"days_{meal_name}")
                    if sel_days and st.button(f"🛒 Order Ingredients for '{meal_name}'", key=f"order_{meal_name}", use_container_width=True):
                        order = {
                            "id": f"ORD-{len(st.session_state.orders)+1:04d}",
                            "date": datetime.today().strftime("%b %d, %Y"),
                            "items": len(dish_keys) * len(sel_days),
                            "total": round(total * len(sel_days), 2),
                            "days": sel_days,
                            "meal": meal_name,
                            "type": "explore",
                        }
                        st.session_state.orders.append(order)
                        st.success(f"✅ Order placed! {len(dish_keys)} dishes × {len(sel_days)} days = ${order['total']:.2f}")
                        st.balloons()

    # ── TAB 3: ORDERS ─────────────────────────────────────────
    with tab3:
        st.markdown("<div class='page-title'>My Orders</div>", unsafe_allow_html=True)
        if not st.session_state.orders:
            st.markdown("""
            <div style='text-align:center;padding:50px 20px'>
              <div style='font-size:48px;margin-bottom:16px'>📦</div>
              <div style='font-family:DM Serif Display,serif;font-size:22px;color:#E8F5E9'>No orders yet</div>
              <div style='color:#6B8F71;margin-top:8px'>Place your first order from My Meals or the Meal Plan tab.</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            for order in reversed(st.session_state.orders):
                label = order.get("meal", "Meal Plan Order")
                days_str = ", ".join(order.get("days", []))
                st.markdown(f"""
                <div class='order-card'>
                  <div style='display:flex;justify-content:space-between;align-items:center'>
                    <div>
                      <span style='font-weight:700;color:#E8F5E9;font-size:16px'>{order['id']}</span>
                      <span style='color:#6B8F71;font-size:13px;margin-left:10px'>Placed {order['date']}</span>
                    </div>
                    <span class='badge badge-green'>✓ CONFIRMED</span>
                  </div>
                  <div style='margin-top:10px;color:#6B8F71;font-size:14px'>
                    📂 {label} · {order['items']} item(s)<br>
                    📅 {days_str}
                  </div>
                  <div style='display:flex;justify-content:space-between;margin-top:12px;padding-top:12px;border-top:1px solid #1E3325'>
                    <span style='color:#6B8F71'>Total</span>
                    <span style='font-family:DM Serif Display,serif;font-size:22px;color:#4ADE80'>${order['total']:.2f}</span>
                  </div>
                </div>
                """, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("<div style='font-family:DM Serif Display,serif;font-size:20px;color:#4ADE80'>NutriSupply</div>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("**ℹ️ Meal Plan Parsing**")
    st.markdown("This app parses your meal plan locally in Python — no external AI or API keys required.")

    st.markdown("---")
    st.markdown("**📊 Session Stats**")
    st.markdown(f"Meals created: **{len(st.session_state.meals)}**")
    st.markdown(f"Orders placed: **{len(st.session_state.orders)}**")
    if st.button("🔄 Reset Session"):
        for k in ["mode", "meal_plan_result", "meals", "orders", "scheduled", "view_dish"]:
            st.session_state[k] = {} if k in ["meals", "orders", "scheduled"] else None
        st.rerun()

# ─────────────────────────────────────────────────────────────
# MAIN ROUTER
# ─────────────────────────────────────────────────────────────
render_header()

if st.session_state.mode is None:
    render_home()
elif st.session_state.mode == "plan":
    render_meal_plan_mode()
elif st.session_state.mode == "explore":
    render_explore_mode()
