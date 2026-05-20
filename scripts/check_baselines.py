from src.baselines import random_ticket, generate_multiple_random_tickets


print("One random ticket:")
print(random_ticket())

print("\nFive random tickets:")
tickets = generate_multiple_random_tickets(number_of_tickets=5)

for ticket in tickets:
    print(ticket)