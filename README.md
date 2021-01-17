# SAM
SAM is a telegram bot that can be added to group chats to allow for easy scheduling. Once SAM is added to a group chat, it sends a list of times to the entire group. Each group member can then choose the specific hours that they are available, and SAM notifies the people who are all available at a specific time.

It is structured in such a way that the severer handling Telegram communication is separate from the server handling data transactions, which allows for a more flexible framework to add platforms other than telegram.
