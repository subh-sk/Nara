import random
import string
from faker import Faker
from datetime import datetime, timedelta

class RandomDataGenerator:
    """
    A class to generate random data such as names, addresses, usernames, passwords, dates of birth, etc.

    Attributes:
        fake (Faker): A Faker instance for generating various types of fake data.
        fake_indian (Faker): A Faker instance for generating Indian-specific fake data.
        fake_foreign (Faker): A Faker instance for generating foreign-specific fake data.
    """

    def __init__(self):
        """
        Initializes the RandomDataGenerator class.

        Creates instances of Faker for generating various types of fake data.
        """
        self.fake = Faker()
        self.fake_indian = Faker('en_IN')
        self.fake_foreign = Faker(['en_US', 'fr_FR', 'de_DE', 'es_ES', 'it_IT'])

    def name(self) -> str:
        """
        Generates a random full name.

        Returns:
            str: A random full name.
        """
        return self.fake.name().strip()

    def firstName(self) -> str:
        """
        Generates a random first name.

        Returns:
            str: A random first name.
        """
        return self.fake.first_name().strip()

    def lastName(self) -> str:
        """
        Generates a random last name.

        Returns:
            str: A random last name.
        """
        return self.fake.last_name().strip()

    def indianName(self) -> str:
        """
        Generates a random Indian full name.

        Returns:
            str: A random Indian full name.
        """
        return self.fake_indian.name().strip()

    def foreignName(self) -> str:
        """
        Generates a random foreign full name.

        Returns:
            str: A random foreign full name.
        """
        return self.fake_foreign.name().strip()

    def location(self) -> str:
        """
        Generates a random location.

        Returns:
            str: A random location.
        """
        return self.fake.location_on_land()

    def address(self) -> str:
        """
        Generates a random address.

        Returns:
            str: A random address.
        """
        return self.fake.address().replace("\n", ", ")

    def indianAddress(self) -> str:
        """
        Generates a random Indian address.

        Returns:
            str: A random Indian address.
        """
        return self.fake_indian.address().replace("\n", ", ")

    def foreignAddress(self) -> str:
        """
        Generates a random foreign address.

        Returns:
            str: A random foreign address.
        """
        return self.fake_foreign.address().replace("\n", ", ")

    def pinCode(self) -> str:
        """
        Generates a random pincode.

        Returns:
            str: A random pincode.
        """
        return self.fake.postcode()

    def dob(self, start_age: int = 18, end_age: int = 90) -> str:
        """
        Generates a random date of birth.

        Args:
            start_age (int, optional): Minimum age for generated date of birth in years. Defaults to 18.
            end_age (int, optional): Maximum age for generated date of birth in years. Defaults to 90.

        Returns:
            str: A random date of birth in 'YYYY-MM-DD' format.
        """
        start_date = datetime.now() - timedelta(days=end_age*365)
        end_date = datetime.now() - timedelta(days=start_age*365)
        dob = self.fake.date_between(start_date=start_date, end_date=end_date)
        return dob.strftime("%Y-%m-%d")

    def id(self, name: str = None) -> str:
        """
        Generates an ID based on a given name or a random name if none provided.

        Args:
            name (str, optional): Name to generate ID from. Defaults to None.

        Returns:
            str: Generated ID.
        """
        if not name:
            name = self.name()
        id = name.replace(" ", "").replace(".", "")
        random_number = random.randint(0, 9999)
        id += str(random_number)
        return id

    def username(self, name: str = None) -> str:
        """
        Generates a username based on a given name or a random name if none provided.

        Args:
            name (str, optional): Name to generate username from. Defaults to None.

        Returns:
            str: Generated username.
        """
        if not name:
            name = self.name()
        username = name.lower().replace(" ", "").replace(".", "")
        random_number = random.randint(0, 9999)
        username += str(random_number)
        return username

    def randomString(self, length: int = 10) -> str:
        """
        Generates a random string of specified length.

        Args:
            length (int, optional): Length of the random string. Defaults to 10.

        Returns:
            str: Generated random string.
        """
        letters = string.ascii_letters + string.digits
        return ''.join(random.choice(letters) for i in range(length))

    def password(self, length: int = 12, special_count: int = 2, digit_count: int = 2) -> str:
        """
        Generates a random password with specified constraints.

        Args:
            length (int, optional): Length of the password. Defaults to 12.
            special_count (int, optional): Number of special symbols in the password. Defaults to 2.
            digit_count (int, optional): Number of digits in the password. Defaults to 2.

        Returns:
            str: Generated password.
        
        Raises:
            ValueError: If the password length is too short for the given constraints.
        """
        if length < (special_count + digit_count + 2):
            raise ValueError("Password length is too short for the given constraints")

        uppercase_letters = string.ascii_uppercase
        lowercase_letters = string.ascii_lowercase
        digits = string.digits
        special_symbols = "!@#$%^&*()_+=-[]{}|:;,.<>?"

        password = (
            random.choice(uppercase_letters) +
            random.choice(lowercase_letters)
        )
        
        password += ''.join(random.choice(special_symbols) for _ in range(special_count))
        password += ''.join(random.choice(digits) for _ in range(digit_count))

        remaining_length = length - len(password)
        all_characters = uppercase_letters + lowercase_letters + digits + special_symbols
        password += ''.join(random.choice(all_characters) for _ in range(remaining_length))

        password_list = list(password)
        random.shuffle(password_list)

        return ''.join(password_list)

# Example usage
if __name__ == "__main__":

    generator = RandomDataGenerator()

    