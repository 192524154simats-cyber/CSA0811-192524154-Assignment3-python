
"""
Merging phone contacts (designed from the requirements).

Contact (input): dict with optional name, numbers and emails.
Person (output): dict containing names, numbers and emails as sets.

Two contacts are the same person if they share:
1. At least one normalised phone number.
2. An email address, only when neither contact has a valid phone number.

Names are collected for display and are never used as matching keys.
"""

import string

TITLES = {"dr", "mr", "mrs", "ms", "prof", "shri", "smt", "sri"}


def normalise_number(raw):
    """Convert a phone number into a valid 10-digit Indian mobile number."""
    digits = "".join(ch for ch in str(raw) if ch.isdigit())

    if len(digits) == 12 and digits.startswith("91"):
        digits = digits[2:]
    elif len(digits) == 11 and digits.startswith("0"):
        digits = digits[1:]

    return digits if len(digits) == 10 else None


def normalise_email(raw):
    """Convert email addresses to lowercase and remove surrounding spaces."""
    email = str(raw).strip().lower()

    if "@" in email and not email.startswith("@") and not email.endswith("@"):
        return email

    return None


def normalise_name(raw):
    """Remove titles and punctuation and capitalise name words."""
    cleaned = str(raw).translate(
        str.maketrans("", "", string.punctuation.replace("'", ""))
    ).lower().split()

    words = [word for word in cleaned if word not in TITLES]

    return " ".join(word.capitalize() for word in words)


def merge(contacts):
    """
    Merge matching contacts into people.

    Uses a dictionary for fast average O(n) matching.
    Returns a list of person dictionaries.
    """

    people = {}
    key_to_person = {}
    next_id = 0

    for contact in contacts:
        numbers = {
            number
            for number in (
                normalise_number(value)
                for value in contact.get("numbers", [])
            )
            if number
        }

        emails = {
            email
            for email in (
                normalise_email(value)
                for value in contact.get("emails", [])
            )
            if email
        }

        name = normalise_name(contact.get("name", ""))

        # Contacts with valid numbers are matched by number only.
        # Email is used for matching only when there is no valid number.
        keys = numbers if numbers else emails

        # No valid matching information: keep as a separate person.
        if not keys:
            people[next_id] = {
                "names": {name} if name else set(),
                "numbers": numbers,
                "emails": emails
            }
            next_id += 1
            continue

        owners = {
            key_to_person[key]
            for key in keys
            if key in key_to_person
        }

        if not owners:
            person_id = next_id
            next_id += 1

            people[person_id] = {
                "names": set(),
                "numbers": set(),
                "emails": set()
            }

        else:
            person_id = min(owners)

            # Merge previously separate people when necessary.
            for other_id in owners - {person_id}:
                absorbed = people.pop(other_id)

                people[person_id]["names"].update(absorbed["names"])
                people[person_id]["numbers"].update(absorbed["numbers"])
                people[person_id]["emails"].update(absorbed["emails"])

                # Redirect old matching keys to the surviving person.
                for key, owner in list(key_to_person.items()):
                    if owner == other_id:
                        key_to_person[key] = person_id

        person = people[person_id]

        if name:
            person["names"].add(name)

        person["numbers"].update(numbers)
        person["emails"].update(emails)

        # Store only the actual matching keys.
        for key in keys:
            key_to_person[key] = person_id

    return list(people.values())


def display_name(person):
    """Return the longest available normalised name."""
    return (
        max(person["names"], key=lambda name: (len(name), name))
        if person["names"]
        else "(no name)"
    )


def merge_pairwise(contacts):
    """
    ALTERNATIVE (Alternative Concept):

    Compare every pair of contacts.
    Union-Find is used to join matching contacts.

    Returns the groups and number of pair comparisons.
    """

    n = len(contacts)
    keys = []

    for contact in contacts:
        numbers = {
            value
            for value in (
                normalise_number(item)
                for item in contact.get("numbers", [])
            )
            if value
        }

        emails = {
            value
            for value in (
                normalise_email(item)
                for item in contact.get("emails", [])
            )
            if value
        }

        keys.append(numbers if numbers else emails)

    parent = list(range(n))

    def find(index):
        while parent[index] != index:
            parent[index] = parent[parent[index]]
            index = parent[index]

        return index

    comparisons = 0

    for i in range(n):
        for j in range(i + 1, n):
            comparisons += 1

            if keys[i] & keys[j]:
                parent[find(i)] = find(j)

    groups = {}

    for i in range(n):
        groups.setdefault(find(i), []).append(i)

    return groups, comparisons
