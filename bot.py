import discord
from discord.ext import commands, tasks
from discord import app_commands, Embed, ButtonStyle, ui
from discord.ui import Button, View, Select, Modal, TextInput
from discord.utils import get
from discord import TextStyle
from functools import wraps
import os
import io
import random
import asyncio
import time
import re
import subprocess
import sys
import math
import traceback
from keep_alive import keep_alive
from datetime import datetime, timedelta  # Tu as déjà la bonne importation pour datetime et timedelta
from collections import defaultdict, deque
import pymongo
from pymongo import MongoClient
from motor.motor_asyncio import AsyncIOMotorClient
import psutil
import pytz
import platform
from discord import Interaction
import logging
from typing import Optional

token = os.environ['ETHERYA']
intents = discord.Intents.all()
start_time = time.time()
bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

#Configuration du Bot:
# --- ID Owner Bot ---
ISEY_ID = 792755123587645461
# Définir GUILD_ID
GUILD_ID = 1034007767050104892

# --- ID Etherya ---
BOUNTY_CHANNEL_ID = 1355298449829920950
ETHERYA_SERVER_ID = 1034007767050104892
AUTORIZED_SERVER_ID = 1034007767050104892
WELCOME_CHANNEL_ID = 1355198748296351854


# Fonction pour créer des embeds formatés
def create_embed(title, description, color=discord.Color.blue(), footer_text=""):
    embed = discord.Embed(title=title, description=description, color=color)
    embed.set_footer(text=footer_text)
    return embed

# Connexion MongoDB
mongo_uri = os.getenv("MONGO_DB")  # URI de connexion à MongoDB
print("Mongo URI :", mongo_uri)  # Cela affichera l'URI de connexion (assure-toi de ne pas laisser cela en prod)
client = MongoClient(mongo_uri)
db = client['Cass-Eco2']

# Collections
collection = db['ether_eco']  #Stock les Bal
collection2 = db['ether_daily']  #Stock les cd de daily
collection3 = db['ether_slut']  #Stock les cd de slut
collection4 = db['ether_crime']  #Stock les cd de slut
collection5 = db['ether_collect'] #Stock les cd de collect
collection6 = db['ether_work'] #Stock les cd de Work
collection7 = db['ether_inventory'] #Stock les inventaires
collection8 = db['info_cf'] #Stock les Info du cf
collection9 = db['info_logs'] #Stock le Salon logs
collection10 = db['info_bj'] #Stock les Info du Bj
collection11 = db['info_rr'] #Stock les Info de RR
collection12 = db['info_roulette'] #Stock les Info de SM
collection13 = db['info_sm'] #Stock les Info de SM
collection14 = db['ether_rob'] #Stock les cd de Rob
collection15 = db['anti_rob'] #Stock les rôle anti-rob
collection16 = db['ether_boutique'] #Stock les Items dans la boutique
collection17 = db['joueur_ether_inventaire'] #Stock les items de joueurs
collection18 = db['ether_effects'] #Stock les effets
collection19 = db['ether_badge'] #Stock les bagde
collection20 = db['inventaire_badge'] #Stock les bagde des joueurs
collection21 = db['daily_badge'] #Stock les cd des daily badge
collection22 = db['start_date'] #Stock la date de commencemant des rewards
collection23 = db['joueur_rewards'] #Stock ou les joueurs sont
collection24 = db['cd_renforcement'] #Stock les cd
collection25 = db['cd_emission'] #Stock les cd
collection26 = db['cd_manipulation'] #Stock les cd
collection27 = db['cd_materialisation'] #Stock les cd
collection28 = db['cd_transformation'] #Stock les cd
collection29 = db['cd_specialisation'] #Stock les cd
collection30 = db['cd_haki_attaque'] #Stock les cd
collection31 = db['cd_haki_subis'] #Stock les cd
collection32 = db['ether_quetes'] #Stock les quetes
collection33 = db['inventory_collect'] #Stock les items de quetes
collection34 = db['collect_items'] #Stock les items collector
collection35 = db['ether_guild'] #Stock les Guild
collection36 = db['guild_inventaire'] #Stock les inventaire de Guild
collection37 = db['ether_bounty'] #Stock les Primes de Pirates
collection38 = db['ether_honor'] #Stock les Honor des Marines
collection39 = db['cd_capture_ether'] #Stock les cd d'attaque
collection40 = db['cd_bombe'] #Stock les cd des bombes
collection41 = db['cd_gura'] #Stock les cd de seismes
collection42 = db['cd_glace'] #Stock les cd d'attaque de glace
collection43 = db['glace_subis'] #Stock le cd avant de retirer le rôle de subis de glace
collection44 = db['cd_tenebre'] #Stock les cd de Yami
collection45 = db['cd_protection_tenebre'] #Stock le temps de protection de Yami
collection46 = db['cd_gear_second'] #Stock le cd des Gear Second
collection47 = db['cd_gear_fourth'] #Stock les cd des Gear Fourth
collection48 = db['cd_use_fourth'] #Stock les cd des utilisation du Gear Fourth
collection49 = db['cd_royaume_nika'] #Stock le cd des utilisation du Royaume
collection50 = db['cd_acces_royaume'] #Stock le cd d'acces au Royaume
collection51 = db['cd_nika_collect'] #Stock le cd de reutilisation du Nika Collect
collection52 = db['cd_eveil_attaque'] #Stock le cd de reutilisation du Nika Eveil
collection53 = db['cd_eveil_subis'] #Stock le cd de soumission du Nika Eveil
collection54 = db['cd_bourrasque'] #Stock le cd de reutilisation du Uo Uo no Mi
collection55 = db['cd_bourrasque_subis'] #Stock le cd de soumission du Uo Uo no Mi
collection56 = db['cd_tonnerre_attaque'] #Stock les cd de reutillisation du Tonnerre Divin
collection57 = db['cd_tonnerre_subis'] #Stock les cd de soumission du Tonnerre Divin
collection58 = db['cd_eveil_uo'] #Stock les cd d'eveil du Dragon
collection59 = db['message_jour'] #Stock les message des membres chaque jour
collection60 = db['cd_wobservation'] #Stock les cd de W Observation
collection61 = db['cd_observation']


