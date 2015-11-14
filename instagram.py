from instagram.client import InstagramAPI

'needs pip install python-instagram'

CID = '1500207b59d34a87a53120d33e56c041'
CIDS = '41ede89cba7e44ecb604fce95f444672'


con = InstagramAPI(client_id = CID, client_secret = CIDS)

NYCtag = c.tag_search("NYC")

for tag in NYCtag:
    print tag.images['standard_resolution'].url
