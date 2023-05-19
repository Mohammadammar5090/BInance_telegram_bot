import telebot
from telebot import types 
import random
from telegram import ParseMode
import BINANCE
TOKEN = ' telegram bot token '

#Init the  bot with token
bot = telebot.TeleBot(TOKEN)


# set list of commands on the left side keyboard
bot.set_my_commands([
    telebot.types.BotCommand("/start ", "BOT commands"),
    telebot.types.BotCommand("/cancel", "print usage")
                    ])

#This will generate buttons for us in more elegant way
def generate_buttons(ordar_names, markup):

    for button in ordar_names:
        markup.add(types.KeyboardButton(button))
    return markup



#To catch the message you need to use this decorator. 
@bot.message_handler(commands=['start'])
def commands_buttons(message):



    #Init keyboard markup      
    markup = types.ReplyKeyboardMarkup(row_width=5,one_time_keyboard=True,resize_keyboard=True)
    
    #Add to buttons by list with ours generate_buttons function.
    markup = generate_buttons(['Make an order',
                                'Show info all coin in the account',
                                'Show the free (usdt/busd) in the account',
                                'Show the history of (buy/sell) orders'],
                                 markup)
    
    
    message = bot.reply_to(message, "Hi there! What you want to do?", reply_markup=markup)

    # Here we assign the next handler function and pass in our response from the user. 
    bot.register_next_step_handler(message,executing_commands1)
    


def executing_commands1(message):
    print(message.text)


    if message.text=="Make an order":

            amount=["Make market order",
                    "Make limil order",
                    "Make OCO order"]

            get_button = types.ReplyKeyboardMarkup(row_width=2,one_time_keyboard=True)

    # Add to buttons by list with ours generate_buttons function.

            markup_amount = generate_buttons(amount,get_button) # money is how much the user will spent from the free (USDT/BUSD) coin he had
           
            message = bot.reply_to(message, "Choose what you want to do :", reply_markup=markup_amount)
            bot.register_next_step_handler(message,executing_commands1_2)



        
    if message.text=="Show info all coin in the account":
        bot.send_message(message.chat.id,"This is what you have in your account : ")
        bot.send_document(message.chat.id,(open(r"C:\Users\omara\OneDrive\Desktop\BOT Binance\Account_asset_info.xlsx","rb")))

    if message.text=="Show the free (usdt/busd) in the account":
        pass

    if message.text=="Show the history of (buy/sell) orders":
        pass





def executing_commands1_2(message):

    if message.text=="Make market order": # the BUSD and USDT  coins

        amount=["Make market order buy",
                "Make market order sell"]

        get_button = types.ReplyKeyboardMarkup(row_width=2,one_time_keyboard=True)
        
        markup = generate_buttons(amount,get_button)
        message = bot.reply_to(message, "Choose what you want to do :", reply_markup=markup)
        bot.register_next_step_handler(message,executing_commands1_3)

    if message.text=="Make limil order": # the BUSD and USDT  coins

        amount=["Make limil order buy",
                "Make limil order sell"]

        get_button = types.ReplyKeyboardMarkup(row_width=2,one_time_keyboard=True)
        
        markup = generate_buttons(amount,get_button)
        message = bot.reply_to(message, "Choose what you want to do :", reply_markup=markup)
        bot.register_next_step_handler(message,executing_commands1_3)

    if message.text=="Make OCO order": # the BUSD and USDT  coins

        amount=["Make OCO order buy",
                "Make OCO order sell"]

        get_button = types.ReplyKeyboardMarkup(row_width=2,one_time_keyboard=True)
        
        markup = generate_buttons(amount,get_button)
        message = bot.reply_to(message, "Choose what you want to do :", reply_markup=markup)
        bot.register_next_step_handler(message,executing_commands1_3)



# helper function
def assistant_factor(message,type,text0,function):

    get_button = types.ReplyKeyboardMarkup(row_width=2,one_time_keyboard=True)
    markup = generate_buttons(type,get_button)
    message = bot.reply_to(message, text0, reply_markup=markup)
    bot.register_next_step_handler(message,function)