def load_guild_settings(guild_id):
    # Charger les données de la collection principale
    ether_eco_data = collection.find_one({"guild_id": guild_id}) or {}
    ether_daily_data = collection2.find_one({"guild_id": guild_id}) or {}
    ether_slut_data = collection3.find_one({"guild_id": guild_id}) or {}
    ether_crime_data = collection4.find_one({"guild_id": guild_id}) or {}
    ether_collect = collection5.find_one({"guild_id": guild_id}) or {}
    ether_work_data = collection6.find_one({"guild_id": guild_id}) or {}
    ether_inventory_data = collection7.find_one({"guild_id": guild_id}) or {}
    info_cf_data = collection8.find_one({"guild_id": guild_id}) or {}
    info_logs_data = collection9.find_one({"guild_id": guild_id}) or {}
    info_bj_data = collection10.find_one({"guild_id": guild_id}) or {}
    info_rr_data = collection11.find_one({"guild_id": guild_id}) or {}
    info_roulette_data = collection12.find_one({"guild_id": guild_id}) or {}
    info_sm_roulette_data = collection13.find_one({"guild_id": guild_id}) or {}
    ether_rob_data = collection14.find_one({"guild_id": guild_id}) or {}
    anti_rob_data = collection15.find_one({"guild_id": guild_id}) or {}
    ether_boutique_data = collection16.find_one({"guild_id": guild_id}) or {}
    joueur_ether_inventaire_data = collection17.find_one({"guild_id": guild_id}) or {}
    ether_effects_data = collection18.find_one({"guild_id": guild_id}) or {}
    ether_badge_data = collection19.find_one({"guild_id": guild_id}) or {}
    inventaire_badge_data = collection20.find_one({"guild_id": guild_id}) or {}
    daily_badge_data = collection21.find_one({"guild_id": guild_id}) or {}
    start_date_data = collection22.find_one({"guild_id": guild_id}) or {}
    joueur_rewards_data = collection23.find_one({"guild_id": guild_id}) or {}
    cd_renforcement_data = collection24.find_one({"guild_id": guild_id}) or {}
    cd_emission_data = collection25.find_one({"guild_id": guild_id}) or {}
    cd_manipultation_data = collection26.find_one({"guild_id": guild_id}) or {}
    cd_materialisation_data = collection27.find_one({"guidl_id": guild_id}) or {}
    cd_transformation_data = collection28.find_one({"guild_id": guild_id}) or {}
    cd_specialisation_data = collection29.find_one({"guild_id": guild_id}) or {}
    cd_haki_attaque_data = collection30.find_one({"guild_id": guild_id}) or {}
    cd_haki_subis_data = collection31.find_one({"guild_id": guild_id}) or {}
    ether_quetes_data = collection32.find_one({"guild_id": guild_id}) or {}
    inventory_collect_data = collection33.find_one({"guild_id": guild_id}) or {}
    collect_items_data = collection34.find_one({"guild_id": guild_id}) or {}
    ether_guild_data = collection35.find_one({"guild_id": guild_id}) or {}
    guild_inventaire_data = collection36.find_one({"guild_id": guild_id}) or {}
    ether_bounty_data = collection37.find_one({"guild_id": guild_id}) or {}
    ether_honnor_data = collection38.find_one({"guild_id": guild_id}) or {}
    cd_capture_ether_data = collection39.find_one({"guild_id": guild_id}) or {}
    cd_bombe_data = collection40.find_one({"guild_id": guild_id}) or {}
    cd_gura_data = collection41.find_one({"guild_id": guild_id}) or {}
    cd_glace_data = collection42.fing_one({"guild_id": guild_id}) or {}
    glace_subis_data = collection43.find_one({"guild_id": guild_id}) or {}
    cd_tenebre_data = collection44.find_one({"guild_id": guild_id}) or {}
    cd_protection_tenebre_data = collection45.find_one({"guild_id": guild_id}) or {}
    cd_gear_second_data = collection46.find_one({"guild_id": guild_id}) or {}
    cd_gear_fourth_data = collection47.find_one({"guild_id": guild_id}) or {}
    cd_use_fourth_data = collection48.find_one({"guild_id": guild_id}) or {}
    cd_royaume_nika_data = collection49.find_one({"guild_id": guild_id}) or {}
    cd_acces_royaume_data = collection50.find_one({"guild_id": guild_id}) or {}
    cd_nika_collect_data = collection51.find_one({"guild_id": guild_id}) or {}
    cd_eveil_attaque_data = collection52.find_one({"guild_id": guild_id}) or {}
    cd_eveil_subis_data = collection53.find_one({"guild_id": guild_id}) or {}
    cd_bourrasque_data = collection54.find_one({"guild_id": guild_id}) or {}
    cd_bourrasque_subis_data = collection55.find_one({"guild_id": guild_id}) or {}
    cd_tonnerre_attaque_data = collection56.find_one({"guild_id": guil_id}) or {}
    cd_tonnerre_subis_data = collection57.find_one({"guild_id": guild_id}) or {}
    cd_eveil_uo_data = collection58.find_one({"guild_id": guild_id}) or {}
    message_jour_data = collection59.find_one({"guild_id": guild_id}) or {}
    cd_wobservation_data = collection60.find_one({"guild_id": guild_id}) or {}
    cd_observation_data = collection61.find_one({"guild_id": guild_id}) or {}
    
    # Débogage : Afficher les données de setup
    print(f"Setup data for guild {guild_id}: {setup_data}")

    combined_data = {
        "ether_eco": ether_eco_data,
        "ether_daily": ether_daily_data,
        "ether_slut": ether_slut_data,
        "ether_crime": ether_crime_data,
        "ether_collect": ether_collect_data,
        "ether_work": ether_work_data,
        "ether_inventory": ether_inventory_data,
        "info_cf": info_cf_data,
        "info_logs": info_logs_data,
        "info_bj": info_bj_data,
        "info_rr": info_rr_data,
        "info_roulette": info_roulette_data,
        "info_sm": info_sm_data,
        "ether_rob": ether_rob_data,
        "anti_rob": anti_rob_data,
        "ether_boutique": ether_boutique_data,
        "joueur_ether_inventaire": joueur_ether_inventaire_data,
        "ether_effects": ether_effects_data,
        "ether_badge": ether_badge_data,
        "inventaire_badge": inventaire_badge_data,
        "daily_badge": daily_badge_data,
        "start_date": start_date_data,
        "joueur_rewards": joueur_rewards_data,
        "cd_renforcement": cd_renforcement_data,
        "cd_emission": cd_emission_data,
        "cd_manipultation": cd_manipultation_data,
        "cd_materialisation": cd_materialisation_data,
        "cd_transformation" : cd_transformation_data,
        "cd_specialisation" : cd_specialisation_data,
        "cd_haki_attaque": cd_haki_attaque_data,
        "cd_haki_subis": cd_haki_subis_data,
        "ether_quetes": ether_quetes_data,
        "inventory_collect": inventory_collect_data,
        "collect_items": collect_items_data,
        "ether_guild": ether_guild_data,
        "guild_inventaire": guild_inventaire_data,
        "ether_bounty": ether_bounty_data,
        "ether_honnor": ether_honnor_data,
        "cd_capture_ether": cd_capture_ether_data,
        "cd_bombe": cd_bombe_data,
        "cd_gura": cd_gura_data,
        "cd_glace": cd_glace_data,
        "glace_subis": glace_subis_data,
        "cd_tenebre": cd_tenebre_data,
        "cd_protection_tenebre": cd_protection_tenebre_data,
        "cd_gear_second": cd_gear_second_data,
        "cd_gear_fourth": cd_gear_fourth_data,
        "cd_use_fourth": cd_use_fourth_data,
        "cd_royaume_nika": cd_royaume_nika_data,
        "cd_acces_royaume": cd_acces_royaume_data,
        "cd_nika_collect": cd_nika_collect_data,
        "cd_eveil_attaque": cd_eveil_attaque_data,
        "cd_eveil_subis": cd_eveil_subis_data,
        "cd_bourrasque": cd_bourrasque_data,
        "cd_bourrasque_subis": cd_bourrasque_subis_data,
        "cd_tonnerre_attaque": cd_tonnerre_attaque_data,
        "cd_tonnerre_subis": cd_tonnerre_subis_data,
        "cd_eveil_uo": cd_eveil_uo_data,
        "message_jour": message_jour_data,
        "cd_wobservation": cd_wobservation_data,
        "cd_observation": cd_observation_data
    }

    return combined_data

