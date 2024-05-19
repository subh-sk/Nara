import time
from mailtm import Email
from time import sleep
import re
from rich import print
from Nara.Extra.TempMail.retry import retry
from rich.console import Console


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


def MailUrl(Printable=False,Timeout=30) ->str: # type: ignore
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
    >>> generator = MailUrl(Printable=False, Timeout=30)
    >>> email_address = next(generator)
    >>> print(email_address)
    example@example.com
    >>> url_list = next(generator)
    >>> print(url_list)
    ['https://example.com', 'http://example.org']
    '''

    try:
        test = Email()
        test.register()

        if Printable:print(f"[#0b7ce6]\nEmail Adress: [/#0b7ce6] [#0be654]{str(test.address)}[/#0be654]")
    
        yield test.address
        for _ in range(Timeout):
            for message in test.message_list():
                test.message_ids.append(message['id'])
                message = test.message(message['id'])

                # if Printable:
                #     print(f"[#0b7ce6]\nSubject: [/#0b7ce6]{message['subject']}")
                #     print(f"[#0b7ce6]Content:  [/#0b7ce6]{message['html'][0]}")

                # content = message['html'][0]
                content="\nSubject: " + message['subject']+"\nContent: " + message['text'] if message['text'] else message['html'][0]
                url_pattern = r'https?://\S+'
                links = re.findall(url_pattern, content)
                if Printable:print(f"[#0b7ce6]\nLinks: [/#0b7ce6]{links}")
                yield links
            if len(test.message_list()) == 0:
                dynamic_waiting(duration=1,check=False,steps=_+1)
            else:dynamic_waiting(done_text="[green]Links found[/green]",duration=1,check=True)
            if _ == Timeout - 1:
                raise Exception("[#fa6c61]\nTimeout: No Links found till " + str(Timeout) + " seconds.")
    except Exception as e:print(f"[#fa6c61]{e}[/#fa6c61]"); yield []

@retry(retries=5, delay=1)
def OnlyMail(Printable:bool=False) ->str:
    '''
    Generates a new email address and optionally prints it.

    This function generate a new email address and returns the email address as a string. If an error
    occurs during this process, the function recursively calls itself
    until it succeeds.

    Parameters:
    Printable (bool): If set to True, the generated email address will be
                       printed to the console. Default is False.

    Returns:
    str: The generated email address.

    Example:
    >>> email_address = OnlyMail()
    >>> print(email_address)
    edxrkmqdbh1btci3xjgnnxbd@fthcapital.com
    '''
    try:
        test = Email()
        test.register()
        if Printable:print(f"[#0b7ce6]\nEmail Adress: [/#0b7ce6] [#0be654]{str(test.address)}[/#0be654]") 
        return test.address
    except: raise Exception("Failed to generate email address.")


def MailOtp(OtpLength=6,Printable=False,Timeout=30)->int: # type: ignore
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
        test = Email()
        test.register()

        if Printable:print(f"[#0b7ce6]\nEmail Adress: [/#0b7ce6] [#0be654]{str(test.address)}[/#0be654]")
    
        yield test.address
        for _ in range(Timeout):
            for message in test.message_list():
                test.message_ids.append(message['id'])
                message = test.message(message['id'])

                if Printable:
                    print(f"[#0b7ce6]\nSubject: [/#0b7ce6]{message['subject']}")
                    print(f"[#0b7ce6]Content:  [/#0b7ce6]{message['html']}")

                content = message['html']
                otp_pattern = r'\b\d{' + str(OtpLength) + r'}\b'
                otp = re.findall(otp_pattern, content[0])
                yield otp
            if len(test.message_list()) == 0:
                dynamic_waiting(duration=1,check=False,steps=_+1)
            else:dynamic_waiting(done_text="[green]OTP found[/green]",duration=1,check=True)
            if _ == Timeout - 1:
                raise Exception("[#fa6c61]\nTimeout: No OTP found till " + str(Timeout) + " seconds.")
    except Exception as e:print(f"[#fa6c61]{e}[/#fa6c61]"); yield []

if __name__ == "__main__":
    # OnlyMail(Printable=True)
    mail_OBJ = MailUrl(Timeout=20,Printable=True)
    print(next(mail_OBJ))
    input("wait = ")
    url = next(mail_OBJ)
    print(url)