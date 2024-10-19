import json
from telethon import TelegramClient, events, sync,types
from dotenv import load_dotenv,set_key,get_key
import os 
import asyncio
import warnings
from time import sleep,time
from telethon.tl.functions.channels import InviteToChannelRequest
from telethon.tl.functions.photos import UploadProfilePhotoRequest
from typing import Dict, List,Optional
from telethon.tl.types import InputPeerChannel, Message,InputMediaPoll, Poll, PollAnswer
from telethon.tl.custom import Button
import io
import requests
from functools import wraps
import ast
import mimetypes
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.style import Style
import getpass

console = Console()

# Suppress DeprecationWarning
warnings.simplefilter("ignore", category=DeprecationWarning)

load_dotenv()



def ConfigureDatabase():
    """
    Configures the database by setting up environment variables required for 
    accessing the Telegram API and channel.

    This function prompts the user to input their Telegram API ID, API Hash, 
    phone number, channel ID, and session name. It then writes these details 
    to a `.env` file and loads the environment variables.

    The environment variables are:
        - `API_ID`: The API ID obtained from my.telegram.org.
        - `API_HASH`: The API Hash obtained from my.telegram.org.
        - `PHONE_NUMBER`: The phone number associated with the Telegram account, including the country code.
        - `CHANNEL_ID`: The ID of the Telegram channel.
        - `SESSION_NAME`: The name of the session.

    After configuring, the function loads these variables from the `.env` file 
    into the environment.

    Raises
    ------
    Exception
        If there is any issue with creating or writing to the `.env` file.
    """
    
    dotenv_path = os.path.join(os.getcwd(), '.env')
    if not os.path.exists(dotenv_path):
        open(dotenv_path, 'w').close()

    global API_ID, API_HASH, CHANNEL_ID, PHONE_NUMBER

    API_ID = input("Enter Your API ID: ")
    API_HASH = input("Enter Your API HASH: ")
    PHONE_NUMBER = input("Enter Your Phone Number with country code: ")
    CHANNEL_ID = input("Enter Your Channel ID: ")
    SESSION_NAME = input("Session Name: ")
    
    # Check if the .env file exists, if not create it
    # if not os.path.exists(dotenv_path):
    #     open(dotenv_path, 'w').close()

    set_key(dotenv_path, 'CHANNEL_ID', CHANNEL_ID)
    set_key(dotenv_path, 'API_ID', API_ID)
    set_key(dotenv_path, 'API_HASH', API_HASH)
    set_key(dotenv_path, 'PHONE_NUMBER', PHONE_NUMBER)
    set_key(dotenv_path, 'SESSION_NAME', SESSION_NAME)
    
    load_dotenv()
    # Your API ID and hash (from my.telegram.org)
    API_ID = get_key(dotenv_path,'API_ID')
    API_HASH = get_key(dotenv_path,'API_HASH')
    PHONE_NUMBER = get_key(dotenv_path,'PHONE_NUMBER')  # Your phone number including country code
    CHANNEL_ID = int(get_key(dotenv_path,'CHANNEL_ID'))
    SESSION_NAME = get_key(dotenv_path,"SESSION_NAME")
    print("configured Successfully.")





