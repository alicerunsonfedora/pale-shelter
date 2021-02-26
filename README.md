# No Love (Codename "Pale Shelter")

You've tried to get into a relationship many, many times; each time is an additional failure to add to your list. You're now over it and want to move on. It can't hurt to keep trying, right?

No Love is a game written in Python about relationships for the Wowie! Jam 3.0, where to give up on relationships is to win, and to succeed in getting one is a failure. Can you drain yourself and give yourself pale shelter, or will you fail?

## Planning

- Fail to start a relationship (stay single for as long as you can)
    - Game ends when you "die" (no love left)
        - Win if you run out of love
        - Lose if you end up in a relationship
- Gain points by staying alive long enough at the cost of your love being drained
- _Drain the love meter_
- Power-ups:
    - "Heart" power-up adds love to the love meter
    - "Money" power-up drains meter faster

## Building from source

### Requirements

- Python 3.9 or greater
- Pipenv

Clone the repository and then run `pipenv install` to install the dependencies for the game. You can then run `pipenv run game` to run the game as-is or run `pipenv run build` to build a copy of the game for your platform.

## Licensing

The source code for this game is licensed under the Mozilla Public License v2.0. Assets in this game are licensed under their respective licenses and can be reviewed accordingly.