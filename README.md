# Toutatis
👋 Hi there! For any professional inquiries or collaborations, please reach out to me at:
megadose@protonmail.com

📧 Preferably, use your professional email for correspondence. Let's keep it short and sweet, and all in English!

Toutatis is a tool that allows you to extract information from instagrams accounts such as e-mails, phone numbers and more </br>
For BTC Donations : 1FHDM49QfZX6pJmhjLE5tB2K6CaTLMZpXZ
## 💡 Prerequisite
[Python 3](https://www.python.org/downloads/release/python-370/)

## 🛠️ Installation
### With PyPI

```pip install toutatis```

### With Github

```bash
git clone https://github.com/megadose/toutatis.git
cd toutatis/
python3 setup.py install
```

## 📚 Usage:

### Find information from a username

```
# Replace placeholders with real values:
toutatis -u vlad_leonov7 -s <instagramsessionid>
```

> ⚠️ Common mistake: don't swap `-u` and `-s`. If your command looks like `toutatis -u username -s vlad_leonov`, you likely passed the username as the session id by mistake — use `-s <your_sessionid_here>` instead.

### Find information from an Instagram ID

```
toutatis -i instagramID -s instagramsessionid
```

## 📈 Example

```
Informations about     : xxxusernamexxx
Full Name              : xxxusernamesxx | userID : 123456789
Verified               : False | Is buisness Account : False
Is private Account     : False
Follower               : xxx | Following : xxx
Number of posts        : x
Number of tag in posts : x
External url           : http://example.com
IGTV posts             : x
Biography              : example biography
Public Email           : public@example.com
Public Phone           : +00 0 00 00 00 00
Obfuscated email       : me********s@examplemail.com
Obfuscated phone       : +00 0xx xxx xx 00
------------------------
Profile Picture        : https://scontent-X-X.cdninstagram.com/
```

## 📚 To retrieve the sessionID
Follow these steps in your browser (must be logged in to Instagram):
1. Open Instagram and sign in.
2. Open Developer Tools (F12) → Application (Chrome) or Storage (Firefox).
3. Under Cookies, select `https://www.instagram.com`, find the `sessionid` cookie and copy its value.
4. Keep it private — it grants access to your logged-in session.

![](https://files.catbox.moe/1rfi6j.png)

## Thank you to :

- [EyupErgin](https://github.com/eyupergin)
- [yazeed44](https://github.com/yazeed44)
