from datetime import datetime, timezone
from typing import TypeAlias

import disnake

import utils

from .messages_cz import MessagesCZ
from .views import View

SLOWMODE_CHANNEL_TYPES: TypeAlias = (
    disnake.TextChannel | disnake.Thread | disnake.VoiceChannel | disnake.ForumChannel
)

MODERATION_TRUE = "moderation:resolve:true"
MODERATION_FALSE = "moderation:resolve:false"


# Reflects UI slider values
delay_timestamps = {
    "5s": 5,
    "10s": 10,
    "15s": 15,
    "30s": 30,
    "1min": 60,
    "2min": 2 * 60,
    "5min": 5 * 60,
    "10min": 10 * 60,
    "15min": 15 * 60,
    "30min": 30 * 60,
    "1h": 1 * 60 * 60,
    "2h": 2 * 60 * 60,
    "6h": 6 * 60 * 60,
}


async def slowmode_delay_autocomp(
    inter: disnake.ApplicationCommandInteraction, string: str
) -> dict[str, int]:
    return {key: value for key, value in delay_timestamps.items() if string.lower() in key.lower()}


async def mod_tag(message: disnake.Message, role: str, room: disnake.TextChannel):
    if len(message.content) < 3800:
        embed = disnake.Embed(
            title=f"Tagged {role}",
            description=f"**User:** {message.author.mention}\n"
            f"**Link:** [#{message.channel}]({message.jump_url})\n"
            f"**Content:**\n{message.content}",
            color=disnake.Color.yellow(),
        )
    else:
        embed = disnake.Embed(
            title=f"Tagged {role}",
            description=f"**User:** {message.author.mention}\n"
            f"**Link:** [#{message.channel}]({message.jump_url})\n",
            color=disnake.Color.yellow(),
        )
        parts = utils.general.split_to_parts(message.content, 1024)
        for msg in parts:
            embed.add_field(name="Content", value=msg, inline=False)

    embed.add_field(name="Resolved by:", value="---")
    embed.set_footer(text=datetime.now().strftime("%d.%m.%Y %H:%M"))
    await room.send(embed=embed, view=View("Resolve", MODERATION_FALSE))


async def log(
    inter: disnake.GuildCommandInteraction,
    prev_delay: int,
    curr_delay: int,
    channel: SLOWMODE_CHANNEL_TYPES,
    log_channel: disnake.TextChannel,
):
    """
    Log slowmode changes
    """
    embed = disnake.Embed(title="Channel slowmode change", color=disnake.Colour.yellow())
    embed.add_field(name="Mod", value=f"{inter.author.mention} ({inter.author.name})")
    embed.add_field(name="Channel", value=f"[#{channel.name}]({channel.jump_url})", inline=False)
    embed.add_field(name="Old value", value=f"{prev_delay} seconds")
    embed.add_field(name="New value", value=f"{curr_delay} seconds")
    embed.timestamp = datetime.now(tz=timezone.utc)
    await log_channel.send(embed=embed)


async def temp_ban(
    inter: disnake.GuildCommandInteraction,
    user: disnake.Member,
    duration: str,
    reason: str,
    config,
):
    """
    Temporarily ban a user
    """
    # Parse duration
    # seconds = utils.time.parse_time(duration)
    seconds = 0
    if seconds is None:
        await inter.edit_original_response(MessagesCZ.invalid_duration_format)
        return

    # Check if duration is within limits
    if seconds < 60 or seconds > 315360000:  # Between 1 minute and 10 years
        await inter.edit_original_response(MessagesCZ.duration_limits)
        return

    # Calculate unban time
    # unban_time = datetime.now(tz=timezone.utc).timestamp() + seconds
    reason = f"{reason} ({duration})"
    # Ban the user
    try:
        await user.ban(reason=reason)
    except disnake.Forbidden:
        await inter.edit_original_response(MessagesCZ.ban_permission_error)
        return
    except disnake.HTTPException:
        await inter.edit_original_response(MessagesCZ.ban_failed)
        return

    # Log the ban in the database (pseudo-code, replace with actual DB logic)
    # db.bans.insert_one({"user_id": user.id, "unban_time": unban_time, "reason": reason, "banned_by": inter.author.id})

    await inter.edit_original_response(
        MessagesCZ.temp_ban_success(user_mention=user.mention, duration=duration)
    )


async def perm_ban(
    inter: disnake.GuildCommandInteraction,
    user: disnake.Member,
    reason: str,
    config,
):
    """
    Permanently ban a user
    """
    if (
        (reason is not None)
        and reason.split()[-1].startswith("(")
        and reason.split()[-1].endswith(")")
        and reason.split()[-1][1:-1].isdigit()
    ):
        await inter.edit_original_response(MessagesCZ.perm_ban_bracket_error)
        return
    try:
        await user.ban(reason=reason)
    except disnake.Forbidden:
        await inter.edit_original_response(MessagesCZ.ban_permission_error)
        return
    except disnake.HTTPException:
        await inter.edit_original_response(MessagesCZ.ban_failed)
        return

    # Log the permanent ban in the database (pseudo-code, replace with actual DB logic)
    # db.bans.insert_one({"user_id": user.id, "unban_time": None, "reason": reason, "banned_by": inter.author.id})

    await inter.edit_original_response(MessagesCZ.perm_ban_success(user_mention=user.mention))


async def unban(
    inter: disnake.GuildCommandInteraction,
    user: disnake.User,
    reason: str,
    config,
):
    """
    Unban a user
    """
    try:
        await inter.guild.unban(user, reason=reason)
    except disnake.NotFound:
        await inter.edit_original_response(MessagesCZ.invalid_user(user_id=user.id))
        return
    except disnake.Forbidden:
        await inter.edit_original_response(MessagesCZ.ban_permission_error)
        return
    except disnake.HTTPException:
        await inter.edit_original_response(MessagesCZ.ban_failed)
        return

    # Log the unban in the database (pseudo-code, replace with actual DB logic)
    # db.bans.delete_one({"user_id": user.id})

    await inter.edit_original_response(MessagesCZ.unban_success(user_mention=user.mention))