# --- Initialisation au démarrage ---
@bot.event
async def on_ready():
    print(f"{bot.user.name} est connecté.")
    bot.uptime = time.time()
    activity = discord.Activity(
        type=discord.ActivityType.streaming,
        name="Etherya",
        url="https://www.twitch.tv/tonstream"
    )
    await bot.change_presence(activity=activity, status=discord.Status.online)

    print(f"🎉 **{bot.user}** est maintenant connecté et affiche son activité de stream avec succès !")
    print("📌 Commandes disponibles 😊")
    for command in bot.commands:
        print(f"- {command.name}")

    try:
        synced = await bot.tree.sync()
        print(f"✅ Commandes slash synchronisées : {[cmd.name for cmd in synced]}")
    except Exception as e:
        print(f"❌ Erreur de synchronisation des commandes slash : {e}")

# --- Gestion globale des erreurs ---
@bot.event
async def on_error(event, *args, **kwargs):
    print(f"Une erreur s'est produite : {event}")
    embed = discord.Embed(
        title="❗ Erreur inattendue",
        description="Une erreur s'est produite lors de l'exécution de la commande. Veuillez réessayer plus tard.",
        color=discord.Color.red()
    )
    try:
        await args[0].response.send_message(embed=embed)
    except Exception:
        pass

