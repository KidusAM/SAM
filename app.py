import telegram
import logging 
import socket
import traceback

TOKEN = '1543058829:AAEJyUJeyGD5Z1u7xjvtmN12TMFyZrZ0lsE'




def connectServer():
    HOST = '127.0.0.1'
    PORT = 4065
    
    global sock 
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.connect((HOST,PORT))
        



def send (msg:str):
    global sock
    sock.sendall(msg.encode())
    
    
    
    

from telegram import Update
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (Updater,CommandHandler,MessageHandler,Filters,ConversationHandler,CallbackContext,CallbackQueryHandler)

bot = telegram.Bot(token=TOKEN)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)


def start(update:Update, context:CallbackContext):
    
                  
    if (update.effective_chat.type=="private"):
        context.bot.send_message(chat_id=update.effective_chat.id, 
                             text="""Hello my name is Sam, I can help organize casual meetups with your friends. If you would like to schedule meetups with your friends today please type in command /schedule
                  to scheule a time to speak. Please add me to a group chat with your friends""")
    
    elif (update.effective_chat.type=="group"):
        context.bot.send_message(chat_id=update.effective_chat.id, 
                             text="""Hello my name is Sam, I can help organize casual meetups with your friends. If you would like to schedule meetups with your friends today please type in command /schedule
                  to scheule a time to speak""")
        gid = str(update.effective_chat.id)
        uid = str(update.message.from_user.id)
        fname = update.message.from_user.first_name
      
        send(" ".join(("ADD",uid,gid,fname)))
    
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, 
                             text="""Hello my name is Sam, I can help organize casual meetups with your friends. If you would like to schedule meetups with your friends today please type in command /schedule
                  to scheule a time to speak""")
        

    
                             

def schedule(update: Update,context: CallbackContext):

    inline_keyboard = []
    
    
    lst =  ['09:00-10:00','10:00-11:00','11:00-12:00',
            '12:00-13:00','13:00-14:00','14:00-15:00',
            '16:00-17:00','17:00-18:00','18:00-19:00',
            '19:00-20:00','20:00-21:00','21:00-22:00',
            '22:00-23:00','23:00-24:00']
    
    for item in lst:
        inline_keyboard.append([
            InlineKeyboardButton(item, callback_data=parseTime(item))
            ])

    
    reply_markup = InlineKeyboardMarkup(inline_keyboard)

    update.message.reply_text("Choose the time you're free",reply_markup=reply_markup)
    
    
def parseTime(timeVal):
    return timeVal[0:2]


def button(update: Update, context:CallbackContext):
    query = update.callback_query

    chat_id = query.from_user.id
    uid = chat_id 

    query.answer()

    bot.sendMessage(chat_id, f"Selected option: {query.data}")
    send(" ".join(("SCHEDULE",str(uid),query.data)))
    



      

    

    
def parseLst(names):
    string =  ""
    for i in range(len(names)):
        if(i==0):
            string = string+names[i]
        else:
            string = string+", "+names[i]
    
    return string                
                        
                
                
                
                

def main():
     
     updater = Updater(TOKEN, use_context=True)
     dispatcher = updater.dispatcher
     connectServer()
     
     conv_handler = ConversationHandler(
         entry_points=[CommandHandler('start', start),
                       CommandHandler('schedule',schedule)
                       ],
         states=  {},
         fallbacks = [],
         )
     
     dispatcher.add_handler(conv_handler)
    
     updater.start_polling()
    
    
    
     while(True):
              try:
                   global sock 
                   data = sock.recv(4096).decode().strip()
                   print(data)
                   time_lst = data.split(" ")
                   time = time_lst[0]
                   lower_time = time+":00"
                   if(int(time)<10):
                       upper_time = "0"+str(int(time)+1)+":00"
                   else:
                       upper_time = str(int(time)+1)+":00"
                
                
                   uid_name_dict = []
                
                
                   uid_name = time_lst[1].split(",")
                
                   names  = []
                   for val in uid_name:
                       val_list = val.split(';')
                       val_uid = val_list[0]
                       val_name = val_list[1]
                       uid_name_dict.append((val_uid,val_name))
                       names.append(val_name)
                  
                   for key in uid_name_dict:
                       j=None
                       UID = key[0]
                       name = key[1]
                       for i in range(len(names)):
                           if (names[i]==name):
                               j=i
                               break
                       names.pop(j)
                       bot.sendMessage(chat_id=UID,text="""Hello {nom}, you are scheduled to meet with {noms} from {ltime} to {utime} """.format(nom=name,noms=parseLst(names),ltime=lower_time,utime=upper_time))
                       names.append(name)
                    
                    
                     
              except KeyboardInterrupt:
                     updater.idle()
                    
              except: 
                      traceback.print_exc()    
                      continue
                      
        
if __name__ == "__main__":
    main()
    
        
        
         












