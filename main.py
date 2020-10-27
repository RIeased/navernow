import xbmc, xbmcgui, os, xbmcaddon, xbmcplugin, requests

def main():
    __settings__ = xbmcaddon.Addon()
    home = __settings__.getAddonInfo('path')
    addon_handle = int(sys.argv[1])
    icon = xbmc.translatePath(os.path.join(home, 'icon.png'))

    livePageUrl = "http://now.naver.com/api/nnow/v1/stream/livelist"
    request = requests.get(url=livePageUrl).json()

    try:

        data = request["liveList"]
        num = len(data)

        for f in range(0, num):
            count = f
            c = data[count]

            if c["status"] == 'ONAIR':
                b = c["contentId"]

                url1 = "https://now.naver.com/api/nnow/v1/stream/" + b + "/livestatus"
                g = requests.get(url1).json()

                if g["status"]["videoStreamUrl"] == "":
                    naverlive = g["status"]["liveStreamUrl"]

                else:
                    naverlive = g["status"]["videoStreamUrl"]

                try:
                    url2 = "https://now.naver.com/api/nnow/v1/stream/" + b + "/content/"
                    h = requests.get(url2).json()
                    content = h["contentList"]

                    for ct in content:
                        tit = ct["playlist"]["title"]
                        nt = ct["home"]["image"]["url"]

                        li = xbmcgui.ListItem(tit)
                        li.setThumbnailImage(nt)
                        xbmcplugin.addDirectoryItem(handle=addon_handle, url=naverlive, listitem=li, isFolder=False)

                except ValueError:
                    pass

    except ValueError:
        pass

    xbmcplugin.endOfDirectory(addon_handle)

if __name__ == '__main__':
    main()