#------------------------------------------------- Gcreate
@bot.command(name="gcreate")
async def creer_guilde(ctx):
    guild_id = ctx.guild.id
    user_id = ctx.author.id

    # Vérifier s'il est déjà dans une guilde
    guilde_existante = collection35.find_one({"guild_id": guild_id, "membres.user_id": user_id})
    if guilde_existante:
        return await ctx.send("Tu es déjà dans une guilde.")

    # Vérifier les coins
    user_data = collection.find_one({"guild_id": guild_id, "user_id": user_id})
    if not user_data or user_data.get("cash", 0) < 5000:
        return await ctx.send("Tu n'as pas assez de coins pour créer une guilde (5000 requis).")

    def check_msg(m):
        return m.author == ctx.author and m.channel == ctx.channel

    # Demander le nom de la guilde
    await ctx.send("📝 Quel est le nom de ta guilde ? (Ce sera l'ID interne)")
    try:
        msg_nom = await bot.wait_for("message", check=check_msg, timeout=60)
        nom_guilde = msg_nom.content.strip()
    except asyncio.TimeoutError:
        return await ctx.send("⏳ Temps écoulé. Recommence la commande.")

    # Vérifier si une guilde avec ce nom existe déjà
    if collection35.find_one({"guild_id": guild_id, "guild_name": nom_guilde}):
        return await ctx.send("❌ Une guilde avec ce nom existe déjà.")

    # Demander la description
    await ctx.send("📄 Donne une petite description pour ta guilde :")
    try:
        msg_desc = await bot.wait_for("message", check=check_msg, timeout=60)
        description = msg_desc.content.strip()
    except asyncio.TimeoutError:
        return await ctx.send("⏳ Temps écoulé. Recommence la commande.")

    # Demander une PFP pour la guilde
    await ctx.send("🎨 Envoie une image pour la photo de profil de ta guilde (PFP) :")
    try:
        msg_pfp = await bot.wait_for("message", check=check_msg, timeout=60)
        pfp_url = msg_pfp.attachments[0].url if msg_pfp.attachments else None
        if not pfp_url:
            return await ctx.send("❌ Tu n'as pas envoyé d'image pour la PFP.")
    except asyncio.TimeoutError:
        return await ctx.send("⏳ Temps écoulé. Recommence la commande.")

    # Demander une bannière pour la guilde
    await ctx.send("🎨 Envoie une image pour la bannière de ta guilde :")
    try:
        msg_banniere = await bot.wait_for("message", check=check_msg, timeout=60)
        banniere_url = msg_banniere.attachments[0].url if msg_banniere.attachments else None
        if not banniere_url:
            return await ctx.send("❌ Tu n'as pas envoyé d'image pour la bannière.")
    except asyncio.TimeoutError:
        return await ctx.send("⏳ Temps écoulé. Recommence la commande.")

    # Déduire les coins
    collection.update_one(
        {"guild_id": guild_id, "user_id": user_id},
        {"$inc": {"cash": -5000}}
    )

    # Log éco si tu veux
    await log_eco_channel(
        bot, guild_id, ctx.author, "Création Guilde", 5000,
        user_data["cash"], user_data["cash"] - 5000,
        note=f"Guilde: {nom_guilde}"
    )

    # Enregistrement dans la DB
    nouvelle_guilde = {
        "guild_id": guild_id,
        "guild_name": nom_guilde,
        "description": description,
        "pfp_url": pfp_url,
        "banniere_url": banniere_url,
        "bank": 0,
        "vault": 0,
        "membres": [
            {
                "user_id": user_id,
                "role": "Créateur",
                "joined_at": datetime.utcnow()
            }
        ]
    }

    collection35.insert_one(nouvelle_guilde)

    await ctx.send(f"✅ Guilde **{nom_guilde}** créée avec succès !")


