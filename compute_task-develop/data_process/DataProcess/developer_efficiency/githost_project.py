import sys
#Python urllib 库用于操作网页 URL，并对网页的内容进行抓取处理
if sys.version_info < (3, 0):
    import urllib
else:
    from urllib.request import urlopen

import json


class GithostInfo(object):
    def __init__(self, url_addr, token):
        self.url_addr = url_addr
        self.token = token

    def project_list(self):
        for index in range(100):
            url = "https://%s/api/v4/projects?private_token=%s&per_page=100&page=%d&order_by=name" % (
                self.url_addr, self.token, index)
            print(url)

            if sys.version_info < (3, 0):
                all_projects = urllib.urlopen(url)
            else:
                all_projects = urlopen(url)

            all_projects_dict = json.loads(all_projects.read().decode(encoding='UTF-8'))
            if len(all_projects_dict) == 0:
                break
            for thisProject in all_projects_dict:
                try:
                    this_project_url = thisProject['ssh_url_to_repo']
                    this_project_path = thisProject['path_with_namespace']
                    print(this_project_url + ' ' + this_project_path)
                except Exception as e:
                    print("Error on %s: %s" % (this_project_url, e.strerror))


def all_projects_info():
    githost_info = GithostInfo('githost.nevint.com', 'glpat-rhUXbtzqfyKb_Gh-rmCL')
    githost_info.project_list()


if __name__ == '__main__':
    all_projects_info()
