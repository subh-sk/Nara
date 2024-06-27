import time
from mailtm import Email
from time import sleep
import re
from rich import print
from nara.extra.TempMail.retry import retry
from rich.console import Console
from rich.table import Table
from rich.markdown import Markdown
import requests
import random
console = Console()

import time
import sys

def print_with_overwrite(message):
    sys.stdout.write("\r" + " " * 50)  # Clear the entire line
    sys.stdout.write(f"\r" + message)
    sys.stdout.flush()

def dynamic_waiting(duration=1,message="waiting",done_text = "Done",check=True,steps:int=None):
    end_time = time.time() + duration
    
    states = [f'{message}.', f'{message}..', f'{message}...']
    state_index = 0
    if steps: states = [states[steps%3]]

    while time.time() < end_time:
        # Print the current state and flush the output buffer
        print_with_overwrite(states[state_index])
        
        # Move to the next state
        state_index = (state_index + 1) % len(states)
        
        # Wait for 1 second
        time.sleep(1)

    # Print "done" when the waiting period is over
    if check:print_with_overwrite(done_text)
class tempmailio:
    def __init__(self,email_name:str=None,domain:str=None,timeout:int=30,Printable=False) -> None:
        self.email_name = email_name
        self.domain = domain
        
        self.timeout = timeout
        self.Printable = Printable
        
    def cheeck_domain(self) -> None:
        domains = requests.get("https://api.internal.temp-mail.io/api/v4/domains")
        # Create a table
        table = Table(title="Available Domain Information")

        # Define the columns
        table.add_column("Name", justify="left", style="cyan", no_wrap=True)
        table.add_column("Type", justify="left", style="magenta")
        table.add_column("Forward Available", justify="left", style="green")
        table.add_column("Forward Max Seconds", justify="right", style="yellow")
        domains = domains.json().get('domains')
        # Add rows to the table
        for domain in domains:
            table.add_row(
                domain['name'],
                domain['type'],
                str(domain['forward_available']),
                str(domain['forward_max_seconds'])
            )

        # Print the table to the console
        console.print(table)

    def mailioUrl(self) ->list[str]: # type: ignore
        '''
        Generates a new email address and fetches URLs from incoming emails.

        This function generates a new email address using the `Email` class, registers it, 
        and yields the email address. On subsequent iterations, it fetches URLs from the 
        email messages.

        Parameters
        ----------
        Printable : bool, optional
            If set to True, the generated email address and email contents will be printed 
            to the console. Default is False.
        Timeout : int, optional
            The maximum number of iterations to fetch URLs. Default is 30.

        Yields
        ------
        str
            The generated email address (on the first iteration).
        list
            A list of URLs found in the email messages (on subsequent iterations).

        Raises
        ------
        Exception
            If no URLs are found within the specified timeout period.

        Examples
        --------
        >>> generator = mailioUrl(Printable=False, Timeout=30)
        >>> email_address = next(generator)
        >>> print(email_address)
        example@example.com
        >>> url_list = next(generator)
        >>> print(url_list)
        ['https://example.com', 'http://example.org']
        '''

        try:

            # https://api.internal.temp-mail.io/api/v4/domains
            # https://api.internal.temp-mail.io/api/v3/email/am1ypljq9a@rfcdrive.com/messages


            # https://api.internal.temp-mail.io/api/v3/email/new = post :paylod = {name: "wem2cd5cat", domain: "rfcdrive.com"}
            if self.email_name == None and self.domain == None:  payload = {"min_name_length":10,"max_name_length":10}
            elif self.domain == None and self.email_name : payload = {"name": self.email_name,"max_name_length":10}
            elif self.domain  and self.email_name== None : payload = {"min_name_length":10,"domain":self.domain}
            elif self.domain and self.email_name : payload = {"name": self.email_name,"domain":self.domain}

            url = "https://api.internal.temp-mail.io/api/v3/email/new"
            headers = {"Content-Type": "application/json"}

            response = requests.post(url, json=payload, headers=headers)
            # print(response.status_code)
            if response.status_code != 200: raise Exception(f"Failed to generate email address: {response.status_code} {response.text}")
            mail =response.json().get("email") 

            if self.Printable:console.print(f"[#0b7ce6]\nEmail Adress: [/#0b7ce6] [#0be654]{mail}[/#0be654]")
        
            yield mail
            # print(get_content.json())
            for _ in range(self.timeout):
                messages =requests.get(f"https://api.internal.temp-mail.io/api/v3/email/{mail}/messages")
                message = messages.json()
                if message:
                    message:dict = message[0]
                    if self.Printable:
                        # Create a table
                        table = Table(title="Email Information")

                        # Define the columns
                        table.add_column("Field", justify="left", style="cyan", no_wrap=True)
                        table.add_column("Value", justify="left", style="magenta")

                        # Add rows to the table
                        for key, value in message.items():
                            table.add_row(key, str(value))

                        # Print the table to the console
                        console.print(table)

                    # content = message['html'][0]
                    content="\nSubject: " + message.get('subject')+"\nContent: " + message['body_html']
                    url_pattern = r'https?://[^\s">]+'
                    links = re.findall(url_pattern, content)
                    if self.Printable:print(f"[#0b7ce6]\nLinks: [/#0b7ce6]{links}")
                    dynamic_waiting(done_text="Links found\n",duration=1,check=True)
                    yield links
                    break
                else:dynamic_waiting(duration=1,check=False,steps=_+1)
                if _ == self.timeout - 1:
                    raise Exception("[#fa6c61]\nTimeout: No Links found till " + str(self.timeout) + " seconds.")
        except Exception as e:print(f"[#fa6c61]{e}[/#fa6c61]"); yield []


    def mailioOtp(self,OtpLength=6)->list[int]: # type: ignore
        '''
        Generates a new email address and fetches OTPs from incoming email.

        This function generates a new email address using the `Email` class, registers it, 
        and yields the email address. On subsequent iterations, it fetches OTPs (One-Time 
        Passwords) from the email messages. The OTPs are identified based on the specified 
        length.

        Parameters
        ----------
        otp_length : int, optional
            The length of the OTP to be fetched. Default is 6.
        Printable : bool, optional
            If set to True, the generated email address and email contents will be printed 
            to the console. Default is False.
        timeout : int, optional
            The maximum number of iterations to fetch OTPs. Default is 30.

        Yields
        ------
        str
            The generated email address (on the first iteration).
        list
            A list of OTPs found in the email messages (on subsequent iterations).

        Examples
        --------
        >>> generator = Mail_otp(otp_length=6, Printable=False)
        >>> email_address = next(generator)
        >>> print(email_address)
        example@example.com
        >>> otp_list = next(generator)
        >>> print(otp_list)
        ['789012']
        
        '''

        try:
            if self.email_name == None and self.domain == None:  payload = {"min_name_length":10,"max_name_length":10}
            elif self.domain == None and self.email_name : payload = {"name": self.email_name,"max_name_length":10}
            elif self.domain and self.email_name== None : payload = {"min_name_length":10,"domain":self.domain}
            elif self.domain and self.email_name : payload = {"name": self.email_name,"domain":self.domain}

            url = "https://api.internal.temp-mail.io/api/v3/email/new"
            headers = {"Content-Type": "application/json"}

            response = requests.post(url, json=payload, headers=headers)
            # print(response.status_code)
            if response.status_code != 200: raise Exception(f"Failed to generate email address: {response.status_code} {response.text}")
            mail =response.json().get("email") 

            if self.Printable:console.print(f"[#0b7ce6]\nEmail Adress: [/#0b7ce6] [#0be654]{mail}[/#0be654]")
        
            yield mail
            for _ in range(self.timeout):
                messages =requests.get(f"https://api.internal.temp-mail.io/api/v3/email/{mail}/messages")
                message = messages.json()
                if message:
                    message:dict = message[0]
                    if self.Printable:
                        # Create a table
                        table = Table(title="Email Information")

                        # Define the columns
                        table.add_column("Field", justify="left", style="cyan", no_wrap=True)
                        table.add_column("Value", justify="left", style="magenta")

                        # Add rows to the table
                        for key, value in message.items():
                            table.add_row(key, str(value))

                        # Print the table to the console
                        console.print(table)

                    # content = message['html'][0]
                    content="\nSubject: " + message.get('subject')+"\nContent: " + message['body_html']
                    otp_pattern = r'\b\d{' + str(OtpLength) + r'}\b'
                    otp = re.findall(otp_pattern, content[0])
                    if self.Printable:print(f"[#0b7ce6]\OTP: [/#0b7ce6]{otp}")
                    dynamic_waiting(done_text="OTP found\n",duration=1,check=True)
                    yield otp
                    break
                else:dynamic_waiting(duration=1,check=False,steps=_+1)
                if _ == self.timeout - 1:
                    raise Exception("[#fa6c61]\nTimeout: No Links found till " + str(self.timeout) + " seconds.")
        except Exception as e:print(f"[#fa6c61]{e}[/#fa6c61]"); yield []


if __name__ == "__main__":
    t = tempmailio(Printable=True)
    a = t.mailioUrl()
    print(next(a))
    print(next(a))