@bot.command(name="g")
async def afficher_guilde(ctx):
    guild_id = ctx.guild.id
    user_id = ctx.author.id

    # Récupérer la guilde du joueur
    guilde = collection35.find_one({"guild_id": guild_id, "membres.user_id": user_id})
    if not guilde:
        return await ctx.send("Tu n'es dans aucune guilde.")

    guild_name = guilde.get("guild_name", "Inconnue")
    description = guilde.get("description", "Aucune description.")
    banque = guilde.get("bank", 0)
    coffre_fort = guilde.get("vault", 0)
    membres = guilde.get("membres", [])
    pfp_url = guilde.get("pfp_url")
    banniere_url = guilde.get("banniere_url")

    embed = discord.Embed(
        title=f"Informations sur la guilde : {guild_name}",
        color=discord.Color.blue()
    )

    # Ajouter la PFP si elle existe
    if pfp_url:
        embed.set_thumbnail(url=pfp_url)

    # Ajouter la bannière si elle existe
    if banniere_url:
        embed.set_image(url=banniere_url)

    embed.add_field(name="Description", value=description, inline=False)
    embed.add_field(name="Banque", value=f"{int(banque):,} <:ecoEther:1341862366249357374>", inline=True)  # Retirer les décimales
    embed.add_field(name="Coffre fort", value=f"{int(coffre_fort):,} / 750,000 <:ecoEther:1341862366249357374>", inline=True)  # Retirer les décimales
    embed.add_field(name="ID", value=guilde.get("guild_name"), inline=False)

    # Affichage des membres
    membre_text = ""
    for membre in membres:
        mention = f"<@{membre['user_id']}>"
        role = membre.get("role", "Membre")
        if role == "Créateur":
            membre_text += f"**Créateur** | {mention}\n"
        else:
            membre_text += f"**Membre** | {mention}\n"

    embed.add_field(name=f"Membres ({len(membres)}/5)", value=membre_text or "Aucun membre", inline=False)

    await ctx.send(embed=embed)

@bot.command(name="reset-teams")
async def reset_teams(ctx):
    # Vérifier si l'utilisateur a l'ID correct
    if ctx.author.id != 792755123587645461:
        return await ctx.send("Tu n'as pas la permission d'utiliser cette commande.")

    # Effacer toutes les guildes de la base de données
    result = collection35.delete_many({})
    
    if result.deleted_count > 0:
        await ctx.send(f"✅ Toutes les guildes ont été supprimées avec succès. {result.deleted_count} guildes supprimées.")
    else:
        await ctx.send("❌ Aucune guilde trouvée à supprimer.")

