# TrustSystemDBConverter

## Overview
`TrustSystemDBConvertor` is a Python script designed as a successor to the original FiveM script named VehicleTrustSystem. This tool simplifies the process of migrating player data from the FiveM server where the VehicleTrustSystem script was running to an SQL database and a JSON file. The SQL database file will contain the queries to be run within the `BadgerTrustSystem+` script which is the successor to the `VehicleTrustSystem` script and is database storage based rather than file based.

## Features
* **Player Data Migration:** Efficiently migrates player data, focusing on Discord-related information, from the FiveM server's `VehicleTrustSystem` script to an SQL inserts database file.


* **JSON File Generation:** Creates a JSON file containing data for players whose Discords could not be found during migration, providing an easy-to-read and portable representation of missing information.
## How to use?
1. **Setup and Configuration:**
   * Ensure the original VehicleTrustSystem script is installed and configured on your FiveM server.
   * Configure the Python script with the necessary details, such as the `playersDB.json` file provided from your txAdmin instance and your `whitelist.json` file provided from the `VehicleTrustSystem` script. Place these files within the `/assets/` directory.


2. **Run the Script:**
   * Execute the Python script to initiate the data migration process.
   * Observe the progress of the migration, and check the generated SQL inserts file and JSON file.


3. **Database Integration:**
   * Apply the generated SQL inserts file to update your SQL database with the migrated player data.


4. **Review Missing Discord Data:**
   * Examine the generated JSON file to identify players whose Discord information could not be migrated successfully.
## Contributions
Contributions and feedback are welcome! Feel free to open issues or pull requests for improvements, bug fixes, or additional features.