def executing_commands1_3(message):
    message_handler=message.text
    amount=['BNBBUSD',       
                'BTCBUSD',
                    'ETHBUSD',
                        'ADABUSD',
                            'BNBUSDT',
                                'BTCUSDT', 
                                    'ETHUSDT',
                                        'ADAUSDT']


    text_buy='Choose the ticker you want to buy or\n you can enter it like "BNBBUSD" :'
    text_sell='Choose the ticker you want to sell or\n you can enter it like "BNBBUSD" :'

    ############# Make market order ############
    if message.text == "Make market order buy":

        assistant_factor(message,amount,text_buy,make_market_buy)

    if message.text == "Make market order sell":

        assistant_factor(message,amount,text_sell,make_market_sell)


    ############# Make limil order ############
    if message.text == "Make limil order buy":

        assistant_factor(message,amount,text_buy,make_limil_buy)
  
    if message.text == "Make limil order sell":

        assistant_factor(message,amount,text_sell,make_limil_sell)


    ############# Make OCO order ############
    if message.text == "Make OCO order buy":

        assistant_factor(message,amount,text_buy,executing_commands1_3_1)

    if message.text == "Make OCO order sell":
        assistant_factor(message,amount,text_sell,executing_commands1_3_1)


    else:
        '''
        
        Do something

        '''
        pass










coin_list=[]
amount_llist=[]
limit_llist=[]
amount=['5% =(money)',       
            '10% =(money)',
                '25% =(money)',
                    '50% =(money)',
                        '60% =(money)',
                            '75% =(money)', 
                                '90% =(money)',
                                    '100% =(money)']

            
text_buy='Choose the quantity you want to purchase or\n you can enter it like "{price of coin digit}" :'
text_sell='Choose the quantity you want to sell or\n you can enter it like "{price of coin digit}" :'

def make_market_buy(message,amount=amount):
    
    ticker = message.text
    coin_list.append(ticker)

    text = text_buy

    assistant_factor(message,amount,text,confirm_market_buy)

def make_market_sell(message,amount=amount):

    ticker = message.text
    coin_list.append(ticker)
    text = text_sell                      
    assistant_factor(message,amount,text,confirm_market_buy)
    

############################################################################
############################################################################
def make_limil_buy(message,amount=amount):

    ticker = message.text
    coin_list.append(ticker) 

    text = text_buy                      
    assistant_factor(message,amount,text,confirm_limit_buy)


def make_limil_sell(message,amount=amount):
    ticker = message.text
    coin_list.append(ticker) 

    text = text_sell                      
    assistant_factor(message,amount,text,confirm_limit_sell)

############################################################################
############################################################################






#########################################################
###################### confirm ##########################
#########################################################
def confirm_market_buy(message,coin_list=coin_list,amount_llist=amount_llist):
    amount_llist.append(message.text)
    print(amount_llist,"     ",coin_list)
    '''



        If he had enough of the BUSD or USDT to continue    
    
    
    
    '''
    markeup=types.InlineKeyboardMarkup([[types.InlineKeyboardButton("Confirm market buy order",callback_data="Confirm market buy order")],
                                        [types.InlineKeyboardButton("Cancel market buy order",callback_data="Cancel market buy order")]])
    message = bot.reply_to(message, "Do you want to confirm the oreder? : ", reply_markup=markeup)



def confirm_market_sell(message,coin_list=coin_list,amount_llist=amount_llist,limit_llist=limit_llist):
    amount_llist.append(message.text)
    print(amount_llist,"     ",coin_list)
    '''



        If he had enough of the coin to continue    
    
    
    
    '''
    markeup=types.InlineKeyboardMarkup([[types.InlineKeyboardButton("Confirm market sell order",callback_data="Confirm market sell order")],
                                        [types.InlineKeyboardButton("Cancel market sell order",callback_data="Confirm market sell order")]])
    message = bot.reply_to(message, "Do you want to confirm the oreder? : ", reply_markup=markeup)


def confirm_limit_buy(message,coin_list=coin_list,amount_llist=amount_llist,limit_llist=limit_llist):

    '''

        If he had enough of the coin to continue    
    
    '''

    amount_llist.append(message.text)
    print(amount_llist,"     ",coin_list)

    text = '''Please enter the limit to buy
              Note: It must be the same number of digits
              in this example or less : "{the price W.R.T binance}" '''
    markup = types.ForceReply(selective=False)
    message = bot.reply_to(message,text,reply_markup=markup)

    '''
        If he enter the true thing   
    '''    

    limit_llist.append(message.text)
    print(limit_llist)
    bot.register_next_step_handler(message,confirm_button)


def confirm_button(message):
    markeup=types.InlineKeyboardMarkup([[types.InlineKeyboardButton("Confirm limit buy order",callback_data="Confirm limit buy order")],
                                        [types.InlineKeyboardButton("Cancel limit buy order",callback_data="Confirm limit buy order")]])
    message = bot.reply_to(message, "Do you want to confirm the oreder? : ", reply_markup=markeup)