@bot.command(name="ginvite")
async def ginvite(ctx, member: discord.Member):
    # Récupérer les informations de la guilde du joueur qui invite
    guild_id = ctx.guild.id
    guilde = collection35.find_one({"guild_id": guild_id})
    if not guilde:
        return await ctx.send("Aucune guilde trouvée.")

    guild_name = guilde.get("guild_name", "Inconnue")
    description = guilde.get("description", "Aucune description.")
    pfp_url = guilde.get("pfp_url")
    
    # Créer l'embed d'invitation
    embed = discord.Embed(
        title=f"Invitation à la guilde {guild_name}",
        description=f"Tu as été invité à rejoindre la guilde **{guild_name}** !\n\n{description}",
        color=discord.Color.blue()
    )
    
    if pfp_url:
        embed.set_thumbnail(url=pfp_url)

    # Créer les boutons "Accepter" et "Refuser"
    class InviteButtons(View):
        def __init__(self, inviter, invited_member):
            super().__init__()
            self.inviter = inviter
            self.invited_member = invited_member

        @discord.ui.button(label="Accepter", style=discord.ButtonStyle.green)
        async def accept_button(self, interaction: discord.Interaction, button: discord.ui.Button):
            # Action quand le membre accepte l'invitation
            if interaction.user == self.invited_member:
                # Ajouter le membre à la guilde
                collection35.update_one(
                    {"guild_id": guild_id},
                    {"$push": {"membres": {"user_id": self.invited_member.id, "role": "Membre"}}}
                )
                await interaction.response.send_message(f"{self.invited_member.mention} a accepté l'invitation à la guilde {guild_name} !", ephemeral=True)
                # Envoie un message dans la guilde (optionnel)
                await ctx.send(f"{self.invited_member.mention} a rejoint la guilde {guild_name}.")

        @discord.ui.button(label="Refuser", style=discord.ButtonStyle.red)
        async def decline_button(self, interaction: discord.Interaction, button: discord.ui.Button):
            # Action quand le membre refuse l'invitation
            if interaction.user == self.invited_member:
                await interaction.response.send_message(f"{self.invited_member.mention} a refusé l'invitation.", ephemeral=True)

    # Créer la vue pour les boutons
    view = InviteButtons(ctx.author, member)

    # Envoyer l'embed et ajouter la vue avec les boutons dans le salon d'origine
    await ctx.send(embed=embed, view=view)

    await ctx.send(f"Une invitation a été envoyée à {member.mention}.")

# Commande .cdep : Déposer des coins dans le coffre-fort de la guild
@bot.command(name="cdep")
async def cdep(ctx, amount: int):
    guild_id = ctx.guild.id
    user_id = ctx.author.id

    # Vérifier les coins de l'utilisateur
    user_data = collection.find_one({"guild_id": guild_id, "user_id": user_id})
    if not user_data or user_data.get("cash", 0) < amount:
        return await ctx.send("Tu n'as pas assez de coins pour faire ce dépôt.")

    # Déposer les coins dans le coffre-fort
    collection35.update_one(
        {"guild_id": guild_id},
        {"$inc": {"vault": amount}},
    )
    # Déduire les coins du joueur
    collection.update_one(
        {"guild_id": guild_id, "user_id": user_id},
        {"$inc": {"cash": -amount}},
    )

    await ctx.send(f"{int(amount):,} coins ont été déposés dans le coffre-fort de la guilde.")

# Commande .cwith : Retirer des coins du coffre-fort de la guilde
@bot.command(name="cwith")
async def cwith(ctx, amount: int):
    guild_id = ctx.guild.id

    # Récupérer les informations de la guilde
    guilde = collection35.find_one({"guild_id": guild_id})
    if not guilde or guilde.get("vault", 0) < amount:
        return await ctx.send("Le coffre-fort de la guilde n'a pas assez de coins.")

    # Retirer les coins du coffre-fort
    collection35.update_one(
        {"guild_id": guild_id},
        {"$inc": {"vault": -amount}},
    )
    
    # Ajouter les coins à la banque
    collection35.update_one(
        {"guild_id": guild_id},
        {"$inc": {"bank": amount}},
    )

    await ctx.send(f"{int(amount):,} coins ont été retirés du coffre-fort de la guilde.")

# Commande .gban : Bannir un membre de la guilde
@bot.command(name="gban")
async def gban(ctx, member: discord.Member):
    guild_id = ctx.guild.id

    # Vérifier si l'utilisateur est dans la guilde
    guilde = collection35.find_one({"guild_id": guild_id})
    if not guilde or not any(membre['user_id'] == member.id for membre in guilde['membres']):
        return await ctx.send(f"{member.mention} n'est pas dans la guilde.")

    # Bannir le membre de la guilde
    collection35.update_one(
        {"guild_id": guild_id},
        {"$pull": {"membres": {"user_id": member.id}}},
    )

    await ctx.send(f"{member.mention} a été banni de la guilde.")

@bot.command(name="gdelete")
async def gdelete(ctx, guild_id: int):
    # Vérifier que l'utilisateur est autorisé à supprimer la guilde (par exemple, propriétaire)
    if ctx.author.id != 792755123587645461:  # ISEY_ID
        return await ctx.send("Tu n'as pas la permission de supprimer cette guilde.")
    
    # Vérifier si la guilde existe dans la base de données
    guilde = collection35.find_one({"guild_id": guild_id})
    if not guilde:
        return await ctx.send(f"Aucune guilde trouvée avec l'ID {guild_id}.")

    # Supprimer la guilde
    collection35.delete_one({"guild_id": guild_id})

    await ctx.send(f"La guilde avec l'ID {guild_id} a été supprimée avec succès.")

