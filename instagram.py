from instagram.client import InstagramAPI

'needs pip install python-instagram'

CID = 'd1ea621e34594ddba981f42614d8b0fc'
CIDS = '3ebafbbe4b224811b18d6823f89fba3e'


con = InstagramAPI(client_id = CID, client_secret = CIDS)

NYCtag = c.tag_search("NYC")

for tag in NYCtag:
    print tag.images['standard_resolution'].url
