# SAM
SAM is a telegram bot that can be added to group chats to allow for easy scheduling. Once SAM is added to a group chat, it sends a list of times to the entire group. Each group member can then choose the specific hours that they are available, and SAM notifies the people who are all available at a specific time.

It is structured in such a way that the severer handling Telegram communication is separate from the server handling data transactions, which allows for a more flexible framework to add platforms other than telegram.

File_organization: 
- app.py
  -SAMBACK:
    - main.py
    - DB:
      - data.db 
 
 App.py harnesses the python telegram-bot to communciate through telegram's API directly with users who add SaM to their groups. This front end server will recieve times to schedule meetings and send these times to the backend server which is main.py. Main.py processes this information from the front-end implementing into a database and running databses queries in SQL lite. Once a match has been found between users, main.py sends a request to app.py to forward users who have matched a message outlining the time of the scheduled meeting and the perso/persons they will be meeting with. 
 
 
 
 
  


