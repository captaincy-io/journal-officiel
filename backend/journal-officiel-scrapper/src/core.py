import random
from datetime import datetime


def generate_random_browser_headers():
    """
    Generates random browser headers to simulate different user agents and accept languages.

    The function randomly selects a User-Agent string and an Accept-Language string from predefined lists,
    and returns a dictionary containing these headers along with other common HTTP headers.

    Returns:
        dict: A dictionary containing the following HTTP headers:
            - User-Agent: A randomly selected User-Agent string from a predefined list.
            - Accept-Language: A randomly selected Accept-Language string from a predefined list.
            - Accept: A constant string representing accepted content types.
            - Connection: A constant string indicating the connection type.
            - Upgrade-Insecure-Requests: A constant string indicating the preference for secure requests.

    Example:
        >>> headers = generate_random_browser_headers()
        >>> print(headers)
        {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
    """

    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0",
        "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; AS; rv:11.0) like Gecko",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
        "Mozilla/5.0 (Linux; Android 11; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Mobile Safari/537.36"
    ]

    accept_languages = [
        "en-US,en;q=0.9",
        "en-GB,en;q=0.8,fr;q=0.6",
        "fr-FR,fr;q=0.9,en;q=0.8",
        "de-DE,de;q=0.9,en;q=0.8",
        "es-ES,es;q=0.9,en;q=0.8"
    ]

    return {
        "User-Agent": random.choice(user_agents),
        "Accept-Language": random.choice(accept_languages),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1"
    }


def sanitize_date(date_str, date_format="%Y/%m/%d"):
    """
    Sanitizes a date string by attempting to parse it into a datetime object using the specified format.

    The function tries to parse the provided date string according to the given date format. If parsing is
    successful, it returns a datetime object. If the date string is invalid and cannot be parsed, the function
    prints an error message and returns None.

    Args:
        date_str (str): The date string to be sanitized.
        date_format (str): The format in which the date string is expected (default is "%Y/%m/%d").

    Returns:
        datetime or None: A datetime object if parsing is successful, or None if the date string is invalid.

    Example:
        >>> valid_date = sanitize_date("2024/07/29")
        >>> print(valid_date)
        2024-07-29 00:00:00

        >>> invalid_date = sanitize_date("29/07/2024", "%d/%m/%Y")
        >>> print(invalid_date)
        2024-07-29 00:00:00

        >>> invalid_date = sanitize_date("07/29/2024")
        Invalid date format
        >>> print(invalid_date)
        None
    """

    try:
        # Attempt to parse the date
        return datetime.strptime(date_str, date_format)
    except ValueError:
        print("Invalid date format")
        return None
