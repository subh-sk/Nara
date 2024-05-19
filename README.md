<h1 align="center">
<img src="https://raw.githubusercontent.com/subh-sk/Nara/main/Logo/nara.png" width="300">
</h1><br>


# Nara

Nara is a comprehensive Python package designed to streamline various tasks such as creating temporary emails, generating random passwords, IDs, names, and more. It also includes features for caching to enhance response times, modifying JSON structures effortlessly, and integrating multiple AI models for real-time information retrieval and engaging chatbot interactions.


## Key Features

- **Temporary Email Creation**: Easily generate and manage temporary emails for testing and other purposes.
- **Random Data Generation**: Generate random passwords, IDs, names, and other data with customizable options.
- **Caching**: Implement caching mechanisms to store data temporarily and improve performance.
- **JSON Manipulation**: Simplify JSON data modification and handling with built-in utilities.
- **AI Integration**: Access and interact with multiple AI models for real-time information and human-like chatbot conversations.
- **AI Training**: Train and customize AI models to enhance their performance and adaptability.

Whether you are developing applications, automating tasks, or integrating AI-based solutions, Nara provides a robust and flexible toolkit to meet your needs.

## Installation

You can install the package using pip:

```bash
pip install nara
```

## Usage
Here is a simple example of how to use Nara:
```py
from nara.Extra import tempmail

    # Example usage for generating a temporary email
    OnlyMail(Printable=True) #only for generate email

    # Example usage for generating a temporary email and get verification link
    mail_OBJ = MailUrl(Timeout=20,Printable=True)
    print(next(mail_OBJ))
    input("wait = ")
    url = next(mail_OBJ)
    print(url)

    # Example usage for generating a temporary email and get verification Code
    mail_OBJ = MailOtp(OtpLength=6,Timeout=20,Printable=True)
    print(next(mail_OBJ))
    input("wait = ")
    url = next(mail_OBJ)
    print(url)
    



```


## Authors
> - Subhash Kumar
> - Divyansh Shukla
> - Yateesh Reddy

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing
Contributions are welcome! Please read the CONTRIBUTING.md file for details on how to contribute to this project.

## Contact
If you have any questions or suggestions, feel free to contact us at naravirtualai@gmail.com.

## Acknowledgements
Special thanks to all the contributors and users who have supported this project.