class TeleCloudChannel:
    def __init__(self,api_id:str=None,api_hash:str=None,channel_id:int=None,phone_number:int=None,session_name:str=None):
        if api_id is None or api_hash is None or channel_id is None or phone_number is None or session_name is None:
            
            dotenv_path = os.path.join(os.getcwd(), '.env')
            if not os.path.exists(dotenv_path):
                open(dotenv_path, 'w').close()
            
            if  get_key(dotenv_path,'CHANNEL_ID') is None or get_key(dotenv_path,'API_ID') is None or get_key(dotenv_path,'API_HASH') is None or get_key(dotenv_path,'PHONE_NUMBER') is None:
                # raise Exception("Configure your telegram channel.\nfrom nara import tele_db\ntele_db.ConfigureDatabase()")
                ConfigureDatabase()
                load_dotenv()
            
            # Your API ID and hash (from my.telegram.org)
            self.API_ID = get_key(dotenv_path,'API_ID')
            self.API_HASH = get_key(dotenv_path,'API_HASH')
            self.PHONE_NUMBER = get_key(dotenv_path,'PHONE_NUMBER')  # Your phone number including country code
            self.SESSION_NAME = get_key(dotenv_path,"SESSION_NAME")
            self.CHANNEL_ID = get_key(dotenv_path,'CHANNEL_ID')
            # print("channel id = ",self.CHANNEL_ID,type(self.CHANNEL_ID))
        else:
            self.API_ID = api_id
            self.API_HASH = api_hash
            self.PHONE_NUMBER = phone_number
            self.SESSION_NAME = session_name
            self.CHANNEL_ID = int(channel_id)
        # Create the client and connect
        self.client:TelegramClient =TelegramClient(self.SESSION_NAME, self.API_ID, self.API_HASH)
        self.client.start(self.PHONE_NUMBER)
        if not  self.client.is_user_authorized():
            print("You need to authorize first. Follow the instructions printed on the console.")
            return False
        
        # # Fetch the channel entity once and set it globally
        # self.channel:InputPeerChannel =  self.client.get_entity(CHANNEL_ID)
        try:
            self.channel = self.client.get_entity(types.PeerChannel(int(self.CHANNEL_ID)))
            print(f"Successfully connected to channel: {self.channel.title}")
        except Exception as e:
            print(f"An error occurred while getting the channel entity: {e}")
            self.channel = None
    
    async def add_participant(self, PHONE_NUMBER: str) -> None:
        try:
            await self.client(InviteToChannelRequest(
                channel=self.channel,
                users=[await self.client.get_input_entity(PHONE_NUMBER)]
            ))
            print(f"User with phone number {PHONE_NUMBER} added to the channel.")
        except Exception as e:
            print(f"An error occurred while adding participant: {e}")
    
    async def forward_message(self, from_chat_id: int, to_chat_id: int, message_ids: List[int]) -> None:
        try:
            await self.client.forward_messages(to_chat_id, from_chat_id, message_ids)
            print(f"Messages forwarded successfully.")
        except Exception as e:
            print(f"An error occurred while forwarding messages: {e}")
    
    async def pin_message(self, message_id: int) -> None:
        try:
            await self.client.pin_message(self.channel, message_id)
            print("Message pinned successfully.")
        except Exception as e:
            print(f"An error occurred while pinning the message: {e}")
    
    async def get_chat_info(self) -> None:
        try:
            chat = await self.client.get_entity(self.channel)
            print(f"Chat Title: {chat.title}")
            print(f"Participants Count: {chat.participants_count}")
            print(f"Admins: {chat.admins}")
            print(f"ID: {chat.id}")
        except Exception as e:
            print(f"An error occurred while getting chat info: {e}")

    
    async def set_chat_photo(self, photo_path: str) -> None:
        try:
            await self.client(UploadProfilePhotoRequest(
                file=await self.client.upload_file(photo_path)
            ))
            print("Chat photo set successfully.")
        except Exception as e:
            print(f"An error occurred while setting chat photo: {e}")


    async def send_message(self, message: str,) -> int:
            sent_message = await self.client.send_message(self.channel, message)
            return sent_message.id

    async def get_messages(self, limit: int = 10) -> List[Message]:
        messages = await self.client.get_messages(self.channel, limit=limit)
        for message in messages:
            # print(f"Message ID: {message.id}")
            # print(f"Date: {message.date}")
            # print(f"Sender: {message.sender_id}")
            # print(f"Message: {message.message}\n")
            # print("message = ",message)
            pass
        return messages
    
        


    async def find_text_by_id(self, message_id: int) -> str:
        try:
            message = await self.client.get_messages(self.channel, ids=message_id)
            
            if message:
                return message.text
            else:
                return ""
        except Exception as e:
            print(f"An error occurred while finding text by ID: {e}")
            return ""
    
    async def get_caption_and_save_file(self, message_id: int,table_id:str='1',save_file:bool=False) -> tuple:
        try:
            # Get the message by its ID
            message = await self.client.get_messages(self.channel, ids=message_id)

            # Get the caption if available
            caption = message.message if message.message else ""

            # Check if the message has media (file)
            if message.media and save_file:
                # Define the file path to save the media
                file_path = os.path.join(os.getcwd(), f"downloaded_id_{message_id}")

                # Download the media (file)
                await self.client.download_media(message, file=file_path)

                # Return the caption and file path
                return caption, file_path
            else:
                # No media found, return only the caption
                return caption, None

        except Exception as e:
            print(f"An error occurred: {e}")
            return "", None

    async def extract_list_from_message(self, message_id: int) -> list:
        try:
            # Get the text of the message
            message_text = await self.find_text_by_id(message_id)
            message_text = message_text.replace('`', '')
                        # Find the index of '[' and ']'
            start_index = message_text.find('[')
            end_index = message_text.find(']',-1)

            # Extract the substring containing the list
            if start_index != -1 and end_index != -1:
                list_string = message_text[start_index:end_index+1]
                # Remove any newline characters
                list_string = list_string.replace('\n', '')
                # Convert the string representation of list to a list
                extracted_list = eval(list_string)
                return extracted_list
            else:raise Exception("List not found in message while extrating list from msg id")
        except Exception as e:
            print(f"An error occurred while extracting list from message: {e}")
            return []

    async def find_message_by_same_text(self, search_text: str) -> Optional[Message]:
        try:
            async for message in self.client.iter_messages(self.channel):
                if message.message and search_text.lower() == message.message.lower():
                    # print(f"Message found: {message.message}")
                    return (message.id, message.message)
            # print("No message found with the given text.")
            return None
        except Exception as e:
            print(f"An error occurred while searching for the message: {e}")

    async def find_message_by_text(self, search_text: str) -> Optional[Message]:
        try:
            async for message in self.client.iter_messages(self.channel):
                if message.message and search_text.lower() in message.message.lower():
                    return (message.id, message.message)
            return None
        except Exception as e:
            print(f"An error occurred while searching for the message: {e}")
    async def get_message_text(self, message_id: int) -> str:
        try:
            message = await self.client.get_messages(self.channel, ids=message_id)
            if message:
                return message.text
            else:
                return ""
        except Exception as e:
            return ""
    async def edit_message(self, message_id: int, new_message_text: str) -> None:
        try:
            await self.client.edit_message(self.channel, message_id, new_message_text)
        except Exception as e:
            print(f"An error occurred while editing the message: {e}")

    async def upload_file(self, file: str,file_extension: str, caption: str = None) -> None:
        if file.startswith("http://") or file.startswith("https://"):
           
            # Handle the case where the input is a URL
                response = requests.get(file)
                response.raise_for_status()
                file_data = io.BytesIO(response.content)
                
                # Extract the file name and ensure it has a valid extension
                file_name = file.split("?")[0].split("/")[-1]
                mime_type, _ = mimetypes.guess_type(file_name)
                if mime_type is None:
                    file_name += '.'+file_extension.replace(".","")  # Default to .png if no valid extension found
                
                file_data.name = file_name
        else:
            # Handle the case where the input is a file path
            file_data = await self.client.upload_file(file)
            
        await self.client.send_file(self.channel, file_data, caption=caption)
        print(f"File uploaded: {file} with caption: {caption}")


    async def upload_files(self, files_with_extensions: dict, caption: str = "",message_id=None) -> list:
        file_data_list = []
        
        try:
            for file, file_extension in files_with_extensions.items():
                if file.startswith("http://") or file.startswith("https://"):
                    # Handle the case where the input is a URL
                    response = requests.get(file)
                    response.raise_for_status()
                    file_data = io.BytesIO(response.content)
                    
                    # Extract the file name and ensure it has a valid extension
                    file_name = file.split("?")[0].split("/")[-1]
                    mime_type, _ = mimetypes.guess_type(file_name)
                    if mime_type is None:
                        file_name += '.' + file_extension.replace(".", "")  # Use provided file extension
                    
                    file_data.name = file_name
                else:
                    # Handle the case where the input is a file path
                    file_data = await self.client.upload_file(file)
                
                file_data_list.append(file_data)

            if message_id:
                reply_msg = await self.client.send_file(self.channel, file_data_list, caption=caption,reply_to=message_id)
                msg_id:list = [msg.id for msg in reply_msg]
                return msg_id
            else:  
                msgs = await self.client.send_file(self.channel, file_data_list, caption=caption)
                msg_id:list = [msg.id for msg in msgs]
                return msg_id

            # print(f"Files uploaded: {list(files_with_extensions.keys())} with caption: {caption}")
        except Exception as e:
            raise Exception(f"An error occurred while uploading files: {e}")




    async def download_file(self, message: Message, file_path: str) -> None:
        await self.client.download_media(message, file_path)
        print(f"File downloaded to: {file_path}")

    async def delete_message(self, message_id: int) -> None:
        try:
            await self.client.delete_messages(self.channel, message_id)
            print(f"Message with ID {message_id} deleted successfully.")
        except Exception as e:
            print(f"An error occurred while deleting the message: {e}")

    async def delete_all_messages(self) -> None:
        try:
            async for message in self.client.iter_messages(self.channel):
                await self.client.delete_messages(self.channel, message.id)
            print("All messages deleted successfully.")
        except Exception as e:
            print(f"An error occurred while deleting messages: {e}")

        
    async def find_replies_to_message_id(self, message_id: int) -> List[str]:
        try:
            replies_text = []
            async for message in self.client.iter_messages(self.channel, reply_to=message_id):
                replies_text.append(message.text)
            return replies_text
        except Exception as e:
            print(f"An error occurred while finding replies to message ID {message_id}: {e}")
            return []

    async def find_table(self, table_id: str) -> Optional[Message]:
        try:
            async for message in self.client.iter_messages(self.channel):
                if message.message and table_id.lower() in message.message.lower() and message.message.lower().startswith("table_id:"):
                    return (message.id, message.message)
            return None
        except Exception as e:
            print(f"An error occurred while searching for the message: {e}")

    async def send_message_in_reply(self, message_id: int, message: str) -> None:
        try:
            reply_msg = await self.client.send_message(self.channel, message, reply_to=message_id)
            return reply_msg.id
        except Exception as e:
            print(f"An error occurred while sending message in reply mode: {e}")

    async def table_list(self) -> list:
        try:
            table_li:list = []
            async for message in self.client.iter_messages(self.channel):
                if message.message and message.message.lower().startswith("table_id:"):
                    table_li.append(message.message.split('\n')[0])
            return table_li
        except Exception as e:
            print(f"An error occurred while sending message in reply mode: {e}")



    async def main(self) -> None:
        if not await self.connect_client():
            return

        # Example: Sending a message
        # await self.send_message('{"id":"1"}',formatted=True)
        # await self.send_message('`{"id":"45"}`')

        # # Example: Edit messages
        # await self.edit_message(message_id=12, new_message_text="Edited message by subh")

        # # Example: REPLYING TO MESSAGES
        # await self.send_reply_message(reply_to_message_id=406, message="Reply dsfgdfg by subh")

        # # Example: Getting messages
        # messages = await self.get_messages(limit=3)

        # # Example: Uploading a file
        # await self.upload_file('path/to/your/file.txt')

        # # Example: Uploading an image from a URL
        await self.upload_file_from_url(file_url='https://cdn.discordapp.com/attachments/1192019829171957842/1246615576080810094/360_F_436675446_jGWzkVDah3b6ONZxhhN13s6I4iFnjLGJ.png?ex=665d08ba&is=665bb73a&hm=d74e8a1b9db1c8494160b34230493f27994ec4439660ef8c8ef61f144bd43936&', caption='[]')
        # # uplaoding an video/any file from a URL
        # await self.upload_file_from_url(file_url='https://cdn.discordapp.com/attachments/1231664483210891426/1246697245928063006/1.mp4?ex=665d54c9&is=665c0349&hm=2f16ccde978d9c01a8aeda937bf3b70288a5c27dd70d4033c175372510ded4c4&', caption='This is an video from URL')

        # # Example: Downloading a file
        # await self.download_file(messages[0], 'path/to/save/file.txt')

        # # Example: Deleting a message
        # await self.delete_message(message_id=12)

        # # Example: Deleting all messages
        # await self.delete_all_messages()


    async def msg_edit_dlt(self,id:int,msg_id:int,_id_:int,key:str,delete:bool=False,edit:bool=False,new_value:str=None) -> None:
        table_content_ids:list = await self.extract_list_from_message(message_id=msg_id)
        if not table_content_ids:print("_id_ not found.");return
        elif not any(_id_ in ([item[0]] if isinstance(item, list) and len(item) > 1 else item if isinstance(item, list) else [item])for item in table_content_ids):print("_id_ not found.");return
        try:
            msg_data,msg_file =  await self.get_caption_and_save_file(message_id=_id_,table_id=id)
            msg_data:dict = ast.literal_eval(msg_data)
            if key in list(msg_data.keys()):
                if delete:
                    msg_data.pop(key)
                    if key =="file_attachments":
                        msg_data.pop('_id_')
                        await self.delete_message(message_id=_id_)
                        filtered_table_content_ids = [item for item in table_content_ids if not (isinstance(item, list) and _id_ in item or item == _id_)]
                        
                        await self.edit_message(message_id=msg_id,new_message_text=f"`table_id:{id}\n{filtered_table_content_ids}`")
                        return msg_data
                    
                if edit:msg_data[key] = new_value
                
                await self.edit_message(message_id=_id_,new_message_text=f"{msg_data}")
                return True
            else:print("Key not found.");return
        except:print("error msg_data = ",msg_data,type(msg_data))
    
    
    async def close_telegram_channel(self) -> None:
        await self.client.disconnect()
    
    

