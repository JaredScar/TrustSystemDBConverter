import json

players_db_file = "assets/playersDB.json"
whitelist_file = "assets/whitelist.json"

vehIdTracker = {}
userTracker = {}
vehId = 1
uid = 1

validPlayersWithDiscord = 0
invalidPlayersWithDiscord = 0

invalidDatas = {}

with open(players_db_file, 'r', encoding="utf-8") as db:
    dbData = json.load(db)
    with open(whitelist_file, 'r', encoding="utf-8") as wl:
        wlData = json.load(wl)
        players = dbData.get("players", [])
        for player in players:
            display_name = player.get("displayName", "").replace("\\", "\\\\")
            player_ids = player.get("ids", [])
            discordId = ""
            for id in player_ids:
                if "discord" in id.lower():
                    discordId = id.lower()
            for id in player_ids:
                if "license" in id.lower():
                    # It's a license, we want to check for vehicles
                    playerWhitelistData = wlData.get(id, [])
                    if discordId and playerWhitelistData:
                        validPlayersWithDiscord = validPlayersWithDiscord + 1
                        for item in playerWhitelistData:
                            allowed = item['allowed']
                            owner = item['owner']
                            spawncode = item['spawncode'].replace("\\", "")
                            if allowed == True or owner == True:
                                # Add DB statement to insert if not owner (trust), if owner (owner)
                                with open('out/inserts.sql', 'a', encoding='utf-8') as file:
                                    if not discordId in userTracker:
                                        # User tracker does not have Discord... Insert user
                                        file.write('\nINSERT INTO `users` (`discord`, `last_username`, `uid`) VALUES ('
                                               + discordId.replace("discord:", "") + ', "' + display_name + '", ' + str(uid) + ');')
                                        userTracker[discordId] = uid
                                    if owner:
                                        if not spawncode in vehIdTracker:
                                            # Does not already have the vehicle saved... We insert it
                                            file.write('\nINSERT INTO `vehicles` (`vid`, `spawncode`, `owned_by_uid`) VALUES ('
                                                   + str(vehId) + ', "' + spawncode + '", ' + str(userTracker[discordId]) + ');')
                                            vehIdTracker[spawncode] = vehId
                                        else:
                                            # Already has vehicle tracked... Update with owner UID
                                            file.write(
                                                '\nUPDATE `vehicles` SET `owned_by_uid` = ' + str(uid) + ' WHERE `vid` = ' + str(vehId) + ';')
                                    else:
                                        # Not an owner, we need to insert the vehicle with no owner
                                        file.write(
                                            '\nINSERT INTO `vehicles` (`vid`, `spawncode`, `owned_by_uid`) VALUES ('
                                            + str(vehId) + ', "' + spawncode + '", null);')
                                vehId = vehId + 1
                                uid = uid + 1
                    else:
                        if playerWhitelistData:
                            print(
                                "[ERROR] Could not find discord for player with last known in-game name `"
                                + display_name + "`")
                            for item in playerWhitelistData:
                                allowed = item['allowed']
                                owner = item['owner']
                                spawncode = item['spawncode'].replace("\\", "")
                                datas = []
                                if allowed == True or owner == True:
                                    # We need to add this to their data
                                    datas.append({'spawncode': spawncode, 'owner': owner, 'allowed': allowed})
                                invalidDatas[id] = {'display_name': display_name, 'datas': datas}
                            invalidPlayersWithDiscord = invalidPlayersWithDiscord + 1
with open('out/missingDiscordUsers.json', 'w') as json_file:
    json.dump(invalidDatas, json_file, indent=4)
print("[DEBUG] Had " + str(validPlayersWithDiscord) + " valid players with a Discord ID associated to them...")
print("[DEBUG] Had " + str(invalidPlayersWithDiscord) + " invalid players with no Discord ID associated...")