# Commande .gdep : Déposer des coins dans la banque de la guilde
@bot.command(name="gdep")
async def gdep(ctx, amount: str):
    guild_id = ctx.guild.id

    if amount == "all":
        # Déposer tout l'argent dans la banque
        user_data = collection.find_one({"guild_id": guild_id, "user_id": ctx.author.id})
        amount = user_data.get("cash", 0)

        if amount == 0:
            return await ctx.send("Tu n'as pas de coins à déposer.")

    # Convertir la quantité en entier
    amount = int(amount)

    # Déposer les coins dans la banque de la guilde
    collection35.update_one(
        {"guild_id": guild_id},
        {"$inc": {"bank": amount}},
    )

    # Déduire les coins du joueur
    collection.update_one(
        {"guild_id": guild_id, "user_id": ctx.author.id},
        {"$inc": {"cash": -amount}},
    )

    await ctx.send(f"{amount:,} coins ont été déposés dans la banque de la guilde.")

# Commande .gkick : Expulser un membre de la guilde
@bot.command(name="gkick")
async def gkick(ctx, member: discord.Member):
    guild_id = ctx.guild.id

    # Vérifier si le membre est dans la guilde
    guilde = collection35.find_one({"guild_id": guild_id})
    if not guilde or not any(membre['user_id'] == member.id for membre in guilde['membres']):
        return await ctx.send(f"{member.mention} n'est pas dans la guilde.")

    # Expulser le membre
    collection35.update_one(
        {"guild_id": guild_id},
        {"$pull": {"membres": {"user_id": member.id}}},
    )

    await ctx.send(f"{member.mention} a été expulsé de la guilde.")

# Commande .gleave : Quitter la guilde
@bot.command(name="gleave")
async def gleave(ctx):
    guild_id = ctx.guild.id
    user_id = ctx.author.id

    # Vérifier si l'utilisateur est dans la guilde
    guilde = collection35.find_one({"guild_id": guild_id})
    if not guilde or not any(membre['user_id'] == user_id for membre in guilde['membres']):
        return await ctx.send("Tu n'es pas dans cette guilde.")

    # Quitter la guilde
    collection35.update_one(
        {"guild_id": guild_id},
        {"$pull": {"membres": {"user_id": user_id}}},
    )

    await ctx.send(f"{ctx.author.mention} a quitté la guilde.")

# Commande .gowner : Transférer la propriété de la guilde
@bot.command(name="gowner")
async def gowner(ctx, new_owner: discord.Member):
    guild_id = ctx.guild.id

    # Vérifier si l'utilisateur est le propriétaire actuel (par exemple, le créateur)
    guilde = collection35.find_one({"guild_id": guild_id})
    if not guilde or not any(membre['user_id'] == ctx.author.id and membre['role'] == 'Créateur' for membre in guilde['membres']):
        return await ctx.send("Tu n'es pas le propriétaire de la guilde.")

    # Transférer la propriété
    collection35.update_one(
        {"guild_id": guild_id, "membres.user_id": ctx.author.id},
        {"$set": {"membres.$.role": "Membre"}},
    )
    collection35.update_one(
        {"guild_id": guild_id, "membres.user_id": new_owner.id},
        {"$set": {"membres.$.role": "Créateur"}},
    )

    await ctx.send(f"La propriété de la guilde a été transférée à {new_owner.mention}.")

# Commande .gunban : Débannir un membre de la guilde
@bot.command(name="gunban")
async def gunban(ctx, member: discord.Member):
    guild_id = ctx.guild.id

    # Vérifier si le membre est banni
    guilde = collection35.find_one({"guild_id": guild_id})
    if not guilde or not any(membre['user_id'] == member.id and membre['role'] == 'Banni' for membre in guilde['membres']):
        return await ctx.send(f"{member.mention} n'est pas banni de cette guilde.")

    # Débannir le membre
    collection35.update_one(
        {"guild_id": guild_id},
        {"$pull": {"membres": {"user_id": member.id, "role": "Banni"}}},
    )

    await ctx.send(f"{member.mention} a été débanni de la guilde.")

