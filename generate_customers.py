"""
Create customers.csv with 100 sample incoming customer inquiries.

Columns: id, customer_name, date, channel, message, category

category is one of: Feature request, Support/ticket, Pricing issue

Run it with:
    python generate_customers.py
"""

import csv
import random
from datetime import date, timedelta

# Fixed seed so the script produces the same file every time it runs
random.seed(7)

NUM_ROWS = 100
OUTPUT_FILE = "customers.csv"

CHANNELS = ["Email", "Phone", "Live chat", "Web form", "WhatsApp", "Facebook", "Twitter/X"]

FIRST_NAMES = [
    "Noa", "Yossi", "Maya", "Daniel", "Tamar", "Omer", "Shira", "Eitan", "Liat",
    "Amit", "Rachel", "David", "Sarah", "Michael", "Dana", "Ron", "Yael", "Avi",
    "Michal", "Itai", "Emma", "Liam", "Olivia", "Noah", "Hila", "Gal", "Nir",
]
LAST_NAMES = [
    "Cohen", "Levi", "Mizrahi", "Peretz", "Biton", "Friedman", "Azoulay", "Katz",
    "Shapiro", "Goldberg", "Ben-David", "Avraham", "Smith", "Johnson", "Brown",
    "Garcia", "Miller", "Rosen", "Dahan", "Halevi",
]

# Details that get dropped into the message templates
PRODUCTS = ["the mobile app", "the web dashboard", "the reports module", "the invoicing tool",
            "the team calendar", "the inventory screen", "the customer portal"]
FEATURES = ["dark mode", "export to Excel", "Hebrew right-to-left support", "Google Calendar sync",
            "two-factor login", "bulk delete", "custom fields", "a Slack integration",
            "offline mode", "scheduled reports", "keyboard shortcuts", "an open API"]
PLANS = ["Starter", "Pro", "Business", "Enterprise"]
DEVICES = ["iPhone 15", "Samsung Galaxy S24", "an old Windows 10 laptop", "a MacBook Air", "an iPad"]
TIMES = ["since this morning", "for three days now", "after your last update",
         "every Monday", "only on weekends", "since we added new users"]

# Message templates: different topics, lengths and tones.
# {placeholders} are filled with random details from the lists above.
TEMPLATES = [
    "Hi, could you add {feature}? Our whole team keeps asking for it.",
    "{product} crashes on my {device} {time}. Please fix it ASAP!!",
    "Why did my bill go up to {amount} this month? Nobody told us about a price change.",
    "Just wanted to say thank you - your support rep solved my issue in 5 minutes.",
    "I can't log in. The reset password email never arrives (checked spam too).",
    "We're a nonprofit with {seats} users. Do you offer a discount on the {plan} plan?",
    "Is there any way to get {feature}? We'd even pay extra for it.",
    "Order #{order} still hasn't been processed. It's been {days} days.",
    "{product} is so slow {time} that my employees gave up using it.",
    "How do I cancel my subscription? I can't find the button anywhere.",
    "You charged my card twice for the {plan} plan. I want a refund of {amount}.",
    "Suggestion: let us choose which columns appear in {product}.",
    "The numbers in {product} don't match what I see in my bank account.",
    "Can I move from {plan} to {plan2} in the middle of the month? How is it billed?",
    "Our accountant needs invoices in Hebrew. Is that possible?",
    "Love the product, but {feature} is the one thing stopping us from switching fully.",
    "I accidentally deleted a client record. Is there any way to restore it?",
    "Your competitor offers {feature} for free. Why should we stay with you?",
    "The new design of {product} is confusing - where did the search bar go?",
    "We'd like to add {seats} more users. Is there volume pricing?",
    "Got an 'Error 500' when uploading a file bigger than {size} MB.",
    "Please call me back regarding ticket #{ticket}, nobody has answered for {days} days.",
    "Can you add a way to tag customers by city? Would help our sales team a lot.",
    "Notifications from {product} arrive twice {time}. Very annoying.",
    "Is my data stored in Israel or abroad? Our legal team is asking.",
    "Annual plan vs monthly - how much do we actually save on {plan}?",
    "The app logs me out every few minutes on my {device}.",
    "Can we get a demo of the {plan} plan for our managers next week?",
    "Your trial ended but I never got a chance to try {feature}. Can you extend it?",
    "I was promised a {percent}% discount by your sales rep but it's not on my invoice.",
    "Printing from {product} cuts off the last column of every page.",
    "Would love {feature} - right now I copy everything by hand.",
    "Hello?? I've been waiting on hold for 40 minutes.",
    "How do I give my assistant view-only access without paying for another seat?",
    "After the update I can't see last year's data in {product}.",
    "Is there a student or startup price? {plan} is out of our budget.",
]

