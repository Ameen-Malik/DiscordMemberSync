# Discord Member Data Collector

A Discord bot that helps collect and verify member data from your server.

## Features

- **Member Data Collection**: Collect all server members' data (username, display name, ID)
- **Member Verification**: Match members against a list of verified usernames
- **CSV Export**: Export results in organized CSV files

## Setup

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file with your Discord bot token:
   ```
   DISCORD_BOT_TOKEN=your_token_here
   ```

## Usage

### 1. Collect Member Data
Run the bot and use the command:
```
!fetch_user_data
```
This creates a CSV file with all server members' data.

### 2. Verify Members
1. Create a `usernames.csv` file with verified usernames
2. Use the command:
   ```
   !fetch_ids
   ```
This generates two files:
- `matching_user_ids_[server_id].csv`: Verified members
- `unmatched_user_ids_[server_id].csv`: Unverified members

## Files
- `collect_mem_data.py`: Collects all server member data
- `verified_mem_data.py`: Verifies members against a list
- `requirements.txt`: Project dependencies

## Note
Make sure your bot has the following permissions:
- View Server Members
- Read Messages
- Send Messages

## Author
**Ameen Malik**  
Email: am.ameenmalik@gmail.com 