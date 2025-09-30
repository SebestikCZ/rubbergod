from config.messages import Messages as GlobalMessages


class MessagesCZ(GlobalMessages):
    time_param = "Délka prodlevy mezi zprávami v sekundách"
    set_brief = "Nastaví slowmode v aktuálním kanálu"
    set_success = "Slowmode v kanálu {channel} nastaven na {delay} sekund."
    remove_brief = "Vypne slowmode v aktuálním kanálu"
    remove_success = "Slowmode v kanálu {channel} úspěšně odstraněn."
    temp_ban_brief = "Dočasně zabanuje uživatele"
    perm_ban_brief = "Permanentně zabanuje uživatele"
    unban_brief = "Odbanuje uživatele"
    user_param = "Uživatel, kterého chcete zabannovat/odbannovat"
    duration_param = "Doba trvání banu (např. 1h, 30m, 2d)"
    reason_param = "Důvod banu"
    invalid_duration_format = "Neplatný formát délky trvání. Použijte formáty jako `1h`, `30m`, `2d`."
    duration_limits = "Délka trvání musí být mezi 1 minutou a 10 lety."
    ban_permission_error = "Nemám oprávnění k zabannování tohoto uživatele."
    ban_failed = "Nepodařilo se zabannovat uživatele. Zkuste to prosím znovu."
    perm_ban_bracket_error = "Pro permanentní bany prosím neuvádějte závorky s číslem na konci důvodu."
    perm_ban_success = "Uživatel {user_mention} byl úspěšně permanentně zabannován."
    invalid_user = "Uživatel s ID `{user_id}` nebyl nalezen."
    temp_ban_success = "Uživatel {user_mention} byl úspěšně dočasně zabannován na {duration}."
    unban_success = "Uživatel {user_mention} byl úspěšně odbannován."

    moderation_log = "### {action_emoji} {target.mention} `{target.id}` was {action}\n" \
                    "- {timestamp}\n" \
                    "- Given By: {entry.user.mention} `{entry.user.id}`\n" \
                    "- Reason: `{entry.reason}`"
    moderation_log_tempban = "### {action_emoji} {target.mention} `{target.id}` was {action}\n" \
                             "- {timestamp}\n" \
                             "- Given By: {entry.user.mention} `{entry.user.id}`\n" \
                             "- Reason: `{entry.reason}`" \
                             " (Duration: `{duration}`)"