# Optional openings and sign-offs, to vary the tone even more
OPENINGS = ["", "", "", "Hello, ", "Good morning. ", "Hey team, ", "Urgent: ", "Quick question - "]
CLOSINGS = ["", "", "", " Thanks.", " Thanks in advance!", " Regards.", " Waiting for your reply.", " :("]


def random_name():
    """Return a random 'First Last' customer name."""
    return f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"


def random_date():
    """Return a random date in the last 90 days before 2026-10-22, as YYYY-MM-DD."""
    end = date(2026, 10, 22)
    return (end - timedelta(days=random.randint(0, 89))).isoformat()


def random_message():
    """Build one message: pick a template, fill in details, add an opening/closing."""
    plan, plan2 = random.sample(PLANS, 2)
    body = random.choice(TEMPLATES).format(
        feature=random.choice(FEATURES),
        product=random.choice(PRODUCTS),
        device=random.choice(DEVICES),
        time=random.choice(TIMES),
        plan=plan,
        plan2=plan2,
        amount=f"{random.randint(49, 990)} ILS",
        seats=random.randint(3, 250),
        order=random.randint(10000, 99999),
        ticket=random.randint(1000, 9999),
        days=random.randint(2, 14),
        size=random.choice([10, 25, 50, 100]),
        percent=random.choice([10, 15, 20, 25]),
    )
    opening = random.choice(OPENINGS)
    # After "Hello, " or "Quick question - " the sentence continues, so lowercase
    # its first letter ("Hello, could you..."). Keep "I" capitalized.
    if opening.endswith((", ", "- ")) and not body.startswith("I "):
        body = body[0].lower() + body[1:]
    message = opening + body + random.choice(CLOSINGS)
    return message[0].upper() + message[1:]


# Keywords used to classify a message. Pricing is checked first, then feature
# requests; anything that matches neither is treated as a support ticket.
PRICING_KEYWORDS = ["bill", "charged", "price", "pricing", "discount", "refund", "plan",
                    "budget", "paying for", "trial", "save on"]
FEATURE_KEYWORDS = ["could you add", "can you add", "add a way", "suggestion", "would love",
                    "any way to get", "one thing stopping", "offers", "is that possible",
                    "let us choose"]


def classify(message):
    """Return the message's category: Pricing issue, Feature request or Support/ticket."""
    text = message.lower()
    if any(word in text for word in PRICING_KEYWORDS):
        return "Pricing issue"
    if any(word in text for word in FEATURE_KEYWORDS):
        return "Feature request"
    return "Support/ticket"


def classify_with_ai(message):
    """
    Alternative to classify(): ask Claude which category a message belongs to.

    NOT USED YET - main() still calls classify(). To switch, replace
    classify(row["message"]) with classify_with_ai(row["message"]) in main().

    Before using it you need:
      1. pip install anthropic
      2. An API key from console.anthropic.com (separate from a Pro/Max
         subscription), saved in the ANTHROPIC_API_KEY environment variable.
         Never write the key in this file.
    """
    # Imported here, not at the top of the file, so the script still runs
    # for people who haven't installed these packages.
    from typing import Literal

    import anthropic
    from pydantic import BaseModel

    # The answer must be exactly one of these three strings
    class Classification(BaseModel):
        category: Literal["Feature request", "Support/ticket", "Pricing issue"]

    client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY automatically
    response = client.messages.parse(
        model="claude-opus-5-5",  # "claude-haiku-5-5" is much cheaper and likely good enough
        max_tokens=1024,
        system="You classify customer inquiries for a software company.",
        messages=[{"role": "user", "content": f"Classify this customer message:\n\n{message}"}],
        output_format=Classification,
    )
    return response.parsed_output.category


def main():
    # Build 100 messages, retrying until every message is different
    messages = []
    while len(messages) < NUM_ROWS:
        msg = random_message()
        if msg not in messages:
            messages.append(msg)

    # Create the rows and sort them by date, oldest first
    rows = [
        {"customer_name": random_name(), "date": random_date(),
         "channel": random.choice(CHANNELS), "message": msg}
        for msg in messages
    ]
    rows.sort(key=lambda row: row["date"])

    # Write the CSV. utf-8-sig helps Excel open it with the right encoding.
    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "customer_name", "date", "channel", "message", "category"])
        for i, row in enumerate(rows, start=1):
            writer.writerow([i, row["customer_name"], row["date"], row["channel"], row["message"],
                             classify(row["message"])])

    print(f"Created {OUTPUT_FILE} with {len(rows)} customer inquiries.")


if __name__ == "__main__":
    main()
