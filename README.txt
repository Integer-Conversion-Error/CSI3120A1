Esad Kaya 300283659
Wesley Maya 300244659

Some ideas lightly inspired by GeeksForGeeks and W3Schools, as well as a conversation with Professor Karim in front of CBY. Switching the idea to top-down to at least get something over the line was thanks to him, I doubt we could have managed to get bottom-up working anything close to this by now.

A1.py is the main file. Other python files are simply crude testing environments.
The assignment works for the most part. It can accurately parse all valid strings correctly, but due to our original approach of (unknowingly) making the parser work bottom-up, we lost valuable time and thus our strategy change happened late. This meant our top down parser is still rough around the edges, with a lot of nasty recursive-related behaviours being tip-toed around. Some invalid cases still do get parsed as if they are "valid", mostly due to the ambiguity with the rules. While we tried to redefine the rules to prevent this, unfortunately we were not completely successful in eliminating all unwanted behaviour. Some are handled outside the functions, as said before. The parse tree also works, though sometimes it encounters unwanted behaviour with not going down a level on an open bracket. This is simply bypassed by moving along (incrementing "index").

Overall, our top down parser was a very eye-opening task, and we feel confident that we have the necessary experience to dust ourselves off and go all the way next time.