# Commande .gwith : Retirer des coins de la banque de la guilde
@bot.command(name="gwith")
async def gwith(ctx, amount: int):
    guild_id = ctx.guild.id

    # Récupérer les informations de la guilde
    guilde = collection35.find_one({"guild_id": guild_id})
    if not guilde or guilde.get("bank", 0) < amount:
        return await ctx.send("La banque de la guilde n'a pas assez de coins.")

    # Retirer les coins de la banque
    collection35.update_one(
        {"guild_id": guild_id},
        {"$inc": {"bank": -amount}},
    )

    # Ajouter les coins au joueur (ici on les ajoute à l'auteur de la commande)
    collection.update_one(
        {"guild_id": guild_id, "user_id": ctx.author.id},
        {"$inc": {"cash": amount}},
    )

    await ctx.send(f"{amount:,} coins ont été retirés de la banque de la guilde.")

@bot.tree.command(name="dep-guild-inventory", description="Dépose un item de ton inventaire vers celui de ta guilde")
@app_commands.describe(item_id="ID de l'item à transférer", quantite="Quantité à transférer")
async def dep_guild_inventory(interaction: discord.Interaction, item_id: int, quantite: int):
    user = interaction.user
    guild_id = interaction.guild.id
    user_id = user.id

    if quantite <= 0:
        return await interaction.response.send_message("❌ La quantité doit être supérieure à 0.", ephemeral=True)

    # Vérifie la guilde du joueur
    guilde = collection35.find_one({"guild_id": guild_id, "membres.user_id": user_id})
    if not guilde:
        return await interaction.response.send_message("❌ Tu n'es dans aucune guilde.", ephemeral=True)

    # Vérifie l'inventaire du joueur
    items = list(collection17.find({
        "guild_id": guild_id,
        "user_id": user_id,
        "item_id": item_id
    }))

    if len(items) < quantite:
        return await interaction.response.send_message(f"❌ Tu n'as pas `{quantite}` de cet item dans ton inventaire.", ephemeral=True)

    # Supprimer les items du joueur
    for i in range(quantite):
        collection17.delete_one({
            "_id": items[i]["_id"]
        })

    # Ajouter à l'inventaire de la guilde
    existing = collection36.find_one({
        "guild_id": guild_id,
        "item_id": item_id
    })

    if existing:
        collection36.update_one(
            {"_id": existing["_id"]},
            {"$inc": {"quantity": quantite}}
        )
    else:
        # On récupère les infos du premier item pour les détails
        item_data = items[0]
        collection36.insert_one({
            "guild_id": guild_id,
            "item_id": item_id,
            "item_name": item_data.get("item_name", "Inconnu"),
            "emoji": item_data.get("emoji", ""),
            "quantity": quantite
        })

    await interaction.response.send_message(
        f"✅ Tu as transféré **{quantite}x** `{item_id}` dans l'inventaire de ta guilde.",
        ephemeral=True
    )

@bot.tree.command(name="with-guild-inventory", description="Retire un item de l'inventaire de la guilde vers le tien")
@app_commands.describe(item_id="ID de l'item à retirer", quantite="Quantité à retirer")
async def with_guild_inventory(interaction: discord.Interaction, item_id: int, quantite: int):
    user = interaction.user
    guild_id = interaction.guild.id
    user_id = user.id

    if quantite <= 0:
        return await interaction.response.send_message("❌ La quantité doit être supérieure à 0.", ephemeral=True)

    # Vérifie la guilde du joueur
    guilde = collection35.find_one({"guild_id": guild_id, "membres.user_id": user_id})
    if not guilde:
        return await interaction.response.send_message("❌ Tu n'es dans aucune guilde.", ephemeral=True)

    # Vérifie l'inventaire de la guilde
    guild_item = collection36.find_one({
        "guild_id": guild_id,
        "item_id": item_id
    })

    if not guild_item or guild_item.get("quantity", 0) < quantite:
        return await interaction.response.send_message("❌ Pas assez de cet item dans l'inventaire de la guilde.", ephemeral=True)

    # Retirer les items de la guilde
    new_quantity = guild_item["quantity"] - quantite
    if new_quantity > 0:
        collection36.update_one(
            {"_id": guild_item["_id"]},
            {"$set": {"quantity": new_quantity}}
        )
    else:
        collection36.delete_one({"_id": guild_item["_id"]})

    # Ajouter les items dans l'inventaire du joueur
    insert_items = []
    for _ in range(quantite):
        insert_items.append({
            "guild_id": guild_id,
            "user_id": user_id,
            "item_id": item_id,
            "item_name": guild_item.get("item_name", "Inconnu"),
            "emoji": guild_item.get("emoji", "")
        })
    if insert_items:
        collection17.insert_many(insert_items)

    await interaction.response.send_message(
        f"📦 Tu as récupéré **{quantite}x** `{item_id}` depuis l'inventaire de la guilde.",
        ephemeral=True
    )

# Token pour démarrer le bot (à partir des secrets)
# Lancer le bot avec ton token depuis l'environnement  
keep_alive()
bot.run(token)
