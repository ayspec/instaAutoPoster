import os, random, json, requests, threading
from InstagramAPI import InstagramAPI
from time import sleep, time
from requests_toolbelt import MultipartEncoder

class InstagramAPIedit(InstagramAPI):
    def uploadPhoto(self, photo, caption=None, upload_id=None, is_sidecar=None):
	    if upload_id is None:
		    upload_id = str(int(time() * 1000))
	    data = {'upload_id': upload_id,
		        '_uuid': self.uuid,
		        '_csrftoken': self.token,
		        'image_compression': '{"lib_name":"jt","lib_version":"1.3.0","quality":"87"}',
		        'photo': ('pending_media_%s.jpg' % upload_id, open(photo, 'rb'), 'application/octet-stream', {'Content-Transfer-Encoding': 'binary'})}
	    if is_sidecar:
		    data['is_sidecar'] = '1'
	    m = MultipartEncoder(data, boundary=self.uuid)
	    self.s.headers.update({'X-IG-Capabilities': '3Q4=',
		                       'X-IG-Connection-Type': 'WIFI',
		                       'Cookie2': '$Version=1',
		                       'Accept-Language': 'en-US',
		                       'Accept-Encoding': 'gzip, deflate',
		                       'Content-type': m.content_type,
		                       'Connection': 'close',
		                       'User-Agent': self.USER_AGENT})
	    response = self.s.post(self.API_URL + "upload/photo/", data=m.to_string())
	    if response.status_code == 200:
	    	if self.configure(upload_id, photo, caption):
	    		mjs = self.LastJson
	    		self.expose()
	    		return mjs
	    return False

def dumpConfig():
    filename = "config.json"
    if filename:
        with open(filename, 'r') as f:
            cfg = json.load(f)
    return cfg

def getUsername():
    cfg = dumpConfig()
    igUsername = cfg['username']
    return igUsername

def getPassword():
    cfg = dumpConfig()
    igPassword = cfg['password']
    return igPassword

def getInterval():
    cfg = dumpConfig()
    interval = cfg['interval']
    return interval

def getCaption():
    cfg = dumpConfig()
    caption = cfg['caption']
    return caption

def loginInsta(username, password):
    insta_api = InstagramAPIedit(username, password)
    if (insta_api.login()):
    	print("Logged to Instagram successfully")
    else:
    	print("ERROR: Failed to login to Instagram, please make sure you've used the correct username and password and that the connection is not faulty as well.")
    return insta_api

def postPhoto(interval, caption, insta_api):
    threading.Timer(interval, postPhoto).start()
    randPhoto = random.choice(os.listdir("photos"))
    randPhoto = "photos/" + randPhoto
    post = insta_api.uploadPhoto(randPhoto, caption=caption)
    if post:
        print("posted photo")
    else:
        print("post failed")
    os.remove(randPhoto)
    print("deleted " + randPhoto)

def main():

    username = getUsername()
    password = getPassword()
    interval = getInterval()
    caption = getCaption()

    insta_api = loginInsta(username, password)
    postPhoto(interval, caption, insta_api)

if __name__ == "__main__":
    main()