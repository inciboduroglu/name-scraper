import csv
import os.path


class SpooderPipeline(object):

    def process_item(self, item, spider):
        field_names = ['name', 'usage', 'gender', 'related-names']

        # get category and use it as filename
        page_name = item["page_name"]
        filename = f'{page_name}.csv'

        # check if file has been created before. if yes; create, and add headers
        if not os.path.isfile(filename):
            with open(filename, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=field_names)
                writer.writeheader()

        del item["page_name"]

        with open(filename, 'a', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=field_names)
            # writer.writeheader()
            writer.writerow(item)
