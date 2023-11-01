import discord
from discord.ext import commands, tasks
import asyncio
import pandas as pd
import numpy as np

import creds
import config
import functions as func

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=['_'], case_insensitive=True, intents=discord.Intents.all() )

async def get_role_users(g_id: int, r_id: int):
    # g = bot.get_guild(g_id)
    # r = discord.utils.get(g.roles, id=r_id)
    # discord_ids = [m.id for m in r.members]
    # return discord_ids
    attempts = 0
    while True:
        try:
            g = bot.get_guild(g_id)
            r = discord.utils.get(g.roles, id=r_id)
            discord_ids = [m.id for m in r.members]
            return discord_ids
            
        except Exception as err:
            print ("get_role_users function error : ")
            print(err)
            attempts += 1
            if attempts > 4:
                break
            else:
                await asyncio.sleep(5)
                pass
    



@tasks.loop(minutes=config.get_discord_id_timer)
async def get_discord_ids():

    df_forum_id_discord_id = await func.get_current_roles()

    admin_ids = await get_role_users(config.guild_id, config.admin_role)
    await asyncio.sleep(3)

    game_admin_ids = await get_role_users(config.guild_id, config.game_admin_role)
    await asyncio.sleep(3)

    mod_ids = await get_role_users(config.guild_id, config.mod_role)
    await asyncio.sleep(3)

    staff_csgo_ids = await get_role_users(config.guild_id, config.staff_csgo_role)
    await asyncio.sleep(3)

    staff_rust_ids = await get_role_users(config.guild_id, config.staff_rust_role)
    await asyncio.sleep(3)

    staff_unturned_ids = await get_role_users(config.guild_id, config.staff_unturned_role)
    await asyncio.sleep(3)

    staff_minecraft_ids = await get_role_users(config.guild_id, config.staff_minecraft_role)
    await asyncio.sleep(3)

    # staff_ids = await get_role_users(config.guild_id, config.staff_role)
    # await asyncio.sleep(3)

    mvp_plus_ids = await get_role_users(config.guild_id, config.mvp_plus_role)
    await asyncio.sleep(3)

    mvp_ids = await get_role_users(config.guild_id, config.mvp_role)
    await asyncio.sleep(3)

    vip_plus_ids = await get_role_users(config.guild_id, config.vip_plus_role)
    await asyncio.sleep(3)

    vip_ids = await get_role_users(config.guild_id, config.vip_role)
    await asyncio.sleep(3)

    legend_ids = await get_role_users(config.guild_id, config.legend_role)


    admin_duplicates_game_admin = set(admin_ids) & set(game_admin_ids)
    # this list is pure game admins that was't in admins
    final_game_admin_ids = list(admin_duplicates_game_admin ^ set(game_admin_ids))

    admin_game_admin_unique = set(admin_ids + game_admin_ids)
    admin_duplicates_mods = admin_game_admin_unique & set(mod_ids)
    # this list is pure mods that wasn't in admin & game admin
    final_mod_ids = list(admin_duplicates_mods ^ set(mod_ids))

    admin_mod_unique = set(admin_ids + game_admin_ids + mod_ids)
    admin_mod_dupe_staff_csgo = admin_mod_unique & set(staff_csgo_ids)
    # this list is pure staffs that wasn't in admin * game admin & mods
    final_staff_csgo_ids = list(admin_mod_dupe_staff_csgo ^ set(staff_csgo_ids))

    admin_mod__staff_csgo_unique = set(admin_ids + game_admin_ids + mod_ids + staff_csgo_ids)
    admin_mod_staff_csgo_dupe_staff_rust = admin_mod__staff_csgo_unique & set(staff_rust_ids)
    # this list is pure staffs that wasn't in admin * game admin & mods
    final_staff_rust_ids = list(admin_mod_staff_csgo_dupe_staff_rust ^ set(staff_rust_ids))

    admin_mod__staff_csgo_rust_unique = set(admin_ids + game_admin_ids + mod_ids + staff_csgo_ids + staff_rust_ids)
    admin_mod_staff_csgo__staff_rust_dupe_unturned = admin_mod__staff_csgo_rust_unique & set(staff_unturned_ids)
    # this list is pure staffs that wasn't in admin * game admin & mods
    final_staff_unturned_ids = list(admin_mod_staff_csgo__staff_rust_dupe_unturned ^ set(staff_unturned_ids))

    admin_mod__staff_csgo_rust_unturned_unique = set(admin_ids + game_admin_ids + mod_ids + staff_csgo_ids + staff_rust_ids + staff_unturned_ids)
    admin_mod_staff_csgo_staff_rust_unturned_dupe_minecraft = admin_mod__staff_csgo_rust_unturned_unique & set(staff_minecraft_ids)
    # this list is pure staffs that wasn't in admin * game admin & mods
    final_staff_minecraft_ids = list(admin_mod_staff_csgo_staff_rust_unturned_dupe_minecraft ^ set(staff_minecraft_ids))

    admin_mod_staff_unqiue = set(admin_ids + game_admin_ids + mod_ids + staff_csgo_ids + staff_rust_ids + staff_unturned_ids + staff_minecraft_ids)
    admin_mod_staff_dupe_mvp_plus = admin_mod_staff_unqiue & set(mvp_plus_ids)
    # this list is pure premiums that wasn't in admin or mods or staffs
    final_mvp_plus_ids = list(admin_mod_staff_dupe_mvp_plus ^ set(mvp_plus_ids))

    admin_mod_staff_mvpplus_unqiue = set(admin_ids + game_admin_ids + mod_ids + staff_csgo_ids + staff_rust_ids + staff_unturned_ids + staff_minecraft_ids + mvp_plus_ids)
    admin_mod_staff_mvp_plus_dupe_mvp = admin_mod_staff_mvpplus_unqiue & set(mvp_ids)
    # this list is pure premiums that wasn't in admin or mods or staffs
    final_mvp_ids = list(admin_mod_staff_mvp_plus_dupe_mvp ^ set(mvp_ids))

    admin_mod_staff_mvpplus_mvp_unqiue = set(admin_ids + game_admin_ids + mod_ids + staff_csgo_ids + staff_rust_ids + staff_unturned_ids + staff_minecraft_ids + mvp_plus_ids + mvp_ids)
    admin_mod_staff_mvp_plus_mvp_dupe_vipplus = admin_mod_staff_mvpplus_mvp_unqiue & set(vip_plus_ids)
    # this list is pure premiums that wasn't in admin or mods or staffs
    final_vip_plus_ids = list(admin_mod_staff_mvp_plus_mvp_dupe_vipplus ^ set(vip_plus_ids))

    admin_mod_staff_mvpplus_mvp_vipplus_unqiue = set(admin_ids + game_admin_ids + mod_ids + staff_csgo_ids + staff_rust_ids + staff_unturned_ids + staff_minecraft_ids + mvp_plus_ids + mvp_ids + vip_plus_ids)
    admin_mod_staff_mvp_plus_mvp__vipplus_dupe_vip = admin_mod_staff_mvpplus_mvp_vipplus_unqiue & set(vip_ids)
    # this list is pure premiums that wasn't in admin or mods or staffs
    final_vip_ids = list(admin_mod_staff_mvp_plus_mvp__vipplus_dupe_vip ^ set(vip_ids))

    admin_mod_staff_mvpplus_mvp_vipplus_vip_unqiue = set(admin_ids + game_admin_ids + mod_ids + staff_csgo_ids + staff_rust_ids + staff_unturned_ids + staff_minecraft_ids + mvp_plus_ids + mvp_ids + vip_plus_ids + vip_ids)
    admin_mod_staff_mvp_plus_mvp__vipplus_vip_dupe_legends = admin_mod_staff_mvpplus_mvp_vipplus_vip_unqiue & set(legend_ids)
    # this list is pure premiums that wasn't in admin or mods or staffs
    final_legend_ids = list(admin_mod_staff_mvp_plus_mvp__vipplus_vip_dupe_legends ^ set(legend_ids))

    # admin_mod_staff_premium_unqiue = set(admin_ids + mod_ids + staff_ids + vip_ids)
    # admin_mod_staff_premium_dupe_legends = admin_mod_staff_premium_unqiue & set(legend_ids)
    # # this list is pure legends that wasn't in admin or mods or staffs or premium
    # final_legend_ids = list(admin_mod_staff_premium_dupe_legends ^ set(legend_ids))

    gameadmin_mod_staff_mvpplus_mvp_vipplus_vip_legend = final_game_admin_ids + final_mod_ids + final_staff_csgo_ids + final_staff_rust_ids + final_staff_unturned_ids + final_staff_minecraft_ids + final_mvp_plus_ids + final_mvp_ids + final_vip_plus_ids + final_vip_ids + final_legend_ids
    

    # downgrade back to member roles for those with expired or resigned
    df_forum_id_discord_id['discord_id'] = df_forum_id_discord_id['discord_id'].astype(np.int64)
    forum_discord_ids = df_forum_id_discord_id['discord_id'].tolist()
    
    forum_discord_same_ids = set(forum_discord_ids) & set(gameadmin_mod_staff_mvpplus_mvp_vipplus_vip_legend)
    
    forum_discord_ids_covert_member = list(forum_discord_same_ids ^ set(forum_discord_ids))
    
    for x in forum_discord_ids_covert_member:
        try:
            forum_id2 = df_forum_id_discord_id.loc[df_forum_id_discord_id['discord_id'] == int(x),'forum_id'].iloc[0]
            await func.update_forum_roles(int(forum_id2),'Member')
            await asyncio.sleep(3)
        except Exception as err:
            print(" member id error " + str(x))
            print(err)
    # ------------------

    df_user_ids = await func.get_user_ids()
    df_user_ids['discord_id'] = df_user_ids['discord_id'].astype(np.int64)
    if isinstance(df_user_ids,pd.DataFrame):
        
        discord_id_list = df_user_ids['discord_id'].tolist()

        final_game_admin_ids = list(set(discord_id_list) & set(final_game_admin_ids))
        final_mod_ids = list(set(discord_id_list) & set(final_mod_ids))

        final_staff_csgo_ids = list(set(discord_id_list) & set(final_staff_csgo_ids))
        final_staff_rust_ids = list(set(discord_id_list) & set(final_staff_rust_ids))
        final_staff_unturned_ids = list(set(discord_id_list) & set(final_staff_unturned_ids))
        final_staff_minecraft_ids = list(set(discord_id_list) & set(final_staff_minecraft_ids))

        final_mvp_plus_ids = list(set(discord_id_list) & set(final_mvp_plus_ids))
        final_mvp_ids = list(set(discord_id_list) & set(final_mvp_ids))

        final_vip_plus_ids = list(set(discord_id_list) & set(final_vip_plus_ids))
        final_vip_ids = list(set(discord_id_list) & set(final_vip_ids))

        final_legend_ids = list(set(discord_id_list) & set(final_legend_ids))
        # --------------------------

        # Game Admin Role syncer 
        for x in final_game_admin_ids:
            try:
                forum_id = df_user_ids.loc[df_user_ids['discord_id'] == int(x), 'user_id'].iloc[0]
                await func.update_forum_roles(int(forum_id),'Game Admins')
                await asyncio.sleep(3)
            except Exception as err:
                print(" Game Admins id error " + str(x))
                print(err)

        # Mod Role syncer 
        for x in final_mod_ids:
        
            try:
                forum_id = df_user_ids.loc[df_user_ids['discord_id'] == int(x), 'user_id'].iloc[0]
                await func.update_forum_roles(int(forum_id),'Moderator')
                await asyncio.sleep(3)
            except Exception as err:
                print(" mod id error " + str(x))
                print(err)

        # staff role syncer
        for y in final_staff_csgo_ids:
            try:
                forum_id = df_user_ids.loc[df_user_ids['discord_id'] == int(y), 'user_id'].iloc[0]
                await func.update_forum_roles(int(forum_id),'Staff - CSGO')
                await asyncio.sleep(3)
            except Exception as err:
                print(" Staff - CSGO id error " + str(y))
                print(err)
        
        for y in final_staff_rust_ids:
            try:
                forum_id = df_user_ids.loc[df_user_ids['discord_id'] == int(y), 'user_id'].iloc[0]
                await func.update_forum_roles(int(forum_id),'Staff - RUST')
                await asyncio.sleep(3)
            except Exception as err:
                print(" Staff - RUST id error " + str(y))
                print(err)
        
        for y in final_staff_unturned_ids:
            try:
                forum_id = df_user_ids.loc[df_user_ids['discord_id'] == int(y), 'user_id'].iloc[0]
                await func.update_forum_roles(int(forum_id),'Staff - Unturned')
                await asyncio.sleep(3)
            except Exception as err:
                print(" Staff - Unturned id error " + str(y))
                print(err)

        for y in final_staff_minecraft_ids:
            try:
                forum_id = df_user_ids.loc[df_user_ids['discord_id'] == int(y), 'user_id'].iloc[0]
                await func.update_forum_roles(int(forum_id),'Staff - Minecraft')
                await asyncio.sleep(3)
            except Exception as err:
                print(" Staff - Minecraft id error " + str(y))
                print(err)

        # MVP Plus role syncer
        for z in final_mvp_plus_ids:
            try:
                forum_id = df_user_ids.loc[df_user_ids['discord_id'] == int(z), 'user_id'].iloc[0]
                await func.update_forum_roles(int(forum_id),'MVP+')
                await asyncio.sleep(3)
            except Exception as err:
                print(" MVP+ id error " + str(z))
                print(err)
        
        # MVP role syncer
        for z in final_mvp_ids:
            try:
                forum_id = df_user_ids.loc[df_user_ids['discord_id'] == int(z), 'user_id'].iloc[0]
                await func.update_forum_roles(int(forum_id),'MVP')
                await asyncio.sleep(3)
            except Exception as err:
                print(" MVP id error " + str(z))
                print(err)

        # VIP Plus role syncer
        for z in final_vip_plus_ids:
            try:
                forum_id = df_user_ids.loc[df_user_ids['discord_id'] == int(z), 'user_id'].iloc[0]
                await func.update_forum_roles(int(forum_id),'VIP+')
                await asyncio.sleep(3)
            except Exception as err:
                print(" VIP+ id error " + str(z))
                print(err)

        # VIP role syncer
        for z in final_vip_ids:
            try:
                forum_id = df_user_ids.loc[df_user_ids['discord_id'] == int(z), 'user_id'].iloc[0]
                await func.update_forum_roles(int(forum_id),'VIP')
                await asyncio.sleep(3)
            except Exception as err:
                print(" VIP id error " + str(z))
                print(err)

        # Legends role syncer
        for z in final_legend_ids:
            try:
                forum_id = df_user_ids.loc[df_user_ids['discord_id'] == int(z), 'user_id'].iloc[0]
                await func.update_forum_roles(int(forum_id),'Legends')
                await asyncio.sleep(3)
            except Exception as err:
                print(" premium id error " + str(z))
                print(err)
    else:
        print(df_user_ids)

    print("role sync done!")

@bot.event
async def on_ready():
    print('Logged on as {}!'.format(bot.user.name))
    await bot.change_presence(activity = discord.Game(name = "Forum Role Sync!"))
    get_discord_ids.start()

bot.run(creds.bot_token())