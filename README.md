# Pokémon Pickup Bot

This is a bot I am developing to automate the process of farming items obtained via pickup in Pokémon games via Citra, a 3ds emulator. Pickup is an ability where after a battle a Pokémon has a chance of picking up an item, and this bot serves to battle, check for items and recharge moves constantly, allowing the bot to run ad infinitum. Users will be able to customize the routing to the poke center, the patch of wild grass which has Pokémon, and even choose which slots contain the pickup Pokémon. 



## Getting Started

For now, all you need is the QTGui.py file, as that contains everything pertinent to running the bot. I will describe each button as well as how to most effectively use it:

1. **Run Pickup**: This button will go into your inventory, and check each selected Pokémon for if they have items, then return to the overworld screen.
2. **Record Route**: This will start a listener for the arrow keys, allowing you to record your route through the patch of tall grass. When recording, try to leave half a second in between keypresses and don't run at all, as the listener can **only** record arrow keys.  **Press esc to stop recording** the route.
3. **Run Route**: This will run the route that you have recorded, make sure your game is **full screen** so the bot can detect if you are entering a battle or not. After each battle, the bot will check for items collected by Pokémon. Before running the route, **make sure you record a path to the poke center**.
4. **Show Route**: This button will simply show you the currently saved route: the direction you're  going in and for how long. This is good to make sure you have recorded a route, and that it is going to the right place.
5. **Clear Route**: This button deletes the current route, allowing you to re-record it until it's just right.
6. **Poke Center**: This button runs the current route to the poke center. Again, make sure to be **full screen** so that the bot can detect that you're in battle.
7. **Poke Route**: This button allows you to record your route from the current route to the Pokémon Center. To do this in the best way possible follow these tips:
   1. Start recording from the end of the route. This way the bot will never come up short while returning to heal.
   2. Leave about a half second delay between key presses. This process is single threaded, and therefore it can take some time for the bot to record the current route. 
   3. **You press esc once you are able to talk to Nurse Joy**. The bot can handle the talking to her, as well as walking back to the original spot to maintain consistency. 
8. **Clear Poke Route**: This button runs will clear the current route to the poke center. This is useful if the bot is off by an inch or a mile from the poke center, and allows the user to re-record the route without restarting the bot.
9. **Slot Checkboxes**: These checkboxes allow you to choose which slots you currently have a pickup Pokémon in.
10. **HM Checkboxes**: These checkboxes allow you to tell the bot whether a pickup Pokémon has an HM move or not.

To exit the bot, you can just press the escape button.



## Some Notes on the Bot

As of now, you have to record your route in the grass as well as to the Pokémon center every time you activate it, in the future, this will be changed to save a local file with your pre-recorded routes.

Always press escape to end the recording of the current route. Minute keypresses can be exaggerated by the bot, so try to only record long held keypresses.

The bot cannot record anything but direction keys and if you press the escape button. **If you get into battle while recording, use your mouse to fight or run.**



## Libraries Used for this Project

I have made extensive use of the following:

[PyQt5](https://riverbankcomputing.com/software/pyqt/intro): Provides an extensive GUI framework, allowing the user easy interaction with the bot.

[PyWin32](https://github.com/mhammond/pywin32): Allows me to more easily record keypresses as well as transmit them to windows for action input in Citra.

[Pynput](https://pypi.org/project/pynput/): Allowing me to monitor the keyboard, listening for arrow keys and the escape button.

[Pyscreenshot](https://pypi.org/project/pyscreenshot/): Allowing me to detect when a user enters a battle.



## Current State and Future Development

This project is in development, and is developing towards a 1.0 release. Right now it's at 0.8, as there are some features I would like to add to make this bot fully functional.

Future Requirements include the following, sorted by priority:

1. A button to exit the bot's current route and allow the user full control
2. A button to clear the current poke_route  (*added*)
3. QSS styling, giving the GUI a better look 
4. The ability to check if the bot is stuck and needs to be moved
5. Input from users as to what they'd like to see added