class user_db:
    """
    Initializes the user_db instance for the specified table ID.

    This method creates an instance of the user_db class and associates it with the provided table ID. It also
    checks for the existence of the corresponding table in the Telegram channel. If the table is not found,
    the method prompts the user to create it. If the user agrees, the table is created, and the message ID
    representing the table is set.

    Parameters
    ----------
    table_id : str
        The ID of the table to be managed.

    Examples
    --------
    Creating an instance of the user_db class for table ID '150':

    >>> table = user_db("150")
    """
    
    def __init__(self,table_id:str=None,api_id:str=None,api_hash:str=None,channel_id:int=None,phone_number:int=None,session_name:str=None):
        self.id = table_id
        self.tele_channel = TeleCloudChannel(api_id=api_id,api_hash=api_hash,channel_id=channel_id,phone_number=phone_number,session_name=session_name)
        self.msg_id:Optional[int] = None
        self.check = asyncio.get_event_loop()
        if self.id:
            self.check.run_until_complete(self._init_check_table())

    async def _init_check_table(self):
        result = await self.tele_channel.find_table(table_id=self.id)
        # print("result = ",result)
        if not result:
            print("Table not Found.")
            msg_id = await self.tele_channel.send_message(message=f"`table_id:{self.id}`\n[]")
            print("Table Created with id : ",self.id)
            self.msg_id = msg_id
            print("Table Created with id : ",self.id)
            await self._post_table_creation()
            
        else:
            self.msg_id = result[0]
            # print("self.msg_id = ",self.msg_id)
            
            
    async def _post_table_creation(self):
        # Handle any logic needed after table creation
        await self._init_check_table()

    def create_table(self,table_id:str) -> None:
        '''
        Create a new table.
        '''
        result = self.check.run_until_complete( self.tele_channel.find_table(table_id=table_id))
        if not result:
            self.check.run_until_complete(self.tele_channel.send_message(message=f"`table_id:{table_id}`\n[]"))
            print("Table Created with id : ",table_id)
            self.id = table_id
        
    def show_table(self,save_file:bool = False) -> list:
        """
        Retrieves and displays all documents in the table.

        This function extracts the list of document IDs from the specified message, retrieves the content 
        of each document, optionally saves any associated files, and returns a list of all documents.

        Parameters
        ----------
        save_file : bool, optional
            If True, saves the files associated with the documents. Default is False.

        Returns
        -------
        list
            A list of dictionaries representing the documents in the table.

        Examples
        --------
        >>> instance = YourClass()
        >>> documents = instance.show_table(save_file=True)
        >>> print(documents)
        [{'_id_': 1, 'name': 'Document1'}, {'_id_': 2, 'name': 'Document2'}]

        """
        table_content_ids:list = self.check.run_until_complete(self.tele_channel.extract_list_from_message(message_id=self.msg_id))
        datas = []
        # print("table_content_ids = ",table_content_ids)
        for ids in table_content_ids:
            if isinstance(ids,list):
                for i in ids:
                    msg_file:tuple = self.check.run_until_complete(self.tele_channel.get_caption_and_save_file(message_id=i,save_file=save_file,table_id=self.id))
                    if msg_file[0]:
                        datas.append(ast.literal_eval(msg_file[0]))
            else:
                data = self.check.run_until_complete(self.tele_channel.get_message_text(message_id=ids))        
                datas.append(ast.literal_eval(data))
        return datas
    def pop(self,_id_:int) -> bool|Exception:
        """
        Removes a document identified by _id_ from the table.

        This function deletes the specified document and updates the table content.
        If the document is successfully deleted, the function returns True.

        Parameters
        ----------
        _id_ : int
            The ID of the document to be removed.

        Returns
        -------
        bool or Exception
            Returns True if the operation is successful. Raises an Exception if the type of `_id_` is incorrect.

        Raises
        ------
        Exception
            If `_id_` is not of type int.

        Examples
        --------
        >>> instance = YourClass()
        >>> success = instance.pop(12345)
        >>> print(success)
        True

        """
        if type(_id_)==int:
            table_content_ids:list = self.check.run_until_complete(self.tele_channel.extract_list_from_message(message_id=self.msg_id))
            # print("table_content_ids = ",table_content_ids)
            # pop_msg= self.show_table()[index]
            if not table_content_ids:raise Exception("IndexError: pop from empty list")
            elif not any(_id_ in ([item[0]] if isinstance(item, list) and len(item) > 1 else item if isinstance(item, list) else [item])for item in table_content_ids):print("_id_ not found.");return False
            
            self.check.run_until_complete(self.tele_channel.delete_message(message_id=_id_))
            filtered_table_content_ids = [
            item for item in table_content_ids 
            if not (isinstance(item, list) and _id_ in item or item == _id_)
            ]
            self.check.run_until_complete(self.tele_channel.edit_message(message_id=self.msg_id,new_message_text=f"`table_id:{self.id}\n{filtered_table_content_ids}`"))
            return True
        else:raise Exception("key must be of type int.")

    def delete(self,_id_:int,key:str)->bool|Exception:
        """
        Deletes a specific key-value pair in the document identified by _id_.

        This function removes the specified key from the document. It ensures that the
        key is not '_id_', which is a reserved key. If the key is successfully deleted, 
        the modified document is appended to the table.

        Parameters
        ----------
        _id_ : int
            The ID of the document from which the key is to be deleted.
        key : str
            The key in the document to be deleted.

        Returns
        -------
        bool or Exception
            Returns True if the operation is successful. Raises an Exception if the key is '_id_' 
            or if the types of the parameters are incorrect.

        Raises
        ------
        Exception
            If `key` is '_id_', or if the types of `_id_` or `key` are incorrect.

        Examples
        --------
        >>> instance = YourClass()
        >>> success = instance.delete(12345, 'title')
        >>> print(success)
        True

        """
        if type(key)==str and type(_id_)==int:
            if key=='_id_':raise Exception("Key can't be _id_. _id_ is reserved key.")
            
            msg_get = self.check.run_until_complete(self.tele_channel.msg_edit_dlt(id=self.id,msg_id=self.msg_id,_id_=_id_,key=key,delete=True))
            print("msg_get = ",msg_get,type(msg_get))
            if type(msg_get) ==dict:
                self.append(data=msg_get)
            return True
        else:raise Exception("key must be of str.")
    
    def append(self,data:dict) -> bool|Exception:
        """
    Appends a new record to the table.

    This method appends a new record to the table stored in the Telegram channel. The record is expected
    to be a dictionary. If the record contains files, they will be uploaded and linked to the table. The method
    also assigns a unique ID (`_id_`) to each record.

    Parameters
    ----------
    data : dict
        The record to be appended to the table. If the record contains a key `_file`, it should be a dictionary
        with file paths or URLs as keys and their extensions as values. For example:
        {
            "name": "example",
            "_file": {
                "path/to/file1.txt": "txt",
                "http://example.com/image.jpg": "jpg"
            }
        }

    Returns
    -------
    bool
        Returns True if the record is successfully appended.

    Raises
    ------
    Exception
        If the `data` parameter is not of type dict.
        If the record contains a key `_id_`.

    Examples
    --------
    >>> db = user_db("150")
    >>> record = {"name": "example", "value": 123}
    >>> db.append(record)
    True

    >>> file_record = {
        "name": "example with files",
        "_file": {
            "path/to/file1.txt": "txt",
            "http://example.com/image.jpg": "jpg"
        }
    }
    >>> db.append(file_record)
    True

    >>> instance = YourClass()
    >>> data = {"name": "Alice", "age": 30}
    >>> instance.append(data)
    True

    >>> data_with_file = {"id":"1","name": "Alice", "age": 30,
    ...     "_file": {
    ...         "path/to/file.jpg": "jpg","file_url","jpg"
    ...     }
    ... }
    >>> instance.append(data_with_file)
    True

        """
        if type(data)==dict:
            if data.get("_id_"):raise Exception("Key can't be _id_. _id_ is reserved key.")
            table_content_ids:list = self.check.run_until_complete(self.tele_channel.extract_list_from_message(message_id=self.msg_id))
            # print("table_content = ",table_content_ids,type(table_content_ids))
            last_id = self.check.run_until_complete(self.tele_channel.get_messages(limit=1))
            last_id = last_id[0].id
            data["_id_"] = last_id+1
            if data.get("_file"):
                files = data["_file"]
                # print("files = ",files,type(files))
                data["file_attachments"] = len(list(data["_file"].keys()))

                data.pop('_file')
                reply_msg = self.check.run_until_complete(self.tele_channel.upload_files(files_with_extensions=files,caption=f'{data}',message_id=self.msg_id))
            else:reply_msg = self.check.run_until_complete( self.tele_channel.send_message_in_reply(message_id=self.msg_id,message=f'{data}'))
            # print("reply_msg = ",reply_msg)
            table_content_ids.append(reply_msg)
            # print("table_content = ",table_content_ids)
            
            self.check.run_until_complete( self.tele_channel.edit_message(message_id=self.msg_id,new_message_text=f"`table_id:{self.id}\n{table_content_ids}`"))
            return True
        else:raise Exception("data must be of type dict.")


    def edit(self,_id_:int,key:str,new_value:str) -> bool|Exception:
        """
        Edits a specific key-value pair in the document identified by _id_.

        This function updates the value of a specified key in the document. It ensures that the
        key is neither '_id_' nor 'file_attachments', which are reserved keys.

        Parameters
        ----------
        _id_ : int
            The ID of the document to be edited.
        key : str
            The key in the document whose value is to be updated.
        new_value : str
            The new value to be assigned to the key.

        Returns
        -------
        bool or Exception
            Returns True if the operation is successful. Raises an Exception if the key is '_id_' or 
            'file_attachments', or if the types of the parameters are incorrect.

        Raises
        ------
        Exception
            If `key` is '_id_' or 'file_attachments', or if the types of `_id_`, `key`, or `new_value` are incorrect.

        Examples
        --------
        >>> instance = YourClass()
        >>> success = instance.edit(12345, 'key', 'New value')
        >>> print(success)
        True

        """
        if type(key)==str and type(_id_)==int and type(new_value)==str:
            if key=='_id_' or key=='file_attachments':raise Exception("Key can't be _id_ or file_attachments. _id_ and file_attachments is reserved key.")

            self.check.run_until_complete(self.tele_channel.msg_edit_dlt(id=self.id,msg_id=self.msg_id,_id_=_id_,key=key,edit=True,new_value=new_value))
            return True
        else:raise Exception("key must be of type str and _id_ must be of type int and new_value must be of type str.")    
        
            
    def count(self) -> int:
        """
        Returns the number of items in the message extracted from the Telegram channel.

        This function retrieves a list of items from a specific message in the Telegram channel
        and returns the count of items in that list.

        Returns
        -------
        int
            The number of items in the message.

        Examples
        --------
        >>> instance = YourClass()
        >>> num_items = instance.count()
        >>> print(f"Number of items: {num_items}")
        5
        """
        return  len(self.check.run_until_complete(self.tele_channel.extract_list_from_message(message_id=self.msg_id)))
    

    def show_docs(self,_id_:list,save_file:bool=False) -> list|Exception:
        """
        Retrieves and optionally saves documents based on a list of document IDs.

        This function checks if the provided IDs are in the table content. For each valid ID,
        it fetches the document's caption and optionally saves the file associated with the document.
        The function returns a list of document data.

        Parameters
        ----------
        _id_ : list
            A list of document IDs to retrieve.
        save_file : bool, optional
            A flag to indicate whether to save the document files (default is False).

        Returns
        -------
        list or Exception
            A list of dictionaries containing document data if successful. Raises an Exception if 
            the input `_id_` is not of type list.

        Raises
        ------
        Exception
            If `_id_` is not of type list.

        Examples
        --------
        >>> instance = YourClass()
        >>> docs = instance.show_docs([12345, 67890])
        >>> print(docs)
        [{'key': 'value', 'key2': '...'}, {'key': 'value', 'key2': '...'}]

        >>> docs = instance.show_docs([12345, 67890], save_file=True)
        >>> print(docs) #it will save the file attachments if the document has them
        [{'key': 'value', 'key2': '...'}, {'key': 'value', 'key2': '...'}]

        """
        if type(_id_)==list:
            table_content_ids:list = self.check.run_until_complete(self.tele_channel.extract_list_from_message(message_id=self.msg_id))
            # print("table_content = ",table_content_ids,type(table_content_ids))
            show_msg= []
            for i in _id_:
                if not table_content_ids:print("Table Documents are empty.");return
                elif not any(i in ([item[0]] if isinstance(item, list) and len(item) > 1 else item if isinstance(item, list) else [item])for item in table_content_ids):print(f"_id_({i}) not found.");continue
                try:
                    msg_data,msg_file =  self.check.run_until_complete(self.tele_channel.get_caption_and_save_file(message_id=i,table_id=self.id,save_file=save_file))
                    msg_data:dict = ast.literal_eval(msg_data)
                    show_msg.append(msg_data) if msg_data else None
                except Exception as e:print(e)
            return show_msg
        else:raise Exception("key must be of type list.")

    def close(self) -> None:
        """
        Closes the connection to the Telegram channel.

        Returns
        -------
        None
            This function does not return anything.

        Examples
        --------
        >>> instance = YourClass()
        >>> instance.close()
        """
        self.check.run_until_complete(self.tele_channel.close_telegram_channel())

