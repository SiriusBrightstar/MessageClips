# Privacy Policy for MessageClips

MessageClips is designed with a "privacy-first" approach. We aim to process the absolute minimum amount of data required to function.

1. **Data Collection**: MessageClips **does not** store any user data, message content, or metadata in a persistent database.
2. **Data Processing**:
   - When you react with a bookmark emoji (🔖), the bot temporarily reads the message content to send it to your DMs. 
   - This data is processed in-memory and is not logged or saved after the DM is sent.
3. **Data Sharing**: We do not share, sell, or trade any information with third parties.
4. **Logs**: Standard system logs (via journalctl) may contain technical metadata (e.g., User IDs) for troubleshooting purposes but never include message contents. These logs are stored locally on the hosting server and are automatically rotated and purged by the system (systemd-journald) based on disk space and age.
5. **Third Parties**: This bot operates on the Discord platform; please refer to [Discord's Privacy Policy](https://discord.com/privacy) for information on how they handle your data.
