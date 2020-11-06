import json


class SpooderPipeline(object):

    def process_item(self, item, spider):
        # get category and use it as filename
        filename = 'names.json'

        with open(filename, 'w') as f:
            json.dump(item, f)