def table_list()->list:
    """
    Retrieves the list of tables from your database after authenticating the user.

    Returns
    -------
    list
        A list of tables retrieved from your Database.

    Examples
    --------
    >>> tables = table_list()
    
    """
    
    tele = TeleCloudChannel()
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(tele.table_list())
    
    # try:
    #     tele = TeleCloudChannel()
    #     loop = asyncio.get_event_loop()
    #     return loop.run_until_complete(tele.table_list())
    # except Exception as e:
        
    #     print("Database locked because you are using satabase somewhere. close user_db class and try again")



if __name__ == "__main__":
    st = time()
    tele = TeleCloudChannel()
    loop = asyncio.get_event_loop()
    # loop.run_until_complete(tele.edit_message(message_id=797,new_message_text='{"dfg":"dfgdf"}'))
    # loop.run_until_complete(tele.send_message("sdfhdf hii subh"))
    # a = loop.run_until_complete(tele.get_messages(limit=1))
    # print(a[0].id)
    # loop.run_until_complete(tele.delete_all_messages())
    print(loop.run_until_complete(tele.table_list()))
    # print(loop.run_until_complete(tele.get_caption_and_save_file(message_id=608,save_file=True)))
    # print(loop.run_until_complete(tele.upload_files(files_with_extensions={"https://cdn.discordapp.com/attachments/1231664483210891426/1247132867289681940/1.jpg?ex=665eea7e&is=665d98fe&hm=c9f4d70f45d824ff2c0869b34f0a9a1ae4090e14eace0f0e67a2bd81ee134d53&":'jpg',"https://images.unsplash.com/photo-1575936123452-b67c3203c357?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8aW1hZ2V8ZW58MHx8MHx8fDA%3D":'png'},caption="online")))
    # loop.run_until_complete(tele.upload_file(file="https://images.unsplash.com/photo-1575936123452-b67c3203c357?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8aW1hZ2V8ZW58MHx8MHx8fDA%3D",caption="online",file_extension='png'))
    # loop.run_until_complete(tele.create_poll("table_id:127",options=["None","Hii"]))
    # a = loop.run_until_complete(tele.get_replies_to_message(message_id=429))
    # a = loop.run_until_complete(tele.search_replies_to_original_message("table_id:127"))
    # a = loop.run_until_complete(tele.get_all_replies(message_id=429))
    # print(a)

    # while 1:
    #     x = input(">>> ")
    #     eval(x)

    print(f"Time taken: {time() - st} seconds")
    # pass



