from channels.generic.websocket import WebsocketConsumer
import json
from asgiref.sync import async_to_sync
from django.contrib.auth.models import User
from ExThree.models import Message
from django.db.models import Q

class ChatConsumerController(WebsocketConsumer):
    
    def websocket_connect(self, event):
        # accept the connection 
        self.accept()
        
        # getting user is of users tring to chat 
        self.custom_user_id = self.scope['url_route']['kwargs'].get('custom_user_id')
        self.request_user_id = self.scope['url_route']['kwargs'].get('request_user_id')
 
        GetCustomUser = User.objects.get(id = self.custom_user_id)
        GetRequestUser = User.objects.get(id = self.request_user_id)
        
        CustomUser = GetCustomUser.username
        RequestUser = GetRequestUser.username
        
        
        if GetCustomUser is not None and GetRequestUser is not None:
            Users = [CustomUser, RequestUser]
            Users_Id = [self.custom_user_id, self.request_user_id]
            
            # retrive the message of user saved in databse 
            GetUserMsg = Message.objects.filter(
                Q(sender=GetRequestUser, receiver=GetCustomUser) |  # Messages sent to GetCustomUser by GetRequestUser
                Q(sender=GetCustomUser, receiver=GetRequestUser)    # Messages sent to GetRequestUser by GetCustomUser
            )
            print(GetUserMsg)
            
            # Prepare the messages as a list of dictionaries
            messages = []
            for msg  in GetUserMsg:
                messages.append({
                    'content': msg.content,
                    'sender': msg.sender.username,
                    'receiver': msg.receiver.username,
                    'timestamp': msg.timestamp,  # Format the timestamp as needed
                })
            
            
            # Sort the lists
            Users_Id.sort()
            Users.sort()
            
            # create unique room name using user and user_id
            self.room_name = f"{Users[0]}{Users_Id[0]}{Users[1]}{Users_Id[1]}"
            
            
            # create the group of two users 
            async_to_sync(self.channel_layer.group_add)(
                self.room_name , 
                self.channel_name
            )
            
            # send the users to frontend to show on which user in chat 
            self.send(text_data=json.dumps({
                'type': "websocket.accept",
                'CustomUser': CustomUser,
                'user'  : self.channel_name ,
                'messages': messages,
            }))
            
        self.CustomUser = CustomUser
        self.RequestUser = RequestUser   
            
            
        
    def websocket_receive(self, event):
        print(event)
        
        # load the messges getting from frontend 
        text_payload = json.loads(event['text'])
        
        # get the actual messges from text_payload 
        message = text_payload.get('ChatMessage')
        sender  = text_payload.get('Sender')
        time = text_payload.get('time')
        
        # check if the message if empty or not 
        if message != None and message != '':
            
            receiver = None
            if sender == self.RequestUser:
                receiver = self.CustomUser
            else:
                receiver = self.RequestUser
            
            
            SenderUser = User.objects.get(username = sender)
            ReceiverUser = User.objects.get(username = receiver)
            
            #  save the data to databse 
            UserMessages = Message.objects.create(
                sender = SenderUser , 
                receiver = ReceiverUser ,
                content = message , 
                timestamp = time ,
            )
            UserMessages.save()
            
            #  send the message back to user group / room 
            async_to_sync(self.channel_layer.group_send)(self.room_name , {
                'type': 'chat.message',      # create the handler for messges 
                'Text_msg': message ,
                'sender' : sender, 
                'time' : time ,
                'user' : self.channel_name,
            })
            
            
    
    # handler for chat.message 
    def chat_message(self , text_data=None):
        self.send(text_data = json.dumps({
            'type': 'websocket.send' , 
            'text_message': text_data['Text_msg'] , 
            'Sender' : text_data['sender'],
            'time' : text_data['time'],
            'channel_user': self.channel_name ,
            
        }))
        
        self.close()
        
    
    def websocket_disconnect(self, event):
        #disconnect the connection
        async_to_sync(self.channel_layer.group_discard)(
            self.room_name,
            self.channel_name
        )
        