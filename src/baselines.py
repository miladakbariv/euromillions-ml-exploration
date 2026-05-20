import random


def random_ticket() -> dict:
    """
    Generate a completely random EuroMillions ticket.

    Main numbers:
        5 unique numbers from 1 to 50

    Lucky Stars:
        2 unique numbers from 1 to 12
    """
    main_numbers = sorted(random.sample(range(1, 51), 5))
    lucky_stars = sorted(random.sample(range(1, 13), 2))

    return {
        "main_numbers": main_numbers,
        "lucky_stars": lucky_stars,
        "method": "random",
    }


def generate_multiple_random_tickets(number_of_tickets: int = 5) -> list[dict]:
    """
    Generate multiple random EuroMillions tickets.
    """
    tickets = []

    for _ in range(number_of_tickets):
        ticket = random_ticket()
        tickets.append(ticket)

    return tickets