def confirm_limit_sell(message,coin_list=coin_list,amount_llist=amount_llist):

    '''

        If he had enough of the coin to continue    
    
    '''

    amount_llist.append(message.text)
    print(amount_llist,"     ",coin_list)

    text = '''Please enter the limit to sell
              Note: It must be the same number of digits
              in this example or less : "{the price W.R.T binance}" '''
    message = bot.send_message(message.chat.id,text)

    '''

        If he enter the true thing   
    
    '''    

    limit_llist.append(message.text)


    markeup=types.InlineKeyboardMarkup([[types.InlineKeyboardButton("Confirm limit sell order",callback_data="Confirm limit sell order")],
                                        [types.InlineKeyboardButton("Cancel limit sell order",callback_data="Confirm limit sell order")]])
    message = bot.reply_to(message, "Do you want to confirm the oreder? : ", reply_markup=markeup)

@bot.callback_query_handler(func=lambda call:types.CallbackQuery)
def callback_inline(call):

    ############# Make market order ############
    if call.data=="Confirm market buy order":
        bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
        bot.send_message(call.message.chat.id,"the order is confirmed again? /start")

    if call.data=="Confirm market sell order":
        bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)           
        bot.send_message(call.message.chat.id,"the order is canceled again?/ start")


    if call.data=="Cancel market buy order":
        bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
        bot.send_message(call.message.chat.id,"the order is confirmed again? /start")

    if call.data=="Cancel market sell order":
        bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)           
        bot.send_message(call.message.chat.id,"the order is canceled again?/ start")

    ############# Make limil order ############
    if call.data=="Confirm limit buy order":
        bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
        bot.send_message(call.message.chat.id,"the order is confirmed again? /start")

    if call.data=="Confirm limit sell order":
        bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)           
        bot.send_message(call.message.chat.id,"the order is canceled again?/ start")


    if call.data=="Cancel limit buy order":
        bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
        bot.send_message(call.message.chat.id,"the order is confirmed again? /start")

    if call.data=="Cancel limit sell order":
        bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)           
        bot.send_message(call.message.chat.id,"the order is canceled again?/ start")

    ############# Make OCO order ############






        amount_llist.pop(0)
        coin_list.pop(0)


def make_buy(message,coin):
    msg1=str(message.text).find("=")
    msg=str(message.text)[:msg1-2]
    print(coin)
    print(msg) 
    #
    get_button = types.ReplyKeyboardMarkup(row_width=2,one_time_keyboard=True,resize_keyboard=True) 
    markup_confirm = generate_buttons([ 'confirm',       
                                        'cancel'],
                                        get_button) 

    message = bot.reply_to(message, "Do you want to continue?", reply_markup=markup_confirm)
    bot.register_next_step_handler(message,make_buy_confirm)  






def make_sell(message):
        msg1=str(message.text).find("=")
        msg=str(message.text)[:msg1-2]
        print(msg) 
        # 
        get_button = types.ReplyKeyboardMarkup(row_width=2,one_time_keyboard=True,resize_keyboard=True)
        markup_confirm = generate_buttons(['confirm',       
                                          'cancel'],
                                          get_button) 

        message = bot.reply_to(message, "Do you want to continue?", reply_markup=markup_confirm)
        bot.register_next_step_handler(message,make_sell_confirm)  






def make_buy_confirm(message):

    print(message.text,"::","execute the confirm buy order (will be here)")

    if message.text=="confirm":
        bot.send_message(message.chat.id," *The buy order is confirmed*  ",parse_mode=ParseMode.MARKDOWN) # `text` copy
        bot.send_message(message.chat.id,"again? --> /start")
    
    if message.text=="cancel":
        bot.send_message(message.chat.id," *The buy order is canceled*  ",parse_mode=ParseMode.MARKDOWN) # `text` copy
        bot.send_message(message.chat.id,"again? --> /start")
    

def make_sell_confirm(message):

    print(message.text,"::","execute the confirm sell order (will be here)")
    if message.text=="confirm":
        bot.send_message(message.chat.id," *The sell order is confirmed*  ",parse_mode=ParseMode.MARKDOWN) # `text` copy
        bot.send_message(message.chat.id,"again? --> /start")

    if message.text=="cancel":
        bot.send_message(message.chat.id," *The sell order is canceled*  ",parse_mode=ParseMode.MARKDOWN) # `text` copy
        bot.send_message(message.chat.id,"again? --> /start")
        

# Here we no longer need to specify the decorator function

# Launches the bot in infinite loop mode with additional
#...exception handling, which allows the bot
#...to work even in case of errors. 
bot.infinity_polling()



